from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.factors.discrete import TabularCPD
from pgmpy.inference import VariableElimination

#### ---------- FORMA 1 DE MONTAR A REDE BAYESIANA: montando o grafo na mão (quando ja sabe as probabilidades de antemão)

# Cria o grafo
# Chuva -> GramaMolhada e Regador -> GramaMolhada
modelo = DiscreteBayesianNetwork([('Chuva', 'GramaMolhada'), ('Regador', 'GramaMolhada')])

# Bota as probabilidades
# Chuva: 30%, Regador: 50%
cpd_chuva = TabularCPD(variable='Chuva', variable_card=2, values=[[0.7], [0.3]])
cpd_regador = TabularCPD(variable='Regador', variable_card=2, values=[[0.5], [0.5]])

# Probabilidade de Grama Molhada dados Chuva e Regador
# Ordem das colunas no pgmpy para os pais [Chuva, Regador]:
'''
no caso a coluna fica assim
Chuva | Regador | p(molhado) | p(não molhado)
 0    |   0     |  0         |  1
 0    |   1     |  0.7       |  0.3
 1    |   0     |  0.9       |  0.1
 1    |   1     |  0.99      |  0.01
'''
cpd_grama = TabularCPD(
    variable='GramaMolhada', 
    variable_card=2, # numero de estados que a variavel pode ter (no caso 2: molhado ou não molhado).
    values=[ # uma linha para cada valor no variable_card
        [1.0, 0.3, 0.1, 0.01],  # Grama NÃO molhada
        [0.0, 0.7, 0.9, 0.99]   # Grama molhada
    ],
    evidence=['Chuva', 'Regador'],
    evidence_card=[2, 2] # numero de estados de cada uma das evidencias (no caso, chuva tem 2 e regador tem 2)
)

modelo.add_cpds(cpd_chuva, cpd_regador, cpd_grama)
model_build_correctly = modelo.check_model()
if(not model_build_correctly): print("Rede não foi montada corretamente. Verifique se a quantidade das cardinalidades estão todas corretas")

# Fazendo inferência (qual a chance de chover se a grama estiver molhada?)
infer = VariableElimination(modelo)
resultado = infer.query(variables=['Chuva'], evidence={'GramaMolhada': 1})
print(resultado, '\n')

# Fazendo inferência (qual a chance da grama estar molhada?)
infer = VariableElimination(modelo)
resultado = infer.query(variables=['GramaMolhada'])
print(resultado, '\n\n------------------------')

#### ---------- FORMA 2 DE MONTAR A REDE BAYESIANA: usando algoritmo PC pra montar o grafo e MLE pra descobrir as probabilidades
import pandas as pd
import numpy as np
from pgmpy.causal_discovery import PC

# algoritmo PC usa dados para construir o grafo e MLE para definir as probabilidades. Vou criar os dados
rng = np.random.default_rng(42)
num_amostras = 5000
# Chuva: 30%, Regador: 50%
chuva = rng.binomial(1, 0.3, size=num_amostras) # 1 = chove, 0 = não chove
regador = rng.binomial(1, 0.5, size=num_amostras) # 1 = regador ligado, 0 = desligado

prob_molhada = np.select(
    [
        (chuva == 0) & (regador == 0),
        (chuva == 0) & (regador == 1),
        (chuva == 1) & (regador == 0),
        (chuva == 1) & (regador == 1),
    ],
    [0, 0.7, 0.9, 0.99],
    default=0.0,
)
grama_molhada = rng.binomial(1, prob_molhada)

data = pd.DataFrame({
    "Chuva": chuva,
    "Regador": regador,
    "GramaMolhada": grama_molhada,
})

# Cria o grafo usando algoritmo PC
pc = PC(
    ci_test='chi_square',
    significance_level=0.05, # limite para o teste de independência (ex: 0.05)
    max_cond_vars=2, # num maximo de vars condicionais a considerar no teste de independencia (no caso são 2 pq são chuva e regador)
    return_type='dag')
rede_pc = pc.fit(data)

print("\nEstrutura estimada pelo algoritmo PC:")
print("Edges:", rede_pc.causal_graph_.edges())

# Faz o cálculo de probabilidade
modelo = DiscreteBayesianNetwork(rede_pc.causal_graph_.edges())
# descobre as probabilidades entre as variaveis usando os dados
modelo.fit(data) # por default usa MLE
infer = VariableElimination(modelo)

# Fazendo inferência (qual a chance de chover se a grama estiver molhada?)
resultado = infer.query(variables=['Chuva'], evidence={'GramaMolhada': 1})
print(resultado, '\n')

# Fazendo inferência (qual a chance da grama estar molhada?)
infer = VariableElimination(modelo)
resultado = infer.query(variables=['GramaMolhada'])
print(resultado)
