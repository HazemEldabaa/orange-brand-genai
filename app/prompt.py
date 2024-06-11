import streamlit as st
from prompt_utils import send_prompt

prompt = st.text_input("Enter your prompt here:")
generate_button = st.button("Generate Image")
url = st.text_input("Enter your link here:")
json_url = st.text_input("Enter your json link here:")

if generate_button:
    if url and json_url and prompt:
        dictionary = send_prompt(url, prompt, json_url) 
    for key, value in dictionary.items():
        if key == 'image':
            st.image(value, caption='Generated Image')
        else:
            st.write(value)
