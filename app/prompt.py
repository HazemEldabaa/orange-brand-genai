import streamlit as st
from prompt_utils import send_prompt

PAGE_TITLE = "Prompt"
PAGE_ICON = ":orange_heart:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

prompt = st.text_input("Enter your prompt here:")
generate_button = st.button("Generate Image")
headless = st.checkbox("Headless Mode", value=False)

url = "https://56fa32efe8bd3d139e.gradio.live/"
json_link = "https://56fa32efe8bd3d139e.gradio.live/file=/content/drive/MyDrive/Fooocus/outputs/2024-06-14/log.html"

st.write(f'Here is the link to the Gradio app: {url}')

if generate_button:
    if prompt:
        with st.spinner('Generating image...'):
            dictionary = send_prompt(url, prompt, json_link, headless=headless)
        if dictionary:
            for key, value in dictionary.items():
                if key == 'image':
                    st.image(value, caption='Generated Image')
                else:
                    st.write(value)
        else:
            st.write("Failed to generate image. Please try again.")
    else:
        st.write("Please enter a prompt.")
