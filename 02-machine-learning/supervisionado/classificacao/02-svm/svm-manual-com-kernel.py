import matplotlib.pyplot as plt
import numpy as np

# Classificador SVM com kernel linear, Regularização C e margem rígida (hard margin)
class SVMKernelManual:
  C: float
  kernel: np.ndarray
  alphas: np.ndarray
  support_vectors: np.ndarray
  support_labels: np.ndarray
  b: float
  tx_aprendizado: float
  max_iters: int
  
  def __init__(self, taxa_aprendizado=0.01, C=1.0, max_iters=200):
    self.tx_aprendizado = taxa_aprendizado
    self.C = C
    self.max_iters = max_iters
    self.alphas = None
    self.b = None
    self.support_vectors = None
    self.support_labels = None

  # Kernel linear: k(x1, x2) = x1 · x2
  def kernel(self, x1, x2):
    return np.dot(x1, x2)

  def fit(self, X, y):
    n_samples = X.shape[0]
    self.alphas = np.zeros(n_samples) # 1 alfa pra cada linha
    self.support_vectors = X.copy() # todos os pontos começam sendo vetores
    self.support_labels = y.copy()
    self.b = 0.0

    for _ in range(self.max_iters):
      # Loop de treinamento (SGD)
      for idx, x_i in enumerate(X):
        kernel_values = []
        # calculo do multiplicador de lagrange
        for x_j in self.support_vectors:
          kernel = self.kernel(x_i, x_j)
          kernel_values.append(kernel)
        score = self.b + np.sum(self.alphas * self.support_labels * kernel_values)

        if y[idx] * score < 1:
          self.alphas[idx] += self.tx_aprendizado * self.C
          self.b += self.tx_aprendizado * y[idx]
  
  def predict(self, x):
    score = self.b + np.sum( self.alphas * self.support_labels * np.array([self.kernel(x, x_j) for x_j in self.support_vectors]) )
    return np.sign(score)

  @property
  def w(self):
    # alfa * y * X
    return np.sum(self.alphas[:, None] * self.support_labels[:, None] * self.support_vectors, axis=0)


# Criando nossos dados
# 2 classes: -1 e 1
X_treino = np.array([
  [1.0, 2.0], [1.8, 2.4], [2.4, 2.8], [3.0, 3.5], [3.4, 4.1], [4.1, 4.4], [4.9, 4.9], [5.2, 5.8], 
  [6.0, 6.0], [7.0, 6.8], [2.8, 4.2], [3.7, 4.7], [4.2, 5.3], [5.1, 5.8], [6.3, 6.5], [7.3, 7.4]
])
ytreino = np.array([-1, -1, -1, -1, -1, 1, 1, 1, 1, 1, -1, 1, -1, 1, 1, -1])

modelo = SVMKernelManual(taxa_aprendizado=0.01, C=1.0, max_iters=200)
modelo.fit(X_treino, ytreino)
print(f'Reta divisória: {modelo.w[0]:.2f}x1 + {modelo.w[1]:.2f}x2 + {modelo.b:.2f}')

# Testando o modelo com novos pontos
X_novo = [1, 8]
predicao = modelo.predict(np.array([X_novo]))
print(f"Predição para {X_novo}: {predicao}")

X_novo = [5.5, 0]
predicao = modelo.predict(np.array([X_novo]))
print(f"Predição para {X_novo}: {predicao}")

X_novo = [7.0, 1]
predicao = modelo.predict(np.array([X_novo]))
print(f"Predição para {X_novo}: {predicao}")


# mostra os dados no grafico, cada categoria com uma cor
plt.figure(figsize=(7, 6))
plt.scatter(X_treino[ytreino == -1, 0], X_treino[ytreino == -1, 1], color='blue', edgecolors='k', label='azul = -1')
plt.scatter(X_treino[ytreino == 1, 0], X_treino[ytreino == 1, 1], color='red', edgecolors='k', label='vermelho = 1')

x_min, x_max = X_treino[:, 0].min() - 1, X_treino[:, 0].max() + 1
x_reta = np.linspace(x_min, x_max, 200)
y_reta = -(modelo.w[0] * x_reta + modelo.b) / modelo.w[1]

plt.plot(x_reta, y_reta, color='green', label='Reta divisória')
plt.legend(loc='lower right')
plt.show()
