import streamlit as st 

PAGE_TITLE = "Conclusion"
PAGE_ICON = ":orange_heart:"
# Set the page layout to wide
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# Create three columns
col1, col2, col3 = st.columns([1.25, 7.5, 1.25])

with col2:

    with st.expander('Conclusions'):
        st.markdown("""
                ## Can realistic and potentially usable images for Orange be produced using AI? 
    ## Yes, they can.

    - ### Checkpoints (base and refiners): the most impactful
    - ### A good prompt: positive and negative keywords, details and weights
    - ### Specific tools (LoRAs, wildcards, inpainting) good image ⇒ great image
    - ### There is no catch-all answer for difficult objects ⇒ iterative process
    - ### Use the same seed to keep testing consistent

    """)
        
    with st.expander("Final remarks"):
        st.markdown("""
    - ### Fooocus:
        - #### User-friendly and easy to learn
        - #### Contains many features similar to competitors
        - #### Constantly being developed
        - #### Limited to SDXL1.0 models and SDXL1.0/SD 1.5 refiners
        - #### Effective but other tools offer extended capabilities
    - ### Automatic1111:
        - #### Supports a wider array of checkpoints
        - #### Offers greater customizability
        - #### User interface is complex but similar to Fooocus
        - #### Less forgiving with some of its technology
    - ### ComfyUI:
        - #### Advanced compared to Automatic1111
        - #### Enables setup of entire workflows/pipelines
        - #### Supports generation, rescaling, retouching, masking...
        - #### Moves beyond the manual iterative process
        """)
