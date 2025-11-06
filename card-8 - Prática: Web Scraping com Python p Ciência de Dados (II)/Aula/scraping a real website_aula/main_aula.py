from bs4 import BeautifulSoup  # Biblioteca para analisar o HTML
import requests  # Para fazer requisições à internet
import time  # Para adicionar pausas no programa
import os  # Para manipular diretórios

print('Put some skill that you are not familiar with')
unfamiliar_skill = input('>')  # Recebe a skill digitada
print(f'Filtering out {unfamiliar_skill}')  # Mostra o filtro aplicado


# Função principal que busca vagas
def find_jobs():
    # Garante que a pasta 'posts' exista
    os.makedirs('posts', exist_ok=True)

    # Faz uma requisição ao site TimesJobs com busca por vagas de Python
    html_text = requests.get(
        'https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=Python&txtKeywords=Python%2C&txtLocation='
    ).text

    soup = BeautifulSoup(html_text, 'lxml')  # Analisa o conteúdo HTML
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')  # Encontra todos os blocos de vagas

    # Percorre cada vaga encontrada
    for index, job in enumerate(jobs):
        # Obtém a data de publicação (com verificação de segurança)
        published_tag = job.find('span', class_='sim-posted')
        published_date = published_tag.span.text.strip() if published_tag and published_tag.span else 'Unknown'

        # Filtra apenas as vagas recentes
        if 'few' in published_date or 'day' in published_date:
            # Extrai o nome da empresa
            company_tag = job.find('h3', class_='joblist-comp-name')
            company_name = company_tag.text.strip() if company_tag else 'Unknown'

            # Extrai as habilidades pedidas
            skills_tag = job.find('span', class_='srp-skills')
            skills = skills_tag.text.strip() if skills_tag else 'Not specified'

            # Pega o link para mais informações sobre a vaga
            more_info_tag = job.header.h2.a if job.header and job.header.h2 and job.header.h2.a else None
            more_info = more_info_tag['href'] if more_info_tag else 'No link available'

            # Verifica se a skill indesejada NÃO está na vaga
            if unfamiliar_skill.lower() not in skills.lower():
                # Cria um arquivo de texto para salvar as informações
                with open(f'posts/{index}.txt', 'w', encoding='utf-8') as f:
                    f.write(f"Company Name: {company_name}\n")
                    f.write(f"Required Skills: {skills}\n")
                    f.write(f"More Info: {more_info}\n")
                    f.write(f"Published: {published_date}\n")

                # Mostra no terminal que o arquivo foi salvo
                print(f'File saved: posts/{index}.txt')

    print('--- Search finished ---')


# Executa o script continuamente, verificando vagas a cada 10 minutos
if __name__ == '__main__':
    while True:
        find_jobs()
        time_wait = 10
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)
