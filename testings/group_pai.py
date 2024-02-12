#%%
import autogen
# %%
config_list = [
    {
        # "api_type" : "open_ai",
        # "base_url": "http://localhost:4321/v1",
        # "api_key": "NULL" 
        # "api_base": "https://api.pawan.krd/pai-001-rp/v1",
        "base_url": "https://api.pawan.krd/pai-001-light-rp/v1",
        "api_key": "pk-swAmmfqGxOtmoYEnoBtCjNWPBddlTOcQzrGyXEduUwDLGNDl"
    }
]
llm_config = {
#   'request_timeout': 600,
  'seed': 42,
  'config_list': config_list,
  'temperature': 0,
  'max_tokens': -1
}
# %%

user_proxy = autogen.UserProxyAgent(
  name = 'Svetlio',
  human_input_mode='NEVER',
  max_consecutive_auto_reply=10,
  is_termination_msg=lambda x: x.get('content', '').rstrip().endswith('TERMINATE'),
  code_execution_config={'work_dir': 'web'},
  llm_config=llm_config,
  system_message="""Reply TERMINATE if task has been solved at full satisfaction.
  Otherwize, reply CONTINUE, or the reason why task is not solved yet."""
)

content_creator = autogen.AssistantAgent(
  name = 'Content Creator',
  system_message='I am a Content Creator that  talks about everything',
  llm_config=llm_config
)

script_writer = autogen.AssistantAgent(
  name = 'Script Writer',
  system_message='I am a script writer for the Content Creator',
  llm_config=llm_config
)

researcher = autogen.AssistantAgent(
  name = 'Researcher',
  system_message='I am a researcher for the Content Creator and look up white papers and web sites',
  llm_config=llm_config
)

reviewer = autogen.AssistantAgent(
  name = 'Reviewer',
  system_message='I am a reviewer for the Content Creator, Script Writer and Researcher once they are done and have come with a script.\
     I will double check there are no mistakes.',
  llm_config=llm_config
)

# %%
groupchat = autogen.GroupChat(
    agents=[user_proxy, content_creator, script_writer, researcher, reviewer],
    messages=[],
)

manager = autogen.GroupChatManager(
    groupchat=groupchat,
    llm_config=llm_config
)

user_proxy.initiate_chat(
    manager=manager, 
    message = 'I need a detailed inforamtion about the bulgarian actor Todor Kolev. You can check wikipedia.',
    recipient=content_creator)
# %%
for message in groupchat.messages:
    print(message)
# %%
