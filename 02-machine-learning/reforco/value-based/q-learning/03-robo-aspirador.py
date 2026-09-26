import random
from typing import Dict, List, Tuple
from matplotlib import pyplot as plt
import numpy as np

# cria novo tipo de variavel para uma posicao no labirinto
Point = Tuple[int, int]

# Ambiente em qua a IA vai agir. O AMBIENTE É RESPONSAVEL POR DEFINIR O VALOR DA RECOMPENSA
class RoboAspiradorEnv:
	size: int
	max_battery: int
	base: Point
	initial_obstacles: List[Point]
	robot_pos: List[Point]
	battery: int
	step_count: int
	dirt_map: np.ndarray
	obstacles: List[List[Point]]

	def __init__(self, size=6, max_battery=20):
		self.size = size
		self.max_battery = max_battery
		self.base = (0, 0)  # Estação de Recarga / Base

		# Obstáculos dinâmicos iniciais (móveis/pessoas/pets)
		self.initial_obstacles = [(2, 2), (4, 3)]
		self.reset()

	def reset(self):
		self.robot_pos = list(self.base)
		self.battery = self.max_battery
		self.step_count = 0

		# Mapa de Sujeira: 1 = Sujo (precisa limpar), 0 = Limpo. começa com tudo sujo
		self.dirt_map = np.ones((self.size, self.size), dtype=int)
		self.dirt_map[self.base] = 0  # A base começa limpa

		# Posições dos obstáculos móveis
		self.obstacles = [list(obs) for obs in self.initial_obstacles]

		return self.get_state()

	# Move os obstáculos levemente para células adjacentes
	def move_obstacles(self):
		for i in range(len(self.obstacles)):
			row, col = self.obstacles[i]
			vizinhos_livres = []
			# testa todas as casas vizinhas e guarda no array as casas possíveis para o obstaculo ir
			for desloc_row, desloc_col in [(-1, 0), (1, 0), (0, -1), (0, 1)]:
				new_row, new_col = row + desloc_row, col + desloc_col
				# Não pode mover para fora do mapa, nem para a base, nem para cima do robô
				if 0 <= new_row < self.size and 0 <= new_col < self.size:
					if (new_row, new_col) != self.base and [new_row, new_col] != self.robot_pos:
						vizinhos_livres.append([new_row, new_col])

			# 30% de chance do obstáculo mudar de lugar. Escolhe aleatoriamente um dos vizinhos livres
			if vizinhos_livres and random.random() < 0.30:
				self.obstacles[i] = random.choice(vizinhos_livres)

	# Estado = (linha, coluna, nível bateria, se a celula que o robo tá agora está suja)
	def get_state(self):
		row, col = self.robot_pos
		is_dirty = self.dirt_map[row, col]
		return (row, col, self.battery, is_dirty)

	# Ações: Cima=0, Baixo=1, Esquerda=2, Direita=3
	# encerra se a bateria descarregar ou se voltar pra base após limpar tudo. Se limpar tudo mas a bateria acabar antes de voltar então ganha menos ponto
	def step(self, action):
		self.step_count += 1
		self.battery -= 1  # Consumo constante de bateria a cada passo

		# Movimentação leve dos obstáculos a cada 3 passos
		if self.step_count % 3 == 0:
			self.move_obstacles()

		acoes_possiveis = [(-1, 0), (1, 0), (0, -1), (0, 1)]
		desloc_row, desloc_col = acoes_possiveis[action]
		new_row, new_col = self.robot_pos[0] + desloc_row, self.robot_pos[1] + desloc_col

		reward = 0.0
		done = False

		# Colisão com paredes ou obstáculos móveis
		if not (0 <= new_row < self.size and 0 <= new_col < self.size) or [new_row, new_col] in self.obstacles:
			reward -= 10.0  # Penalidade por colisão
			# Robô permanece na mesma posição (não vai pra casa ja ocupada)
		else:
			self.robot_pos = [new_row, new_col]

		row, col = self.robot_pos

		# Limpeza da Célula
		if self.dirt_map[row, col] == 1:
			self.dirt_map[row, col] = 0
			reward += 20.0  # Alta recompensa por limpar área suja
		else:
			reward -= 0.5  # Custo de deslocamento em área já limpa

		# Retorno à Base e Gestão de Bateria
		if tuple(self.robot_pos) == self.base:
			if self.battery > 0 and self.all_clean():
				# Sucesso: Retornou à base antes de descarregar totalmente
				reward += 100.0
				done = True
			elif 0 < self.battery < self.max_battery and not self.all_clean():
				# Recarrega se estiver de passagem pela base
				self.battery = self.max_battery
				reward += 5.0

		# bateria acabou sem limpar tudo
		elif self.battery <= 0 and not done and not self.all_clean():
			# Falha crítica: Descarregou totalmente fora da base
			reward -= 100.0
			done = True
		# bateria acabou após limpar tudo mas antes de chegar na base
		elif self.battery <= 0 and done and self.all_clean():
			reward -= 30.0
			done = True

		return self.get_state(), reward, done

	def all_clean(self):
		obstacle_set = {tuple(obs) for obs in self.obstacles}
		# checa se todas as celulas são 0 ignorando as que são obstaculos
		for row in range(self.size):
			for col in range(self.size):
				if (row, col) not in obstacle_set and self.dirt_map[row, col] == 1:
					return False
		return True

# modelo da IA. É aqui que ao algoritmo é executado
class QLearningVacuumAgent:
	table: Dict
	alpha: float
	gamma: float
	epsilon: float
	epsilon_decay: float
	min_epsilon: float
	n_actions: int
	
	def __init__(self,alpha=0.1,gamma=0.95,epsilon=1.0,epsilon_decay=0.9992,min_epsilon=0.02):
		self.table = {}
		self.alpha = alpha
		self.gamma = gamma
		self.epsilon = epsilon
		self.epsilon_decay = epsilon_decay
		self.min_epsilon = min_epsilon
		self.n_actions = 4  # Cima, Baixo, Esquerda, Direita

	# pega todos os valores da tabela para um certo estado (linha)
	# cria uma nova linha (chave) ao descobrir um novo estado. 
	# Cada estado é uma combinação de posição, bateria e se a posicao atual ta limpa ou não
	def _get_table_values(self, state):
		if state not in self.table:
			self.table[state] = np.zeros(self.n_actions)
		return self.table[state]

	# Algoritmo para decidir entre Eploração e Explotação (Epsilon-Greedy)
	def choose_action(self, state):
		if random.random() < self.epsilon:
			return random.randint(0, self.n_actions - 1)
		return np.argmax(self._get_table_values(state))

	def learn(self, state, action, reward, next_state, done):
		q_current = self._get_table_values(state)[action]
		q_next = 0 if done else np.max(self._get_table_values(next_state))

		# Equação de Atualização de Bellman
		target = reward + self.gamma * q_next
		self.table[state][action] += self.alpha * (target - q_current)

		# a parte que só é executada ao acabar o episódio/simulação
		if done and self.epsilon > self.min_epsilon:
			self.epsilon *= self.epsilon_decay

# cria o ambiente, IA e a treina
env = RoboAspiradorEnv(size=6, max_battery=100)
agent = QLearningVacuumAgent()
episodes = 8_000
max_passos = 1_000
recompensas_por_episodio = []
passos_por_episodio = []
for ep in range(episodes):
	if(ep % 100 == 0): print('TREINAMENTO EPISODIO ', ep)
	state = env.reset()
	done = False
	total_reward = 0

	while not done and env.step_count < max_passos:
		action = agent.choose_action(state)
		next_state, reward, done = env.step(action)
		agent.learn(state, action, reward, next_state, done)
		state = next_state
		total_reward += reward

	recompensas_por_episodio.append(total_reward)
	passos_por_episodio.append(env.step_count)

# ============================ IA TREINADA. AGORA MOSTRA ELA FUNCIONANDO ============================
agent.epsilon = 0.0  # Desativa exploração para o teste final
state = env.reset()
done = False

trajetoria = [list(env.robot_pos)]
acoes_nomes = ['Cima', 'Baixo', 'Esquerda', 'Direita']

print('\n\n--- SIMULAÇÃO DE NAVEGAÇÃO APÓS O TREINAMENTO ---')
step_idx = 0
max_steps = 10_000
while not done and step_idx < max_steps:
	action = agent.choose_action(state)
	state, reward, done = env.step(action)
	trajetoria.append(list(env.robot_pos))
	step_idx += 1

	row, col, bat, sujo = state
	celulas_limpas = np.sum(env.dirt_map == 0)
	porcentagem_limpa = (celulas_limpas / (env.size * env.size)) * 100

	# imprime o mapa com mostrando cada passo
	grid_visual = np.full((env.size, env.size), ' [ . ] ', dtype=object)
	# popula o mapa com as casas sujas, base e robo
	for r in range(env.size):
		for c in range(env.size):
			if (r, c) == env.base:
				grid_visual[r, c] = ' [ B ] '  # Base de Carregamento
			if env.dirt_map[r, c] == 1:
				grid_visual[r, c] = ' [ * ] '  # Célula não limpa
			if env.robot_pos[0] == r and env.robot_pos[1] == c:
				grid_visual[row, col] = ' [ o ] '
	# Marca os obstáculos móveis
	for row, col in env.obstacles:
		grid_visual[row, col] = ' [ X ] '  # Obstáculo móvel
	# mostra na tela o mapa
	for r in range(env.size):
		linha_str = ''.join(grid_visual[r, :])
		print(linha_str)
	print('---------------\n')

# imprimindo estatistica do desempenho da IA
celulas_limpas = np.sum(env.dirt_map == 0)
total_celulas = env.size * env.size
porcentagem_limpa = (celulas_limpas / total_celulas) * 100
print('\n------------------------- ESTATISTICAS -------------------------')
if(not done): print('IA NÃO CONSEGUIU CONCLUIR O TRABALHO')
print(f'• Área Limpa: {celulas_limpas}/{total_celulas} células ({porcentagem_limpa:.1f}%)')
print(f'• Bateria Restante ao Retornar à Base: {env.battery}/{env.max_battery}')
print(f'• Movimento do Robô (Total de Passos): {len(trajetoria) - 1}')


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
# Tira a média móvel de 30 episódios para mostrar uma curva mais suave com a tendência
media_movel = np.convolve(passos_por_episodio, np.ones(30) / 30, mode='valid')
plt.figure(figsize=(9, 5))
plt.plot(passos_por_episodio, alpha=0.3, color='gray', label='Episódio')
plt.plot(media_movel, color='blue', linewidth=2, label='Média Móvel (30 ep)')
plt.title('Evolução da quantidade de passos — Q-Learning')
plt.xlabel('Episódio')
plt.ylabel('Num Passos')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
