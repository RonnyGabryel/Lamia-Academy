# Relatório <4>- <Prática: Principais Bibliotecas e Ferramentas Python para Aprendizado de Máquina (I)>
## Sistema de Análise de Vendas - Meu projeto prático com NumPy e Pandas

import numpy as np
import pandas as pd
from datetime import datetime, timedelta

print("Bora analisar umas vendas\n")

# Criando dados de vendas do zero

# Vou fixar a semente pra gente ter sempre os mesmos resultados
np.random.seed(2024)
print("Primeiro vou criar uns dados fake de vendas pra brincar...")

# Cara, vou simular dados de vendas de um e-commerce aqui
# A ideia é usar tudo que aprendi de NumPy e Pandas numa situação real

# Definindo as categorias e regiões que vou usar
n_vendas = 1000  # mil vendas - um número bacana pra testar
categorias = ['Eletrônicos', 'Roupas', 'Casa', 'Livros', 'Esporte']
regioes = ['Norte', 'Nordeste', 'Centro-Oeste', 'Sudeste', 'Sul']

# Aqui vou gerar valores de vendas que façam sentido
print("Criando valores de vendas...")
# Uso lognormal porque vendas costumam ter muitas compras baratas e poucas caras
# É mais realista que distribuição normal
valores_vendas = np.random.lognormal(mean=4, sigma=1, size=n_vendas)
valores_vendas = np.round(valores_vendas, 2)  # deixo só 2 casas decimais - fica mais limpo
print(f"Criei {len(valores_vendas)} vendas com valor médio de R$ {valores_vendas.mean():.2f}")

# Agora vou escolher as categorias - mas não aleatório total
print("\nEscolhendo categorias...")
# Eletrônicos vende mais, então vou dar peso maior pra ele
pesos_categorias = [0.3, 0.25, 0.2, 0.15, 0.1]  # Eletrônicos domina
categorias_vendas = np.random.choice(
    categorias, 
    size=n_vendas, 
    p=pesos_categorias
)
print("Distribuição que ficou:")
for cat in categorias:
    count = np.sum(categorias_vendas == cat)
    print(f"  {cat}: {count} vendas ({count/n_vendas*100:.1f}%)")

# Regiões também precisam fazer sentido - Sudeste vende mais mesmo
print("\nDefinindo as regiões...")
# Baseei nos dados reais do Brasil - Sudeste concentra população e renda
pesos_regioes = [0.08, 0.28, 0.08, 0.42, 0.14]  # Sudeste leva vantagem
regioes_vendas = np.random.choice(
    regioes,
    size=n_vendas,
    p=pesos_regioes
)

# Criando as datas de venda - espalho ao longo de 2023
print("\nCriando datas...")
# Quero que as vendas estejam espalhadas pelo ano todo
data_inicio = datetime(2023, 1, 1)
data_fim = datetime(2023, 12, 31)
dias_diferenca = (data_fim - data_inicio).days

# Gero dias aleatórios e somo na data inicial
dias_aleatorios = np.random.randint(0, dias_diferenca, n_vendas)
datas_vendas = [data_inicio + timedelta(days=int(d)) for d in dias_aleatorios]

print(f"Vendas de {min(datas_vendas).strftime('%d/%m/%Y')} até {max(datas_vendas).strftime('%d/%m/%Y')}")

# Montando o DataFrame

print("\nAgora vou juntar tudo num DataFrame - a parte mais legal!")

# Aqui uso o pandas pra organizar tudo numa tabela bonitinha
# É muito mais fácil trabalhar com dados organizados assim
df_vendas = pd.DataFrame({
    'Data': datas_vendas,
    'Categoria': categorias_vendas,
    'Regiao': regioes_vendas,
    'Valor': valores_vendas
})

# Vou extrair umas informações extras da data - sempre útil
print("Criando campos extras...")
# Pandas facilita muito extrair ano, mês, etc. da data
df_vendas['Ano'] = df_vendas['Data'].dt.year
df_vendas['Mes'] = df_vendas['Data'].dt.month
df_vendas['Dia_Semana'] = df_vendas['Data'].dt.day_name()
df_vendas['Trimestre'] = df_vendas['Data'].dt.quarter

# Vou criar faixas de preço pra analisar melhor
print("Criando faixas de valor...")
# pd.cut() é perfeito pra isso - divide os valores em categorias
df_vendas['Faixa_Valor'] = pd.cut(
    df_vendas['Valor'], 
    bins=[0, 50, 100, 200, 500, np.inf],
    labels=['Baixo', 'Médio-Baixo', 'Médio', 'Alto', 'Premium']
)

print(f"Pronto! DataFrame com {len(df_vendas)} vendas e {len(df_vendas.columns)} colunas")
print("Dá uma olhada nas primeiras linhas:")
print(df_vendas.head())

# Hora de analisar os dados!

print("\nBora ver que insights eu consigo tirar desses dados")

# Primeiro vou dar uma olhada geral nos valores
print("Estatísticas básicas dos valores:")
print(df_vendas['Valor'].describe())
# Describe() é vida! Me dá média, mediana, quartis - tudo que preciso

# Agora vou ver como cada categoria se saiu
print("\nAnálise por categoria - aqui fica interessante:")
analise_categoria = df_vendas.groupby('Categoria')['Valor'].agg([
    'count',    # quantas vendas
    'sum',      # quanto faturou
    'mean',     # ticket médio
    'std',      # o quanto varia
    'min',      # menor venda
    'max'       # maior venda
]).round(2)

print(analise_categoria)
# GroupBy é demais! Faz todo o trabalho pesado de agrupar e calcular

# Checando as regiões também
print("\nE por região:")
analise_regiao = df_vendas.groupby('Regiao')['Valor'].agg([
    'count', 'sum', 'mean'
]).round(2)
print(analise_regiao)

# Vou ver se tem alguma sazonalidade por mês
print("\nVendas por mês - será que tem sazonalidade?")
analise_mensal = df_vendas.groupby('Mes')['Valor'].agg([
    'count', 'sum', 'mean'
]).round(2)

# Deixo os meses com nomes - fica mais fácil de ler
meses_nomes = {1:'Jan', 2:'Fev', 3:'Mar', 4:'Abr', 5:'Mai', 6:'Jun',
              7:'Jul', 8:'Ago', 9:'Set', 10:'Out', 11:'Nov', 12:'Dez'}
analise_mensal.index = [meses_nomes[i] for i in analise_mensal.index]
print(analise_mensal)

# Análises mais avançadas

print("\nAgora vou fazer umas análises mais legais...")

# Vou ver se existe correlação entre as variáveis numéricas
print("Checando correlações:")
# Só com números, claro - não tem como correlacionar texto
df_correlacao = df_vendas[['Valor', 'Mes', 'Trimestre']].corr()
print(df_correlacao.round(3))

# Quero saber dos produtos caros - premium de verdade
print("\nAnálise dos produtos premium (acima de R$ 500):")
# Filtro condicional - uma das coisas mais úteis do pandas
produtos_premium = df_vendas[df_vendas['Valor'] > 500]
premium_regiao = produtos_premium.groupby('Regiao').agg({
    'Valor': ['count', 'mean', 'sum']
}).round(2)
print(premium_regiao)

# Vou ver se tem diferença por trimestre - sazonalidade por categoria
print("\nSazonalidade: vendas por trimestre e categoria")
sazonalidade = df_vendas.groupby(['Trimestre', 'Categoria'])['Valor'].agg([
    'count', 'sum'
]).round(2)
print(sazonalidade)

# As 10 maiores vendas - sempre bom saber onde estão os outliers
print("\nTop 10 vendas:")
top_vendas = df_vendas.nlargest(10, 'Valor')[['Data', 'Categoria', 'Regiao', 'Valor']]
print(top_vendas)

# Insights e conclusões

print("\nE aí, que conclusões posso tirar? ")

# Vou descobrir qual categoria fatura mais
categoria_top = df_vendas.groupby('Categoria')['Valor'].sum().idxmax()
faturamento_top = df_vendas.groupby('Categoria')['Valor'].sum().max()

print(f" Categoria que mais fatura: {categoria_top} com R$ {faturamento_top:.2f}")

# Região com maior ticket médio - onde o pessoal gasta mais por compra
regiao_ticket_alto = df_vendas.groupby('Regiao')['Valor'].mean().idxmax()
ticket_alto_valor = df_vendas.groupby('Regiao')['Valor'].mean().max()

print(f" Região com maior ticket médio: {regiao_ticket_alto} (R$ {ticket_alto_valor:.2f})")

# Mês que mais vendeu
mes_top = df_vendas.groupby('Mes')['Valor'].sum().idxmax()
faturamento_mes_top = df_vendas.groupby('Mes')['Valor'].sum().max()

print(f" Mês que mais faturou: {meses_nomes[mes_top]} (R$ {faturamento_mes_top:.2f})")

# Algumas estatísticas interessantes usando percentis
print(f"\n Distribuição interessante:")
print(f"   80% das vendas ficam abaixo de R$ {np.percentile(df_vendas['Valor'], 80):.2f}")
vendas_altas = df_vendas['Valor'] > np.percentile(df_vendas['Valor'], 80)
print(f"   Só {np.sum(vendas_altas) / len(df_vendas) * 100:.1f}% das vendas são consideradas 'altas'")

# Minhas recomendações baseadas nos dados
print("\n MINHAS RECOMENDAÇÕES:")
print("1. Investir pesado em Eletrônicos - é onde tá o dinheiro!")
print("2. Focar no Sudeste pra volume, mas não esquecer das outras regiões")
print("3. Entender por que alguns meses vendem mais - tem sazonalidade aí")
print("4. Trabalhar produtos premium em todas as regiões - tem potencial")

print(f"\n RESUMÃO FINAL:")
print(f"   Total de vendas: {len(df_vendas):,}")
print(f"   Faturamento total: R$ {df_vendas['Valor'].sum():,.2f}")
print(f"   Ticket médio: R$ {df_vendas['Valor'].mean():.2f}")

print("\n" + "="*50)
print("MISSÃO CUMPRIDA!")
print("Usei NumPy pra gerar dados realistas")
print("Pandas pra organizar e analisar tudo")
print("E ainda tirei insights úteis pros negócios!")
print("="*50)
