#%%
import autogen
# %%
config_list = [
        {
                # "api_type" : "open_ai",
                "base_url": "http://localhost:4321/v1",
                "api_key": "NULL" 
        }
]
llm_config = {
    # 'request_timeout': 600,
    'seed': 43,
    'config_list': config_list,
    'temperature': 0,
    'max_tokens': -1,
    # 'use_cache' : False
}
# %%
termination_msg = lambda x: isinstance(x, dict) and "TERMINATE" == str(x.get("content", ""))[-9:].upper()

assitent = autogen.AssistantAgent(
    name = 'History researcher',
    system_message='You are good at finding facts in historical movies.  Reply `TERMINATE` in the end when everything is done.',
    llm_config=llm_config
)

coder = autogen.AssistantAgent(
    name = 'Senior_Python_Engineer',
    system_message="You are a senior python engineer. Assume that wikipedia is installed. Print the code and reply `TERMINATE` in the end when everything is done.",
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name = 'Boss',
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=5,
    is_termination_msg=termination_msg,
    code_execution_config={'work_dir': 'web', 'use_docker': True},
    llm_config=llm_config,
    system_message='Reply TERMINATE if task has been solved at full satisfaction. \
        Otherwize, reply CONTINUE, or the reason why task is not solved yet.'
)
#%%
task = 'Find the movie Oppenheimer using Wikipedia API. Wikipedia is installed. \
    Tell me whether conversation between Oppenheimer and Einsten really exists in history.'
group_chat = autogen.GroupChat(
    agents=[assitent, coder, user_proxy],
    messages=[],
    max_round=10
)

manager = autogen.GroupChatManager(
    groupchat=group_chat,
    llm_config=llm_config
)

# %%
user_proxy.initiate_chat(
    manager=manager, 
    message = task,
    recipient=assitent)
# %%
