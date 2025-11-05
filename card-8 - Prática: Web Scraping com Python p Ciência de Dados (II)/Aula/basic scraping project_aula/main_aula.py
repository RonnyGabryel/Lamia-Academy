# Importa a biblioteca BeautifulSoup do pacote bs4,
# usada para analisar o conteúdo HTML de uma página.
from bs4 import BeautifulSoup

# Abre o arquivo local 'home_aula.html' no modo leitura ('r')
with open('home_aula.html', 'r') as html_file:
    # Lê todo o conteúdo do arquivo e guarda na variável 'content'
    content = html_file.read()

    # Cria um objeto BeautifulSoup para interpretar o HTML usando o parser 'lxml'
    soup = BeautifulSoup(content, 'lxml')

    # Busca todos os elementos <div> com a classe 'card'
    # Isso retorna uma lista de blocos (cards) do site.
    course_card = soup.find_all('div', class_='card')

    # Percorre cada card encontrado
    for course in course_card:
        # Pega o texto contido dentro da tag <h5> do card (geralmente o nome do curso)
        course_name = course.h5.text

        # Pega o texto dentro da tag <a> e separa as palavras com split()
        # Pega apenas a última palavra [-1], que provavelmente é o preço
        course_price = course.a.text.split()[-1]

        # Exibe o nome e o preço formatados
        print(f'{course_name} costs {course_price}')