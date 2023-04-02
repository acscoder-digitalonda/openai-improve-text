import streamlit as st
import summarizer as sm

st.title('OpenAI API Demonstration')
st.write('Enter your google document URL ex: https://docs.google.com/document/d/1FKq0wnRDkCES6PwGKZh0p-DeoZUjUd0VLfwsdxcBlkk/edit.')
st.write('Make sure you shared that document with acscoder@digitalonda.com or public for everyone can read.')
          
url = st.text_input('Enter your google docs URL')
if st.button('Submit'):
    with st.spinner('Please wait for the result...'):
        rep = sm.run_doc(url)
        st.write('Here is your result: ', rep)