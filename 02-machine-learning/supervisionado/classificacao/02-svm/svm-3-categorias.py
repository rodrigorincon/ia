import numpy as np
import matplotlib.pyplot as plt
from sklearn import datasets
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.svm import SVC
from sklearn.metrics import classification_report, accuracy_score
import pandas as pd

# Carregando a base de dados (possui 3 classes de flores)
dados = datasets.load_iris()
X = dados.data  # Características (comprimento/largura da pétala/sépala)
y = dados.target  # Classes (0, 1 ou 2)

print(X, '\n\n')
print(y)

# Padronizando as características (essencial para o bom desempenho do SVM)
normalizador = StandardScaler()
X = normalizador.fit_transform(X)

# Dividindo os dados entre Treino garantindo a proporção nos grupos
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.2, random_state=42, stratify=y)

# Executa o SVM
# kernel por padrão é RBF. Os valores possiveis são linear, poly, rbf e sigmoid
modelo_svm = SVC(kernel='linear', random_state=42)
modelo_svm.fit(X_treino, y_treino)

# Fazendo previsões com a base de teste
previsoes = modelo_svm.predict(X_teste)

# Exibindo os resultados de desempenho
print("--- Resultados do Modelo SVM ---")
print(f"Acurácia Geral: {accuracy_score(y_teste, previsoes):.2%}\n")
print("Relatório de Classificação Detalhado:")
print(classification_report(y_teste, previsoes, target_names=dados.target_names))


# Gráfico dos dados e linhas de divisão do SVM
X2 = X_treino[:, :2]
classes = dados.target_names
cores = {'setosa': 'blue', 'versicolor': 'green', 'virginica': 'red'}

# adiciona os dados
for classe_idx, nome in enumerate(classes):
    mask = y_treino == classe_idx
    plt.scatter(X2[mask, 0], X2[mask, 1], color=cores[nome], edgecolors='k', label=nome, alpha=0.8)

# adiciona as retas
x_min, x_max = X2[:, 0].min() - 0.5, X2[:, 0].max() + 0.5
x_reta = np.linspace(x_min, x_max, 300)
for idx, nome in enumerate(classes):
    w = modelo_svm.coef_[idx]
    b = modelo_svm.intercept_[idx]
    if np.isclose(w[1], 0):
        y_reta = np.full_like(x_reta, -b / w[0])
    else:
        y_reta = -(w[0] * x_reta + b) / w[1]
    plt.plot(x_reta, y_reta, linestyle='--', linewidth=2, label=f'reta {nome}')

plt.legend(loc='lower right')
plt.show()

# Previsão para um novo exemplo
novo_dado = np.array([[6, 3.1, 5.1, 1.8]])
novo_dado_esc = normalizador.transform(novo_dado)
predicao = modelo_svm.predict(novo_dado_esc)[0]
print(f"\nPrevisão para {novo_dado}: {dados.target_names[predicao]} (classe {predicao})")

novo_dado = np.array([[5.1, 3.6, 1.3, 0.3]])
novo_dado_esc = normalizador.transform(novo_dado)
predicao = modelo_svm.predict(novo_dado_esc)[0]
print(f"\nPrevisão para {novo_dado}: {dados.target_names[predicao]} (classe {predicao})")

