import random

# SIMULAÇÃO DE MONTE CARLO PARA ADIVINHAR O VALOR DE PI
# para isso fazemos um quadrado de lado 2 e um círculo inteiro
# medimos quantos pontos aleatorios estão dentro do círculo e quantos fora (semelhante a forma de calcular area da curva sem fazer integral)

# ESTRUTURA DE UMA SIMULAÇÃO DE MONTE CARLO
# definir a distribuição a ser usada e seus parametros
# loop de N simulações (geralmente dezenas ou centenas de milhares)
# Em cada loop:
#   geração de K valores aleatórios seguindo a distribuição definida
#   calcular se está dentro da curva ou não
# calcular média dos valores dentro da curva

# número de pontos aleatórios (número de repetições)
num_amostras = 100_000

# conta quantos pontos caíram dentro do círculo (distância <= 1)
dentro_circulo = 0

for _ in range(num_amostras):
  # Gera coordenadas x e y entre -1 e 1
  x = random.uniform(-1,1)
  y = random.uniform(-1,1)
  # calcula a distância do centro (0,0)
  distancia = (x**2 + y**2)**0.5

  # verifica se caiu dentro do círculo (distância <= 1)
  if(distancia <= 1): dentro_circulo += 1

pi_estimado = 4 * dentro_circulo / num_amostras
print(f"Valor estimado de Pi: {pi_estimado}")
