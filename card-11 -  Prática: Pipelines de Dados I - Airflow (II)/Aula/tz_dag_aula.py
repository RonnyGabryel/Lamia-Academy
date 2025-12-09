import pendulum  
from airflow import DAG  
from airflow.utils import timezone  
from airflow.operators.dummy_operator import DummyOperator  
from datetime import timedelta, datetime  

# Define o fuso horário local (Paris)
local_tz = pendulum.timezone("Europe/Paris")  

# Configurações padrão da DAG
default_args = {  
    'start_date': datetime(2015, 3, 29, 1),  # Data de início: 29/03/2015 à 01:00
    'owner': 'Airflow'
}  

# Criação da DAG
with DAG(  
    dag_id='tz_dag',  # Nome da DAG
    schedule_interval="0 1 * * *",  # Executa diariamente à 01:00
    default_args=default_args  
) as dag:  
    
    # Task dummy
    dummy_task = DummyOperator(task_id='dummy_task')  
    
    # Obtém todas as datas de execução programadas da DAG
    run_dates = dag.get_run_dates(start_date=dag.start_date)  
    
    # Pega a última data de execução (se existir)
    next_execution_date = run_dates[-1] if len(run_dates) != 0 else None  
    
    # Imprime informações sobre fusos horários e datas da DAG
    print('datetime from Python is Naive: {0}'.format(timezone.is_naive(datetime(2025, 12, 8, 1))))  
    # Naive = sem informação de fuso horário
    
    print('datetime from Airflow is Aware: {0}'.format(timezone.is_naive(timezone.datetime(2025, 12, 8, 1)) == False))  
    # Aware = com informação de fuso horário
    
    # Imprime detalhes completos da DAG
    print('[DAG:tz_dag] timezone: {0} - start_date: {1} - schedule_interval: {2} - Last execution_date: {3} - next execution_date {4} in UTC - next execution_date {5} in local time'.format(
        dag.timezone,  # Fuso horário da DAG
        dag.default_args['start_date'],  # Data de início
        dag._schedule_interval,  # Intervalo de agendamento
        dag.latest_execution_date,  # Última execução realizada
        next_execution_date,  # Próxima execução em UTC
        local_tz.convert(next_execution_date) if next_execution_date is not None else None  
        # Próxima execução convertida para horário de Paris
    ))