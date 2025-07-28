# Relatório 2: Prática: Linguagem de Programação Python (I)
# Sistema de Gerenciamento de Games  Biblioteca Pessoal
# Demonstrando todos os conceitos aprendidos no mini curso
# Uma coisa que me ajudou a fazer isso foi a documentação de python "https://docs.python.org/pt-br/3/" 
# Primeiro vou importar algumas coisas 
import random
from datetime import datetime

# ========== COLEÇÕES: LISTAS, TUPLAS, SETS E DICIONÁRIOS ==========

# TUPLAS  Dados que não mudam (como vi na aula, tuplas são imutáveis)
PLATAFORMAS_DISPONIVEIS = ("PC", "PlayStation", "Xbox", "Nintendo Switch", "Mobile")
CLASSIFICACOES_ETARIAS = ("Livre", "10+", "12+", "14+", "16+", "18+")
INFO_SISTEMA = ("Sistema de Games v1.0", "Desenvolvido em Python", "Para gerenciar biblioteca pessoal")

# SETS  Conjuntos para evitar duplicatas (aprendi que sets eliminam repetições automaticamente)
generos_populares = {"Ação", "RPG", "Estratégia", "Puzzle", "Aventura", "Corrida", "Esporte", "Simulação"}
desenvolvedoras_favoritas = {"Valve", "CD Projekt", "Nintendo", "Rockstar", "Blizzard"} # pode ser que eu adicione mais depois

# LISTAS - Para armazenar os games (mutáveis e ordenadas como visto na aula)
biblioteca_games = []
wishlist = []  # lista de jogos que quero comprar

# DICIONÁRIOS  Estruturas chave:valor para configurações e estatísticas
# Lembrando da aula: dicionários são úteis para acessar dados por chave específica
config_usuario = {
    'nome_usuario': 'GameMaster',
    'plataforma_preferida': 'PC',
    'budget_mensal': 200.00,
    'genero_favorito': 'RPG'
}

# Estatísticas que vou calcular depois
estatisticas_globais = {
    'total_games': 0,
    'horas_totais': 0,
    'dinheiro_gasto': 0.0,
    'games_zerados': 0,
    'nota_media': 0.0
}

contador_total = 0  # ia usar para contar algo mas mudei de ideia
temp_var = ""       # variável temporária que usei para testes
ultima_pesquisa = None  # para guardar última busca, mas não implementei ainda

# ========== CLASSE GAME  POO ==========

class Game:
    # Atributo de classe (compartilhado por todas as instâncias)
    total_games_cadastrados = 0
    
    def __init__(self, nome, genero, plataforma, preco=0.0):
        # Método construtor  aprendi que __init__ é chamado quando crio um objeto
        self.nome = nome
        self.genero = genero
        self.plataforma = plataforma
        self.preco = preco
        self.horas_jogadas = 0
        self.nota_pessoal = 0
        self.zerado = False
        self.data_compra = datetime.now().strftime("%d/%m/%Y")  # pego a data atual
        self.observacoes = []  # lista para comentários pessoais
        
        # Incremento o contador de classe
        Game.total_games_cadastrados += 1
    
    def adicionar_horas(self, horas):
        # Método para adicionar horas jogadas
        if horas > 0:  # validação básica
            self.horas_jogadas += horas
            return True
        return False
    
    def avaliar_jogo(self, nota):
        # Método para dar nota de 0 a 10
        if 0 <= nota <= 10:  # operadores relacionais para validar
            self.nota_pessoal = nota
            return True
        else:
            return False
    
    def marcar_como_zerado(self):
        # Marca o jogo como finalizado
        self.zerado = True
        print(f"Parabéns! Você zerou {self.nome}!")
    
    def adicionar_observacao(self, obs):
        # Adiciona comentário pessoal sobre o jogo
        self.observacoes.append(obs)  # usando append como vi na aula sobre listas
    
    # Método especial para representação em string
    def __str__(self):
        status = " Zerado" if self.zerado else " Jogando"
        return f"{self.nome} ({self.genero}) {self.plataforma} | {status} | Nota: {self.nota_pessoal}/10"

# ========== FUNÇÕES COM *ARGS E **KWARGS ==========

def registrar_compra_multipla(*games, **detalhes):
    """
    Função que demonstra *args e **kwargs da aula
    *args recebe vários jogos
    **kwargs recebe detalhes como desconto, loja, etc.
    """
    print("=== Registrando Compra Múltipla ===")
    
    # Processando argumentos posicionais (*args)
    total_gasto = 0
    for game in games:
        print(f"Comprando: {game.nome} R$ {game.preco}")
        biblioteca_games.append(game)
        total_gasto += game.preco
    
    # Processando argumentos nomeados (**kwargs)
    desconto = detalhes.get('desconto', 0)  # se não tiver desconto, usa 0
    loja = detalhes.get('loja', 'Loja Genérica')
    promocao = detalhes.get('promocao', False)
    
    if desconto > 0:
        total_gasto = total_gasto * (1 - desconto/100)  # operadores aritméticos
        print(f"Desconto aplicado: {desconto}%")
    
    print(f"Total gasto na {loja}: R$ {total_gasto:.2f}")
    
    if promocao:  # estrutura if simples
        print("Compra realizada em promoção!")
    
    return total_gasto

def buscar_games_avancada(*criterios, **filtros):
    """Outra função demonstrando *args e **kwargs busca personalizada"""
    resultados = []
    
    # Testei fazer uma busca mais complexa mas ficou meio complicado
    # por enquanto só retorno os games mesmo
    for game in biblioteca_games:
        if len(criterios) == 0 or game.genero in criterios:
            resultados.append(game)
    
    return resultados

# ========== FUNÇÕES LAMBDA, MAP, FILTER ==========

# LAMBDAS Funções de uma linha como vi na aula
# Lambda para calcular valor com desconto
aplicar_desconto = lambda preco, desconto: preco * (1 - desconto/100)

# Lambda para verificar se jogo é caro (mais de 100 reais)
eh_caro = lambda game: game.preco > 100

# Lambda para formatar nome do jogo
formatar_nome = lambda nome: nome.strip().title()

# Lambda para calcular horas por real gasto
custo_beneficio = lambda game: game.horas_jogadas / game.preco if game.preco > 0 else 0

# Função que usa MAP  aplicar operação em todos elementos da lista
def aplicar_desconto_biblioteca(desconto_percent):
    """Aplica desconto em todos os jogos usando map()"""
    # Usando map como visto na aula aplica função em toda lista
    precos_originais = list(map(lambda game: game.preco, biblioteca_games))
    precos_com_desconto = list(map(lambda preco: aplicar_desconto(preco, desconto_percent), precos_originais))
    
    print(f"Preços originais: {precos_originais}")
    print(f"Com {desconto_percent}% desconto: {precos_com_desconto}")
    return precos_com_desconto

# Função que usa FILTER - filtrar elementos da lista
def filtrar_games_por_criterio(criterio):
    """Filtra jogos usando filter() e lambda"""
    if criterio == "caros":
        return list(filter(eh_caro, biblioteca_games))
    elif criterio == "zerados":
        return list(filter(lambda game: game.zerado, biblioteca_games))
    elif criterio == "bem_avaliados":
        return list(filter(lambda game: game.nota_pessoal >= 8, biblioteca_games))
    else:
        return biblioteca_games

# ========== ESTRUTURAS DE CONTROLE ==========

def sistema_recomendacao(usuario_genero, budget):
    """
    Função que demonstra IF/ELIF/ELSE da aula
    Sistema de recomendação baseado em gênero e orçamento
    """
    print("\n=== Sistema de Recomendação ===")
    
    # Estrutura IF/ELIF/ELSE múltipla como no exemplo da aula
    if budget >= 200 and usuario_genero == "RPG":
        print("Recomendo: Cyberpunk 2077 ou The Witcher 3!")
        recomendacao = "AAA RPG"
    elif budget >= 100 and usuario_genero == "Ação":
        print("Recomendo: GTA V ou Red Dead Redemption 2!")
        recomendacao = "AAA Ação"
    elif budget >= 50:
        print("Recomendo: Hollow Knight ou Celeste!")
        recomendacao = "Indie"
    else:
        print("Recomendo: Jogos gratuitos como Fortnite ou LoL!")
        recomendacao = "Free-to-Play"
    
    # Operador ternário da aula
    disponibilidade = "Disponível" if budget > 0 else "Sem orçamento"
    print(f"Status: {disponibilidade}")
    
    return recomendacao

def relatorio_detalhado():
    """Função que usa vários tipos de loops (FOR e WHILE)"""
    print("\n=== Relatório Detalhado da Biblioteca ===")
    
    if not biblioteca_games:  # operador not (lógico)
        print("Nenhum jogo cadastrado ainda.")
        return
    
    # LOOP FOR  percorrer lista como visto na aula
    print("\n Todos os Games:")
    for i, game in enumerate(biblioteca_games, 1):  # enumerate para numerar
        print(f"{i}. {game}")
    
    # Usando FOR para cálculos
    total_horas = 0
    total_gasto = 0
    games_zerados = 0
    
    for game in biblioteca_games:
        total_horas += game.horas_jogadas  # operadores aritméticos
        total_gasto += game.preco
        if game.zerado:  # if simples
            games_zerados += 1
    
    # LOOP WHILE  exemplo da aula adaptado
    contador = 0
    games_bem_avaliados = []
    while contador < len(biblioteca_games):
        game_atual = biblioteca_games[contador]
        if game_atual.nota_pessoal >= 8:  # operadores relacionais
            games_bem_avaliados.append(game_atual)
        contador += 1  # incremento
    
    # Operadores lógicos (AND, OR)
    tem_games_caros = any(game.preco > 100 for game in biblioteca_games)
    todos_avaliados = all(game.nota_pessoal > 0 for game in biblioteca_games)
    
    print(f"\n Estatísticas:")
    print(f"Total de games: {len(biblioteca_games)}")
    print(f"Horas totais jogadas: {total_horas}")
    print(f"Dinheiro gasto: R$ {total_gasto:.2f}")
    print(f"Games zerados: {games_zerados}")
    print(f"Games bem avaliados (8+): {len(games_bem_avaliados)}")
    print(f"Tem jogos caros (>R$100): {'Sim' if tem_games_caros else 'Não'}")
    print(f"Todos os jogos foram avaliados: {'Sim' if todos_avaliados else 'Não'}")

# ========== MENU PRINCIPAL ==========

def mostrar_menu():
    """Menu principal do sistema"""
    opcoes = [  # lista com opções
        "Adicionar novo game",
        "Ver biblioteca completa", 
        "Adicionar horas jogadas",
        "Avaliar um jogo",
        "Marcar jogo como zerado",
        "Sistema de recomendação",
        "Relatórios e estatísticas",
        "Testar funções avançadas",
        "Configurações",
        "Sair"
    ]
    
    print("\n" + "="*50)
    print(" SISTEMA DE GERENCIAMENTO DE GAMES ")
    print("="*50)
    
    # FOR para mostrar opções numeradas
    for i, opcao in enumerate(opcoes, 1):
        print(f"{i}. {opcao}")

def encontrar_game_por_nome(nome):
    """Função auxiliar para encontrar jogo na biblioteca"""
    nome_busca = nome.lower()  # convertendo para minúsculo para busca
    for game in biblioteca_games:
        if nome_busca in game.nome.lower():
            return game
    return None

def menu_testes_avancados():
    """Menu para testar as funções lambda, map, filter"""
    print("\n=== Testes de Funções Avançadas ===")
    print("1. Testar MAP (aplicar desconto)")
    print("2. Testar FILTER (filtrar jogos)")
    print("3. Testar LAMBDA (custo benefício)")
    print("4. Voltar")
    
    opcao = input("Escolha uma opção: ")
    
    if opcao == "1":
        if biblioteca_games:
            desconto = float(input("Digite o desconto (%): "))
            aplicar_desconto_biblioteca(desconto)
        else:
            print("Adicione alguns jogos primeiro!")
    
    elif opcao == "2":
        print("Filtros disponíveis: caros, zerados, bem_avaliados")
        criterio = input("Digite o critério: ")
        resultados = filtrar_games_por_criterio(criterio)
        
        if resultados:
            print(f"\nJogos filtrados ({criterio}):")
            for game in resultados:
                print(f" {game}")
        else:
            print("Nenhum jogo encontrado com esse critério.")
    
    elif opcao == "3":
        if biblioteca_games:
            print("\n Custo Benefício (horas por real):")
            for game in biblioteca_games:
                cb = custo_beneficio(game)
                print(f"{game.nome}: {cb:.2f} horas/R$")
        else:
            print("Adicione alguns jogos primeiro!")

def main():
    """Função principal  executa o sistema"""
    
    # Vou adicionar alguns jogos de exemplo para testar
    # (deixei isso aqui para não ficar sempre vazio durante os testes)
    exemplos_iniciais = False  # mudo para True quando quero testar rapidamente
    
    if exemplos_iniciais:
        # Testando a função de compra múltipla
        game1 = Game("The Witcher 3", "RPG", "PC", 89.90)
        game2 = Game("Cyberpunk 2077", "RPG", "PC", 199.90)
        game3 = Game("Hollow Knight", "Aventura", "PC", 29.90)
        
        registrar_compra_multipla(game1, game2, game3, 
                                desconto=15, loja="Steam", promocao=True)
    
    # Loop principal do sistema
    while True:
        mostrar_menu()
        
        try:  # tratamento básico de erro
            opcao = input("\nEscolha uma opção (1 10): ")
            
            if opcao == "1":
                # Adicionar novo game
                print("\n Adicionar Novo Game ")
                nome = input("Nome do jogo: ")
                nome = formatar_nome(nome)  # usando lambda
                
                print(f"Gêneros disponíveis: {', '.join(generos_populares)}")
                genero = input("Gênero: ")
                
                print(f"Plataformas: {', '.join(PLATAFORMAS_DISPONIVEIS)}")
                plataforma = input("Plataforma: ")
                
                preco = float(input("Preço (R$): "))
                
                novo_game = Game(nome, genero, plataforma, preco)
                biblioteca_games.append(novo_game)
                
                print(f"{nome} adicionado à biblioteca!")
            
            elif opcao == "2":
                # Ver biblioteca
                if biblioteca_games:
                    print("\n Sua Biblioteca:")
                    for i, game in enumerate(biblioteca_games, 1):
                        print(f"{i}. {game}")
                else:
                    print("Sua biblioteca está vazia!")
            
            elif opcao == "3":
                # Adicionar horas
                if not biblioteca_games:
                    print("Adicione alguns jogos primeiro!")
                    continue
                
                nome = input("Nome do jogo: ")
                game = encontrar_game_por_nome(nome)
                
                if game:
                    horas = float(input("Quantas horas jogou: "))
                    if game.adicionar_horas(horas):
                        print(f"{horas} horas adicionadas a {game.nome}")
                        print(f"Total de horas: {game.horas_jogadas}")
                    else:
                        print("Número de horas inválido!")
                else:
                    print("Jogo não encontrado!")
            
            elif opcao == "4":
                # Avaliar jogo
                if not biblioteca_games:
                    print("Adicione alguns jogos primeiro!")
                    continue
                
                nome = input("Nome do jogo para avaliar: ")
                game = encontrar_game_por_nome(nome)
                
                if game:
                    nota = float(input("Sua nota (0 10): "))
                    if game.avaliar_jogo(nota):
                        print(f"Você deu nota {nota} para {game.nome}")
                    else:
                        print("Nota deve ser entre 0 e 10!")
                else:
                    print("Jogo não encontrado!")
            
            elif opcao == "5":
                # Marcar como zerado
                if not biblioteca_games:
                    print("Adicione alguns jogos primeiro!")
                    continue
                    
                nome = input("Nome do jogo que você zerou: ")
                game = encontrar_game_por_nome(nome)
                
                if game:
                    game.marcar_como_zerado()
                    obs = input("Quer adicionar algum comentário? (Enter para pular): ")
                    if obs:
                        game.adicionar_observacao(obs)
                else:
                    print("Jogo não encontrado!")
            
            elif opcao == "6":
                # Sistema de recomendação
                genero = input("Qual seu gênero favorito? ")
                budget = float(input("Qual seu orçamento (R$)? "))
                sistema_recomendacao(genero, budget)
            
            elif opcao == "7":
                # Relatórios
                relatorio_detalhado()
            
            elif opcao == "8":
                # Testes avançados
                menu_testes_avancados()
            
            elif opcao == "9":
                # Configurações (básico)
                print(f"\n Configurações atuais:")
                for chave, valor in config_usuario.items():
                    print(f"{chave}: {valor}")
                
                # Operador ternário para mostrar status
                status_budget = "Alto" if config_usuario['budget_mensal'] > 150 else "Baixo"
                print(f"Status do orçamento: {status_budget}")
            
            elif opcao == "10":
                print("Saindo do sistema... Até mais!")
                break
            
            else:
                print("Opção inválida! Tente novamente.")
        
        except ValueError:
            print("Erro: Digite um número válido!")
        except Exception as e:
            print(f"Erro inesperado: {e}")

# Executa o programa
if __name__ == "__main__":
    print("Iniciando Sistema de Games...")
    main()
