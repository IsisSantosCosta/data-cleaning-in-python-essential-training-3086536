# %%
import re
import numpy as np
import pandas as pd

df = pd.read_csv('rides.csv')
df
# %%
# Find out all the rows that have bad values
# - Missing values are not allowed
# - A plate must be a combination of at least 3 upper case letters or digits
# - Distance much be bigger than 0
# %%

# %% MISSING VALUES
mv_array = df.loc[df.isnull().any(axis=1)].index
mv_issue = len(mv_array) * ['missing values']
mv = pd.DataFrame({'issue': mv_issue, 'row': mv_array})
mv

# %% INVALID PLATES
df.index
pl_all = pd.Series(df.index).apply(lambda x: x if x not in mv.index else '')
pl_all = list(df.index.difference(mv.index))
pl_all = list(df.index.difference(mv.index))
df['plate'].iloc[pl_all]

# %%
pattern = '^[A-Z0-9]{3}[A-Z0-9]*$'
valid_plates = []
for i in df['plate']: 
  if re.match(pattern, str(i)):
    valid_plates += [i]
print(valid_plates)

# %%
ip_ = []
for i in range(0, len(df)):
  if df.iloc[i,]['plate'] not in valid_plates:
    ip_ += [['invalid plates', i]]
    print(df.iloc[i,]['plate'])
ip = pd.DataFrame(ip_, columns=['issue', 'row'])
ip

# %%
pd.concat([mv,ip])

# %% DISTANCE <= 0 
nd_rows = []
for i in range(0, len(df)):
  if df.iloc[i,]['distance']<0:
    nd_rows += [['distance < 0', i]]
    print(df.iloc[i,]['plate'])
nd = pd.DataFrame(nd_rows, columns=['issue', 'row'])
nd

# %%
errors = pd.concat([mv, ip, nd])
errors.sort_values('row', inplace=True)
errors.set_index('row')

# %%
