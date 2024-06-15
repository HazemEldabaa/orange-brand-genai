import streamlit as st
import streamlit.components.v1 as components
import os
from bs4 import BeautifulSoup

PAGE_TITLE = "Orange Image GenAI"
PAGE_ICON = ":orange_heart:"
st.set_page_config(page_title="Select your Ad", page_icon=":camera:", layout="wide")

def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    soup = BeautifulSoup(html_content, 'html.parser')
    
    images_data = []

    for container in soup.select('.image-container'):
        image_name = container.find('img')['src']
        image_url = f'extracted/Jean/{os.path.basename(image_name)}'

        metadata = {}
        for row in container.select('table.metadata tr'):
            label = row.find('td', class_='label').text.strip()
            value = row.find('td', class_='value').text.strip()
            metadata[label] = value
        
        metadata['Image Name'] = image_name
        
        images_data.append((metadata, image_url))
    
    return images_data

file_path = 'app/frontend/public/extracted/Jean/log.html'
images_data = parse_html_file(file_path)

st.markdown('## :camera: :orange[Select your Ad]')
imageCarouselComponent = components.declare_component('image-carousel-component', path='app/frontend/public')

imageUrls = [img[1] for img in images_data]
selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=300)
col1, col2 = st.columns([1.5, 1.5])
col3, col4 = st.columns([3, 1.5])
if selectedImageUrl is not None:
    for metadata, image_path in images_data:

        if selectedImageUrl.endswith(os.path.basename(image_path)):
            if metadata['Resolution'] == '(1152, 896)':
                with col3:
                    st.image(selectedImageUrl, use_column_width=True)

                with col4:
                    if selectedImageUrl.endswith(os.path.basename(image_path)):
                        st.markdown("### :orange[Prompt:]")
                        st.markdown(f'###### {metadata["Prompt"]}')
                        st.markdown("### :orange[Base Model:]")
                        st.markdown(f'###### {metadata["Base Model"]}')
                        if metadata.get('Refiner Model'):
                            st.markdown("### :orange[Refiner:]")
                            st.markdown(f'###### {metadata["Refiner Model"]}')
                        if metadata.get('LoRA 1'):
                            st.markdown("### :orange[LoRA 1:]")
                            st.markdown(f'###### {metadata["LoRA 1"]}')
                        if metadata.get('LoRA 2'):
                            st.markdown("### :orange[LoRA 2:]")
                            st.markdown(f'###### {metadata["LoRA 2"]}')
                            
                with st.expander("Show All Parameters:", expanded=False):
                    st.json(metadata)
            else:
                with col1:
                    st.image(selectedImageUrl, use_column_width=True)

                with col2:
                    if selectedImageUrl.endswith(os.path.basename(image_path)):
                        st.markdown("## :orange[Prompt:]")
                        st.markdown(f'##### {metadata["Prompt"]}')
                        st.markdown("## :orange[Base Model:]")
                        st.markdown(f'##### {metadata["Base Model"]}')
                        if metadata.get('Refiner Model'):
                            st.markdown("### :orange[Refiner:]")
                            st.markdown(f'###### {metadata["Refiner Model"]}')
                        if metadata.get('LoRA 1'):
                            st.markdown("## :orange[LoRA 1:]")
                            st.markdown(f'##### {metadata["LoRA 1"]}')
                        if metadata.get('LoRA 2'):
                            st.markdown("## :orange[LoRA 2:]")
                            st.markdown(f'##### {metadata["LoRA 2"]}')
                        
                with st.expander("Show All Parameters:", expanded=False):
                    st.json(metadata)
