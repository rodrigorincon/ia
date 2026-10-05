# APRENDIZADO POR REFORÇO: FAMÍLIA ATOR-CRÍTICO

A família Actor-Critic (Ator-Crítico) é uma união do policy-based e value-based, juntando o melhor das duas abordagens. Ele foi criado justamente como uma evolução ao policy-based, que por conta de sua alta variância não funcionava bem. 

Enquanto os métodos baseados em valor sofrem para lidar com altas dimensões e os baseados em política sofrem com alta variância estatística, o Ator-Crítico resolve ambos os problemas usando o poder do Valor para orientar a Política, sem perder as vantagens que a política traz.

O "Ator" é responsável por **escolher a ação e atualizar os parâmetros da política**. Ele é a parte policy-based, herdando a flexibilidade desse grupo para lidar com espaços contínuos e ambientes aleatórios. Ele é o motor do algoritmo, que faz as decisões inteligentes.

O "Crítico" **avalia quão boa foi a ação tomada, estimando uma função de valor (V(s) ou Q(s, a))**. Ele é a parte value-based. Ele é o balizador, orientando o ator em cada passo, reduzindo drasticamente a variância e acelerando a convergência.

- Ator = Policy-Based (ajusta os pesos $\theta$ da rede)
- Crícico = Value-Based (ajusta a função/tabela V ou Q)

Ao invés de usar retornos inteiros de Monte Carlo (como no REINFORCE), o Ator atualiza sua política usando as estimativas do Crítico. Isso **reduz drasticamente a variância dos gradientes** mantendo um aprendizado estável e contínuo.

## Diferença Entre os Algoritmos

Os algoritmos variam em **como estruturam essa cooperação e controlam a estabilidade do aprendizado**. Abordagens clássicas como o A3C utilizam múltiplos agentes rodando em paralelo para explorar o ambiente e atualizar uma rede central. O PPO e o TRPO definem restrições matemáticas e **limites na função de perda**, o que impede o ator de fazer atualizações muito agressivas na política. Isso garante que o aprendizado seja estável e não destrua o progresso anterior. 

Outras variações, como o SAC, integram ainda a maximização da entropia de forma automática para forçar o equilíbrio ideal entre exploração e explotação ao longo de toda a otimização.

## Conceitos Usados

### 1. Função Vantagem (Advantage Function - A(s,a))

A vantagem quantifica quão melhor foi tomar uma ação específica A no estado S em comparação com a ação média esperada para aquele estado:

$$A(s, a) = Q(s, a) - V(s)$$

Na prática, aproxima-se a vantagem usando a Estimativa de Vantagem Generalizada (GAE) ou o Erro TD de 1-passo:

$$\hat{A}_t = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$$

- Se $\hat{A}_t > 0$: A ação foi melhor do que a média. O Ator deve **aumentar** a probabilidade dessa ação.

- Se $\hat{A}_t < 0$: A ação foi pior do que a média. O Ator deve **diminuir** a probabilidade dessa ação.

### 2. Regularização por Entropia H(p)

A entropia é a medida de incerteza de uma distribuição de probabilidade. Adicionar a entropia à função de perda do Ator impede que a distribuição de probabilidade colapse rapidamente em uma ação determinística no início do treino:

$$H(P(\cdot \mid S_t)) = -\sum_a P(a \mid S_t) \log P(a \mid S_t)$$

### 3. Estimativa de Vantagem Generalizada (GAE - Generalized Advantage Estimator)

Utilizada intensamente pelo PPO e A2C, a GAE combina o tradeoff entre viés e variância ao ponderar erros TD de múltiplos passos com os parâmetros $\gamma$ (desconto) e $\lambda$ (suavização GAE):

$$\hat{A}_t^{GAE(\gamma, \lambda)} = \sum_{l=0}^{\infty} (\gamma \lambda)^l \delta_{t+l}^V$$

Onde $\delta_t^V = R_{t+1} + \gamma V(S_{t+1}) - V(S_t)$ é o erro TD básico.

## Passo a Passo Geral

1. **Inicialização:** Inicialize aleatoriamente os parâmetros do Ator ($\theta$) e do Crítico ($w$).

2. **Interação com o Ambiente:** O agente observa o estado $S_t$, passa pela rede do Ator $P_\theta(A_t \mid S_t)$ e seleciona uma ação $A_t$.

3. **Cálculo da Avaliação:** O ambiente retorna a recompensa $R_{t+1}$ e o novo estado $S_{t+1}$. O Crítico calcula a estimativa de valor $V_w(S_t)$ e $V_w(S_{t+1})$.

4. **Cálculo do Sinal de Feedback:** Calcula-se a Vantagem $\hat{A}_t$ ou Erro TD $\delta_t$:

$$
\hat{A}_t = R_{t+1} + \gamma V_w(S_{t+1}) - V_w(S_t)
$$

5. **Atualização do Crítico:** Atualiza-se os pesos do Crítico para minimizar o erro entre seu valor estimado e a recompensa real obtida.

6. **Atualização do Ator:** Atualiza-se os pesos do Ator na direção que aumenta as chances das ações que obtiveram vantagens positivas ($\hat{A}_t > 0$).

7. **Repetição:** Repita o processo até a política e a função de valor convergirem.

## Matemática

A atualização dos parâmetros do Ator ($\theta$) é guiada pela direção do gradiente ponderada pela vantagem calculada pelo Crítico:

$$\nabla_\theta J(\theta) = E_{P_\theta} \left[ \nabla_\theta \log P_\theta(A_t \mid S_t) \cdot \hat{A}_t \right]$$

A atualização dos parâmetros do Crítico ($w$) busca minimizar o Erro Quadrático Médio do valor previsto em relação ao retorno observado $y_t$:

$$L(w) = \frac{1}{2} \left( y_t - V_w(S_t) \right)^2 \quad \text{onde } y_t = R_{t+1} + \gamma V_w(S_{t+1})$$

### A Regra de Atualização em Conjunto

$$\theta = \theta + \alpha_{actor} \nabla_\theta \log P_\theta(A_t \mid S_t) \cdot \hat{A}_t(S_t, A_t)$$

$$w = w + \alpha_{critic} \left( R_{t+1} + \gamma V_w(S_{t+1}) - V_w(S_t) \right) \nabla_w V_w(S_t)$$

## Resumo

- **Quando usar:** Algoritmos da família Ator-Crítico (especialmente PPO e SAC) são as escolhas padrão na maioria dos problemas modernos de aprendizado por reforço devido à alta estabilidade e flexibilidade para lidar com ações discretas e contínuas.
- **Pontos Negativos:**
  - Exige sintonia cuidadosa do balanço de aprendizado entre Ator e Crítico.
  - Treinar redes neurais profundas para funções de valor e políticas simultaneamente pode levar a instabilidades se a taxa de aprendizado do Crítico for inadequada.
- **Função de Custo:** Combinada (Ator + Crítico + Entropia):

$$L(\theta, w) = L_{Actor}(\theta) + c_1 L_{Critic}(w) - c_2 H(P_\theta)$$

- **Otimização:** Subida/Descida de Gradiente Estocástica (Adam) com otimização conjunta via backpropagation.

## A3C (Asynchronous Advantage Actor-Critic)

O A3C foi introduzido pela DeepMind e utiliza múltiplos agentes (trabalhadores/workers) executando instâncias paralelas do ambiente em threads de CPU separadas.

Cada trabalhador interage com sua própria cópia do ambiente, calcula gradientes locais e atualiza de forma **assíncrona** uma rede neural global compartilhada. Essa arquitetura **substituiu a necessidade do Replay Buffer** (usado no DQN), pois a execução em paralelo de múltiplos trabalhadores quebra a correlação entre amostras temporais consecutivas.

Os algoritmos variam em **como estruturam essa cooperação e controlam a estabilidade do aprendizado**. Abordagens clássicas como o A3C utilizam múltiplos agentes rodando em paralelo para explorar o ambiente e atualizar uma rede central. O PPO e o TRPO definem restrições matemáticas e **limites na função de perda**, o que impede o ator de fazer atualizações muito agressivas na política. Isso garante que o aprendizado seja estável e não destrua o progresso anterior. 

Outras variações, como o SAC, integram ainda a maximização da entropia de forma automática para forçar o equilíbrio ideal entre exploração e explotação ao longo de toda a otimização.

- **Quando usar:** Ambientes simulados leves onde é possível rodar dezenas de cópias do ambiente simultaneamente em processadores multinúcleo (CPUs).

- **Tipo:** On-Policy

- **Pontos Negativos:**
  - Não aproveita eficientemente o paralelismo de GPUs devido às atualizações assíncronas em CPU.
  - Pode apresentar instabilidade se as atualizações assíncronas sobrescreverem parâmetros rapidamente (resolvido posteriormente pelo A2C, que é síncrono).
  - Ineficiência de amostras por ser On-Policy.

- **Função de Custo / Atualização:** Perda combinada do Ator e do Crítico com Regularização por Entropia:

$$L_{A3C}(\theta, w) = L_{Actor}(\theta) + c_1 L_{Critic}(w) - c_2 H(P_\theta(s))$$

## PPO (Proximal Policy Optimization)

O PPO é considerado o estado da arte quando se trata de aprendizado por reforço (incluindo o alinhamento de LLMs via RLHF). Ele resolve um problema crítico dos métodos de gradiente de política: **passos de atualização muito grandes podem destruir permanentemente o desempenho da política**.

O PPO contorna esse problema limitando o quanto a nova política $P_\theta$ pode se afastar da política antiga $P_{\theta_{old}}$. Em vez de usar restrições matemáticas complexas (como a divergência KL do TRPO), o PPO utiliza uma função de custo truncada (Clip).

As redes neurais do PPO costuma compilhar as mesmas camadas ocultas, economizando processamento, porém a camada de saída delas são diferentes. Na **rede Ator a função de saída deve ser softmax (para ações discretas) ou linear/tanh (para ações contínuas)**. Usa-se tanh quando se quer trnasformar a saída entre -1 e +1. Na **rede Crítico a função de saída deve ser sempre Linear**.

- **Quando usar:** Padrão para a maioria dos problemas de controle contínuo, robótica e alinhamento de modelos de linguagem onde se busca estabilidade e robustez a hiperparâmetros.
- **Pontos Negativos:**
  - Relativamente ineficiente em amostras pequenas (requer muitas interações por ser On-Policy).
  - Sensível à escala das recompensas e normalização das vantagens.
- **Função de Custo da Política (Clipped Objective):**

$$L^{CLIP}(\theta) = \hat{E}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \, \text{clip}(r_t(\theta), 1-\epsilon, 1+\epsilon)\hat{A}_t \right) \right]$$

Aonde 
- $r_t(\theta) = \frac{P_\theta(a_t \mid s_t)}{P_{\theta_{old}}(a_t \mid s_t)}$ é a razão entre as probabilidades da nova política e da antiga política. 

Se a razão $r_t(\theta)$ cresce além de $1+\epsilon$ ou diminui abaixo de $1-\epsilon$, o objetivo é cortado, impedindo atualizações exageradas.

## SAC (Soft Actor-Critic)

O SAC é um algoritmo **Off-Policy** projetado especificamente para espaços de **ações contínuas**, baseado na formulação de **Aprendizado com Entropia Máxima**.

Em vez de focar apenas em maximizar o retorno esperado de recompensas, o SAC maximiza simultaneamente a **entropia da política**. Encorajar alta entropia faz com que o agente explore ativamente ações alternativas e evite a convergência precoce para máximos locais.

- **Quando usar:** Robótica real e simulações complexas com espaços de ações contínuas, onde a eficiência de amostragem é prioritária.
- **Pontos Negativos:**
  - Inaplicável diretamente a espaços de ações discretas na sua formulação padrão.
  - Alto custo de ajuste dos coeficientes de temperatura da entropia ($\alpha$).
  - Treinamento computacionalmente mais pesado por utilizar múltiplas redes Q.
- **Objetivo de Entropia Máxima:**

$$J(P) = \sum_{t=0}^{T} E_{(s_t, a_t) \sim \rho_P} \left[ R(s_t, a_t) + \alpha \, H(P(\cdot \mid s_t)) \right]$$

Onde $H(P(\cdot \mid s_t)) = -\log P(a_t \mid s_t)$ é a entropia da política e $\alpha$ é a temperatura da entropia que controla o peso da exploração versus explotação.

## Tipo de Rede Neural

A arquitetura da rede neural é dividida entre o Ator e o Crítico. As redes podem compartilhar as camadas ocultas iniciais (especialmente quando processam imagens) ou ser inteiramente independentes.

- **Arquitetura Dual / Duas Cabeças:** Uma espinha dorsal comum (MLP ou CNN) extrai recursos do estado, conectando-se a duas saídas separadas:

  1. **Cabeça do Ator:** Saída Softmax (ações discretas) ou Média $\mu$ e Desvio Padrão $\sigma$ (ações contínuas).
  2. **Cabeça do Crítico:** Uma única saída escalar representando o Valor do Estado V(s). Usa a função de ativação Linear.

```
                      ┌───────────────┐
                      │ Estado (Input)│
                      └───────┬───────┘
                              │
                              ▼
                      ┌───────────────┐
                      │Camadas Ocultas│
                      │(MLP / CNN)    │
                      └───────┬───────┘
                              │
             ┌────────────────┴────────────────┐
             ▼                                 ▼
   ┌──────────────────┐              ┌──────────────────┐
   │  Cabeça do Ator  │              │ Cabeça do Crítico│
   │Dist. Prob. π(a|s)│              │  Valor V(s)      │
   └──────────────────┘              └──────────────────┘

```

- **Redes no SAC:** Utiliza redes separadas:
  - **Rede do Ator:** Gera parâmetros da distribuição normal multivariada (com truque de reparametrização).
  - **Duas Redes Críticas ($Q_1, Q_2$):** Recebem (s, a) e estimam o valor Q. Usa-se o mínimo min(Q_1, Q_2) para evitar superestimativa de valor.
