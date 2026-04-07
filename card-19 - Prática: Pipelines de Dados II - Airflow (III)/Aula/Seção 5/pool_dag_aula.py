# importação das bibliotecas e operadores http e bash
from airflow import DAG
from airflow.operators.http_operator import SimpleHttpOperator
from airflow.operators.bash_operator import BashOperator
from datetime import datetime

# definição das configurações básicas da dag
default_args = {
    'start_date': datetime(2019, 1, 1),
    'owner': 'Airflow',
    'email': 'owner@test.com'
}

# instanciação da dag com id e agendamento diário
with DAG(dag_id='pool_dag', schedule_interval='0 0 * * *', default_args=default_args, catchup=False) as dag:
    
    # busca taxas de câmbio do euro via api e envia para o xcom
    get_forex_rate_EUR = SimpleHttpOperator(
        task_id='get_forex_rate_EUR',
        method='GET',
        http_conn_id='forex_api',
        endpoint='/latest?base=EUR',
        xcom_push=True
    )
 
    # busca taxas de câmbio do dólar via api e envia para o xcom
    get_forex_rate_USD = SimpleHttpOperator(
        task_id='get_forex_rate_USD',
        method='GET',
        http_conn_id='forex_api',
        endpoint='/latest?base=USD',
        xcom_push=True
    )
 
    # busca taxas de câmbio do iene via api e envia para o xcom
    get_forex_rate_JPY = SimpleHttpOperator(
        task_id='get_forex_rate_JPY',
        method='GET',
        http_conn_id='forex_api',
        endpoint='/latest?base=JPY',
        xcom_push=True
    )
 
    # comando bash usando jinja para percorrer e imprimir dados do xcom
    bash_command="""
        {% for task in dag.task_ids %}
            echo "{{ task }}"
            echo "{{ ti.xcom_pull(task) }}"
        {% endfor %}
    """

    # tarefa bash que executa o comando para exibir os resultados
    show_data = BashOperator(
        task_id='show_result',
        bash_command=bash_command
    )

    # as três buscas rodam em paralelo antes de exibir os dados
    [get_forex_rate_EUR, get_forex_rate_USD, get_forex_rate_JPY] >> show_data