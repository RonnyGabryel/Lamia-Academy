from airflow import DAG
from airflow.operators.empty import EmptyOperator
from airflow.operators.python import PythonOperator
from airflow.operators.subdag import SubDagOperator
from datetime import datetime

# SubDAG para agrupar etapas de validação de dados de um relatório

default_args = {
    'owner': 'Ronny_Pratica',
    'start_date': datetime(2026, 1, 1),
}

DAG_NAME = 'subdag_pratica_dag'

def criar_subdag_validacao(parent_dag_name, child_dag_name, args):
    #Subdag com duas etapas de validação de dados
    subdag = DAG(
        dag_id=f'{parent_dag_name}.{child_dag_name}',
        default_args=args,
        schedule='@once',
    )

    def checar_nulos():
        print("Verificando campos nulos nos dados...")

    def checar_duplicatas():
        print("Verificando registros duplicados...")

    checar_nulos_task = PythonOperator(
        task_id='checar_nulos',
        python_callable=checar_nulos,
        dag=subdag
    )

    checar_duplicatas_task = PythonOperator(
        task_id='checar_duplicatas',
        python_callable=checar_duplicatas,
        dag=subdag
    )

    checar_nulos_task >> checar_duplicatas_task
    return subdag


def criar_subdag_relatorio(parent_dag_name, child_dag_name, args):
    # Subdag com duas etapas de geração de relatório
    subdag = DAG(
        dag_id=f'{parent_dag_name}.{child_dag_name}',
        default_args=args,
        schedule='@once',
    )

    def gerar_pdf():
        print("Gerando relatório em PDF...")

    def enviar_email():
        print("Enviando relatório por e-mail...")

    gerar_pdf_task = PythonOperator(
        task_id='gerar_pdf',
        python_callable=gerar_pdf,
        dag=subdag
    )

    enviar_email_task = PythonOperator(
        task_id='enviar_email',
        python_callable=enviar_email,
        dag=subdag
    )

    gerar_pdf_task >> enviar_email_task
    return subdag


with DAG(
    dag_id=DAG_NAME,
    default_args=default_args,
    schedule='@once',
    catchup=False,
    tags=['aula', 'subdag']
) as dag:

    inicio = EmptyOperator(task_id='inicio')

    validacao = SubDagOperator(
        task_id='subdag_validacao',
        subdag=criar_subdag_validacao(DAG_NAME, 'subdag_validacao', default_args)
    )

    relatorio = SubDagOperator(
        task_id='subdag_relatorio',
        subdag=criar_subdag_relatorio(DAG_NAME, 'subdag_relatorio', default_args)
    )

    fim = EmptyOperator(task_id='fim')

    inicio >> validacao >> relatorio >> fim
