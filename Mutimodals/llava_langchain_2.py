#%%
import langchain
import base64
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage
# from langchain.chat_models import ChatOpenAI
import requests
import json
# %%
# url = "http://localhost:4321/v1"
url = "http://localhost:8000"
# url = "http://localhost:11434/v1"

client = ChatOpenAI(base_url=url, api_key="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")
# embedding = OpenAIEmbeddings()
# %%
image_path = 'img/agents.png'
image_path = 'img/stop.jpg'
image_path = 'img/kiss.jpeg'
image_path = 'img/table_small.jpg'

def encode_image(image_path):
    with open(image_path, "rb") as image_file:
        return base64.b64encode(image_file.read()).decode('utf-8')

base64_image = encode_image(image_path)
# %%

msg = client.invoke(
    [
        AIMessage(content = "You are a bot that can understand images and read tables."),
        HumanMessage(
            content=[
                
                {"type": "text", "text": "How many hours JohnDoe worked and what was his total earnings?"},
                {"type": "image_url", "image_url": {"url": f"data:image/jpeg;base64,{base64_image}"}},
            ]
        ),
    ]
)
# %%
print(msg)
# %%
