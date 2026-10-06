# Criação do ambiente do Super Mario Bros com os "wrappers" que transformam o jogo em algo que a IA aprende mais fácil.
# Um wrapper envolve o ambiente e altera o que entra (ações) ou o que sai (observação, recompensa) dele.
import gymnasium as gym
import gym_super_mario_bros  # registra os ambientes "SuperMarioBros-..." no gymnasium
from gym_super_mario_bros.actions import SIMPLE_MOVEMENT
from nes_py.wrappers import JoypadSpace
import config

class PularFrames(gym.Wrapper):
	"""Repete a mesma ação por N frames e soma as recompensas.
	Frames seguidos são quase idênticos, então decidir a cada frame só deixaria o treino mais lento."""

	def __init__(self, env, n_frames):
		super().__init__(env)
		self.n_frames = n_frames

	def step(self, acao):
		recompensa_total = 0.0
		for _ in range(self.n_frames):
			obs, recompensa, terminado, truncado, info = self.env.step(acao)
			recompensa_total += recompensa
			if terminado or truncado:
				break
		return obs, recompensa_total, terminado, truncado, info

def criar_ambiente(fase=config.FASE_TREINO, render_mode=None):
	# A recompensa padrão do ambiente já é pensada para o Mario: ganha pontos ao andar para a direita,
	# perde com o tempo passando e perde muito ao morrer. O episódio termina ao morrer ou pegar a bandeira.
	env = gym.make(f"SuperMarioBros-{fase}-v0", render_mode=render_mode)

	# O controle do NES tem 256 combinações de botões. Reduzimos para 7 ações úteis:
	# nada, direita, direita+pulo, direita+correr, direita+pulo+correr, pulo, esquerda
	env = JoypadSpace(env, SIMPLE_MOVEMENT)

	env = PularFrames(env, config.PULAR_FRAMES)

	# cor não ajuda a jogar, e imagem menor = rede menor e treino mais rápido
	env = gym.wrappers.GrayscaleObservation(env) # remove as cores
	env = gym.wrappers.ResizeObservation(env, (config.TAMANHO_IMAGEM, config.TAMANHO_IMAGEM))

	env = gym.wrappers.TransformReward(env, lambda r: r / config.ESCALA_RECOMPENSA)

	# uma imagem parada não mostra se o Mario está subindo ou caindo; com vários frames a rede percebe o movimento
	# observação final: (4, 84, 84)
	env = gym.wrappers.FrameStackObservation(env, config.FRAMES_EMPILHADOS)
	return env
