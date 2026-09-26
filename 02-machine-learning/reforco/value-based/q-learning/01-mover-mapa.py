from typing import Tuple, List

import matplotlib.pyplot as plt
import numpy as np
# scikit learn não tem algoritmos por reforço. As libs que podem ser usadas são
# Gymnasium / OpenAI Gym para jogos ou PyTorch / TensorFlow quando tem muitas colunas e exige redes neurais

# programa: a IA precisa aprender a navegar por um espaço 4x4 com alguns buracos

# cria nosso ambiente (mapa), ações possíveis e altera esse ambiente
# o ambiente é o proprio objeto (não tem um atributo mapa). goal, my_pos, size e holes compõem o ambiente
# actions é a lista de ações possíveis
# o método step altera o ambiente (nos move no mapa - altera my_pos, que faz parte do ambiente)
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


env = GridWorld(size=4)
n_states = env.size * env.size
n_actions = len(env.actions)

# Inicialização da Tabela Q com zeros (Dimensões: 16 x 4)
# cada linha é um estado (16 pois são o numero de lugares q pode estar) e as colunas são as ações q pode fazer
Q_table = np.zeros((n_states, n_actions))

# Hiperparâmetros
alpha = 0.1  # Taxa de Aprendizado
gamma = 0.99  # Fator de Desconto
epsilon = 1.0  # Taxa de Exploração inicial (100% aleatório)
epsilon_decay = 0.995  # Decaimento do epsilon a cada episódio
min_epsilon = 0.01  # Mínimo de exploração mantido
episodios = 800  # numero de vezes que vamos repetir a simulação

# treinamento do modelo
episodios_a_imprimir = [0, 100, 700]
recompensas_por_episodio = []
passos_por_episodio = []
np.random.seed(42)
for episodio in range(episodios):
	state = env.reset() # como é uma simulação nova, iniciamos do 0
	done = False
	max_passos = 10_000
	passos = 0
	recompensa_total = 0

	if(episodio in episodios_a_imprimir): print(f'\n\n===================== EPISODIO {episodio} =====================')

	while not done and passos < max_passos:
		# Algoritmo de escolha entre Exploração e Explotação: Epsilon-Greedy (versão mais simples do minimax)
		# epsilon começa em 100% aleatorio e vai reduzindo epsilon a cada nova simulação (mas sem nunca chegar a 0 pra ter sempre uma pitada de aleatorio). 
		# Como o conhecimento se acumula entre as simulações a gente começa a proxima simulção melhor que na anterior.
		# sorteamos um numero aleatorio. Se ele for menor que o epsilon atual fazemos um movimento aleatorio, senão fazemos o melhor movimento possivel pra essa posição (linha)
		# como epilon começa no 100% no inicio é tudo aleatorio e no final é quase tudo deterministico.
		if np.random.rand() < epsilon:
			action = np.random.choice(n_actions)  # Exploração (Aleatório)
		else:
			action = np.argmax(Q_table[state])  # Explotação (Melhor ação Q). Pega a melhor ação para a linha (estado/posição)

		# Executa ação no ambiente
		prev_state = state
		state, reward, done = env.step(action)
		recompensa_total += reward

		# Função de custo: atualiza a tabela Q a partir da equação de Bellman para Q-Learning
		best_next_action = np.argmax(Q_table[state])
		td_target = reward + gamma * Q_table[state, best_next_action]
		td_error = td_target - Q_table[prev_state, action]
		Q_table[prev_state, action] += alpha * td_error

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

	# acabei 1 simulação (cheguei ao ponto ou estourei o limite)
	# Atualização do Epsilon
	epsilon = max(min_epsilon, epsilon * epsilon_decay)
	recompensas_por_episodio.append(recompensa_total)
	passos_por_episodio.append(passos)

# =====================================================================
# EXIBIÇÃO DA POLÍTICA APRENDIDA
simbolos_acoes = ['↑', '↓', '←', '→']
politica_aprendida = np.array([simbolos_acoes[np.argmax(Q_table[s])] for s in range(n_states)]).reshape(4, 4)
print('--- POLÍTICA OTIMIZADA APRENDIDA (EIXO 4x4) ---')
print(politica_aprendida)
print(f'Maior Recompensa: {max(recompensas_por_episodio)} no Episodio: {np.argmax(recompensas_por_episodio)}. Num passos: {passos_por_episodio[np.argmax(recompensas_por_episodio)]}')


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
# repare que a maioria das barras são negativas, significando que o valor 10 pra alcançar o ponto final foi pouco. Melhor aumentar
# sinal que deu andou muito em circulo tbm
# teve muita mudança brusca tbm, indicando que o modelo demora a convergir, aprende devagar e ainda desaprende de uma simulação pra outra
# porém a média móvel mostra que apesar da variância a tendência sempre foi positiva e convergiu. Podemos ver isso tbm que os picos e vales foram diminuindo com o passar do tempo
# aumentar as recompensas deixou ainda maior a variância, pois a faixa de valores é expandida

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
# repare que a maioria das barras são negativas, significando que o valor 10 pra alcançar o ponto final foi pouco. Melhor aumentar
# sinal que deu andou muito em circulo tbm
# teve muita mudança brusca tbm, indicando que o modelo demora a convergir, aprende devagar e ainda desaprende de uma simulação pra outra
# porém a média móvel mostra que apesar da variância a tendência sempre foi positiva e convergiu. Podemos ver isso tbm que os picos e vales foram diminuindo com o passar do tempo
