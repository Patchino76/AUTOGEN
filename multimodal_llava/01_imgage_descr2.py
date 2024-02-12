#%%
import json
import os
import base64

import matplotlib.pyplot as plt
import requests
from PIL import Image

# %%

image_path = "img/agents.png"

with open(image_path, "rb") as image_file:
    encoded_image = base64.b64encode(image_file.read()).decode("utf-8")

# %%
url = "http://localhost:8000/"

payload = {
    "model" : "llava",
    "prompt" : "Describe the image",
    "stream" : False,
    "images" : [encoded_image]
}



# %%
response = requests.post(url=url, data = json.dumps(payload))
print(response.text)
# %%
