import streamlit as st

PAGE_TITLE = "Orange Advice app"
PAGE_ICON = ":orange_heart:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# Thin divider line
horizontal_bar = "<hr style='margin-top: 0; margin-bottom: 0; height: 1px; \
                        border: 1px solid #2b2a29;'><br>"

# Define the content of the Home page

# Display logo in sidebar
st.markdown(
    """
    <style>
        [data-testid=stSidebar] [data-testid=stImage]{
            text-align: center;
            color: black;
            display: block;
            margin-left: auto;
            margin-right: auto;
            width: 100%;
        }
        [data-testid="stSidebar"] {
        color: black; 
        }
    </style>
    """, unsafe_allow_html=True
)

with st.sidebar:
    st.image("imgs/orange_mail.png", width=150)


# Display header image and title
st.image("imgs/orange_people.png", use_column_width="always")
st.title("Team contacts")
st.markdown(horizontal_bar, True)

st.markdown(
    """    
        **Jean Duffy**: 
            https://github.com/jduffy93
        
        **Maarten Knaepen**: 
            https://github.com/MaartenKnaepen
        
        **Mark Shevchenko**: 
            https://github.com/pr0fi7
        
        **Polina Yarova**: 
            https://github.com/polinaya777
        
        **Sylvain Legay**: 
            https://github.com/slvg01
                        
"""
)

# Display footer
footer = """
    <style>    
    .footer {
    position: fixed;
    left: 0;
    bottom: 0;
    width: 100%;
    background-color: #FF6600;
    color: white;
    text-align: center;
    padding: 10px;
    }
    </style>
    <div class="footer">
        Developed with  ❤
    </div>
"""
st.markdown(footer, unsafe_allow_html=True)