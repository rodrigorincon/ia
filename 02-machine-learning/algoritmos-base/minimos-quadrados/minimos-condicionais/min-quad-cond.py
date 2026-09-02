import numpy as np
from statsmodels.tsa.arima.model import ARIMA

# cria os dados (serie temporal) e define o tamanho da janela (p)
np.random.seed(42)
y_total = np.random.rand(100) 
p = 3
n = len(y_total)

####### MANUAL

# cria o vetor Y e a matriz X para o modelo AR(p)
Y = y_total[p:] # vetor começa na posição p e vai até o fim

# matriz X terá n - p linhas e p colunas.
X = np.zeros((n - p, p))

# preenche os valores da matriz X com os dados anteriores
for i in range(p):
    # a cada loop preenche uma coluna na matriz
    # preenche a coluna inteira de uma vez
    X[:, i] = y_total[p - (i + 1) : n - (i + 1)]

# executa a formula dos minimos quadrados A = (X^T * X)^-1 * X^T * Y
X_T = X.T
A = np.linalg.inv(X_T @ X) @ X_T @ Y

# 5. EXIBINDO OS RESULTADOS
print("Coeficientes Encontrados (Phi):")
print(f"Phi 1 (Ontem):       {A[0]:.4f}")
print(f"Phi 2 (Anteontem):   {A[1]:.4f}")
print(f"Phi 3 (3 dias atrás): {A[2]:.4f}")


####### USANDO BIBLIOTECA
print("\n--- Usando biblioteca ---")
modelo = ARIMA(y_total, order=(p, 0, p)).fit()
phi_list = modelo.params
print("Coeficientes Encontrados (Phi):")
for i in range(p):
    print(f"Phi {i + 1}: {phi_list[i]:.4f}")