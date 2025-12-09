from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# Configurações padrão da DAG
default_args = {
    "start_date": datetime(2025, 12, 8, 1),  # Data de início: 08/12/2025 às 01:00 2025,
    "owner": "Airflow"  # Dono da DAG
}

# Criação da DAG
with DAG(
    dag_id="start_and_schedule_dag",  # Nome único da DAG
    schedule_interval="0 * * * *",  
    default_args=default_args,
) as dag:

    # Primeira task 
    dummy_task_1 = DummyOperator(task_id="dummy_task_1")

    # Segunda task
    dummy_task_2 = DummyOperator(task_id="dummy_task_2")

    # Define a ordem task_1 executa primeiro, depois task_2
    dummy_task_1 >> dummy_task_2