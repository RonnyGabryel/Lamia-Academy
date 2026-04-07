# importação das bibliotecas e operadores dummy e bash
from airflow import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# definição das configurações básicas da dag
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

# instanciação da dag com id e agendamento diário
with DAG(dag_id='queue_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # tarefas bash simulando carga intensiva 
    t_1_ssd = BashOperator(task_id='t_1_ssd', bash_command='echo "I/O intensive task"')

    t_2_ssd = BashOperator(task_id='t_2_ssd', bash_command='echo "I/O intensive task"')

    t_3_ssd = BashOperator(task_id='t_3_ssd', bash_command='echo "I/O intensive task"')

    # tarefas bash simulando carga intensiva de cpu
    t_4_cpu = BashOperator(task_id='t_4_cpu', bash_command='echo "CPU instensive task"')

    t_5_cpu = BashOperator(task_id='t_5_cpu', bash_command='echo "CPU instensive task"')

    # tarefa bash simulando dependência de spark
    t_6_spark = BashOperator(task_id='t_6_spark', bash_command='echo "Spark dependency task"')

    # tarefa dummy que serve apenas como ponto de sincronização final
    task_7 = DummyOperator(task_id='task_7')

    # todas as tarefas anteriores rodam em paralelo e convergem para a task_7
    [t_1_ssd, t_2_ssd, t_3_ssd, t_4_cpu, t_5_cpu, t_6_spark] >> task_7