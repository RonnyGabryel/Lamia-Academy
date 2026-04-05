from airflow import DAG
from airflow.operators.trigger_dagrun import TriggerDagRunOperator
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# passando o ID do pedido e o valor via conf

default_args = {
    'owner': 'Ronny_Pratica',
    'start_date': datetime(2026, 1, 1),
}

def preparar_dados():
    print("Dados do pedido validados e prontos para envio ao DAG de processamento.")

with DAG(
    dag_id='triggerdagop_controller_pratica',
    default_args=default_args,
    schedule='@once',
    catchup=False,
    tags=['aula', 'trigger_dagrun']
) as dag:

    preparar = PythonOperator(
        task_id='preparar_dados_pedido',
        python_callable=preparar_dados
    )

    # Dispara o DAG alvo
    disparar = TriggerDagRunOperator(
        task_id='disparar_processamento_pedido',
        trigger_dag_id='triggerdagop_target_pratica',  # DAG que sera disparado
        conf={
            'pedido_id': 'PED-2026-001',
            'valor': 350.00,
            'cliente': 'Ronny'
        },
        wait_for_completion=False  # não bloqueia este DAG aguardando o outro terminar
    )

    fim = EmptyOperator(task_id='fim')

    preparar >> disparar >> fim
