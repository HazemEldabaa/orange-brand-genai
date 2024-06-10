import streamlit as st
import os
import sqlite3
import random
# Database setup
def init_db():
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY,
            image_index INTEGER,
            image_side TEXT,
            correct BOOLEAN,
            incorrect BOOLEAN,
            like BOOLEAN,
            dislike BOOLEAN,
            timestamp DATETIME DEFAULT CURRENT_TIMESTAMP
        )
    ''')
    
    conn.commit()
    conn.close()

def log_click(image_index, image_side, correct, incorrect, like, dislike):
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO clicks (image_index, image_side, correct, incorrect, like, dislike)
        VALUES (?, ?, ?, ?, ?, ?)
    ''', (image_index, image_side, correct, incorrect, like, dislike))
    
    conn.commit()
    
    c.execute('''
        SELECT 
            SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
            SUM(CASE WHEN incorrect THEN 1 ELSE 0 END) as incorrect_count,
            SUM(CASE WHEN like THEN 1 ELSE 0 END) as like_count,
            SUM(CASE WHEN dislike THEN 1 ELSE 0 END) as dislike_count,
            COUNT(*) as total_count
        FROM clicks
    ''')
    stats = c.fetchone()
    conn.close()
    
    if stats[4] > 0:
        correct_percentage = (stats[0] / (stats[0]+stats[1])) * 100
        incorrect_percentage = (stats[1] / (stats[0]+stats[1])) * 100
        like_percentage = (stats[2] / stats[4]) * 100
        dislike_percentage = (stats[3] / stats[4]) * 100
    else:
        correct_percentage = 0
        incorrect_percentage = 0
        like_percentage = 0
        dislike_percentage = 0
    
    return correct, correct_percentage if correct else incorrect_percentage, like_percentage, dislike_percentage

def completion():
    st.markdown('## :orange[Thank you for completing the survey]')

def main_page(min_index, max_index):
    st.markdown('<h1 style="text-align: center; color: orange;">🟧 Blind Test</h1>', unsafe_allow_html=True)

    # Create three columns
    col1, col2, col3 = st.columns([1, 1.5, 1])
    image_path = "app/images/"
    images = sorted(os.listdir(image_path))  # Ensure images are sorted
    random.shuffle(images)
    # Adjust max_index to ensure it doesn't exceed the length of the images list
    max_index = min(max_index, len(images))

    if min_index >= max_index:
        completion()
        return

    for index in range(min_index, max_index, 2):
        image_name = images[index]
        image_label = "positive" if "positive_" in image_name else "negative"

        with col1:
            st.write("\n" * 25)  
            st.markdown("#### Real or AI?")

            if st.button("I'm 100% real bro!", key=f"real_{index}"):
                correct = image_label == "positive"
                incorrect = not correct
                correct_or_incorrect, percentage, like_percentage, dislike_percentage = log_click(index, "right", correct, incorrect, None, None)
                #st.session_state[f'real_message_{index}'] = (correct_or_incorrect, percentage)
                if correct:
                    st.success(f"Correct! {percentage:.0f}% of others guessed correctly.")
                else:
                    st.error(f"Incorrect! {percentage:.0f}% of others guessed incorrectly.")
            if st.button("Definitely AI made!", key=f"not_human_{index}"):
                correct = image_label == "negative"
                incorrect = not correct
                correct_or_incorrect, percentage, like_percentage, dislike_percentage = log_click(index, "right", correct, incorrect, None, None)
                #st.session_state[f'not_human_message_{index}'] = (correct_or_incorrect, percentage)
                if correct:
                    st.success(f"Correct! {percentage:.0f}% of others guessed correctly.")
                else:
                    st.error(f"Incorrect! {percentage:.0f}% of others guessed incorrectly.")
                                 

        with col2:
            st.image(os.path.join(image_path, image_name), use_column_width=True, caption=f"Image {index+1}")

        with col3:
            st.write("\n" * 25)  # Create vertical space for alignment
            st.markdown("#### Like this image?")
            col6, col7 = st.columns([1, 1])
            with col6:
                if st.button("👍", key=f"like_{index}"):
                    correct, correct_percentage, like_percentage, dislike_percentage = log_click(index, "left", None, None, True, False)
                    st.session_state[f'like_message_{index}'] = f"Liked! {like_percentage:.2f}% of others liked this image."
            with col7:
                if st.button("👎", key=f"dislike_{index}"):
                    correct, correct_percentage, like_percentage, dislike_percentage = log_click(index, "left", None, None, False, True)
                    st.session_state[f'dislike_message_{index}'] = f"Disliked! {dislike_percentage:.2f}% of others disliked this image."
            if f'like_message_{index}' in st.session_state:
                st.success(st.session_state[f'like_message_{index}'])
                del st.session_state[f'like_message_{index}']

            if f'dislike_message_{index}' in st.session_state:
                st.error(st.session_state[f'dislike_message_{index}'])
                del st.session_state[f'dislike_message_{index}']    
            if st.button("Show Click Stats", key=f"stats_{index}"):
                st.sidebar.title("Click Statistics")
                conn = sqlite3.connect('user_clicks.db')
                c = conn.cursor()
                c.execute('''
                    SELECT 
                        SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
                        SUM(CASE WHEN incorrect THEN 1 ELSE 0 END) as incorrect_count,
                        SUM(CASE WHEN like THEN 1 ELSE 0 END) as like_count,
                        SUM(CASE WHEN dislike THEN 1 ELSE 0 END) as dislike_count,
                        COUNT(*) as total_count
                    FROM clicks
                ''')
                stats = c.fetchone()
                conn.close()
                st.sidebar.write(f"Correct Clicks: {(stats[0]/(stats[0]+stats[1])*100):.0f}%")
                st.sidebar.write(f"Incorrect Clicks: {(stats[1]/(stats[0]+stats[1])*100):.0f}%")
                # st.sidebar.write(f"Clicks: {stats[0]},{stats[1]}")
                # st.sidebar.write(f"Like Clicks: {stats[2]}")
                # st.sidebar.write(f"Dislike Clicks: {stats[3]}")
                # st.sidebar.write(f"stats: {stats[4]}")
            if st.button("Next Image"):
                st.session_state['min_index'] += 2
                st.session_state['max_index'] += 2
                st.rerun()              

        # Display messages if available in the session state
        if f'like_message_{index}' in st.session_state:
            st.success(st.session_state[f'like_message_{index}'])
            del st.session_state[f'like_message_{index}']

        if f'dislike_message_{index}' in st.session_state:
            st.error(st.session_state[f'dislike_message_{index}'])
            del st.session_state[f'dislike_message_{index}']

        # if f'real_message_{index}' in st.session_state:
        #     correct_or_incorrect, percentage = st.session_state[f'real_message_{index}']
        #     if correct_or_incorrect:
        #         st.success(f"Correct! {percentage:.0f}% of others guessed correctly.")
        #     else:
        #         st.error(f"Incorrect! {percentage:.0f}% of others guessed incorrectly.")
        #     del st.session_state[f'real_message_{index}']

        # if f'not_human_message_{index}' in st.session_state:
        #     correct_or_incorrect, percentage = st.session_state[f'not_human_message_{index}']
        #     if correct_or_incorrect:
        #         st.success(f"Correct! {percentage:.0f}% of others guessed correctly.")
        #     else:
        #         st.error(f"Incorrect! {percentage:.0f}% of others guessed incorrectly.")
        #     del st.session_state[f'not_human_message_{index}']

# Initialize indices
if 'min_index' not in st.session_state:
    st.session_state['min_index'] = 0
if 'max_index' not in st.session_state:
    st.session_state['max_index'] = 1

# Initialize database
init_db()

# Display the main page
main_page(st.session_state['min_index'], st.session_state['max_index'])
