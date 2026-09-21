from sklearn.datasets import load_iris
from sklearn.model_selection import train_test_split
from sklearn.naive_bayes import GaussianNB
from sklearn.metrics import accuracy_score, classification_report

# carrega os dados. Y pode ter 3 valores
data = load_iris()
X = data.data
y = data.target

# divide os dados em treino e teste
X_train, X_test, y_train, y_test = train_test_split(X, y, test_size=0.2, random_state=42)

# executa o algoritmo do naive bayes ASSUMINDO DISTRIBUIÇÃO NORMAL
model = GaussianNB()
model.fit(X_train, y_train)

# testar a precisão dele
y_pred = model.predict(X_test)
accuracy = accuracy_score(y_test, y_pred)
print(f"Acuracia: {(100 * accuracy):.2f}%\n")
print("Relatorio:")
print(classification_report(y_test, y_pred, target_names=data.target_names))

# testa um dado novo
new_flower = [[5.1, 3.5, 1.4, 0.2]]
predicted_class_index = model.predict(new_flower)[0]
predicted_species = data.target_names[predicted_class_index]

print(f"Tipo da flor {new_flower}: {predicted_species}")
