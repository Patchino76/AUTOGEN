#%%
import openai
from openai import OpenAI
import base64
import requests
import time
# %%
client = OpenAI(base_url="http://localhost:4321/v1/", api_key="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")
# %%
image_path = 'img/stop.jpg'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)
# %%
# Perform image inference
completion = client.chat.completions.create(
    model="local-model",  # Specify the LLaVA model
    messages=[
        {
            "role": "user",
            "content": [
                {"type": "text", "text": "What’s in this image?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ],
        }
    ],
    max_tokens=1000,
    stream=True
)
# %%
# Print the result
for chunk in completion:
    if chunk.choices[0].delta.content:
        print(chunk.choices[0].delta.content, end="", flush=True)


# %%
