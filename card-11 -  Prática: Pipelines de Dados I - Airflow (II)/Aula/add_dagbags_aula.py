import os  
from airflow.models import DagBag  # Classe para carregar dinamicamente de pastas

# Lista com caminhos absolutos das pastas que contêm DAGs
dags_dirs = [  
    '/usr/local/airflow/project_a',  # Pasta do projeto A
    '/usr/local/airflow/project_b'   # Pasta do projeto B
]  

# Itera sobre cada pasta de DAGs
for dir in dags_dirs:  
    # Cria uma instância de DagBag para carregar todas as DAGs da pasta
    dag_bag = DagBag(os.path.expanduser(dir))  

    # Verifica se o dag_bag foi criado com sucesso
    if dag_bag:  
        # Itera sobre todas as DAGs carregadas (dicionário {dag_id: dag_object})
        for dag_id, dag in dag_bag.dags.items():  
            # Adiciona cada DAG ao escopo global para que o Airflow as encontre
            globals()[dag_id] = dag
