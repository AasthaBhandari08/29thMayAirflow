from google.cloud import bigquery
from google.oauth2 import service_account
import os
import csv
import datetime
import json
import os
import pandas as pd
from pandas import DataFrame

import requests
import datetime
from datetime import timedelta
from airflow.models import XCom
from airflow.utils.dates import days_ago

# import airflow
# from airflow import DAG
# from airflow.operators.bash_operator import BashOperator
# from airflow.operators.python_operator import PythonOperator


os.environ["GOOGLE_APPLICATION_CREDENTIALS"] = "/home/nineleaps/Downloads/airflow29thMay-1d5c1ef708db.json"

# Put your own project id here
PROJECT_ID = 'airflow29thmay-08'

# create a client instance for your project
client = bigquery.Client()

# create a new datset
client.create_dataset("covid19")
DATA_SET_ID='covid19'

TABLE = "covid_data"
# rows_uploaded = 0


def fetch_covid_data():
    JSONContent = requests.get("https://api.covid19india.org/data.json").json()

    if 'error' not in JSONContent:
        channels_list = JSONContent["statewise"]
    channel = []
    c = 0.0
    for i in channels_list:
        c = c+1
        channel.append([i['state'], i['lastupdatedtime'], i['confirmed']])
    channel = channel[1:]

    dataset = DataFrame(channel, columns=['State', 'Lastupdatedtime', 'Confirmed'])
    dataset.sample(5)
    dataset.to_csv('file1.csv',encoding='utf-8',sep= '\t', index=False)
    return c

def upload_covid_data_BQ():
    # tell the client everything it needs to know to upload our csv
    dataset_ref = client.dataset(DATA_SET_ID)
    table_ref = dataset_ref.table(TABLE)
    job_config = bigquery.LoadJobConfig()
    job_config.source_format = bigquery.SourceFormat.CSV
    # job_config.skip_leading_rows = 1
    job_config.autodetect = True
    job_config.schema_update_options = ['ALLOW_FIELD_ADDITION']

    with open('/home/nineleaps/PycharmProjects/air/file1.csv', "rb") as source_file:
        job = client.load_table_from_file(source_file, table_ref, job_config=job_config)

    job.result()

    print("Loaded {} rows into {}:{}.".format(job.output_rows, DATA_SET_ID, TABLE))
    global rows_uploaded
    rows_uploaded = float(job.output_rows)
    return job.output_rows



def percentage_upload(**kwargs):
    # file = open("/home/nineleaps/Desktop/file1.csv")
    # reader = csv.reader(file)
    # total_rows= float(len(list(reader)))
    # print (total_rows-1,rows_uploaded)
    # print (type(total_rows-1),type(rows_uploaded))
    # print (((total_rows-1)/rows_uploaded)*100)

    ti = kwargs['ti']
    v1 = ti.xcom_pull(task_ids='source2')
    total_rows = ti.xcom_pull(task_ids='source1')
    print(type(v1),v1,total_rows)
    print("percentage = {}".format((v1 / (total_rows-1.0) * 100)))

# fetch_covid_data()
# upload_covid_data_BQ()
# percentage_upload()