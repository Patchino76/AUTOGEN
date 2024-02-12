#%%
import os
import autogen
from autogen import UserProxyAgent, ConversableAgent, AssistantAgent
import requests
from IPython import get_ipython
from typing_extensions import Annotated
# %%
# os.environ['AUTOGEN_USE_DOCKER'] = "False"
config_list = [
    {
        'model': 'llama2',
        'api_key': "none",
        # 'base_url': "http://127.0.0.1:11434/",
        'base_url': "http://localhost:4321/v1/",
        'api_type': 'openai',
    }
]
print(config_list[0])
#%%
llm_config={
    "timeout": 600,
    "cache_seed": 42,
    "config_list": config_list,
}
# %%


# create an AssistantAgent named "assistant"
assistant = autogen.AssistantAgent(
    name="assistant",
    llm_config=llm_config,
)
# create a UserProxyAgent instance named "user_proxy"
user_proxy = autogen.UserProxyAgent(
    name="agent",
    # is_termination_msg=lambda x: x.get("content", "") and x.get("content", "").rstrip().endswith("TERMINATE"),
    human_input_mode="NEVER",
    max_consecutive_auto_reply=3,
    code_execution_config={"work_dir":"_output","use_docker":False,},
    # code_execution_config={"use_docker":False,},
    llm_config=llm_config,
    system_message=""""Reply TERMINATE if the task has been solved at full satisfaction.
    Otherwise, reply CONTINUE, or the reason why the task is not solved yet."""
)
#%%
@user_proxy.register_for_execution()
@assistant.register_for_llm(name="python", description="run cell in ipython and return the execution result.")
def exec_python(cell: Annotated[str, "Valid Python cell to execute."]) -> str:
    ipython = get_ipython()
    result = ipython.run_cell(cell)
    log = str(result.result)
    if result.error_before_exec is not None:
        log += f"\n{result.error_before_exec}"
    if result.error_in_exec is not None:
        log += f"\n{result.error_in_exec}"
    return log


@user_proxy.register_for_execution()
@assistant.register_for_llm(name="sh", description="run a shell script and return the execution result.")
def exec_sh(script: Annotated[str, "Valid Python cell to execute."]) -> str:
    return user_proxy.execute_code_blocks([("sh", script)])
#%%
# the assistant receives a message from the user_proxy, which contains the task description
user_proxy.initiate_chat(
    assistant,
    message="Find 5 facts about the planet Mercury and list few sentences about each of them.",
)


# %%
