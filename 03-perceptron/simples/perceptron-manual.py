from typing import List
import matplotlib.pyplot as plt
import numpy as np

# taxa de aprendizado: passo de correção dos pesos a cada erro
TAXA_APRENDIZADO = 0.1
MAX_EPOCAS = 100

class Perceptron:
	taxa_aprendizado: float
	max_epocas: int
	pesos: List[float]
	bias: float
	erros_por_epoca: List[int]
	
	def __init__(self, taxa_aprendizado: float, max_epocas: int):
		self.taxa_aprendizado = taxa_aprendizado
		self.max_epocas = max_epocas
		self.pesos = None
		self.bias = 0.0
		self.erros_por_epoca = []

	def _degrau(self, z):
		# função de ativação do perceptron: sem meio-termo, só +1 ou -1
		return 1 if z >= 0 else -1

	def fit(self, X: np.ndarray, y: np.ndarray) -> None:
		n_features = X.shape[1]
		# pesos começam em zero: o perceptron não precisa de inicialização aleatória para convergir (diferente do gradiente descendente)
		self.pesos = np.zeros(n_features)
		self.bias = 0.0
		self.erros_por_epoca = []

		for epoca in range(self.max_epocas):
			erros = 0
			for xi, yi in zip(X, y):
				z = np.dot(xi, self.pesos) + self.bias
				# yi*z <= 0 significa sinais diferentes: classificou errado. Atualiza os pesos
				# não faz nada quando é maior pq nenhuma ação deve ser feita nesse caso (atualização dos pesos só quando erra)
				if yi * z <= 0:
					self.pesos += self.taxa_aprendizado * yi * xi
					self.bias += self.taxa_aprendizado * yi
					erros += 1 # conta a quantidade de variáveis erradas teve na época
			self.erros_por_epoca.append(erros)
			if erros == 0:
				# nenhum erro na época inteira = convergiu
				print(f"Convergiu na época {epoca + 1}")
				break
		else:
			print(f"Não convergiu em {self.max_epocas} épocas (dados podem não ser linearmente separáveis)")
		return

	def predict(self, X: np.ndarray) -> np.ndarray:
		z = X @ self.pesos + self.bias
		return self._degrau(z)


rng = np.random.RandomState(42)
num_por_classe= 50
classeA = rng.randn(num_por_classe, 2) + np.array([-2, -2])
classeB = rng.randn(num_por_classe, 2) + np.array([2, 2])

X = np.vstack([classeA, classeB])
y = np.hstack([-np.ones(num_por_classe), np.ones(num_por_classe)])

perceptron = Perceptron(TAXA_APRENDIZADO, MAX_EPOCAS)
perceptron.fit(X, y)

print("Pesos encontrados:", perceptron.pesos)
print("Bias encontrado:", perceptron.bias)
print("Erros por época:", perceptron.erros_por_epoca)
# Prevê a categoria de um dado novo
prev1 = perceptron.predict([ [-1, -2] ])
print("Categoria da previsão 1:", prev1)
prev2 = perceptron.predict([ [2, 3] ])
print("Categoria da previsão 2:", prev2)


# plota o gráfico com os dados e a reta do perceptron
plt.figure(figsize=(7, 6))
plt.scatter(X[y == -1, 0], X[y == -1, 1], c="tab:red", label="classe -1", edgecolors="k")
plt.scatter(X[y == 1, 0], X[y == 1, 1], c="tab:blue", label="classe +1", edgecolors="k")

w0, w1 = perceptron.pesos
bias = perceptron.bias
x0_vals = np.linspace(X[:, 0].min() - 1, X[:, 0].max() + 1, 100)
x1_vals = -(w0 * x0_vals + bias) / w1
plt.plot(x0_vals, x1_vals, "k--", label="Linha do perceptron")
plt.title("Perceptron")
plt.xlabel("x0")
plt.ylabel("x1")
plt.legend()
plt.show()