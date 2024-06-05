import replicate
import cv2
import urllib
import numpy as np
import requests
import ssl
import mediapipe as mp
import pandas as pd

# Function to upload an image to file.io
def upload_to_fileio(image_path):
    api_url = "https://file.io"
    with open(image_path, "rb") as img:
        response = requests.post(api_url, files={"file": img})
    if response.status_code == 200:
        return response.json()["link"]
    else:
        print(f"Failed to upload image to file.io. Status code: {response.status_code}")
        print(f"Response: {response.text}")
        raise Exception("Failed to upload image to file.io")

def create_mask(image):
    mp_face_mesh = mp.solutions.face_mesh
    face_mesh = mp_face_mesh.FaceMesh(static_image_mode=True, max_num_faces=10)

    results = face_mesh.process(cv2.cvtColor(image, cv2.COLOR_BGR2RGB))
    if not results.multi_face_landmarks:
        raise Exception("No face landmarks detected")

    mask = np.zeros((image.shape[0], image.shape[1]), dtype=np.uint8)
    face_oval = mp_face_mesh.FACEMESH_FACE_OVAL
    df = pd.DataFrame(list(face_oval), columns=["p1", "p2"])

    for landmarks in results.multi_face_landmarks:
        routes_idx = []

        p1 = df.iloc[0]["p1"]
        p2 = df.iloc[0]["p2"]

        for i in range(df.shape[0]):
            obj = df[df["p1"] == p2]
            p1 = obj["p1"].values[0]
            p2 = obj["p2"].values[0]

            route_idx = [p1, p2]
            routes_idx.append(route_idx)

        routes = []

        for source_idx, target_idx in routes_idx:
            source = landmarks.landmark[source_idx]
            target = landmarks.landmark[target_idx]

            relative_source = (int(image.shape[1] * source.x), int(image.shape[0] * source.y))
            relative_target = (int(image.shape[1] * target.x), int(image.shape[0] * target.y))

            routes.append(relative_source)
            routes.append(relative_target)

        cv2.fillPoly(mask, [np.array(routes)], 255)

    return mask  # Inverting the mask


output = replicate.run(
    "konieshadow/fooocus-api-realistic:612fd74b69e6c030e88f6548848593a1aaabe16a09cb79e6d714718c15f37f47",
    input={
        "prompt": "happy family with teens wearing T-shirts, mobile phones, orange color",
        "cn_type1": "ImagePrompt",
        "cn_type2": "ImagePrompt",
        "cn_type3": "ImagePrompt",
        "cn_type4": "ImagePrompt",
        "sharpness": 2,
        "image_seed": -1,
        "uov_method": "Disabled",
        "image_number": 1,
        "guidance_scale": 3,
        "refiner_switch": 0.5,
        "negative_prompt": "unrealistic, saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
        "style_selections": "Fooocus V2,Fooocus Photograph,Fooocus Negative",
        "uov_upscale_value": 0,
        "outpaint_selections": "",
        "outpaint_distance_top": 0,
        "performance_selection": "Speed",
        "outpaint_distance_left": 0,
        "aspect_ratios_selection": "1152*896",
        "outpaint_distance_right": 0,
        "outpaint_distance_bottom": 0,
        "inpaint_additional_prompt": ""
    }
)

# Since output is a list, get the first URL
url = output[0]
print(url)

# Create an unverified SSL context
ssl_context = ssl._create_unverified_context()

req = urllib.request.urlopen(url, context=ssl_context)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)  # 'Load it as it is'

# Save the image
cv2.imwrite('happy_family.png', img)
mask = create_mask(img)
cv2.imwrite('mask.png', mask)
# Upload images to file.io and get URLs
try:
    image_url = upload_to_fileio("happy_family.png")
    mask_url = upload_to_fileio("mask.png")
except Exception as e:
    print(e)
    exit(1)

output = replicate.run(
    "konieshadow/fooocus-api-realistic:612fd74b69e6c030e88f6548848593a1aaabe16a09cb79e6d714718c15f37f47",
    input={
        "prompt": "",
        "cn_type1": "ImagePrompt",
        "cn_type2": "ImagePrompt",
        "cn_type3": "ImagePrompt",
        "cn_type4": "ImagePrompt",
        "sharpness": 2,
        "image_seed": -1,
        "uov_method": "Disabled",
        "image_number": 1,
        "guidance_scale": 3,
        "refiner_switch": 0.5,
        "negative_prompt": "unrealistic, saturated, high contrast, big nose, painting, drawing, sketch, cartoon, anime, manga, render, CG, 3d, watermark, signature, label",
        "style_selections": "Fooocus V2,Fooocus Photograph,Fooocus Negative",
        "uov_upscale_value": 0,
        "inpaint_input_mask": mask_url,
        "inpaint_input_image": image_url,
        "outpaint_selections": "",
        "outpaint_distance_top": 0,
        "performance_selection": "Speed",
        "outpaint_distance_left": 0,
        "aspect_ratios_selection": "1152*896",
        "outpaint_distance_right": 0,
        "outpaint_distance_bottom": 0,
        "inpaint_additional_prompt": "detailed face"
    }
)
url2 = output[0]
print(url2)

req = urllib.request.urlopen(url2, context=ssl_context)
arr = np.asarray(bytearray(req.read()), dtype=np.uint8)
img = cv2.imdecode(arr, -1)  # 'Load it as it is'

# Save the image
cv2.imwrite('happy_family2.png', img)

