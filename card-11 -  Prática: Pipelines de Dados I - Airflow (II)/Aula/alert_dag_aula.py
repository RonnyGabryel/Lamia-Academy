from airflow import DAG  
from airflow.operators.bash_operator import BashOperator  # Para executar comandos Bash
from datetime import datetime, timedelta  

# Configurações padrão da DAG
default_args = {  
    'start_date': datetime(2025, 12, 8,),  # Data de início:08/12/2025 
    'owner': 'Airflow'
}  

# Criação da DAG
with DAG(  
    dag_id='alert_dag',  # Nome da DAG
    schedule_interval="0 0 * * *",  # Executa diariamente à meia-noite (00:00)
    default_args=default_args,  
    catchup=True  # Executa todas as datas passadas
) as dag:  
    
    # Task 1 executa comando que FALHA propositalmente
    t1 = BashOperator(  
        task_id='t1', 
        bash_command="exit 1"  # Retorna código de erro
    )  
    
    # Task 2 executa comando que imprime second task
    t2 = BashOperator(  
        task_id='t2', 
        bash_command="echo 'second task'" 
    )  
    
    # Define a ordem t1 executa primeiro, depois t2
    t1 >> t2