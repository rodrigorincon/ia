from sklearn.cluster import KMeans
from sklearn.metrics import silhouette_score, calinski_harabasz_score, davies_bouldin_score
from sklearn.datasets import make_blobs

# Criando dados de exemplo
X, _ = make_blobs(n_samples=2000, centers=8, cluster_std=0.90, random_state=42)

# guardam os resultados de cada teste
silhuetas = []
calinski_scores = []
davies_scores = []

# Testando valores de k de 1 a 10
k_valores = range(1, 11)
for k in k_valores:
  kmeans = KMeans(n_clusters=k, n_init=10, random_state=42)
  kmeans.fit(X)
  # caso só haja 1 grupo (todo o dataset foi colocado num grupo só) a função de silhueta quebra, então colocamos ao inves de executar consideramos None
  if( len(set(kmeans.labels_)) == 1):
    silhuetas.append(None)
    continue
  # indice Calinski-Harabasz
  ch_score = calinski_harabasz_score(X, kmeans.labels_)
  calinski_scores.append(ch_score)
  # indice Davies-Bouldin
  db_score = davies_bouldin_score(X, kmeans.labels_)
  davies_scores.append(db_score)
  # coeficiente de silhueta
  silhueta_score = silhouette_score(X, kmeans.labels_) # ja retorna o coeficiente médio do dataset
  silhuetas.append(silhueta_score)

###### PEGA O MELHOR RESULTADO DA SILHUETA ######
print(f'Coeficiente de Silhueta para cada K: {silhuetas}\n')
silhueta_idx = max((val, i) for i, val in enumerate(silhuetas) if val is not None)[1]
print(f'K com maior coeficiente: {k_valores[silhueta_idx]}')

###### PEGA O MELHOR RESULTADO DO CALINSKI-HARABASZ ######
print(f'\n------\nCoeficiente de Calinski-Harabasz para cada K: {calinski_scores}\n')
calinski_idx = max((val, i) for i, val in enumerate(calinski_scores) if val is not None)[1]
print(f'K com maior coeficiente: {k_valores[calinski_idx]}')

###### PEGA O MELHOR RESULTADO DO DAVIES-BOULDIN ######
print(f'\n------\nCoeficiente de Davies-Bouldin para cada K: {davies_scores}')
davies_idx = min((val, i) for i, val in enumerate(davies_scores) if val is not None)[1]
print(f'K com menor coeficiente: {k_valores[davies_idx]}')
