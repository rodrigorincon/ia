import random
from typing import Dict, List, Tuple
from matplotlib import pyplot as plt
import numpy as np

# cria variável que representa o labirinto
Labirinto = np.ndarray[List[int]]
Point = Tuple[int, int]

# FUNÇÃO PARA CRIAR AS MATRIZES DOS LABIRINTOS (0 LIVRE, 1 PAREDE)
# RETORNA A MATRIZ, O PONTO INICIAL E O FINAL
def criar_labirinto(id: int) -> Tuple[Labirinto, Point, Point]:
	# Labirinto de Treino 1
	if id == 1:
		grid = np.array([
			[0, 0, 0, 0, 0, 0, 0], 
			[0, 1, 1, 1, 0, 1, 0], 
			[0, 1, 0, 1, 0, 1, 0], 
			[0, 1, 0, 0, 0, 1, 0], 
			[0, 1, 1, 1, 0, 0, 0], 
			[0, 0, 0, 1, 1, 1, 0], 
			[0, 1, 0, 0, 0, 0, 0],
		])
		start, goal = (0, 0), (6, 6)

	# Labirinto de Treino 2
	elif id == 2:
		grid = np.array([
			[0, 0, 0, 0, 0, 0, 0, 0, 0], 
			[0, 1, 1, 1, 1, 1, 0, 1, 0], 
			[0, 1, 0, 0, 0, 1, 0, 1, 0], 
			[0, 1, 0, 1, 0, 1, 0, 1, 0], 
			[0, 1, 0, 1, 0, 0, 0, 0, 0], 
			[0, 0, 0, 1, 1, 1, 1, 1, 0], 
			[0, 1, 0, 0, 0, 0, 0, 1, 0], 
			[0, 1, 1, 1, 1, 1, 0, 1, 0], 
			[0, 0, 0, 0, 0, 0, 0, 0, 0],
		])
		start, goal = (0, 1), (8, 7)

	# Labirinto de Treino 3
	elif id == 3:
		grid = np.array([
			[0, 1, 0, 0, 0, 1, 0, 0], 
			[0, 1, 0, 1, 0, 1, 1, 0], 
			[0, 0, 0, 1, 0, 0, 0, 0], 
			[1, 1, 0, 1, 1, 1, 0, 1], 
			[0, 0, 0, 0, 0, 0, 0, 0],
		])
		start, goal = (0, 0), (4, 7)

	# Labirinto de Teste 4 (Inédito para o agente)
	elif id == 4:
		grid = np.array([
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
		start, goal = (10, 1), (6, 12)

	# Labirinto de Teste 4 (Inédito para o agente)
	elif id == 5:
		grid = np.array([
			[0, 0, 1, 0, 0, 0],
			[0, 1, 1, 0, 1, 0],
			[0, 0, 0, 0, 1, 0],
			[1, 1, 0, 1, 0, 0],
			[0, 0, 0, 0, 1, 0],
			[0, 1, 1, 0, 0, 0],
		])
		start, goal = (0, 0), (5, 5)

	return grid, start, goal

# Ambiente em qua a IA vai agir. O AMBIENTE É RESPONSAVEL POR DEFINIR O VALOR DA RECOMPENSA
class MazeEnv:
	labirinto: Labirinto
	rows: int
	cols: int
	start: Point
	goal: Point
	last_pos: Point
	position: List[Point]
  
	def __init__(self, labirinto, start, goal):
		self.labirinto = labirinto
		self.rows, self.cols = labirinto.shape
		self.start = start
		self.goal = goal
		self.position = list(start)

	def reset(self):
		self.position = list(self.start)
		self.last_pos = None
		return self.get_state()

	# State = casas vizinhas nessa ordem: (Cima, Baixo, Esquerda, Direita), direção da saída (se está na linha/coluna atual, anterior ou afrente) e ultima_posicao
  # funcionamento não é totalmente cego. Sabe pra que lado está a saída
	def get_state(self):
		row, col = self.position
		goal_row, goal_col = self.goal

		# Paredes ou limites do mapa nas casas vizinhas (1 = Parede, 0 = Livre)
		wall_up = 1 if (row - 1 < 0 or self.labirinto[row - 1, col] == 1) else 0
		wall_down = 1 if (row + 1 >= self.rows or self.labirinto[row + 1, col] == 1) else 0
		wall_left = 1 if (col - 1 < 0 or self.labirinto[row, col - 1] == 1) else 0
		wall_right = (1 if (col + 1 >= self.cols or self.labirinto[row, col + 1] == 1) else 0)

		# Direção da saída relativa à posição atual (-1, 0 ou 1)
		dir_row = 1 if goal_row > row else (-1 if goal_row < row else 0)
		dir_col = 1 if goal_col > col else (-1 if goal_col < col else 0)

		last_p = tuple(self.last_pos) if self.last_pos is not None else (-1, -1)
		return (wall_up, wall_down, wall_left, wall_right, dir_row, dir_col, last_p)

	# Ações: 0: Cima, 1: Baixo, 2: Esquerda, 3: Direita
	def step(self, action):
		acoes_possiveis = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		desloc_row, desloc_col = acoes_possiveis[action]

		new_row, new_col = self.position[0] + desloc_row, self.position[1] + desloc_col
		done = False
		reward = 0

		# Tentativa de colisão com parede ou saída do mapa
		if not (0 <= new_row < self.rows and 0 <= new_col < self.cols) or self.labirinto[new_row, new_col] == 1:
			reward = -5.0
		else:
			reward += self.voltou_pra_ultima_posicao(new_row, new_col)
			self.position = [new_row, new_col]
			if tuple(self.position) == self.goal:
				reward += 100.0  # Sucesso ao achar a saída
				done = True
			else:
				reward += -0.5 # Penalidade de movimento para buscar o menor caminho

		return self.get_state(), reward, done

	def voltou_pra_ultima_posicao(self, new_row, new_col):
		# Penalidade adicional caso tente retornar imediatamente à posição anterior
		# No Q-Learn, não devemos criar regras (ifs e código) proibindo certos movimentos. 
		# Ao invés disso permitimos mas damos penalidades para essa ação e deixamos a IA aprender a não fazer isso
		self.last_pos = list(self.position)
		if self.last_pos is not None and [new_row, new_col] == self.last_pos:
			return -100.0  # Penaliza o movimento de retorno imediato (evita ir e voltar pra mesma casa)
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
		# Os primeiros 4 elementos do estado indicam paredes: 0 = Livre, 1 = Parede
		wall_up, wall_down, wall_left, wall_right = state[:4]
		paredes = [wall_up, wall_down, wall_left, wall_right]
		# Filtra apenas os índices das ações que NÃO levam a uma parede (valor 0)
		acoes_validas = [i for i in range(self.n_actions) if paredes[i] == 0]
		# Caso de emergência: se não houver ações válidas (ex: encurralado), permite todas
		if not acoes_validas:
			acoes_validas = list(range(self.n_actions))

		# Exploração: escolhe aleatoriamente entre as ações válidas
		if random.random() < self.epsilon:
			return random.choice(acoes_validas)

		# Explotação: busca a ação de maior pontuação Q apenas dentre as ações válidas
		q_values = self._get_table_values(state)
		melhor_acao = max(acoes_validas, key=lambda idx: q_values[idx])
		return melhor_acao

	def learn(self, state, action, reward, next_state, done):
		q_current = self._get_table_values(state)[action]
		q_next = 0 if done else np.max(self._get_table_values(next_state))

		target = reward + self.gamma * q_next
		self.table[state][action] += self.alpha * (target - q_current)

		# a parte que só é executada ao acabar o episódio/simulação
		if done and self.epsilon > self.min_epsilon:
			self.epsilon *= self.epsilon_decay


# TREINAMENTO INTERCALADO NOS 3 PRIMEIROS LABIRINTOS
ambientes_treino = [
	MazeEnv(*criar_labirinto(1)),
	MazeEnv(*criar_labirinto(2)),
	MazeEnv(*criar_labirinto(3)),
]

agent = QLearningMazeAgent()
episodes = 6_000
max_steps = 150

recompensas_por_episodio = []
passos_por_episodio = []
for ep in range(episodes):
	# Intercala os labirintos para o agente aprender regras gerais e evitar memorizar um mapa específico
	env = ambientes_treino[ep % 3]
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

##### TESTE E VALIDAÇÃO NO 4º LABIRINTO (INÉDITO) ----------------------------
grid_teste, start_teste, goal_teste = criar_labirinto(5)
env_teste = MazeEnv(grid_teste, start_teste, goal_teste)

agent.epsilon = 0.0  # Desativa exploração para o teste
state = env_teste.reset()
done = False

trajetoria = [list(env_teste.position)]
print('--- SIMULAÇÃO NO 4º LABIRINTO (NUNCA VISTO PELO ROBÔ) ---')
step_idx = 0
while not done and step_idx < max_steps:
	action = agent.choose_action(state)
	next_state, reward, done = env_teste.step(action)
	trajetoria.append(list(env_teste.position))
	step_idx += 1
	state = next_state

	# imprime o mapa mostrando cada passo
	env_teste.print_labirinto()
	print('------------------------\n')

print('\n======================== MAPA FINAL DO LABIRINTO ========================')
print('          MAPA FINAL DO TESTE (LABIRINTO 4)        ')
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