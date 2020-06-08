from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from datetime import datetime
from airflow.utils.dates import days_ago
import requests
import pandas as pd
from airflow_tasks import *
import csv
import airflow
# from pandas.io import gbq
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
    'start_date': airflow.utils.dates.days_ago(0),
    'email': ['aasthabhandari08@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),

}

dag = DAG(
  dag_id='my_dag',
  description='Covid Data DAG',
  default_args=default_args)

t1 = PythonOperator(
  task_id='source1',
  python_callable=fetch_covid_data,
  dag=dag)

t2 = PythonOperator(
  task_id='source2',
  python_callable=upload_covid_data_BQ,
  dag=dag
)

t3 = PythonOperator(
  task_id='source3',
  python_callable=percentage_upload,
  provide_context =  True,
  dag=dag
)

t1 >> t2 >> t3
# upload_covid_data_BQ()
# fetch_covid_data()