import matplotlib.pyplot as plt
import numpy as np
from sklearn.linear_model import Perceptron

TAXA_APRENDIZADO = 0.1
MAX_EPOCAS = 100

rng = np.random.RandomState(42)
num_por_classe= 50
classeA = rng.randn(num_por_classe, 2) + np.array([-2, -2])
classeB = rng.randn(num_por_classe, 2) + np.array([2, 2])

X = np.vstack([classeA, classeB])
y = np.hstack([-np.ones(num_por_classe), np.ones(num_por_classe)])

# tol é o quão grande uma mudança tem de ser para ser considerada. Qualquer coisa abaixo disso é considerado igual
modelo = Perceptron(eta0=TAXA_APRENDIZADO, max_iter=MAX_EPOCAS, tol=1e-3, random_state=42)
modelo.fit(X, y)

pesos = modelo.coef_[0]
bias = modelo.intercept_[0]
print("Pesos encontrados:", pesos)
print("Bias encontrado:", bias)
print("Épocas até parar:", modelo.n_iter_)

# Prevê a categoria de um dado novo
prev1 = modelo.predict([ [-1, -2] ])
print("Categoria da previsão 1:", prev1)
prev2 = modelo.predict([ [2, 3] ])
print("Categoria da previsão 2:", prev2)

# plota o gráfico com os dados e a reta do perceptron
plt.figure(figsize=(7, 6))
plt.scatter(X[y == -1, 0], X[y == -1, 1], c="tab:red", label="classe -1", edgecolors="k")
plt.scatter(X[y == 1, 0], X[y == 1, 1], c="tab:blue", label="classe +1", edgecolors="k")

w0, w1 = pesos
x0_vals = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 100)
x1_vals = -(w0 * x0_vals + bias) / w1
plt.plot(x0_vals, x1_vals, "k--", label="Linha do perceptron")
plt.title("Perceptron")
plt.xlabel("x0")
plt.ylabel("x1")
plt.legend()
plt.show()