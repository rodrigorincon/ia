import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import apriori, association_rules

# Dados de exemplo. Cada linha é um carrinho de compras
compras = [
	['Pao', 'Leite', 'Manteiga'],
	['Pao', 'Fralda', 'Cerveja', 'Ovos'],
	['Leite', 'Fralda', 'Cerveja', 'Cafe'],
	['Pao', 'Leite', 'Fralda', 'Cerveja'],
	['Pao', 'Leite', 'Manteiga', 'Cafe'],
]

# PRÉ-PROCESSAMENTO (One-Hot Encoding)
# O Apriori usa uma matriz booleana, aonde cada linha é uma compra e cada coluna é um produto (Linhas = Transações, Colunas = Itens)
te = TransactionEncoder()
matriz_booleana = te.fit_transform(compras)
df = pd.DataFrame(matriz_booleana, columns=te.columns_)
print("--- MATRIZ TRANSACIONAL PROCESSADA ---")
print(df, '\n')

###### PARTE 1 DO APRIORI ######

# a função da lib funciona só com DataFrame do pandas. Passar uma matriz feita a mão direto vai dar errado
# min_support = 0.40 significa que o item (ou combinação) precisa aparecer em pelo menos 40% das compras (2 de 5)
# max_len é K, a quantidade máxima de combinações de produtos que iremos avaliar
itemsets_frequentes = apriori(df, min_support=0.40, max_len=3, use_colnames=True)
print("\n--- RETORNO DA FUNÇÃO APRIORI ---")
print(itemsets_frequentes) # devolve um DataFrame com as colunas support (probabilidade de tá presente) e itemsets (lista de produtos presente)

# Criando uma coluna com a quantidade de itens no conjunto (tamanho do itemset)
itemsets_frequentes['num_produtos'] = itemsets_frequentes['itemsets'].apply(lambda x: len(x))
print("\n--- ITEMSETS FREQUENTES ENCONTRADOS ---")
print(itemsets_frequentes.sort_values(by='support', ascending=False)) # ordena dos que saem em maior quantidade

###### PARTE 2 E 3 DO APRIORI ######

# Caso metric="confidence", min_threshold será a nossa CONFIANÇA. min_threshold = 0.60 significa uma Confiança mínima de 60% para validar a regra 
# prob de A ser comprado dado que B também é deve ser >= de min_threshold
# Caso metric="lift", aí min_threshold passa a ser o LIFT mínimo.
# Lembrando que CONFIANÇA = [0,1] e LIFT = [0, infinito] (geralmente usamos lift entre 1 e 2)
regras = association_rules(itemsets_frequentes, metric="confidence", min_threshold=0.60)
print("\n--- RETORNO DA FUNÇÃO DA PARTE 2 E 3 ---")
print(regras.to_string(index=False)) # ela retorna uma porrada de estatísticas e nem todas nos são interessantes

# Selecionando e ordenando as colunas mais importantes
colunas_chave = ['antecedents', 'consequents', 'support', 'confidence', 'lift']
regras_ordenadas = regras[colunas_chave].sort_values(by='lift', ascending=False) # ordenamos pelo lift por ser a var principal
print("\n--- REGRAS DE ASSOCIAÇÃO GERADAS ---")
print(regras_ordenadas.to_string(index=False))
# antecedents é A e consequents é B (chance/probabilidade de consequents ser comprado dado antecedents)

###### PARTE 3 DO APRIORI (REMOVE DADOS COM LIFT ABAIXO DO LIMIAR) ######
regras_finais = regras_ordenadas.iloc[ regras_ordenadas['lift'] > 1.15 ]
print("\n--- COMBINAÇÕES FINAIS APÓS RECORTE DO LIFT ---")
print(regras_finais.to_string(index=False))
