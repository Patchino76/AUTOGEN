#%%
import json
import os
import random
import time
from typing import Any, Callable, Dict, List, Optional, Tuple, Type, Union

import matplotlib.pyplot as plt
import requests
from PIL import Image
from termcolor import colored

import autogen
from autogen import Agent, AssistantAgent, ConversableAgent, UserProxyAgent
from autogen.agentchat.contrib.llava_agent import LLaVAAgent, llava_call
# %%

# ollama running llava: http://localhost:11434/     
llava_config_list = [
    {
        "model": "llava",
        "api_key": "NULL",
        "base_url": "http://localhost:8000",
    }
]

#REMOTE WORKS but it is paid
# import replicate
# os.environ["REPLICATE_API_TOKEN"] = "r8_cIBJmM2DRotYVSntnm9jeM06czYJ1mh1WzIJG"
# llava_config_list = [
#     {
#         "model": "whatever, will be ignored for remote",  # The model name doesn't matter here right now.
#         # "api_key": "r8_cIBJmM2DRotYVSntnm9jeM06czYJ1mh1WzIJG",  # Note that you have to setup the API key with os.environ["REPLICATE_API_TOKEN"]
#         "base_url": "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
#     }
# ]
# %%

rst = llava_call(
    "Describe this AutoGen framework <img https://raw.githubusercontent.com/microsoft/autogen/main/website/static/img/autogen_agentchat.png> with bullet points.",
    llm_config={"config_list": llava_config_list, "temperature": 0},
)

print(rst)


# %%
