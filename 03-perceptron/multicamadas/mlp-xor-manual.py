from pathlib import Path
from typing import List
import matplotlib.pyplot as plt
import numpy as np

SEED = 0
TAXA_APRENDIZADO = 1.0
EPOCAS = 10_000 # cada época é 1 volta de todos os dados na rede neural
NEURONIOS_OCULTOS = 2 # arquitetura 2-2-1
# de quantas em quantas épocas imprimir a perda
PRINT_PERDA = 1000

# MLP com apenas 1 camada oculta usando sigmoide na camada oculta e na de saída
class MLP:
	neuronios_ocultos: int
	taxa_aprendizado: float
	W1: np.ndarray
	b1: np.ndarray
	W2: np.ndarray
	b2: np.ndarray
	perdas_por_epoca: List[float]

	def __init__(self, neuronios_ocultos: int, taxa_aprendizado: float, seed: int):
		self.neuronios_ocultos = neuronios_ocultos
		self.taxa_aprendizado = taxa_aprendizado
		self.rng = np.random.default_rng(seed)
		self.perdas_por_epoca = []

	def _sigmoide(self, z: np.ndarray) -> np.ndarray:
		# ativação suave: o degrau tem derivada 0 e travaria o backpropagation
		return 1 / (1 + np.exp(-z))

	def _derivada_sigmoide(self, z: np.ndarray) -> np.ndarray:
		# sigma'(z) = sigma(z) * (1 - sigma(z)): reaproveita a própria sigmoide
		s = self._sigmoide(z)
		return s * (1 - s)

	# executa a rede neural inteira. Como só tem 1 camada oculta calcula a soma (Z) e a função de ativação (A) 2 vezes, 
	# para a camada oculta e para camada de saída
	# retorna o calculo bruto de cada camada e o resultado da função de ativação de cada camada. O ultimo é a probabilidade, não a categoria em si
	def _forward(self, X: np.ndarray):
		# guardamos Z1, A1 e Z2 porque o backward precisa deles
		Z1 = X @ self.W1 + self.b1
		A1 = self._sigmoide(Z1)
		Z2 = A1 @ self.W2 + self.b2
		y_pred = self._sigmoide(Z2)
		return Z1, A1, Z2, y_pred

	def _perda(self, y: np.ndarray, y_pred: np.ndarray) -> float:
		# entropia cruzada binária; o epsilon evita log(0) (-infinito, quebrando a conta) quando a sigmoide satura
		eps = 1e-12
		y_pred = np.clip(y_pred, eps, 1 - eps)
		return float(-np.mean(y * np.log(y_pred) + (1 - y) * np.log(1 - y_pred)))

	def _backpropagation(self, X: np.ndarray, y: np.ndarray, Z1, A1, y_pred):
		num_dados = X.shape[0]
		# erro da saída: nas funções de perda mais comuns de a derivada fica y_pred - y_real
		delta2 = y_pred - y
		delta_W2 = A1.T @ delta2 / num_dados # saída daquela camada * erro_restante / num_dados
		delta_bias2 = delta2.sum(axis=0, keepdims=True) / num_dados
		# o erro volta pela camada de saída (W2.T) e é escalonado pela derivada da ativação oculta
		delta1 = (delta2 @ self.W2.T) * self._derivada_sigmoide(Z1)
		delta_W1 = X.T @ delta1 / num_dados
		delta_bias1 = delta1.sum(axis=0, keepdims=True) / num_dados
		return delta_W1, delta_bias1, delta_W2, delta_bias2

	def fit(self, X: np.ndarray, y: np.ndarray, epocas: int, PRINT_PERDA: int) -> None:
		n_entradas = X.shape[1]
		# pesos pequenos e ALEATÓRIOS: se fossem todos zero (ou iguais), os neurônios ocultos
		# receberiam o mesmo gradiente e ficariam idênticos para sempre (simetria)
		self.W1 = self.rng.normal(0, 0.5, size=(n_entradas, self.neuronios_ocultos))
		self.W2 = self.rng.normal(0, 0.5, size=(self.neuronios_ocultos, 1))
		# os bias podem começar em zero: a simetria já foi quebrada pelos pesos
		self.b1 = np.zeros((1, self.neuronios_ocultos))
		self.b2 = np.zeros((1, 1))
		self.perdas_por_epoca = []

		for epoca in range(epocas):
			Z1, A1, Z2, y_pred = self._forward(X) # executa todas as camadas da rede neural
			perda = self._perda(y, y_pred) # calcula a função de perda  apenas para salvar o historico de sua mudança e plotar depois. Não é usado na logica
			self.perdas_por_epoca.append(perda)

			delta_W1, delta_bias1, delta_W2, delta_bias2 = self._backpropagation(X, y, Z1, A1, y_pred) # calcula o backpropagation de cada peso de cada camasa
			# gradiente descendente: um passo contra o gradiente
			self.W1 -= self.taxa_aprendizado * delta_W1
			self.b1 -= self.taxa_aprendizado * delta_bias1
			self.W2 -= self.taxa_aprendizado * delta_W2
			self.b2 -= self.taxa_aprendizado * delta_bias2

			if epoca % PRINT_PERDA == 0 or epoca == epocas - 1:
				print(f"Época {epoca:5d} | perda = {perda:.4f}")

	def predict_proba(self, X: np.ndarray) -> np.ndarray:
		return self._forward(X)[3]

	# limiar 0.5: probabilidade da classe 1 maior que 50% vira classe 1
	def predict(self, X: np.ndarray) -> np.ndarray:
		return (self.predict_proba(X) >= 0.5).astype(int)


# dados de treino para o XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([[0], [1], [1], [0]], dtype=float)

mlp = MLP(NEURONIOS_OCULTOS, TAXA_APRENDIZADO, SEED)
mlp.fit(X, y, EPOCAS, PRINT_PERDA)

print("\nPrevisões finais:")
probabilidadess = mlp.predict_proba(X)
categorias = mlp.predict(X)
for xi, yi, prob, cat in zip(X, y, probabilidadess, categorias):
	print(f"  entrada {xi} | esperado {int(yi[0])} | probabilidade {prob[0]:.4f} | classe {cat[0]}")

acertos = int((categorias == y).sum())
print(f"\nAcertos: {acertos}/4 -> XOR resolvido? {acertos == 4}")
print("\nPesos aprendidos:")
print("W1 (entrada -> oculta):\n", mlp.W1)
print("b1:", mlp.b1)
print("W2 (oculta -> saída):\n", mlp.W2)
print("b2:", mlp.b2)

# --- Gráficos ---
# curva de perda: mostra o platô perto de ln(2) = 0.693 (rede chutando 50% para tudo) e a queda depois
plt.figure(figsize=(7, 4))
plt.plot(mlp.perdas_por_epoca, color="tab:blue")
plt.axhline(np.log(2), color="gray", linestyle=":", label="ln 2 (chute 50%)")
plt.title("XOR: perda (entropia cruzada) por época")
plt.xlabel("época")
plt.ylabel("perda")
plt.legend()
plt.tight_layout()
plt.show()

# mostra como a camada oculta distorce o espaço, permitindo criar uma linha reta que separe os dados do tipo 0 dos do tipo 1
# espaço oculto: onde os 4 pontos caem depois da camada oculta. Com 2 neurônios ocultos
# o espaço (a1_1, a1_2) é 2D e a camada de saída vira uma reta simples nele
A1 = mlp._forward(X)[1]
plt.figure(figsize=(6, 5.5))
plt.scatter(A1[y[:, 0] == 0, 0], A1[y[:, 0] == 0, 1], c="tab:blue", s=120, edgecolors="k", label="classe 0")
plt.scatter(A1[y[:, 0] == 1, 0], A1[y[:, 0] == 1, 1], c="tab:red", s=120, edgecolors="k", label="classe 1")
# a saída decide por W2[0]*a1 + W2[1]*a2 + b2 = 0 (probabilidade 0.5)
a1_vals = np.linspace(-0.1, 1.1, 100)
a2_vals = -(mlp.W2[0, 0] * a1_vals + mlp.b2[0, 0]) / mlp.W2[1, 0]
plt.plot(a1_vals, a2_vals, "k--", label="reta da camada de saída")
plt.xlim(-0.1, 1.1)
plt.ylim(-0.1, 1.1)
plt.title("XOR: espaço da camada oculta (linearmente separável)")
plt.xlabel("a1_1 (neurônio oculto 1)")
plt.ylabel("a1_2 (neurônio oculto 2)")
plt.legend()
plt.tight_layout()
plt.show()
