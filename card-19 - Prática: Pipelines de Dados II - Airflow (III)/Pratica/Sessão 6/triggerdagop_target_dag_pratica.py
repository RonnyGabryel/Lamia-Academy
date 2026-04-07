from airflow import DAG
from airflow.operators.python import PythonOperator
from airflow.operators.bash import BashOperator
from airflow.operators.empty import EmptyOperator
from datetime import datetime

# Este DAG é disparado pelo controller e recebe os dados do pedido via conf

default_args = {
    'owner': 'Ronny_Pratica',
    'start_date': datetime(2026, 1, 1),
}

def processar_pedido(**context):
    # recupera os dados passados pelo controller via conf
    conf = context['dag_run'].conf
    pedido_id = conf.get('pedido_id', 'desconhecido')
    valor     = conf.get('valor', 0)
    cliente   = conf.get('cliente', 'desconhecido')

    print(f"Processando pedido {pedido_id} do cliente {cliente}")
    print(f"Valor total: R$ {valor:.2f}")

    if valor >= 300:
        print("Pedido qualifica para frete grátis!")
    else:
        print("Frete será calculado normalmente.")

def registrar_no_banco(**context):
    conf = context['dag_run'].conf
    pedido_id = conf.get('pedido_id', 'desconhecido')
    print(f"Pedido {pedido_id} registrado no banco de dados com sucesso.")

with DAG(
    dag_id='triggerdagop_target_pratica',
    default_args=default_args,
    schedule=None,  # nunca agendado só executa quando disparado pelo controller
    catchup=False,
    tags=['aula', 'trigger_dagrun']
) as dag:

    processar = PythonOperator(
        task_id='processar_pedido',
        python_callable=processar_pedido
    )

    registrar = PythonOperator(
        task_id='registrar_no_banco',
        python_callable=registrar_no_banco
    )

    #confirma via bash usando o conf recebido com template Jinja
    confirmar = BashOperator(
        task_id='confirmar_processamento',
        bash_command='echo "Pedido {{ dag_run.conf[\"pedido_id\"] if dag_run.conf else \"\" }} processado com sucesso!"'
    )

    fim = EmptyOperator(task_id='fim')

    processar >> registrar >> confirmar >> fim
