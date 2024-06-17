# ADD THIS AS A LAST CELL IN YOUR NOTEBOOK
# DEFINE THE VARIABLES AS NEEDED
import wandb
from PIL import Image
import numpy as np
import json

# Add your API key here
wandb.login(key="your-api-key")

# Change this with the path of the json file containing your parameters
with open('parameters.json', 'r') as file:
    config = json.load(file)
# Initialize W&B run
wandb.init(project="image-generation", name="experiment-1", config=config)

# Example: Generate and save images during training (dummy example)
prompt = # your prompt object here
image = # your image object here from the model
image_path = f"generated_image_epoch_{epoch}.png" # Change the name as you like, you can have an image for each epoch or only the last one
image.save(image_path) # to save the image to the path and name specified above

# Log training metrics and the generated image
wandb.log({
    "prompt": prompt, # Log the prompt
    "epoch": epoch, # define this in your training loop
    "loss": loss,  # Dummy loss value, replace with your actual loss or remove
    "generated_image": wandb.Image(image_path) # Log the image
})

# Finish the W&B run
wandb.finish()
