import streamlit as st
from prompt_utils import send_prompt

prompt = st.text_input("Enter your prompt here:")
generate_button = st.button("Generate Image")

url = "###put a link of gradio here"
json_link = "###put a json link here"

if generate_button:
    if prompt:
        dictionary = send_prompt(url,prompt, json_link) 
    for key, value in dictionary.items():
        if key == 'image':
            st.image(value, caption='Generated Image')
        else:
            st.write(value)
    else:
        st.write("Please enter a prompt.")