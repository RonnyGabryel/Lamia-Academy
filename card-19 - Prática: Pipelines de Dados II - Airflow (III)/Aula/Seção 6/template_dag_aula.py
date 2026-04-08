# importação de bibliotecas 
import sys
import airflow
from airflow import DAG, macros
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from airflow.operators.postgres_operator import PostgresOperator
from datetime import datetime, timedelta

# inclusão do caminho dos scripts no pythonpath
sys.path.insert(1, '/usr/local/airflow/dags/scripts')

# importação de função personalizada
from process_logs import process_logs_func

# definição das configurações de execução
default_args = {
            "owner": "Airflow",
            "start_date": airflow.utils.dates.days_ago(1),
            "depends_on_past": False,
            "email_on_failure": False,
            "email_on_retry": False,
            "email": "youremail@host.com",
            "retries": 1
        }

# instanciação da dag com agendamento
with DAG(dag_id="template_dag", schedule_interval="@daily", default_args=default_args) as dag:

    # tarefa bash que imprime a data
    t0 = BashOperator(
            task_id="t0",
            bash_command="echo {{ macros.ds_format(ts_nodash, '%Y%m%dT%H%M%S', '%Y-%m-%d-%H-%M') }}")

    # tarefa bash que executa script
    t1 = BashOperator(
            task_id="generate_new_logs",
            bash_command="./scripts/generate_new_logs.sh",
            params={'filename': 'log.csv'})

    #t2 = BashOperator(
    #        task_id="logs_exist",
    #        bash_command="test -f " + TEMPLATED_LOG_DIR + "log.csv",
    #        )

    #t3 = PythonOperator(
    #        task_id="process_logs",
    #        python_callable=process_logs_func,
    #        provide_context=,
    #        templates_dict=,
    #        params={'filename': 'log.csv'}
    #        )

    # definição da sequência do fluxo de tarefas
    #t0 >> t1 >> t2 >> t3