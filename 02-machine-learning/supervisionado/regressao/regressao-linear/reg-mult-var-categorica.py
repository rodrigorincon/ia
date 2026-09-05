import pandas as pd
import statsmodels.formula.api as smf
import statsmodels.api as sm

df = pd.DataFrame({
  "charges": [16884.924, 1725.5523, 4449.462, 21984.47061, 3866.8552, 3756.6216, 8240.5896, 7281.5056, 6406.4107, 28923.13692, 2721.3208, 27808.7251, 1826.843, 11090.7178, 39611.7577, 1837.237, 10797.3362, 2395.17155, 10602.385],
  "sex": ['female', 'male', 'male', 'male', 'male', 'female', 'female', 'female', 'male', 'female', 'male', 'female', 'male', 'female', 'male', 'male', 'female', 'male', 'male'],
  "age": [19, 18, 28, 33, 32, 31, 46, 37, 37, 60, 25, 62, 23, 56, 27, 19, 52, 23, 56],
  "bmi": [27.9, 33.77, 33, 22.705, 28.88, 25.74, 33.44, 27.74, 29.83, 25.84, 26.22, 26.29, 34.4, 39.82, 42.13, 24.6, 30.78, 23.845, 40.3],
  "children": [0, 1, 3, 0, 0, 0, 1, 3, 2, 0, 0, 0, 0, 0, 0, 1, 1, 0, 0],
  "smoker": ['yes', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'no', 'yes', 'no', 'no', 'yes', 'no', 'no', 'no', 'no'],
  "region": ['southwest', 'southeast', 'southeast', 'northwest', 'northwest', 'southeast', 'southeast', 'northwest', 'northeast', 'northwest', 'northeast', 'southeast', 'southwest', 'southeast', 'southeast', 'southwest', 'northeast', 'northeast', 'southwest']
})

############### Forma 1
modelo = smf.ols('charges ~ age + C(sex, Treatment(reference="female")) + bmi + children + C(smoker, Treatment(reference="no")) + C(region, Treatment(reference="northeast"))', data = df).fit()
print(modelo.summary(), '\n')

# estimando valores
novo_sex = 'male'
novo_age = 34
novo_bmi = 30
novo_children = 0
novo_smoker = 'no'
novo_region = 'southwest'

novo_X = pd.DataFrame({'const': [1], 'sex': [novo_sex], 'age': [novo_age], 'bmi': [novo_bmi], 'children': [novo_children], 'smoker': [novo_smoker], 'region': [novo_region]})
valor_plano_previsto = modelo.predict(novo_X)
print(f'Previsão do valor do plano de saude:')
print(f'Salário previsto: R$ {valor_plano_previsto[0]:.2f}\n\n\n')

############### Forma 2
sex = (df['sex'] == 'male').astype(int) # Male=1, Female=0
smoker = (df['smoker'] == 'yes').astype(int) # smoker=1, no smoker=0
# na categorica multipla, northeast será nosso 0
northwest = (df['region'] == 'northwest').astype(int) # northwest=1, others=0
southeast = (df['region'] == 'southeast').astype(int) # southeast=1, others=0
southwest = (df['region'] == 'southwest').astype(int) # southwest=1, others=0

list_x = pd.DataFrame({
  "sex": sex,
  "age": df['age'],
  "bmi": df['bmi'],
  "children": df['children'],
  "smoker": smoker,
  "northwest": northwest,
  "southeast": southeast,
  "southwest": southwest
}) # usa dataframe para passar os dados pq a função espera os dados onde cada linha é um ponto. Passar como um array vai dar erro
# em outras palavras, como array passaria uma matriz 8x20 e o métodos espers 20x8
x = sm.add_constant(list_x)
modelo = sm.OLS(df['charges'], x).fit()
print(modelo.summary(), "\n")

# estimando valores
novo_sex = 1 # male
novo_age = 34
novo_bmi = 30
novo_children = 0
novo_smoker = 0 # no smoker
novo_northwest = 0 # quero estimar para outra região
novo_southeast = 0 # quero estimar para outra região
novo_southwest = 1 # quero estimar para essa região

novo_X = pd.DataFrame({'const': [1], 'sex': [novo_sex], 'age': [novo_age], 'bmi': [novo_bmi], 'children': [novo_children], 
                       'smoker': [novo_smoker], 'northwest': [novo_northwest], 'southeast': [novo_southeast], 'southwest': [novo_southwest]})
valor_plano_previsto = modelo.predict(novo_X)
print(f'Previsão do valor do plano de saude:')
print(f'Salário previsto: R$ {valor_plano_previsto[0]:.2f}')
