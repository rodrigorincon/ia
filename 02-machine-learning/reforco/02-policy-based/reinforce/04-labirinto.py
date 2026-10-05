import random
from typing import List, Tuple
from matplotlib import pyplot as plt
import numpy as np
import torch
import torch.nn as nn

# cria variável que representa o labirinto
Labirinto = np.ndarray[List[int]]
Point = Tuple[int, int]

# GERA UM LABIRINTO ALEATÓRIO (0 LIVRE, 1 PAREDE) COM (2*altura) x (2*largura) CASAS
# Treinar em vários labirintos diferentes faz a IA aprender regras gerais ao invés de decorar um mapa.
# No Q-Learning isso era para cobrir o máximo de estados da tabela. Na rede neural é para ela generalizar:
# estados parecidos geram ações parecidas, mesmo que aquele estado exato nunca tenha aparecido no treino
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
		vizinhos = []
		for desloc_row, desloc_col in [(-2, 0), (2, 0), (0, -2), (0, 2)]:
			if(0 <= row + desloc_row < rows and 0 <= col + desloc_col < cols and labirinto[row + desloc_row, col + desloc_col] == 1):
				vizinhos.append((row + desloc_row, col + desloc_col, desloc_row // 2, desloc_col // 2))
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
	# Assim o que ele aprende nos labirintos de treino continua valendo num labirinto nunca visto.
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

	# Assim como no Q-Learning, não criamos regras (ifs e código) proibindo certos movimentos.
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


# A POLÍTICA P_θ(a|s): rede neural que recebe o estado e devolve a "nota" (logit) de cada ação
# Aqui a rede NÃO termina em Softmax: devolve os logits crus para podermos bloquear as ações inválidas (paredes)
# antes de transformar em probabilidade (ver choose_action)
class PoliticaRede(nn.Module):
	def __init__(self, n_entradas, n_acoes, n_neuronios=64):
		super().__init__()
		self.rede = nn.Sequential(
			nn.Linear(n_entradas, n_neuronios),
			nn.ReLU(),
			nn.Linear(n_neuronios, n_neuronios),
			nn.ReLU(),
			nn.Linear(n_neuronios, n_acoes),
		)

	def forward(self, x):
		return self.rede(x)


# modelo da IA. É aqui que ao algoritmo é executado
class ReinforceMazeAgent:
	politica: PoliticaRede
	otimizador: torch.optim.Optimizer
	gamma: float
	n_actions: int
	log_probs: List[torch.Tensor]
	recompensas: List[float]

	def __init__(self, alpha=0.001, gamma=0.95):
		self.gamma = gamma
		self.n_actions = 4
		# 25 entradas: 4 vizinhos x 4 códigos (one-hot) + direção da saída em linha e coluna (3 + 3, one-hot) + visitas aqui (one-hot de 1 a 3)
		self.politica = PoliticaRede(25, self.n_actions)
		self.otimizador = torch.optim.Adam(self.politica.parameters(), lr=alpha)
		# memória do episódio atual. O REINFORCE só aprende quando o episódio acaba (Monte Carlo)
		self.log_probs = []
		self.recompensas = []

	# Transforma a tupla do estado em vetor para a rede. Todos os campos são categorias, então viram one-hot.
	# Ex: o código de vizinho 3 não é "3x maior" que o 1, são situações diferentes (parede, livre, visitada...)
	def _estado_para_tensor(self, state):
		vetor = []
		for codigo in state[:4]:      # vizinhos: 0..3
			one_hot = [0, 0, 0, 0]
			one_hot[codigo] = 1
			vetor += one_hot
		for direcao in state[4:6]:    # direção da saída: -1, 0 ou 1
			one_hot = [0, 0, 0]
			one_hot[direcao + 1] = 1
			vetor += one_hot
		visitas = [0, 0, 0]           # visitas na casa atual: 1, 2 ou 3+
		visitas[state[6] - 1] = 1
		vetor += visitas
		return torch.tensor(vetor, dtype=torch.float32)

	# Não há Epsilon-Greedy: a exploração vem do sorteio da ação a partir das probabilidades da rede.
	# Como no Q-Learning, filtramos as ações válidas: os logits das ações que levam a parede viram -infinito,
	# então depois do Softmax elas ficam com probabilidade 0 e nunca são sorteadas
	# deterministico=True escolhe sempre a ação mais provável (usado depois de treinado)
	def choose_action(self, state, deterministico=False):
		# Os primeiros 4 elementos do estado descrevem os vizinhos: 0 = Parede, 1..3 = Livre (com nº de visitas)
		mascara_validas = torch.tensor([codigo != 0 for codigo in state[:4]])
		# Caso de emergência: se não houver ações válidas (ex: encurralado), permite todas
		if not mascara_validas.any():
			mascara_validas[:] = True

		logits = self.politica(self._estado_para_tensor(state))
		logits = logits.masked_fill(~mascara_validas, float('-inf'))
		distribuicao = torch.distributions.Categorical(logits=logits) # aplica o Softmax internamente

		if deterministico:
			return torch.argmax(distribuicao.probs).item()
		action = distribuicao.sample()
		self.log_probs.append(distribuicao.log_prob(action)) # guarda log P_θ(a|s) para o gradiente no fim do episódio
		return action.item()

	# só guarda a recompensa. No Q-Learning aprendiamos a cada passo, aqui esperamos o episódio terminar
	def store_reward(self, reward):
		self.recompensas.append(reward)

	# chamado ao fim do episódio: calcula os retornos e atualiza os pesos da rede
	def learn(self):
		# Retorno G_t de cada passo, de trás pra frente: G_t = R_{t+1} + γ*G_{t+1}
		retornos = []
		G = 0.0
		for r in reversed(self.recompensas):
			G = r + self.gamma * G
			retornos.insert(0, G)
		retornos = torch.tensor(retornos)

		# Normalização dos retornos (média 0 e desvio padrão 1) para diminuir a ALTA VARIÂNCIA do REINFORCE.
		# Dentro de cada episódio, ações acima da média ganham probabilidade e as abaixo perdem (funciona como um "baseline")
		if len(retornos) > 1:
			retornos = (retornos - retornos.mean()) / (retornos.std() + 1e-8)

		# L = - sum(log P_θ(a_t|s_t) * G_t). Sinal de menos pois o PyTorch minimiza e queremos subida de gradiente
		loss = -(torch.stack(self.log_probs) * retornos).sum()
		self.otimizador.zero_grad()
		loss.backward()
		self.otimizador.step()

		# limpa a memória para o próximo episódio (on-policy: só aprende com dados da política atual)
		self.log_probs = []
		self.recompensas = []


agent = ReinforceMazeAgent()
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
		agent.store_reward(reward)
		state = next_state
		step_count += 1
		total_reward += reward

	# fim do episódio: agora o agente aprende com tudo o que aconteceu
	agent.learn()
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

state = env_teste.reset()
done = False

trajetoria = [list(env_teste.position)]
print('--- SIMULAÇÃO NO LABIRINTO NOVO ---')
step_idx = 0
# Num labirinto novo o agente não conhece o caminho: ele precisa explorar (e às vezes voltar de becos),
# então damos um limite de passos maior que no treino, proporcional ao tamanho do labirinto
max_steps_teste = 2 * grid_teste.size
while not done and step_idx < max_steps_teste:
	# Desativa exploração para o teste (sempre a ação mais provável). no_grad pois não vamos mais treinar
	with torch.no_grad():
		action = agent.choose_action(state, deterministico=True)
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
plt.title('Evolução do Aprendizado — REINFORCE')
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
plt.title('Evolução da quantidade de passos — REINFORCE')
plt.xlabel('Episódio')
plt.ylabel('Num Passos')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
