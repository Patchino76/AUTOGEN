#%%
import os
import autogen
from autogen import UserProxyAgent, ConversableAgent, AssistantAgent
# %%
os.environ['AUTOGEN_USE_DOCKER'] = "False"
# os.environ['OPENAI_API_KEY '] = "NULL"

# config_list = [
#         {
#                 "api_type" : "open_ai",
#                 "base_url": "http://127.0.0.1:11434/",
#                 "api_key": "NULL" 
#         }
# ]
config_list ={
                "api_type" : "openai",
                "base_url": "http://localhost:4321/v1/",
                "api_key": "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" 
        }

llm_config = {
    # 'cache_seed': 42,
    'config_list': config_list,
    'temperature': 0.1,
    'timeout': 60
}
# %%
# coder = autogen.AssistantAgent(
#     name="Coder",
#     system_message="You are an expert coder in Python. I will give you a task and you will help me to solve it.",
#     llm_config=llm_config
# )
# assistant = ConversableAgent("agent", llm_config=llm_config)

user_proxy = UserProxyAgent(
    name="user",
    human_input_mode="NEVER",
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get("content", "").rstrip().endswith("TERMINATE"),
    code_execution_config={"work_dir": "coding"},
    llm_config=llm_config,
    system_message="Reply TERMINATE if task has been solved at full satisfaction.",
)


# %%
task = "Generate 10 random integers with numpy library"
user_proxy.initiate_chat(
    coder,
    task
)
# %%
# task = "Generate 10 random integers with numpy library"
# initiation_message = {
#     "content": task,
#     "sender": user_proxy.name,
#     "recipient": coder.name
# }

# # Provide the messages and model arguments when calling initiate_chat
# user_proxy.initiate_chat(
#     messages=[initiation_message],
#     model=coder,
#     recipient=coder
# )

# %%
