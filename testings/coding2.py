#%%
import autogen
# %%
config_list = [
    {
        "api_type" : "open_ai",
        # "api_base": "http://localhost:4321/v1",
        "api_base": "https://api.pawan.krd/pai-001-light-beta/v1",
        # "api_key": "NULL" 
         "api_key": "pk-swAmmfqGxOtmoYEnoBtCjNWPBddlTOcQzrGyXEduUwDLGNDl"
    }
]
llm_config = {
  'request_timeout': 600,
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
  code_execution_config={'work_dir': 'coding'},
  llm_config=llm_config,
  system_message="""Reply TERMINATE if task has been solved at full satisfaction.
  Otherwize, reply CONTINUE, or the reason why task is not solved yet."""
)

coder = autogen.AssistantAgent(
  name = 'Coder',
  system_message='I am a python coder.',
  llm_config=llm_config,
  
)


# %%

user_proxy.initiate_chat(
    coder, 
    message = 'Generate 100 random numbers between 0 and 100 and print the result.',
)
# %%
