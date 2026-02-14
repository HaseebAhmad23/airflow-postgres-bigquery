from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime
import pandas as pd
import psycopg2
from google.cloud import bigquery

def extract_and_load():
    # Connect to Postgres
    conn = psycopg2.connect(
        host="localhost",   # Important!
        database="webshop",
        user="postgres",
        password="postgres"
    )

    query = "SELECT * FROM webshop.customer;"
    df = pd.read_sql(query, conn)
    conn.close()

    if df.empty:
        print("No data found.")
        return

    print("Postgres data found.")

    client = bigquery.Client()
    table_id = "postgresql-store-database.raw_data.customer"

    job = client.load_table_from_dataframe(df, table_id)
    job.result()

    print(f"Loaded {len(df)} rows to BigQuery.")

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
