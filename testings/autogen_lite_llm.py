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
    'seed': 42,
    'config_list': config_list,
    'temperature': 0,
    'max_tokens': -1
}
# %%
assitent = autogen.AssistantAgent(
    name = 'Peder Asistent',
    system_message='I am a helpful assistant.',
    llm_config=llm_config
)

coder = autogen.AssistantAgent(
    name = 'Peder Coder',
    system_message='I am a wikipedia speciallist.',
    llm_config=llm_config
)

user_proxy = autogen.UserProxyAgent(
    name = 'Svetlio proxy',
    human_input_mode='TERMINATE',
    max_consecutive_auto_reply=10,
    is_termination_msg=lambda x: x.get('content', '').rstrip().endswith('TERMINATE'),
    code_execution_config={'work_dir': 'web'},
    llm_config=llm_config,
    system_message='Reply TERMINATE if task has been solved at full satisfaction. \
        Otherwize, reply CONTINUE, or the reason why task is not solved yet.'
)
#%%
task = 'Find any information on the web for company ATEL Control Systems'
group_chat = autogen.GroupChat(
    agents=[assitent, coder, user_proxy],
    messages=[],
    max_round=5
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
