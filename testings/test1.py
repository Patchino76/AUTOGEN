#%%
import autogen
# %%
config_list = [
    {
        "api_type" : "open_ai",
        "api_base": "http://localhost:4321/v1",
        "api_key": "pk-swAmmfqGxOtmoYEnoBtCjNWPBddlTOcQzrGyXEduUwDLGNDl"
    }
]
llm_config = {
  'request_timeout': 600,
  'seed': 42,
  'config_list': config_list,
  'temperature': 0
}
# %%
assistant = autogen.AssistantAgent(
  name = 'assistent',
  system_message='You are a coder specialized in Python.',
  llm_config=llm_config
)
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


# %%
task = """
    Write a pythpn method that returns the sum of two numbers.
"""

user_proxy.initiate_chat(
  assistant,
  message=task
)
# %%
