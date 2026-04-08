# importação de bibliotecas
import airflow
from subdags.subdag import factory_subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.executors.sequential_executor import SequentialExecutor
from airflow.executors.celery_executor import CeleryExecutor

# definição do nome 
DAG_NAME="test_subdag"

# configurações básicas com data de início dinâmica
default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2)
}

# instanciação da dag principal para execução única
with DAG(dag_id=DAG_NAME, default_args=default_args, schedule_interval="@once") as dag:
    
    # tarefa dummy de início do fluxo
    start = DummyOperator(
        task_id='start'
    )

    # definição da primeira subdag 
    subdag_1 = SubDagOperator(
        task_id='subdag-1',
        subdag=factory_subdag(DAG_NAME, 'subdag-1', default_args),
        executor=SequentialExecutor()
    )

    # tarefa dummy intermediária 
    some_other_task = DummyOperator(
        task_id='check'
        )

    # definição da segunda subdag 
    subdag_2 = SubDagOperator(
        task_id='subdag-2',
        subdag=factory_subdag(DAG_NAME, 'subdag-2', default_args),
        executor=SequentialExecutor()
    )

    # tarefa dummy de finalização
    end = DummyOperator(
        task_id='final'
    )

    # definição da ordem 
    start >> subdag_1 >> some_other_task >> subdag_2 >> end