import numpy as np
import matplotlib.pyplot as plt
import statsmodels.api as sm

def print_precision_stats(model):
  # margem de erro
  intervalos = model.conf_int() # intervalo de confiança (por padrão com alfa=0.05)
  margem_erro_coef_ang2 = np.round((intervalos[2][1] - intervalos[2][0])/2, 2)
  margem_erro_coef_ang1 = np.round((intervalos[1][1] - intervalos[1][0])/2, 2)
  margem_erro_coef_lin = np.round((intervalos[0][1] - intervalos[0][0])/2, 2)
  # AIC e r2
  r2 = model.rsquared
  r2_ajustado = model.rsquared_adj
  aic = model.aic
  bic = model.bic
  # imprime os resultados
  print('--- Estatísticas de Precisão ---')
  print('Erros de cada ponto:', model.resid, '\n')
  print(f'Margem de erro Coef Angular 1: {margem_erro_coef_ang1:.2f}')
  print(f'Margem de erro Coef Angular 2: {margem_erro_coef_ang2:.2f}')
  print(f'Margem de erro Coef Linear: {margem_erro_coef_lin:.2f}')
  print(f'R²: {r2:.2f}')
  print(f'R² ajustado: {r2_ajustado:.2f}')
  print(f'AIC: {aic:.2f}')
  print(f'BIC: {bic:.2f}')
  print('-------------------------------\n')

# cria os dados
np.random.seed(42)
x1 = np.linspace(1, 10, 10)
x2 = np.linspace(2, 30, 10)
y = 1 + 2.3*x1 + 4*x2 # função: y = 1 + 2.3x1 + 4x2
erro = np.random.normal(0, 0.4 * (x1**1.3) * (x2**1.3)) # Erro cresce com X
y += erro
y = np.array(y)

# cria a matriz de variáveis independentes (X) com duas variáveis (x1 e x2)
# Cada linha deve ser um ponto com os valores X1 e X2 e cada coluna uma variável
X = sm.add_constant(np.column_stack((x1, x2)))

# para fazer a matriz de covariância dos erros precisamos dos erros. E para ter os erros precisamos de uma reta de comparação
# Como ainda não temos a reta, precisamos rodar o OLS (mínimos quadrados ordinários) pra cria-la e então medir os erros.
modelo_ols = sm.OLS(y, X).fit()

# calcula a matriz de covariância dos erros (variância dos erros) a partir do OLS
residuos = np.asarray(modelo_ols.resid)

# centraliza os resíduos (necessario pela equação da covariancia)
residuos_centered = residuos - residuos.mean()

n = residuos_centered.size
# matriz de covariância completa: cov(X1, X2) = (X1 - X_mean)*(X2 - X_mean)/(n-1)
# np.outer faz a multiplicação de cada elemento do vetor com todos os outros elementos do outro vetor, formando uma matriz
matriz_covariancia = np.outer(residuos_centered, residuos_centered) / (n - 1)

# caso tenha valores negativos ou zero na matriz, adiciona-se um pequeno valor à diagonal até que seja positiva-definida. 
# Isso é necessário para que a matriz seja invertível e o GLS funcione corretamente.
if(not np.all(matriz_covariancia > 0)):
  soma_diagonal = np.trace(matriz_covariancia)
  base_eps = 1e-8 * (soma_diagonal if soma_diagonal != 0 else 1.0)
  eps = base_eps
  max_iter = 10
  for i in range(max_iter):
    try:
      np.linalg.cholesky(matriz_covariancia)
      break
    except np.linalg.LinAlgError:
      # regulariza a matriz adicionando um pequeno "jitter" até ficar positiva-definida
      # esse valor começa pequeno e vai aumentando a cada iteração, até que a matriz seja positiva-definida
      matriz_covariancia += np.eye(n) * eps
      eps *= 10
  else:
    raise np.linalg.LinAlgError('Could not make Sigma positive-definite after regularization')

# faz o calculo do GLS (FGLS) com a matriz de covariância dos erros
modelo_gls = sm.GLS(y, X, sigma=matriz_covariancia).fit()
coef = modelo_gls.params
print(f'A equacao via GLS eh {coef[0]:.2f} + {coef[1]:.2f}*X1 + {coef[2]:.2f}*X2')
print_precision_stats(modelo_gls) # imprime estatísticas do modelo GLS
