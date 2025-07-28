# Relatório 2 – Aula: Linguagem de Programação Python (I)

### Listas
print('Listas')
print(' ')

# Listas em Python começam no índice 0
# Ou seja: número 1 está no índice 0, número 2 no índice 1, e assim por diante
nums = [1, 2, 3]

# type(nums) mostra que 'nums' é uma lista
print(type(nums))  # <class 'list'>

# append() adiciona elementos ao final da lista
nums.append(3)
nums.append(4)
nums.append(5)

# len() retorna o tamanho da lista, ou seja, quantos elementos ela tem
print(len(nums))  # Deve mostrar 6

# Esta linha está comentada, mas se fosse executada, ela alteraria o valor do índice 3 para 100
nums[3] = 100

# insert(posição, valor) insere um valor na posição indicada
# Aqui, estamos colocando o valor -200 na posição 0 (começo da lista)
nums.insert(0, -200)

# A lista tem 7 elementos agora (índices de 0 a 6), mas se tentar acessar um índice que **não existe**, dá erro
# Se você tentar acessar um índice maior que o último, dá IndexError
# Então essa linha abaixo vai dar erro se você já não tiver 7 ou mais elementos na lista
print(nums[6])  #só funciona se a lista tiver pelo menos 7 elementos

# Índices negativos contam a partir do fim da lista:
# -1 é o último elemento, -2 é o penúltimo, e assim por diante
print(nums[-1])  # Último elemento
print(nums[-2])  # Penúltimo elemento

# Mostra todos os elementos da lista
print(nums)

### Tuplas

print("Tuplas")
print(' ')

# Tuplas são como listas mas imutáveis (não dá pra alterar, adicionar ou remover elementos depois de criadas)
nomes = ('Ana', 'bia', 'Gui', 'rafael', 'luigi')

# Aqui usamos o operador 'in' para verificar se o valor 'bia' está dentro da tupla
# Isso também funciona em listas
# A comparação é sensível a maiúsculas/minúsculas, ou seja, 'bia' ≠ 'Bia'
print('bia' in nomes)  # True

# Acessando elementos por índice:
print(nomes[0])     # Primeiro elemento 'Ana'

# Slice da tupla:
# nomes[1:3] pega os elementos do índice 1 até o 2 (o 3 não entra)
# Ou seja: mostra ['bia', 'Gui']
print(nomes[1:3])   

# nomes[1:] pega do índice 1 até o final
print(nomes[1:])    # ['bia', 'Gui', 'rafael', 'luigi']

# nomes[1:-1] vai do índice 1 até o penúltimo (índice -1 é o último, mas ele não é incluído)
print(nomes[1:-1])  # ['bia', 'Gui', 'rafael']

# nomes[2:] pega do índice 2 até o fim
print(nomes[2:])    # ['Gui', 'rafael', 'luigi']

# nomes[:-2] pega do começo até dois antes do fim (exclui os dois últimos)
print(nomes[:-2])   # ['Ana', 'bia', 'Gui']

# Se quiser criar uma tupla com um único elemento, precisa da vírgula no final
# Senão o Python trata como uma string comum (ou outro tipo isolado)
x = ('bia',)
print(type(x))  # <class 'tuple'> — sem vírgula seria <class 'str'>

# len() mostra quantos elementos tem na tupla
print(len(nomes))  # 5

# type() mostra que é uma tupla
print(type(nomes))  # <class 'tuple'>

# Imprime a tupla completa
print(nomes)

### Conjuntos

print("Conjuntos")
print(' ')

# Um conjunto (set) em Python é definido com chaves {}, mas diferente de dicionário, não tem pares chave:valor
# Sets não mantêm ordem e não aceitam elementos duplicados
print({1, 2, 3})          # Cria e imprime um conjunto simples
print(type({1, 2, 3}))    # Mostra que o tipo é 'set'

# Se colocarmos elementos repetidos, o set automaticamente ignora os duplicados
# print({1, 2, 3, 3, 3, 3})  #Exemplo: mesmo colocando vários 3, o conjunto só terá um

# Vamos criar um conjunto com valores repetidos
conj = {1, 2, 3, 3, 3, 3}

# Não é possível acessar um set com índice (como conj[1])
# Isso vai gerar um erro: TypeError: 'set' object is not subscriptable
# print(conj[1])

# Mas podemos imprimir o conjunto inteiro normalmente
print(conj)  # Vai mostrar: {1, 2, 3}

# len() mostra quantos elementos únicos existem no conjunto
# Como os repetidos são ignorados, o resultado será 3
print(len(conj))

### Dicionários

print("Dicionários")
print(' ')


# Vamos definir um dicionário chamado 'aluno'
# Dicionários em Python são estruturas que armazenam **pares chave:valor**
# A chave geralmente é uma string (mas pode ser outro tipo imutável)
# A ideia é associar um nome (a chave) a um dado específico (o valor)

aluno = {
    'nome': 'Pedrinho',   # chave 'nome' com valor 'Pedrinho'
    'nota': 9.2,          # chave 'nota' com valor numérico 9.2
    'ativo': True         # chave 'ativo' com valor booleano True
}

# type(aluno) mostra que o tipo da variável é 'dict' (dicionário)
print(type(aluno))  # <class 'dict'>

# Acessando valores específicos do dicionário usando a chave entre colchetes
print(aluno['nome'])   # Vai imprimir o valor da chave 'nome': Pedrinho
print(aluno['nota'])   # Vai imprimir 9.2
print(aluno['ativo'])  # Vai imprimir True

# len() retorna o número de pares chave:valor dentro do dicionário
print(len(aluno))      # Vai mostrar 3, porque tem três chavess

## Operadores
### Unários

print("Unários")
print(' ')


# not é uma negação lógica
# Ele é um operador que age sobre um valor booleano (True ou False)
# Basicamente, ele inverte: True vira False, False vira True

print(not False)  # True
print(not True)   # False

# Agora uns exemplos com números:

print(-3)     # Isso é um número negativo comum -3
print(--3)    # Aqui não é incremento como em C++
              # O primeiro menos inverte o sinal, o segundo inverte de novo resultado: 3
print(+3)     # Sinal de positivo continua 3

# Em Python **não existe operador de incremento (++) ou decremento (--)**
# Isso existe em linguagens como C, C++, Java, etc.

w = 12
# w++  # Isso aqui geraria um erro em Python (SyntaxError)
print(w)  # Vai imprimir 12 normalmente, sem alteração

### Aritméticos

print("Aritméticos")
print(' ')

x = 10
y = 3

# Aqui usamos operadores binários (operam sobre dois valores)
# Exemplo: x + y o operador '+' atua entre dois operandos: x e y
# Isso é chamado de forma infixa (operador fica no meio), comum em Python e na maioria das linguagens

print(x + y)  # Soma 10 + 3 = 13
print(x - y)  # Subtração 10 - 3 = 7
print(x * y)  # Multiplicação 10 * 3 = 30
print(x / y)  # Divisão com resultado float 10 / 3 = 3.333...
print(x % y)  # Módulo (resto da divisão) 10 % 3 = 1

# Em linguagens como C ou Java, há outras formas:
# Prefixo: +3 (sinal antes do número), ou ++x (não existe em Python)
# Pós-fixo: x++ (também não existe em Python)
# Infixo: x + y a forma padrão em Python

# Agora um exemplo prático com par e ímpar
par = 34
impar = 33

# O operador '%' (módulo) é muito usado para verificar paridade
# Um número é par se o resto da divisão por 2 for 0
print(par % 2 == 0)     # True 34 é par

# Um número é ímpar se o resto da divisão por 2 for 1
print(impar % 2 == 1)   # True 33 é ímpar


### Relacionais

print("Relacionais")
print(' ')

# Operadores relacionais funcionam com valores numéricos também

x = 7 
y = 5 

print(x > y)   # True x é maior que y
print(x >= y)  # True x é maior ou igual a y
print(x < y)   # False x não é menor que y
print(x <= y)  # False x não é menor ou igual a y
print(x == y)  # False x não é igual a y
print(x != y)  # True x é diferente de y

# Comparações também consideram o tipo dos valores
# Aqui temos uma string '5' e um número inteiro 5
print('5' != 5)  # True são tipos diferentes (str int), então são considerados diferentes

# Em Python não existe o operador === como em JavaScript
# Em Python o '==' já verifica valor e tipo ao mesmo tempo


### Atribuição

print("Atribuição")
print(' ')

# A atribuição é usada desde o começo, mas existem variações:
# Atribuições aditivas, subtrativas, multiplicativas, divisivas, etc.

resultado = 2    
print(resultado)  # Vai imprimir 2

# Aqui a variável 'resultado' recebe um novo valor
# Python simplesmente joga fora o valor antigo e armazena o novo
resultado = 3
print(resultado)  # Agora imprime 3

# Em Python, variáveis não têm tipo fixo (tipagem dinâmica)
# Podemos trocar um número por uma string sem problema nenhum
resultado = 'Rapaz vontade de comer bolacha com plástico e tudo'
print(resultado)  # Agora imprime a string

# Vamos voltar para um valor numérico e testar as variações de atribuição
resultado = 3

# Isso aqui é diferente do que parece:
resultado = +resultado  # Isso não soma com ele mesmo, só reforça o sinal positivo (resultado continua 3)

# Atribuição aditiva:
resultado += 3  # resultado = resultado + 3  agora é 6

# Atribuição subtrativa:
resultado -= 3  # resultado = resultado - 3  agora é 3 de novo

# Atribuição multiplicativa:
resultado *= 3  # resultado = resultado * 3  agora é 9

# Atribuição divisiva:
resultado /= 3  # resultado = resultado / 3  agora é 3.0 (note que vira float)

# Atribuição modular:
resultado %= 6  # resultado = resultado % 6  agora é 3.0, pois 3.0 % 6 = 3.0

print(resultado)  # Imprime o resultado final


### Lógicos

print("Lógicos")
print(' ')

b1 = True
b2 = False
b3 = True

# Operadores lógicos:
# AND retorna True só se **TODAS** as expressões forem verdadeiras
print(b1 and b2 and b3)  # False porque b2 é False

# OR retorna True se **PELO MENOS UMA** das expressões for verdadeira
print(b1 or b2 or b3)  # True → b1 e b3 são True

# Diferença lógica  equivalente ao operador != em C
print(b1 != b2)  # True  b1 e b2 são diferentes

# NOT  inverte o valor lógico
print(not b1)  # False  inverte True
print(not b2)  # True  inverte False
print(not b3)  # False

# Combinação de operadores:
# Aqui usamos AND e NOT juntos
print(b1 and not b2 and b3)  
# True and True and True tudo verdadeiro, então retorna True

# É possível combinar operadores lógicos com operadores relacionais
x = 3
y = 4

# Aqui o resultado é:
# b1  True
# not b2 True
# x < y True (3 < 4)
# Então: True and True and True resultado final: True
print(b1 and not b2 and x < y)

### Ternários

print("Ternários")
print(' ')

# Aprendendo operador ternário (forma compacta de if/else)

lockdown = False
grana = 30

# Sintaxe do ternário em Python: 
# valor_se_verdadeiro if condição else valor_se_falso
# Aqui estamos dizendo:
# Se lockdown for True ou grana for menor ou igual a 100 status será 'Em casa'
# Senão, será 'LES BORA'
status = 'Em casa' if lockdown or grana <= 100 else 'LES BORA'

# Diferente de C, aqui não precisa abrir parênteses nem usar `?` e `:` — bem mais limpo
# Em C seria algo assim:
# status = (lockdown || grana <= 100) ? "Em casa" : "LES BORA";

# Imprimindo o status formatado
print(f'{status}')  # Interpreta a variável status e imprime o valor dela

# Aqui também, só que adicionamos uma string na frente
print(f'O status é: {status}')  # Interpreta status dentro da f-string

## Controle
### IF

print(' ')
print("If")
print(' ')


# Interessante: 'if' é uma palavra reservada em Python
# Por isso o nome do arquivo precisa evitar só 'if_1.py'

nota = float(input('Informe a nota do aluno: '))
presenca = True if input('presença (s/n):') == 's' else False
#ele faz uma verificação para ver se tem presença

# Em Python, blocos de código são definidos por indentação (TAB ou 4 espaços)
# Nada de chaves como em C, só a indentação que define o bloco do if/elif/else

if nota >= 9 and presenca:
    print('Passou com excelência!')
elif nota >= 7:
    print('Recuperação') 
elif nota >= 5.5:
    print('Reprovou')
else:
    print('Desempenho muito abaixo do esperado') 

# Exibe a nota informada no final
print(nota)

# Em Python, certos valores são considerados "false" (avaliam como False em contextos booleanos)
# E outros são "true" (avaliam como True), mesmo que não sejam do tipo bool

a = 'valor'  # String não vazia é true entra no if

a = 0        # Número zero é false cai no else
a = -1       # Qualquer número diferente de zero, mesmo negativo é true
a = ''       # String vazia é false
a = ' '      # String com espaço ainda é considerada não vazia é true
a = []       # Lista vazia false
a = {}       # Dicionário vazio false

# Essa estrutura verifica se 'a' é "verdadeiro" (true) ou "falso" (false)
if a:
    print('Tá tendo!')  # Executa se for true
else:
    print('Não existe')  # Executa se for false
    
### FOR

print(' ')
print("For")
print(' ')


# Comparado ao C, o Python é realmente muito mais amigável pra escrever laços

# range(10) vai de 0 até 9 (não inclui o 10)
for i in range(10):
    print(i, end=' ')  # end=' ' evita a quebra de linha e imprime tudo na mesma linha
print(' ')

# range(1, 11) vai de 1 até 10 (não inclui o 11)
for i in range(1, 11):
    print(i, end=' ')
print(' ')

# range com passo vai de 1 até 99, pulando de 7 em 7
for i in range(1, 100, 7):
    print(i, end=' ')
print(' ')

# contagem decrescente começa em 20 e vai até 1, de 3 em 3 para trás
for i in range(20, 0, -3):
    print(i, end=' ')
print(' ')

# Iterando sobre uma lista
nums = [2, 4, 6, 8]
for n in nums:
    print(n, end=' ')
print()

print(' ')

# Iterando sobre uma string vai letra por letra
texto = 'Rapaz'
for letra in texto:
    print(letra)

# Iterando sobre um set elimina duplicatas automaticamente
for n in {1, 2, 3, 4, 4, 4}:
    print(n)  # só imprime 1, 2, 3, 4

# Dicionário com chaves e valores
produto = {
    'nome': 'Patricio',
    'especie': 'pinguin', 
}

# Iterando apenas nas chaves
for atributo in produto:
    print(atributo, '==>', produto[atributo])

# Iterando nas chaves e valores ao mesmo tempo com .items()
for atributo, valor in produto.items():
    print(atributo, '==>', valor)  # Corrigido: antes usava "nome", mas não existia essa variável

### While

print(' ')
print("While")
print(' ')

# Primeiro exemplo: loop que só para quando o usuário digitar -1
x = 0

# Enquanto x for diferente de -1, continua pedindo número
while x != -1:
    x = float(input('Digite um número (ou -1 para sair):\n'))

print('Saiu!')  # Quando x for -1, sai do loop


# Calcular a média das notas
total = 0      # Soma das notas
qtde = 0       # Quantidade de notas válidas
nota = None    # Pode começar como None (ou 1) pra garantir que o loop rode ao menos uma vez
nota = 1  # valor inicial só pra entrar no loop

while nota != 0:
    nota = float(input('Atribua uma nota (ou 0 para sair):\n'))
    
    if nota != 0:
        qtde += 1
        total += nota

        # Só calcula a média se já tiver pelo menos uma nota válida
        print(f'A média da turma é: {total / qtde}')

print('Saiu!')


## Funções
### Básicas

print(' ')
print("Básicas")
print(' ')

# Quando for definir uma função, usa-se a palavra-chave def, 
# seguida do nome da função e parênteses com os parâmetros de entrada.
# Mesmo que a função não faça nada ainda, é preciso usar pass 
# para indicar que ela está vazia (evita erro de sintaxe).

def saudacao(nome='Pessoa', idade=20): 
    print(f'Bom dia, {nome}! Você nem parece ter {idade} anos!')

# Posso criar outra função com o mesmo nome, mas isso **sobrescreve** a anterior.
# Em Python, a última definição com o mesmo nome "apaga" a anterior (não tem sobrecarga).
# Exemplo (comentado para não sobrescrever de verdade):
# def saudacao(): 
#     print('Busque conhecimento!')

# Esse bloco abaixo serve para garantir que o código dentro dele
# só vai rodar se o arquivo for executado diretamente (e não importado).
if __name__ == '__main__':
    saudacao(nome='Pessoa', idade=20)


# Agora outra função:
def soma_e_mutiplo(a, b, x):
    return a + b * x

# Importante lembrar em Python, a multiplicação tem precedência sobre a soma
# Ou seja, a expressão `a + b * x` é interpretada como: a + (b * x)

### Args

print(' ')
print("Args")
print(' ')

# PEP significa Python Enhancement Proposal (Proposta de Aprimoramento do Python).
# É o nome dado aos documentos que descrevem melhorias ou padrões para a linguagem Python,
# como por exemplo o famoso PEP 8 (guia de estilo de código).

# Função com *args:
def soma(*nums):
    # *nums permite receber vários argumentos não nomeados (empacotados em uma tupla).
    total = 0
    for n in nums:
        total += n
    return total
    # Exemplo de uso: soma(1, 2, 3) → 6

# Função com **kwargs:
def resultado_final(**kwargs):
    # **kwargs permite receber vários argumentos nomeados (empacotados em um dicionário).
    
    # Aqui usamos uma expressão condicional para definir o status com base na nota:
    status = 'aprovado(a)' if kwargs['nota'] >= 7 else 'reprovado(a)'
    
    # A string final é construída usando uma f-string:
    return f'{kwargs["nome"]} foi {status}'

    # Observação:
    # - Aspas simples (') e duplas (") servem para criar strings. Você pode usar qualquer uma.
    # - Mas dentro de f-strings, se a string principal estiver entre aspas simples,
    #   use aspas duplas dentro (ou vice-versa) para evitar erro de sintaxe.

# Exemplo:
# resultado_final(nome='Ana', nota=8)  'Ana foi aprovado(a)'
# resultado_final(nome='João', nota=4)  'João foi reprovado(a)'



### map_reduce

print(' ')
print("map_reduce")
print(' ')

# Map é uma função que aplica outra função a cada item de uma lista (ou iterável),
# retornando uma **nova lista transformada** (do mesmo tamanho).
# Útil quando você quer "mapear" de uma lista para outra tipo fazer uma conversão em massa.

from functools import reduce  # Importa a função reduce, que serve pra acumular valores (tipo somar todos os itens de uma lista)

# Função que recebe um valor delta e retorna outra função (função dentro da função)
def somar_nota(delta):
    def somar(nota):
        return nota + delta
    return somar

# Lista original de notas
notas = [6.4, 7.2, 5.4, 8.4]

# Aplica a função de somar 1.5 em cada nota — com map
notas_finais_1 = map(somar_nota(1.5), notas)

# Aplica a função de somar 1.6 em cada nota — só pra mostrar que dá pra variar o delta
notas_finais_2 = map(somar_nota(1.6), notas)

# Map retorna um iterador então pra ver os valores você pode converter em lista ou iterar com for
print(notas_finais_1)
print(' ')
print(notas_finais_2) 
print(' ')

# Agora somando todas as notas manualmente
total = 0
for n in notas:
    total += n

print(total)  # Soma total das notas originais
print(' ')

# Definindo uma função de soma normal (recebe dois valores e retorna a soma)
def somar(a, b):
    return a + b

# Usando reduce pra acumular os valores da lista (começando do 0)
reduce = reduce(somar, notas, 0)

print(total)  # Mostra de novo o total (igual ao anterior)

# Agora usando enumerate pra iterar pela lista com índice
for i, nota in enumerate(notas):  # enumerate retorna índice + valor
    print(i, nota)  # Mostra a posição e a nota
    notas[i] = nota + 1.5  # Soma 1.5 em cada nota

print(notas)  # Lista atualizada com 1.5 somado em cada valor
print(' ')

# Mesmo resultado do for acima, mas usando range(len()) — estilo mais manual
for i in range(len(notas)):
    notas[i] = nota + 1.5  # Isso aqui tá errado — 'nota' não está definido aqui

print(notas)  # Isso vai dar erro ou repetir o valor errado — corrigir a variável
print(' ')


### lambdas

print(' ')
print("lambdas")
print(' ')

from functools import reduce

# Lista de dicionários cada um representando um aluno com nome e nota
alunos = [
    {'nome': 'Ana', 'nota': 7.2},
    {'nome': 'Breno', 'nota': 8.1},
    {'nome': 'Claudio', 'nota': 8.7},
    {'nome': 'Pedro', 'nota': 6.4},
    {'nome': 'Rafael', 'nota': 6.7},
]

# filter serve para filtrar elementos de uma lista com base numa condição
# lambda é uma função anônima (sem nome) muito usada para expressar lógica simples
aluno_aprovado = lambda aluno: aluno['nota'] >= 7  # passa só os que têm nota => 7

# Extrai apenas a nota de cada aluno map vai aplicar isso em cada elemento
obter_nota = lambda aluno: aluno['nota']

# Função para somar dois valores usada no reduce
somar = lambda a, b: a + b

# Primeiro filtra só os alunos aprovados nota => 7
alunos_aprovados = filter(aluno_aprovado, alunos)

# Depois pega só as notas desses alunos
notas_alunos_aprovados = map(obter_nota, alunos_aprovados)

# Agora soma todas essas notas com reduce começando do 0
total = reduce(somar, notas_alunos_aprovados, 0)

# Mostra o iterador de notas ainda não convertido em lista
print(notas_alunos_aprovados)

print(' ')

# Mostra a nota do terceiro aluno índice 2 Claudio
print(obter_nota(alunos[2]))  # 8.7

print(' ')

# Mostra a lista original de alunos
print(alunos)

print(' ')

print(aluno_aprovado)

### Comprehension

print(' ')
print("Comprehension")
print(' ')

from functools import reduce

# Lista de dicionários, cada um representando um aluno com nome e nota
alunos = [
    {'nome': 'Ana', 'nota': 7.2},
    {'nome': 'Breno', 'nota': 8.1},
    {'nome': 'Claudio', 'nota': 8.7},
    {'nome': 'Pedro', 'nota': 6.4},
    {'nome': 'Rafael', 'nota': 6.7},
]

# filter serve para filtrar elementos de uma lista com base numa condição
# lambda é uma função anônima (sem nome) muito usada para expressar lógica simples
aluno_aprovado = lambda aluno: aluno['nota'] >= 7  # passa só os que têm nota => 7

# Lambda que extrai a nota de um aluno
obter_nota = lambda aluno: aluno['nota']

# Lambda que soma dois valores (usado no reduce)
somar = lambda a, b: a + b

# Aqui a variável 'aluno_aprovado' foi redefinida como uma lista de notas (substitui a função acima)
# List comprehension: extrai apenas as notas da lista de alunos
aluno_aprovado = [aluno['nota'] for aluno in alunos]
print(aluno_aprovado)  # Exibe só as notas

print(' ')

# Agora 'aluno_aprovado' vira uma lista com os nomes dos alunos
aluno_aprovado = [aluno['nome'] for aluno in alunos]
print(aluno_aprovado)  # Exibe só os nomes

print(' ')

# Agora 'aluno_aprovado' vira uma lista de dicionários, contendo apenas os alunos com nota >= 7
aluno_aprovado = [aluno for aluno in alunos if aluno['nota'] >= 7]
print(aluno_aprovado)  # Exibe apenas os alunos aprovados (nota >= 7)

print(' ')

# Extrai só as notas dos alunos aprovados
notas_alunos_aprovados = [aluno['nota'] for aluno in aluno_aprovado]

# Soma todas as notas dos aprovados usando reduce
total = reduce(somar, notas_alunos_aprovados, 0)

# Calcula a média dos alunos aprovados
print(total / len(aluno_aprovado))

### funcionais

print(' ')
print("funcionais")
print(' ')

# Funções simples:
def soma(a, b):
    return a + b

def sub(a, b):
    return a - b

# Aqui, estou atribuindo a função 'soma' a uma variável chamada 'somar'.
# Isso significa que 'somar' agora pode ser usada como função também.
somar = soma
print(soma(3, 4))  # Resultado: 7

# Função que recebe outra função como parâmetro:
def opercao_aritimetica(fn, op1, op2):
    return fn(op1, op2)

# Passando a função 'soma' como argumento:
resultado = opercao_aritimetica(soma, 13, 48)
print(resultado)  # 61

# Passando a função 'sub':
resultado = opercao_aritimetica(sub, 13, 48)
print(resultado)  # -35

# Função que retorna outra função (função interna / função de alta ordem):
def soma_parcial(a):
    # Dentro dela, é criada outra função que recebe 'b' e soma com 'a':
    def concluir_soma(b):
        return a + b
    return concluir_soma
    # Isso é chamado de "closure" — a função interna lembra do valor de 'a'.

# Criando uma versão fixa da soma com 'a = 1':
soma_1 = soma_parcial(1)

# Agora posso passar apenas o valor de 'b':
r1 = soma_1(2)  # 1 + 2 = 3
r2 = soma_1(3)  # 1 + 3 = 4
r3 = soma_1(4)  # 1 + 4 = 5

# Também posso usar de forma direta (sem guardar na variável):
resultado_final = soma_parcial(10)(12)  # 10 + 12 = 22

# Mostrando todos os resultados:
print(resultado_final, r1, r2, r3)  # 22 3 4 5

## Classe
### Produto

print(' ')
print("Produto")
print(' ')

# Definição da classe Produto
class Produto:
    def __init__(self, nome, preco=1.99, desconto=0):
        self.nome = nome                   # Nome do produto (acessível publicamente)
        self.__preco = preco               # Preço do produto (atributo privado)
        self.desconto = desconto           # Desconto como percentual (ex: 0.1 = 10%)

    # Getter para o atributo privado __preco
    @property
    def preco(self):
        return self.__preco

    # Setter para o atributo preco com validação
    @preco.setter
    def preco(self, novo_preco):
        if novo_preco > 0:
            self.__preco = novo_preco   # Atribui novo valor ao preço se for positivo

    # Método que calcula o preço com desconto aplicado
    def preco_com_desconto(self):
        return (1 - self.desconto) * self.preco

# Criação de dois objetos da classe Produto
p1 = Produto('Caneta', 10, 0.1)     # 10% de desconto
p2 = Produto('Caderno', 12.99, 0.2) # 20% de desconto

# Tentativa de alterar o preço para um valor negativo será ignorada pelo setter
p1.preco = -70     # Ignorado preço não muda
p2.preco = -1.99   # Também ignorado

# Impressão dos dados dos produtos
# A última parte precisa ser chamada com parênteses, pois é uma função
print(p1.nome, p1.preco, p1.desconto, p1.preco_com_desconto())  
print(' ')
print(p2.nome, p2.preco, p2.desconto, p2.preco_com_desconto())  

###Membros

print(' ')
print("Membros")
print(' ')

# Classe aninhada dentro de Membros (embora isso não seja comum ou necessário)
class Membros:

    # Classe interna Contador
    class Contador:
        contador = 0  # Atributo de classe (compartilhado entre todas as instâncias)

        def inst(self):
            return 'Foi!'  # Método de instância

        @classmethod
        def inc(cls):
            cls.contador += 1  # Incrementa o contador da classe
            return cls.contador
        
        @classmethod
        def dec(cls):
            cls.contador -= 1  # Decrementa o contador da classe
            return cls.contador
        
        @staticmethod
        def mais_um(n):
            return n + 1  # Corrigido: variável 'i' estava incorreta

# Criando instância da classe Contador
c1 = Membros.Contador()

# Chamada do método de instância
print(c1.inst())  # Saída: "Foi!"

# Usando métodos de classe para incrementar e mostrar o contador
print(c1, Membros.Contador.inc())  # 1
print(c1, Membros.Contador.inc())  # 2
print(c1, Membros.Contador.inc())  # 3

# Usando métodos de classe para decrementar o contador
print(c1, Membros.Contador.dec())  # 2
print(c1, Membros.Contador.dec())  # 1
print(c1, Membros.Contador.dec())  # 0

# Usando método estático para somar +1 a um valor
print(Membros.Contador.mais_um(99))  # 100

###herança

print(' ')
print("Heranca")
print(' ')

# Definindo a classe base Carro
class Carro:
    def __init__(self):
        self.__velocidade = 0  # Atributo privado para armazenar a velocidade

    @property
    def velocidade(self):
        return self.__velocidade  # Getter para acessar a velocidade atual

    def acelerar(self):
        self.__velocidade += 5    # Aumenta a velocidade em 5
        return self.__velocidade
    
    def frear(self):
        self.__velocidade -= 5    # Diminui a velocidade em 5
        return self.__velocidade

# Classes Uno e Mercedes como subclasses de Carro

# Uno herda de Carro sem nenhuma modificação
class Uno(Carro):
    pass

# Mercedes herda de Carro, mas sobrescreve o método acelerar
class Mercedes(Carro):
    def acelerar(self):
        super().acelerar()  # Chama o método da classe base
        return super().acelerar()  # Chama mais uma vez e retorna o resultado final

# Testando a classe Uno
c1 = Uno()
print(c1.acelerar())  # 5
print(c1.acelerar())  # 10
print(c1.acelerar())  # 15
print(c1.frear())     # 10
print(c1.frear())     # 5
print(c1.frear())     # 0

# Testando a classe Mercedes
c1 = Mercedes()
print(c1.acelerar())  # 5
print(c1.acelerar())  # 10
print(c1.acelerar())  # 15
print(c1.frear())     # 10
print(c1.frear())     # 5
print(c1.frear())     # 0
