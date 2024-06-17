import streamlit as st
PAGE_TITLE = "Appendix"
PAGE_ICON = ":orange_heart:"
st.set_page_config(page_title=PAGE_TITLE, page_icon=PAGE_ICON, layout="wide")

# Create three columns
col1, col2, col3 = st.columns([1.25, 7.5, 1.25])

with col2:

    st.markdown(""" This page contains more detailed explanations of the tools used in this demo. """)

    with st.expander("Model Selection (Checkpoint)"):
        st.markdown("""
    - ### Choose a model that aligns with your artistic or thematic goals, and is the base for how your prompt is interpreted.
    - ### These are large models (2GB-12GB or more!)
    - ### Consider using different open source models (community made: Civitai) for varied styles, such as photorealistic, cartoonish, abstract, or impressionistic.
    - ### Regularly update your model to leverage improvements and new features.
        """)

    with st.expander("Prompts (Stable Diffusion)"):
        st.markdown("""
    - ### Positive Prompts:
        - Use descriptive and specific language to guide the AI towards the desired image.
        - Include details such as a subject, colors, styles, lighting, composition and quality.
        - Example: "A serene landscape with a clear blue sky, mountains in the background, and a calm lake reflecting the scenery."
        - Does not need to be sentences, as they can introduce too many keywords!
    - ### Negative Prompts:
        - Specify elements you want to avoid in the image.
        - Like the positive prompt, this can be an object, style, mood, artifacts or NSFW.
        - Example: "people, urban elements, artificial lighting, hands, over-saturation, logos, text, bad quality."
    - ### Weights:
        - Assign higher weights to crucial aspects of the prompt to ensure they are more prominent in the generated image (or the opposite).
        - Two methods:
            - multiple parentheses: "A (serene) landscape with a (((clear))) blue sky"
            - add weight numbers: (close up:1.3), viewer is close, (facing viewer:1.1). The scene is lit with (bright light:1.2)
        """)

    with st.expander("Utilizing Predefined Styles"):
        st.markdown("""
    - ### Styles are a predefined set of keywords (positive and negative)
    - ### Leverage the predefined style checkboxes in Fooocus to quickly apply popular and effective styles to your images (or create your own -> Orange style).
    - ### These checkboxes allow you to easily select from a variety of preset styles such as "photorealistic," "fantasy," "corporate," "watercolor," and more.
    - ### Combining these checkboxes with detailed prompts can enhance the consistency and quality of your generated images.
    - ### Experiment with different checkboxes to see how they affect the output and find the styles that best match your creative vision.
        """)

    with st.expander("Refiners (Checkpoint)"):
        st.markdown("""
    - ### Use refiners to enhance specific aspects of the image during the generation (denoising).
    - ### Also large models (2GB-12GB or more!)
    - ### Adjusts parameters like sharpness, color balance, contrast and texture to change the overall quality.
    - ### Introduces new keyword opportunities that were not present in the base model.
    - ### Experiment with different refiners to see which best suits your image (and if you need one at all).
        """)

    with st.expander("LoRAs (Low-Rank Adaptations)"):
        st.markdown("""
    - ### Incorporate LoRAs to fine-tune the model for specific styles, themes or subjects.
    - ### Lightweight models (less than 200MB)
    - ### Example: A LoRA for generating images in the style of a famous artist or for a specific genre like cyberpunk.
        """)

    with st.expander("Wildcards"):
        st.markdown("""
    - ### Utilize wildcards to introduce variability and creativity in the prompts, to avoid default interpretations.
    - ### Create lists of interchangeable terms or phrases to keep your image generation dynamic.
    - ### Example wildcard list for a landscape prompt: "A serene __landscape__ with a clear blue sky". Where landscape is {forest|desert|mountains|ocean}.
        """)

    with st.expander("General Tips"):
        st.markdown("""
    - ### Start with simple prompts, then slowly build up.
    - ### Combine elements from different prompts and models to create more complex and unique images.
    - ### Continuously experiment with new tools (inpainting, image prompting etc.) and parameters (weights, guidance, sharpness) to refine your process.
    - ### Gather feedback and iteratively improve your prompts and settings based on the results you achieve.
    - ### Sometimes hyper-specific prompts work better: iphone14 is better than mobile phone.
    - ### When you find a prompt you like, remember to keep the same seed!
    - ### Aspect ratio is very important to image generation and greatly changes the interpretation of prompts. It will be much more difficult to generate a man standing at his full height in a landscape/horizontal image, than a portrait image.
    - ### Distance to a subject can be difficult to control (model dependant), but adding keywords of what you want to include can help force the distance. Example: "short hair", "nike trainers" instead of "full body".
    - ### Poses: There are a few ways to control human poses but in general introducing a LoRA or using image prompting (PyraCanny in fooocus) are the best ways.
    - ### Hands and eyes are the most difficult thing to generate (and teeth sometimes), here are some tips:
        - #### There are negative prompts that can help: "Poorly drawn hands, Missing fingers, Bad anatomy" etc.
        - #### For positive prompts you can specify: "beautiful hands, beautiful eyes". The simpler the hand the better. Open hands will generate more clearly than closed hands, etc. If hands are not something critical to the composition, then you can hide them or put them in pockets.
        - #### Although if you are limiting yourself to just prompting with a base model, you will have issues.
        - #### Mobius as a base model and Realistic Vision as a refiner seem to be better when generating hands on average, but even then they can be hit and miss.
        - #### There are many LoRAs that aim to help with this process, and it's just a bit of trial and error to see which ones work with which base model.
        - #### There are also textual embeddings, which are even smaller than LoRAs which can be used to change the generation.
        - #### Distance will affect clarity, so it's best for them to be either large (to capture details clearly) or small (so that you can barely see them/they will be blurred).
        - #### High contrast on the subject can affect how well eyes and teeth generate and line imperfections will be more visible for hands and fingers.
        - #### You can also regenerate the hands specifically (or anything else) in an image you like by using inpainting. You create a mask over the area and its surroundings and either run a new prompt, or rerun your old prompt. Usually it will take many iterations to get something satisfying.
        """)