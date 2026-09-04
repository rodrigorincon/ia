import pandas as pd
import numpy as np
import statsmodels.api as sm

idades = [45, 50, 30, 60, 55, 40, 35, 70, 65, 50, 42, 36, 53, 58, 62, 39, 48, 33, 66, 41, 57, 49, 34, 61, 47, 38, 54, 63, 32, 46]
glicose = [85, 120, 75, 140, 110, 90, 80, 160, 150, 100, 95, 82, 115, 135, 145, 87, 102, 78, 155, 98, 128, 106, 81, 138, 104, 89, 118, 148, 77, 112]
diabetes = [0, 1, 0, 0, 0, 0, 0, 1, 1, 0, 0, 0, 1, 1, 1, 0, 0, 0, 1, 0, 1, 0, 0, 1, 0, 0, 1, 1, 0, 0]

# REGRESSÃO LOGISTICA COM PANDAS
X = pd.DataFrame({'idade': idades, 'glicose': glicose})
y = pd.DataFrame({'diabetes': diabetes})

X = sm.add_constant(X)
modelo = sm.Logit(y, X)

# Executa reg logística com regularização (Lasso ou Ridge)
# alpha: taxa de penalidade (quanto maior, mais penalidade)
# L1_wt: 1 = Lasso (L1), 0 = Ridge (L2), or between 0 & 1 for Elastic Net
resultado_lasso = modelo.fit_regularized(alpha=0.1, L1_wt=1.0)
print(f'Pesos Lasso: {resultado_lasso.params}')

# Rodando com Ridge para comparar
# L1_wt: 1 = Lasso (L1), 0 = Ridge (L2), or between 0 & 1 for Elastic Net
resultado_ridge = modelo.fit_regularized(alpha=0.1, L1_wt=0.0)
print(f'Pesos Ridge: {resultado_ridge.params}')

# Por curiosidade, rodarei o modelo sem regularização para comparar os pesos
resultado_padrao = sm.Logit(y, X).fit()
print(f'Pesos (sem regularização): {resultado_padrao.params}')

# PREVISÃO
novo_valor_idade = 60
novo_valor_glicose = 130
novo_X = pd.DataFrame({'const': [1], 'idade': [novo_valor_idade], 'glicose': [novo_valor_glicose]})

prob_prevista_lasso = resultado_lasso.predict(novo_X)
print(f'\nA probabilidade prevista de ser diabético (COM LASSO) é: {prob_prevista_lasso[0]:.2f}') 

prob_prevista_ridge = resultado_ridge.predict(novo_X)
print(f'\nA probabilidade prevista de ser diabético (COM RIDGE) é: {prob_prevista_ridge[0]:.2f}') 

prob_prevista_padrao = resultado_padrao.predict(novo_X)
print(f'\nA probabilidade prevista de ser diabético (SEM REGULARIZAÇÃO) é: {prob_prevista_padrao[0]:.2f}') 
