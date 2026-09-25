import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_blobs
from sklearn.preprocessing import StandardScaler
from sklearn.svm import OneClassSVM

# Dados de treino contendo APENAS observações normais (Inliers)
X_train, _ = make_blobs(n_samples=300, centers=1, cluster_std=0.80, random_state=42)

# Dados de teste: novos inliers + anomalias/outliers gerados aleatoriamente
np.random.seed(42)
X_test_inliers, _ = make_blobs(n_samples=50, centers=1, cluster_std=0.80, random_state=100)
X_test_outliers = np.random.uniform(low=-4, high=4, size=(30, 2))
X_test = np.vstack([X_test_inliers, X_test_outliers])

# padronização dos dados
scaler = StandardScaler()
X_train_scaled = scaler.fit_transform(X_train)
X_test_scaled = scaler.transform(X_test)

# executa o algoritmo
# nu = fração maxima de anomalias
# gamma='scale': Define a largura de banda do kernel RBF. (quão em cima dos dados passa a fronteira)
oc_svm = OneClassSVM(kernel='rbf', gamma='scale', nu=0.05)
oc_svm.fit(X_train_scaled)

# Predição nos dados de teste:
# Retorna  1 para INLIERS (observações normais)
# Retorna -1 para OUTLIERS (anomalias)
preds_test = oc_svm.predict(X_test_scaled)

n_inliers = np.sum(preds_test == 1)
n_outliers = np.sum(preds_test == -1)

print('--- RESULTADOS DA DETECÇÃO DE ANOMALIAS ---')
print(f'Total de amostras no conjunto de teste: {len(X_test)}')
print(f'Amostras Classificadas como Normais (1): {n_inliers}')
print(f'Amostras Classificadas como Anomalias (-1): {n_outliers}')

##### plotagem do gráfico

# pega os dados da fronteira para plotar
xx, yy = np.meshgrid(np.linspace(-3.5, 3.5, 500), np.linspace(-3.5, 3.5, 500))
Z = oc_svm.decision_function(np.c_[xx.ravel(), yy.ravel()])
Z = Z.reshape(xx.shape)

plt.figure(figsize=(9, 6))
# Plot do limite de decisão aprendida (Z = 0 é a fronteira exata)
plt.contourf(xx, yy, Z, levels=np.linspace(Z.min(), 0, 7), cmap=plt.cm.Blues_r, alpha=0.3)
plt.contour(xx, yy, Z, levels=[0], linewidths=2, colors='navy', linestyles='-')

# Plot dos dados de treino (Normais)
plt.scatter(X_train_scaled[:, 0], X_train_scaled[:, 1], c='white', s=30, edgecolors='k', label='Treino (Inliers)')
# Plot dos testes classificados como Inliers
plt.scatter(X_test_scaled[preds_test == 1, 0], X_test_scaled[preds_test == 1, 1], c='mediumseagreen', s=50, edgecolors='k', marker='o', 
            label='Teste: Predição Inlier (1)')
# Plot dos testes classificados como Outliers
plt.scatter(X_test_scaled[preds_test == -1, 0], X_test_scaled[preds_test == -1, 1], c='crimson', s=60, edgecolors='k', marker='x', 
            linewidths=2, label='Teste: Predição Outlier (-1)')
plt.title('Detecção de Anomalias com One-Class SVM (Kernel RBF)')
plt.xlabel('Atributo 1 (Padronizado)')
plt.ylabel('Atributo 2 (Padronizado)')
plt.legend(loc='upper right')
plt.grid(True, linestyle='--', alpha=0.5)
plt.show()