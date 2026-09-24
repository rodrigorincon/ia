import pandas as pd
from itertools import combinations
from pyECLAT import ECLAT # mlxtend NÃO IMPLEMENTA ECLAT, tem de baixar uma outra biblioteca

# Dados de exemplo. Cada linha é um carrinho de compras
# todas as transações devem ter o mesmo tamanho. Preencha as menores None.
compras = [
	['Pao', 'Leite', 'Manteiga', None],
	['Pao', 'Fralda', 'Cerveja', 'Ovos'],
	['Leite', 'Fralda', 'Cerveja', 'Cafe'],
	['Pao', 'Leite', 'Fralda', 'Cerveja'],
	['Pao', 'Leite', 'Manteiga', 'Cafe']
]
df = pd.DataFrame(compras)
print(df)

# Instancia o objeto com os dados em DataFrame
eclat = ECLAT(data=df)
# Executa o algoritmo
# min_support: suporte mínimo em decimal
# min_combination: quantidade mínima de itens no conjunto
# max_combination: K. Quantidade máxima de itens no conjunto
indices_transacoes, suportes = eclat.fit(min_support=0.04, min_combination=1, max_combination=3)

print('----- INDICES')
print(indices_transacoes, '\n') # lista todas as combinações e as linhas do DataFrame em que elas ocorrem
print('----- SUPORTES')
print(suportes) # lista o suporte de todas as combinações


# Calcula Confiança e Lift a partir do dicionário de suportes do pyECLAT
# A biblioteca não tem funções q calcule essas 2 métricas
def calcular_regras_associacao(suportes_dict, min_confiança=0.60, min_lift=1.0, separator=' & '):

	# Mapeia as chaves de string para frozensets para facilitar operações de conjuntos
	# converte as chaves "Pao & Leite" em valores separados
	suportes_sets = { frozenset(chave.split(separator)): valor for chave, valor in suportes_dict.items() }

	regras = []
	# Processa apenas conjuntos com 2 ou mais itens
	for itemset, sup_conjunto in suportes_sets.items():
		if len(itemset) >= 2:
			itens = list(itemset)

			# Gera todos os subsets possíveis para antecedente (A) e consequente (B)
			for r in range(1, len(itens)):
				for antecedente_tuple in combinations(itens, r):
					antecedente = frozenset(antecedente_tuple)
					consequente = itemset - antecedente

					sup_antecedente = suportes_sets.get(antecedente)
					sup_consequente = suportes_sets.get(consequente)

					if sup_antecedente and sup_consequente:
						# Cálculo das métricas
						confianca = sup_conjunto / sup_antecedente
						lift = confianca / sup_consequente

						if confianca >= min_confiança and lift >= min_lift:
							regras.append({
								'antecedente': list(antecedente),
								'consequente': list(consequente),
								'suporte': sup_conjunto,
								'confianca': confianca,
								'lift': lift,
							})

	df_regras = pd.DataFrame(regras)
	return df_regras.sort_values(by='lift', ascending=False)

# calcula o lift e a confiança de cada combinação usando método criado manualmente
df_regras = calcular_regras_associacao(suportes, min_confiança=0.60, min_lift=1.0, separator=' & ')
print("--- REGRAS DE ASSOCIAÇÃO GERADAS A PARTIR DO PYECLAT ---")
print(df_regras.to_string(index=False))
# essa lib parece retornar muito mais linhas de combinações que apriori e fp-growth, alem de dar lift alto pra casos q só ocorreram 1 vez
# recomendo usar o fp-growth como primeira opção