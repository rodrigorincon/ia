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

iris1 = iris.loc[iris.target.isin([1,2]),['petal length (cm)','petal width (cm)', 'target']]
X = iris1.drop('target', axis=1)
Y = iris1.target

# separa dados de teste e treino
X_train, X_test, Y_train, Y_test = train_test_split(X, Y, test_size=0.33, random_state=42)

# ---------------------- EXECUTA A ÁRVORE DE DECISÃO ----------------------
clf = tree.DecisionTreeClassifier(random_state=42)
path = clf.cost_complexity_pruning_path(X_train, Y_train)
# Lista de valores potenciais para alfa
alfas = path.ccp_alphas
print('Lista de Potenciais Alfas Para nossa árvore: ', alfas)

# ---------------------- CRIA UMA NOVA ARVORE PODADA para cada alfa sugerido ----------------------
for alfa in alfas:
    clf_podado = tree.DecisionTreeClassifier(random_state=42, ccp_alpha=alfa)
    clf_podado.fit(X_train, Y_train)
    acuracia = accuracy_score(Y_test, clf_podado.predict(X_test))

    fig, ax = plt.subplots()
    tree.plot_tree(clf_podado)
    plt.title(f'Arvore podada com alfa {alfa:.4f}. Acuracia = {acuracia:.4f}')
    plt.show()


