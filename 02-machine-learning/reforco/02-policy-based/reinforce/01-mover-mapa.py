from typing import Tuple, List
import matplotlib.pyplot as plt
import numpy as np
import torch
import torch.nn as nn
# o REINFORCE usa uma rede neural como política, por isso usamos o PyTorch. Ele calcula os gradientes sozinho
# e tem os otimizadores prontos (Adam) para fazer a subida de gradiente

# programa: a IA precisa aprender a navegar por um espaço 4x4 com alguns buracos

# cria nosso ambiente (mapa), ações possíveis e altera esse ambiente
# o ambiente é o proprio objeto (não tem um atributo mapa). goal, my_pos, size e holes compõem o ambiente
# actions é a lista de ações possíveis
# o método step altera o ambiente (nos move no mapa - altera my_pos, que faz parte do ambiente)
# NÃO TEM NENHUMA DIFERENÇA EM RELAÇÃO AO Q-LEARNING
class GridWorld:
	size: int
	my_pos: Tuple[int, int]
	goal: Tuple[int, int]
	holes: List[Tuple[int, int]]
	actions: List[int]

	def __init__(self, size=4):
		self.size = size
		self.my_pos = (0, 0) # Estado Inicial (canto superior esquerdo)
		self.goal = (3, 3)  # Objetivo (canto inferior direito)
		self.holes = [(1, 1), (2, 2)]  # Obstáculos / Buracos
		self.actions = [0, 1, 2, 3]  # 0: Cima, 1: Baixo, 2: Esquerda, 3: Direita

	def reset(self):
		self.my_pos = (0, 0)
		return self._pos_to_index(self.my_pos)

	# pega o indice da posição no mapa
	def _pos_to_index(self, pos):
		return pos[0] * self.size + pos[1]

	# retorna se chegou ao ponto final e a recompensa (recompensa imediata)
	def step(self, action):
		row, col = self.my_pos

		if action == 0: # Cima
			row = max(0, row - 1)
		elif action == 1: # Baixo
			row = min(self.size - 1, row + 1)
		elif action == 2: # Esquerda
			col = max(0, col - 1)
		elif action == 3: # Direita
			col = min(self.size - 1, col + 1)

		self.my_pos = (row, col)
		next_state_idx = self._pos_to_index(self.my_pos)

		# Verificação de estados terminais e recompensas
		if self.my_pos == self.goal:
			return (next_state_idx, 10.0, True)  # Recompensa por atingir o objetivo = 10
		elif self.my_pos in self.holes:
			return (next_state_idx, -10.0, True) # Penalidade por cair no buraco = -10
		else:
			# Penalidade de movimento = -1 (busca menor caminho então pune a cada passa para depois ficar com o modelo que dá menos passos)
			# como nao sabemos a direção do objetivo, todas as casa tem a mesma penalidade
			return (next_state_idx, -1.0, False)


# A POLÍTICA P_θ(a|s): rede neural que recebe o estado e devolve a probabilidade de cada ação
# Substitui a tabela Q. Ao invés de guardar um valor para cada (estado, ação) a rede calcula diretamente a chance de escolher cada ação.
# θ são os pesos da rede, e é eles que o REINFORCE ajusta
# Como as ações são discretas (para qual lado andar) a camada de saída usa softmax
class PoliticaRede(nn.Module): # herda a rede neural base
	def __init__(self, n_states, n_actions, n_neuronios=32):
		super().__init__()
		self.rede = nn.Sequential(
			nn.Linear(n_states, n_neuronios), # cria a camada de entrada (com n_states neuronios) e a camada oculta com todos neuronios ligados
			nn.ReLU(), # diz que a camada oculta usa ReLU
			nn.Linear(n_neuronios, n_actions), # cria a camada de saída com todos neuronios ligados
			nn.Softmax(dim=-1), # transforma a saída em probabilidades (soma = 1). Ações discretas usam Softmax
		)

	def forward(self, x):
		return self.rede(x)

# a rede não entende "estado 5". Transformamos o índice num vetor one-hot (16 posições, tudo 0 e um único 1 na casa atual)
# Se passassemos o número 5 direto a rede acharia que o estado 5 é "maior" ou "mais parecido" com o 6 do que com o 1, o que não faz sentido
def posix_to_one_hot(state: int, n_states: int) -> torch.Tensor:
	vetor = torch.zeros(n_states)
	vetor[state] = 1.0
	return vetor

# calcula a entropia atraveś do bonus de entropia: média da equação de entropia de Shannon sobre todos os estados
# Não existe epsilon: a exploração é o próprio sorteio das ações pela política (está embutida na propria política)
# Como a rede neural devolve uma probabilidade, essa probabilidade descreve a propria chance de fazer exploração/explotação
# No começo a distribuição é uniforme (exploração maxima) e conforme aprende vai diminuindo
def calcular_entropia_politica(politica: PoliticaRede, n_states: int) -> float:
	with torch.no_grad(): # só estamos medindo, não queremos que o PyTorch guarde o grafo para calcular gradiente
		todos_estados = torch.eye(n_states) # matriz identidade = one-hot de todos os estados de uma vez
		probs = politica(todos_estados)
		# Fórmula da Entropia de Shannon: H(s) = - sum(prob * log2(prob)). clamp evita log(0)
		entropias_estados = -(probs * torch.log2(probs.clamp(min=1e-12))).sum(dim=1)
	# Retorna a entropia média do ambiente
	return entropias_estados.mean().item()


# Monte Carlo: calcula o retorno G_t de cada passo, só possível depois que o episódio acabou
# G_t = R_{t+1} + γ*R_{t+2} + γ²*R_{t+3} + ... (tudo que veio DEPOIS da ação, com desconto)
# Percorre de trás pra frente para reaproveitar a conta: G_t = R_{t+1} + γ*G_{t+1}
def calcular_retornos(recompensas: List[float], gamma: float) -> torch.Tensor:
	retornos = []
	G = 0.0
	for r in reversed(recompensas):
		G = r + gamma * G
		retornos.insert(0, G)
	return torch.tensor(retornos)


env = GridWorld(size=4)
n_states = env.size * env.size
n_actions = len(env.actions)

# Hiperparâmetros
alpha = 0.01  # Taxa de Aprendizado (usada pelo otimizador da rede)
gamma = 0.99  # Fator de Desconto
episodios = 800  # numero de vezes que vamos repetir a simulação

torch.manual_seed(42)
np.random.seed(42)
politica = PoliticaRede(n_states, n_actions) # pesos θ inicializados aleatoriamente (passo 1 do REINFORCE)
otimizador = torch.optim.Adam(politica.parameters(), lr=alpha)

# treinamento do modelo
episodios_a_imprimir = [0, 100, 700]
recompensas_por_episodio = []
passos_por_episodio = []
entropia_por_episodio = []
for episodio in range(episodios):
	state = env.reset() # como é uma simulação nova, iniciamos do 0
	done = False
	# Limite bem menor que no Q-Learning: no início a política é aleatória e um episódio de milhares de passos
	# geraria um retorno enorme e negativo, que faz uma atualização gigante nos pesos e desestabiliza o treino
	max_passos = 100
	passos = 0
	recompensa_total = 0

	# Calcula e registra a entropia média da política antes de iniciar as ações do episódio
	entropia_atual = calcular_entropia_politica(politica, n_states)
	entropia_por_episodio.append(entropia_atual)

	if(episodio in episodios_a_imprimir): print(f'\n\n===================== EPISODIO {episodio} =====================')

	# guardamos todos os passos do episódio, pois o REINFORCE só aprende quando o episódio acaba (passo 2)
	log_probs = []
	recompensas = []
	while not done and passos < max_passos:
		# Não existe Epsilon-Greedy: a rede devolve uma distribuição de probabilidades e SORTEAMOS a ação a partir dela.
		# Ações com mais probabilidade saem mais vezes (explotação), mas as outras ainda podem sair (exploração).
		# Conforme a rede aprende as probabilidades ficam concentradas na melhor ação e a exploração diminui sozinha
		probs = politica(posix_to_one_hot(state, n_states))
		distribuicao = torch.distributions.Categorical(probs)
		action = distribuicao.sample()

		# guarda o log P_θ(a|s) da ação escolhida. É dele que o PyTorch vai tirar o gradiente depois
		log_probs.append(distribuicao.log_prob(action))

		# Executa ação no ambiente
		state, reward, done = env.step(action.item())
		recompensas.append(reward)
		recompensa_total += reward

		# imprime cada passo dado para ajudar a visualização
		# mostra que nos episodios finais dura bem menos passos e vai bem mais direto ao ponto
		if(episodio in episodios_a_imprimir):
			print(f'Passo {passos}')
			matriz = '.'*env.size*env.size
			matriz = matriz[:state] + 'X' + matriz[state+1:]
			for i in range(env.size):
				print(matriz[i*4:i*4+4])
			print('')

		passos += 1

	# acabei 1 simulação (cheguei ao ponto ou estourei o limite). Agora sim o REINFORCE aprende
	# Cálculo dos retornos G_t de cada passo (passo 3)
	retornos = calcular_retornos(recompensas, gamma)

	# Função de custo (passo 4): L = - sum(log P_θ(a_t|s_t) * G_t)
	# O PyTorch só sabe MINIMIZAR (gradiente descendente). Minimizar -J é o mesmo que maximizar J (gradiente ascendente),
	# por isso o sinal de menos. Ações com G_t alto ganham probabilidade, ações com G_t baixo perdem
	loss = -(torch.stack(log_probs) * retornos).sum()

	otimizador.zero_grad() # zera os gradientes do episódio anterior (o PyTorch acumula por padrão)
	loss.backward()        # backpropagation: calcula ∇_θ da loss para todos os pesos
	otimizador.step()      # atualiza os pesos θ da rede

	recompensas_por_episodio.append(recompensa_total)
	passos_por_episodio.append(passos)

# =====================================================================
# EXIBIÇÃO DA POLÍTICA APRENDIDA
# a política é a ação de maior probabilidade em cada estado
simbolos_acoes = ['↑', '↓', '←', '→']
with torch.no_grad():
	probs_todos_estados = politica(torch.eye(n_states))
politica_aprendida = np.array([simbolos_acoes[torch.argmax(probs_todos_estados[s]).item()] for s in range(n_states)]).reshape(4, 4)
print('--- POLÍTICA OTIMIZADA APRENDIDA (EIXO 4x4) ---')
print(politica_aprendida)
print(f'Maior Recompensa: {max(recompensas_por_episodio)} no Episodio: {np.argmax(recompensas_por_episodio)}. Num passos: {passos_por_episodio[np.argmax(recompensas_por_episodio)]}')


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
# Tira a média móvel de 30 episódios para mostrar uma curva mais suave com a tendência
media_movel = np.convolve(passos_por_episodio, np.ones(30) / 30, mode='valid')
plt.figure(figsize=(9, 5))
plt.plot(passos_por_episodio, alpha=0.3, color='gray', label='Episódio')
plt.plot(media_movel, color='blue', linewidth=2, label='Média Móvel (30 ep)')
plt.title('Evolução da quantidade de passos — REINFORCE')
plt.xlabel('Episódio')
plt.ylabel('Num Passos')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()

# VISUALIZAÇÃO: CURVA DE ENTROPIA
# no REINFORCE a entropia cai de forma "orgânica" (a rede vai ficando confiante), e não seguindo uma curva fixa de decaimento como o epsilon
plt.figure(figsize=(9, 5))
plt.plot(entropia_por_episodio, color='purple', linewidth=2, label='Entropia Média (bits)')
plt.title('Evolução da Entropia')
plt.xlabel('Episódio')
plt.ylabel('Entropia')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()
