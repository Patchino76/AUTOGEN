# %%
import os
from crewai import Agent, Task, Crew, Process

from langchain.agents import load_tools
from langchain_openai import ChatOpenAI

# %%
url = "http://localhost:4321/v1/"  # lm studio
url = "http://localhost:11434/v1"  # ollama
url = "http://localhost:8000"  # litellm
llm = ChatOpenAI(
    base_url=url, api_key="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"
)
#%%
from langchain_experimental.utilities import PythonREPL
from langchain.agents import Tool

python_repl = PythonREPL()
repl_tool = Tool(
    name="python_repl",
    description="A Python shell. Use this to execute python commands. Input should be a valid python command. If you want to see the output of a value, you should print it out with `print(...)`.",
    func=python_repl.run,
)


human_tools = load_tools(["human"])
# %%
Script_writer = Agent(
    role="Python script writer",
    goal="""Generate ppython script based on a given task.""",
    backstory="""You are a great python coder that can produce 
    a python script based on a given task.""",
    verbose=True,
    allow_delegation=False,
    llm=llm,
)
Script_executor = Agent(
    role="Python script executor",
    goal="""responsible for actitivies 
    to execute  python scripts""",
    backstory="""Tou can execute given python scipts and 
    is necessary you can correnct errors and fix them.""",
    verbose=True,
    allow_delegation=False,
    tools=[human_tools, python_repl],
    llm=llm,
)


# %%
task_script = Task(
    description="""generate 10 random numbers between 0 and 100""",
    agent=Script_writer,
)

task_executor = Task(
    description="""Execute the script and print the results.""",
    agent=Script_executor,
)

# %%
crew = Crew(
    agents=[
        Script_writer,
        Script_executor,
    ],
    tasks=[
        task_script,
        task_executor,
    ],
    verbose=2,
)
# %%
result = crew.kickoff()
# %%
print("######################")
print(result)
