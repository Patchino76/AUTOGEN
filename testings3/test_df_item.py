#%%
import pandas as pd

data = {'A': [1, 4, 3], 'B': [4, 5, 6]}
df = pd.DataFrame(data)
df

#%%
for column_name, series in df.items():
    print(f"Column: {column_name}")
    print(series)
# %%
rez = [value for index, value in df['A'].items() if value > 1]
rez
# %%
