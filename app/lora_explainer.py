import streamlit as st 
PAGE_TITLE = "Orange Image GenAI"
PAGE_ICON = ":orange_heart:"
# Set the page layout to wide
st.set_page_config(layout="wide")

# Create three columns
left, mid, right = st.columns([1.25, 7.5, 1.25])

with mid:

    st.markdown("""# Refiner""")

    st.markdown(""" ### A refiner in the context of Stable Diffusion XL (SDXL) enhances the details and quality of generated images. \n  ### It works by fine-tuning the output of a primary model, ensuring higher fidelity and realism.""")

    # Display images with descriptions in columns
    col1, col2 = st.columns(2)

    with col1:
        st.image("app/lora/before_refiner.png", caption="Image generated by Orange")
    with col2:
        st.image("app/lora/after_refiner.png", caption="After using realisticVisionV60B1_v51HyperVAE refiner")

    st.markdown("""# LoRA""")

    st.markdown(""" ### A LoRA (Low-Rank Adaptation) fine-tunes pre-trained models efficiently by adjusting only low-rank components of weight matrices. \n ### This method is resource-efficient and ideal for adapting large models to new tasks.""")

    st.markdown('<div style="text-align: center; font-size: 1.5em; font-weight: bold;">Age slider LoRA</div>', unsafe_allow_html=True)


    col_a, col_b, col_c = st.columns(3)


    
    # Display images in the first row
    with col_a:
        st.image("app/lora/young.png", caption="weight -2")
    with col_b:
        st.image("app/lora/after_refiner.png", caption="weight 0")
    with col_c:
        st.image("app/lora/old.png", caption="weight 2")

    # Display the title "People slider LoRA" in a large font
    st.markdown('<div style="text-align: center; font-size: 1.5em; font-weight: bold;">People slider LoRA</div>', unsafe_allow_html=True)

    # Create new columns for the second row of images
    col_d, col_e, col_f = st.columns(3)

    # Display images in the second row
    with col_d:
        st.image("app/lora/many_people.png", caption="weight -2")
    with col_e:
        st.image("app/lora/runner.png", caption="weight 0")
    with col_f:
        st.image("app/lora/no_people.png", caption="weight 2")
        
    st.markdown("""# Wildcards""")
    st.markdown(""" ### Wildcards are a powerful tool for creating complex prompts. 
                \n ### They allow you to vary a single prompt easily.
                \n ### For these images the following prompt was used: """)
    st.code("'masterpiece, best quality, photo, old __ethnicity__ smiling man in the sun looking away from viewer, on the right of image, shirt'")
    col6, col7, col8 = st.columns(3)
    with col6:
        st.image("app/lora/malaysian.png", caption="__ethnicity__ = 'Malaysian'")
    with col7:
        st.image("app/lora/nigerian.png", caption="__ethnicity__ = 'Nigerian'")
    with col8:
        st.image("app/lora/irish.png", caption="__ethnicity__ = 'Irish'")
        