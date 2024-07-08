# 🟧Orange GenAI project: 

## 🎯 Objectives:
- Evaluate if AI generated images could be a on par with human generated picture. Those pictures shoud reflect Orange Branding and focus on Seniors Customer Segment.
- To answer that question we have : 
    - first investigated open source image GenAI model ad well as GUI . We have deciced to work with Stable Diffusion and Fooocus
    - then we created an app aiming mainly to provide : 
        - a blintest environment to evaluate the potential of AI Generated image vs real one
        - an image recording system displaying main generation parameters as well as details log for each image saved
        - a simple prompting feature allowing people to test without the hassle of engineering or software technicalities. 
    - generated a couple thousands of image in between 🚀

<br>

<div align="center">
  <a href="https://orangeblindtest.streamlit.app/">CLICK THE MAGICIAN TO TRY THE APP !!!</a>
</div>

<br>

<div align="center">
  <a href="https://orangeblindtest.streamlit.app/">
    <img src="resized_magician.png" alt="![CLICK THE MAGICIAN TO TRY THE APP !!!" />
  </a>
</div>

## 🔧 Installation

To install the app scripts , follow these steps:

- Clone the repository to your local machine using the command :
    - `git clone https://github.com/HazemEldabaa/orange-brand-genai.git`
    
- Get into the appfolder: 
    - `cd into orange-brand-genai`
    
- Create your virtual environment and ensure that you have the required dependencies installed by executing:
    - `pip install -r requirements.txt`


    

## 👟 Running
- you may just click the `TRY THE APP` link in the above Objectives pragraph to try the app online,

- Or if you are trying to duplicate or create your own app based on your own set of pdf : 
    - once the above installation is done then 
        - Get into the app folder: `cd app`
        - Run the app locally : `streamlit run app.py`

- Note that being able to run the prompt feature in the app requires : 
    - either to contact us so that we can initialize the tech pipeline if you are using the online app,
    - or set up yourself a collab (or other server offering GPU) environment and run Fooocus GUI from there (code for collab can be found in the collab.ipynb file). You can find full information on how to do it here : https://github.com/lllyasviel/Fooocus/tree/main 




## 🔥 Credit
- Special Thanks to Lyumin Zhang and supporting people for FOOOCUS open source project :  https://github.com/lllyasviel. It really helped us a lot throughout this project