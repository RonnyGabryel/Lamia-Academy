import os # importa o módulo para manipulação
import torch # importa a biblioteca principal do pytorch
import torch.nn as nn # importa o módulo de construção de redes neurais
from torch.nn import functional as F # importa funções prontas como perdas

batch_size = 32 # define a quantidade de sequências processadas
block_size = 8 # define o tamanho máximo do contexto para as previsões
max_iters = 3000 # define o número total de passos de treinamento
eval_interval = 300 # define a frequência de passos para avaliar
learning_rate = 1e-2 # define a taxa de aprendizado para o otimizador
device = 'cuda' if torch.cuda.is_available() else 'cpu' # detecta e usa a placa de vídeo caso esteja disponível
eval_iters = 200 # define quantos lotes serão usados para calcular a média da perda

print(device)
torch.manual_seed(1337) # fixa a semente aleatória para garantir reprodutibilidade

file = os.path.join(os.path.dirname(__file__), 'input.txt') # localiza o arquivo de texto na mesma pasta
with open(file, 'r', encoding='utf-8') as f: # abre o arquivo de texto com codificação
    text = f.read()

chars = sorted(list(set(text))) # extrai e ordena todos os caracteres
vocab_size = len(chars) # guarda o tamanho total do vocabulario
stoi = { ch:i for i,ch in enumerate(chars) } # monta o dicionário que converte caractere
itos = { i:ch for i,ch in enumerate(chars) } # monta o dicionário que converte
encode = lambda s: [stoi[c] for c in s] # define a função que transforma
decode = lambda l: ''.join([itos[i] for i in l]) # define a função que transforma

data = torch.tensor(encode(text), dtype=torch.long) # converte todo o texto codificado
n = int(0.9*len(data)) # calcula o índice de divisão para separar
train_data = data[:n] # separa os primeiros dados
val_data = data[n:] # separa os restantes para o conjunto de validação

def get_batch(split): # define a funcao
    data = train_data if split == 'train' else val_data # escolhe a base de dados
    ix = torch.randint(len(data) - block_size, (batch_size,)) # sorteia os índices iniciais
    x = torch.stack([data[i:i+block_size] for i in ix]) # agrupa os blocos de dados de entrada
    y = torch.stack([data[i+1:i+block_size+1] for i in ix]) # agrupa os blocos de dados alvos
    x, y = x.to(device), y.to(device) # envia os tensores gerados para a memoria do dispositivo
    return x, y

@torch.no_grad()
def estimate_loss(): # define a função que avalia
    out = {} # cria o dicionario para guardar o resultado
    model.eval() # coloca o modelo em modo de avaliação de desempenho
    for split in ['train', 'val']: # percorre as duas bases de dados separadamente
        losses = torch.zeros(eval_iters) # cria um tensor para armazenar as perdas
        for k in range(eval_iters): # roda o laço pelo numero
            X, Y = get_batch(split) # busca um lote de dados correspondente
            logits, loss = model(X, Y) # passa os dados pelo modelo para obter
            losses[k] = loss.item() # armazena o valor numérico da perda no histórico
        out[split] = losses.mean() # calcula a media das perdas
    model.train() # recoloca o modelo de volta no modo
    return out

class BigramLanguageModel(nn.Module): # define a classe do modelo

    def __init__(self, vocab_size): # define o metodo
        super().__init__() # executa a inicializacao padrao
        self.token_embedding_table = nn.Embedding(vocab_size, vocab_size) # cria a tabela de mapeamento direto

    def forward(self, idx, targets=None): # define a lógica de passagem
        logits = self.token_embedding_table(idx) # faz a consulta na tabela

        if targets is None: # checa se o modelo está apenas prevendo
            loss = None # define a perda como nula pois não há alvos
        else: # caso os alvos tenham sido fornecido
            B, T, C = logits.shape # extrai as dimensões de lote
            logits = logits.view(B*T, C) # achata o tensor de previsões para o formato
            targets = targets.view(B*T) # achata o tensor de alvos para o formato
            loss = F.cross_entropy(logits, targets) # calcula o erro comparando as previsoe

        return logits, loss

    def generate(self, idx, max_new_tokens):
        for _ in range(max_new_tokens): # roda o laço repetindo o processo
            logits, loss = self(idx) # passa o contexto atual pelo modelo
            logits = logits[:, -1, :] # isola apenas as previsões feitas para o último caractere
            probs = F.softmax(logits, dim=-1) # converte as pontuações brutas do último caractere
            idx_next = torch.multinomial(probs, num_samples=1) # escolhe um caractere por amostragem baseada
            idx = torch.cat((idx, idx_next), dim=1) # junta o novo caractere sorteado
        return idx

model = BigramLanguageModel(vocab_size) # cria o objeto do modelo
m = model.to(device) # move toda a estrutura

optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate) # inicializa o algoritmo de otimizacao

for iter in range(max_iters): # inicia o treinamento

    if iter % eval_interval == 0: # verifica se chegou o momento de avaliar
        losses = estimate_loss() # calcula as médias das perdas atuais
        print(f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}") # exibe na tela o andamento das perdas do treino

    xb, yb = get_batch('train') # retira um novo lote aleatório com dados

    logits, loss = model(xb, yb) # executa a passagem dos dados para calcular
    optimizer.zero_grad(set_to_none=True) # zera os gradientes antigos liberando espaço
    loss.backward()
    optimizer.step()

context = torch.zeros((1, 1), dtype=torch.long, device=device) # inicializa o contexto gerador com uma matriz
print(decode(m.generate(context, max_new_tokens=500)[0].tolist())) # gera 500 novos caracteres numericos