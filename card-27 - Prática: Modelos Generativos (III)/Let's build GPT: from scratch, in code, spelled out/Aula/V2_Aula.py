import os  # importa o módulo para manipulação
import torch  # importa a biblioteca principal do pytorch
import torch.nn as nn  # importa o módulo de construção de redes neurais
from torch.nn import functional as F  # importa funções prontas como perdas

batch_size = 16  # define a quantidade de sequências processadas
block_size = 32  # define o tamanho máximo do contexto para as previsões
max_iters = 5000  # define o número total de passos de treinamento
eval_interval = 100  # define a frequência de passos para avaliar
learning_rate = 1e-3  # define a taxa de aprendizado para o otimizador
device = 'cuda' if torch.cuda.is_available() else 'cpu'  # detecta e usa a placa de vídeo caso esteja disponível
eval_iters = 200  # define quantos lotes serão usados para calcular a média
n_embd = 64  # define a dimensão de representação dos embeddings
n_head = 4  # define o número de cabeças de atenção em paralelo
n_layer = 4  # define o número de blocos transformers sequenciais
dropout = 0.0  # define a taxa de desativação aleatória de neurônios

print(device)
torch.manual_seed(1337)  # fixa a semente aleatória para garantir reprodutibilidade

file = os.path.join(os.path.dirname(__file__), 'input.txt')  # localiza o arquivo de texto na mesma pasta
with open(file, 'r', encoding='utf-8') as f:  # abre o arquivo de texto com codificação
    text = f.read()

chars = sorted(list(set(text)))  # extrai e ordena todos os caracteres
vocab_size = len(chars)  # guarda o tamanho total do vocabulario
stoi = {ch: i for i, ch in enumerate(chars)}  # monta o dicionário que converte caractere
itos = {i: ch for i, ch in enumerate(chars)}  # monta o dicionário que converte
encode = lambda s: [stoi[c] for c in s]  # define a função que transforma
decode = lambda l: ''.join([itos[i] for i in l])  # define a função que transforma

data = torch.tensor(encode(text), dtype=torch.long)  # converte todo o texto codificado
n = int(0.9 * len(data))  # calcula o índice de divisão para separar
train_data = data[:n]  # separa os primeiros dados
val_data = data[n:]  # separa os restantes para o conjunto de validação


def get_batch(split):  # define a funcao
    data = train_data if split == 'train' else val_data  # escolhe a base de dados
    ix = torch.randint(len(data) - block_size, (batch_size,))  # sorteia os índices iniciais
    x = torch.stack([data[i:i + block_size] for i in ix])  # agrupa os blocos de dados de entrada
    y = torch.stack([data[i + 1:i + block_size + 1] for i in ix])  # agrupa os blocos de dados alvos
    x, y = x.to(device), y.to(device)  # envia os tensores gerados para a memoria do dispositivo
    return x, y


@torch.no_grad()
def estimate_loss():  # define a função que avalia
    out = {}  # cria o dicionario para guardar o resultado
    model.eval()  # coloca o modelo em modo de avaliação de desempenho
    for split in ['train', 'val']:  # percorre as duas bases de dados separadamente
        losses = torch.zeros(eval_iters)  # cria um tensor para armazenar as perdas
        for k in range(eval_iters):  # roda o laço pelo numero
            X, Y = get_batch(split)  # busca um lote de dados correspondente
            logits, loss = model(X, Y)  # passa os dados pelo modelo para obter
            losses[k] = loss.item()  # armazena o valor numérico da perda no histórico
        out[split] = losses.mean()  # calcula a media das perdas
    model.train()  # recoloca o modelo de volta no modo
    return out


class Head(nn.Module):  # define uma única cabeça de auto-atenção

    def __init__(self, head_size):
        super().__init__()
        self.key = nn.Linear(n_embd, head_size, bias=False)  # cria a camada linear para gerar chaves
        self.query = nn.Linear(n_embd, head_size, bias=False)  # cria a camada linear para consultas
        self.value = nn.Linear(n_embd, head_size, bias=False)  # cria a camada linear para valores
        self.register_buffer('tril',
                             torch.tril(torch.ones(block_size, block_size)))  # cria a máscara triangular persistente
        self.dropout = nn.Dropout(dropout)  # cria a camada de descarte para regularização

    def forward(self, x):
        B, T, C = x.shape  # extrai as dimensões do tensor de entrada
        k = self.key(x)  # gera as chaves projetando o tensor x
        q = self.query(x)  # gera as consultas projetando o tensor x
        wei = q @ k.transpose(-2, -1) * C ** -0.5  # calcula afinidades aplicando o fator de escala
        wei = wei.masked_fill(self.tril[:T, :T] == 0, float('-inf'))  # bloqueia a comunicação com o futuro
        wei = F.softmax(wei, dim=-1)  # converte as afinidades em probabilidades por linha
        wei = self.dropout(wei)  # aplica o descarte aleatório nas probabilidades
        v = self.value(x)  # gera as informações de valor projetando x
        out = wei @ v  # pondera os valores de acordo com as probabilidades
        return out


class MultiHeadAttention(nn.Module):  # define múltiplas cabeças rodando em paralelo

    def __init__(self, num_heads, head_size):
        super().__init__()
        self.heads = nn.ModuleList([Head(head_size) for _ in range(num_heads)])  # cria a lista com as cabeças paralelas
        self.proj = nn.Linear(n_embd, n_embd)  # cria a projeção linear para misturar as saídas
        self.dropout = nn.Dropout(dropout)  # cria o descarte para a saída projetada

    def forward(self, x):
        out = torch.cat([h(x) for h in self.heads], dim=-1)  # concatena os resultados de todas as cabeças
        out = self.dropout(self.proj(out))  # projeta linearmente e aplica o descarte
        return out


class FeedForward(nn.Module):  # define a rede neural linear sequencial por token

    def __init__(self, n_embd):
        super().__init__()
        self.net = nn.Sequential(
            nn.Linear(n_embd, 4 * n_embd),  # expande a dimensão interna em quatro vezes
            nn.ReLU(),  # aplica a ativação não-linear relu
            nn.Linear(4 * n_embd, n_embd),  # projeta de volta para a dimensão original
            nn.Dropout(dropout),  # aplica a camada de descarte final
        )

    def forward(self, x):
        return self.net(x)  # passa o tensor pela sequência de camadas


class Block(nn.Module):  # define o bloco transformer completo

    def __init__(self, n_embd, n_head):
        super().__init__()
        head_size = n_embd // n_head  # calcula o tamanho interno de cada cabeça
        self.sa = MultiHeadAttention(n_head, head_size)  # cria o módulo de atenção multi-cabeça
        self.ffwd = FeedForward(n_embd)  # cria o módulo feed-forward de processamento
        self.ln1 = nn.LayerNorm(n_embd)  # cria a primeira normalização de camada
        self.ln2 = nn.LayerNorm(n_embd)  # cria a segunda normalização de camada

    def forward(self, x):
        x = x + self.sa(self.ln1(x))  # aplica normalização, atenção e soma a conexão residual
        x = x + self.ffwd(self.ln2(x))  # aplica normalização, feed-forward e soma a residual
        return x


class BigramLanguageModel(nn.Module):  # define o modelo de linguagem principal

    def __init__(self):
        super().__init__()
        self.token_embedding_table = nn.Embedding(vocab_size, n_embd)  # cria a tabela de embeddings dos caracteres
        self.positional_embedding_table = nn.Embedding(block_size, n_embd)  # cria a tabela de embeddings de posições
        self.blocks = nn.Sequential(
            *[Block(n_embd, n_head=n_head) for _ in range(n_layer)])  # empilha os blocos transformers definidos
        self.ln_f = nn.LayerNorm(n_embd)  # cria a normalização de camada final do modelo
        self.lm_head = nn.Linear(n_embd, vocab_size)  # cria a projeção linear para o vocabulário

    def forward(self, idx, targets=None):
        B, T = idx.shape  # extrai tamanho do lote e do tempo atual
        tok_emb = self.token_embedding_table(idx)  # extrai as representações dos caracteres
        pos_emb = self.positional_embedding_table(
            torch.arange(T, device=device))  # gera os vetores de posição do contexto
        x = tok_emb + pos_emb  # combina as informações de caractere e posição
        x = self.blocks(x)  # passa os dados combinados pela sequência de blocos
        x = self.ln_f(x)  # aplica a normalização final nos dados processados
        logits = self.lm_head(x)  # projeta os resultados finais para o tamanho do vocabulário

        if targets is None:  # checa se o modelo está apenas prevendo
            loss = None  # define a perda como nula pois não há alvos
        else:  # caso existam alvos para comparar
            B, T, C = logits.shape  # extrai as dimensões do tensor
            logits = logits.view(B * T, C)  # achata as previsões para 2D
            targets = targets.view(B * T)  # achata os alvos para 1D
            loss = F.cross_entropy(logits, targets)  # calcula o erro das previsões

        return logits, loss

    def generate(self, idx, max_new_tokens):  # define o método gerador de texto
        for _ in range(max_new_tokens):
            idx_cond = idx[:, -block_size:]  # limita o contexto atual ao tamanho máximo block_size
            logits, loss = self(idx_cond)  # passa o contexto limitado pelo modelo
            logits = logits[:, -1, :]  # isola as previsões referentes ao último passo
            probs = F.softmax(logits, dim=-1)  # transforma as pontuações brutas em probabilidades
            idx_next = torch.multinomial(probs, num_samples=1)  # sorteia o próximo índice baseado nas probabilidades
            idx = torch.cat((idx, idx_next), dim=1)  # anexa o caractere sorteado ao final do contexto
        return idx


model = BigramLanguageModel()  # instancia o modelo de linguagem completo
m = model.to(device)  # move toda a estrutura

optimizer = torch.optim.AdamW(model.parameters(), lr=learning_rate)  # inicializa o algoritmo de otimizacao

for iter in range(max_iters):  # inicia o treinamento

    if iter % eval_interval == 0:  # verifica se chegou o momento de avaliar
        losses = estimate_loss()  # calcula as médias das perdas atuais
        print(
            f"step {iter}: train loss {losses['train']:.4f}, val loss {losses['val']:.4f}")  # exibe na tela o andamento das perdas do treino

    xb, yb = get_batch('train')  # retira um novo lote aleatório com dados

    logits, loss = model(xb, yb)  # executa a passagem dos dados para calcular
    optimizer.zero_grad(set_to_none=True)  # zera os gradientes antigos liberando espaço
    loss.backward()
    optimizer.step()

context = torch.zeros((1, 1), dtype=torch.long, device=device)  # inicializa o contexto gerador com uma matriz
print(decode(m.generate(context, max_new_tokens=500)[0].tolist()))  # gera 500 novos caracteres numericos