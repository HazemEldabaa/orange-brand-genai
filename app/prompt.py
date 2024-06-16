import streamlit as st
from prompt_utils import send_prompt

PAGE_TITLE = "Prompt"
PAGE_ICON = ":orange_heart:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON)

prompt = st.text_input("Enter your prompt here:")
generate_button = st.button("Generate Image")

url = "https://dd6177cb29becbbd74.gradio.live/"
json_link = "https://dd6177cb29becbbd74.gradio.live/file=/content/drive/MyDrive/Fooocus/outputs/2024-06-15/log.html"

st.write(f'Here is the link to the Gradio app: {url}')

if generate_button:
    if prompt:
        with st.spinner('Generating image...'):
            result = send_prompt(url, prompt, json_link, headless=True)
        if result:
            if "error" in result:
                st.error(f"Error: {result['error']}")
            else:
                for key, value in result.items():
                    if key == 'image':
                        st.image(value, caption='Generated Image')
                    else:
                        st.write(value)
        else:
            st.error("Failed to generate image. Please try again.")
    else:
        st.error("Please enter a prompt.")
