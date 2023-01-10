from datetime import timedelta
from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from airflow.utils.dates import days_ago
from datetime import datetime
from twitter_etl import run_twitter_etl

# We define owner as owner and in case of having more DAG files 
# we would set depends_on_past as True, also you can modify the alerts.

default_args = {
    'owner': owner,
    'depends_on_past': False,
    'start_date': datetime(2023, 1, 8),
    'email': [airflow_email],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=1)
}

#Here we set the DAGS. Go to ./README.md for more.

dag = DAG(
    'twitter_dag',
    default_args=default_args,
    description='ETL process',
    schedule_interval=timedelta(days=1),
)

dag = DAG(
    'twitter_dag',
    default_args=default_args,
    description='etl code',
)

run_etl = PythonOperator(
    task_id='complete_twitter_etl',
    python_callable=run_twitter_etl,
    dag=dag, 
)

run_etl
