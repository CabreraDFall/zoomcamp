#!/usr/bin/env python
# coding: utf-8

# In[14]:


import pandas as pd


# In[15]:


prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
df = pd.read_csv(prefix + 'yellow_tripdata_2021-01.csv.gz', nrows=100)


# In[16]:


# Display first rows
df.head()


# In[17]:


# Check data types
df.dtypes


# In[18]:


# Check data shape
df.shape


# In[19]:


dtype = {
    "VendorID": "Int64",
    "passenger_count": "Int64",
    "trip_distance": "float64",
    "RatecodeID": "Int64",
    "store_and_fwd_flag": "string",
    "PULocationID": "Int64",
    "DOLocationID": "Int64",
    "payment_type": "Int64",
    "fare_amount": "float64",
    "extra": "float64",
    "mta_tax": "float64",
    "tip_amount": "float64",
    "tolls_amount": "float64",
    "improvement_surcharge": "float64",
    "total_amount": "float64",
    "congestion_surcharge": "float64"
}

parse_dates = [
    "tpep_pickup_datetime",
    "tpep_dropoff_datetime"
]

df = pd.read_csv(
    prefix + 'yellow_tripdata_2021-01.csv.gz',
    nrows=100,
    dtype=dtype,
    parse_dates=parse_dates
)


# In[20]:


df.head()


# In[21]:


# Check data types
df.dtypes


# In[15]:


get_ipython().system('uv add sqlalchemy "psycopg[binary,pool]"')


# In[22]:


from sqlalchemy import create_engine
engine = create_engine('postgresql+psycopg://root:root@pg-database:5432/ny_taxi')


# In[23]:


print(pd.io.sql.get_schema(df, name='yellow_taxi_data', con=engine))


# In[24]:


df.head(n=0).to_sql(name='yellow_taxi_data', con=engine, if_exists='replace')


# In[25]:


df_iter = pd.read_csv(
     prefix + 'yellow_tripdata_2021-01.csv.gz',
    dtype=dtype,
    parse_dates=parse_dates,
    iterator=True,
    chunksize=100000,
)


# In[32]:


for df_chunk in df_iter:
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:


from tqdm.auto import tqdm

for df_chunk in tqdm(df_iter):
    df_chunk.to_sql(name='yellow_taxi_data', con=engine, if_exists='append')


# In[ ]:




