# APRENDIZADO POR REFORÇO: FAMÍLIA MODEL-BASED

A família model-based (baseados em modelo) toma a decisão de qual ação fazer **fazendo simulações em um modelo do ambiente.** Ele pode construir seu próprio ambiente virtual ou usar um externo, o importante é ter um modelo virtual do mundo real onde ele pode agir a vontade e aprender como se comportar nesse ambiente. Sua lógica é toda em torno dele **fazer simulações num ambiente virtual para aprender ao invés de interagir com o mundo real** e é isso que o diferencia de todos os demais, que agem direto no mundo real.

Ele é especial quando é muito caro ou difícil testar no mundo real (ex: IA de um satélite, robô que será mandado para o espaço ou carro autônomo). **Ele aprende com a simulação e depois que aprendeu é colocado no mundo real**. Por isso o modelo virtual precisa ser o máximo preciso, pois qualquer mínima diferença entre o modelo e a vida real pode ensinar a IA a agir errado, esperando comportamentos diferentes.

Isso também dá a essa família uma vantagem de **alcançar o objetivo com muito menos passos que os anteriores**.

## Modelo Virtual

Para criar o modelo é preciso construir ou usar duas funções fundamentais que descrevem a dinâmica do ambiente:

1. **Função de Transição de Estado T(s, a) = P(s' | s, a):** Preve qual será o próximo estado S' ao tomar a ação A estando no estado S.
2. **Função de Recompensa R(s, a):** Preve qual será a recompensa imediata recebida ao realizar essa transição.

**Essas funções formam o Modelo do Ambiente**. Importante ressaltar que essas **funções são probabilísticas**, então elas não dão 100% de certeza que é assim que o mundo real age. Isso permite o modelo ter certa flexibilidade no mundo real, estar preparado para cenários inéditose a rede neural retornar probabilidades para cada ação. 

O aprendizado e tomada de decisão ocorrem combinando a interação real, a atualização do modelo e o planejamento no modelo simulado.

## Diferenças Para as Demais Famílias

Model-based aprendem **as leis do ambiente e a função de recompensa**. Aprender as leis do ambiente (regras ou leis físicas) é feito através de redes neurais e dados sintéticos produzidos por modelos já conhecidos do mundo. Aprender as recompensas vai pela mesma linha. Ter de descobrir quantos pontos dar ou tirar, além de descobrir como o mundo funciona tornam essa família consideravelmente mais complexa que os demais.

## Diferença Entre os Algoritmos

As diferenças entre os algoritmos está em como consegue o modelo do ambiente (se o modelo é conhecido a priori ou aprendido via dados) e como o planejamento é executado (se para busca em árvore, para gerar experiências sintéticas ou para otimização contínua de trajetórias).

Quando o modelo do ambiente é conhecido de antemão (como as regras do xadrez ou Go) algoritmos de busca em árvore como o **Monte Carlo Tree Search (MCTS)** (usado no AlphaZero) exploram trajetórias futuras para selecionar a melhor ação. 

Quando o ambiente é desconhecido, redes neurais são usadas para aprender a física do mundo a partir de observações (como simulador de clima em meteorologia). Variações como o **MBPO** usam o modelo aprendido para gerar dados sintéticos e treinar agentes de política.

## Conceitos Usados nos Algoritmos Model-Based

### 1. Modelo de Transição e Recompensa

É a representação matemática do ambiente. Pode ser **analítico/exato** (regras do xadrez), **estatístico/tabular** (contagem de frequências no Dyna-Q) ou **aproximado por redes neurais** (MBPO):

$$\hat{s}' \sim T_\phi(s' \mid s, a), \quad \hat{r} = R_\phi(s, a)$$

### 2. Rollouts Sintéticos e Experiências Imaginadas

Em vez de interagir com o ambiente físico para coletar transições $(s, a, r, s')$, o agente executa sua política dentro do modelo dinâmico aprendido. Isso gera dados sintéticos em velocidade incomparavelmente maior do que no mundo real. Podemos usar esses dados para treinar novos modelos, dizendo como o ambiente se comporta nessas situações. Obviamente dados coletados do mundo real tem um peso muito maior que dados tirados de simulação.

### 3. Acúmulo de Erro de Previsão (Compounding Model Error)

É o principal obstáculo dos métodos model-based. Se um modelo tem um pequeno erro $\epsilon$ na previsão de um único passo, ao encadear k passos sequenciais no modelo, o erro se acumula exponencialmente:

$$\text{Erro Total} \approx O(k^2 \epsilon)$$

Isso faz com que o agente tome decisões ótimas dentro de um "mundo falso", resultando em péssimo desempenho no mundo real.

## Passo a Passo Geral

1. **Coleta de Dados:** O agente interage com o ambiente real usando a política atual P e armazena as transições (s, a, r, s') no histórico/buffer.
2. **Atualização do Modelo:** Utiliza a experiência acumulada no buffer para ajustar os parâmetros $\phi$ do modelo do ambiente $T_\phi$ e $R_\phi$ via minimização de erro de previsão (Supervisionado/MSE).
3. **Simulação / Planejamento:**
   - **Forma A (Busca no Tempo de Decisão - MCTS):** Simula trajetórias a partir do estado atual para selecionar a melhor ação imediata.
   - **Forma B (Geração de Dados Imaginados - Dyna/MBPO):** Utiliza o modelo atual para gerar um conjunto de dados simulados de transições futuras.
4. **Atualização da Política e/ou Valor:** Atualiza a função $Q(s, a)$, $V(s)$ ou a política $\pi_\theta$ utilizando os dados simulados (ou a combinação de simulados e reais).
5. **Repetição:** Repita o processo iterativamente.

## Resumo

- **Quando usar:** Quando a coleta de experiências no ambiente real é **extremamente cara, demorada, perigosa ou limitada** (robótica física, sistemas industriais) ou quando o ambiente já fornece um simulador exato e rápido (jogos de regras fixas).
- **Tipo:** Model-Based (pode ser integrado com técnicas On-Policy, Off-Policy, Tabular ou deep learning).
- **Pontos Negativos:**
  - Vítima do **Erro de Acúmulo do Modelo**: se o modelo for impreciso, o agente otimiza para um ambiente irreal (Model Exploitation).
  - Alto custo de processamento computacional para treinar modelos e gerar simulações constantes.
- **Função de Custo do Modelo:** Perda Supervisionada (Erro Quadrático Médio - MSE ou Negative Log-Likelihood) para aprender as transições e recompensas:

$$L(\phi) = \frac{1}{|B|} \sum_{(s,a,r,s') \in B} \left\| T_\phi(s,a) - s' \right\|^2 + \left( R_\phi(s,a) - r \right)^2$$

- **Otimização:** Descida de Gradiente Estocástica (Adam/RMSprop) para treinar o modelo de dinâmica neural, combinada com algoritmos padrão de controle (SAC, Q-Learning, Gradientes de Política) sobre as simulações geradas.

## MCTS (Monte Carlo Tree Search)

É o algoritmo clássico de planejamento baseado em árvore, usado no AlphaZero. Ele constrói assimetricamente uma árvore de busca expandindo apenas os ramos mais promissores, combinando a precisão da busca em árvore com a flexibilidade das simulações de Monte Carlo.

- **Quando usar:** Jogos de tabuleiro com regras e modelos perfeitos (ex: Xadrez, Go), cenários onde os estados são discretos.
- **Tipo:** Model-Based, On-Policy / Planejamento por Busca em Árvore.
- **Recompensa:** Avaliada ao final das simulações ou via funções de avaliação nos nós folha.
- **Pontos Negativos:**
  - Inviável para ambientes em tempo real com orçamentos computacionais muito baixos por passo de decisão.
  - Exige um modelo/simulador muito preciso; erros na dinâmica do modelo se acumulam na árvore.
  - Dificuldade nativa para lidar com espaços de ações contínuos.

### Funcionamento do MCTS

O MCTS repete essas 4 fases a cada tomada de decisão:

1. **Seleção:** A partir da raiz (estado atual), o agente navega pela árvore escolhendo nós usando a fórmula **UCT (variação do UCB para árvores)** para balancear exploração e explotação até atingir um nó folha não completamente expandido.
  - Escolher um nó filho é escolher entre explorar (um ramo não expandido) e explotar (seguir num ramo bem expandido).
2. **Expansão:** Adiciona um ou mais nós filhos ao nó folha selecionado, representando **ações ainda não exploradas**.
3. **Simulação (Rollout):** A partir do novo nó, executa uma simulação até o fim do episódio (ou até uma profundidade limite) escolhendo ações aleatórias ou heurísticas para obter uma estimativa de retorno.
4. **Backpropagation:** Atualiza as estatísticas de visitas N e recompensa acumulada R de todos os nós percorridos desde a raiz.

### Função de Seleção UCT

A escolha do nó na fase de Seleção utiliza a equação:

$$UCT = \frac{R(v)}{N(v)} + c \sqrt{\frac{\ln N(parent)}{N(v)}}$$

Onde:
- $R(v)$ é a recompensa acumulada no nó $v$.
- $N(v)$ é o número de vezes que o nó $v$ foi visitado.
- $N(parent)$ é o número de visitas do nó pai.
- c é a constante de exploração (geralmente $\sqrt{2}$).

### AlphaZero

É um programa da DeepMind que usa esse algoritmo. É uma evolução do Alpha Go (que venceu o campeão de Go), capaz de jogar qualquer jogo de tabuleiro. Seu sucessor, o MuZero, consegue além desses jogos jogar jogos de videogame como o Atari.

## Dyna-Q

O Dyna-Q é uma arquitetura clássica que unifica o **aprendizado direto** (aprendizado por reforço real) com o **planejamento** (aprendizado com modelo). 

Ele usa a experiência real coletada no ambiente para duas coisas simultaneamente:

1. Atualizar a tabela de valores $Q(s, a)$ diretamente (como o Q-Learning).
2. Treinar um modelo do ambiente $\text{Model}(s, a) \rightarrow (r, s')$.

Para usar esse algoritmo tem de ser possível transformar o ambiente em uma tabela como no Q-learning. Durante a fase de planejamento, o agente realiza N chamadas ao seu modelo aprendido, gerando transições hipotéticas para executar atualizações adicionais do Q-Learning.

- **Quando usar:** Ambientes discretos e tabulares onde a amostragem real é cara ou demorada, mas a dinâmica do ambiente pode ser memorizada rapidamente.
- **Tipo:** Off-Policy, Tabular, Model-Based.
- **Pontos Negativos:**
  - Limitado a estados e ações discretos (versão tabular).
  - Se o modelo aprendido for incorreto (devido a mudanças no ambiente), o planejamento com dados falsos pode degradar a política (problema mitigado pelo Dyna-Q+).
- **Função de Custo / Equação de Atualização:** Mesma equação de Bellman do Q-Learning, aplicada tanto nos dados reais quanto nos dados simulados:

$$Q(S, A) = Q(S, A) + \alpha \left[ R + \gamma \max_a Q(S', a) - Q(S, A) \right]$$

### Arquitetura do Dyna-Q

```
            ┌─────────────────────────────┐
            │       Experiência Real      │
            └──────┬───────────────┬──────┘
                   │               │
                   ▼               ▼
┌──────────────────────┐      ┌──────────────────────┐
│  Aprendizado Direto  │      │ Aprendizado do Modelo│
│  Atualiza Q(s,a)     │      │ Registra T(s,a),R    │
└──────────┬───────────┘      └──────────┬───────────┘
           │                             │
           │                             ▼
           │                  ┌──────────────────────┐
           │                  │   Modelo do Ambiente │
           │                  └──────────┬───────────┘
           │                             │
           │                             ▼
           │                  ┌──────────────────────┐
           │                  │  Planejamento (N x)  │
           │                  │  Gera (s,a) simulados│
           │                  └──────────┬───────────┘
           │                             │
           ▼                             ▼
┌────────────────────────────────────────────────────┐
│                  Tabela Q Atualizada               │
└────────────────────────────────────────────────────┘
```

## MBPO (Model-Based Policy Optimization)

O MBPO é um algoritmo moderno que usa redes neurais profundas projetado para resolver a principal falha dos métodos model-based profundos: a **propagação e acúmulo do erro do modelo**.

Em vez de gerar simulações longas no modelo neural (o que acumula imprecisões rapidamente e destrói o treinamento), o MBPO gera **trajetórias extremamente curtas (Short Rollouts)** a partir de estados reais coletados do ambiente e armazenados no buffer.

Essas experiências sintéticas curtas são combinadas com o buffer real para treinar um algoritmo de controle base (geralmente o **SAC - Soft Actor-Critic**).

- **Quando usar:** Problemas robóticos e de controle contínuo complexos onde a amostragem no ambiente real é extremamente cara, perigosa ou lenta.
- **Tipo:** Off-Policy, Deep RL, Model-Based / Actor-Critic.
- **Pontos Negativos:**
  - Alto custo computacional para treinar múltiplos modelos neurais em paralelo.
  - Hiperparâmetros sensíveis (tamanho das simulações sintéticas, proporção de dados reais vs. sintéticos).

### Ensemble de Modelos Neurais

Para evitar prever transições incorretas em áreas pouco exploradas do ambiente, o MBPO utiliza um **Ensemble de Redes Neurais Gaussiana** $\{M_{\phi_1}, M_{\phi_2}, \dots, M_{\phi_B}\}$.

Cada rede $M_{\phi_i}$ prevê a média $\mu_i(s, a)$ e a variância $\sigma_i^2(s, a)$ do próximo estado e recompensa:

$$P_{\phi_i}(s', r \mid s, a) = \mathcal{N}\left(\mu_i(s,a), \Sigma_i(s,a)\right)$$

A discordância entre as previsões das redes do ensemble indica **incerteza do modelo**. O MBPO usa essa incerteza para limitar o tamanho dos *rollouts* ou desacreditar simulações não confiáveis.

### Erro do Modelo e Limite de Simulações (k)

O MBPO prova teoricamente que o erro do retorno da política estocástica simulada $\eta(P)$ versus real $\eta_{real}(P)$ é limitado por:

$$\eta_{real}(P) \ge \eta_{simu}(\pi) - \left[ \frac{2\gamma \epsilon_{\text{mult}}}{1-\gamma} + \frac{2\gamma^2 \epsilon_{\text{model}}}{(1-\gamma)^2} \right]$$

Onde $\epsilon_{\text{model}}$ é o erro do modelo e k é a profundidade da simulação. Como o termo do erro cresce quadraticamente com a profundidade da simulação, o MBPO utiliza **horizonte curto (k pequeno, ex: k=1 a k=15)** a partir de estados reais distribuídos.

## Tipo de Rede Neural

A escolha da arquitetura de rede neural usada depende das entradas e do papel que o componente desempenha:

- **Dyna-Q:** Usa estruturas tabulares (dicionários/matrizes) tanto para a tabela Q quanto para o modelo determinístico.
- **MBPO:**
  - **Ensemble:** MLPs (ou CNNs para imagens)
  - **Redes de Política e Valor (SAC Base):** MLPs com saídas normais para o Actor e duplas redes Q para o Critic.
- **MCTS com Deep Learning (AlphaZero / MuZero):** CNNs processam a representação do estado/tabuleiro.

## Comparação Entre os Algoritmos da Família

| Característica | Dyna-Q | MCTS | MBPO |
| ----- | ----- | ----- | ----- |
| **Representação do Modelo** | Tabular / Frequência | Simulador Exato / Rede Neural | Ensemble de MLPs normais |
| **Estratégia de Uso do Modelo** | Planejamento em background (Background Planning) | Busca em Árvore em Tempo de Decisão (Decision-time Planning) | Gerador de Rollouts Curtos para ter uma lista de estados-recompensas Sintético |
| **Espaço de Ações** | Discreto | Discreto (Padrão) | Contínuo |
| **Mitigação do Erro do Modelo** | Nenhuma (assume ambiente estático/simples) | Sem erro (assume simulador exato ou refinado) | Ensemble de Modelos + Rollouts de Curtas Passadas ($k$) |
| **Eficiência de Amostras Reais** | Média | Baixa / Nula (necessita simulador) | **Extremamente Alta** |
