import streamlit as st 

st.markdown("""A refiner in the context of Stable Diffusion XL (SDXL) enhances the details and quality of generated images. 
            It works by fine-tuning the output of a primary model, ensuring higher fidelity and realism.""")

# Display images with descriptions in columns
col1, col2 = st.columns(2)

with col1:
    st.image("app/lora/before_refiner.png", caption="Before refiner")
with col2:
    st.image("app/lora/after_refiner.png", caption="After refiner")

st.markdown("""A LoRA (Low-Rank Adaptation) fine-tunes pre-trained models efficiently by adjusting only low-rank components of weight matrices. 
            This method is resource-efficient and ideal for adapting large models to new tasks.""")

# Display images with descriptions in columns
col3, col4, col5 = st.columns(3)

with col3:
    st.image("app/lora/young.png", caption="LoRA weight -2")
    st.image("app/lora/many_people.png", caption="LoRA weight -2")
with col4:
    st.image("app/lora/after_refiner.png", caption="LoRA weight 0")
    st.image("app/lora/runner.png", caption="LoRA weight 0")
with col5:
    st.image("app/lora/old.png", caption="LoRA weight 2")
    st.image("app/lora/no_people.png", caption="LoRA weight 2")

