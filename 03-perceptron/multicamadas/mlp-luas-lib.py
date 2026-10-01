import matplotlib.pyplot as plt
import numpy as np
from sklearn.datasets import make_moons
from sklearn.model_selection import train_test_split
from sklearn.neural_network import MLPClassifier

SEED = 42
NEURONIOS_OCULTOS = 8
EPOCAS = 2000
TAMANHO_BATCH = 32
TAXA_APRENDIZADO = 0.05 # taxa de aprendizado inicial do adam

X, y = make_moons(n_samples=300, noise=0.2, random_state=SEED)
X_treino, X_teste, y_treino, y_teste = train_test_split(X, y, test_size=0.3, random_state=SEED)

mlp = MLPClassifier(hidden_layer_sizes=(NEURONIOS_OCULTOS,), activation="logistic", solver="adam", learning_rate_init=TAXA_APRENDIZADO,
										batch_size=TAMANHO_BATCH, max_iter=EPOCAS, n_iter_no_change=100, random_state=SEED)
mlp.fit(X_treino, y_treino)

acuracia_treino = mlp.score(X_treino, y_treino)
acuracia_teste = mlp.score(X_teste, y_teste)
print(f"Épocas executadas: {mlp.n_iter_}")
print(f"Perda final no treino: {mlp.loss_curve_[-1]:.4f}")
print(f"Acurácia de treino: {acuracia_treino:.4f} ({len(X_treino)} pontos)")
print(f"Acurácia de teste:  {acuracia_teste:.4f} ({len(X_teste)} pontos)")

# --- Gráfico: fronteira de decisão na tela ---
margem = 0.5
xx, yy = np.meshgrid(
	np.linspace(X[:, 0].min() - margem, X[:, 0].max() + margem, 300),
	np.linspace(X[:, 1].min() - margem, X[:, 1].max() + margem, 300),
)
prob_grade = mlp.predict_proba(np.c_[xx.ravel(), yy.ravel()])[:, 1].reshape(xx.shape)

plt.figure(figsize=(7.5, 6))
cs = plt.contourf(xx, yy, prob_grade, levels=np.linspace(0, 1, 11), cmap="RdBu_r", alpha=0.6)
plt.contour(xx, yy, prob_grade, levels=[0.5], colors="k", linewidths=2)
plt.colorbar(cs, label="probabilidade da classe 1")
for classe, cor in [(0, "tab:blue"), (1, "tab:red")]:
	plt.scatter(X_treino[y_treino == classe, 0], X_treino[y_treino == classe, 1],
		c=cor, marker="o", edgecolors="k", label=f"treino classe {classe}")
	plt.scatter(X_teste[y_teste == classe, 0], X_teste[y_teste == classe, 1],
		c=cor, marker="^", s=80, edgecolors="k", label=f"teste classe {classe}")
plt.title(f"Luas (sklearn): fronteira de decisão (teste: {acuracia_teste:.1%})")
plt.xlabel("x1")
plt.ylabel("x2")
plt.legend(loc="upper right", fontsize=8)
plt.tight_layout()
plt.show()
