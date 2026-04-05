from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

default_args = {
    'start_date': datetime(2026, 1, 1),
    'owner': 'Ronny_Pratica',
}

with DAG(dag_id='pool_pratica_dag', schedule='@daily', default_args=default_args, catchup=False) as dag:

    t1 = BashOperator(task_id='carga_01', bash_command='sleep 5', pool='default_pool')
    t2 = BashOperator(task_id='carga_02', bash_command='sleep 5', pool='default_pool')
    t3 = BashOperator(task_id='carga_03', bash_command='sleep 5', pool='default_pool')

    #execuções
    [t1, t2, t3]