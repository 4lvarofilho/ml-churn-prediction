import os
from typing import Optional
import pandas as pd
from google.cloud import bigquery

def load_local_csv(path: str) -> pd.DataFrame:
    return pd.read_csv(path)

def load_from_bigquery(project: str, dataset: str, table: str, location: str = "US") -> pd.DataFrame:
    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project)
    client = bigquery.Client(project=project, location=location)
    query = f"SELECT * FROM `{project}.{dataset}.{table}`"
    df = client.query(query).result().to_dataframe(create_bqstorage_client=False)
    return df