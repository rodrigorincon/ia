import pandas as pd
import numpy as np
from pgmpy.models import DiscreteBayesianNetwork
from pgmpy.inference import VariableElimination
from pgmpy.causal_discovery import PC

# algoritmo PC usa dados para construir o grafo e MLE para definir as probabilidades. Vou criar os dados
rng = np.random.default_rng(42)
num_amostras = 5000

# regras: 1/3 de chance de chuva. 1/3 de chance de sair de carro se chover e 0% se não chover
# regras: Nv Gas: 0 = pouca gasolina, 1 = tanque na metade, 2 = cheio (1/3 de chance de cada)
# destino final: 0 = casa, 1 = shopping, 2 = fazenda
# destino: se ñ sair de carro fica em casa. Se sair e nv gas é baixo ou médio, vai pro shopping. Se alto vai pra fazenda
chuva = rng.binomial(1, 1/3, size=num_amostras) # 1 = chove, 0 = não chove
sair_carro = np.where(chuva == 1, rng.binomial(1, 1/3, size=num_amostras), 1)
nivel_gasolina = rng.choice([0, 1, 2], size=num_amostras, p=[1/3, 1/3, 1/3])
destino = np.where(
    sair_carro == 0,
    0,
    np.where(nivel_gasolina < 2, 1, 2)
)

df = pd.DataFrame({
  "Chuva": chuva,
  "Carro": sair_carro,
  "Gasolina": nivel_gasolina,
  "Destino": destino
})

# Cria o grafo usando algoritmo PC
pc = PC(
    ci_test='chi_square',
    significance_level=0.05, # limite para o teste de independência (ex: 0.05)
    max_cond_vars=2, # num maximo de vars condicionais a considerar no teste de independencia (no caso são 2 pq são chuva e regador)
    return_type='dag')
rede_pc = pc.fit(df)

# chuva -> carro, carro -> destino, gasolina -> destino
print("\nEstrutura estimada pelo algoritmo PC:")
print("Edges:", rede_pc.causal_graph_.edges())

# Faz o cálculo de probabilidade
modelo = DiscreteBayesianNetwork(rede_pc.causal_graph_.edges())
# descobre as probabilidades entre as variaveis usando os dados
modelo.fit(df) # por default usa MLE
infer = VariableElimination(modelo)

# Fazendo inferência (qual a chance de estar chovendo se fui pro shopping?)
resultado = infer.query(variables=['Chuva'], evidence={'Destino': 1})
print(resultado, '\n')

# Fazendo inferência (qual a chance da eu ir pra fazenda?)
infer = VariableElimination(modelo)
resultado = infer.query(variables=['Destino']).get_value(Destino=2)
print(resultado)
