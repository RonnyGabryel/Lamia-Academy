# importação das bibliotecas do Airflow e operadores Bash e Python
from airflow import DAG
from airflow.operators.bash_operator import BashOperator
from airflow.operators.python_operator import PythonOperator
from datetime import datetime

# definição das configurações básicas da DAG
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

# função Python simples que imprime um parâmetro e retorna
def process(p1):
    print(p1)
    return 'done'

# instanciação da DAG com ID
with DAG(dag_id='parallel_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # criação dinâmica de 3 tarefas Bash task_1, task_2, task_3
    tasks = [BashOperator(task_id='task_{0}'.format(t), bash_command='sleep 5'.format(t)) for t in range(1, 4)]

    # tarefa que executa a função Python 
    task_4 = PythonOperator(task_id='task_4', python_callable=process, op_args=['my super parameter'])

    # tarefa Bash que imprime uma mensagem de finalização no log
    task_5 = BashOperator(task_id='task_5', bash_command='echo "pipeline done"')

    # definição do fluxo as 3 tarefas
    tasks >> task_4 >> task_5