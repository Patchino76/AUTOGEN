# %%
# https://www.youtube.com/watch?v=8RtxvXIx61Y
# AutoGen Tutorial | ANY Open-Source LLM using LMStudio with MemGPT
import os
import autogen
from memgpt.autogen.memgpt_agent import create_autogen_memgpt_agent
import openai
from dotenv import load_dotenv

load_dotenv()
# %%

config_list = [
    {
        "api_type": os.getenv("api_type"),
        "api_base": os.getenv("api_base"),
        "api_key": os.getenv("api_key"),
    }
]
# %%
openai.api_base = os.getenv("api_base")
openai.api_key = os.getenv("api_key")
openai.api_type = os.getenv("api_type")

llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
    "max_tokens": -1,
}
# %%
user_proxy = autogen.UserProxyAgent(
    name = 'Svetlio',
    human_input_mode='NEVER',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get('content', '').rstrip().endswith('TERMINATE'),
    code_execution_config={'work_dir': 'mem1'},
    llm_config=llm_config,
    system_message="A human admin"
)
pm = autogen.AssistantAgent(
  name = "Product manager",
  system_message="You are a product manager and you are creative in software product ideas and requirements.\
  I will give you a task and you will help me to solve it.",
  llm_config=llm_config
)
# %%
# for debugging mem gpt
DEBUG = True
interface_kwargs = {
  'debug': DEBUG,
  'show_inner_thoughts': DEBUG,
  'show_function_outputs' : DEBUG
}

use_memgpt = bool(os.getenv("use_memgpt"))

if not use_memgpt:
  print('using autogen coder')
  coder = autogen.AssistantAgent(
    name = "Coder",
    system_message="You are an expert coder in Python.\
    I will give you a task and you will help me to solve it.",
    llm_config=llm_config
  )
else:
  print('using memgpt')
  coder = create_autogen_memgpt_agent(
  autogen_name = "MemGPT Coder",
  interface_kwargs=interface_kwargs,
  persona_description="I am a 10X engineer trained in Python. I will help you to solve a task.",
  user_description="You are participating in a group chat with a user ({user_proxy.name})",
  )
# %%
groupchat = autogen.GroupChat(
  agents=[coder, user_proxy, pm],
  messages=[],
  max_round=2
)

manager = autogen.GroupChatManager(
  groupchat=groupchat,
  llm_config=llm_config
)
# %%
user_proxy.initiate_chat(
  manager=manager, 
  message = "Create a simple random number generator in python, that's it." ,
  recipient=pm)
# %%