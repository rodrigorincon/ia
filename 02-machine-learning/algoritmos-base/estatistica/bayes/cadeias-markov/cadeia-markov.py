import numpy as np

# Definindo os estados possíveis do clima
estados = ["Ensolarado", "Nublado", "Chuvoso"]

# Matriz de probabilidades
# Linhas: estado atual (Ensolarado, Nublado, Chuvoso)
# Colunas: próximo estado (Ensolarado, Nublado, Chuvoso)
# A soma de cada linha deve ser igual a 1.0
matriz_transicao = np.array([
    [0.8, 0.1, 0.1],  # Se está Ensolarado
    [0.3, 0.4, 0.3],  # Se está Nublado
    [0.2, 0.5, 0.3]   # Se está Chuvoso
])

# Simulando o clima pra daqui X dias
dias_simulacao = 5
matriz_final = np.linalg.matrix_power(matriz_transicao, dias_simulacao)

# checando a probabilidade
print(f'Matriz de probabilidade para {dias_simulacao} dias: ', matriz_final.round(4)*100)

# Definindo o estado inicial (começa em Ensolarado)
estado_inicial = 0

probs = [ matriz_final[estado_inicial, i].round(4) for i in range(len(estados))]
print(f"Probabilidades para o dia {dias_simulacao}: {probs}")

maior_valor = max(probs)
indice = probs.index(maior_valor)
print(f"Clima do dia {dias_simulacao}: {estados[indice]} - {(100*maior_valor):.2f}%")
