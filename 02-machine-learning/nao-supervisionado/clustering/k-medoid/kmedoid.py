import matplotlib.pyplot as plt
from sklearn_extra.cluster import KMedoids
import numpy as np

# base de dados onde cada linha é um ponto
X = np.array([
	[1, 2],
	[1.5, 1.8],
	[0.8, 0.6],
	[8, 8],
	[8.5, 9],
	[9, 8.2]
])

kmedoids = KMedoids(n_clusters=2, random_state=42)
kmedoids.fit(X)

previsoes = kmedoids.labels_ # lista a qual grupo cada ponto foi definido
centroides = kmedoids.cluster_centers_ # lista os centroides de cada grupo

print("Retorno das previsoes: \n", previsoes)
print("Centroides encontrados:\n", centroides)

grupo1 = [X[i] for i in range(len(X)) if previsoes[i] == 0]
grupo2 = [X[i] for i in range(len(X)) if previsoes[i] == 1]
print('Pontos do grupo 1: ', grupo1)
print('Pontos do grupo 2: ', grupo2)

# Visualizando os dados e os centroides no gráfico
plt.scatter(X[:, 0], X[:, 1], c=previsoes, cmap='viridis', s=100)
plt.scatter(centroides[:, 0], centroides[:, 1], c='red', marker='X', s=200, label='Centroides')
plt.title('K-Medoid')
plt.legend()
plt.show()
