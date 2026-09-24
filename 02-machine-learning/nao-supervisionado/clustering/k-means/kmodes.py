import numpy as np
import pandas as pd
from kmodes.kmodes import KModes
from sklearn.impute import SimpleImputer

dados = {
	'Profissao': ['Engenheiro','Médico','Engenheiro',np.nan,'Advogado','Médico','Advogado','Engenheiro'],
	'Escolaridade': ['Superior','Pós',np.nan,'Médio','Superior','Pós','Superior',np.nan],
	'Uso_Cartao': ['Alto','Médio','Baixo','Baixo',np.nan,'Alto','Médio','Baixo'],
	'Canal_Preferido': ['App','Web','App','Presencial','Web',np.nan,'Web','App'],
}
df = pd.DataFrame(dados)
print("--- DATASET ORIGINAL (COM DADOS FALTANTES) ---")
print(df)


# tratamento de dados faltantes
# O K-Modes não aceita NaNs diretamente. Temos de fazer uma dessas 2 coisas:
# OPÇÃO 1: troca NAN pela Moda (Valor mais frequente da coluna)
# OPÇÃO 2: troca NaN por uma categoria nova ('Ausente')

# Opção 1 (troca pela Moda com SimpleImputer)
imputer = SimpleImputer(strategy='most_frequent')
df_tratado = pd.DataFrame(imputer.fit_transform(df), columns=df.columns)

# Opção 2: trocar NaN por uma categoria nova
# df_tratado = df.fillna('Ausente')

print("\n--- DATASET APÓS IMPUTAÇÃO DA MODA ---")
print(df_tratado)

# treinamento
# init define como escolher os centros iniciais (opções: Huang, Cao, random). 
# Huang é simples e rápido e Cao é mais robusto (é o kmeans++ do kmodes)
km = KModes(n_clusters=2, init='Cao', n_init=500, random_state=42)
clusters = km.fit_predict(df_tratado)

df_tratado['Cluster'] = clusters
print("\n--- ATRIBUIÇÃO DOS CLUSTERS AOS DADOS ---")
print(df_tratado)

print("\n--- MODAS (CENTROIDES) DE CADA CLUSTER ---")
df_centroides = pd.DataFrame(km.cluster_centroids_, columns=df.columns)
print(df_centroides)