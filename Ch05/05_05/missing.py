# %%
import pandas as pd


df = pd.read_csv('cart.csv', parse_dates=['date'])
df

# %% 
df['amount'].fillna(1, inplace=True)
df

# %%
most_common = df['name'].mode()[0]
df['name'].fillna(most_common, inplace=True)
df

# %%
df['date'].fillna(method='ffill', inplace=True)
df

# %%
df['price'].dropna()
prices = df.dropna(subset=['price']).groupby('name').mean()['price']
prices
# df.groupby(['name']).mean()['price']

# %%
df.merge(prices, how='left')

# %%
import numpy as np
prices = df.groupby('name')['price'].transform(np.mean)
prices

# %%
df['price'].fillna(prices, inplace=True)
df