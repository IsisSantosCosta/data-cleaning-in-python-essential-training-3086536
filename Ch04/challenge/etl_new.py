"""
Load traffic.csv into "traffic" table in sqlite3 database.

Drop and report invalid rows.
- ip should be valid IP (see ipaddress)
- time must not be in the future
- path can't be empty
- status code must be a valid HTTP status code (see http.HTTPStatus)
- size can't be negative or empty

Report the percentage of bad rows. Fail the ETL if there are more than 5% bad rows
"""

# %%
import pandas as pd
import sqlite3
from datetime import datetime as dt
import http.client

# %%
df = pd.read_csv('traffic.csv', parse_dates=True)
df.head()

# %%
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df.dtypes

# %%
df.describe()
http_responses = pd.DataFrame(http.client.responses)
http_responses

# %%
def is_valid_row(row):
    # if ip
    if row['time'] > dt.now():
        return False
    if pd.isnull(row['path']) or row['path'].strip == '':
        return False
    return True
valid_rows = df[df.apply(is_valid_row, axis=1)]
valid_rows

# %%
invalid_rows = df[~df.index.isin(valid_rows.index)]
invalid_rows