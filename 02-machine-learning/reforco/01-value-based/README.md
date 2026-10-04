# APRENDIZADO POR REFORÇO: FAMÍLIA VALUE-BASED

A família value-based (baseados em valor) tomam a decisão de qual ação fazer calculando indiretamente **quão bom é estar em um determinado estado ou executar uma ação específica**. 

Eles não definem uma política diretamente, ao invés disso eles aprendem uma função de valor do estado V(s) ou de estado-ação Q(s, a). Essa função é uma equação que calcula quão bom é estar em um determinado estado (no caso de V(s)) ou fazer determinada ação naquele estado (no caso de Q(s,a)) dado o que já aprenderam até o momento. **Essa função V ou Q são implicitamente sua política**.

Em muitos algoritmos esses valores V ou Q são armazenados numa tabela chamada tabela Q. Essa tabela é sua memória e aprendizado. É nela que fica guardado o conhecimento aprendido (qual o valor de cada ação em cada estado). Cada estado é uma tabela e cada ação é uma coluna. Assim, se quiser saber quão bom é uma ação A em um estado S é só olhar a linha e coluna respectivos.

## Diferença Para as Demais Famílias

- **Value-based comparam diretamente os valores calculados para cada ação disponível naquele estado**.
- Policy-based otimizam a política diretamente sem precisar de funções de valor V ou Q.
- Model-based aprendem as dinâmicas e probabilidades de transição do ambiente para planejar ações futuras.

## Diferença Entre os Algoritmos

Os algoritmos dessa família se diferenciam na forma de atualizar esses valores Q(s, a) e na capacidade de lidar com a dimensionalidade dos dados. 

Por exemplo: Q-Learning e SARSA mudam ligeiramente como atualizam a tabela Q. Já o DQN (Deep Q-Network) usam redes neurais para estabilizar a aprendizagem.

## Q-Learning

É o algoritmo mais clássico de aprendizado por reforço e o mais simples. Ele constrói uma tabela (Tabela Q) onde as linhas são estados e as colunas são ações. Ele atualiza esses valores usando o erro de **Diferença Temporal (TD Error)**.

- **Quando usar:** Problemas pequenos e discretos com poucos estados e poucas ações (ex: labirintos simples, jogos de tabuleiro em grade).
- **Tipo:** Off-Policy, Tabular, Model-Free.
- **Pontos Negativos:**
  - Inviável para espaços contínuos ou muito grandes (sofre com a "explosão dimensional" da tabela).
  - Inviável para ações contínuas (ex: girar o volante em $32.5$º).
- **Função de Custo / Equação de Atualização:** Baseada na Equação de Bellman

A atualização da tabela Q se dá através da equação de Bellman, onde **atualizamos a posição que estamos agora** (estado e ação de agora, não o estado que vamos e ação escolhida). Para atualizar usamos o melhor valor do **estado destino (próximo estado)**. Isso significa que quão melhor for o estado que vamos, melhor se torna o estado que o leva para ele.

$$Q(S_t, A_t) = Q(S_t, A_t) + \alpha \left[ R_{t+1} + \gamma \max_a Q(S_{t+1}, A) - Q(S_t, A_t) \right]$$

Podemos reescrever de forma mais simples assim

$$Pos_{atual} = Pos_{atual} + \alpha \left[ R + \gamma \max_a Pos_{futura} - Pos_{atual} \right]$$

Podemos desmembrar essa conta como em valor destino e diferença temporal:

$\text{ValorDesitno} = R_{t+1} + \gamma \max_a Q(S_{t+1}, a)$

$\text{TD Erro} = \text{ValorDesitno} - Q(S_t, A_t)$

Podendo simplifcar a quação para

$Q(S_t, A_t) = Q(S_t, A_t) + \alpha \text{TD Erro}$

Onde:
- $\alpha$ é a taxa de aprendizado.
- $R_{t+1}$ é a recompensa da ação.
- $\gamma$ é Fator de Desconto (diminuição da recompensa devido aprendizado atrasado).
- $Q(S_t, A_t)$ é o valor da tabela.

Ou seja, atualiza a tabela a cada ação de acordo com as recompensas. Ao recebermos a recompensa sabemos quão bom foi essa ação nessa tal situação. Com isso atualizamos a tabela na posição de onde estávamos informando que aquela ação no estado anterior é boa/ruim nesse nível. A função de custo e otimização são a mesma.

Modelar o que é um estado e como impedir que tenhamos dezenas de milhares de estados é o que faz desafiador programar esse algoritmo, exigindo criatividade e diversos testes do programador. Ex: um labirinto não é inteligente usar a coordenada das casas como estado, pois ao usar um labirinto novo com as paredes em outros lugares ou que seja maior a grande maioria das linhas da tabela não terão sido preenchidas.

## SARSA (State-Action-Reward-State-Action)

Muito semelhante ao Q-Learning, mas é um algoritmo **On-Policy**. Em vez de considerar a melhor ação do estado destino ($\max_a Q(S_{t+1}, a)$), o SARSA utiliza a **ação real a ser feita no próximo passo $A_{t+1}$** escolhida pela política (incluindo o ruído de exploração). Essa política é a função de escolha entre exploração e explotação.

Seu nome é a sigla para Ambiente -> Ação -> Recompensa -> Ambiente -> Ação.

Podemos considerá-lo o Q-Learning cauteloso, pois é mais avesso a explorar e "toma menos risco". Essa cautela é feita na hora de atualizar a tabela Q, usando a melhor ação possível para o próximo estado (ação com maior valor possível para aquele estado), ignorando o risco da exploração. 

No cálculo também deve considerar a ação escolhida e o próximo estado na hora de definir a parte ValorDesitno. Repare a minúscula diferença na equação de Bellman.

$$Q(S_t, A_t) = Q(S_t, A_t) + \alpha \left[ R_{t+1} + \gamma Q(S_{t+1}, A_{t+1}) - Q(S_t, A_t) \right]$$

Como falado, ele não assume que faremos a melhor escolha no próximo passo, mas sim já calcula a próxima ação (vê se pegaremos a melhor escolha ou faremos uma ação de exploração) antes de fazer a atualização.

- **Quando usar:** Quando o ambiente possui perigos mortais e o agente não pode se dar ao luxo de ser "otimista demais" durante o treino (ex: robô real andando perto de um precipício, mercado financeiro).
- **Tipo:** On-Policy, Tabular, Model-Free.
- **Pontos Negativos:**
  - Mais lento para encontrar a trajetória perfeita/ótima em comparação com o Q-Learning, pois é mais cauteloso.
- **Função de Custo / Equação de Atualização:** igual a do Q-learning.

### Comparação código Q-learning e SARSA

O exemplo usa a estratégia de exploração/explotação epsilon-greedy.

**Q-learning**

```python
while not done and passos < max_passos:
  if np.random.rand() < epsilon:
    action = np.random.choice(n_actions) # Exploração
  else:
    action = np.argmax(Q_table[state])   # Explotação (Melhor ação Q). Pega a melhor ação para a linha (estado/posição)

  # Executa ação no ambiente
  prev_state = state
  next_state, R, done = env.step(action)
  recompensa_total += R

  # Função de custo: atualiza a tabela Q a partir da equação de Bellman para Q-Learning
  best_next_action = np.argmax(Q_table[next_state])
  td_target = R + gamma * Q_table[next_state, best_next_action]
  td_error = td_target - Q_table[prev_state, action]
  Q_table[prev_state, action] += alpha * td_error

  state = next_state
```

**SARSA**

```python
state = initial_state

if np.random.rand() < epsilon:
  action = np.random.choice(n_actions) # Exploração
else:
  action = np.argmax(Q_table[state])   # Explotação (Melhor ação Q). Pega a melhor ação para a linha (estado/posição)

while not done and passos < max_passos:
  # Executa ação no ambiente
  next_state, R, done = env.step(action)
  recompensa_total += R

  if np.random.rand() < epsilon:
    next_action = np.random.choice(n_actions) # Exploração
  else:
    next_action = np.argmax(Q_table[state])   # Explotação (Melhor ação Q). Pega a melhor ação para a linha (estado/posição)

  # Equação de Bellman para SARSA (On-policy update using Q(S', A'))
  td_target = reward + gamma * Q_table[next_state, next_action]
  td_error = td_target - Q_table[state, action]
  Q_table[state, action] += alpha * td_error

  state = next_state
```

## DQN (Deep Q-Network)

Substitui a tabela Q por uma **Rede Neural Profunda** que calcula o ganho de cada ação. A rede recebe o estado atual S (que pode ser uma imagem de pixels do ambiente) e gera as estimativas Q(S, a) para todas as ações possíveis. Ou seja, a **rede tem uma saída para cada ação possível**. A saída de maior valor é escolhida como a ação a ser feita.

Foi pioneiro em 2013 quando a DeepMind o usou para ensiar uma IA a jogar jogos de Atari, recebendo os pixels da tela. Algoritmos mais avançados como PPO e A3C são melhores hoje.

D DQN **pode usar qualquer rede neural profunda**, mas ficou muito associada as redes neurais convolucionais por causa do seu uso pelo DeepMind para os jogos de Atari. O DeepMind escolheu a rede convolucional por ser adaptada para tratar imagens. Como a entrada era a tela do jogo naquele instante (uma matriz de pixels, uma imagem) essa arquitetura de rede era a ideal para esse fim. Mas isso não significa que ele funcione apenas com esse.

### Funcionamento da Rede Neural

A rede neural recebe como entrada o estado atual S (no caso do Atari, uma imagem), processa com a rede neural e retorna a função de valor Q(s, a) para cada ação. A saída 1 é o valor de realizar a ação 1 Q(s, a1) e assim por diante.

O treino da rede neural acontece através do erro da rede com a equação de Bellman. Após escolher a maior saída como ação a fazer, executa-se a missão e pegamos a recompensa junto do próximo estado. Com o retorno do ambiente (recompensa e próximo estado) calculamos a equação de Bellman igual no SARSA. A diferençe entre a equação e o valor Q(s,a) retornado pela rede (valor escolhido pela gente, referente a ação tomada) é o nosso erro. Esse **erro é a base da função de custo derivada pelo backpropagation para atualização da rede**. 

```
  ┌──────────────┐
  │    ESTADO    │
  │Imagem do jogo│
  │+Replay Buffer│
  └─────┬────────┘
        │
        ▼
  ┌─────────────┐
  │ Rede Neural │
  └─────┬───────┘
        │
        ▼
  ┌───────────────┐
  │ Saída da rede │
  │ Q1 Q2 Q3 ...  │
  └─────┬─────────┘
        │
        ▼
  EXECUTA AÇÃO Qi
        │
  ┌─────┴─────┐
  ▼           ▼
recompensa   próximo
  │           estado
  └─────┬─────┘
        ▼
Equação de Bellman
        │
        ▼
       erro (Bellman - Qi)
        │
        ▼
 Backpropagation
        │
        ▼
 atualiza pesos da rede neural
```

O cálculo da função de custo dessa rede é:

$$L = \frac{[y - Q(s,a)]^2}{2}$$

Aonde:
- y é a equação de Bellman (que usa a recompensa e o próximo estado após executarmos a ação no ambiente).
- Q(s,a) é a saída da rede neural para a ação escolhida.

É a partir dessa equação de custo que o backpropagation calcula a correção dos pesos. Repare que y - Q(s,a) é nosso erro: diferença entre o real (Bellman) e o previsto (saída da rede neural). Logo a função de custo é $\text{erro}^2/2$ e a derivada é o próprio erro. Minimizando o erro fazemos a rede se comportar igual a função de Bellman.

### Replay Buffer e Target Network

Para estabilizar o treino de redes neurais em RL, o DQN introduziu duas inovações cruciais: **Replay Buffer** e **Target Network**.

O Replay Buffer é uma memória onde o agente guarda suas experiências (conjunto de estado, ação, recompensa, estado seguinte e se concluiu). Cada experiência é um registro completo de onde estava, o que fez e o que aconteceu após sua ação. Ao treinar a rede normalmente ela **aprende apenas considerando o passo anterior, sem memória de todas as decisões que a levaram até lá**. Isso causa muita **instabilidade no treino**, dificultando encontrar um comportamento útil.

O que o **Replay Buffer faz é sortear um batch de X experiências passadas e usá-los no treino**.  As experiências passadas não precisam estar em ordem e não precisam ser próximas de si. Pode ser uma do início do episódio e uma do fim. Correlação temporal não é importante e deve ser quebrada nesse sorteio. Isso melhora a estabilidade e também permite reutilizar experiências antigas.

O **Target Network é uma cópia separada da rede principal** usada para calcular os valores-alvo do treinamento (equação de Bellman). Enquanto a rede principal recebe o estado atual e Replay Buffer, responde o próximo passo e atualiza seus pesos a cada passo, o Target Network busca calcular a função de Bellman para o estado atual, sem saber a ação e escolhida e o próximo estado. Ele é atualizado com menos frequência (geralmente a cada N iterações ou por cópia periódica dos pesos da rede principal). 

Essa separação é importante porque a equação de Bellman usa um valor futuro estimado, e se esse valor for calculado pela mesma rede que está sendo treinada o alvo muda continuamente durante o ajuste dos pesos. **Isso é outra causa de instabilidade** no aprendizado. Com a Target Network, a rede principal aprende a aproximar um alvo mais estável, enquanto a rede alvo fornece valores de referência mais consistentes. Em outras palavras, ela reduz a correlação entre o alvo e a própria atualização, tornando o treinamento do DQN muito mais robusto.

### Resumo

- **Quando usar:** Espaços de **estados complexos e contínuos** (imagens, sensores), mas com **ações discretas** (ex: mover para Esquerda/Direita/Pular).
- **Tipo:** Off-Policy, Baseado em Valor, Deep RL.
- **Pontos Negativos:**
  - Tende a superestimar os valores Q (corrigido posteriormente pelo Double DQN).
  - Incapaz de lidar nativamente com ações contínuas.
- **Função de Custo:** Erro Quadrático Médio (MSE) sobre o Erro TD:
- **Otimização:** Gradiente Descendente Estocástico (Adam/RMSprop) com os minibatches definidos pelo Replay Buffer.
