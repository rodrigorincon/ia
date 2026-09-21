import numpy as np
import matplotlib.pyplot as plt

##### EXEMPLO DE MONTE CARLO USANDO CURVA NORMAL
# simularemos 1 mes de vendas diversas vezes para ver em quantos saímos no lucro

# parametros da curva normal
venda_media_diaria = 5000       # Média
desvio_padrao_diario = 1200     # Desvio Padrão
dias_uteis_no_mes = 22          # Tamanho da amostra usada em cada simulação

# parametros do Monte Carlo
n_simulacoes = 100_000            # Número de cenários/meses simulados
meta_faturamento_mes = 120_000   # Meta para pagar os custos fixos

# guarda o faturamento total de cada um dos 100.000 meses simulados
faturamentos_mensais = []

# execução da simulação de Monte Carlo
for _ in range(n_simulacoes):
  # Pega 22 dias (1 mes) aleatorios seguindo a curva normal
  vendas_mes = np.random.normal(venda_media_diaria, desvio_padrao_diario, dias_uteis_no_mes)
  # Soma o faturamento total daquele mês simulado
  faturamentos_mensais.append(np.sum(vendas_mes))

faturamentos_mensais = np.array(faturamentos_mensais)

# análise dos resultados simulados
faturamento_medio = np.mean(faturamentos_mensais)
probabilidade_prejuizo = np.mean(faturamentos_mensais < meta_faturamento_mes) * 100

print(f"--- RESULTADO DA SIMULAÇÃO ---")
print(f"Faturamento Médio Mensal Esperado: R$ {faturamento_medio:,.2f}")
print(f"Risco de Prejuízo (Faturamento abaixo da meta): {probabilidade_prejuizo:.2f}%")

# plotando a curva normal criada pelas simulações
plt.figure(figsize=(10, 6))
plt.hist(faturamentos_mensais, bins=50, color='skyblue', edgecolor='black', density=True, alpha=0.6)
plt.axvline(meta_faturamento_mes, color='red', linestyle='--', linewidth=2, label=f'Meta Mínima (R$ {meta_faturamento_mes:,})')
plt.axvline(faturamento_medio, color='green', linestyle='-', linewidth=2, label=f'Faturamento Médio (R$ {faturamento_medio:,.0f})')

plt.title('Simulação de Monte Carlo: Distribuição do Faturamento Mensal')
plt.xlabel('Faturamento Total do Mês (R$)')
plt.ylabel('Densidade de Probabilidade')
plt.legend()
plt.grid(True, alpha=0.3)
plt.show()
