from bs4 import BeautifulSoup  # Analisa o HTML
import requests  # Faz requisições HTTP
import os  # Cria pastas e manipula arquivos
import time  # Controla pausas entre execuções
import difflib  # Para comparar similaridade de textos


print("Digite uma palavra ou parte do título que deseja procurar:")  # Mostra no terminal a mensagem pedindo o termo de busca
busca = input("> ").lower().strip()  # Pega o texto digitado deixa tudo em minúsculo e remove espaços extras
print(f"\n Buscando livros com títulos parecidos com: '{busca}'\n")  # Exibe mensagem informando o que será buscado

def buscar_livros():  # Define a função principal que fará a busca dos livros
    headers = {"User-Agent": "Mozilla/5.0"}  # Define um cabeçalho pra simular um navegador
    html_texto = requests.get("http://books.toscrape.com/", headers=headers).text  # Faz a requisição e pega o HTML da página
    soup = BeautifulSoup(html_texto, "html.parser")  # Analisa o HTML da página usando o BeautifulSoup

    livros = soup.find_all("article", class_="product_pod")  # Encontra todos os blocos de livros na página

    encontrados = 0  # Inicia o contador de livros encontrados

    for index, livro in enumerate(livros):  # Percorre todos os livros encontrados, com um índice pra nomear os arquivos
        titulo = livro.find("h3").find("a")["title"]  # Pega o título do livro dentro da tag <a>
        titulo_lower = titulo.lower()  # Converte o título pra minúsculo pra facilitar a comparação

        similaridade = difflib.SequenceMatcher(None, busca, titulo_lower).ratio()  # Mede a similaridade entre o termo buscado e o título do livro

        # Aceita títulos com pelo menos similaridade ou que contenham diretamente o termo
        if busca in titulo_lower or similaridade > 0.4:
            encontrados += 1

            link = livro.find("h3").find("a")["href"] # Pega o link parcial do livro
            url_completa = f"http://books.toscrape.com/catalogue/{link}"

            preco = livro.find("p", class_="price_color").text # Pega o preço do livro
            estrelas = livro.find("p", class_="star-rating")["class"][1]
            traducao_estrelas = { # Dicionário pra converter texto de estrelas em número
                "One": "1",
                "Two": "2",
                "Three": "3",
                "Four": "4",
                "Five": "5",
            }
            num_estrelas = traducao_estrelas.get(estrelas, estrelas)  # Pega o número de estrelas correspondente

            estoque = livro.find("p", class_="instock availability")  # Pega a informação de disponibilidade do livro
            status_estoque = "Fora de estoque"
            if estoque and "In stock" in estoque.text:
                status_estoque = "Em estoque"

            with open(f"livros/{index}.txt", "w",encoding="utf-8") as f:  # Cria e abre um arquivo de texto pra salvar as informações do livro
                f.write(f"Título: {titulo}\n")  # Escreve o título no arquivo
                f.write(f"Preço: {preco}\n")  # Escreve o preço
                f.write(f"Avaliação: {num_estrelas} estrelas\n")  # Escreve o número de estrelas
                f.write(f"Status: {status_estoque}\n")  # Escreve a disponibilidade
                f.write(f"Link: {url_completa}\n")  # Escreve o link completo do livro

            print(f" Livro salvo: livros/{index}.txt")  # Mostra no terminal que o livro foi salvo com sucesso

            if encontrados == 0:  # Caso nenhum livro tenha sido encontrado
                print(" Nenhum livro encontrado com esse nome.")  # Mostra mensagem avisando que nada foi achado
            else:  # Caso existam livros encontrados
                print(f"\n {encontrados} livro(s) encontrados e salvos!\n")  # Mostra a quantidade de livros salvos


if __name__ == "__main__":  # Garante que o código abaixo só execute se o arquivo for rodado diretamente
    while True:  # Cria um loop infinito pra repetir o processo de busca
        buscar_livros()  # Chama a função principal que faz a busca
        intervalo = 10  # Define o tempo de espera entre as execuções
        print(f"\n Aguardando {intervalo} minutos para nova verificação...\n")  # Mostra no terminal o tempo de espera
        time.sleep(intervalo * 60)  # Pausa o programa pelo tempo definido antes de repetir