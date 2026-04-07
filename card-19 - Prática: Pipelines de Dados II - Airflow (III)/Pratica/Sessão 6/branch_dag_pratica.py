from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import BranchPythonOperator, PythonOperator
from datetime import datetime

# Branch DAG
default_args = {
    'owner': 'Ronny_Pratica',
    'start_date': datetime(2026, 1, 1),
}

def verificar_tipo_pedido(**context):
    # Branch baseado no valores simulados
    valor = 150  # em produção viria de uma variavel 
    if valor < 100:
        return 'pedido_pequeno'
    elif valor < 500:
        return 'pedido_medio'
    else:
        return 'pedido_grande'

def processar_pequeno():
    print("Pedido pequeno: envio padrão em até 7 dias")

def processar_medio():
    print("Pedido médio: envio expresso em até 3 dias")

def processar_grande():
    print("Pedido grande: envio prioritário com seguro incluso")

def finalizar_pedido():
    print("Pedido registrado e confirmação enviada ao cliente!")

with DAG(
    dag_id='branch_pratica_dag',
    default_args=default_args,
    schedule=None,  # schedule em vez de schedule_interval
    catchup=False,
    tags=['aula', 'branch']
) as dag:

    inicio = EmptyOperator(task_id='inicio')  # EmptyOperator substitui DummyOperator 

    branch = BranchPythonOperator(
        task_id='verificar_tipo_pedido',
        python_callable=verificar_tipo_pedido
    )

    pequeno = PythonOperator(task_id='pedido_pequeno', python_callable=processar_pequeno)
    medio   = PythonOperator(task_id='pedido_medio',   python_callable=processar_medio)
    grande  = PythonOperator(task_id='pedido_grande',  python_callable=processar_grande)
    
    # garantir q o end roda
    fim = EmptyOperator(
        task_id='fim',
        trigger_rule='none_failed_min_one_success'
    )

    inicio >> branch
    branch >> [pequeno, medio, grande]
    [pequeno, medio, grande] >> fim
