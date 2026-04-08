# importação das bibliotecas 
import airflow
import requests
from airflow.models import DAG
from airflow.operators.dummy_operator import DummyOperator
from airflow.operators.python_operator import BranchPythonOperator, PythonOperator

# definição das configurações 
default_args = {
    'owner': 'Airflow',
    'start_date': airflow.utils.dates.days_ago(2),
}

# dicionário com os nomes
IP_GEOLOCATION_APIS = {
    'ip-api': 'http://ip-api.com/json/',
    'ipstack': 'https://api.ipstack.com/',
    'ipinfo': 'https://ipinfo.io/json'
}

# função que testa as apis
def check_api():
    for api, link in IP_GEOLOCATION_APIS.items():
        r = requests.get(link)
        try:
            data = r.json()
            if data and 'country' in data and len(data['country']):
                return api
        except ValueError:
            pass
    return 'none'

# instanciação da dag 
with DAG(dag_id='branch_dag', 
    default_args=default_args, 
    schedule_interval="@once") as dag:

    # operador de ramificação 
    check_api = BranchPythonOperator(
        task_id='check_api',
        python_callable=check_api
    )

    # tarefa dummy executada 
    none = DummyOperator(
        task_id='none'
    )

    # tarefa dummy que representa 
    save = DummyOperator(task_id='save')

    # fluxo padrão 
    check_api >> none >> save

    # criação dinâmica de tarefas 
    for api in IP_GEOLOCATION_APIS:
        process = DummyOperator(
            task_id=api
        )
    
        check_api >> process >> save