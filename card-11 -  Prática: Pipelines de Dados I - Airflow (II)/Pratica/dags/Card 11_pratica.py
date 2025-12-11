import pendulum
from airflow import DAG 
from airflow.models import DagBag  # Classe para carregar DAGs dinamicamente
from airflow.operators.empty import EmptyOperator 
from airflow.operators.bash import BashOperator 
from airflow.operators.python import PythonOperator 
from datetime import datetime, timedelta 

# Usa o fuso horário de São Paulo
local_tz = pendulum.timezone("America/Sao_Paulo")


default_args = {
    'start_date': datetime(2024, 12, 10, tzinfo=local_tz),  #Aplica timezone
    'owner': 'bibliotecario', 
    'retries': 2,
    'retry_delay': timedelta(minutes=3),
    'email_on_failure': True,  # Adiciona notificação
    'email': ['biblioteca@exemplo.com'],  # Email para alertas
}

# Função que simula o processamento de empréstimos
def processar_emprestimos():
    print("Processando empréstimos realizados hoje")
    print("Verificando limite de livros por usuário")
    print("Registrando data de devolução prevista")
    print("Empréstimos processados com sucesso")

# Função que simula a categorização por tipo de livro
def categorizar_livro(categoria):
    print(f"Processando empréstimos da categoria: {categoria}")
    print(f"Total de livros {categoria} emprestados: simulando contagem...")
    print(f"Verificando disponibilidade de {categoria} no acervo")

# Função que simula o processamento de devoluções
def processar_devolucoes():
    print("Processando devoluções recebidas hoje...")
    print("Verificando estado de conservação dos livros")
    print("Atualizando status para 'disponível'")
    print("Devoluções processadas com sucesso!")

# Função que calcula multas por atraso
def calcular_multas():
    print("Calculando multas por atraso")
    print("Verificando devoluções em atraso")
    print("Calculando valor da multa (R$ 2,00 por dia)")
    print("Enviando notificação aos usuários em débito")
    print("Multas calculadas e registradas!")

# Função que atualiza o estoque/disponibilidade
def atualizar_estoque():
    print("Atualizando disponibilidade do acervo...")
    print("- Livros emprestados: removidos do estoque disponível")
    print("- Livros devolvidos: adicionados ao estoque disponível")
    print("- Estoque atualizado no sistema!")

with DAG(
    dag_id='Sistema_Biblioteca',  # Nome da DAG no Airflow
    schedule="0 9 * * *",  # Executa todo dia às 9h da manhã
    default_args=default_args, 
    catchup=False  # Impede execuções de datas anteriores
) as dag:
    
    # Primeira task marca o início da DAG
    start = EmptyOperator(task_id='start')
    
    # Task 2: Busca as movimentações do dia no banco de dados
    buscar_movimentacoes = BashOperator(
        task_id='buscar_movimentacoes',
        bash_command="echo 'Buscando empréstimos e devoluções do dia no banco de dados...'"
    )
    
    # Task 3: Processa os empréstimos realizados
    processar_emprestimos_task = PythonOperator(
        task_id='processar_emprestimos',
        python_callable=processar_emprestimos
    )
    
    # Categorias de livros da biblioteca
    categorias = ['literatura', 'tecnicos', 'infantis']
    
    # Cria dinamicamente uma task para cada categoria de livro
    categorizar_tasks = [
        PythonOperator(
            task_id=f'categorizar_{categoria}',  # Gera um ID para cada categoria
            python_callable=categorizar_livro,  # Chama a função que processa a categoria
            op_args=[categoria]  # Passa o nome da categoria como argumento
        ) for categoria in categorias
    ]
    
    # Task 4: Processa as devoluções recebidas
    processar_devolucoes_task = PythonOperator(
        task_id='processar_devolucoes',
        python_callable=processar_devolucoes
    )
    
    # Task 5: Calcula multas por atraso
    calcular_multas_task = PythonOperator(
        task_id='calcular_multas',
        python_callable=calcular_multas
    )
    
    # Task 6: Atualiza o estoque ou disponibilidade
    atualizar_estoque_task = PythonOperator(
        task_id='atualizar_estoque',
        python_callable=atualizar_estoque
    )
    
    # Task 7: Gera o relatório final do dia
    gerar_relatorio = BashOperator(
        task_id='gerar_relatorio',
        bash_command="echo 'Gerando relatório diário da biblioteca...'"
    )
    
    # Última task marca o fim da DAG
    end = EmptyOperator(task_id='end')
    
    # Define o fluxo de execução das tasks
    start >> buscar_movimentacoes >> processar_emprestimos_task >> categorizar_tasks
    categorizar_tasks >> processar_devolucoes_task >> calcular_multas_task
    calcular_multas_task >> atualizar_estoque_task >> gerar_relatorio >> end