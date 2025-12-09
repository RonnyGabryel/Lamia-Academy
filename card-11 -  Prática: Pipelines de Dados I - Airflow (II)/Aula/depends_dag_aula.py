from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.dummy_operator import DummyOperator

from datetime import datetime, timedelta

# Configurações padrão da DAG
default_args = {
    'start_date': datetime(2025, 12, 8,), # Data de início:08/12/2025
    'owner': 'Airflow'
}

# Função Python que será executada pela task 2
def second_task():
    print('Hello from second_task')
    # raise ValueError('This will turns the python task in failed state')  # Comentado forçaria erro

# Função Python que será executada pela task 3
def third_task():
    print('Hello from third_task')
    # raise ValueError('This will turns the python task in failed state')  # Comentado forçaria erro

# Criação da DAG
with DAG(
    dag_id='depends_task',  # Nome da DAG
    schedule_interval="0 0 * * *",  # Executa diariamente à meia-noite
    default_args=default_args
) as dag:
    
    # Task 1 executa comando bash
    bash_task_1 = BashOperator(task_id='bash_task_1', bash_command="echo 'first task'")
    
    # Task 2 executa função Python second_task()
    python_task_2 = PythonOperator(task_id='python_task_2', python_callable=second_task)

    # Task 3 executa função Python third_task()
    python_task_3 = PythonOperator(task_id='python_task_3', python_callable=third_task)

    # Define a ordem bash_task_1 > python_task_2 > python_task_3 (sequencial)
    bash_task_1 >> python_task_2 >> python_task_3