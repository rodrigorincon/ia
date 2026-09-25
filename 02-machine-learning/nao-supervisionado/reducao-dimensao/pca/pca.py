import matplotlib.pyplot as plt
import numpy as np
import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.decomposition import PCA
from sklearn.preprocessing import StandardScaler

# carregamento dos dados
cancer = load_breast_cancer()
X = cancer.data
y = cancer.target
feature_names = cancer.feature_names
target_names = cancer.target_names
print(f'Numero original de colunas: ', X.shape[1]) # 30

# padronização dos dados (z-score)
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# aplicação do algoritmo
# n_components = k (número de colunas finais que terá) OU variancia explicada mínima (porcentagem minima de informação preservada)
# Se passar INT, será numero de colunas finais. Se quiser plotar gráfico coloque k=2 ou 3
# Se passar FLOAT, será variancia explicada mínima (ex: k = 0.8). Nesse caso precisa passar um param adicional, svd_solver='full'
k = 0.6
pca = PCA(n_components=k, svd_solver='full', random_state=42)
X_pca = pca.fit_transform(X_scaled)

# pega as variancias explicadas de cada coluna para analisar o quanto cada uma é explicativa e quantos % explicamos com esse numero
# lembrando que segundo a literatura o minimo deveria ser 80%
variancia_explicada = pca.explained_variance_ratio_
variancia_total = np.sum(variancia_explicada)

print('--- RESULTADOS DA REDUÇÃO DE DIMENSIONALIDADE (PCA) ---')
for i, pc in enumerate(variancia_explicada):
    print(f'Variância explicada pela CP{i}: {(100*pc):.2f}%')
print(f'Quantos porcento da variância dos dados orignais foram mantidos: {(100*variancia_total):.2f}%\n')


# Matriz de Cargas (Loadings): Mostra a contribuição de cada variável original em cada CP
df_loadings = pd.DataFrame(pca.components_, columns=feature_names)
print('--- MATRIZ DE CARGAS / PESOS (LOADINGS) ---')
print(df_loadings.round(3))


# visualização dos dados de 30 dimensões em 2
def plot_cancer_new_vars(X_pca, target_names):
	plt.figure(figsize=(9, 6))
	cores = ['navy', 'turquoise', 'darkorange']
	for i, color, target_name in zip(range(3), cores, target_names):
		plt.scatter(X_pca[y == i, 0], X_pca[y == i, 1], color=color, alpha=0.8, s=50, edgecolors='k', label=target_name)
	plt.title(f'PCA')
	plt.xlabel(f'Componente Principal 1 ({variancia_explicada[0] * 100:.1f}%)')
	plt.ylabel(f'Componente Principal 2 ({variancia_explicada[1] * 100:.1f}%)')
	plt.legend(loc='best')
	plt.grid(True, linestyle='--', alpha=0.5)
	plt.show()

if(k == 2): plot_cancer_new_vars(X_pca, target_names)