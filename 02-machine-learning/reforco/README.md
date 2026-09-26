# APRENDIZADO POR REFORÇO

O **Aprendizado por Reforço** (Reinforcement Learning ou RL) é a vertente do Machine Learning voltada para a **tomada de decisões sequenciais**. Diferente do aprendizado supervisionado e do não supervisionado o Aprendizado por Reforço aprende por **tentativa e erro** através da **interação direta com um ambiente dinâmico**.

Se no aprendizado supervisionado nós damos um livro com perguntas e gabarito, e no não supervisionado entregamos apenas o livro sem respostas, no aprendizado por reforço nós colocamos o algoritmo em um robô ou videogame e dizemos: "Seus pontos sobem quando você faz algo bom e caem quando faz algo ruim. Descubra sozinho como tirar a pontuação máxima."

## Ciclo de Interação Agente-Ambiente

O algoritmo de Aprendizado por Reforço é estruturado em torno do modelo de **Processos de Decisão de Markov (MDP)**. O agente opera em um ciclo contínuo de 4 elementos:

1. **Agente:** O algoritmo/modelo.
2. **Ambiente:** O mundo onde o agente opera (o jogo, o mercado financeiro, o simulador físico).
3. **Estado ($S_t$):** A situação do ambiente no momento t.
4. **Ação ($A_t$):** O movimento ou escolha feita pelo agente no momento t.
5. **Recompensa ($R_t$):** O sinal numérico devolvido pelo ambiente (escalar) que avalia o quão boa ou ruim foi a ação $A_t$ ao sair do estado $S_t$.

O agente (modelo) mede com seus sensores como o ambiente a sua volta está e decide por uma ação a fazer. Ele faz uma ação e com ela altera o ambiente (ou altera sua relação com ele, se movendo por exemplo). Ele mede através de sensores como o ambiente ficou após sua ação e recebe uma pontuação (recompensa) sobre essa ação. Com essa recompensa ele sabe se tomou uma boa decisão ou não e toma uma nova decisão sobre sua próxima ação.

**Exemplos Práticos**:
- **Jogos (AlphaGo, Atari):** O agente escolhe botões/jogadas para maximizar a pontuação final do jogo.
- **Robótica:** O agente ajusta o torque dos motores para aprender a andar sem cair.
- **Sistemas de Recomendação:** Ajustar respostas de LLMs (como ChatGPT) usando feedback humano como sinal de recompensa.

> **Objetivo**: Encontrar uma **Política (P)** otimizada que indique qual ação tomar em cada estado para **maximizar a recompensa acumulada** ao longo do tempo. Isso é feito testando e maximizando os parâmetros internos da política até achar o melhor valor (semelhante ao gradiente descendente atualizando os pesos).

## Diferença para o Aprendizado Supervisionado e Não Supervisionado

| Característica | Aprendizado Supervisionado | Aprendizado Não Supervisionado | Aprendizado por Reforço |
| :--- | :--- | :--- | :--- |
| **Fonte de Sinal** | variável com saída esperada (Y) | Nenhum sinal externo | **Recompensas numéricas** (R) esparsas/atrasadas |
| **Origem dos Dados** | Dataset estático e pré-coletado | Dataset estático e pré-coletado | **Dinâmica e gerada em tempo real** pela interação |
| **Dependência Temporal** | Amostras são assumidas como independentes | Amostras são assumidas como independentes | **Altamente dependente** (Ações alteram o estado futuro) |
| **Foco do Modelo** | Mapeamento X -> Y (Previsão) | Mapeamento X -> Estrutura (Agrupamento/Compressão) | Mapeamento S -> A (**Ação / Tomada de Decisão**) |
| **Feedback** | Imediato e correto | Ausente | Atrasado e avaliativo (não instrucional) |

Outras diferenças cruciais são que a maioria dos algoritmos de **aprendizado por reforço usam redes neurais** como parte obrigatória deles. Não há manipulação de dados estáticos (variáveis X ou Y). O loop de treinamento é trocado por um loop de simulação ou interação (que costumam repetir milhões de vezes e exigir multi-thread).

## Hiper-Parâmetros

- **Fator de Desconto ($\gamma$)**: para quando a recompensa é tardia
- **Taxa de Aprendizado ($\alpha$)**
- **Taxa de Exploração (e)**: taxa de exploração 
- **Tamanho do Replay Buffer**
- **Coeficiente de Entropia**

## Relação com os Dados

No RL não existe uma matriz de dados X estática baixada antes do treino. Os dados são criados **dinamicamente** na forma de **Trajetórias ou Episódios** ($\tau$):

$$\tau = (S_0, A_0, R_0, S_1, A_1, R_1, ..., S_T)$$

Cada interação gera uma tupla de transição: $(S_t, A_t, R_{t+1}, S_{t+1})$. 

- **Algoritmos On-Policy:** Usam os dados da transição instantaneamente para atualizar o modelo e depois os **descartam os dados após o uso**. Apenas interações geradas pela política atual são válidas (como em uma Cadeia de Markov tradicional).
- **Algoritmos Off-Policy:** Armazenam milhões de tuplas passadas em uma memória chamada **Replay Buffer** (D) e fazem amostragem em mini-lotes para treinar, aumentando a eficiência de amostra.

> Por conta disso **NÃO EXISTE DADOS DE TREINO E TESTE** no sentido tradicional, pois não há um dataset fixo previamente conhecido que possamos dividir. Em vez disso, a relação com dados ocorre da seguinte forma:

1. **Fase de Treinamento (age no mundo)** 
  - O agente interage com o ambiente adicionando **ruído de exploração** para descobrir novos caminhos e recompensas.
  - Ex: escolhendo ações aleatórias com probabilidade e.
  - Gera dados para serem avaliados.
2. **Fase de Avaliação (analisa como o mundo mudou)** 
  - O agente executa a política buscando zerar o ruído de exploração e com isso medir o desempenho real acumulado.
  - Processa os dados gerados na fase anterior
  - Analisa como o mundo mudou e se melhorou ou não sua situação.
3. **Generalização em Ambientes Não Vistos** 
  - Testa se o agente realmente aprendeu ou apenas memorizou a simulação (overfitting).
  - Altera-se as **sementes aleatórias (seeds)** do ambiente, muda os mapas de início ou utiliza-se cenários do mundo real (diferentes do simulador de treino).

---

## Componentes Principais

### Recompensa

A cada ação que fazemos recebemos uma recompensa, que nos diz o quão boa foi essa ação. A recompensa pode ser tardia (faço a ação agora mas só vou descobrir se ela foi boa depois). Mas o importante é entender que agir no ambiente significa ganhar ou perder pontos conforme a ação foi benéfica ou não. 

Diferentes ações e/ou consequências podem dar recompensas diferentes. Ex: bater o carro na parede pode dar -1000 de recompensa enquanto pegar um tanque de combustível dá 100 e se afastar da linha de chegada dá a distância que se está do destino. Um dos desafios do aprendizado por reforço é criar pontuações que reflitam os pesos dessas ações. Uma pontuação desbalanceada fará seu modelo aprender errado e priorizar comportamentos diferentes do esperado. Ex: ele pode escolher ficar parado porque é mais seguro que correr o risco de bater na parede. 

Ficar atento ao valor e a diferença entre eles é essencial. No exemplo do carro, se a pista de corrida tem 10km, andar 1 metro na direção certa e ganhar 1 ponto pode afetar muito pouco perante o risco de batida, merecendo um valor maior por metro.

### Episódio

Episódio é uma simulação. Durante o aprendizado fazemos centenas ou até milhares de simulações aonde o modelo testa diversos caminhos. Cada simulação é chamada de episódio. 

Podemos entender o episódio também como uma sequência de ações desde o início até o fim da interação, quando algum objetivo é alcançado ou o modelo encerra. Todos os passos dados do início até acabar a interação com o ambiente é o episódio e essa unidade é crucial quando a recompensa só é dada ao final da simulação (quando só sabemos se deu certo ao finalizar).

### Política (p)

É o algoritmo usado pelo modelo. Também chamado de estratégia, política ou algoritmo. É ele que define qual ação tomar para cada cenário. A política pode ser:

- **Política Determinística:** $p(a) = \mu(s)$
- **Política Estocástica:** $p(a|s) = P(A_t = a \mid S_t = s)$

Em contextos simples (como no aprendizado **baseado em valor**) a política pode ser só uma tabela (**tabela Q**), onde cada linha é um cenário e as colunas as ações possíveis. Nesses cenários você deve conhecer todos os cenários de antemão e todas as ações possíveis de serem feitas em qualquer momento. Algoritmos mais complexos montam essa tabela conforme explora o ambiente. Esse tipo de modelo é chamado de Aprendizado Q (Q-learning).

Em cenários reais complexos o algoritmo/política é uma rede neural aonde a entrada é o cenário atual e a saída é a ação a ser tomada.

> **O OBJETIVO FINAL DE TODO RL** é **ajustar os parâmetros da política** ao longo de milhares de simulações até encontrar a Política Ótima (maximizá-la). A função de otimização portanto busca definir os melhores parâmetros do algoritmo.

> OBS: TODO APRENDIZADO POR REFORÇO POSSUI POLÍTICA, MESMO AQUELES QUE NÃO SÃO BASEADOS EM POLÍTICA

### Função de Valor (V e Q)

Função matemática que diz o quão bom é estar naquele estado ou tomar uma ação específica naquele estado. Existem duas funções de valor: a de permanecer no estado atual (V) e a de tomar uma certa ação em certo estado (Q).

A função de permanecer no estado (V) costuma ser representada como V(s). A função de tomar uma ação costuma ser representada como Q(s, a).

### Entropia

A entropia é o grau de incerteza que a política (modelo) tem sobre o que fazer. Em outras palavras, entropia é a aleatoriedade das ações tomadas pelo agente. **Quanto menor a entropia, melhor** (mais certo está do que está fazendo).

No início a entropia/aleatoriedade é alta, pois estamos explorando e descobrindo o mundo. Quando a entropia é alta a distriuição de ações é uniforme (todas as ações possíveis tem a mesma chance de ocorrer). 

Conforme aprendemos a entropia cai e a distribuição de ações cria picos (algumas ações são mais prováveis que outras). O objetivo é que a entropia seja **baixa e estável ao final**.

## Frequência das Recompenas

A depender do que está fazendo as recomepensas podem vir logo após a ação (Ação -> Recompensa -> Ação), podem vir durante a execução mas muito depois (com atraso) ou podem vir só ao final da execução (quando encerra o modelo). As vezes você até pode escolher entre as três opções, modelando de forma diferente a IA conforme julgar melhor.

Exemplos: 

- No xadrez você sabe imediatamente se uma ação é boa ou ruim calculando o número de casas que está atacando e de aberturas que cria. 
- Uma IA que pousa um foguete só pontua ao final (pousou com sucesso ou não) pois não é possível mensurar se cada pequeno passo foi benigno ou não.
- Uma IA que joga Mário pode pontuar só no final (venceu: +1 ou morreu: -1) ou receber recompensas mais imediatas (uma conta que leve em consideração o distância do ponto final e o tempo restante).
- Uma IA que controle o fluxo de tráfego de uma cidade decide fechar uma pista. As consequências dessa ação só se mostram 5 horas depois (imaginando que a IA lê o estado do ambiente a cada minuto, é uma eternidade depois).

Dar um **retorno imediato** permite o modelo aprender exatamente cada pequena ação, porém **exige que o programador defina o peso e qualidade de centenas de pequenas ações**. Ela pode cair facilmente no **viés de modelagem** (quando modela as recompensas errado ou a partir de opiniões próprias).

Dar **recompensas atrasadas** ou só ao final evita o viés e hiper-modelagem do ambiente, porém cria um novo problema: a **atribuição de culpa** (na literatura chama de crédito).

### Atribuição de Culpa/Crédito

Esse é um dos maiores desafios do RL (junto com decidir entre explorar e exploitar). Como saber exatamente qual das centenas de ações tomadas ao longo do tempo foi a verdadeira responsável pelo sucesso ou fracasso final? Esse problema é resolvido através de três mecanismos principais:

1. **Fator de Desconto ($\gamma$)**

Propaga a recompensa do futuro de volta para o passado, ponderando que ações mais antigas têm uma fatia de responsabilidade no resultado final. Ele atribiu culpa parcial a cada ação. O desafio é saber quanto de culpa dar a cada passo.

2. **Função de Valor (Q ou V)**

Aprende a estimar quão bom é estar em certos estados e fazer certas ações em certo espaço. Isso torna possível saber se uma ação é boa ou não sem receber a recompensa imediata.

3. **Diferença Temporal (TD Learning) e Eligibility Traces**

Atualizam os estados anteriores com base na mudança de expectativa a cada passo, repassando a "culpa" da recompensa final para as ações passadas que construíram aquele cenário.

## PASSO-A-PASSO

- Inicializa os hiper-parâmetros (tabela Q com valores 0, e com valor máximo...) e define um estado inicial
- Para cada episódio/simulação
  - Reinicia o ambiente (mas mantém a função, política ou tabela)
  - Reinicia a contagem de ações
  - Enquanto não chegar ao objetivo ou estourar o limite de ações
    - Escolhe uma ação (a partir do parâmetro e - que escolhe entre explorar e explotar -, o estado atual, modelo, função, política e/ou tabela Q)
    - Faz a ação
    - Calcula a recompensa
    - Atualiza a tabela, função ou política (a partir da recompensa, estado e ação)

## Tipos de RL

O RL se divide em quatro grandes paradigmas de acordo com como o algoritmo aprende a tomar decisão:

1. **Baseados em Valor (Value-Based):** Aprendem a estimar a função de valor Q(s, a) e escolhem a ação de maior valor.
  - Pontua quão bom é cada estado e escolhe o estado disponível com maior ponto.
  - Usa Tabela Q.
2. **Baseados em Política (Policy-Based):** Otimizam a política $p_\theta(a|s)$ diretamente, sem precisar de uma tabela Q.
  - Busca os parâmetros internos $\theta$ (parâmetros da função política) que dão o melhor retorno.
3. **Ator-Crítico (Actor-Critic):** Mistura dos 2 tipos acima.
  - O Ator atualiza a política e o Crítico avalia a qualidade da ação.
4. **Baseados em Modelo (Model-Based):** Cria uma versão interna do mundo real (modelo) para planejar ações futuras antes de executá-las
  - Simula o mundo real e treina nele (carros autônomos, IAs que jogam xadrez para aprender...).
  - Ex: AlphaZero.

Na literatura você encontra muito a divisão entre os baseado em modelo e todo o resto, como se valor, política e ator fossem sub-tipos do tipo "sem modelo".

### Baseado em valor (Value-Based)

Estes algoritmos não aprendem a ação diretamente. Eles aprendem a prever o valor Q(s, a) para cada par estado-ação e, no momento da decisão, simplesmente escolhem a ação com maior Q ($\arg\max_a Q(s,a)$).

### Q-Learning

É o algoritmo clássico de RL, sendo o mais simples. Ele constrói uma tabela (Tabela Q) onde as linhas são estados e as colunas são ações. Ele atualiza esses valores usando o erro de **Diferença Temporal (TD Error)**.

- **Quando usar:** Problemas pequenos e discretos com poucos estados e poucas ações (ex: labirintos simples, jogos de tabuleiro em grade).
- **Tipo:** Off-Policy, Tabular, Model-Free.
- **Pontos Negativos:**
  - Inviável para espaços contínuos ou muito grandes (sofre com a "explosão dimensional" da tabela).
  - Inviável para ações contínuas (ex: girar o volante em $32.5$º).
- **Função de Custo / Equação de Atualização:** Baseada na Equação de Bellman:

$$Q(S_t, A_t)_{antigo} = Q(S_t, A_t)_{antigo} + \alpha \left[ R_{t+1} + \gamma \max_a Q(S_{t+1}, a) - Q(S_t, A_t)_{antigo} \right]$$

Onde:
- $\alpha$ é a taxa de aprendizado.
- $R_{t+1}$ é a recompensa da ação.
- $\gamma$ é Fator de Desconto (diminuição da recompensa devido aprendizado atrasado).
- $Q(S_t, A_t)$ é o valor da tabela.

Ou seja, atualiza a tabela a cada ação de acordo com as recompensas. Ao recebermos a recompensa sabemos quão bom foi essa ação nessa tal situação. Com isso atualizamos a tabela na posição de onde estávamos informando que aquela ação no estado anterior é boa/ruim nesse nível. A função de custo e otimização são a mesma.

### SARSA (State-Action-Reward-State-Action)

Muito semelhante ao Q-Learning, mas é um algoritmo **On-Policy**. Em vez de considerar a melhor ação da tabela ($\max_a Q(S_{t+1}, a)$), o SARSA utiliza a **ação real $A_{t+1}$** escolhida pela política (incluindo o ruído de exploração).

Seu nome é a sigla para Ambiente -> Ação -> Recompensa -> Ambiente -> Ação.

Podemos considerá-lo o Q-Learning cauteloso, pois é mais avesso a explorar e "toma menos risco".

- **Quando usar:** Quando o ambiente possui perigos mortais e o agente não pode se dar ao luxo de ser "otimista demais" durante o treino (ex: robô real andando perto de um precipício, mercado financeiro).
- **Tipo:** On-Policy, Tabular, Model-Free.
- **Pontos Negativos:**
  - Mais lento para encontrar a trajetória perfeita/ótima em comparação com o Q-Learning, pois é mais cauteloso.
- **Função de Custo / Equação de Atualização:** igual a do Q-learning.

### DQN (Deep Q-Network)

Substitui a tabela Q por uma **Rede Neural Profunda** que calcula o ganho de cada ação. A rede recebe o estado atual S (que pode ser uma imagem de pixels do ambiente) e gera as estimativas Q(S, a) para todas as ações possíveis. 

Para estabilizar o treino de redes neurais em RL, o DQN introduziu duas inovações cruciais: **Replay Buffer** e **Target Network**.

- **Quando usar:** Espaços de **estados complexos e contínuos** (imagens, sensores), mas com **ações discretas** (ex: jogos de Atari, mover para Esquerda/Direita/Pular).
- **Tipo:** Off-Policy, Baseado em Valor, Deep RL.
- **Pontos Negativos:**
  - Tende a superestimar os valores Q (corrigido posteriormente pelo Double DQN).
  - Incapaz de lidar nativamente com ações contínuas.
- **Função de Custo:** Erro Quadrático Médio (MSE) sobre o Erro TD:
- **Otimização:** Gradiente Descendente Estocástico (Adam/RMSprop) com os minibatches definidos pelo Replay Buffer.

### Baseado em política (Policy-Based)

Ao invés de estimar valores de ações para depois escolher a maior, estes algoritmos otimizam os parâmetros $\theta$ de uma política $p_\theta(a|s)$ **diretamente**.

### REINFORCE (Monte Carlo Policy Gradient)

O REINFORCE ajusta os parâmetros (pesos) quem aumentam a probabilidade das ações que resultaram em retornos acumulados altos ($G_t$) e diminuem a probabilidade das ações que geraram retornos baixos.

Seu comportamento é igual a de uma rede neural, aonde os parâmetros são pesos, a função de custo é uma derivada e a função de otimização é o gradiente descendente (que atualiza os pesos iterativamente igual o backpropagation).

- **Quando usar:** Quando as **ações são contínuas** (posso andar 3,45 cm a 18 graus de onde estou) ou problemas onde a política ótima é estocástica.
- **Tipo:** On-Policy, Policy Gradient, Monte Carlo.
- **Recompensa**: Só quando encerra.
- **Pontos Negativos:**
  - **Alta Variância:** Como usa o retorno completo do episódio ($G_t$), o gradiente oscila drasticamente, tornando o treinamento lento e instável.
  - Exige a conclusão do episódio inteiro para realizar uma única atualização dos pesos.
- **Função de Custo / Objetivo:** Maximizar o retorno esperado através do Teorema do Gradiente da Política:

$$\nabla_\theta J(\theta) = \mathbb{E}_{\pi_\theta} \left[ \sum_{t=0}^{T} \nabla_\theta \ln \pi_\theta(A_t | S_t) \cdot G_t \right]$$

- **Otimização:** Subida de Gradiente (Gradient Ascent) nos parâmetros $\theta$ do algoritmo.

### Baseado em modelos (Model-Based)

Enquanto os modelos anteriores apenas reagem ao estado, os algoritmos baseado em modelos tentam **aprender as leis do ambiente** (a função de transição P(S' | S, A) e a função de recompensa R(S, A)). Com isso, eles conseguem **simular o futuro em suas "mentes"** antes de agir no mundo real.

Esses modelos criam simulações do ambiente inteiro e se executam nele para aprender. Só depois são colocados no mundo real.

### AlphaZero / MCTS (Monte Carlo Tree Search)

Combina redes neurais profundas com a busca em árvore de Monte Carlo (MCTS). A rede neural prevê os valores dos estados e as probabilidades de jogada, enquanto a árvore MCTS realiza milhares de simulações do jogo para frente a partir do estado atual para selecionar o melhor movimento.

- **Quando usar:** Jogos determinísticos de informação perfeita com regras claras (Xadrez, Go, Shogi).
- **Tipo:** Model-Based / Planejamento por Busca em Árvore.
- **Pontos Negativos:**
  - Exige um simulador perfeito e determinístico do ambiente para realizar a busca na árvore.
  - Custo computacional de inferência extremamente alto por jogada.

### Dyna-Q e World Models (MBPO - Model-Based Policy Optimization)

O algoritmo aprende um modelo do mundo simultaneamente enquanto interage com o ambiente real. Em seguida, ele gera "experiências imaginárias" usando esse modelo interno para treinar o agente sem precisar gastar tempo no ambiente real.

- **Quando usar:** Quando interagir com o ambiente real é extremamente caro, perigoso ou demorado (ex: desgaste mecânico de robôs caros, testes clínicos).
- **Pontos Negativos:**
  - **Exploitation do Modelo:** Se o modelo do mundo aprendido cometer um pequeno erro, o agente aprenderá a explorar essa falha do modelo ("trapaceando" na simulação) e falhará miseravelmente quando testado no ambiente real.

### Ator-Crítico (Actor-Critic)

Em algoritmos do tipo Ator-Crítico a rede Ator representa a Política (decide a ação) e atualiza a política na direção indicada pelo Crítico. Já a rede Crítico representa a Função de Valor (avalia se a decisão da política foi boa ou ruim).

```
       +---------------------------------------------+
       |                  Ambiente                   |
       +---------------------------------------------+
          ^                                    |
          | Ação (A_t)                         | Estado (S_t), Recompensa (R_t)
          |                                    v
   +--------------+  Vantagem A(s,a)   +---------------+
   | ATOR (Policy)| <----------------- | CRÍTICO(FV)|
   +--------------+                    +---------------+
```

### A2C / A3C (Advantage Actor-Critic)

Usa a função de **Vantagem (A(s, a) = Q(s, a) - V(s))** em vez do retorno bruto $G_t$. A vantagem indica o quanto uma ação específica foi melhor do que a ação média esperada para aquele estado. Ele é executado em multi-threads para explorar as possibilidades de ação. Ele cria uma cópia do ambiente para cada thread para ser atualizada pelo respectivo modelo.

O **A2C** é a versão síncrona (espera todos os agentes paralelos terminarem o passo para só então atualizar a rede neural) enquanto o **A3C** é a versão assíncrona (todos atualizam uma rede central de forma assíncrona).

- **Quando usar:** Ambientes com aceleradores de hardware e necessidade de treinar em ambientes paralelos para diversidade de dados.
- **Tipo:** On-Policy, Actor-Critic.
- **Pontos Negativos:** Sensível à escolha de taxas de aprendizado entre o Ator e o Crítico.

### PPO (Proximal Policy Optimization)

É atualmente o **algoritmo padrão do estado da arte** para a maioria dos problemas de RL. O PPO resolve a instabilidade dos gradientes de política limitando o quanto a nova política pode se afastar da política antiga a cada atualização. Isso impede que o agente dê um "passo de gradiente desastroso" que destrua o aprendizado prévio.

- **Quando usar:** Algoritmo de uso geral excelente para **ações contínuas e discretas**, controle de robótica, jogos complexos e alinhamento de LLMs.
- **Tipo:** On-Policy, Actor-Critic.
- **Pontos Negativos:**
  - Por ser On-Policy, exige mais amostras totais de interação do que algoritmos Off-Policy.
- **Otimização:** Subida de gradiente estocástico com múltiplas épocas sobre minibatches de dados coletados.
- **Função de Custo:**

$$L(\theta) = \hat{E}_t \left[ \min\left( r_t(\theta)\hat{A}_t, \, \text{clip}(r_t(\theta), 1-e, 1+e)\hat{A}_t \right) \right]$$

Aonde 

- $r_t(\theta) = \frac{p_\theta(a_t|s_t)}{p_{\theta_{antigo}}(a_t|s_t)}$ é a razão de probabilidade entre a política nova e a antiga
- e é o parâmetro de corte (geralmente $0.1$ ou $0.2$).

### SAC (Soft Actor-Critic)

O SAC é um algoritmo Off-Policy focado em maximizar não apenas a recompensa acumulada, mas também a **Entropia da Política**. Isso força o agente a explorar o ambiente ao máximo e manter ações tão aleatórias quanto possível, desde que continuem cumprindo a tarefa.

- **Quando usar:** **Controle robótico contínuo** e cenários reais onde a **eficiência de amostras é crítica** e o ambiente exige alta robustez contra perturbações.
- **Tipo:** Off-Policy, Actor-Critic, Máxima Entropia.
- **Pontos Negativos:**
  - Alta complexidade matemática e muitos hiperparâmetros para ajustar.
  - Inviável para espaços de ações discretas na sua formulação padrão.
- **Função de Custo / Objetivo:**

$$J(p) = \sum_{t=0}^{T} E_{(s_t, a_t) \sim \rho_p} \left[ R(s_t, a_t) + \alpha H(p(\cdot | s_t)) \right]$$

Aonde: 

- H é a Entropia da política 
- $\alpha$ é o parâmetro de temperatura que controla o peso da exploração.

## Dilema Exploração vs. Explotação

- **Exploração (Exploration):** Tentar ações desconhecidas para descobrir se elas levam a recompensas maiores no futuro.
- **Explotação (Exploitation):** Escolher as ações que o agente já sabe que geram altas recompensas com base no conhecimento atual.

O equilíbrio entre os dois é o dilema central do aprendizado por reforço. Sempre haverá a questão entre fazer o que já se sabe que é bom ou tentar algo novo (trocar o certo pelo duvidoso).

1. **Quando focar em Explorar**:

- Início do treinamento
- Ambiente com recompensas esparsas: quando a recompensa só vem após muitas ações (como labirinto ou xadrez)
- Quando o ambiente e as regras mudam com o tempo (ex: mercado financeiro. O que dava certo ontem hoje não dá). O **conhecimento fica obsoleto**.

2. **Quando focar em Explotar**:

- Quando a entropia é baixa e há pouca instabilidade.
- Quando está em produção (o sistema já aprendeu e não queremos que ele saia agindo como no momento 0 ao por em produção)
- Quando estamos próximos do limite de passos (já estamos no final, vamos com o que temos)
- Quando estamos no meio do treino e o tempo é curto ou temos pouco orçamento (precisamos encerrar logo o treino)

Existem diversos algoritmos que escolhem entre as duas abordagens:

- Bônus de Entropia
- Softmax
- Limite Superior de Confiança (UCB)
- Amostragem de Thompson (abordagem bayesiana)

### Bônus de Entropia

***TODO***

### Softmax

***TODO***

### Limite Superior de Confiança (UCB)

***TODO***

### Amostragem de Thompson (abordagem bayesiana)

***TODO***

### Resumo Comparativo

| Estratégia | Tipo de Decisão | Ponto Forte | Ponto Fraco |
| :---       | :---            | :---        | :---        |
| Softmax | Probabilística (proporcional ao Valor) | Atribui probabilidades com base no valor estimado; evita explorar ações sabidamente ruins. | Sensível à escala das recompensas e exige o ajuste fino do parâmetro de Temperatura (T). |
| UCB | Determinística (guiada por Incerteza) | Eficiente; prioriza o que é menos conhecido. | Difícil de escalar para espaços de estados contínuos. |
| Thompson | Probabilística (Bayesiana) | Altamente eficiente no uso de dados. | Requer modelagem matemática das distribuições. |
| Bônus de Entropia | Contínua na Função Objetivo | Padrão da indústria em RL Profundo | Requer ajuste fino do bônus de entropia B |

## Métricas de Qualidade e Comparação entre Modelos

Métricas tradicionais Acurácia, R² ou Erro Quadrático Médio não funcionam aqui. Para medir o sucesso global da política, o RL utiliza métricas focadas no acúmulo de recompensa e estabilidade:

***TODO*** (entender melhor e disecar elas)

### 1. Recompensa Acumulada/Total ($G_t$)
É a soma das recompensas obtidas ao longo dos episódios:

$$G_t = \sum_{k=0}^{\infty} \gamma^k R_{t+k+1}$$

Aonde: 
- $\gamma$ é o **fator de desconto** (dá mais valor a recompensas imediatas do que a recompensas no futuro distante). Vai de 0 a 0.9999999.
- R é recompensa de cada momento.

### 2. Curva de Aprendizado (Curva de Recompensa Média por Episódio)
Plota a recompensa total média obtida pelos episódios ao longo do tempo de treino.

- **Modelo Bom:** Apresenta uma curva ascendente estável que atinge um patamar alto (convergência).

- **Modelo Instável:** Apresenta oscilações drásticas (o agente aprende, desaprende e despenca o desempenho).

### 3. Eficiência de Amostra
Mede **quantos passos (interação no ambiente)** o modelo precisou para atingir uma determinada pontuação.

- Em robótica real ou simuladores lentos, o algoritmo com **maior eficiência de amostra é o vencedor**, mesmo que demore mais tempo computacional por passo. **O importante é tomar menos ações, não gastar menos tempo**.

### 4. Entropia da Política (H(p))
Mede a entropia, ou seja, o grau de incerteza que a política tem sobre o que fazer. **Um bom modelo vai aprendendo gradualmente, portanto a entropia deve cair lentamente e finalizar em um valor baixo ESTÁVEL.**

Um modelo ruim pode acontecer uma dessas 3 coisas:

- **Entropia despenca logo no início**: indica que o agente parou de explorar. 
  - Descobriu um mínimo local, descobriu uma forma de não ser punido e não faz mas nada ou então ganhou uma recompensa boa e se contentou com o pouco.
  - Ex: ficar andando em círculo para não bater em nenhuma parede.
  - **Como corrigir**: aumentar o coeficiente bônus de entropia B ou diminuir a taxa de aprendizado.

- **Entropia alta sempre**: indica que o modelo não aprendeu nada.
  - Não consegue encontrar nenhuma ação positiva, portanto não converge.
  - Causas: falta de feedback ou recompensas muito esparsas.
  - **Como corrigir**: diminuir o coeficiente bônus de entropia B ou aumentar a taxa de aprendizado.

- **Entropia instável**: indica que o sistema aprende e desaprende toda hora.
  - O gráfico tem quedas e picos toda hora, ficando todo irregular.
  - O agente estava aprendendo bem, mas uma atualização de gradiente muito agressiva destrói os pesos da rede neural, fazendo-o esquecer o que aprendeu.
  - **Como corrigir**: diminuir a taxa de aprendizado ou aumentar o tamanho dos lotes (batches).

## COMPARATIVO GERAL DOS ALGORITMOS DE RL

| Algoritmo | Tipo | Espaço de Ações | Eficiência de Amostra | Estabilidade de Treino | Casos de Uso Principais |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q-Learning** | Model-Free / Value | Discreto | Baixa | Alta | Problemas de grid simples, didático |
| **DQN** | Model-Free / Value | Discreto | Média | Média | Jogos retrô (Atari), decisões discretas |
| **REINFORCE** | Model-Free / Policy | Discreto / Contínuo | Muito Baixa | Baixa | Problemas simples de controle, didático |
| **PPO** | Model-Free / Actor-Critic | Discreto / Contínuo | Média | **Muito Alta** | **Padrão da Indústria, Robótica, RLHF** |
| **SAC** | Model-Free / Actor-Critic | Contínuo | **Muito Alta** | Alta | Robótica real, controle de precisão |
| **AlphaZero** | Model-Based / Tree Search | Discreto | Alta (com simulador) | Alta | Jogos de tabuleiro (Go, Xadrez) |