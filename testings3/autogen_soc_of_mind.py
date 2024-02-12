#%%
import autogen
import os
os.environ['AUTOGEN_USE_DOCKER'] = "False"
# %%
url = "http://localhost:8000"
url = "http://localhost:4321/v1"
config_list = [
        {
                "model" : "mistral",
                "api_type" : "openai",
                "base_url": url,
                "api_key": "NULL" 
        }
]
llm_config = {
    # 'request_timeout': 600,
    'cache_seed': 42,
    'config_list': config_list,
    'temperature': 0,
    'max_tokens': -1
}
# %%
assistant = autogen.AssistantAgent(
    "inner-assistant",
    llm_config=llm_config,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)

code_interpreter = autogen.UserProxyAgent(
    "inner-code-interpreter",
    human_input_mode="NEVER",
    code_execution_config={
        "work_dir": "coding",
        "use_docker": False,
    },
    default_auto_reply="",
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
)

groupchat = autogen.GroupChat(
    agents=[assistant, code_interpreter],
    messages=[],
    speaker_selection_method="round_robin",  # With two agents, this is equivalent to a 1:1 conversation.
    allow_repeat_speaker=False,
    max_round=8,
)

# %%

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    is_termination_msg=lambda x: x.get("content", "").find("TERMINATE") >= 0,
    llm_config=llm_config,
)
# %%

from autogen.agentchat.contrib.society_of_mind_agent import SocietyOfMindAgent  
# %%

task = "On which days in 2024 was Microsoft Stock higher than $370?"

society_of_mind_agent = SocietyOfMindAgent(
    "society_of_mind",
    chat_manager=manager,
    llm_config=llm_config,
)

user_proxy = autogen.UserProxyAgent(
    "user_proxy",
    human_input_mode="NEVER",
    code_execution_config=False,
    default_auto_reply="",
    is_termination_msg=lambda x: True,
)

# %%
user_proxy.initiate_chat(society_of_mind_agent, message=task)
# %%
