# importação de utilitários de data
import airflow.utils.dates
from airflow.models import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator

# definição das configurações básicas 
default_args = {
    "start_date": airflow.utils.dates.days_ago(1), 
    "owner": "Airflow"
}

# função que recebe e imprime 
def remote_value(**context):
    print("Value {} for key=message received from the controller DAG".format(context["dag_run"].conf["message"]))

# instanciação da dag de destino
with DAG(dag_id="triggerdagop_target_dag", default_args=default_args, schedule_interval=None) as dag:

    # tarefa python que processa o valor 
    t1 = PythonOperator(
            task_id="t1",
            provide_context=True,
            python_callable=remote_value, 
        )

    # tarefa bash que imprime a mensagem 
    t2 = BashOperator(
        task_id="t2",
        bash_command='echo Message: {{ dag_run.conf["message"] if dag_run else "" }}')

    # tarefa bash que pausa 
    t3 = BashOperator(
        task_id="t3",
        bash_command="sleep 30"
    )