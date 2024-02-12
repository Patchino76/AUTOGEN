# %%
import autogen
from autogen.agentchat.contrib.math_user_proxy_agent import MathUserProxyAgent

# %%
config_list = [
    {
        "api_type": "open_ai",
        # "api_base": "http://localhost:4321/v1",
        "api_base": "https://api.pawan.krd/pai-001-light-beta/v1",
        # "api_key": "NULL"
        "api_key": "pk-swAmmfqGxOtmoYEnoBtCjNWPBddlTOcQzrGyXEduUwDLGNDl",
    }
]
llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
    "max_tokens": -1,
}
# %%

mathproxyagent = MathUserProxyAgent(
    name="mathproxyagent", 
    human_input_mode="NEVER",
    code_execution_config={"use_docker": False},
)

assistant = autogen.AssistantAgent(
    name="Assistent",
    system_message="You are a helpful assistant.",
    llm_config=llm_config,
)


# %%
math_problem = "Find all numbers between 1 and 100 that are divisible by 3 or 5"
mathproxyagent.initiate_chat(assistant, problem=math_problem)
# %%
