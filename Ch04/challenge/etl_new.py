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
from ipaddress import ip_address

# %%
df = pd.read_csv('traffic.csv', parse_dates=True)
df.head()

# %%
df['time'] = pd.to_datetime(df['time'], errors='coerce')
df.dtypes

# %%
df.describe()
http_responses = list(pd.Series(http.client.responses).index)
http_responses

# %%
def is_valid_row(row):
    # if ~row['ip'].str.match(r'[0-9]{3}\.'):
      # return False
    try:
        ip_address(row['ip'])
    except ValueError:
        return False
    if row['time'] > dt.now():
      return False
    if pd.isnull(row['path']) or row['path'].strip == '':
      return False
    if row['status'] not in http_responses:
      return False
    if row['size'] < 0 or pd.isnull(row['size']):
      return False
    return True

valid_rows = df[df.apply(is_valid_row, axis=1)]
valid_rows

# %%
invalid_rows = df[~df.index.isin(valid_rows.index)]
invalid_rows

# %%
df_valid = df.iloc[valid_rows.index]
df_valid

# %%
def load_df_to_sql(df):
  schema = '''
    CREATE TABLE IF NOT EXISTS traffic (
      ip TEXT,
      time DATETIME,
      path TEXT NOT NULL,
      status INT,
      size BIGINT
    );
  '''

  db_file = 'traffic.db'
  conn = sqlite3.connect(db_file)
  conn.executescript(schema)

  try:
    with conn as cur:
        cur.execute('BEGIN')
        df.to_sql('traffic', conn, if_exists='append', index=False)
  finally:
    conn.close()
  
  print('✓ SQL table traffic.db has been succesfully created and populated.')


# %%
def etl(valid_rows, invalid_rows):
  pct_invalid = 100 * len(invalid_rows) / (len(valid_rows) + len(invalid_rows))
  print('% invalid rows: ' + str(pct_invalid))
  if pct_invalid > 5:
    print('Too many bad values! Please correct before moving forward')
  else:
    print('Good to go!')
    load_df_to_sql(df_valid)

# %%
etl(valid_rows, invalid_rows)