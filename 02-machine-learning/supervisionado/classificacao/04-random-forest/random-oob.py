import pandas as pd
from sklearn.datasets import load_breast_cancer
from sklearn.model_selection import train_test_split
from sklearn.ensemble import RandomForestClassifier
from sklearn.metrics import accuracy_score, classification_report, confusion_matrix

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

# roda a floresta aleatoria com 100 árvores divididos em 10 threads E USANDO OS DADOS NÃO PRESENTES NA ÁRVORE PARA TESTÁ-LA
modelo = RandomForestClassifier(n_estimators=100, n_jobs=10, oob_score=True, random_state=42)
modelo.fit(X_train, y_train)

print(f"OOB Score: {modelo.oob_score_:.4f}")

# analisa a acuracia do modelo (exatamente igual a oob_score=false)
y_pred = modelo.predict(X_test)
acuracia = accuracy_score(y_test, y_pred)
print(f"Acuracia: {acuracia:.4f}\n")
print("Relatorio do modelo:")
print(classification_report(y_test, y_pred, target_names=data.target_names))
