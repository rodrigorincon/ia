import matplotlib.pyplot as plt
import numpy as np

# Classificador SVM sem kernel, Regularização C e margem rígida (hard margin)
class SVMManual:
  C: float
  w: np.ndarray
  b: float
  tx_aprendizado: float
  max_iters: int

  def __init__(self, taxa_aprendizado=0.001, C=1.0, max_iters=1000):
    self.tx_aprendizado = taxa_aprendizado
    self.C = C
    self.max_iters = max_iters
    self.w = None
    self.b = None

  def fit(self, X, y):
    n_features = X.shape[1]

    # define os pesos iniciais como 0 (incluindo intercepto)
    self.w = np.zeros(n_features)
    self.b = 0.0

    for _ in range(self.max_iters):
      # Loop de treinamento (SGD)
      for idx, x_i in enumerate(X):
        # equacao do hinge loss: 1 - y * f(x) e f(x) = w * x + b
        fx = np.dot(x_i, self.w) - self.b
        hinge_loss = 1 - y[idx] * fx
        
        # Condição da margem rígida
        if(hinge_loss <= 0):
          # Classificado fora da margem
          # derivada da função de perda caso não haja violação da margem: w (apenas aplica a regularização)
          # a derivada do intercepto é 0, então não há atualização para b

          # equacao da atualizacao de pesos do gradiente: w_novo = w_antigo - taxa_aprendizado * derivada_do_svm
          # equação do SVM = 0.5 * ||w||^2 + C * funcao_custo
          # derivada: 2 * 0.5 * ||w|| + C * w = ||w|| + Cw. Dividindo por C fica: w/C + w
          # equacao margem = 2/||w||
          
          #derivada_svm = (1 + self.C) * self.w
          derivada_svm = 2 * 1 / self.C * self.w

          self.w = self.w - self.tx_aprendizado * derivada_svm
        else:
          # Classificado dentro da margem ou classificado incorretamente
          # derivada da função de perda caso haja violação da margem: w - C * y * x
          # derivada do intercepto é -C * y, então atualizamos b também
          
          # equacao da atualizacao de pesos do gradiente: w_novo = w_antigo - taxa_aprendizado * derivada_do_svm
          # equação do SVM = 0.5 * ||w||^2 + C * funcao_custo
          # derivada: 2 * 0.5 * ||w|| + C * (Cyx) = w + Cyx. Dividindo tudo por C fica: 2w/C + yx
          
          yx = np.dot(x_i, y[idx])
          derivada_svm = 2/self.C * self.w - yx
          self.w = self.w - self.tx_aprendizado * derivada_svm

          # derivada do SVM em relação ao intercepto: 0 + C * (-y) = -Cy
          
          #derivada_svm = -self.C * y[idx]
          derivada_svm = y[idx]
          self.b = self.b - self.tx_aprendizado * derivada_svm

  def predict(self, X):
    approx = np.dot(X, self.w) - self.b
    return np.sign(approx) # se tiver acima da reta retorna 1, senão retorna -1


# Criando nossos dados
# 2 classes: -1 e 1
X_treino = np.array(
    [[1, 2], [2, 3], [3, 3], [2, 1], [3, 2], [7, 8], [8, 9], [7, 6], [9, 7]]
)
ytreino = np.array([-1, -1, -1, -1, -1, 1, 1, 1, 1])

# Executa o SVM que usa gradiente descendente estocástico (SGD) para otimizar os pesos
# sem kernel, regularização C e margem rígida (hard margin)
modelo = SVMManual(taxa_aprendizado=0.001, C=10.0, max_iters=1000) # taxa_aprendizado é usado no para o gradiente descendente.
modelo.fit(X_treino, ytreino) # SVM usando Gradiente Descendente Estocástico (SGD) por debaixo dos panos
print(f'Reta divisória: {modelo.w[0]:.2f}x1 + {modelo.w[1]:.2f}x2 + {modelo.b:.2f}')

# mostra os dados no grafico, cada categoria com uma cor
plt.scatter(X_treino[ytreino == -1, 0], X_treino[ytreino == -1, 1], color='blue', edgecolors='k', label='azul = -1')
plt.scatter(X_treino[ytreino == 1, 0], X_treino[ytreino == 1, 1], color='red', edgecolors='k', label='vermelho = 1')
plt.plot(X_treino[:, 0], (-modelo.w[0] * X_treino[:, 0] + modelo.b) / modelo.w[1], color='green', label='Reta divisória')
plt.legend(loc='lower right')
plt.show()

# Testando o modelo com novos dados
X_teste = np.array([1.5, 1.5])
predicao = modelo.predict(X_teste)
print(f"Predições para {X_teste}: {predicao}")

X_teste = np.array([8, 8])
predicao = modelo.predict(X_teste)
print(f"Predições para {X_teste}: {predicao}")

