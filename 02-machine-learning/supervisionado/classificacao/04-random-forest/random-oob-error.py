import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score
import matplotlib.pyplot as plt

# carrega os dados
data = load_breast_cancer()
X = data.data
y = data.target

df = pd.DataFrame(data.data)
df.columns = data.feature_names
df['target'] = data.target
print(df.head())
print('Num Linhas: ', df.shape[0], 'Num colunas:', df.shape[1])
print('quantos casos temos de cada categoria: \n', df.target.value_counts())

# divide os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

### AQUI VAMOS TESTAR A FLORESTA COM DIVERSOS NUMEROS DE ARVORE PARA VER QUAL O MELHOR HIPER-PARAMETRO

# warm_start significa que ao rodar de novo reparoveita os usos anteriores. Ou seja, se rodei com 1 arvore antes e agora vou rodar com 2 
# não vou jogar fora a arvore da rodada anterior e criar 2 novas, eu uso a anterior e crio só 1 nova
modelo = RandomForestClassifier(warm_start=True, oob_score=True, random_state=42)

# define o numer minimo e maximo e o array pra guardar o erro de cada tentativa
min_trees = 10
max_trees = 200
oob_errors = []
contador = range(min_trees, max_trees + 1)
# janela de verificação para ver se o erro OOB estabilizou. Se os ultimos JANELA registros tiverem dentro da mesma margem entao estabilizou e pode parar
janela = 5
tolerancia = 0.001
diferenca_oob_error = []
num_trees_final = max_trees
estabilizou = False

for n_trees in contador:
  modelo.set_params(n_estimators=n_trees)
  modelo.fit(X, y)
  # OOB Error = 1 - OOB Score
  oob_error = 1 - modelo.oob_score_
  oob_errors.append(oob_error)
  # verifica os ultimos valores do erro para ver se estabilizou
  if(len(oob_errors) >= 2): # se tiver 2 ou mais erros (ignora o 1º loop)
    diferenca_oob_error.append( abs(oob_error - oob_errors[-2]) ) # guarda a diferença entre o erro atual e o ultimo antes dele
    if(len(diferenca_oob_error) >= janela and all( diff <= tolerancia for diff in diferenca_oob_error[-janela:]) ):
      num_trees_final = n_trees - janela
      estabilizou = True
      print('Estabilizou em ', num_trees_final, 'árvores!')
      break

plt.figure(figsize=(10, 6))
plt.plot(contador[:len(oob_errors)], oob_errors, marker='o', color='b', linestyle='-')
plt.xlabel('Num Arvores (n_estimators)')
plt.ylabel('OOB Error')
plt.title('Definindo o numero ideal de arvores')
plt.grid(True)

if(estabilizou):
  plt.axvline(x=num_trees_final, color='red', linestyle='--', linewidth=1.5, label=f'Estabiliza em {num_trees_final} árvores')

plt.legend(loc='best')
plt.show()

# analisa a acuracia do modelo
modelo.set_params(n_estimators=num_trees_final, warm_start=False)
modelo.fit(X, y)
y_pred = modelo.predict(X_test)
acuracia = accuracy_score(y_test, y_pred)
print(f"Acuracia: {acuracia:.4f}\n")
