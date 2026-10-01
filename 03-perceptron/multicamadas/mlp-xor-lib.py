import matplotlib.pyplot as plt
import numpy as np
from sklearn.neural_network import MLPClassifier

SEED = 0
TAXA_APRENDIZADO = 1.0
EPOCAS = 10_000  # limite máximo; o treino pode parar antes ao convergir
NEURONIOS_OCULTOS = 2 # arquitetura 2-2-1

# dados de treino para o XOR
X = np.array([[0, 0], [0, 1], [1, 0], [1, 1]], dtype=float)
y = np.array([0, 1, 1, 0])

# activation = função de ativação (logistic - sigmoide, relu, identity, tanh)
# solver = função de otimização (lbfgs, sgd (gradiente descendente), adam (gradiente com otimizador adam))
# a taxa de aprendizado se chama init pq o Adam altera ela a cada iteração. No gradiente desc. normal ela é fixa
# momentum = usado só no gradiente descendente pra dar "inércia". Acelera a saída de platôs mas pode fazer passar reto em minimos curtos
# alpha = usado na regularização L2. 0 indica sem regularização
# como nosso conjunto de treino é 4, o batch_size usa todos os dados duma vez (sem mini-batch)
# tol = se a perda for menor que isso considera que ñ houve perda (nada mudou nessa epoca) 
# n_iter_no_change = se ficar esse numero de rodadas sem alterações (ou com alterações abaixo de tol) encerra
# 	obs: tol=1e-4 e n_iter=10 estava parando no plato inicial, antes da queda. Testar e plotar varias combinaçõe spra ver quando finalmente supera um plato
mlp = MLPClassifier(hidden_layer_sizes=(NEURONIOS_OCULTOS,), activation="logistic", solver="sgd", learning_rate_init=TAXA_APRENDIZADO,
										momentum=0, alpha=0, batch_size=4, max_iter=EPOCAS, tol=1e-6, n_iter_no_change=500, random_state=SEED)
mlp.fit(X, y)

print("Previsões finais:")
probs = mlp.predict_proba(X)[:, 1] # pega a segunda coluna de todas as linhas
classes = mlp.predict(X)
for xi, yi, p, c in zip(X, y, probs, classes):
	print(f"  entrada {xi} | esperado {yi} | probabilidade {p:.4f} | classe {c}")

acertos = int((classes == y).sum())
print(f"\nAcertos: {acertos}/4 -> XOR resolvido? {acertos == 4}")
print(f"Perda final: {mlp.loss_curve_[-1]:.4f} em {mlp.n_iter_} épocas")
print(f'Parou antes: {mlp.n_iter_ < EPOCAS}')

print("\nPesos aprendidos:")
print("W1:", mlp.coefs_[0])
print("Bias 1:", mlp.intercepts_[0])
print("W2:", mlp.coefs_[1])
print("Bias 2:", mlp.intercepts_[1])

# --- Gráficos ---
plt.figure(figsize=(7, 4))
# curva de perda. A propia classe do sklearn guarda a perda de cada iteração
plt.plot(mlp.loss_curve_, color="tab:blue")
plt.axhline(np.log(2), color="gray", linestyle=":", label="ln 2 (chute 50%)")
plt.title("XOR: perda (entropia cruzada) por época")
plt.xlabel("época")
plt.ylabel("perda")
plt.legend()
plt.tight_layout()
plt.show()
