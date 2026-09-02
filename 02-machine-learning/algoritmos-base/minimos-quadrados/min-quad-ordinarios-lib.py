import statsmodels.api as sm

# encontrar a equação que define o preço do imóvel em função do tamanho (m²)
preco = [840000, 822000, 713000, 689000, 685000, 645000, 625000, 620000, 587500, 585000, 583000, 569000, 546000, 540000, 537000, 
516000, 511000, 510000, 495000, 463000, 457000, 451000, 435000, 431700, 414000, 401500, 399000, 380000, 380000, 375900, 372000, 367500,
356500, 330000, 330000, 307500]

m2 = [257, 232, 222, 204, 252, 234, 253, 226, 195, 180, 206, 303, 166, 138, 270, 181, 162, 160, 157, 159, 153, 156, 139, 176, 109, 107, 
128, 124, 118, 211, 93, 118, 132, 126, 136, 78]

# REGRESSÃO LINEAR SIMPLES

# Por algum motivo, o statsmodels não adiciona o intercepto automaticamente, então precisamos fazer isso manualmente.
X = sm.add_constant(m2) # Adicionar intercepto (A0 da equação y = A0 + A1*x)
y = preco
regressao = sm.OLS(y, X).fit() # OLS = Ordinary Least Squares (Mínimos Quadrados Ordinários). 

# RESPOSTA DA REGRESSÃO: COEFICIENTES
coef_ang = regressao.params[1] # 1925.13
coef_lin = regressao.params[0] # 172,690.60

print(f'Equação formada: {coef_ang:.2f}X + {coef_lin:.2f}')

# PREVER O VALOR PARA UM IMÓVEL DE 200 M²
area_nova = 200
X_novo = sm.add_constant([area_nova], has_constant='add') # Adicionar intercepto
previsao = regressao.predict(X_novo)
preco_previsto = previsao[0]

print(f'\n-------Previsão para Imóvel de {area_nova} m² -------')
print(f'Preço previsto: R$ {round(preco_previsto, 2)}')
