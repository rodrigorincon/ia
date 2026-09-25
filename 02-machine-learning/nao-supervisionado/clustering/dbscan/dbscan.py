import matplotlib.pyplot as plt
import numpy as np
from sklearn.cluster import DBSCAN
from sklearn.datasets import make_moons
from sklearn.neighbors import NearestNeighbors
from sklearn.preprocessing import StandardScaler

# criação de dados com formato de lua
X_moons, _ = make_moons(n_samples=400, noise=0.08, random_state=42)

# Adicionando outliers aleatórios (ruído)
np.random.seed(42)
outliers = np.random.uniform(low=-1.5, high=2.5, size=(25, 2))
X = np.vstack([X_moons, outliers])

# padronização dos dados
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

####### definindo os hiper-parametros ----------------------
# min_samples >= 2 * num variáveis X (dimensoes)
num_cols = X_scaled.shape[1]
min_samples = 2 * num_cols

# eps (raio R): Método do Gráfico k-Distance. Calcula a distância de cada ponto para o seu k-ésimo vizinho mais próximo
neighbors = NearestNeighbors(n_neighbors=min_samples)
neighbors_fit = neighbors.fit(X_scaled)
distances, _ = neighbors_fit.kneighbors(X_scaled) # retorna os vizinhos de 1 até n_neighbors
# Ordena as distâncias até o k-ésimo vizinho em ordem crescente
k_distances = np.sort(distances[:, min_samples - 1])

# Precisa olhar no gráfico para achar o ponto de inflexão. Já olhei o valor no gráfico e adicionei o valor no código
eps_ideal = 0.25 # cotovelo por volta do vizinho 400
plt.plot(list(range(1, len(k_distances) + 1)), k_distances, marker='o')
plt.xlabel('Vizinho (k)')
plt.ylabel('Distância')
plt.title('Método do Cotovelo para definir o valor de R')
plt.show()
print(f'Numero mínimo de pontos na vizinhança: {min_samples}')
print(f'Raio ideal: {eps_ideal}')

####### executando DBSCAN ----------------------
# eps: Raio da vizinhança (R), min_samples: Quantidade mínima de pontos no raio para que ele seja um núcleo
# algorithm: otimização para bases imensas (ball_tree, kd_tree ou auto), leaf_size: param usado pelo ball_tree, kd_tree
dbscan = DBSCAN(eps=eps_ideal, min_samples=min_samples, metric='euclidean', algorithm='ball_tree', leaf_size=30)
labels = dbscan.fit_predict(X_scaled)

# conta quantos dados pertencentem a algum grupo e quantos são outlier (-1)
num_ruidos = list(labels).count(-1)
num_grupos = len(set(labels)) - (1 if -1 in labels else 0)

print('--- RESULTADOS DO DBSCAN ---')
print(f'Número de grupos identificados: {num_grupos}')
print(f'Número de pontos de Ruído/Outliers (-1): {num_ruidos}')
print(f'Quantidade de Pontos Centrais (Nucleos): {len(dbscan.core_sample_indices_)}')

plt.figure(figsize=(9, 6))

# Máscara booleana para separar ruído, nucleo e borda
mascara_ruido = labels == -1
mascara_core = np.zeros_like(labels, dtype=bool)
mascara_core[dbscan.core_sample_indices_] = True

# Plot dos pontos pertencentes aos Clusters
plt.scatter(X_scaled[~mascara_ruido, 0], X_scaled[~mascara_ruido, 1], c=labels[~mascara_ruido], cmap='tab10', s=40, alpha=0.8, 
            edgecolors='k', label='Clusters Encontrados')
# Destaque para os Pontos de Ruído (-1)
plt.scatter( X_scaled[mascara_ruido, 0],X_scaled[mascara_ruido, 1],c='black',marker='x',s=70,linewidths=2,label='Ruído / Outliers (-1)')
plt.title('DBSCAN')
plt.xlabel('Atributo 1 (Padronizado)')
plt.ylabel('Atributo 2 (Padronizado)')
plt.legend()
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()