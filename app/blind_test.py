import streamlit as st
import os
import sqlite3
import random
import time
from datetime import datetime, timedelta

# Database setup
def init_db():
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    
    # Create table if it doesn't exist
    c.execute('''
        CREATE TABLE IF NOT EXISTS clicks (
            id INTEGER PRIMARY KEY,
            user_id TEXT,
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

def log_click(user_id, image_index, image_side, correct, incorrect, like, dislike):
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    c.execute('''
        INSERT INTO clicks (user_id, image_index, image_side, correct, incorrect, like, dislike)
        VALUES (?, ?, ?, ?, ?, ?, ?)
    ''', (user_id, image_index, image_side, correct, incorrect, like, dislike))
    
    conn.commit()
    
    c.execute('''
        SELECT 
            SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
            SUM(CASE WHEN incorrect THEN 1 ELSE 0 END) as incorrect_count
        FROM clicks
    ''')
    global_correct_stats = c.fetchone()
    
    if global_correct_stats[0] + global_correct_stats[1] > 0:
        global_correct_percentage = (global_correct_stats[0] / (global_correct_stats[0] + global_correct_stats[1])) * 100
        global_incorrect_percentage = (global_correct_stats[1] / (global_correct_stats[0] + global_correct_stats[1])) * 100
    else:
        global_correct_percentage = 0
        global_incorrect_percentage = 0

    # Fetch like/dislike stats for the specific image
    c.execute('''
        SELECT 
            SUM(CASE WHEN "like" THEN 1 ELSE 0 END) as like_count,
            SUM(CASE WHEN dislike THEN 1 ELSE 0 END) as dislike_count
        FROM clicks
        WHERE image_index = ?
    ''', (image_index,))
    like_dislike_stats = c.fetchone()
    
    if like_dislike_stats[0] + like_dislike_stats[1] > 0:
        like_percentage = (like_dislike_stats[0] / (like_dislike_stats[0] + like_dislike_stats[1])) * 100
        dislike_percentage = (like_dislike_stats[1] / (like_dislike_stats[0] + like_dislike_stats[1])) * 100
    else:
        like_percentage = 0
        dislike_percentage = 0
    
    conn.close()
    return image_index, correct or incorrect, global_correct_percentage, like_percentage, dislike_percentage

def get_statistics(user_id):
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    
    # User statistics
    c.execute('''
        SELECT 
            SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
            SUM(CASE WHEN incorrect THEN 1 ELSE 0 END) as incorrect_count,
            SUM(CASE WHEN "like" THEN 1 ELSE 0 END) as like_count,
            SUM(CASE WHEN dislike THEN 1 ELSE 0 END) as dislike_count,
            COUNT(*) as total_count
        FROM clicks
        WHERE user_id = ?
    ''', (user_id,))
    user_stats = c.fetchone()
    
    # Global statistics
    c.execute('''
        SELECT 
            SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
            SUM(CASE WHEN incorrect THEN 1 ELSE 0 END) as incorrect_count,
            SUM(CASE WHEN "like" THEN 1 ELSE 0 END) as like_count,
            SUM(CASE WHEN dislike THEN 1 ELSE 0 END) as dislike_count,
            COUNT(*) as total_count
        FROM clicks
    ''')
    global_stats = c.fetchone()
    
    conn.close()
    
    return user_stats, global_stats

def show_statistics(user_id):
    user_stats, global_stats = get_statistics(user_id)
    
    st.markdown('## :orange[Survey Completed]')
    
    if user_stats[4] > 0:
        user_correct_percentage = (user_stats[0] / (user_stats[0] + user_stats[1])) * 100 if (user_stats[0] + user_stats[1]) > 0 else 0
        user_incorrect_percentage = (user_stats[1] / (user_stats[0] + user_stats[1])) * 100 if (user_stats[0] + user_stats[1]) > 0 else 0
    else:
        user_correct_percentage = 0
        user_incorrect_percentage = 0
    
    st.write("### Your Statistics")
    st.write(f"Correct guesses: {user_correct_percentage:.0f}%")
    st.write(f"Incorrect guesses: {user_incorrect_percentage:.0f}%")
    st.write(f"Likes: {user_stats[2]}")
    st.write(f"Dislikes: {user_stats[3]}")
    st.write(f"Total responses: {user_stats[4]}")
    
    if global_stats[4] > 0:
        global_correct_percentage = (global_stats[0] / (global_stats[0] + global_stats[1])) * 100 if (global_stats[0] + global_stats[1]) > 0 else 0
        global_incorrect_percentage = (global_stats[1] / (global_stats[0] + global_stats[1])) * 100 if (global_stats[0] + global_stats[1]) > 0 else 0
    else:
        global_correct_percentage = 0
        global_incorrect_percentage = 0
    
    st.write("### Global Statistics")
    st.write(f"Correct guesses: {global_correct_percentage:.0f}%")
    st.write(f"Incorrect guesses: {global_incorrect_percentage:.0f}%")
    st.write(f"Likes: {global_stats[2]}")
    st.write(f"Dislikes: {global_stats[3]}")
    st.write(f"Total responses: {global_stats[4]}")


def main_page(user_id):
    st.markdown('<h1 style="text-align: center; color: orange;">🟧 Blind Test</h1>', unsafe_allow_html=True)

    if 'displayed_images' not in st.session_state:
        st.session_state['displayed_images'] = []

    col1, col2, col3 = st.columns([1, 1.5, 1])
    image_path = "app/images/"
    images = sorted(os.listdir(image_path))  # Ensure images are sorted
    random.shuffle(images)

    images = [img for img in images if img not in st.session_state['displayed_images']]
    max_index = len(images)

    if max_index == 0:
        show_statistics(user_id)
        return

    image_name = images[0]
    image_label = "positive" if "positive_" in image_name else "negative"
    st.session_state['displayed_images'].append(image_name)
    image_index = len(st.session_state['displayed_images']) - 1

    with col1:
        st.write("\n" * 25)
        st.markdown("#### Real or AI?")

        real_btn = st.button("I'm 100% real bro!")
        ai_btn = st.button("Definitely AI made!")

        if real_btn:
            correct = image_label == "positive"
            incorrect = not correct
            id, correct_or_incorrect, percentage, like_percentage, dislike_percentage = log_click(user_id, image_index, "right", correct, incorrect, None, None)
            if correct:
                st.success(f"Correct! {percentage:.0f}% of others guessed correctly.")
            else:
                st.error(f"Incorrect! {percentage:.0f}% of others guessed incorrectly.")
            st.session_state['next_image'] = True
        if ai_btn:
            correct = image_label == "negative"
            incorrect = not correct
            id, correct_or_incorrect, percentage, like_percentage, dislike_percentage = log_click(user_id, image_index, "right", correct, incorrect, None, None)
            if correct:
                st.success(f"Correct! {percentage:.0f}% of others guessed correctly.")
            else:
                st.error(f"Incorrect! {percentage:.0f}% of others guessed incorrectly.")
            st.session_state['next_image'] = True

    with col2:
        st.image(os.path.join(image_path, image_name), use_column_width=True, caption=f"Image {image_index + 1}")

    with col3:
        st.write("\n" * 25)  # Create vertical space for alignment
        st.markdown("#### Like this image?")
        like_btn = st.button("👍")
        dislike_btn = st.button("👎")
        col6, col7 = st.columns([1, 1])
        with col6:
            if like_btn:
                st.session_state['next_image']=False
                id, correct, correct_percentage, like_percentage, dislike_percentage = log_click(user_id, image_index, "left", None, None, True, False)
                st.session_state[f'like_message_{image_index}'] = f"Liked! {like_percentage:.0f}% of others liked this image."
        with col7:
            if dislike_btn:
                st.session_state['next_image']=False
                id, correct, correct_percentage, like_percentage, dislike_percentage = log_click(user_id, image_index, "left", None, None, False, True)
                st.session_state[f'dislike_message_{image_index}'] = f"Disliked! {dislike_percentage:.0f}% of others disliked this image."
        if f'like_message_{image_index}' in st.session_state:
            st.success(st.session_state[f'like_message_{image_index}'])
            del st.session_state[f'like_message_{image_index}']
            st.session_state['next_image'] = False

        if f'dislike_message_{image_index}' in st.session_state:
            st.error(st.session_state[f'dislike_message_{image_index}'])
            del st.session_state[f'dislike_message_{image_index}']
            st.session_state['next_image'] = False

        # Display countdown timer without blocking
        countdown_placeholder = st.empty()
        start_time = datetime.now()
        end_time = start_time + timedelta(seconds=10)
        while datetime.now() < end_time:
            countdown_placeholder.markdown(f":orange[Time left: **{(end_time - datetime.now()).seconds}** seconds]")
            time.sleep(1)
        st.rerun()
        #st.session_state['next_image'] = True

    if st.session_state.get('next_image'):
        st.session_state['next_image'] = False
        st.experimental_rerun()

# Initialize session state variables
if 'next_image' not in st.session_state:
    st.session_state['next_image'] = False
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(random.randint(1000, 9999))

# Initialize database
init_db()

# Display the main page
main_page(st.session_state['user_id'])
