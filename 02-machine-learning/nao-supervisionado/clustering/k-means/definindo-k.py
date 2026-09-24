import matplotlib.pyplot as plt
from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score
from sklearn.datasets import make_blobs

# Criando dados de exemplo
X, _ = make_blobs(n_samples=2000, centers=8, cluster_std=0.90, random_state=42)

############## MÉTODO DO COTOVELO ##############

# Testando valores de k de 1 a 10
inercia = []
k_valores = range(1, 11)

for k in k_valores:
  kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
  kmeans.fit(X)
  inercia.append(kmeans.inertia_)

# Plotando o gráfico do cotovelo
plt.plot(k_valores, inercia, marker='o')
plt.xlabel('Número de Clusters (k)')
plt.ylabel('Inércia (WCSS)')
plt.title('Método do Cotovelo')
plt.show() # o melhor valor será 3

############## COEFICIENTE DE SILHUETA ##############

# Testando valores de k de 1 a 10
silhuetas = []
k_valores = range(1, 11)

for k in k_valores:
  kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
  kmeans.fit(X)
  # caso só haja 1 grupo (todo o dataset foi colocado num grupo só) a função de silhueta quebra, então colocamos ao inves de executar consideramos -1
  if( len(set(kmeans.labels_)) == 1):
    silhuetas.append(-1)
    continue  
  score = silhouette_score(X, kmeans.labels_) # ja retorna o coeficiente médio do dataset
  silhuetas.append(score)

print(f'Coeficiente de Silhueta para cada K: {silhuetas}')

maior_silhueta = max(silhuetas)
silhueta_idx = silhuetas.index(maior_silhueta)
print(f'K com maior coeficiente: {k_valores[silhueta_idx]}')