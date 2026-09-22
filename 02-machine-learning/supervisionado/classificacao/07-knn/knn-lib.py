import numpy as np
from sklearn.model_selection import train_test_split
from sklearn.preprocessing import StandardScaler
from sklearn.neighbors import KNeighborsClassifier, KNeighborsRegressor
from sklearn.metrics import accuracy_score, root_mean_squared_error

# ======================= KNN PARA CLASSIFICAÇÃO

# Base de dados: [Horas de Estudo, Faltas] -> Status (0: Reprovado, 1: Aprovado)
X = np.array([
  [2.0, 8.0],
  [8.0, 1.0],
  [7.0, 3.0],
  [3.0, 6.0],
  [6.0, 2.0],
  [1.5, 9.0],
  [9.0, 0.0],
  [5.5, 4.0]
])
y = np.array([0, 1, 1, 0, 1, 0, 1, 1])

# Dividindo os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Transformação das variáveis X (botar elas na mesma escala)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Instanciando o modelo de CLASSIFICAÇÃO com K=3 e métrica Euclidiana
knn_clf = KNeighborsClassifier(n_neighbors=3, metric='euclidean')
knn_clf.fit(X_train, y_train) # só memoriza os dados, mas ñ faz nenhum calculo com eles

# Previsão no conjunto de teste
y_pred = knn_clf.predict(X_test)
print("--- RESULTADOS DA CLASSIFICAÇÃO ---")
print(f"Acurácia Geral: {accuracy_score(y_test, y_pred):.2%}")

# Previsão para um novo aluno específico: [6.0 horas de estudo, 3.0 faltas]
novo_aluno = np.array([[6.0, 3.0]])
novo_aluno = scaler.transform(novo_aluno)

pred_aluno = knn_clf.predict(novo_aluno)
prob_aluno = knn_clf.predict_proba(novo_aluno)
print(f"Classe prevista para o novo aluno (6h estudo, 3 faltas): {pred_aluno[0]} (1: Aprovado, 0: Reprovado)")
print(f"Probabilidade estimada [Reprovado, Aprovado]: {prob_aluno[0]} \n---------------------\n")

# ======================= KNN PARA REGRESSÃO

# Base de dados: [Área m², N° Quartos] -> Preço do Imóvel (R$)
X = np.array([
  [50.0, 1],
  [120.0, 3],
  [75.0, 2],
  [90.0, 2],
  [80.0, 2],
  [40.0, 1],
  [150.0, 4],
  [110.0, 3]
])
y = np.array([200000, 500000, 320000, 380000, 350000, 180000, 620000, 470000])

# Dividindo os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.25, random_state=42)

# Transformação das variáveis X (botar elas na mesma escala)
scaler = StandardScaler()
X_train = scaler.fit_transform(X_train)
X_test = scaler.transform(X_test)

# Instanciando o modelo de Regressão com K=3 e métrica Euclidiana
knn = KNeighborsRegressor(n_neighbors=3, metric='euclidean')
knn.fit(X_train, y_train)

# Previsão no conjunto de teste
y_pred = knn_clf.predict(X_test)
print(f"RMSE: {root_mean_squared_error(y_test, y_pred):.2%}")

# Previsão para um novo imóvel: [85.0 m², 2 quartos]
novo_imovel = np.array([[85, 2]])
novo_imovel = scaler.transform(novo_imovel)

preco_estimado = knn.predict(novo_imovel)

print("\n--- RESULTADOS DA REGRESSÃO ---")
print(f"Preço estimado para o novo imóvel (85m², 2 qts): R$ {preco_estimado[0]:,.2f}\n---------ssss")

# Descobrindo quais foram os 3 vizinhos mais próximos selecionados
distancias, indices = knn.kneighbors(novo_imovel)
print("Índices dos 3 vizinhos mais próximos no treino:", indices[0])
print("Distâncias dos 3 vizinhos mais próximos:", distancias[0])