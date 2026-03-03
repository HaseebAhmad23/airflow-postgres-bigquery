# End-to-End ELT Pipeline – PostgreSQL → BigQuery → dbt

![PostgreSQL](https://img.shields.io/badge/PostgreSQL-Database-336791?style=for-the-badge&logo=postgresql&logoColor=white)
![Apache Airflow](https://img.shields.io/badge/Apache_Airflow-Orchestration-24bfbd?style=for-the-badge&logo=apacheairflow&logoColor=white)
![Google BigQuery](https://img.shields.io/badge/BigQuery-Data_Warehouse-6dbf24?style=for-the-badge&logo=googlebigquery&logoColor=white)
![dbt](https://img.shields.io/badge/dbt-Transformations-FF694B?style=for-the-badge&logo=dbt&logoColor=white)
![Python](https://img.shields.io/badge/Python-3.x-bf7524?style=for-the-badge&logo=python&logoColor=white)
![Docker](https://img.shields.io/badge/Docker-Containerized-bf248b?style=for-the-badge&logo=docker&logoColor=white)

This repository contains a complete **ELT (Extract, Load, Transform)** data pipeline built using modern data engineering tools. built using modern data engineering tools. The pipeline extracts data from PostgreSQL, loads it into Google BigQuery using Apache Airflow, and then transforms raw BigQuery data into analytics-ready dimensional models using dbt. 

---

## Architecture Overview

```
PostgreSQL (Webshop Database)
        ↓
Apache Airflow DAG
        ↓
Python Extraction & Loading
        ↓
BigQuery `raw_data` dataset
        ↓
dbt Transformations
        ↓
BigQuery `transform_data` dataset
```

The architecture separates the pipeline into two layers:

- **EL layer** – Extracts data from PostgreSQL and loads it into Google BigQuery using Apache Airflow
- **Transformation layer** – Transforms raw BigQuery data into analytics-ready dimensional models using dbt

---

## Technologies Used

| Tool | Purpose |
|---|---|
| Apache Airflow (Docker) | Orchestration & scheduling |
| PostgreSQL | Source database |
| Google BigQuery | Cloud data warehouse |
| Python | EL scripting |
| dbt (v1.8.x) | SQL-based transformations |
| Docker | Containerized Airflow environment |
| Google Cloud Service Accounts | Authentication |
| GitHub Actions | (CI/CD) pipeline |
---

## Project Structure

```
elt-pipeline/
│
├── dags/
│   └── postgres_to_bigquery.py      # Airflow DAG for (Extract + Load)
│
├── dbt_transformation/
│   ├── models/
│   │   ├── staging/    # Data cleaning & standardization
│   │   │   ├── stg_customer.sql
│   │   │   ├── stg_order.sql
│   │   │   └── stg_webshop_db.yml
│   │   ├── marts/      # Dimensional models
│   │   │   ├── dim_customer.sql
│   │   │   └── marts_webshop_db.yml
│   │   └── src_webshop_db.yml
│   └── dbt_project.yml
│
├── Dockerfile
├── docker-compose.yaml      # Airflow stack 
├── keys/                    # Service account key 
├── README.md
├── .github/workflows/
│   └── main.yml             # CI/CD pipeline
│
└── .env                     # Environment variables
```

---

## EL Layer — Extraction & Loading 

### Airflow Pipeline

1. Connect to PostgreSQL source database
2. Extract tables: `customer`, `order`, `order_positions`, `products`
3. Apply minimal structural transformation for loading
4. Load each table into BigQuery `raw_data` dataset using `WRITE_TRUNCATE` mode

### Setup Instructions

#### 1. Install Docker (v24+ recommended)

```bash
docker --version
docker compose version
```

#### 2. Build Custom Airflow Image & Start Services

```bash
docker compose build --no-cache
docker compose up airflow-init
docker compose up
```

#### 3. Configure Google BigQuery Credentials

Create a `keys/` folder and place your service account JSON file:

```
elt-pipeline/keys/gcp-key.json
```

> This folder is excluded via `.gitignore` and must never be committed.

Update the environment variable in `docker-compose.yaml`:

```yaml
GOOGLE_APPLICATION_CREDENTIALS=/opt/airflow/keys/gcp-key.json
```

#### 4. Access Airflow UI

Open [http://localhost:8080](http://localhost:8080)

Default credentials:
- **Username:** airflow
- **Password:** airflow

### DAG Behavior

The `postgres_to_bigquery` DAG:

- Connects to the PostgreSQL source
- Extracts the following tables: `customer`, `products`, `order`, `order_positions`
- Loads each table into BigQuery `raw_data` dataset
- Uses `WRITE_TRUNCATE` mode (full refresh on each run)

---

## Transformation Layer — dbt

### Data Warehouse Setup

- **BigQuery Project:** `postgresql-store-database`
- **Datasets:**
  - `raw_data` → Ingested source data (populated by Airflow)
  - `transform_data` → dbt-generated analytical models

### Transformation Layers

#### Staging Layer (`models/staging/`)

Purpose:
- Clean raw data
- Rename columns consistently
- Convert data types (e.g. nanosecond timestamps → BigQuery `TIMESTAMP`)
- Cast string monetary fields to `NUMERIC`
- Standardize primary/foreign key naming

Materialization: **Views**

#### Marts Layer (`models/marts/`)

Purpose:
- Build analytics-ready dimensional models
- Create aggregated metrics for BI and reporting

`dim_customer` includes:
- First and most recent order dates
- Total number of orders
- Geographic information
- Cleaned customer attributes

Materialization: **Tables**

### Data Quality & Testing

dbt schema tests are implemented across both layers:

- `unique`
- `not_null`
- `relationships`
- `accepted_values`

These tests enforce primary key validity, foreign key integrity, and business rules.

### How to Run dbt

#### 1. Install dbt for BigQuery

```bash
pip install dbt-bigquery
```

#### 2. Configure `~/.dbt/profiles.yml`

```yaml
dbt_transformation:
  target: dev
  outputs:
    dev:
      type: bigquery
      method: service-account
      project: postgresql-store-database
      dataset: transform_data
      location: EU
      keyfile: /path/to/gcp-key.json
```

#### 3. Validate Connection

```bash
cd dbt_transformation
dbt debug
```

#### 4. Run Transformations

```bash
dbt run
```

#### 5. Run Tests

```bash
dbt test
```

#### 6. Generate & Serve Documentation

```bash
dbt docs generate
dbt docs serve
```

Open [http://localhost:8080](http://localhost:8080) to browse the interactive docs.

---

## Recommended Workflow

```
1. Start Airflow → triggers postgres_to_bigquery DAG
2. Airflow extracts PostgreSQL tables → loads into BigQuery raw_data
3. Run dbt → transforms raw_data into transform_data dimensional models
4. Query transform_data for analytics and reporting
```

---

## Key Concepts Demonstrated

- End-to-End ELT architecture
- Airflow workflow orchestration
- PostgreSQL data extraction
- BigQuery data warehousing
- dbt transformation modeling
- Data quality testing
- Secure credential handling
- Docker-based infrastructure
- CI/CD integration

---

## Security

- No credentials are stored in this repository
- Service account keys are excluded via `.gitignore`
- All secrets are injected at runtime via `.env`

---

## Author

Haseeb Ahmad (Full-Stack Developer)
