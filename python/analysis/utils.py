from google.cloud import bigquery

def init_bigquery():
    global client 
    client = bigquery.Client()

def fetch_data_from_bigquery(query):
    query_job = client.query(query)
    results = query_job.result()
    return results.to_dataframe()