# %%
import pandas as pd

df = pd.read_csv('workshops.csv')
df
# %%
"""
Fix the data frame. At the end, row should have the following columns:
- start: pd.Timestemap
- end: pd.Timestamp
- name: str
- topic: str (python or go)
- earnings: np.float64
"""


# %%
year_mode = int(df['Year'].mode())
year_mode

# %%  YEAR
df['Year'] = df['Year'].fillna(year_mode).astype('int64')
df

# %%
df[~pd.isnull(df['Month'])]

# %% JUNE
for i in range(2, 5):
    df['Month'][i] = 'June'
df

# %% JULY
for i in range(5, 8):
    df['Month'][i] = 'July'
df

# %% MONTH NUMBER STRINGS
month_nstr = {'June': '06', 'July': '07'}
month_nstr
df['Month'] = df['Month'].map(month_nstr)
df

# %% DROP N/A
df.dropna(axis=0, inplace=True)
df

# %% START: DAY NUMBER STRINGS
df['Start'] = df['Start'].astype('int64').astype('str')
df['Start'] = df['Start'].apply(lambda x: x.zfill(2))
df

# %% End: DAY NUMBER STRINGS
df['End'] = df['End'].astype('int64').astype('str')
df['End'] = df['End'].apply(lambda x: x.zfill(2))
df

# %% START_DATE
start_date = pd.to_datetime(
    df['Year'].astype('str') + '-' +
    df['Month'] + '-' +
    df['Start'])
df['start'] = start_date
df

# %% END_DATE
end_date = pd.to_datetime(
    df['Year'].astype('str') + '-' +
    df['Month'] + '-' +
    df['End'])
df['end'] = end_date
df

# %%
df.dtypes

# %% NAME
df['name'] = df['Name']
df

# %% TOPIC
df['topic'] = df['Name'].apply(lambda x: 'go' if  'go' in x.lower() else 'python')
df

# %% EARNINGS
earnings = df['Earnings'].apply(lambda x: x.replace('$', ''))
earnings = earnings.apply(lambda x: x.replace(',', ''))
earnings = earnings.astype('float64')
df['earnings'] = earnings
df

# %% CLEAN UP
df.drop(df.columns[[0,1,2,3,4,5]], axis=1, inplace=True)
df

# %% EARNINGS BY TOPIC
pd.DataFrame(df.groupby('topic').mean()['earnings'])

# %% EARNINGS BY YEAR_MONTH
year_month = df['start'].astype('str').apply(lambda x: x[0:7])
year_month

# %%
pd.DataFrame(df.groupby(year_month).mean()['earnings'])