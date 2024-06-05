import streamlit as st
import os
import sqlite3
from datetime import datetime

# Database setup

def init_db():
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    c.execute('''
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY,
            image_index INTEGER,
            image_side TEXT,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def log_click(image_index, image_side):
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO clicks (image_index, image_side)
        VALUES (?, ?)
    ''', (image_index, image_side))

    c.execute("SELECT * FROM sqlite_master;")
    data = c.fetchall()
    st.write(data)
    conn.commit()
    conn.close()

# Function to display the main page
def completion():
    st.write('Thank you for completing the survey')

def main_page(min_index, max_index):
    st.title('Image Classification')

    # Create two columns
    col1, col2 = st.columns(2)
    image_path = "/Users/markshevchenkopu/Desktop/my_projects/becode_projects/blind_test/images"
    images = os.listdir(image_path)

    try:
        for index in range(min_index, max_index):
            with col1:
                st.image(os.path.join(image_path, images[index]), width=200, caption=f"Image {index+1}")
                if st.button("I'am AI generated", key=f"image1_{index}"):
                    st.session_state['image_clicked'] = 1
                    log_click(index, 'left')
                    st.experimental_rerun()

            with col2:
                st.image(os.path.join(image_path, images[index + 1]), width=200, caption=f"Image {index+2}")
                if st.button("I'am AI generated", key=f"image2_{index}"):
                    st.session_state['image_clicked'] = 2
                    log_click(index + 1, 'right')
                    st.experimental_rerun()
                    
    except IndexError:
        completion()

# Initialize indices
if 'min_index' not in st.session_state:
    st.session_state['min_index'] = 0
if 'max_index' not in st.session_state:
    st.session_state['max_index'] = 1

# Initialize user_id


# Initialize database
init_db()

# Check which page to display
if 'image_clicked' in st.session_state:
    st.session_state['min_index'] += 2
    st.session_state['max_index'] += 2
    del st.session_state['image_clicked']
    st.experimental_rerun()
else:
    main_page(st.session_state['min_index'], st.session_state['max_index'])

st.sidebar.title("Statistics")
if st.button("Show Click Stats"):
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    c.execute('SELECT image_side, COUNT(*) FROM clicks GROUP BY image_side')
    stats = c.fetchall()
    conn.close()
    for stat in stats:
        st.sidebar.write(f"{stat[0]} Clicks: {stat[1]}")
