import matplotlib.pyplot as plt
from matplotlib.patches import Ellipse
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.mixture import GaussianMixture
from sklearn.preprocessing import StandardScaler

# cria os dados de treino
X_raw, _ = make_blobs(n_samples=600, centers=3, cluster_std=0.80, random_state=42)
# Transformação linear para deformar os clusters em elipses alongadas
matriz_transformacao = [[0.6, -0.6], [-0.3, 0.8]]
X = np.dot(X_raw, matriz_transformacao)

# Padronização
scaler = StandardScaler()
X_scaled = scaler.fit_transform(X)

# n_components = K, init_params = como inicializar os valores (kmeans, kmeans++, random). n_init = quantas vezes executa o kmeans para inicializar
# covariance_type = 'full' (cada grupo tem sua própria matriz de covariância)
# valores para tipo de covariancia: 'full', 'tied', 'diag', 'spherical'
gmm = GaussianMixture(n_components=3, covariance_type='full', init_params='k-means++', n_init=10, random_state=42)
gmm.fit(X_scaled)

# Agrupamento Suave (Soft Clustering) -> Probabilidade de pertencer a CADA cluster
probabilidades = gmm.predict_proba(X_scaled)
print('Prob do potno 50 pertencer a cada grupo: ', probabilidades[49])

print('--- PARÂMETROS DO MODELO GMM ---')
print(f'Convergiu em {gmm.n_iter_} iterações do algoritmo EM')
print(f'BIC: {gmm.bic(X_scaled):.2f}')
print(f'AIC: {gmm.aic(X_scaled):.2f}')

for i in range(3):
	probs_formatadas = [f'{p:.4f}' for p in probabilidades[i]]
	print(f'Ponto {i+1} {X_scaled[i].round(2)} -> Probabilidades por Cluster: {probs_formatadas}')


# ajuda a desenhar o gráfico
def plot_elipse_covariancia(media, covariancia, ax, n_std=2.0, **kwargs):
	v, w = np.linalg.eigh(covariancia)
	v = 2.0 * np.sqrt(2.0) * np.sqrt(v)
	u = w[0] / np.linalg.norm(w[0])
	angulo = np.arctan2(u[1], u[0])
	angulo = 180.0 * angulo / np.pi

	elipse = Ellipse(
		xy=media,
		width=v[0] * (n_std / 2),
		height=v[1] * (n_std / 2),
		angle=angulo,
		**kwargs,
	)
	ax.add_patch(elipse)

# Usa o agrupamento Rígido só para pintar os dados no gráfico. Mostra o dado como sendo do grupo mais provável
labels = gmm.predict(X_scaled)

fig, ax = plt.subplots(figsize=(9, 6))
# Plot dos pontos de dados
sc = ax.scatter(X_scaled[:, 0], X_scaled[:, 1], c=labels, cmap='viridis', s=35, alpha=0.6, edgecolors='k', label='Pontos de Dados')
# Plot dos Centros (Médias) e Contornos das Gaussianas
medias = gmm.means_
covariancias = gmm.covariances_
for i in range(gmm.n_components):
	# Desenha o centro da gaussiana
	ax.scatter(medias[i, 0], medias[i, 1], c='red', marker='X', s=200, linewidths=2, edgecolors='black', zorder=10)
	# Desenha os contornos de confiança (1 e 2 desvios padrão)
	plot_elipse_covariancia(medias[i], covariancias[i], ax, n_std=1.0, color='red', alpha=0.4, linewidth=2)
	plot_elipse_covariancia( medias[i],covariancias[i],ax,n_std=2.0,color='red',alpha=0.2,linewidth=1,)

plt.title('GMM')
plt.xlabel('Atributo 1 (Padronizado)')
plt.ylabel('Atributo 2 (Padronizado)')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()