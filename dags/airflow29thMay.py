from airflow import DAG
# Operators; we need this to operate!
from airflow.operators.bash_operator import BashOperator
from datetime import timedelta
from datetime import datetime
from airflow.utils.dates import days_ago
import requests
<<<<<<< HEAD
import pandas as pd
from airflow_tasks import *
import csv
import airflow
# from pandas.io import gbq
=======
from pandas import DataFrame
import pandas as pd
import csv
from pandas.io import gbq
>>>>>>> 7727d8fde102f1d8b31d933b10ab653d770f8b7a
from airflow.operators.python_operator import PythonOperator


default_args = {
    'owner': 'airflow',
    'depends_on_past': False,
<<<<<<< HEAD
    'start_date': airflow.utils.dates.days_ago(0),
=======
    'start_date': datetime(2020, 6, 2),
>>>>>>> 7727d8fde102f1d8b31d933b10ab653d770f8b7a
    'email': ['aasthabhandari08@gmail.com'],
    'email_on_failure': False,
    'email_on_retry': False,
    'retries': 1,
<<<<<<< HEAD
    'retry_delay': timedelta(minutes=5),

}

dag = DAG(
  dag_id='my_dag',
  description='Covid Data DAG',
=======
    'retry_delay': timedelta(minutes=5)
}


def fetch_covid_data():
    JSONContent = requests.get("https://api.covid19india.org/data.json").json()

    if 'error' not in JSONContent:
        channels_list = JSONContent["statewise"]
    channel = []

    for i in channels_list:
        channel.append([i['state'], i['lastupdatedtime'], i['confirmed']])
    channel = channel[1:]

    dataset = DataFrame(channel, columns=['State', 'Lastupdatedtime', 'Confirmed'])
    dataset.sample(5)
    dataset.to_csv('file1.csv',encoding='utf-8', index=False)
    # path = '/home/nineleaps/PycharmProjects/air/file1.csv'
    # with open(path, 'r', encoding='utf-8') as infile, open(path + 'final.csv', 'w') as outfile:
    #     inputs = csv.reader(infile)
    #     output = csv.writer(outfile)
    #
    #     for index, row in enumerate(inputs):
    #         # Create file with no header
    #         if index == 0:
    #             continue
    #         output.writerow(row)

def upload_covid_data_BQ():
    # Import data from csv file
    data = pd.read_csv('/home/nineleaps/PycharmProjects/air/file1.csv',encoding='utf-8')
    # data = data.drop(data.columns[0], axis=1)

    data.to_gbq(destination_table='airflow.covid',
                project_id='airflow29thmay-08',
                if_exists='replace')

def flag_status():
    # Fetch Data from Big Query Table
    query = '''select count(*) from airflow.covid '''
    result = gbq.read_gbq(query, project_id='airflow29thmay-08')
    print(result)
    data = pd.read_csv('/home/nineleaps/PycharmProjects/air/file1.csv')
    total_rows = len(data.axes[0])
    print(total_rows)

dag = DAG(
  dag_id='my_dag',
  description='Simple tutorial DAG',
>>>>>>> 7727d8fde102f1d8b31d933b10ab653d770f8b7a
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
<<<<<<< HEAD
  python_callable=percentage_upload,
  provide_context =  True,
=======
  python_callable=flag_status,
>>>>>>> 7727d8fde102f1d8b31d933b10ab653d770f8b7a
  dag=dag
)

t1 >> t2 >> t3
# upload_covid_data_BQ()
# fetch_covid_data()