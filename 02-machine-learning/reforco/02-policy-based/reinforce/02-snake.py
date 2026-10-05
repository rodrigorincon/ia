import collections
import random
from typing import List
import numpy as np
import pygame # precisa instalar essa lib para permitir ver o jogo sendo jogado
import torch
import torch.nn as nn

# constantes usadas para renderizar o jogo
LARGURA_GRADE = 15  # Matriz 15x15
ALTURA_GRADE = 15
TAMANHO_BLOCO = 30  # Tamanho em pixels de cada célula
LARGURA_TELA = LARGURA_GRADE * TAMANHO_BLOCO
ALTURA_TELA = ALTURA_GRADE * TAMANHO_BLOCO

# Vetores de Direção: 0: Cima, 1: Direita, 2: Baixo, 3: Esquerda
DIRECOES = [
  np.array([0, -1]), # coordenadas estão em eixos X e Y, não em linha e coluna
  np.array([1, 0]),  # os valores indicam o quanto deve somar nos eixos ao fazer o movimento
  np.array([0, 1]),
  np.array([-1, 0]),
]
MAX_PASSOS_SEM_COMER = 150

# Ambiente em qua a IA vai agir. O AMBIENTE É RESPONSAVEL POR DEFINIR O VALOR DA RECOMPENSA
class SnakeGame:
	direcao_idx: int
	cabeca: np.array
	corpo: any
	pontuacao: int
	passos_sem_comida: int

	def __init__(self):
		self.reset()

	def reset(self):
		self.direcao_idx = 1  # Inicia movendo para a Direita
		self.cabeca = np.array([LARGURA_GRADE // 2, ALTURA_GRADE // 2]) # inicia no meio
		self.corpo = collections.deque([ # corpo é uma fila (deque) de coordenadas
			self.cabeca.copy(),
			self.cabeca - DIRECOES[self.direcao_idx],
			self.cabeca - 2 * DIRECOES[self.direcao_idx],
		])
		self.pontuacao = 0
		self.passos_sem_comida = 0
		self._gerar_comida()
		return self.get_state()

	def _gerar_comida(self):
		# cria um loop infinito até criar numa casa livre (sem corpo)
		while True:
			self.comida = np.array([
				random.randint(0, LARGURA_GRADE - 1),
				random.randint(0, ALTURA_GRADE - 1),
			])
			# Garante que a comida não apareça dentro do corpo
			if not any(np.array_equal(self.comida, p) for p in self.corpo):
				break

	def is_colisao(self, ponto):
		x, y = ponto
		# Colisão com as paredes
		if x < 0 or x >= LARGURA_GRADE or y < 0 or y >= ALTURA_GRADE:
			return True
		# Colisão com o próprio corpo
		if any(np.array_equal(ponto, p) for p in list(self.corpo)[:-1]):
			return True
		return False

	# Retorna uma tupla representando o estado do agente (para onde está virado, casas adjacentes bloqueads e direção da comida)
	def get_state(self):
		# direcoes são as tuplas com os valores a serem somados as posições atuais
		# as direções são relativas a direção que a cobra ta virada. Não necessairamente dir_direita é a direita da tela, mas sim a direita da cobra
		dir_atual = DIRECOES[self.direcao_idx]
		dir_direita = DIRECOES[(self.direcao_idx + 1) % 4]
		dir_esquerda = DIRECOES[(self.direcao_idx - 1) % 4]

		# pega os 3 pontos ao redor da cabeça da cobra (pra onde pode ir). Só pega 3 pontos pq um dos pontos é o corpo e ñ pode ir para lá
		# os pontos são relativos a direção que a cobra ta virada. Se a cobra virar a direita vai pro ponto_direita, ñ necessariamente pra casa a direita na tela
		ponto_frente = self.cabeca + dir_atual
		ponto_direita = self.cabeca + dir_direita
		ponto_esquerda = self.cabeca + dir_esquerda

		# Vizinhos relativos (1 se houver colisão, 0 caso contrário)
		perigo_frente = 1 if self.is_colisao(ponto_frente) else 0
		perigo_direita = 1 if self.is_colisao(ponto_direita) else 0
		perigo_esquerda = 1 if self.is_colisao(ponto_esquerda) else 0

		# Posição relativa da comida
		comida_esquerda = 1 if self.comida[0] < self.cabeca[0] else 0
		comida_direita = 1 if self.comida[0] > self.cabeca[0] else 0
		comida_cima = 1 if self.comida[1] < self.cabeca[1] else 0
		comida_baixo = 1 if self.comida[1] > self.cabeca[1] else 0

		return (
			perigo_frente,
			perigo_direita,
			perigo_esquerda,
			self.direcao_idx,
			comida_esquerda,
			comida_direita,
			comida_cima,
			comida_baixo,
		)

	# Ações Relativas: 0 = Manter em frente, 1 = Virar à Direita, 2 = Virar à Esquerda
	# novamente, a ação é relativa a cabeça da cobra, não a posição na tela
	def step(self, acao_relativa):
		self.passos_sem_comida += 1

		# Atualiza a direção com base na ação
		if acao_relativa == 1:
			self.direcao_idx = (self.direcao_idx + 1) % 4
		elif acao_relativa == 2:
			self.direcao_idx = (self.direcao_idx - 1) % 4

		# Move a cabeça
		nova_cabeca = self.cabeca + DIRECOES[self.direcao_idx]

		# Verifica morte / colisão ou tempo limite (loop infinito)
		if self.is_colisao(nova_cabeca) or self.passos_sem_comida > MAX_PASSOS_SEM_COMER:
			return self.get_state(), -10.0, True, self.pontuacao

		self.cabeca = nova_cabeca
		self.corpo.appendleft(self.cabeca.copy()) # ao inves de atualizar todas as casas do corpo, adiciona uma nova onde ele chegou agora e depois remove a ultima

		# Verifica se comeu a comida
		if np.array_equal(self.cabeca, self.comida):
			self.pontuacao += 1
			self.passos_sem_comida = 0
			self._gerar_comida()
			recompensa = 10.0
		else:
			self.corpo.pop() # move a cobra (só remove a ultima ponta caso ñ tenha comido a comida pq ai cresceu)
			recompensa = -0.1  # Pequena penalidade para incentivar caminho curto

		return self.get_state(), recompensa, False, self.pontuacao


# A POLÍTICA P_θ(a|s): rede neural que recebe o estado e devolve a probabilidade de cada uma das 3 ações
class PoliticaRede(nn.Module):
	def __init__(self, n_entradas, n_acoes, n_neuronios=64):
		super().__init__()
		self.rede = nn.Sequential(
			nn.Linear(n_entradas, n_neuronios),
			nn.ReLU(),
			nn.Linear(n_neuronios, n_acoes),
			nn.Softmax(dim=-1), # transforma a saída em probabilidades (soma = 1)
		)

	def forward(self, x):
		return self.rede(x)


# modelo da IA. É aonde toda a IA está encapsulada
# No lugar da tabela Q (dicionário) temos uma rede neural. A tabela precisava ver cada estado para saber o que fazer nele,
# a rede generaliza: estados parecidos (ex: mesmo perigo, comida num lado parecido) geram probabilidades parecidas
class ReinforceAgent:
	politica: PoliticaRede
	otimizador: torch.optim.Optimizer
	gamma: float
	n_acoes: int
	log_probs: List[torch.Tensor]
	recompensas: List[float]

	def __init__(self, alpha=0.003, gamma=0.99):
		self.gamma = gamma
		self.n_acoes = 3  # 0: Frente, 1: Direita, 2: Esquerda
		# 11 entradas: 3 vizinhos + 4 da direção (one-hot) + 4 da posição da comida
		self.politica = PoliticaRede(11, self.n_acoes)
		self.otimizador = torch.optim.Adam(self.politica.parameters(), lr=alpha)
		# memória do episódio atual. O REINFORCE só aprende quando o episódio acaba (Monte Carlo)
		self.log_probs = []
		self.recompensas = []

	# transforma a tupla do estado num tensor para a rede
	# A direção (0 a 3) vira one-hot: a direção 3 (esquerda) não é "maior" que a 1 (direita), são só categorias diferentes
	def posix_to_one_hot(self, estado):
		vizinhos = list(estado[:3])
		direcao = [0, 0, 0, 0]
		direcao[estado[3]] = 1
		comida = list(estado[4:])
		return torch.tensor(vizinhos + direcao + comida, dtype=torch.float32)

	# Não há Epsilon-Greedy: a exploração vem do sorteio da ação a partir das probabilidades da rede
	# deterministico=True escolhe sempre a ação mais provável (usado depois de treinado)
	def choose_action(self, estado, deterministico=False):
		probs = self.politica(self.posix_to_one_hot(estado))
		if deterministico:
			return torch.argmax(probs).item()
		distribuicao = torch.distributions.Categorical(probs)
		acao = distribuicao.sample()
		self.log_probs.append(distribuicao.log_prob(acao)) # guarda log P_θ(a|s) para o gradiente no fim do episódio
		return acao.item()

	# só guarda a recompensa. No Q-Learning aprendiamos a cada passo, aqui esperamos o episódio terminar
	def store_reward(self, recompensa):
		self.recompensas.append(recompensa)

	# chamado ao fim do episódio: calcula os retornos e atualiza os pesos da rede
	def learn(self):
		# Retorno G_t de cada passo, de trás pra frente: G_t = R_{t+1} + γ*G_{t+1}
		retornos = []
		G = 0.0
		for r in reversed(self.recompensas):
			G = r + self.gamma * G
			retornos.insert(0, G)
		retornos = torch.tensor(retornos)

		# Normalização dos retornos (média 0 e desvio padrão 1). Truque muito usado para diminuir a ALTA VARIÂNCIA do REINFORCE.
		# Um episódio que comeu 5 comidas tem retornos bem maiores que um que comeu 1, e isso faria as atualizações terem tamanhos muito diferentes.
		# Normalizando, dentro de cada episódio as ações acima da média ganham probabilidade e as abaixo perdem,
		# independente da escala da recompensa. Funciona como um "baseline" simples
		if len(retornos) > 1:
			retornos = (retornos - retornos.mean()) / (retornos.std() + 1e-8)

		# L = - sum(log P_θ(a_t|s_t) * G_t). Sinal de menos pois o PyTorch minimiza e queremos subida de gradiente
		loss = -(torch.stack(self.log_probs) * retornos).sum()
		self.otimizador.zero_grad()
		loss.backward()
		self.otimizador.step()

		# limpa a memória para o próximo episódio (on-policy: dados antigos foram gerados por uma política que não existe mais)
		self.log_probs = []
		self.recompensas = []


# usa o pygame para mostrar visualmente o jogo sendo jogado pela IA
# não é mostrando o que aconteceu no treino, é a IA já treinada colocada num ambiente de produção
def executar_demo_visual(agente, env):
	pygame.init()
	tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
	pygame.display.set_caption('REINFORCE Snake')
	relogio = pygame.time.Clock() # para ditar o tempo entre as ações do jogo (controlar fps e a cobra ñ sair andando enquanto a ia ta pensando ainda)

	rodando = True
	estado = env.reset()

	while rodando:
		for event in pygame.event.get(): # se eu fecho manualmente o jogo, encerra o while
			if event.type == pygame.QUIT:
				rodando = False

		# Escolha da ação aprendida pelo agente. Desativa a exploração (sempre a ação mais provável)
		# no_grad pois não vamos mais treinar, não precisa guardar o grafo para gradiente
		with torch.no_grad():
			acao = agente.choose_action(estado, deterministico=True)
		proximo_estado, _, done, pontuacao = env.step(acao) # ignora a recompensa pois como já está treinada não vai mais usar
		estado = proximo_estado

		if done:
			estado = env.reset() # se acabar começa um jogo novo até que se feche o programa

		### Renderização da tela ---------------------------
		# Fundo Cinza Escuro
		tela.fill((30, 30, 30))
		# Desenha a Comida (Vermelho)
		x_c, y_c = env.comida * TAMANHO_BLOCO
		pygame.draw.rect(tela, (230, 50, 50), (x_c, y_c, TAMANHO_BLOCO, TAMANHO_BLOCO))
		# Desenha o Corpo da Cobra (Verde)
		for i, pt in enumerate(env.corpo):
			x, y = pt * TAMANHO_BLOCO
			cor = (0, 255, 120) if i == 0 else (0, 180, 80)  # Cabeça mais clara
			pygame.draw.rect(tela, cor, (x + 1, y + 1, TAMANHO_BLOCO - 2, TAMANHO_BLOCO - 2))
		# Placar na Tela
		fonte = pygame.font.SysFont('arial', 20, bold=True)
		texto = fonte.render(f'Pontuação: {pontuacao}', True, (255, 255, 255))
		tela.blit(texto, (10, 10))

		pygame.display.flip()
		relogio.tick(12)  # Controle de velocidade (12 FPS)

	pygame.quit()
	print('Jogo fechado')


# criação do ambiente (jogo) e do agente como objetos separados
env = SnakeGame()
agente = ReinforceAgent()
# REINFORCE costuma precisar de mais episódios que o Q-Learning: só aprende 1 vez por episódio e o gradiente é ruidoso
episodios = 1_500

max_passos = 10_000
for ep in range(episodios):
	estado = env.reset()
	done = False
	passos = 0

	while not done and passos < max_passos:
		acao = agente.choose_action(estado)
		proximo_estado, recompensa, done, pontuacao = env.step(acao)
		agente.store_reward(recompensa)
		estado = proximo_estado
		passos += 1

	# fim do episódio: agora o agente aprende com tudo o que aconteceu
	agente.learn()
	if ep % 100 == 0: print(f'Episódio {ep} - Pontuação: {pontuacao}')

# TERMINOU O TREINO
# Inicia a renderização interativa após o treino
executar_demo_visual(agente, env)
