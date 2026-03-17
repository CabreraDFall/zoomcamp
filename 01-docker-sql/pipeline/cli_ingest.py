#!/ env python
# coding: utf-8

import click
import pandas as pd
from sqlalchemy import create_engine
from tqdm.auto import tqdm
import os

@click.command()
@click.option('--pg-user', default='root', help='Postgres username')
@click.option('--pg-pass', default='root', help='Postgres password')
@click.option('--pg-host', default='localhost', help='Postgres host')
@click.option('--pg-port', default=5432, help='Postgres port')
@click.option('--pg-db', default='ny_taxi', help='Postgres database name')
@click.option('--year', required=True, type=int, help='Year of the data')
@click.option('--month', required=True, type=int, help='Month of the data')
@click.option('--target-table', default='yellow_taxi_data', help='Target table name')
@click.option('--chunksize', default=100000, help='Chunk size for ingestion')
def main(pg_user, pg_pass, pg_host, pg_port, pg_db, year, month, target_table, chunksize):
    """
    Ingest NYC Taxi data into a Postgres database.
    """
    # Construct formatting for month
    month_str = f"{month:02d}"
    
    # Data URL
    prefix = 'https://github.com/DataTalksClub/nyc-tlc-data/releases/download/yellow/'
    csv_name = f'yellow_tripdata_{year}-{month_str}.csv.gz'
    url = prefix + csv_name
    
    print(f"Connecting to Postgres at {pg_host}:{pg_port}...")
    engine = create_engine(f'postgresql+psycopg://{pg_user}:{pg_pass}@{pg_host}:{pg_port}/{pg_db}')
    
    # Define schema types
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

    print(f"Downloading data from {url}...")
    
    # Read initial chunk to get schema
    df = pd.read_csv(url, nrows=100, dtype=dtype, parse_dates=parse_dates)
    
    # Create the table
    print(f"Creating table {target_table}...")
    df.head(n=0).to_sql(name=target_table, con=engine, if_exists='replace')

    # Re-open iterator for full ingestion
    df_iter = pd.read_csv(
        url,
        dtype=dtype,
        parse_dates=parse_dates,
        iterator=True,
        chunksize=chunksize,
    )

    print(f"Ingesting data into {target_table}...")
    for df_chunk in tqdm(df_iter):
        df_chunk.to_sql(name=target_table, con=engine, if_exists='append')

    print("Ingestion completed successfully!")

if __name__ == '__main__':
    main()
