import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score

# pega os dados para análise
data = load_iris()
iris = pd.DataFrame(data.data)
iris.columns = data.feature_names
iris['target'] = data.target

X = iris.drop('target', axis=1)
Y = iris.target

# separa dados de teste e treino
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.2, random_state=42)

# ---------------------- EXECUTA A ÁRVORE DE DECISÃO ----------------------
clf = tree.DecisionTreeClassifier(random_state=42)
clf.fit(X_train, Y_train)
print(f"Acurácia: {accuracy_score(Y_test, clf.predict(X_test)):.4f}")

fig, ax = plt.subplots(figsize=(14,6))
tree.plot_tree(clf)
plt.show()
