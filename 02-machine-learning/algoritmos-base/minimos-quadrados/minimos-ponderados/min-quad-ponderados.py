import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

def print_precision_stats(model):
  # margem de erro
  intervalos = model.conf_int() # intervalo de confiança (por padrão com alfa=0.05)
  margem_erro_coef_ang = np.round((intervalos[1][1] - intervalos[1][0])/2, 2)
  margem_erro_coef_lin = np.round((intervalos[0][1] - intervalos[0][0])/2, 2)
  # AIC e r2
  r2 = model.rsquared
  r2_ajustado = model.rsquared_adj
  aic = model.aic
  bic = model.bic
  # imprime os resultados
  print('--- Estatísticas de Precisão ---')
  print('Erros de cada ponto:', model.resid, '\n')
  print(f'Margem de erro Coef Angular: {margem_erro_coef_ang:.2f}')
  print(f'Margem de erro Coef Linear: {margem_erro_coef_lin:.2f}')
  print(f'R²: {r2:.2f}')
  print(f'R² ajustado: {r2_ajustado:.2f}')
  print(f'AIC: {aic:.2f}')
  print(f'BIC: {bic:.2f}')
  print('-------------------------------\n')

# cria dados com heterocedasticidade (variância não constante). Quando maior X, mais Y varia
np.random.seed(42)
x = np.linspace(1, 10, 10)
y = 2.5 * x + np.random.normal(0, 0.4 * (x**1.5)) # Erro cresce com X

print('X: ', x)
print('Y: ', y, '\n')
plt.scatter(x, y, label='Dados', color='blue')
plt.xlabel('X')
plt.ylabel('Y')
plt.show()

# Adicionar constante para os modelos
X = sm.add_constant(x)

# Quando não temos os pesos de antemão precisamos calcula-los a partir da variância dos resíduos
# Residuo = erro = distancia de cada ponto da reta. 
# Como ainda não temos reta temos de rodar o OLS (mínimos quadrados ordinários) pra cria-la e então medir os erros.
# A variação dos erros (a partir da linha de regressão) é oq precisamos para definir os pesos. Peso = 1 / variancia
# OU SEJA, temos de rodar o OLS para termos nossos erros para só então termos os pesos e rodar o WLS (FGLS) final.

# PASSO 1: rodar o OLS (mínimos quadrados ordinários)
modelo_ols = sm.OLS(y, X).fit()
coef = modelo_ols.params
print(f'A equacao via OLS eh {coef[0]:.2f} + {coef[1]:.2f}*X')
print_precision_stats(modelo_ols)

# PASSO 2: Calcular a variância dos erros e os pesos
residuos_quadrado = modelo_ols.resid ** 2
pesos = 1.0 / (residuos_quadrado)

# PASSO 3: Usa o modelo WLS (FGLS) final com os pesos calculados
modelo_wls_final = sm.WLS(y, X, weights=pesos).fit()
coef = modelo_wls_final.params
print(f'A equacao via WLS eh {coef[0]:.2f} + {coef[1]:.2f}*X')
print_precision_stats(modelo_wls_final) # deu valores muito melhores em todas as metricas