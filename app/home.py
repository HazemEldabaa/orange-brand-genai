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
    st.image("imgs/orange_home.png", width=150)


# Display header image and title
st.image("imgs/orange_header.png", use_column_width="always")
st.title("Welcome to the Orange Advice app! :orange_heart:")
st.markdown(horizontal_bar, True)


col1, spacer, col2 = st.columns([1, 0.05, 1])

with col1:
    st.markdown(
        """
        We have created a prediction ML-based tool allowing to propose upsell or downsell plan to Orange customers.

        **Our app is designed to be reliable and user-friendly:**
        - based on data and analysis
        - based on strong machine learning models
        - based on skilled data scientists team
        - easy to use and accessible to everyone
        - intuitive and interactive

        ***Enjoy your experience!***
    """
    )

with col2:
    st.markdown(
        """
        Here you can find the possibile Orange tariff plans:
    """
    )    
    st.image("imgs/orange_tariff_plans.png")

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