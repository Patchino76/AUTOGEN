# %%
# https://www.youtube.com/watch?v=8RtxvXIx61Y
# AutoGen Tutorial | ANY Open-Source LLM using LMStudio with MemGPT
import os
import autogen
from memgpt.autogen.memgpt_agent import create_autogen_memgpt_agent
import openai


# %%
config_list = [
    {
        "api_type": "open_ai",
        # "api_base": "http://localhost:4321/v1",
        "api_base": "https://api.pawan.krd/pai-001-light-beta/v1",
        "api_key": "pk-swAmmfqGxOtmoYEnoBtCjNWPBddlTOcQzrGyXEduUwDLGNDl",
    }
]
# openai.api_key = "pk-swAmmfqGxOtmoYEnoBtCjNWPBddlTOcQzrGyXEduUwDLGNDl"
# openai.api_base = "http://localhost:4321/v1"
# openai.api_type = "open_ai"

llm_config = {
    "request_timeout": 600,
    "seed": 42,
    "config_list": config_list,
    "temperature": 0,
    "max_tokens": -1,
}
# %%
# The user agent
user_proxy = autogen.UserProxyAgent(
    name="User_proxy",
    system_message="A human admin.",
    code_execution_config={"last_n_messages": 2, "work_dir": "groupchat"},
    human_input_mode="TERMINATE",
)


# The agent playing the role of the product manager (PM)
pm = autogen.AssistantAgent(
    name="Product_manager",
    system_message="Creative in software product ideas.",
    llm_config=llm_config,
)
# %%
# for debugging mem gpt
DEBUG = True

interface_kwargs = {
    "debug": DEBUG,
    "show_inner_thoughts": DEBUG,
    "show_function_outputs": DEBUG,
}

if 1 == 1:  # not os.getenv("use_memgpt"):
    coder = autogen.AssistantAgent(
        name="Coder",
        system_message=f"I am a 10x engineer, trained in Python. I was the first engineer at Uber "
        f"(which I make sure to tell everyone I work with).\n"
        f"You are participating in a group chat with a user ({user_proxy.name}) "
        f"and a product manager ({pm.name}).",
        llm_config=llm_config,
    )


else:
    coder = create_autogen_memgpt_agent(
        "MemGPT_coder",
        persona_description="I am a 10x engineer, trained in Python. I was the first engineer at Uber "
        "(which I make sure to tell everyone I work with).",
        user_description=f"You are participating in a group chat with a user ({user_proxy.name}) "
        f"and a product manager ({pm.name}).",
        model=os.getenv("model"),
        interface_kwargs=interface_kwargs,
    )
# %%
# Initialize the group chat between the user and two LLM agents (PM and coder)
groupchat = autogen.GroupChat(agents=[user_proxy, coder], messages=[])
manager = autogen.GroupChatManager(groupchat=groupchat, llm_config=llm_config)

# Begin the group chat with a message from the user
user_proxy.initiate_chat(
    manager=manager,
    message="Write a python function that adds to integers and returns the result.",
    recipient=coder,
)
# %%
