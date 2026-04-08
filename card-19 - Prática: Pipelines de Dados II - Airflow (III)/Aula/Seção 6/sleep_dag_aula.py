# importação de bibliotecas 
import pprint as pp
import airflow.utils.dates
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.dummy_operator import DummyOperator
from datetime import datetime, timedelta

# definição das configurações 
default_args = {
        "owner": "airflow", 
        "start_date": airflow.utils.dates.days_ago(1)
    }

# instanciação da dag 
with DAG(dag_id="sleep_dag", default_args=default_args, schedule_interval="@daily") as dag:

    # tarefa dummy inicial
    t1 = DummyOperator(task_id="t1")

    # tarefa bash que pausa a execução
    t2 = BashOperator(
            task_id="t2",
            bash_command="sleep 30"
        )
    
    # definição do fluxo
    t1 >> t2