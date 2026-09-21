import random
import numpy as np
from scipy.stats import norm

# SIMULAÇÃO DE MONTE CARLO PARA CALCULAR A INTEGRAL DA CURVA NORMAL -1 a 1 (com média 0 e desvio 1)
x_min = -1
x_max = 1

# ESTRUTURA DE UMA SIMULAÇÃO DE MONTE CARLO (MÉTODO 2, sem contar pontos dentro e fora da curva)
# definir a distribuição a ser usada e seus parametros
# loop de N simulações (geralmente dezenas ou centenas de milhares)
# Em cada loop:
#   geração de K valores aleatórios seguindo a distribuição definida
#   y previsto = calcular a equação com os valores aleatorios
# calcular média dos valores previstos * a distancia entre os limites em X (no exemplo, 2)

# número de pontos aleatórios (número de repetições)
num_amostras = 10_000

# conta quantos pontos caíram dentro da área da curva
y_estimados = []
for _ in range(num_amostras):
  # Pega um ponto aleatório dentro do intervalo de -1 a 1
  x = random.uniform(x_min, x_max) # k = 1
  # calcula o valor da curva normal para esse ponto
  y = norm.pdf(x, loc=0, scale=1)
  y_estimados.append(y)

integral_estimada = (x_max - x_min) * np.mean(y_estimados)
erro_padrao = (x_max - x_min) * np.std(y_estimados, ddof=1) / np.sqrt(num_amostras)

integral_real = norm.cdf(1, loc=0, scale=1) - norm.cdf(-1, loc=0, scale=1)

print(f"Valor estimado da curva normal: {integral_estimada:.4f}. Valor real: {integral_real:.4f}. Erro Padrão: {erro_padrao:.4f}")

