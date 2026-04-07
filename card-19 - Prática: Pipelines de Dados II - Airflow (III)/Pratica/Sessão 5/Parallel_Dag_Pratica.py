from airflow import DAG
from airflow.operators.python import PythonOperator
from datetime import datetime

#onfigurações básicas da DAG
default_args = {
    'start_date': datetime(2026, 1, 1),
    'owner': 'Ronny_Pratica',
}

def tarefa_paralela(id_task):
    print(f"Executando processo paralelo número: {id_task}")

def finalizar():
    print("Concluído: Todas as frentes foram processadas!")

with DAG(dag_id='parallel_pratica_dag', schedule=None, default_args=default_args, catchup=False) as dag:

    #Cria 3 tarefas que rodam ao mesmo tempo usando Python
    processos = [
        PythonOperator(
            task_id=f'processo_paralelo_{i}',
            python_callable=tarefa_paralela,
            op_args=[i]
        ) for i in range(1, 4)
    ]

    #aguarda os processos acima
    conclusao = PythonOperator(
        task_id='conclusao_geral',
        python_callable=finalizar
    )

    # o fluxo
    processos >> conclusao