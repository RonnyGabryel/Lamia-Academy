from airflow import DAG
from airflow.operators.bash import BashOperator
from datetime import datetime

# normal padrão
default_args = {
    'start_date': datetime(2026, 1, 1),
    'owner': 'Ronny_Pratica',
}

with DAG(
    dag_id='queue_dag_pratica', 
    schedule=None, 
    default_args=default_args, 
    catchup=False,
    tags=['aula', 'infra']
) as dag:

    # Esta tarefa será enviada para a fila padrão 
    tarefa_comum = BashOperator(
        task_id='tarefa_geral',
        bash_command='echo "Rodando no worker padrão"',
        queue='default'
    )

    #esta tarefa seria direcionada para um worker com GPU ou mais Spark e o parâmetro queue é o que define para onde a tarefa fica
    tarefa_especifica = BashOperator(
        task_id='tarefa_pesada_especial',
        bash_command='echo "Rodando em máquina de alta performance"',
        queue='high_mem_queue' 
    )

    #Execução em paralelo para teste de distribuição
    [tarefa_comum, tarefa_especifica]