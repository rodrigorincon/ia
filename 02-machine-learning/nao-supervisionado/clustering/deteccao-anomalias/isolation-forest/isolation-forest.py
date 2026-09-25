import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.ensemble import IsolationForest

# Base principal de dados normais (Inliers)
X_inliers, _ = make_blobs(n_samples=400, centers=2, cluster_std=0.70, random_state=42)
# Adiciona anomalias aleatórias (Outliers)
np.random.seed(42)
X_outliers = np.random.uniform(low=-5, high=5, size=(40, 2))
X = np.vstack([X_inliers, X_outliers])

# Roda o algoritmo
# - n_estimators=100: Número de árvores.
# - contamination=0.09: Proporção esperada de anomalias no dataset.
iso_forest = IsolationForest(n_estimators=100, contamination=0.09, random_state=42)
iso_forest.fit(X)
predicoes = iso_forest.predict(X) # 1 = Dado Normal, -1 = Outlier

# Score de anomalia: Valores quanto mais negativos, maior a probabilidade de ser anomalia
scores = iso_forest.decision_function(X)
print(scores) # enquanto predict retorna a categoria dura (normal ou outlier, 1 ou -1), decision_function retorna a probabilidade
# predict dá a resposta final e decision_function dá a resposta da função S

# informações sobre os dados
n_inliers = np.sum(predicoes == 1)
n_outliers = np.sum(predicoes == -1)
print('--- RESULTADOS DO ISOLATION FOREST ---')
print(f'Total de Amostras Avaliadas: {len(X)}')
print(f'Classificados como Inliers (1): {n_inliers}')
print(f'Classificados como Outliers (-1): {n_outliers}')

# Exemplo de scores para os 3 pontos mais anômalos
indices_mais_anomalos = np.argsort(scores)[:3]
print('\nTop 3 Pontos com Maior Grau de Anomalia:')
for idx in indices_mais_anomalos:
	print(f'  Ponto {X[idx].round(2)} -> S: {scores[idx]:.4f} (Predição: {predicoes[idx]})')

# gráfico
xx, yy = np.meshgrid(np.linspace(-6, 6, 500), np.linspace(-6, 6, 500))
Z = iso_forest.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(9, 6))
# Mapa de contorno dos scores de anomalia
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), Z.max(), 20), cmap=plt.cm.YlOrRd_r)
plt.colorbar(label='Score de Anomalia (Valores menores = Mais anômalo)')
# Desenha a linha limite exata (Fronteira onde score = 0)
plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='black', linestyles='--')
# Plot dos pontos classificados como Inliers
plt.scatter(X[predicoes == 1, 0], X[predicoes == 1, 1], c='white', s=35, edgecolors='k', label='Inliers (Normais)')
# Plot dos pontos classificados como Outliers
plt.scatter(X[predicoes == -1, 0], X[predicoes == -1, 1], c='crimson', s=60, edgecolors='k', marker='x', linewidths=2, label='Outliers (Anomalias)')
plt.title('Detecção de Anomalias com Isolation Forest')
plt.xlabel('Atributo 1')
plt.ylabel('Atributo 2')
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.3)
plt.show()
