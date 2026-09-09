import pandas as pd
from sklearn.datasets import load_iris
import matplotlib.pyplot as plt
from sklearn.model_selection import train_test_split
from sklearn import tree

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
# criterion é a função de perda. Pode ser gini (padrão), entropy ou log_loss
# max_depth define um limite pra tamanho da árvore (por default não define limite). Ajuda a evitar overfitting aceitando todos os nós dessa altura como nós com ruído aceitável
# min_samples_leaf se um nó tiver essa quantidade de dados ñ irá se subdividir mais e será um nó. É um critério de parada e ajuda a evitar overfitting por definir um limite aceitável de ruído
clf = tree.DecisionTreeClassifier(criterion='gini', random_state=42)
clf.fit(X_train, Y_train)

fig, ax = plt.subplots(figsize=(12,6))
tree.plot_tree(clf)
plt.show()

# lendo os dados do nó raiz
atributo_usado = clf.tree_.feature[0]
limite_divisao = clf.tree_.threshold[0]
num_dados = clf.tree_.n_node_samples[0]
total_nodes = clf.tree_.node_count

print('total de nodes da arvore: ',total_nodes)
print('NO RAIZ:')
print('Separou na variavel', atributo_usado, 'No valor', limite_divisao, 'num de dados usados nesse node', num_dados)

# node folha retorna feature = threshold = -2, então para ignorar nós folha basta checar se feature < 0
# imprimindo os nodes folha para se ter uma ideia
for i in range(total_nodes):
  if(clf.tree_.feature[i] >= 0): continue
  atributo_usado = clf.tree_.feature[i]
  limite_divisao = clf.tree_.threshold[i]
  num_dados = clf.tree_.n_node_samples[i]
  print('Node folha: Variável usada:', atributo_usado, 'valor da divisão valor: ', limite_divisao, 'num de dados usados nesse node', num_dados)

# ---------------------- IMPRINDO GRÁFICO DAS ESCOLHAS DOS PONTOS DE CORTE (lembrando que esse gráfico só é possível setiver apenas 2 vars X)
fig, ax = plt.subplots()
ax.scatter(X_train['petal length (cm)'], X_train['petal width (cm)'], c=Y_train)

x_min, x_max = plt.xlim()
y_min, y_max = plt.ylim()

horizontal_lim1 = horizontal_lim2 = y_min
vertical_lim1 = vertical_lim2 = x_min
for node_idx in range(clf.tree_.node_count):
    # ignora nos folha
    if(clf.tree_.feature[node_idx] < 0): continue
    horizontal_line = clf.tree_.feature[node_idx] == 1
    ponto_divisao = clf.tree_.threshold[node_idx]
    if(horizontal_line):
        if(vertical_lim1 == x_min and vertical_lim2 == x_min):
            min_val = x_min
            max_val = x_max
        else:
            min_val = min(vertical_lim1, vertical_lim2)
            max_val = max(vertical_lim1, vertical_lim2)
        plt.hlines(y=ponto_divisao, xmin=min_val, xmax=max_val, color='r', linestyle='--')
        horizontal_lim2 = horizontal_lim1
        horizontal_lim1 = ponto_divisao
    else:
        if(horizontal_lim1 == y_min and horizontal_lim2 == y_min):
            min_val = y_min
            max_val = y_max
        else:
            min_val = min(horizontal_lim1, horizontal_lim2)
            max_val = max(horizontal_lim1, horizontal_lim2)
        plt.vlines(x=ponto_divisao, ymin=min_val, ymax=max_val, color='r', linestyle='--')
        vertical_lim2 = vertical_lim1
        vertical_lim1 = ponto_divisao

plt.show()