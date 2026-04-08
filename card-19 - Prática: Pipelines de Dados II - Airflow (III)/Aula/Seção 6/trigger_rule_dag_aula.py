# importação das bibliotecas 
import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

# definição das configurações básicas 
default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
}

# funções que simulam o download de websites
def download_website_a():
    print("download_website_a")

def download_website_b():
    print("download_website_b")

def download_failed():
    print("download_failed")

def download_succeed():
    print("download_succeed")

def process():
    print("process")

def notif_a():
    print("notif_a")

def notif_b():
    print("notif_b")

# instanciação da dag com agendamento diário
with DAG(dag_id='trigger_rule_dag', 
    default_args=default_args, 
    schedule_interval="@daily") as dag:

    # tarefa para download do website a
    download_website_a_task = PythonOperator(
        task_id='download_website_a',
        python_callable=download_website_a,
        trigger_rule="all_success"
    )

    # tarefa para download do website b 
    download_website_b_task = PythonOperator(
        task_id='download_website_b',
        python_callable=download_website_b,
        trigger_rule="all_success"    
    )

    # tarefa executada em caso de falha 
    download_failed_task = PythonOperator(
        task_id='download_failed',
        python_callable=download_failed,
        trigger_rule="all_success"
    )

    # tarefa executada em caso de sucesso 
    download_succeed_task = PythonOperator(
        task_id='download_succeed',
        python_callable=download_succeed,
        trigger_rule="all_success"
    )

    # tarefa de processamento principal
    process_task = PythonOperator(
        task_id='process',
        python_callable=process,
        trigger_rule="all_success"
    )

    # tarefa de notificação tipo a
    notif_a_task = PythonOperator(
        task_id='notif_a',
        python_callable=notif_a,
        trigger_rule="all_success"
    )

    # tarefa de notificação tipo b
    notif_b_task = PythonOperator(
        task_id='notif_b',
        python_callable=notif_b,
        trigger_rule="all_success"
    )
