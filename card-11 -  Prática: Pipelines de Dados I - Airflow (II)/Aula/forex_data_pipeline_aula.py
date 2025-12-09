# Importa o módulo principal do Airflow
import airflow
from airflow import DAG

# Sensores para monitoram condições antes de executar tasks
from airflow.sensors.filesystem import FileSensor  # Verifica existência de arquivos
from airflow.providers.http.sensors.http import HttpSensor  # Verifica disponibilidade de APIs

# Operadores para executam ações específicas
from airflow.operators.bash import BashOperator  # Executa comandos bash
from airflow.operators.python import PythonOperator  # Executa funções Python
from airflow.providers.apache.hive.operators.hive import HiveOperator  # Executa queries HiveQL
from airflow.providers.apache.spark.operators.spark_submit import SparkSubmitOperator  # Submete jobs Spark
from airflow.providers.email.operators.email import EmailOperator  # Envia emails
from airflow.providers.slack.operators.slack_webhook import SlackWebhookOperator  # Envia mensagens Slack

# Bibliotecas para manipulação de datas
from datetime import datetime, timedelta

# Bibliotecas padrão Python para manipulação de dados
import json  # Para trabalhar com arquivos JSON
import csv  # Para trabalhar com arquivos CSV
import requests  # Para fazer requisições HTTP

# Configurações padrão aplicadas a todas as tasks
default_args = {
    "owner": "airflow",  # Responsável pelo DAG
    "start_date": datetime(2025, 12, 8),  # Data inicial de execução
    "depends_on_past": False,  # Task não depende da execução anterior
    "email_on_failure": False,  # Desabilita email 
    "email_on_retry": False,  # Desabilita email ao retentar
    "email": "youremail@host.com",  # Email para notificações exemplo usado
    "retries": 1,  # Número de tentativas se falhar
    "retry_delay": timedelta(minutes=5)  # Aguarda 5 min entre tentativas
}

def download_rates():
    with open(
        "/usr/local/airflow/dags/files/forex_currencies.csv"
    ) as forex_currencies:  # abre o arquivo CSV
        reader = csv.DictReader(forex_currencies, delimiter=";")  # le como dicionario
        for row in reader:  # percorre as linhas do arquivo
            base = row["base"] 
            with_pairs = row["with_pairs"].split(" ")  # converte string de pares em lista
            indata = requests.get(
                "https://api.exchangeratesapi.io/latest?base=" + base
            ).json()  # requisicao da API para obter taxas de câmbio
            outdata = {
                "base": base,  # moeda base
                "rates": {},  # dicionário que armazenará as taxas
                "last_update": indata["date"],  # data da última atualização
            }
            for pair in with_pairs:  # Itera sobre os pares de moedas
                outdata["rates"][pair] = indata["rates"][
                    pair
                ]  # guarda taxa de cambio no dicionario
            with open(
                "/usr/local/airflow/dags/files/forex_rates.json", "a"
                ) as outfile:  # abre o JSON para escrita
                json.dump(outdata, outfile)  # escreve o dicionário como JSON
                outfile.write("\n")  # adiciona quebra de linha


# Define o DAG
with DAG(
    dag_id="forex_data_pipeline",  # Nome único do DAG
    schedule_interval="@daily",  # Executa todo dia à meia-noite
    default_args=default_args,  # Aplica as configs acima
    catchup=False  # Não executa datas passadas perdidas
) as dag:
    
    # Sensor HTTP que verifica se a API está disponível
    is_forex_rates_available = HttpSensor(
        task_id="is_forex_currencies_file_available",  # ID único da task
        method='GET',  # Método HTTP usado
        http_conn_id='forex_api',  # Connection ID 
        endpoint='latest',  # Endpoint da API para dados mais recentes
        response_check=lambda response: "rates" in response.text,  # Valida se resposta contém "rates"
        poke_interval=5,  # Verifica a cada 5 segundos
        timeout=20  # Timeout de 20 segundos
    )

    # verifica se o CSV ta disponivel
    is_forex_currencies_file_available = FileSensor(
        task_id="is_forex_currencies_file_available",  # ID único da task
        fs_conn_id="forex_path",  # Connection ID do filesystem configurado no Airflow
        filepath="forex_currencies.csv",  # Nome do arquivo a ser verificado
        poke_interval=5,  # Verifica a cada 5 segundos
        timeout=20,  # Timeout de 20 segundos
    )

    # operador Python para baixar taxas do cambio
    downloading_rates = PythonOperator(
        task_id="downloading_rates",  # nome da tarefa no airflow
        python_callable=download_rates,  # função Python a ser executada
    )

    # operador Bash para salvar taxas de ambio no HDFS
    saving_rates = BashOperator(
        task_id="saving_rates",  # ID único da task
        bash_command="""
            hdfs dfs -mkdir -p /forex && \
            hdfs dfs -put -f $AIRFLOW_HOME/dags/files/forex_rates.json /forex
            """,  # comando bash para criar a pasta e salvar o arquivo
    )

    # operador Hive para criar uma tabela Hive externa
    creating_forex_rates_table = HiveOperator(
        task_id="creating_forex_rates_table",  # ID único da task
        hive_cli_conn_id="hive_conn",  # Connection ID do Hive configurado no Airflow
        hql="""
            CREATE EXTERNAL TABLE IF NOT EXISTS forex_rates(
                base STRING,
                last_update DATE,
                eur DOUBLE,
                usd DOUBLE,
                nzd DOUBLE,
                gbp DOUBLE,
                jpy DOUBLE,
                cad DOUBLE
            )
            ROW FORMAT DELIMITED
            FIELDS TERMINATED BY ','
            STORED AS TEXTFILE
        """,  # Query HiveQL para criar tabela externa com schema definido
    )
    
    # operador Spark para processar os dados
    forex_processing = SparkSubmitOperator(
        task_id="forex_processing",  # ID único da task
        conn_id="spark_conn",  # Connection ID do Spark configurado no Airflow
        application="/usr/local/airflow/dags/scripts/forex_processing.py",  # path do script Spark
        verbose=False,  # Reduz a verbosidade dos logs
    )

    # operador para enviar email
    sending_email_notification = EmailOperator(
        task_id="sending_email",  # ID único da task
        to="airflow_course@yopmail.com",  # Destinatário do email
        subject="forex_data_pipeline",  # Assunto do email
        html_content="""
            <h3>forex_data_pipeline succeeded</h3>
        """,  # Corpo do email em HTML
    )

    # operador para enviar mensagem no Slack
    sending_slack_notification = SlackWebhookOperator(
        task_id="sending_slack",  # ID único da task
        slack_webhook_conn_id="slack_conn",  # Connection ID do Slack Webhook configurado no Airflow
        message="DAG forex_data_pipeline: DONE",  # texto da mensagem
    )

    # ordem de execucao das tarefas
    # Primeiro fluxo verifica API disponível > verifica CSV existe > baixa taxas > salva no HDFS
    (
        is_forex_rates_available
        >> is_forex_currencies_file_available
        >> downloading_rates
        >> saving_rates
    )
    # Segundo fluxo apos salvar no HDFS > cria tabela Hive > processa com Spark
    saving_rates >> creating_forex_rates_table >> forex_processing
    # Terceiro fluxo apos processar com Spark > envia email > envia mensagem Slack
    forex_processing >> sending_email_notification >> sending_slack_notification