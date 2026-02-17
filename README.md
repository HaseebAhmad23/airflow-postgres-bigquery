# Airflow EL Pipeline – PostgreSQL to BigQuery

This repository contains the Extraction & Loading (EL) layer of an end-to-end Data Engineering pipeline.

The pipeline extracts data from PostgreSQL and loads it into Google BigQuery, preparing it for downstream transformation with dbt.

## Architecture Overview
```
PostgreSQL (Webshop DB)
        ↓
Apache Airflow DAG
        ↓
Python Operators
        ↓
Google BigQuery (raw_data dataset)
```
This project focuses exclusively on orchestration and data ingestion.

---

## Technologies Used

1. Apache Airflow (Docker-based setup)

2. PostgreSQL

3. Google BigQuery

4. Python

5. Google Cloud Service Accounts
   
---

## Project Structure
```
airflow-postgres-bigquery/
│
├── dags/
│ └── postgres_to_bigquery.py
│
├── Dockerfile
├── docker-compose.yaml
├── .gitignore
└── README.md
```
---

## Pipeline Flow

1. Connect to PostgreSQL source database

2. Extract tables (customer, order, order_positions, products)

3. Transform minimal structure for loading

4. Load into BigQuery raw_data dataset

5. Prepare data for dbt transformation layer

---

## Setup Instructions

### 1️ Install Docker (v24+ recommended)
```
docker --version
docker compose version
```
---

### 2️ Build Custom Airflow Image
```
docker compose build --no-cache
docker compose up airflow-init
docker compose up
```
---

### 3️ Configure Google BigQuery Credentials

- Create a `keys/` folder and place your service account JSON file:
```
airflow-project/keys/gcp-key.json
```
- Note: This folder is ignored in `.gitignore` and should never be committed.

- Update docker-compose environment:
```
GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/keys/gcp-key.json
```
---

### 4️ Access Airflow UI

http://localhost:8080

Default credentials:

- Username: airflow
- Password: airflow

---

## DAG Behavior

The DAG:

- Connects to PostgreSQL
- Extracts data from:
  - customer
  - products
  - order
  - order_positions
- Loads each table into BigQuery `raw_data` dataset
- Uses WRITE_TRUNCATE mode

---

## Key Concepts Demonstrated

- Docker networking
- Airflow DAG design
- PythonOperator usage
- Postgres extraction
- BigQuery loading via dataframe
- Secure credential handling
- Infrastructure troubleshooting

---

## Security

- No credentials stored in repository
- Service account keys are excluded via `.gitignore`
- No secrets are stored in the repository

---

##  Author
 Haseeb Ahmad  (Full-Stack Developer)

