#%%
import langchain
import base64
from langchain_openai import ChatOpenAI
from langchain.schema import AIMessage, HumanMessage, SystemMessage

# %%

from langchain_community.chat_models import ChatOllama
client = ChatOllama(model="llava:34b-v1.6")
# %%
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
 %%
