from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
from google.cloud import bigquery

POSTGRES_HOST = "172.17.0.1"
POSTGRES_DB = "webshop"
POSTGRES_USER = "postgres"
POSTGRES_PASSWORD = "postgres"

BQ_PROJECT = "postgresql-store-database"
BQ_DATASET = "raw_data"

TABLES = [
    "customer",
    "products",
    "order",
    "order_positions"
]

def extract_and_load():
    # Connect to Postgres
    connection = psycopg2.connect(
        host=POSTGRES_HOST,
        database=POSTGRES_DB,
        user=POSTGRES_USER,
        password=POSTGRES_PASSWORD
    )

    client = bigquery.Client()

    for table in TABLES:
        print(f"Processing table: {table}")

        query = f"SELECT * FROM webshop.{table};"
        df = pd.read_sql(query, connection)

        if df.empty:
            print(f"No data found in {table}")
            continue

        table_id = f"{BQ_PROJECT}.{BQ_DATASET}.{table}"

        job = client.load_table_from_dataframe(
            df,
            table_id,
            job_config=bigquery.LoadJobConfig(
                write_disposition="WRITE_TRUNCATE"
            )
        )

        job.result()

        print(f"Loaded {len(df)} rows into {table}")

    connection.close()

with DAG(
    dag_id="postgres_to_bigquery",
    start_date=datetime(2024, 1, 1),
    schedule_interval=None,
    catchup=False,
) as dag:

    run_pipeline = PythonOperator(
        task_id="extract_and_load",
        python_callable=extract_and_load
    )
