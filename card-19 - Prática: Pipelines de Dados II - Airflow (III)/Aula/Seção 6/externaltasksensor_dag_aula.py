# importação de bibliotecas 
import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.sensors.external_task_sensor import ExternalTaskSensor
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# definição das configurações básicas 
default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(1)
    }

# instanciação da dag 
with DAG(dag_id="externaltasksensor_dag", default_args=default_args, schedule_interval="@daily") as dag:
    
    # sensor que aguarda a conclusão da tarefa t2 na dag externa sleep_dag
    sensor = ExternalTaskSensor(
        task_id='sensor',
        external_dag_id='sleep_dag',
        external_task_id='t2'    
    )

    # tarefa dummy final do fluxo
    last_task = DummyOperator(task_id="last_task")

    # definição do fluxo
    sensor >> last_task