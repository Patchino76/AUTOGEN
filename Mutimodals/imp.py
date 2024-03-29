#%%
import torch
from transformers import AutoTokenizer, AutoModelForCausalLM
from PIL import Image

# %%
torch.set_default_device("cuda")

model = AutoModelForCausalLM.from_pretrained(
     "MILVLG/imp-v1-3b", 
    # return_dict=True,
    torch_dtype = torch.float16,
    device_map = "cuda",
    # low_cpu_mem_usage = True,
    trust_remote_code=True
)

tokenizer = AutoTokenizer.from_pretrained("MILVLG/imp-v1-3b", trust_remote_code=True)
# %%
text = """A chat between a curious user and an artificial intelligence assistant. 
    The assistant gives helpful, detailed, and polite answers to the user's questions. 
    USER: <image>
    Analyze the excel table from the image and export the data in json format where each column name is a key.
    ASSISTANT:"""
image = Image.open("img/table_small.jpg")
# %%
input_ids = tokenizer(text, return_tensors="pt").input_ids
image_tensor = model.image_preprocess(image)
output_ids = model.generate(
    input_ids=input_ids,
    max_new_tokens=1000,
    images = image_tensor,
    use_cache=True
    )[0]

# %%
print(tokenizer.decode(output_ids[input_ids.shape[1]:], skip_special_tokens=True).strip())
# %%
