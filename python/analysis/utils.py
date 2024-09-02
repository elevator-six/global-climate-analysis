import os
import pandas as pd
from google.cloud import bigquery

def init_bigquery():
    global client 
    client = bigquery.Client()

def fetch_data_from_bigquery(query):
    query_job = client.query(query)
    results = query_job.result()
    return results.to_dataframe()

def load_data_and_cache(cache_dir, queries_file, cleaned_data, label):
    with open(queries_file, 'r') as f:
        queries = [query.strip() for query in f.read().split(';') if query.strip()]

    formatted_queries = [query.format(cleaned_data=cleaned_data) for query in queries if query.strip()]

    dataframes = []
    for i, query in enumerate(formatted_queries):
        cache_file = os.path.join(cache_dir, f'df_{label}_{i+1}.csv') 

        if os.path.exists(cache_file):
            print(f'Loading {cache_file} from cache...')
            df = pd.read_csv(cache_file)
        else:
            print(f'Fetching data from BigQuery and saving to {cache_file}...')
            df = fetch_data_from_bigquery(query)
            df.to_csv(cache_file, index=False)

        dataframes.append(df)

    return dataframes