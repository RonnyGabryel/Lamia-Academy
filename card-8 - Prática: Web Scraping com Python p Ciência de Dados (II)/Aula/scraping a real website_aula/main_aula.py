from bs4 import BeautifulSoup  # Biblioteca para analisar o HTML
import requests  # Para fazer requisições à internet
import time  # Para adicionar pausas no programa

# Pedindo uma skill para o usuário
print("Put some skill that you are not familiar with")

# Pega o valor que o usuário deseja passar como skill
unfamiliar_skill = input('>')

print(f"Filtering out {unfamiliar_skill}")  # Mostra qual skill será filtrada

# Função principal que busca vagas
def find_jobs():
    # Requisitando o HTML do site
    html_Text = requests.get('https://www.timesjobs.com/candidate/job-search.html?searchType=personalizedSearch&from=submit&searchTextSrc=ft&searchTextText=Python&txtKeywords=Python%2C&txtLocation=').text

    # Utilizando o BeautifulSoup para ler e interpretar o HTML
    soup = BeautifulSoup(html_Text, 'lxml')

    # Achando todos os "cards" de emprego (cada vaga é um <li>)
    jobs = soup.find_all('li', class_='clearfix job-bx wht-shd-bx')

    # Percorrendo todas as vagas encontradas
    for index, job in enumerate(jobs):

        # Pegando a data de publicação do span
        published_date = job.find('span', class_='sim-posted').span.text.replace(' ', '')

        # Filtrando apenas as vagas recentes
        if 'few' in published_date:

            # Achando o nome da companhia dessa vaga
            company_name = job.find('h3', class_='joblist-comp-name').text.replace(' ', '')

            # Achando as skills exigidas (o site mudou, agora usa 'div' em vez de 'span')
            skills = job.find('div', class_='more-skills-sections').text.replace(' ', '')

            # Pegando o link de mais informações da vaga
            more_info = job.header.h2.a['href']

            # Se a skill que o usuário não domina NÃO estiver na lista de skills da vaga
            if unfamiliar_skill not in skills:
                # Cria (ou substitui) o arquivo .txt com as informações da vaga
                with open(f'posts/{index}.txt', 'w') as f:
                    f.write(f"Company name: {company_name.strip()} \n")
                    f.write(f"Required Skills: {skills.strip()} \n")
                    f.write(f"More info: {more_info}\n")

                # Mostra no terminal que o arquivo foi salvo
                print(f"File saved: {index}")

# Se esse for o arquivo principal executado
if __name__ == '__main__':
    while True:
        find_jobs()  # Executa a função principal
        time_wait = 10  # Tempo de espera em minutos
        print(f'Waiting {time_wait} minutes...')
        time.sleep(time_wait * 60)  # Espera 10 minutos antes de rodar de novo