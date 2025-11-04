import argparse
import os
from pathlib import Path
import pandas as pd
from google.cloud import bigquery

DEFAULT_CSV_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"

def download_csv(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(url)
    df.to_csv(dest, index=False)
    print(f"CSV salvo em: {dest}")
    return dest

def create_dataset_if_not_exists(client: bigquery.Client, dataset_id: str, location: str = "US"):
    dataset_ref = bigquery.Dataset(f"{client.project}.{dataset_id}")
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset já existe: {dataset_id}")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location
        client.create_dataset(dataset)
        print(f"Dataset criado: {dataset_id} (location={location})")

def upload_dataframe_to_bq(client: bigquery.Client, df: pd.DataFrame, dataset_id: str, table_id: str):
    destination = f"{client.project}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE", autodetect=True)
    job = client.load_table_from_dataframe(df, destination, job_config=job_config)
    job.result()
    table = client.get_table(destination)
    print(f"Tabela carregada: {destination} — linhas: {table.num_rows}")
import argparse
import os
from pathlib import Path
import pandas as pd
from google.cloud import bigquery

DEFAULT_CSV_URL = "https://raw.githubusercontent.com/IBM/telco-customer-churn-on-icp4d/master/data/Telco-Customer-Churn.csv"


def download_csv(url: str, dest: Path) -> Path:
    dest.parent.mkdir(parents=True, exist_ok=True)
    df = pd.read_csv(url)
    df.to_csv(dest, index=False)
    print(f"CSV salvo em: {dest}")
    return dest


def create_dataset_if_not_exists(client: bigquery.Client, dataset_id: str, location: str = "US"):
    dataset_ref = bigquery.DatasetReference(client.project, dataset_id)
    try:
        client.get_dataset(dataset_ref)
        print(f"Dataset já existe: {dataset_id}")
    except Exception:
        dataset = bigquery.Dataset(dataset_ref)
        dataset.location = location
        client.create_dataset(dataset)
        print(f"Dataset criado: {dataset_id} (location={location})")


def upload_dataframe_to_bq(client: bigquery.Client, df: pd.DataFrame, dataset_id: str, table_id: str):
    destination = f"{client.project}.{dataset_id}.{table_id}"
    job_config = bigquery.LoadJobConfig(write_disposition="WRITE_TRUNCATE", autodetect=True)
    job = client.load_table_from_dataframe(df, destination, job_config=job_config)
    job.result()
    table = client.get_table(destination)
    print(f"Tabela carregada: {destination} — linhas: {table.num_rows}")


def main(args):
    project = args.project
    dataset = args.dataset
    table = args.table
    csv_url = args.csv_url

    os.environ.setdefault("GOOGLE_CLOUD_PROJECT", project)
    client = bigquery.Client(project=project)

    local_csv = Path("data/raw/telco_churn.csv")
    download_csv(csv_url, local_csv)

    df = pd.read_csv(local_csv)
    print(f"Linhas carregadas localmente: {len(df)} — colunas: {list(df.columns)[:10]}...")

    if args.upload:
        create_dataset_if_not_exists(client, dataset, location=args.location)
        upload_dataframe_to_bq(client, df, dataset, table)
    else:
        print("Upload para BigQuery ignorado (--upload não fornecido).")


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Baixa CSV Telco e opcionalmente envia para BigQuery")
    parser.add_argument("--project", required=True, help="GCP project id")
    parser.add_argument("--dataset", default="churn_data", help="BigQuery dataset name")
    parser.add_argument("--table", default="telco_churn_raw", help="BigQuery table name")
    parser.add_argument("--csv-url", default=DEFAULT_CSV_URL, help="URL do CSV a ser baixado")
    parser.add_argument("--location", default="US", help="BigQuery dataset location")
    parser.add_argument("--upload", action="store_true", help="Enviar para BigQuery")
    args = parser.parse_args()
    main(args)
