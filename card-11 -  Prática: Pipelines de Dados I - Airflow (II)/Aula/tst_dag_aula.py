from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime, timedelta

# Configurações padrão da DAG
default_args = {
    'start_date': datetime(2019, 1, 1)  # Data de início: 01/01/2019
}

# Função Python simples que retorna uma string
def process():
    return 'process'

# Criação da DAG
with DAG(
    dag_id='tst_dag',  # Nome da DAG
    schedule_interval='0 0 * * *',  # Executa diariamente à meia-noite
    default_args=default_args,
    catchup=False 
) as dag:
    
    # Task 1 task dummy (placeholder)
    task_1 = DummyOperator(task_id='task_1')

    # Task 2 executa função Python process()
    task_2 = PythonOperator(task_id='task_2', python_callable=process)

    # Tasks 3, 4 e 5 geradas DINAMICAMENTE em loop
    # Cria lista [task_3, task_4, task_5] automaticamente
    tasks = [DummyOperator(task_id='task_{0}'.format(t)) for t in range(3, 6)]

    # Task 6 task dummy final
    task_6 = DummyOperator(task_id='task_6')

    # Define dependências task_1 > task_2 > [task_3, task_4, task_5 em paralelo] > task_6
    task_1 >> task_2 >> tasks >> task_6