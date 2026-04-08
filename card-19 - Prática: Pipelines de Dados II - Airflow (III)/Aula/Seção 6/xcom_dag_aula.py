# importação de bibliotecas
import airflow
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator
from airflow.operators.bash_operator import BashOperator

# definição das configurações 
args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(1),
}

# função que retorna um valor 
def push_xcom_with_return():
    return 'my_returned_xcom'

# função que recupera o valor 
def get_pushed_xcom_with_return(**context):
    print(context['ti'].xcom_pull(task_ids='t0')) 

# função que faz um push 
def push_next_task(**context):
    context['ti'].xcom_push(key='next_task', value='t3')

# função que recupera a chave 
def get_next_task(**context):
    return context['ti'].xcom_pull(key='next_task')

# função que recupera múltiplos valores
def get_multiple_xcoms(**context):
    print(context['ti'].xcom_pull(key=None, task_ids=['t0', 't2']))

# instanciação da dag 
with DAG(dag_id='xcom_dag', default_args=args, schedule_interval="@once") as dag:
    
    # tarefa python que envia valor via return
    t0 = PythonOperator(
        task_id='t0',
        python_callable=push_xcom_with_return
    )

    # tarefa python que lê o valor de t0
    t1 = PythonOperator(
        task_id='t1',
        provide_context=True,
        python_callable=get_pushed_xcom_with_return
    )

    # tarefa python que define manualmente o próximo passo 
    t2 = PythonOperator(
        task_id='t2',
        provide_context=True,
        python_callable=push_next_task
    )

    # operador de ramificação 
    branching = BranchPythonOperator(
        task_id='branching',
        provide_context=True,
        python_callable=get_next_task,
    )

    # tarefas dummy 
    t3 = DummyOperator(task_id='t3')
    t4 = DummyOperator(task_id='t4')

    # tarefa python que consolida
    t5 = PythonOperator(
        task_id='t5',
        trigger_rule='one_success',
        provide_context=True,
        python_callable=get_multiple_xcoms
    )

    # tarefa bash 
    t6 = BashOperator(
        task_id='t6',
        bash_command="echo value from xcom: {{ ti.xcom_pull(key='next_task') }}"
    )

    # definição do fluxo
    t0 >> t1
    t1 >> t2 >> branching
    branching >> t3 >> t5 >> t6
    branching >> t4 >> t5 >> t6