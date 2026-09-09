import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import tree
from sklearn.metrics import accuracy_score

TREE_LEAF = tree._tree.TREE_LEAF

def recalc_num_nodes(clf, current_node_id):
    if(current_node_id == TREE_LEAF): return 0

    left_node_id = clf.tree_.children_left[current_node_id]
    right_node_id = clf.tree_.children_right[current_node_id]

    num_nodes_left = recalc_num_nodes(clf, left_node_id)
    num_nodes_right = recalc_num_nodes(clf, right_node_id)

    return num_nodes_left + num_nodes_right + 1

# pega os dados para análise
data = load_iris()
iris = pd.DataFrame(data.data)
iris.columns = data.feature_names
iris['target'] = data.target

iris1 = iris.loc[iris.target.isin([1,2]),['petal length (cm)','petal width (cm)', 'target']]
X = iris1.drop('target', axis=1)
Y = iris1.target

# separa dados e, 3 grupos, treino, teste (final) e validação (pra poda)
# 20% teste, 20% poda e 60% treino
X_train_e_poda, X_test, y_train_e_poda, y_test = train_test_split(X, Y, test_size=0.2, random_state=42)
X_train, X_poda, y_train, y_poda = train_test_split(X_train_e_poda, y_train_e_poda, test_size=0.25, random_state=42)

# ---------------------- árvore de decisão SEM PODA ----------------------
clf = tree.DecisionTreeClassifier(random_state=42)
clf.fit(X_train, y_train)

print(f"Acurácia ANTES da poda (dados de poda): {accuracy_score(y_poda, clf.predict(X_poda)):.4f}")
print(f"Acurácia ANTES da poda (dados de Teste): {accuracy_score(y_test, clf.predict(X_test)):.4f}")
print(f"Número total de nós antes: {clf.tree_.node_count}\n")
print(f"Número total de nós antes (contados pela funcao criada): {recalc_num_nodes(clf, 0)}\n")

fig, ax = plt.subplots(figsize=(12,6))
tree.plot_tree(clf)
plt.show()

# ---------------------- árvore de decisão COM PODA DE ERRO REDUZIDO (checar se remover o nó afeta a precisão) ----------------------

# ele não é implementado nativamente, vc precisa cria-lo na mão
# função que executa a poda de erro reduzido
def reduced_error_pruning(clf, X_poda, y_poda):
    tree = clf.tree_
    
    def prune_node(node_id):
        # Se for um nó folha, não há o que podar abaixo dele
        if tree.children_left[node_id] == TREE_LEAF:
            return

        # Caminha de forma recursiva até a base da árvore (pós-ordem / bottom-up)
        prune_node(tree.children_left[node_id])
        prune_node(tree.children_right[node_id])

        # Guarda os ponteiros originais dos filhos caso precise reverter
        left_child = tree.children_left[node_id]
        right_child = tree.children_right[node_id]

        # Calcula a acurácia atual na validação antes de alterar este nó
        baseline_acc = accuracy_score(y_poda, clf.predict(X_poda))

        # "Simula" a poda: Transforma o nó atual em folha desconectando os filhos
        tree.children_left[node_id] = TREE_LEAF
        tree.children_right[node_id] = TREE_LEAF

        # Calcula a nova acurácia com o nó podado
        pruned_acc = accuracy_score(y_poda, clf.predict(X_poda))

        # Se a acurácia piorar, desfaz a poda (reconecta os filhos)
        if pruned_acc < baseline_acc:
            tree.children_left[node_id] = left_child
            tree.children_right[node_id] = right_child

    # Inicia a poda a partir do nó raiz (ID 0)
    prune_node(0)

# Executar a poda utilizando os dados de validação
reduced_error_pruning(clf, X_poda, y_poda)

print(f"Acurácia DEPOIS da poda (dados de poda): {accuracy_score(y_poda, clf.predict(X_poda)):.4f}")
print(f"Acurácia DEPOIS da poda (dados de Teste): {accuracy_score(y_test, clf.predict(X_test)):.4f}")
# o atributo clf.tree_.node_count NÃO É reescrito ao apagar os ponteiros, portanto tem de usar a função criada pra contar o novo numero de nós
print(f"Número total de nós após: {recalc_num_nodes(clf, 0)}\n")

fig, ax = plt.subplots(figsize=(12,6))
tree.plot_tree(clf)
plt.show()
