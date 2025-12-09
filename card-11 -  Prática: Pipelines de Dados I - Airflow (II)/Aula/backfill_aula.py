from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from datetime import datetime, timedelta

# Configurações padrão da DAG
default_args = {
    'start_date': datetime(2025, 12, 8,),  # Data de início:08/12/2025 
    'owner': 'Airflow' 
}

# Criação da DAG
with DAG(
    dag_id='backfill',  # Nome da DAG
    schedule_interval="0 0 * * *",  # Executa diariamente à meia-noite (00:00)
    default_args=default_args,
    catchup=False  # NÃO executa datas passadas automaticamente
) as dag:
    
    # Task 1 executa comando bash que imprime first task
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'")
    
    # Task 2 executa comando bash que imprime second task
    bash_task_2 = BashOperator(task_id='bash_task_2', bash_command="echo 'second task'")

    # Define a ordem task_1 executa primeiro, depois task_2
    bash_task_1 >> bash_task_2