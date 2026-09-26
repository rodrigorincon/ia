import collections
import random
from typing import Dict
import numpy as np
import pygame # precisa instalar essa lib para permitir ver o jogo sendo jogado

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

# Ambiente em qua a IA vai agir
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

		# Perigos relativos (1 se houver colisão, 0 caso contrário)
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


# modelo da IA. É aonde toda a IA está encapsulada
class QLearningAgent:
	table: Dict
	alpha: float
	gamma: float
	epsilon: float
	epsilon_decay: float
	min_epsilon: float
	n_acoes: int

	def __init__(self, alpha=0.1, gamma=0.9, epsilon=1.0, epsilon_decay=0.995, min_eps=0.01):
		self.table = {}  # Tabela Q implementada como Dicionário. Cria uma linha nova (chave no caso) para cada novo estado descoberto. Cada estado é uma célula do jogo
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.epsilon_decay = epsilon_decay
		self.min_epsilon = min_eps
		self.n_acoes = 3  # 0: Frente, 1: Direita, 2: Esquerda

	# pega todos os valores da tabela para um certo estado (linha)
	def _get_table_values(self, estado):
		if estado not in self.table:
			self.table[estado] = np.zeros(self.n_acoes) # cria uma nova linha (chave) ao descobrir um novo estado. Cada estado é uma célula do jogo
		return self.table[estado]

	# Algoritmo para decidir entre Eploração e Explotação (Epsilon-Greedy)
	def choose_action(self, estado):
		if random.random() < self.epsilon:
			return random.randint(0, self.n_acoes - 1) # 
		q_linha = self._get_table_values(estado)
		return np.argmax(q_linha)

	def learn(self, estado, acao, recompensa, proximo_estado, done):
		q_atual = self._get_table_values(estado)[acao]
		q_proximo_max = (0 if done else np.max(self._get_table_values(proximo_estado)))

		# Equação de Atualização de Bellman
		target = recompensa + self.gamma * q_proximo_max
		self.table[estado][acao] += self.alpha * (target - q_atual)

		# a parte que só é executada ao acabar o episódio/simulação
		if done:
			self.epsilon = max(self.min_epsilon, self.epsilon * self.epsilon_decay)


# usa o pygame para mostrar visualmente o jogo sendo jogado pela IA
# não é mostrando o que aconteceu no treino, é a IA já treinada colocada num ambiente de produção
def executar_demo_visual(agente, env):
	pygame.init()
	tela = pygame.display.set_mode((LARGURA_TELA, ALTURA_TELA))
	pygame.display.set_caption('Q-Learning Snake')
	relogio = pygame.time.Clock() # para ditar o tempo entre as ações do jogo (controlar fps e a cobra ñ sair andando enquanto a ia ta pensando ainda)

	# Desativa exploração no cenário real
	agente.epsilon = 0.0

	rodando = True
	estado = env.reset()

	while rodando:
		for event in pygame.event.get(): # se eu fecho manualmente o jogo, encerra o while
			if event.type == pygame.QUIT:
				rodando = False

		# Escolha da ação aprendida pelo agente
		acao = agente.choose_action(estado)
		proximo_estado, _, done, pontuacao = env.step(acao) # ignora a recompensa pois como já está treinada não vai mais usar. Não precisa mais atualizar a tabela Q
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
agente = QLearningAgent()
episodios = 600

for _ in range(episodios):
	estado = env.reset()
	done = False

	while not done:
		acao = agente.choose_action(estado)
		proximo_estado, recompensa, done, pontuacao = env.step(acao)
		agente.learn(estado, acao, recompensa, proximo_estado, done)
		estado = proximo_estado

# Inicia a renderização interativa após o treino
executar_demo_visual(agente, env)