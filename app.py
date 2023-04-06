import streamlit as st
 
import openai
import os
from time import time,sleep
import textwrap
import re

from gdocs import gdocs

def open_file(filepath):
    with open(filepath, 'r', encoding='utf-8') as infile:
        return infile.read()


openai.api_key =  st.secrets["OPENAI_KEY"]


def save_file(content, filepath):
    with open(filepath, 'w', encoding='utf-8') as outfile:
        outfile.write(content)


def gpt3_completion(prompt, engine='text-davinci-003', temp=0.6, top_p=1.0, tokens=2000, freq_pen=0.25, pres_pen=0.0, stop=['<<END>>']):
    max_retry = 5
    retry = 0
    while True:
        try:
            response = openai.Completion.create(
                engine=engine,
                prompt=prompt,
                temperature=temp,
                max_tokens=tokens,
                top_p=top_p,
                frequency_penalty=freq_pen,
                presence_penalty=pres_pen,
                stop=stop)
            text = response['choices'][0]['text'].strip()
            text = re.sub('\s+', ' ', text)
            filename = '%s_gpt3.txt' % time()
            with open('gpt3_logs/%s' % filename, 'w') as outfile:
                outfile.write('PROMPT:\n\n' + prompt + '\n\n==========\n\nRESPONSE:\n\n' + text)
            return text
        except Exception as oops:
            retry += 1
            if retry >= max_retry:
                return "GPT3 error: %s" % oops
            print('Error communicating with OpenAI:', oops)
            sleep(1)

def run_doc(x,pr,engine='text-davinci-003'):
    creds = gdocs.gdoc_creds()
    document_id = gdocs.extract_document_id(x)
    chunks = gdocs.read_gdoc_content(creds,document_id)
    title = gdocs.read_gdoc_title(creds,document_id)

    new_id = gdocs.create_gdoc(creds,title="OpenAI - " + engine + " - " + title)

    count = 0
    
    for chunk in chunks:
        prompt = pr
        prompt += open_file('prompt.txt').replace('<<SUMMARY>>', chunk)
        prompt = prompt.encode(encoding='ASCII',errors='ignore').decode()
        summary = gpt3_completion(prompt,engine)
        print('\n\n\n', count, 'of', len(chunks), ' - ', summary)
        if count > 0:
            summary = '\n\n' + summary

        gdocs.write_gdoc(creds,new_id,summary)
        count = count + 1

    gdocs.gdoc_set_permission(creds,new_id,"jordan@digitalonda.com")
    gdocs.gdoc_set_permission(creds,new_id,"katie@digitalonda.com")

    return( "https://docs.google.com/document/d/"+new_id+"/edit" ) 
 

st.title('OpenAI API Demonstration')
st.write('Enter your google document URL ex: https://docs.google.com/document/d/1FKq0wnRDES6PwGKZh0p-DeoZUjUd0VLfwsdxcBlkk/edit.')
st.write('Make sure you shared that document with acscoder@digitalonda.com or public for everyone can read.')
          
url = st.text_input('Enter your google docs URL')
prompt = st.text_area('Enter your prompt here')
if st.button('Submit'):
    with st.spinner('Please wait for the result...'):
        rep = run_doc(url,prompt)
        st.write('Here is your result: ', rep)