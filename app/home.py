import streamlit as st

PAGE_TITLE = "Orange Image GenAI"
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
    st.image("app/imgs/orange_home.png", width=150)


# Display header image and title
st.image("app/imgs/orange_header.png", use_column_width="always")
st.title("Welcome to the Orange Image GenAI! :orange_heart:")
st.markdown(horizontal_bar, True)


col1, spacer, col2 = st.columns([1, 0.05, 1])

with col1:
    st.markdown(
        """
        We have created an app reflecting our work on AI generated pictures.

        **About the generation environment:**
        - Keywords extracted from brandbook as base
        - Stable diffusion models and improvement layers (Refiners, LoRAs)
        - Fooocus as GUI for easy experimentation
        - Minimum or no manual intervention on the image

        **About the app functionalities:**
        - Make a blind test on generated vs real image
        - Display generated images with their logs
        - Direct prompting and generation

        ***Enjoy your experience!***
    """
    )

with col2:
    # st.markdown(
    #     """
    #     The Squad:
    # """
    # )    
    if st.button("Meet the team", key="team_button"):
        st.image("app/imgs/team-angel.png")

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