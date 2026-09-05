import pandas as pd
import statsmodels.api as sm
import matplotlib.pyplot as plt
import seaborn as sns
import scipy.stats as stats
import statsmodels.stats.api as sms
from statsmodels.stats.stattools import jarque_bera
from statsmodels.stats.outliers_influence import variance_inflation_factor

casas = pd.DataFrame({
  'area': [257, 232, 222, 204, 252, 234, 253, 226, 195, 180, 206, 303, 166, 138, 270, 181, 162, 160, 157, 159, 153, 156, 139, 176, 109, 107, 128, 124, 118, 211, 93, 118, 132, 126, 136, 78],
  'banheiro': [3.5, 2.5, 3, 2.5, 3.5, 2, 2.5, 3.5, 1.5, 1.5, 2.5, 2, 2, 1.5, 2.5, 2, 1.5, 2, 2, 2, 2, 2, 1.5, 1.5, 1.5, 1, 1, 2, 1, 1, 1, 1, 2, 1, 1, 1],
  'quarto': [4, 4, 3, 3, 3, 3, 4, 4, 3, 3, 3, 4, 3, 3, 3, 4, 3, 3, 3, 3, 3, 3, 3, 2, 2, 3, 4, 4, 3, 5, 2, 3, 2, 3, 3, 1],
  'preco': [840000, 822000, 713000, 689000, 685000, 645000, 625000, 620000, 587500, 585000, 583000, 569000, 546000, 540000, 537000, 516000, 511000, 510000, 495000, 463000, 457000, 451000, 435000, 431700, 414000, 401500, 399000, 380000, 380000, 375900, 372000, 367500, 356500, 330000, 330000, 307500]
})
vars_independentes = ['area', 'banheiro', 'quarto']

x = casas[['area', 'banheiro', 'quarto']]
x = sm.add_constant(x)
y = casas['preco']
modelo = sm.OLS(y, x).fit()
print(modelo.summary(), "\n\n")
print(f'A equacao eh {modelo.params['quarto']:.0f}*Quartos + {modelo.params['banheiro']:.0f}*Banheiros + {modelo.params['area']:.0f}*Area + {modelo.params['const']:.0f}')

#### ANALISE DE HOMOCEDASTICIDADE
residuos = modelo.resid

y_reta = modelo.fittedvalues # dá os valores de ŷ, ou seja, os valores de Y dá nossa reta/regressão
sns.scatterplot(x=y_reta, y=residuos)
plt.axhline(y=0, color='gray', linestyle='--')
plt.xlabel('Y Calculados')
plt.ylabel('Resíduos')
plt.show()

# Retorna: Estatística LM, p-valor do LM, Estatística F, p-valor do F
stat_lagrange, lagrange_pvalue, stat_f, f_pvalue = sms.het_breuschpagan(modelo.resid, modelo.model.exog)
# O p-valor de lagrange é melhor para amostras grandes e o do F para amostras pequenas
# Lagrange é o teste padrão do Bresch-Pagan, mas ele é pouco preciso para amostras pequenas e pode dar falsos positivos (erro tipo 1)
# Para corrigir isso ele calcula 2 testes, um mais adequado para N grande e outro para N pequeno e você escolhe o melhor para seu contexto
test_text = "Passou no teste" if lagrange_pvalue > 0.05 else "Não passou no teste"
print(f'P valor do Breush-Pagan: {lagrange_pvalue:.4f}. {test_text}') 
print(f'Por curiosidade, o teste para amostras pequenas foi {f_pvalue:.4f}\n')

#### ANALISE DE NORMALIDADE
sm.qqplot(residuos, line='45', fit = True)
plt.show()

_, shapiro_pvalue = stats.shapiro(residuos)
test_text = "Passou no teste" if shapiro_pvalue > 0.05 else "Não passou no teste"
print(f'P valor do shapiro: {shapiro_pvalue:.4f}. {test_text}\n')

stat_jb, jb_pvalue, skewness, curtose = jarque_bera(residuos)
test_text = "Passou no teste" if jb_pvalue > 0.05 else "Não passou no teste"
print(f'P valor do Jarque-Bera: {jb_pvalue:.4f}. {test_text}')
print(f'Por curiosidade, o nível de assimetria é {skewness:.3f} (o normal é 0) e a curtose é {curtose:.3f} (o normal é 3)\n')

#### ANALISE DE MULTI COLINEARIDADE
correlacoes = casas.corr(method='pearson') # parametro padrão
for i in range(len(vars_independentes)-1):
  for j in range(i+1, len(vars_independentes)):
    corr = correlacoes[vars_independentes[i]][vars_independentes[j]]
    if(corr > 0.7):
      print(f'As vars {vars_independentes[i]} e {vars_independentes[j]} são fortemente correlacionadas {corr:.2f}. Analise retirar uma delas, pegar mais amostras ou usar outro metodo de minimo quadrado')

print('\n')
# Calcula o VIF para cada var independente
df_vars_independentes  = pd.DataFrame(casas).drop('preco', axis=1) # cria um novo df só com as vars independentes

# A entrada pra função tem de ser uma matriz só com as vars independentes (X), aonde cada linha é um ponto
# O 2º parametro é a coluna da variavel que estamos analisando (para ser pulada pelo método)
vif_area = variance_inflation_factor(df_vars_independentes, 0)
vif_banheiro = variance_inflation_factor(df_vars_independentes, 1)
vif_quarto = variance_inflation_factor(df_vars_independentes, 2)

# outra forma, mais automatica porem menos legivel de fazer isso para N vars
for i in range(len(df_vars_independentes.columns)):
  vif = variance_inflation_factor(df_vars_independentes, i)
  if vif > 10:
    var_name = df_vars_independentes.columns[i]
    print(f'A var {var_name} é muito correlacionada com as outras. VIF = {vif:.1f}')

print('\n')
#### ANALISE ANOVA
f_stat = modelo.fvalue
f_pvalue = modelo.f_pvalue

test_text = "Passou no teste" if f_pvalue < 0.05 else "Não passou no teste"
print(f'P valor da Anova: {f_pvalue:.4f}. {test_text}\n')

#### ANALISE TESTE T
t_pvalues = modelo.pvalues[1:] # ignora o A0 (intercepto)
for i in range(len(t_pvalues)):
  p_value = t_pvalues.iloc[i]
  if(p_value > 0.05):
    print(f'Variavel {vars_independentes[i]} NÃO PASSOU no teste T. P-valor = {p_value:.4f}')

print('\n')
#### ANALISE INTERVALO DE CONFIANCA
intervalo = modelo.conf_int() # intervalo de confiança padrão (95%)
for var_name in vars_independentes:
  interv_sup = intervalo.loc[var_name][1]
  interv_inf = intervalo.loc[var_name][0]
  if(interv_sup > 0 and interv_inf < 0):
    print("Variável", var_name, "não passou no teste o intervalo de confiança. Seu intervalo passa pelo 0")

print('\n')
#### ANALISE DESVIO DOS ERROS
desvios_erros = modelo.bse
for i in range(1,len(desvios_erros)):
  desvio_erro = desvios_erros.iloc[i]
  print(f'Desvio do Erro do {vars_independentes[i-1]}: {desvio_erro:.2f}')

print('\n')
#### ANALISE R2 AJUSTADO E AIC E BIC
r2 = modelo.rsquared
r2_ajustado = modelo.rsquared_adj
aic = modelo.aic
bic = modelo.bic

print(f'Coef de Determinação R²: {r2:.2f}')
print(f'Coef de Determinação R² Ajustado: {r2_ajustado:.2f}')
print(f'AIC: {aic:.2f}')
print(f'BIC: {bic:.2f}')