#%%
import os
import autogen
from autogen import UserProxyAgent, ConversableAgent, AssistantAgent

from typing import Dict, Union
from IPython import get_ipython
from IPython.display import Image, Markdown

#USING LITE LLM example:
# pip install litellm
# ollama pull codellama
# litellm --model ollama/codellama --api_base http://localhost:11434 --temperature 0.3 --max_tokens 2048
# %%
# os.environ['AUTOGEN_USE_DOCKER'] = "False"
config_list = [
    {
        'model': 'llama2',
        'api_key': "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",
        # 'base_url': "http://localhost:11434/", #ollama (docker)
        'base_url': "http://localhost:8000/", #litellm
        # 'base_url': "http://localhost:4321/v1/", #lmstudio
        'api_type': 'openai',
    }
]
print(config_list[0])
#%%
llm_config={
    "timeout": 600,
    "cache_seed": 45,
    "config_list": config_list,
    "temperature": 0,
}
# %%
# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="user_proxy",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={
        "work_dir": "coding",
        "use_docker": True,  # Please set use_docker=True if docker is available to run the generated code. Using docker is safer than running the generated code directly.
    },
)
#%%
user_proxy.initiate_chat(
    assistant,
    message="""Write a python script that finds five famous hotels in Sofia, Bulgaria and prints\
        their names and locations. Execute the script and save the data in json format.""", silent=False
)

# %%
