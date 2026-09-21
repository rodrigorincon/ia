import numpy as np
import pandas as pd
import matplotlib.pyplot as plt
from scipy.stats import norm, shapiro
from sklearn.datasets import make_classification
from sklearn.model_selection import train_test_split
from sklearn.metrics import accuracy_score

class NaiveBayesManual:

  # calcula a media, variancia e prior de cada categoria Y
  # prior = proporção da categoria no conjunto
  # ASSUMIMOS QUE OS DADOS TEM DISTRIBUIÇÃO NORMAL, POR ISSO ARMAZENAMOS A MEDIA E VARIANCIA DE CADA CATEGORIA Y
  def fit(self, X, y):
    self.classes = np.unique(y)
    num_total_dados = X.shape[0]
    # inicializa dicionários que descrevem cada categoria
    self.means = {}
    self.variances = {}
    self.priors = {}

    # calcula media, variancia e prior de cada categoria Y
    for categ in self.classes:
      # Pega só os X da categoria analisada
      X_cat = X[y == categ]
      num_dados_dessa_categoria = X_cat.shape[0]
      
      self.means[categ] = np.mean(X_cat, axis=0)
      self.variances[categ] = np.var(X_cat, axis=0) + 1e-9  # evita divisão por zero
      self.priors[categ] = num_dados_dessa_categoria / float(num_total_dados)

  # chama o predict para cada variável x
  def predict(self, X):
    return np.array([self._predict_single(x) for x in X])

  # prevê o Y de cada X. Para isso calcula a probabilidade de X ser de cada categoria Y e fica com a maior
  # log(P(y)) + SUM log( P(Xi|y) )
  # P(y) = prior  P(Xi|y) = verossimilhança para a curva normal
  def _predict_single(self, x):
    posteriors = [] # array de tuplas, onde o 1º valor é a probabilidade e o 2º é a classe

    for c in self.classes:
      prior = np.log(self.priors[c])
      
      # calcula as log-verossimilhanças e as soma (P(X_i|y))
      likelihoods = self._calculate_likelihood(c, x)
      soma_log_verossimilhancas = np.sum(np.log(likelihoods))
      
      # Posterior proportional value
      posterior = prior + soma_log_verossimilhancas
      posteriors.append((posterior, c))
      
    # retorna categoria com a maior probabilidade
    return max(posteriors, key=lambda item: item[0])[1]

  # verossimilhança: calcula a prob do dado x se encaixar na distribuição com certa média e variância
  # usa a media e variancia calculada no fit (assumimos uma curva normal) 
  # e ve o quanto cada x de teste se encaixa na curva feita pelos dados de treino
  def _calculate_likelihood(self, class_idx, x):
    mean = self.means[class_idx]
    var = self.variances[class_idx]

    return norm.pdf(x, loc=mean, scale=np.sqrt(var))

# cria um conjunto de dados aleatorios com 200 dados e 4 variaveis independentes (X) e 2 categorias (Y)
X, y = make_classification(n_samples=200, n_features=4, random_state=42)

# visualizando os dados
df = pd.DataFrame(X)
df['categoria'] = y
print(df.head(10))
print('Quantidade de categorias: ', df.categoria.value_counts())

X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.3, random_state=42)

#### --------------------------------------
# checa se cada uma das colunas dos dados de treino tem distribuição normal
num_colunas_X = X_train.shape[1]
fig, axes = plt.subplots(num_colunas_X, 1, figsize=(8, 3 * num_colunas_X))

for i in range(num_colunas_X):
  xi = X_train[:, i] # X_train é uma matriz, cada dado é uma linha e as colunas são as variáveis independentes
  media_coluna = xi.mean()
  desvio_coluna = xi.std(ddof=0)

  # plota o histograma de cada coluna com uma curva normal aproximada por cima
  ax = axes[i]
  ax.hist(xi, bins=20, density=True, alpha=0.6, color='C0')
  xs = np.linspace(xi.min(), xi.max(), 200)
  ax.plot(xs, norm.pdf(xs, loc=media_coluna, scale=desvio_coluna), 'k--', label='Curva normal (aprox)')

  # FAZ O TESTE DE SHAPIRO-WILK PARA ESSA COLUNA
  stat, pval = shapiro(xi)
  if(pval < 0.05):
    print(f"Coluna {i} NÃO SEGUE distribuição normal. W={stat:.4f} e p-valor={pval:.4f}")
    texto_grafico = 'REPROVADO'
  else:
    texto_grafico = 'APROVADO'

  ax.set_title(f'Coluna {i} - Shapiro p={pval:.4f} {texto_grafico}')
  ax.legend()

plt.tight_layout()
plt.show()

#### --------------------------------------
# cria meu objeto bayes
nb_manual = NaiveBayesManual()
nb_manual.fit(X_train, y_train)

# prevê valores e checa acuracia
y_pred = nb_manual.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acuracia do naive bayes: {(100 * accuracy):.2f}%")
