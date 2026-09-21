import random
import numpy as np

# SIMULAÇÃO DE MONTE CARLO PARA CALCULAR A INTEGRAL DE X^2 de 0 a 10

# ESTRUTURA DE UMA SIMULAÇÃO DE MONTE CARLO
# definir a distribuição a ser usada e seus parametros
# loop de N simulações (geralmente dezenas ou centenas de milhares)
# Em cada loop:
#   geração de K valores aleatórios seguindo a distribuição definida
#   calcular se está dentro da curva ou não
# calcular média dos valores dentro da curva

# número de pontos aleatórios (número de repetições)
num_amostras = 100_000

# conta quantos pontos caíram dentro da área da curva
dentro_area = 0
y_estimados = []
for _ in range(num_amostras):
  # Pega um ponto aleatório dentro do quadrado 10x100 (valor maximo da equação x^2 pra x de 0 a 10)
  x = random.uniform(0,10) # k = 1
  y = random.uniform(0,100)
  # calcula se está dentro da área da curva (menor ou igual que o valor da equação para aquele X)
  val_equacao = x**2
  y_estimados.append(y)
  if(y <= val_equacao): dentro_area += 1

# valores para calcular a integral e o erro padrão
area_quadrado= 10*100
area_curva_real = 333.33

prob_ponto_dentro_curva = dentro_area / num_amostras
area_curva_estimada = prob_ponto_dentro_curva * area_quadrado
erro_padrao = np.std(y_estimados, ddof=1) / np.sqrt(num_amostras)

print(f"Valor estimado de x^2: {area_curva_estimada:.2f}. Valor real: {area_curva_real}. Erro Padrão: {erro_padrao:.4f}")

