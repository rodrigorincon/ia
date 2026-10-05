import gymnasium as gym
from stable_baselines3 import PPO
from stable_baselines3.common.evaluation import evaluate_policy
import torch.nn as nn
# instalar as libs stable-baselines3[extra] gymnasium pytorch

# DESAFIO: Um bastão está equilibrado em cima de um carro em movimento. Você deve manter o bastão equilibrado em cima do carro 
# apenas o empurrando para a esquerda ou direita

NUM_EPISODIOS = 10
MAX_PASSOS = 2048
BATCH_SIZE = 64 # para o gradiente ascendente com mini-batches
TAXA_APRENDIZADO = 0.0003
GAMMA = 0.99 # fator de desconto. O quanto a IA prefere recompensas imediatas a recompensas a longo prazo (valor alto faz ele pensar a longo prazo)
CLIP_RANGE = 0.2 # limita a atualização da política a no máximo 20%

# GAE: método estatístico usado para calcular a vantagem
# vantagem: mede o quanto uma ação específica foi melhor ou pior do que a média esperada naquele estado
# na prática ele balanceia o peso dado entre curto e longo prazo no cálculo da vantagem
# VALOR ALTO SUAVIZA O GRADIENTE E ACELERA A CONVERVENCIA DO TREINO
GAE_LAMBDA = 0.95 

# criação do ambiente
# render_mode='rgb_array' permite avaliar o agente visualmente depois se necessário
# a biblioteca gym já tem um ambiente pré-feito para esse desafio, então não precisamos implementa-lo na mão
env = gym.make("CartPole-v1", render_mode=None, max_episode_steps=MAX_PASSOS)

# define a arquitetura da rede neural do PPO
# o num de camadas ocultas padrão é 2, num de neuronios por camada padrão é 64 e função de ativação padrões é RELU. 
# Para mudar isso tem de passar como abaixo
# a função de ativação da saída não precisa ser especificado pois é fixo (
# Na politica: softmax pra ação discreta e Linear para contínua - podendo ser tanh se quiser normalizar entre -1 e +1
# Na função de valor: Linear)
policy_kwargs = dict(
  net_arch=dict(pi=[64, 64], vf=[64, 64]), # pi = rede da política, vf = rede da função de valor
  activation_fn=nn.ReLU                  # função de ativação (ex: Tanh, ReLU, ELU)
)

# inicialização do modelo PPO (define os hiper-parametros)
# 'MlpPolicy' indica uma rede neural Multilayer Perceptron (ideal para vetores de estado tabulares/contínuos simples)
# verbose=1 mostra o progresso do treinamento no console
# buffer de rollout é n_steps * n_envs, onde n_envs é o número de cópias do ambiente sendo executadas em paralelo)
# ent_coef = coeficiente de entropia

# se o MAX_PASSOS passado no PPO for maior que o passado no ambiente a atualização das redes acontecerá após mais de um episódio.
# ex se no env passamos 1000 e aqui passamos 2000 então atualizaremos os pesos a cada 2 episódios. No caso colocamos o mesmo para atualizar a cada episódio
model = PPO("MlpPolicy", env, verbose=1, learning_rate=TAXA_APRENDIZADO, n_steps=MAX_PASSOS, batch_size=BATCH_SIZE, n_epochs=NUM_EPISODIOS, 
            gamma=GAMMA, gae_lambda=GAE_LAMBDA, clip_range=CLIP_RANGE, ent_coef=0.0, policy_kwargs=policy_kwargs)

print("Iniciando o treinamento do PPO no CartPole-v1...")
# treinamento do agente. total_timesteps diz quantos passos daremos exatamente durante o treinamento (somando todos os passos de todos os episodios)
model.learn(total_timesteps=50_000)
print("Treinamento concluído!")

# Avaliação do desempenho médio do agente treinado
mean_reward, std_reward = evaluate_policy(model, env, n_eval_episodes=10)
print(f"Recompensa média: {mean_reward} +/- {std_reward}")

# Executando um episódio visual para testar o agente na prática
env_visual = gym.make("CartPole-v1", render_mode="human")
obs, info = env_visual.reset()

for _ in range(500):
	# O modelo prediz a melhor ação com base na observação atual do ambiente
	action, _states = model.predict(obs, deterministic=True)
	obs, reward, terminated, truncated, info = env_visual.step(action)
	
	if terminated or truncated:
		obs, info = env_visual.reset()

env.close()
env_visual.close()