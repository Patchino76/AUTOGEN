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

os.environ['AUTOGEN_USE_DOCKER'] = "False"
# %%

# ollama running llava: http://localhost:11434/     
llava_config_list = [
    {
        "model": "llava",
        'api_key': "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",
        "base_url": "http://localhost:4321/v1/",
        'api_type': 'openai',
    }
]

#REMOTE WORKS but it is paid
# import replicate
# os.environ["REPLICATE_API_TOKEN"] = "r8_cIBJmM2DRotYVSntnm9jeM06czYJ1mh1WzIJG"
# llava_config_list = [
#     {
#         "model": "whatever, will be ignored for remote",  # The model name doesn't matter here right now.
#         "api_key": "r8_cIBJmM2DRotYVSntnm9jeM06czYJ1mh1WzIJG",  # Note that you have to setup the API key with os.environ["REPLICATE_API_TOKEN"]
#         "base_url": "yorickvp/llava-13b:2facb4a474a0462c15041b78b1ad70952ea46b5ec6ad29583c0b29dbd4249591",
#     }
# ]
# %%

image_agent = LLaVAAgent(
    name="image-explainer",
    max_consecutive_auto_reply=10,
    llm_config={"config_list": llava_config_list, "temperature": 0.5, "max_new_tokens": 1000},
)

user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={
        "last_n_messages": 3,
        "work_dir": "groupchat",
        "use_docker": False,
    },  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    human_input_mode="NEVER",  # Try between ALWAYS or NEVER
    max_consecutive_auto_reply=0,
)
# %%
# Ask the question with an image
user_proxy.initiate_chat(
    image_agent,
    message="""What's the breed of this dog?
    <img https://th.bing.com/th/id/R.422068ce8af4e15b0634fe2540adea7a?rik=y4OcXBE%2fqutDOw&pid=ImgRaw&r=0>.""",
    )

# %%
