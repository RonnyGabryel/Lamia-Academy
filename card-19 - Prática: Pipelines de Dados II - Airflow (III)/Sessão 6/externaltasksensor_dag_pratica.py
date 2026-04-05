from airflow import DAG
from airflow.sensors.external_task import ExternalTaskSensor 
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from datetime import datetime

# Este DAG aguarda o DAG de processamento de pagamentos concluir

default_args = {
    'owner': 'Ronny_Pratica',
    'start_date': datetime(2026, 1, 1),
}

def liberar_envio():
    print("Pagamento confirmado! Liberando separação do produto no estoque.")

def notificar_cliente():
    print("Notificação enviada ao cliente: seu pedido está a caminho!")

with DAG(
    dag_id='externalsensor_pratica_dag',
    default_args=default_args,
    schedule='@daily',
    catchup=False,
    tags=['aula', 'sensor']
) as dag:

    # Aguarda a task confirmar_pagamento do DAG de pagamentos concluir
    aguardar_pagamento = ExternalTaskSensor(
        task_id='aguardar_confirmacao_pagamento',
        external_dag_id='pagamentos_dag',       # DAG que precisa terminar primeiro
        external_task_id='confirmar_pagamento', # task específica que deve ter sucesso
        mode='poke',      # verifica periodicamente 
        timeout=600,      # desiste após 10 minutos
        poke_interval=30  # verifica a cada 30 segundos
    )

    liberar = PythonOperator(
        task_id='liberar_envio',
        python_callable=liberar_envio
    )

    notificar = PythonOperator(
        task_id='notificar_cliente',
        python_callable=notificar_cliente
    )

    fim = EmptyOperator(task_id='fim')

    aguardar_pagamento >> liberar >> notificar >> fim
