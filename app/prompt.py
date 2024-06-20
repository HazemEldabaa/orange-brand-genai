import streamlit as st


# Define the template for the output
output_template = {
    "prompt": "",
    "negative_prompt": "unrealistic, (saturated:1.2), high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label, Worst quality, Normal quality, Low quality, Low res, Blurry, Jpeg artifacts, Out of focus, Bad anatomy, Bad proportions, Deformed, Disconnected limbs, Disfigured, Extra arms, Extra limbs, Extra hands, Fused fingers, Gross proportions, Long neck, Malformed limbs, Mutated, Mutated hands, Mutated limbs, Missing arms, Missing fingers, Poorly drawn hands, Poorly drawn face, extra fingers, 2D, Sketch, Drawing, Bad photography, Bad photo, Deviant art, Artstation, Octane render, Painting, Oil painting, Illustration, very reflective skin, waxy skin, skin colored clothing, nsfw, nude, grain, buttons",
    "prompt_expansion": "",
    "styles": "[]",
    "performance": "Quality",
    "resolution": "(1152, 896)",
    "guidance_scale": 3,
    "sharpness": 2,
    "adm_guidance": "(1.5, 0.8, 0.3)",
    "base_model": "mobius.safetensors",
    "refiner_model": "Realistic_vision_V6B1.safetensors",
    "refiner_switch": 0.6,
    "clip_skip": 2,
    "sampler": "dpmpp_2m_sde_gpu",
    "scheduler": "karras",
    "vae": "Default (model)",
    "seed": "-1",
    "lora_combined_1": "SDXL_FILM_PHOTOGRAPHY_STYLE_BetaV0.4.safetensors : 1.1",
    "lora_combined_2": "perfect_eyes.safetensors : 0.6",
    "metadata_scheme": False,
    "version": "Fooocus v2.4.3"
}

# Streamlit app layout
st.title("Prompt Generator for Fooocus v2.4.3")
st.write("This page is not working out of the box, contact one of the maintainers on the contact page so we can spin up the server")
st.write('Follow this link: https://12bffe577853bb1d56.gradio.live/')

# Input prompt from user
user_prompt = st.text_input("Enter your prompt:")

# When the user enters a prompt and clicks the button
if user_prompt:
    # Construct the new prompt with additional details
    detailed_prompt = f"{user_prompt}, highly detailed, photorealistic"
    output_template["prompt"] = detailed_prompt

    # Display the output in JSON format
    st.json(output_template)

