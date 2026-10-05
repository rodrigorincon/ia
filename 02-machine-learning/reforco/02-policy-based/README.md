# APRENDIZADO POR REFORÇO: FAMÍLIA POLICY-BASED

A família policy-based (baseada em políticas) tomam a decisão de qual ação fazer ao **otimizar uma política do agente**, sem a necessidade de calcular obrigatoriamente uma função de valor V(s) ou Q(s, a) para tomar decisões. 

Essa política é uma função que recebe parâmetros. Conforme vai explorando o mundo (passando os passos) vai alterado os parâmetros de entrada, tornado a escolha da ação mais precisa. Geralmente essa função é uma rede neural. **Importante lembrar que a política não é uma função de valor V(s)!**

Essa política (função ou rede neural) **calcula probabilidades de tomar cada ação dado o estado P(a|s)**, sem a necessidade da tabela Q. De forma técnica, estes algoritmos otimizam os parâmetros $\theta$ de uma política $P_\theta(a|s)$ **diretamente**. Os algoritmos ajustam os parâmetros através de técnicas como a **Subida de Gradiente (Gradient Ascent)** na direção que aumenta o retorno esperado. O aprendizado consiste em **aumentar a probabilidade de ações que geraram bons resultados** e diminuir a probabilidade de ações que geraram resultados ruins.

## Diferenças Para a Value-Based

Os algoritmos value-based são determinísticos: escolhem a meçhor ação para aquele estado (valor máximo do estado). Os algoritmos policy-based definem uma probabilidade de quão boa uma ação será e a atualizam conforme testam. Usam o gradiente ascendente para ajustar os parâmetros dessa distribuição, aumentando a probabilidade de ações que geram altas recompensas e diminuindo a de ações desastrosas. 

Essa diferença permite a eles lidar naturalmente com espaços contínuos (alta dimensão) e de aprender a lidar em ambientes aleatórios (afinal lidam com probabilidades, permitindo tomar ações ruins, mesmo que com baixas chances), essenciais em ambientes parcialmente observáveis.

## Diferença Entre os Algoritmos

Os algoritmos **mudam muito em como estimam o gradiente e estabilizam o aprendizado** para evitar atualizações destrutivas. O REINFORCE (Monte Carlo Policy Gradient) calcula o gradiente com base na recompensa total do episódio, o que causa uma variância muito alta e retarda a convergência. 

Para consertar esse problema surgiram os métodos Actor-Critic, que combinam o aprendizado de política com uma função de valor auxiliar V(s) (o crítico). Essa combinação reduz a variância usando estimativas de diferença temporal (como no Q-learn). Eles definem restrições matemáticas e limites para o tamanho das alterações na política a cada passo.

# REINFORCE (Monte Carlo Policy Gradient)

É o algoritmo fundamental da família policy-based. Ele faz amostragem de episódios (método Monte Carlo) para calcular o retorno real obtido. Ele calcula a recompensa apenas ao acabar o episódio e só nesse momento atualiza os parâmetros da política (pesos da rede neural).

O objetivo dele é criar uma rede neural que haja como uma distribuição de probabilidade P(a|s). Descobrir qual distribuição dá mais chance de boas ações e menos para ações ruins é o desafio. Para tanto os pesos da rede são atualizados até alcançar esse objetivo.

- **Quando usar:** Quando as **ações são contínuas** (posso andar 3,45 cm a 18 graus de onde estou) ou problemas onde a política ótima é estocástica.
- **Tipo:** On-Policy.
- **Recompensa**: Só quando encerra o episódio.
- **Função de Custo / Objetivo:** Maximizar o retorno esperado através do Teorema do Gradiente da Política:

$$\nabla_\theta J(\theta) = E_{P_\theta} \left[ \sum_{t=0}^{T} \nabla_\theta \ln P_\theta(A_t | S_t) \cdot G_t \right]$$

- **Otimização:** Subida de Gradiente (Gradient Ascent) nos parâmetros $\theta$ do algoritmo.
- **Pontos Negativos:**
  - **Alta Variância:** Como usa o retorno completo do episódio ($G_t$), o gradiente oscila drasticamente, tornando o treinamento lento e instável.
  - **Lentidão:** Exige a conclusão do episódio inteiro para realizar uma única atualização dos pesos (por causa do Monte Carlo).
  - **Convergência Lenta:** Pode ficar preso em máximos locais devido a atualizações ruidosas.

## Conceitos Usados no REINFORCE

### Política Parametrizada ($P_\theta$)

Em vez de buscar um valor numa tabela, o estado S passa por uma rede neural com pesos $\theta$ que produz uma distribuição de probabilidade sobre as ações:

$$P_\theta(a|s) = P(A_t = a \mid S_t = s, \theta)$$

- Para **ações discretas**, a saída da rede passa por uma função Softmax.
- Para **ações contínuas**, a rede prevê a média $\mu$ e o desvio padrão $\sigma$ de uma distribuição normal.

### Retorno Monte Carlo ($G_t$)

É a soma das recompensas obtidas durante todo o episódio t, aplicando o fator de desconto $\gamma$:

$$G_t = \sum_{k=0}^{t-1} \gamma^k R_{k+1}$$

### Log-Probabilidade e o Truque da Razão de Verossimilhança

Para maximizar a recompensa esperada $J(\theta) = E_{t \sim P_\theta}[R(t)]$, precisamos do gradiente $\nabla_\theta J(\theta)$. Pelo Teorema do Gradiente da Política, a derivada da expectativa pode ser calculada reescrevendo a derivada da probabilidade:

$$\nabla_\theta P_\theta(a|s) = P_\theta(a|s) \nabla_\theta \log P_\theta(a|s)$$

Isso permite converter o cálculo do gradiente em uma expectativa calculável a partir de amostras do ambiente.

## A Matemática do REINFORCE

Buscamos maximizar o desempenho esperado da política $J(\theta)$:

$$J(\theta) = E_{P_\theta} [G_0]$$

O Teorema do Gradiente da Política nos dá a direção exata de atualização dos parâmetros $\theta$:

$$\nabla_\theta J(\theta) = E_{P_\theta} \left[ \sum_{t=0}^{T} \nabla_\theta \log P_\theta(A_t|S_t) \cdot G_t \right]$$

A regra de atualização dos pesos $\theta$ via **Subida de Gradiente** é:

$$\theta = \theta + \alpha \sum_{t=0}^{T} \nabla_\theta \log P_\theta(A_t|S_t) \cdot G_t$$

Repare que ao invés do sinal de menos temos o sinal de + por ser gradiente ascendente e não descendente. Podemos desmembrar essa equação para entender a intuição:

$$\text{Atualização} = \alpha \cdot \underbrace{\nabla_\theta \log P_\theta(A_t|S_t)}_{\text{Direção para aumentar a probabilidade da ação}} \cdot \underbrace{G_t}_{\text{Magnitude e sinal da recompensa}}$$

- Se $G_t > 0$ (Retorno bom): Aumenta a probabilidade da ação $A_t$ no estado $S_t$.
- Se $G_t < 0$ (Retorno ruim): Diminui a probabilidade da ação $A_t$ no estado $S_t$.

## Passo a Passo

O treino ocorre executando episódios completos, armazenando os passos e aplicando a subida de gradiente ao final de cada episódio.

1. **Inicialização:** Inicialize os parâmetros $\theta$ da rede neural de política aleatoriamente.

2. **Execute um episódio:** seguindo a política atual $P_\theta$ e guarde cada passo ($S_i$, $A_i$, $R_{i+1}$).
    - A lista de todos os passos é importante para saber qual peso (retornos) cada ação teve na recompensa final.

3. **Cálculo de Retornos:** a partir da recompensa final R calcula o retorno de cada passo

  $$G_i = \sum_{k=0}^{T-1} \gamma^{k} R_{k+1}$$

4. **Backpropagation e Subida de Gradiente**
    - Calcula a log-Probabilidade de cada passo: $log P_θ(A_t | S_t)$
    - Perda do episódio: $L = - \sum_i log(P_i) * G_i$
    - Atualiza pesos θ da rede

    $$\theta = \theta + \alpha \sum_{t=0}^{T-1} \nabla_\theta \log P_\theta(A_t|S_t) G_t$$

5. **Repetição:** Repita os passos 2 a 4 para múltiplos episódios até a política convergir.
