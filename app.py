import streamlit as st
from bs4 import BeautifulSoup
import uuid
import os

# Function to read and parse HTML file
def parse_html_file(file_path):
    with open(file_path, 'r', encoding='utf-8') as file:
        html_content = file.read()
    
    # Parse the HTML
    soup = BeautifulSoup(html_content, 'html.parser')
    
    images_data = []

    # Iterate through each image container
    for i, container in enumerate(soup.select('.image-container')):
        # Extract image name
        image_name = container.find('img')['src']
        image_path = f'extracted/2024-06-04/{image_name}'
        
        # Extract key:value pairs
        metadata = {}
        for row in container.select('table.metadata tr'):
            label = row.find('td', class_='label').text
            value = row.find('td', class_='value').text
            metadata[label] = value
        
        # Add the image name to the metadata
        metadata['Image Name'] = image_name
        
        images_data.append((metadata, image_path))
    
    return images_data

# Specify the path to the HTML file
file_path = 'extracted/2024-06-04/log.html'

# Parse the HTML file and get the metadata
images_data = parse_html_file(file_path)

# Streamlit app
st.title("Image Metadata Viewer")

for metadata, image_path in images_data:
    st.header(metadata.get('Image Name'))
    st.image(image_path)
    st.json(metadata)

# Create the app.py file and run it using Streamlit
