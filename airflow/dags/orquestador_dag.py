from airflow import DAG
from airflow.providers.google.cloud.transfers.gcs_to_bigquery import GCSToBigQueryOperator
from airflow.utils.dates import days_ago
from datetime import datetime, timedelta
import requests
from airflow.operators.python_operator import PythonOperator
from airflow.models import Variable

default_args = {
    'owner': 'rafael-noriega',
    'start_date': days_ago(1),
    'depends_on_past': False,
    'retries': 1,
    'retry_delay': timedelta(minutes=5),
}

dag = DAG(
    'orquestador_dag',
    default_args=default_args,
    schedule_interval="@daily" 
)

project_id = 'prueba-da-dw'
dataset_id = 'raw'
gcs_bucket = 'prueba-da-dw-01'
table = 'incidentes'
filename = 'wr8u-xric'

def build_date(date):
    result_date = datetime.strptime(date, '%Y-%m-%dT%H:%M:%S.%f%z')
    return result_date.strftime('%Y%m%d')

def call_endpoint(**context):   

    execution_date = context["execution_date"]
    execution_date_str = str(execution_date)
    print(f"Execution date: {execution_date_str}")
    f_date = build_date(execution_date_str)

    url = f"https://api-incidentes-ae77s6na2q-ue.a.run.app/api/v1/incidentes/{f_date}"
    print(url)

    payload={}
    headers = {}

    response = requests.request("GET", url, headers=headers, data=payload)

    print(response.text)
    Variable.set("f_filename", f"{f_date}/{filename}-{f_date}.csv")


call_endpoint_operator = PythonOperator(
    task_id='call_endpoint',
    python_callable=call_endpoint,
    provide_context=True,
    dag=dag,
)

load_data_to_bq = GCSToBigQueryOperator(
        task_id='load_csv_file_to_bigquery',
        bucket=gcs_bucket,
        source_objects=[Variable.get("f_filename")],
        destination_project_dataset_table=f'{project_id}.{dataset_id}.{table}',
        schema_fields=[],  # Especificar el esquema si es necesario
        autodetect=True,
        create_disposition='CREATE_IF_NEEDED',
        write_disposition='WRITE_TRUNCATE',  
        source_format='CSV',
        dag=dag,
    ) 



call_endpoint_operator >> load_data_to_bq