from bs4 import BeautifulSoup  # Biblioteca para analisar o HTML
import requests  # Para fazer requisições à internet
import time  # Para adicionar pausas no programa

# Pede ao usuário uma habilidade que ele não domina
print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>')  # Recebe a skill digitada
print(f'Filtering out {unfamiliar_skill}')  # Mostra o filtro aplicado

# Função principal que busca vagas
def find_jobs():    # Faz uma requisição ao site TimesJobs com busca por vagas de Python
    html_text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=Python&txtKeywords=Python%2C&txtLocation=').text
    soup = BeautifulSoup(html_text, 'lxml')  # Analisa o conteúdo HTML com o BeautifulSoup
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')   # Encontra todos os blocos de vagas

    # Percorre cada vaga encontrada
    for index, job in enumerate(jobs):
        published_date = job.find('span', class_='sim-posted').span.text # Pega a data em que a vaga foi publicada
        if 'few' in published_date:
            # Extrai o nome da empresa
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')
            # Extrai as habilidades pedidas
            skills = job.find('span', class_='srp-skills').text.replace(' ', '')
            # Pega o link para mais informações sobre a vaga

            more_info = job.header.h2.a['href'] # Verifica se a skill indesejada NÃO está na vaga
            if unfamiliar_skill not in skills:
                # Cria um arquivo de texto para salvar as informações
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company Name: {company_name.strip()}\n")
                    f.write(f"Required Skills: {skills.strip()}\n")
                    f.write(f'More Info: {more_info}')

                # Mostra no terminal que o arquivo foi salvo
                print(f'File saved: {index}')


# Executa o script continuamente, verificando vagas a cada 10 minutos
if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)