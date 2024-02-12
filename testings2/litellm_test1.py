#%%
import openai

openai.base_url = "http://localhost:8000"
# openai.base_url = "http://0.0.0.0:8000"
# openai.base_url = "http://localhost:11434"
openai.api_key = "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"

# %%
print(f'LiteLLM: response from proxy with streaming')
response = openai.chat.completions.create(
    model="ollama/llama2", 
    messages = [
        {
            "role": "user",
            "content": "this is a test request, acknowledge that you got it"
        }
    ],
    stream=True
)
# %%
for chunk in response:
    print(f'LiteLLM: streaming response from proxy {chunk}')
# %%
