import streamlit as st
import  streamlit.components.v1 as components
import os
from bs4 import BeautifulSoup

st.set_page_config(page_title="Select your Ad", page_icon=":camera:", layout="wide")
def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    images_data = []

    # Iterate through each image container
    for container in soup.select('.image-container'):
        # Extract image name
        image_name = container.find('img')['src']
       # image_path = os.path.join('extracted', os.path.basename(image_name)).replace("\\", "/")
        image_url = f'extracted/Jean/{os.path.basename(image_name)}'

        # Extract key:value pairs
        metadata = {}
        for row in container.select('table.metadata tr'):
            label = row.find('td', class_='label').text.strip()
            value = row.find('td', class_='value').text.strip()
            metadata[label] = value
        
        # Add the image name to the metadata
        metadata['Image Name'] = image_name
        
        images_data.append((metadata, image_url))
    
    return images_data

# Specify the path to the HTML file
file_path = 'app/frontend/public/extracted/Jean/log.html'

# Parse the HTML file and get the metadata
images_data = parse_html_file(file_path)
st.markdown ('## :camera: :orange[Select your Ad]')
imageCarouselComponent = components.declare_component('image-carousel-component', path='app/frontend/public')
# imageUrls = ['extracted/2024-06-04/2024-06-04_09-25-28_6602.png',
#              'extracted/2024-06-04/2024-06-04_09-26-35_5259.png',
#              'https://api.wandb.ai/files/becode/image-generation/2ytn0xms/media/images/generated_image_0_00e9665fceb7356a1e0f.png'
#              ]
imageUrls = [img[1] for img in images_data]
selectedImageUrl = imageCarouselComponent(imageUrls=imageUrls, height=300)
if selectedImageUrl is not None:
    for metadata, image_path in images_data:
        col1, col2 = st.columns([1.5,1.5])
        col3, col4 = st.columns([3,1.5])
        if selectedImageUrl.endswith(os.path.basename(image_path)):
            if metadata['Resolution'] == '(1152, 896)':

                with col3:
                    st.image(selectedImageUrl, use_column_width=True)

                with col4:
                    #for metadata, image_path in images_data:
                        if selectedImageUrl.endswith(os.path.basename(image_path)):
                            st.markdown("### :orange[Prompt:]")
                            st.markdown(f'###### {metadata["Prompt"]}')
                            st.markdown("### :orange[Base Model:]")
                            st.markdown(f'###### {metadata["Base Model"]}')
                            if metadata['Refiner Model']:
                                st.markdown("### :orange[Refiner:]")
                                st.markdown(f'###### {metadata["Refiner Model"]}')
                            st.markdown("### :orange[LoRA 1:]")
                            st.markdown(f'###### {metadata["LoRA 1"]}')
                            if metadata['LoRA 2']:
                                st.markdown("### :orange[LoRA 2:]")
                                st.markdown(f'###### {metadata["LoRA 2"]}')
                            
                with st.expander("Show All Parameters:", expanded=False):
                    st.json(metadata)
                            

            else:
                with col1:
                    st.image(selectedImageUrl, use_column_width=True)

                with col2:
                    for metadata, image_path in images_data:
                        if selectedImageUrl.endswith(os.path.basename(image_path)):
                            st.write('')
                            st.markdown("## :orange[Prompt:]")
                            st.markdown(f'##### {metadata["Prompt"]}')
                            st.markdown("## :orange[Base Model:]")
                            st.markdown(f'##### {metadata["Base Model"]}')
                            if metadata['Refiner Model']:
                                st.markdown("### :orange[Refiner:]")
                                st.markdown(f'###### {metadata["Refiner Model"]}')
                            st.markdown("## :orange[LoRA 1:]")
                            st.markdown(f'##### {metadata["LoRA 1"]}')
                            if metadata['LoRA 2']:
                                st.markdown("## :orange[LoRA 2:]")   
                                st.markdown(f'##### {metadata["LoRA 2"]}')                         

                            break
                with st.expander("Show All Parameters:", expanded=False):
                    st.json(metadata)