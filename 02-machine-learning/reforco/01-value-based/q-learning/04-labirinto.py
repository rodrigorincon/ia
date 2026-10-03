import random
from typing import Dict, List, Tuple
from matplotlib import pyplot as plt
import numpy as np

# cria variável que representa o labirinto
Labirinto = np.ndarray[List[int]]
Point = Tuple[int, int]

# GERA UM LABIRINTO ALEATÓRIO (0 LIVRE, 1 PAREDE) COM (2*altura) x (2*largura) CASAS
# Uma tabela Q só sabe agir em estados que já viu no treino. Com um punhado de labirintos de treino ele vai ter contato com pouquíssimas 
# combinações (vizinhos + direção da saída). Num labirinto novo a IA cai nesses estados com Q zerado e age às cegas. 
# Aumentar a quantidade de labirintos de treino cobre o máximo de casos.
# prob atalho define a quantidade de ciclos terão no labirinto
def gerar_labirinto_aleatorio(altura: int, largura: int, prob_atalho: float = 0.15) -> Tuple[Labirinto, Point, Point]:
	rows = 2 * altura
	cols = 2 * largura
	# começa com o labirinto todo feito de parede e vai abrindo corredores nele
	labirinto = np.ones((rows, cols), dtype=int)

	# Busca em profundidade (DFS) "cavando" corredores entre casas de índice par
	pilha = [(0, 0)]
	labirinto[0, 0] = 0
	while pilha:
		row, col = pilha[-1]
		# ve quais direções dá pra expandir um caminho (expande de 2 em 2 casas). Para expandir o caminho tem de ser parede ainda
		# para não ficar perdendo tempo expandindo um caminho ja aberto
		for desloc_row, desloc_col in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
			if(0 <= row + desloc_row < rows and 0 <= col + desloc_col < cols and labirinto[row + desloc_row, col + desloc_col] == 1):
				vizinhos = [(row + desloc_row, col + desloc_col, desloc_row // 2, desloc_col // 2)]
		if not vizinhos:
			pilha.pop()
			continue
		# escolhe só 1 dos caminhos encontrado e abre caminho nessas casas
		n_row, n_col, meio_r, meio_c = random.choice(vizinhos)
		labirinto[row + meio_r, col + meio_c] = 0
		labirinto[n_row, n_col] = 0
		pilha.append((n_row, n_col))

	# A DFS gera um labirinto sem ciclos. Derrubamos algumas paredes extras para criar ciclos
	for row in range(rows):
		for col in range(cols):
			if labirinto[row, col] == 1 and (row % 2 != col % 2) and random.random() < prob_atalho:
				labirinto[row, col] = 0

	# define as casas iniciais e finais
	livres = [tuple(p) for p in np.argwhere(labirinto == 0)]
	start, goal = random.sample(livres, 2)
	return labirinto, (int(start[0]), int(start[1])), (int(goal[0]), int(goal[1]))

# Ambiente em qua a IA vai agir. O AMBIENTE É RESPONSAVEL POR DEFINIR O VALOR DA RECOMPENSA
class MazeEnv:
	labirinto: Labirinto
	rows: int
	cols: int
	start: Point
	goal: Point
	position: List[Point]
	visitas: np.ndarray

	def __init__(self, labirinto, start, goal):
		self.labirinto = labirinto
		self.rows, self.cols = labirinto.shape
		self.start = start
		self.goal = goal
		self.position = list(start)

	def reset(self):
		self.position = list(self.start)
		# Memória de quantas vezes o agente pisou em cada casa neste episódio
		self.visitas = np.zeros(self.labirinto.shape, dtype=int)
		self.visitas[self.start] = 1
		return self.get_state()

	def _eh_parede(self, row, col):
		casa_valida = 0 <= row < self.rows and 0 <= col < self.cols
		return not casa_valida or self.labirinto[row, col] == 1

	# Codifica cada casa vizinha (Cima, Baixo, Esquerda, Direita):
	#   0 = parede/fora do mapa
	#   1 = livre e nunca visitada
	#   2 = já visitada, mas é a MENOS visitada entre as vizinhas livres
	#   3 = já visitada e existe outra vizinha menos visitada
	# Por que comparar com as vizinhas e não usar o nº de visitas direto? Um contador precisaria de um limite (senão os estados explodem) 
	# e depois que todas as vizinhas batem nesse limite, ficam todas iguais e o agente volta a andar em círculos. 
	# A comparação relativa nunca satura: sempre aponta a saída menos explorada.
	def _codigos_vizinhos(self):
		row, col = self.position
		vizinhos = [(row - 1, col), (row + 1, col), (row, col - 1), (row, col + 1)]
		livres = [v for v in vizinhos if not self._eh_parede(*v)]
		menor_visita = min((self.visitas[v] for v in livres), default=0)

		codigos = []
		for v in vizinhos:
			if self._eh_parede(*v):
				codigos.append(0)
			elif self.visitas[v] == 0:
				codigos.append(1)
			elif self.visitas[v] == menor_visita:
				codigos.append(2)
			else:
				codigos.append(3)
		return codigos

	# State = casas vizinhas nessa ordem: (Cima, Baixo, Esquerda, Direita) + direção da saída (-1, 0 ou 1 em linha e coluna)
	# Funcionamento não é totalmente cego: sabe pra que lado está a saída e lembra por onde já passou.
	# IMPORTANTE: o estado só usa informação RELATIVA ao agente (estado não pode ser coordenadas absolutas). 
	# Assim o que ele aprende nos labirintos de treino continua valendo num labirinto nunca visto. Usar a posição absoluta
	# faz todo estado do labirinto novo ser inédito, com Q zerado.
	def get_state(self):
		row, col = self.position
		goal_row, goal_col = self.goal

		cima, baixo, esquerda, direita = self._codigos_vizinhos()

		# Direção da saída relativa à posição atual (-1, 0 ou 1)
		dir_row = 1 if goal_row > row else (-1 if goal_row < row else 0)
		dir_col = 1 if goal_col > col else (-1 if goal_col < col else 0)

		# Quantas vezes já pisou na casa atual (1, 2 ou 3+). Se o agente estiver preso num ciclo esse número cresce e o estado muda, 
		# dando chance de ele agir diferente e sair do ciclo
		visitas_aqui = min(self.visitas[row, col], 3)

		return (cima, baixo, esquerda, direita, dir_row, dir_col, visitas_aqui)

	# Ações: 0: Cima, 1: Baixo, 2: Esquerda, 3: Direita
	def step(self, action):
		acoes_possiveis = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		desloc_row, desloc_col = acoes_possiveis[action]

		new_row, new_col = self.position[0] + desloc_row, self.position[1] + desloc_col
		done = False
		reward = 0
		codigo_destino = self._codigos_vizinhos()[action]  # calculado ANTES de mover

		# Tentativa de colisão com parede ou saída do mapa
		if self._eh_parede(new_row, new_col):
			reward = -5.0
		else:
			reward += self.penalidade_revisita(codigo_destino)
			self.position = [new_row, new_col]
			self.visitas[new_row, new_col] += 1
			if tuple(self.position) == self.goal:
				reward += 100.0  # Sucesso ao achar a saída
				done = True
			else:
				reward += -0.5 # Penalidade de movimento para buscar o menor caminho

		return self.get_state(), reward, done

	# No Q-Learn, não devemos criar regras (ifs e código) proibindo certos movimentos.
	# Ao invés disso permitimos mas damos penalidades para essa ação e deixamos a IA aprender a não fazer isso.
	# Para penalizar fiar andando em circulos (qualquer tamanho de círculo, seja ir e voltar pras mesmas casas seja um criculo maior)
	# penalizamos pisar em qualquer casa já visitada. A penalidade é moderada quando, dentre todas as opções, é a opção menos visitada, 
	# porque às vezes voltar é necessário (sair de um beco sem saída), e maior quando havia uma opção menos explorada disponível.
	# Se nunca foi para aquela casa a penalidade é 0
	def penalidade_revisita(self, codigo_destino):
		if codigo_destino == 2:
			return -2.0
		if codigo_destino == 3:
			return -20.0
		return 0

	def print_labirinto(self):
		matriz_imprimir = []
		for row in range(self.rows):
			filled_row = ['#' if self.labirinto[row][col] == 1 else '.' for col in range(self.cols)]
			matriz_imprimir.append(filled_row)

		# marca os pontos de inicio e fim
		matriz_imprimir[self.start[0]][self.start[1]] = 'S'
		matriz_imprimir[self.goal[0]][self.goal[1]] = 'G'
		
		# marca aonde a IA está
		matriz_imprimir[self.position[0]][self.position[1]] = '*'
		# Imprime o labirinto
		for row in matriz_imprimir:
			print(' '.join(row))

# modelo da IA. É aqui que ao algoritmo é executado
class QLearningMazeAgent:
	table: Dict
	alpha: float
	gamma: float
	epsilon: float
	epsilon_decay: float
	min_epsilon: float
	n_actions: int

	def __init__(self, alpha=0.1, gamma=0.95, epsilon=1.0, epsilon_decay=0.999, min_epsilon=0.01):
		self.table = {}
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.epsilon_decay = epsilon_decay
		self.min_epsilon = min_epsilon
		self.n_actions = 4

	# pega todos os valores da tabela para um certo estado (linha)
	def _get_table_values(self, state):
		if state not in self.table:
			self.table[state] = np.zeros(self.n_actions) # cria uma nova linha (chave) ao descobrir um novo estado. Cada estado é uma  combnação de célula do jogo, perigos na casa imediatamente a volta e direção da comida
		return self.table[state]

	# Algoritmo para decidir entre Exploração e Explotação (Epsilon-Greedy) filtrando apenas ações válidas
	def choose_action(self, state):
		# Os primeiros 4 elementos do estado descrevem os vizinhos: 0 = Parede, 1..3 = Livre (com nº de visitas)
		vizinhos = state[:4]
		# Filtra apenas os índices das ações que NÃO levam a uma parede
		acoes_validas = [i for i in range(self.n_actions) if vizinhos[i] != 0]
		# Caso de emergência: se não houver ações válidas (ex: encurralado), permite todas
		if not acoes_validas:
			acoes_validas = list(range(self.n_actions))

		# Exploração: escolhe aleatoriamente entre as ações válidas
		if random.random() < self.epsilon:
			return random.choice(acoes_validas)

		# Explotação: busca a ação de maior pontuação Q apenas dentre as ações válidas
		# Em caso de empate sorteia entre as melhores: com max() puro o desempate seria sempre a primeira
		# ação da lista, o que num estado nunca visto (Q zerado) vira um comportamento repetitivo
		q_values = self._get_table_values(state)
		melhor_q = max(q_values[idx] for idx in acoes_validas)
		melhores_acoes = [idx for idx in acoes_validas if q_values[idx] == melhor_q] # pega todas as ações empatadas como melhores
		return random.choice(melhores_acoes)

	def learn(self, state, action, reward, next_state, done):
		q_current = self._get_table_values(state)[action]
		q_next = 0 if done else np.max(self._get_table_values(next_state))

		target = reward + self.gamma * q_next
		self.table[state][action] += self.alpha * (target - q_current)

		# a parte que só é executada ao acabar o episódio/simulação
		if done and self.epsilon > self.min_epsilon:
			self.epsilon *= self.epsilon_decay


agent = QLearningMazeAgent()
episodes = 1_000
max_steps = 300

recompensas_por_episodio = []
passos_por_episodio = []
for ep in range(episodes):
	# A cada periodo usa um labirinto novo para o agente aprender regras gerais e evitar memorizar um mapa específico.
	env = MazeEnv(*gerar_labirinto_aleatorio(random.randint(5, 8), random.randint(5, 8)))
	state = env.reset()
	done = False
	step_count = 0
	total_reward = 0

	while not done and step_count < max_steps:
		action = agent.choose_action(state)
		next_state, reward, done = env.step(action)
		agent.learn(state, action, reward, next_state, done)
		state = next_state
		step_count += 1
		total_reward += reward

	recompensas_por_episodio.append(total_reward)
	passos_por_episodio.append(step_count)

##### TESTE E VALIDAÇÃO EM UM LABIRINTO INÉDITO ----------------------------
grid_teste = np.array([
	[0,0,0,0, 0,0,0,0,0, 0,1, 0,0,0, 0,0,0],
	[0,1,1,0, 1,1,1,1,1, 0,1, 0,1,1, 1,1,0],
	[0,1,1,0, 1,0,0,0,1, 0,1, 0,0,0, 1,1,0],
	[0,1,1,0, 1,0,1,0,1, 0,1, 1,1,1, 1,1,0],
	[0,0,1,0, 1,0,1,0,0, 0,0, 0,0,0, 0,0,0],
	[0,1,1,0, 1,1,1,1,1, 0,1, 1,1,1, 0,1,0],
	[0,1,1,0, 0,0,0,0,0, 0,1, 0,0,1, 0,1,0],
	[0,1,1,0, 1,1,1,1,1, 0,1, 0,1,1, 0,1,0],
	[0,1,1,0, 0,0,1,1,1, 0,1, 0,0,0, 0,1,1],
	[0,1,1,0, 1,1,1,1,1, 0,1, 1,1,1, 0,1,1],
	[0,0,0,0, 0,0,0,0,0, 0,1, 1,1,1, 0,1,1],
	[1,1,1,1, 1,1,1,1,1, 1,1, 1,1,1, 0,1,1],
	[0,0,0,0, 0,0,0,0,0, 0,0, 0,0,0, 0,1,1],
	[0,1,1,1, 1,1,1,1,1, 1,0, 1,1,1, 1,1,1],
	[0,1,1,1, 1,1,0,1,1, 1,0, 1,1,1, 1,1,1],
	[0,1,1,1, 0,1,0,1,1, 1,0, 1,1,1, 1,1,1],
	[0,1,1,1, 0,1,0,0,0, 0,0, 1,1,1, 1,1,1],
	[0,1,1,1, 0,1,1,1,1, 1,0, 1,1,1, 1,1,1],
	[0,0,0,0, 0,0,0,0,0, 0,0, 1,1,1, 1,1,1],
])
start_teste, goal_teste = (10, 1), (6, 12)
env_teste = MazeEnv(grid_teste, start_teste, goal_teste)

agent.epsilon = 0.0  # Desativa exploração para o teste
state = env_teste.reset()
done = False

trajetoria = [list(env_teste.position)]
print('--- SIMULAÇÃO NO LABIRINTO NOVO ---')
step_idx = 0
# Num labirinto novo o agente não conhece o caminho: ele precisa explorar (e às vezes voltar de becos),
# então damos um limite de passos maior que no treino, proporcional ao tamanho do labirinto
max_steps_teste = 2 * grid_teste.size
while not done and step_idx < max_steps_teste:
	action = agent.choose_action(state)
	next_state, reward, done = env_teste.step(action)
	trajetoria.append(list(env_teste.position))
	step_idx += 1
	state = next_state

	# imprime o mapa mostrando cada passo
	env_teste.print_labirinto()
	print('------------------------\n')

print('\n======================== MAPA FINAL DO LABIRINTO ========================')
print(f'Saída Encontrada: {"SIM" if done else "NÃO"}')
print(f'Total de Passos Necessários: {step_idx}')

# VISUALIZAÇÃO: CURVA DE APRENDIZADO
# Tira a média móvel de 30 episódios para mostrar uma curva mais suave com a tendência
media_movel = np.convolve(recompensas_por_episodio, np.ones(30) / 30, mode='valid')
plt.figure(figsize=(9, 5))
plt.plot(recompensas_por_episodio, alpha=0.3, color='gray', label='Episódio')
plt.plot(media_movel, color='blue', linewidth=2, label='Média Móvel (30 ep)')
plt.title('Evolução do Aprendizado — Q-Learning')
plt.xlabel('Episódio')
plt.ylabel('Recompensa Total')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# VISUALIZAÇÃO: Número de Passos em cada episódio
media_movel_passos = np.convolve(passos_por_episodio, np.ones(30) / 30, mode='valid')
plt.figure(figsize=(9, 5))
plt.plot(passos_por_episodio, alpha=0.3, color='gray', label='Episódio')
plt.plot(media_movel_passos, color='blue', linewidth=2, label='Média Móvel (30 ep)')
plt.title('Evolução da quantidade de passos — Q-Learning')
plt.xlabel('Episódio')
plt.ylabel('Num Passos')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()