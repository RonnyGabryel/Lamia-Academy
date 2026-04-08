# importação das bibliotecas 
import airflow
from subdags.subdag import factory_subdag
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.subdag_operator import SubDagOperator
from airflow.executors.celery_executor import CeleryExecutor

# definição do nome da dag principal
DAG_NAME="deadlock_subdag"

# configurações básicas e data de início
default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

# instanciação da dag para execução única
with DAG(dag_id=DAG_NAME, default_args=default_args, schedule_interval="@once") as dag:
    
    # tarefa inicial dummy
    start = DummyOperator(
        task_id='start'
    )

    # definição da subdag 1 
    subdag_1 = SubDagOperator(
        task_id='subdag-1',
        subdag=factory_subdag(DAG_NAME, 'subdag-1', default_args),
        executor=CeleryExecutor()
    )

    # definição da subdag 2 
    subdag_2 = SubDagOperator(
        task_id='subdag-2',
        subdag=factory_subdag(DAG_NAME, 'subdag-2', default_args),
        executor=CeleryExecutor()
    )

    # definição da subdag 3 
    subdag_3 = SubDagOperator(
        task_id='subdag-3',
        subdag=factory_subdag(DAG_NAME, 'subdag-3', default_args),
        executor=CeleryExecutor()
    )

    # definição da subdag 4 
    subdag_4 = SubDagOperator(
        task_id='subdag-4',
        subdag=factory_subdag(DAG_NAME, 'subdag-4', default_args),
        executor=CeleryExecutor()
    )

    # tarefa final dummy
    final = DummyOperator(
        task_id='final'
    )

    # fluxo
    start >> [subdag_1, subdag_2, subdag_3, subdag_4] >> final