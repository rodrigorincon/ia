import numpy as np
from sklearn.preprocessing import StandardScaler
from collections import Counter

def distancia_euclidiana(ponto1, ponto2):
	ponto1 = np.asarray(ponto1, dtype=float)
	ponto2 = np.asarray(ponto2, dtype=float)
	soma_quadrados = np.sum((ponto1 - ponto2) ** 2)
	return np.sqrt(soma_quadrados)

def knn(X_treino, Y_treino, k, x_novo, modo):
	# Calcula a distância entre o novo ponto e TODOS os pontos do treino
	distancias = []
	for i, dado_treino in enumerate(X_treino):
		dist = distancia_euclidiana(x_novo, dado_treino)
		distancias.append( (dist, Y_treino[i]) ) # array de tuplas com a distancia até o ponto e a categoria desse ponto

	# Ordena as distâncias do menor para o maior
	distancias.sort(key=lambda item: item[0])

	# Seleciona os K vizinhos mais próximos e pega a categoria deles
	k_vizinhos = distancias[:k]
	rotulos_vizinhos = [ponto[1] for ponto in k_vizinhos]

	# Dá a resposta de acordo se é classificação ou regressão
	if modo == 'classificacao':
		contagem = Counter(rotulos_vizinhos) # retorna a categoria q mais aparece
		return contagem.most_common(1)[0][0]
	elif modo == 'regressao':
		return sum(rotulos_vizinhos) / k # retorna a media aritimética dos pontos

# ======================= KNN PARA CLASSIFICAÇÃO

# Dados de Treino: [Horas Estudo, Faltas] -> Y (0: Reprovado, 1: Aprovado)
X_treino = [
	[2.0, 8.0],
	[8.0, 1.0],
	[7.0, 3.0],
	[3.0, 6.0],
	[6.0, 2.0]
]
y_treino = [0, 1, 1, 0, 1]

# Novo Aluno para prever: [6.0 horas de estudo, 3.0 faltas]
X_teste = [6.0, 3.0]

# Padroniza as variáveis
scaler = StandardScaler()
X_treino = scaler.fit_transform(X_treino)
X_teste = scaler.transform([X_teste])[0]

# executa o knn
predicao = knn(X_treino, y_treino, 3, X_teste, 'classificacao')

print("--- KNN CLASSIFICAÇÃO ---")
print(f"Novo Aluno (6h estudo, 3 faltas) -> Classe Prevista: {predicao} (1: Aprovado, 0: Reprovado)")

# ======================= KNN PARA REGRESSÃO

# Dados de Treino: [Área m², N° Quartos] -> Preço R$
X_treino = [
    [1.0, 1.0],
    [4.0, 3.0],
    [2.0, 2.0],
    [3.0, 2.0],
    [2.5, 2.0]
]
y_treino = [200000, 500000, 320000, 380000, 350000]

# Novo Imóvel para estimar preço: [2.2 área, 2.0 quartos]
X_teste = [2.2, 2.0]

# Padroniza as variáveis
scaler = StandardScaler()
X_treino = scaler.fit_transform(X_treino)
X_teste = scaler.transform([X_teste])[0]

# executa o knn
predicao = knn(X_treino, y_treino, 3, X_teste, 'regressao')

print("\n--- REGRESSÃO MANUAL ---")
print(f"Novo Imóvel (2.2 área, 2 quartos) -> Preço Estimado: R$ {predicao:.2f}")