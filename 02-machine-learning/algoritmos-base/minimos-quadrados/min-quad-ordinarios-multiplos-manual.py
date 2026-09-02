
import numpy as np

def minimos_quadrados_multiplos(x_matrix, y_values):
    # calculando os coeficientes da equação linear usando a fórmula dos minimos quadrados
    # A = matriz dos coeficientes angulares, aonde o 1º é o intercepto
    # A = (X^T X)^{-1} X^T Y
    X = np.array(x_matrix, dtype=float)
    y = np.array(y_values, dtype=float).flatten()

    # Adiciona intercepto (coluna de 1s)
    lista_ones = np.ones((X.shape[0], 1))
    X = np.hstack((lista_ones, X))

    # Coeficientes pela equação normal: (X^T X)^{-1} X^T y
    x_quadrado = X.T @ X
    x_quadrado_inv = np.linalg.inv(x_quadrado)
    return x_quadrado_inv @ X.T @ y


# equacao original = 3x1 + 2x2 + 5x3 + 2
x1_values = [0, 1, 2, 3]
x2_values = [1, 1, 2, 4]
x3_values = [1, 2, 3, 3]
y_values = [9, 17, 27, 34]

# Monta a matriz X com cada coluna sendo uma variável (sem intercepto)
# Ao invés de cada linha ser um X diferente, cada coluna é uma variável diferente
X = np.column_stack((x1_values, x2_values, x3_values))

a0, a1, a2, a3 = minimos_quadrados_multiplos(X, y_values)
# coef[0] é o intercepto
print(f'A equação da reta de regressão linear é: y = {a1:.1f}x1 + {a2:.1f}x2 + {a3:.1f}x3 + {a0:.1f}')

# equacao original = 3x1 + 2x2 + 5x3 + 2 + ruído
y_values = [9, 19, 26, 33]
a0, a1, a2, a3 = minimos_quadrados_multiplos(X, y_values)
print(f'A equação da reta de regressão linear é: y = {a1:.1f}x1 + {a2:.1f}x2 + {a3:.1f}x3 + {a0:.1f}')
