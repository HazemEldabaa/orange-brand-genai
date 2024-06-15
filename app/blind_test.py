import streamlit as st
import os
import sqlite3
import random
import time
from datetime import datetime, timedelta
PAGE_TITLE = "Blind Test"
PAGE_ICON = ":orange_heart:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# Database setup
def init_db():
    conn = sqlite3.connect('user_clicks.db')
    c = conn.cursor()
    
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
    
    c.execute('''
        SELECT 
            image_side,
            SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
            SUM(CASE WHEN incorrect THEN 1 ELSE 0 END) as incorrect_count,
            COUNT(*) as total_count
        FROM clicks
        WHERE user_id = ?
        GROUP BY image_side
    ''', (user_id,))
    user_stats = c.fetchall()
    
    c.execute('''
        SELECT 
            image_side,
            SUM(CASE WHEN correct THEN 1 ELSE 0 END) as correct_count,
            SUM(CASE WHEN incorrect THEN 1 ELSE 0 END) as incorrect_count,
            COUNT(*) as total_count
        FROM clicks
        GROUP BY image_side
    ''')
    global_stats = c.fetchall()
    
    conn.close()
    
    return user_stats, global_stats

def show_statistics(user_id):
    user_stats, global_stats = get_statistics(user_id)
    
    st.markdown('## :orange[Survey Completed]')
    
    user_summary = {'ai': [0, 0, 0], 'real': [0, 0, 0], 'all': [0, 0, 0]}
    global_summary = {'ai': [0, 0, 0], 'real': [0, 0, 0], 'all': [0, 0, 0]}
    
    for row in user_stats:
        image_side, correct_count, incorrect_count, total_count = row
        user_summary[image_side] = [correct_count, incorrect_count, total_count]
        user_summary['all'][0] += correct_count
        user_summary['all'][1] += incorrect_count
        user_summary['all'][2] += total_count
    
    for row in global_stats:
        image_side, correct_count, incorrect_count, total_count = row
        global_summary[image_side] = [correct_count, incorrect_count, total_count]
        global_summary['all'][0] += correct_count
        global_summary['all'][1] += incorrect_count
        global_summary['all'][2] += total_count

    def calculate_percentage(correct, total):
        return (correct / total * 100) if total > 0 else 0

    col9, col10 = st.columns([1, 1])
    with col9:
        st.write("### Your Statistics")
        for image_type in ['ai', 'real', 'all']:
            correct_percentage = calculate_percentage(user_summary[image_type][0], user_summary[image_type][2])
            st.write(f"{image_type.capitalize()} Images - You Guessed {correct_percentage:.0f}% Correctly")
            st.write(f"Total responses: {user_summary[image_type][2]}")
            st.write("---")
    with col10:
        st.write("### Global Statistics")
        for image_type in ['ai', 'real', 'all']:
            correct_percentage = calculate_percentage(global_summary[image_type][0], global_summary[image_type][2])
            st.write(f"{image_type.capitalize()} Images - Others Guessed {correct_percentage:.0f}% Correctly")
            st.write(f"Total responses: {global_summary[image_type][2]}")
            st.write("---")

def main_page(user_id, min_index, images):
    st.markdown('<h1 style="text-align: center; color: orange;">🟧 Blind Test</h1>', unsafe_allow_html=True)

    if 'displayed_images' not in st.session_state:
        st.session_state['displayed_images'] = []

    if 'ai_or_real' not in st.session_state:
        st.session_state['ai_or_real'] = None

    col1, col2, col3 = st.columns([1, 1.5, 1])
    # bannertop = st.empty()
    # bannerdown = st.empty()

    try:
        index = min_index
        image_name = images[index]
        image_label = "positive" if "positive" in image_name else "negative"
        st.session_state['displayed_images'].append(image_name)
        image_index = len(st.session_state['displayed_images'])

        
        with col1:
            st.write("\n" * 25)
            st.markdown("#### Real or AI?")

            if st.session_state['ai_or_real'] is None:
                st.session_state['ai_or_real'] = 'real' if image_label == "positive" else 'ai'
            ai_or_real = st.session_state['ai_or_real']


            if st.button("100% real, bro !", key=f"real_{index}"):
                correct = ai_or_real == "real"
                incorrect = not correct
                id, correct_or_incorrect, percentage, like_percentage, dislike_percentage = log_click(user_id, image_index, ai_or_real, correct, incorrect, None, None)

                if correct:
                    st.success("Correct!")
                else:
                    st.error("Incorrect!")
                st.session_state['image_clicked'] = True
                st.session_state['min_index'] += 1
                st.session_state['ai_or_real'] = None
                time.sleep(1.5)
                st.rerun()

            if st.button("Definitely AI !", key=f"ai_{index}"):
                correct1 = ai_or_real == "ai"
                incorrect1 = not correct1
                
                id, correct_or_incorrect, percentage, like_percentage, dislike_percentage = log_click(user_id, image_index, ai_or_real, correct1, incorrect1, None, None)

                if correct1:
                    with st.empty():
                        st.success("Correct!")
                else:
                    with st.empty():
                        st.error("Incorrect!")
                st.session_state['image_clicked'] = True
                st.session_state['min_index'] += 1
                st.session_state['ai_or_real'] = None
                time.sleep(0.5)
                st.rerun()

        with col2:
            st.image(os.path.join(image_path, images[index]), use_column_width=True, caption=f"Image {index + 1}")

        with col3:

            countdown_placeholder = st.empty()
            start_time = datetime.now()
            end_time = start_time + timedelta(seconds=10)
            while datetime.now() < end_time:
                countdown_placeholder.markdown(f"## :orange[Time left: **{(end_time - datetime.now()).seconds}** seconds]")
                time.sleep(1)
            st.session_state['image_clicked'] = True
            st.session_state['min_index'] += 1
            st.session_state['ai_or_real'] = None
            st.rerun()

            
    except IndexError:
        show_statistics(user_id)
        return

# Initialize session state variables
if 'user_id' not in st.session_state:
    st.session_state['user_id'] = str(random.randint(1000, 9999))

if 'min_index' not in st.session_state:
    st.session_state['min_index'] = 0

# Initialize database
init_db()
image_path = "images/"
if 'images' not in st.session_state:
    images = sorted(os.listdir(image_path))
    random.shuffle(images)
    st.session_state['images'] = images

# Display the main page
main_page(st.session_state['user_id'], st.session_state['min_index'], st.session_state['images'])