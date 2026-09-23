import pandas as pd
from mlxtend.preprocessing import TransactionEncoder
from mlxtend.frequent_patterns import fpgrowth, association_rules

# Dados de exemplo. Cada linha é um carrinho de compras
compras = [
    ['Pao', 'Leite', 'Manteiga'],
    ['Pao', 'Fralda', 'Cerveja', 'Ovos'],
    ['Leite', 'Fralda', 'Cerveja', 'Cafe'],
    ['Pao', 'Leite', 'Fralda', 'Cerveja'],
    ['Pao', 'Leite', 'Manteiga', 'Cafe']
]

# PRÉ-PROCESSAMENTO (One-Hot Encoding)
# O FP-Growth usa uma matriz booleana, aonde cada linha é uma compra e cada coluna é um produto (Linhas = Transações, Colunas = Itens)
te = TransactionEncoder()
matriz_booleana = te.fit_transform(compras)
df = pd.DataFrame(matriz_booleana, columns=te.columns_)
print("--- MATRIZ TRANSACIONAL PROCESSADA ---")
print(df)

# Execução completa do algoritmo fp-growth. Engloba a criação da arvore e a listagem das combinações
# ele usa a mesma interface do apriori. Recebe os mesmos params e devolve o mesmo objeto igual

# a função da lib funciona só com DataFrame do pandas. Passar uma matriz feita a mão direto vai dar errado
# min_support = 0.40 significa que o item (ou combinação) precisa aparecer em pelo menos 40% das compras (2 de 5)
# max_len é K, a quantidade máxima de combinações de produtos que iremos avaliar (mas isso NÃO É profundidade máxima da árvore)
itemsets_frequentes = fpgrowth(df, min_support=0.40, max_len=3, use_colnames=True)
print("\n--- RETORNO DA FUNÇÃO FP-GROWTH ---")
print(itemsets_frequentes) # devolve um DataFrame com as colunas support (probabilidade de tá presente) e itemsets (lista de produtos presente)

# Criando uma coluna com a quantidade de itens no conjunto (tamanho do itemset)
itemsets_frequentes['tamanho'] = itemsets_frequentes['itemsets'].apply(lambda x: len(x))
print("\n--- ITEMSETS FREQUENTES ENCONTRADOS (FP-GROWTH) ---")
print(itemsets_frequentes.sort_values(by='support', ascending=False)) # ordena dos que saem em maior quantidade

# calcula as métricas suporte, confiança e lift
regras = association_rules(itemsets_frequentes, metric="confidence", min_threshold=0.60)
# Selecionando e ordenando as colunas mais importantes
colunas_chave = ['antecedents', 'consequents', 'support', 'confidence', 'lift']
regras_ordenadas = regras[colunas_chave].sort_values(by='lift', ascending=False)
regras_finais = regras_ordenadas.iloc[ regras_ordenadas['lift'] > 1.15 ]

print("\n--- REGRAS DE ASSOCIAÇÃO GERADAS ---")
print(regras_finais.to_string(index=False))
