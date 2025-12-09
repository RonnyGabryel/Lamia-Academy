from airflow import DAG
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Função Python executada pela task 1
def first_task():
    print("Hello from first task")

# Função Python executada pela task 2
def second_task():
    print("Hello from second task")

# Função Python executada pela task 3
def third_task():
    print("Hello from third task")

# Configurações padrão da DAG
default_args = {
    'start_date': datetime(2019, 1, 1),  # Data de início: 01/01/2019
    'owner': 'Airflow'
}

# Criação da DAG
with DAG(
    dag_id='packaged_dag',  # Nome da DAG
    schedule_interval="0 0 * * *",  # Executa diariamente à meia-noite
    default_args=default_args
) as dag:

    # Task 1 executa função first_task()
    python_task_1 = PythonOperator(task_id='python_task_1', python_callable=first_task)

    # Task 2 executa função second_task()
    python_task_2 = PythonOperator(task_id='python_task_2', python_callable=second_task)

    # Task 3 executa função third_task()
    python_task_3 = PythonOperator(task_id='python_task_3', python_callable=third_task)

    # Define a ordem task_1 > task_2 > task_3 (sequencial)
    python_task_1 >> python_task_2 >> python_task_3