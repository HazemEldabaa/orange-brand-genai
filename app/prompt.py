import streamlit as st
from prompt_utils import send_prompt
PAGE_TITLE = "Orange Image GenAI"
PAGE_ICON = ":orange_heart:"
prompt = st.text_input("Enter your prompt here:")
generate_button = st.button("Generate Image")
headless = st.checkbox("Headless Mode", value=False)

url = "https://56fa32efe8bd3d139e.gradio.live/"
json_link = "https://56fa32efe8bd3d139e.gradio.live/file=/content/drive/MyDrive/Fooocus/outputs/2024-06-14/log.html"

st.write(f'Here is the link to the Gradio app: {url}')

if generate_button:
    if prompt:
        dictionary = send_prompt(url,prompt, json_link, headless=headless) 
    for key, value in dictionary.items():
        if key == 'image':
            st.image(value, caption='Generated Image')
        else:
            st.write(value)
    else:
        st.write("Please enter a prompt.")