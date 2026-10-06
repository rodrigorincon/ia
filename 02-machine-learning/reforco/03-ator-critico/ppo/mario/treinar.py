# Treina o PPO na fase 1-1 do Super Mario Bros e, ao final, mostra a IA jogando as fases 1-1 e 1-2.
# Uso: python treinar.py
import os
from stable_baselines3 import PPO
from stable_baselines3.common.callbacks import BaseCallback, CheckpointCallback
from stable_baselines3.common.vec_env import SubprocVecEnv, VecMonitor
import config
from ambiente import criar_ambiente
from assistir import mostrar_fases

class ProgressoMario(BaseCallback):
	"""Adiciona ao log do stable-baselines3 informações específicas do Mario: até onde ele chega na fase (x), 
	quantos jogos (episódios) terminaram e quantas vezes pegou a bandeira."""

	def __init__(self):
		super().__init__()
		self.episodios = 0
		self.bandeiras = 0

	def _on_step(self):
		# self.locals["infos"] e ["dones"] têm um item por ambiente paralelo
		for info, terminou in zip(self.locals["infos"], self.locals["dones"]):
			if terminou:
				self.episodios += 1
				self.logger.record_mean("mario/x_final", info["x_pos"])
				if info["flag_get"]:
					self.bandeiras += 1
		self.logger.record("mario/episodios", self.episodios)
		self.logger.record("mario/bandeiras", self.bandeiras)
		return True  # False interromperia o treino

def criar_modelo(env):
	if config.CONTINUAR_TREINO and os.path.exists(config.ARQUIVO_MODELO + ".zip"):
		print("Continuando o treino do modelo salvo em", config.ARQUIVO_MODELO)
		return PPO.load(config.ARQUIVO_MODELO, env=env)

	# 'CnnPolicy': a entrada é uma imagem, então a rede começa com camadas convolucionais
	# (a mesma arquitetura da DQN da DeepMind para Atari) que extraem as características da tela.
	# Em cima delas ficam as cabeças da política (ator) e da função de valor (crítico)
	# por não alterar a configuração padrão, tem 2 camadas ocultas apenas, com 60 neuronios em cada
	return PPO("CnnPolicy", env, verbose=1, learning_rate=config.TAXA_APRENDIZADO, n_steps=config.N_STEPS, batch_size=config.BATCH_SIZE,
		n_epochs=config.N_EPOCHS, gamma=config.GAMMA, gae_lambda=config.GAE_LAMBDA, clip_range=config.CLIP_RANGE, ent_coef=config.ENT_COEF)

def treinar():
	# vários jogos rodando em paralelo, cada um em um processo. Isso acelera a coleta de experiência
	# e deixa os dados de cada atualização mais variados
	env = SubprocVecEnv([lambda: criar_ambiente(config.FASE_TREINO) for _ in range(config.N_AMBIENTES)])
	env = VecMonitor(env)  # registra recompensa e duração dos episódios (ep_rew_mean, ep_len_mean no log)

	modelo = criar_modelo(env)
	checkpoints = CheckpointCallback(save_freq=max(config.SALVAR_A_CADA // config.N_AMBIENTES, 1),  # contado em passos de cada ambiente
																	save_path=config.PASTA_MODELOS, name_prefix="checkpoint")

	print(f"Treinando o PPO na fase {config.FASE_TREINO} por {config.TOTAL_PASSOS:,} passos...")
	try:
		modelo.learn(total_timesteps=config.TOTAL_PASSOS, callback=[checkpoints, ProgressoMario()], reset_num_timesteps=False)
	except KeyboardInterrupt:
		print("\nTreino interrompido pelo usuário. Salvando o que foi aprendido até agora.")
	modelo.save(config.ARQUIVO_MODELO)
	env.close()
	print("Modelo salvo em", config.ARQUIVO_MODELO + ".zip")
	return modelo


if __name__ == "__main__":
	modelo = treinar()
	mostrar_fases(modelo)
