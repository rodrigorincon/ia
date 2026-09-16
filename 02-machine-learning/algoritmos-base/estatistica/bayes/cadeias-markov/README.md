# CADEIAS DE MARKOV

É um modelo probabilístico que descreve todos os estados de um sistema e a **probabilidade de mudar de um estado para o outro**. O ponto principal das cadeias de Markov são as probabilidades de sair de um estado e ir para outro. Ele é representado por um grafo aonde cada nó é um estado e as arestas as contém as probabilidades de eles migrarem desse ponto para o outro.

Importante ter em mente que nas cadeias de Markov o próximo estado **depende exclusivamente do estado atual**, ignorando todo o histórico de estados anteriores. Essa característica fundamental é conhecida como a falta de memória. 

As Cadeias de Markov **não são modelos treinados por iterações** (como gradiente descendente), mas sim estruturas matemáticas de modelagem estocástica baseadas em matrizes de transição e grafos de estados. O modelo calcula a probabilidade de um sistema evoluir de um estado A para um estado B através de uma matriz, onde cada linha representa a distribuição de probabilidade sobre os possíveis estados futuros.

## Glossário

### Espaço de Estados

É o conjunto de todos os valores possíveis que $X_i$ pode assumir. Costuma ser representado como S. Em outras palavras, **Espaço de Estados são os nós do grafo**.

Os estados podem ser qualquer coisa, a posição dum robô aspirador num mapa, um status de um objeto, as categorias da variável Y...

### Processo Estocástico

É a formalização matemática de um conjunto de variáveis aleatórias $X_0, X_1, X_2, ..., X_t$ ordenadas no tempo, representando a evolução de um sistema. Ele é `O QUE` descreve a dinâmica incerta do sistema ao longo do tempo.

**Objetivo**: Modelar a trajetória aleatória de um sistema através de um conjunto discreto ou contínuo de estados ao longo do tempo.

### Falta de Memória

Também chamada de **Propriedade de Markov**, é a **premissa simplificadora central** que permite fazermos algo com nossos dados. Ela diz que a distribuição de probabilidade do estado futuro $X_{t+1}$ depende **apenas do estado presente** $X_t$, tornando irrelevante o conhecimento da sequência histórica $X_0, X_1, ..., X_{t-1}$. Ela é o `COMO` reduzimos drasticamente a complexidade do cálculo de sequências temporais.

**Objetivo**: Transformar a probabilidade condicional conjunta de toda a história do sistema em uma probabilidade condicional simples entre dois passos consecutivos.

## Matriz de Transição

Ao invés de termos de montar um grafo, guardar em cada nó uma lista de nós vizinhos e salvar nessa aresta os valores dela, existe uma forma muito mais simples e computacionalmente rápida de fazer: colocar todos os pesos das arestas em matrizes.

Se o número de estados for discreto e finito a gente pode organizar todas as arestas em formato de matriz quadrada, onde cada linha e cada coluna representam um nó (estado). Assim se eu quero ir do estado A para o estado B basta olhar na matriz a linha A e coluna B que tenho a probabilidade dessa aresta. Caso não seja possível ir de um estado para o outro o valor dessa posição é 0. Também podemos ver que esse método cobre grafos bidirecionais. A aresta A->B é diferente de B->A. O primeiro vamos na linha A e coluna B, enquanto o outro vamos na linha B e coluna A, que dão em locais diferentes da matriz com valores diferentes.

A Matriz de Transição tem portanto tamanho NxN, sendo N o total de nós/estados. Ela é representada como P.

$$P = \begin{bmatrix}
P_{11} & P_{12} & \dots & P_{1N} \\
P_{21} & P_{22} & \dots & P_{2N} \\
\vdots & \vdots & \ddots & \vdots \\
P_{N1} & P_{N2} & \dots & P_{NN}
\end{bmatrix}$$

Onde podemos escrever a probabilidade em cada elemento como:

$$P_{ij} = P(X_{t+1} = S_j \mid X_t = S_i)$$

A equação acima é entendida da seguinte forma:

- T é o momento (passo) atual. Portanto no momento atual (T) estamos na posição i. 
- Estamos no estado $S_i$ e no próximo iremos para o estado $S_j$ 
  - Não confundir a posição com tempo. "i" e "j" são nossas posições no momento T e T+1. Portanto não podemos dizer que j = i + 1 por exemplo.
  - "i" e "j" seriam como RJ e SP e T seria como "dia 5". A equação seria "a probabilidade de ir de RJ para SP no dia 6".

Ou seja, a equação significa "probabilidade de estar no estado J dado que no momento anterior estou no estado "i"".

Um ponto importante de se notar é que o nó pode ter uma aresta apontando para ele mesmo. Isso significa que existe uma chance de não mudar de estado. Seria a probabilidade de tudo continuar como tá (continuar no estado atual). Todo nó pode ter uma aresta apontando para si, embora isso não seja obrigatório.

### Propriedades fundamentais da Matriz de Transição

1. **Todos os elementos são não-negativos** (afinal são probabilidades).
2. **A soma de cada linha é exatamente 1** (garantindo uma distribuição de probabilidade válida para a saída de qualquer estado).

A soma de cada linha tem de ser 1 por um motivo muito óbvio: a soma de todas as probabilidades possíveis tem de ser 1! Como a linha representa todos os estados possíveis de se estar (saindo de algum lugar) a soma deles dá 100% = 1. 

Isso mostra que nós temos outra **premissa: todos os estados possíveis foram mapeados**!

Porém o mesmo não é verdade para as colunas. As colunas representam as probabilidades de você chegar no estado J (J sendo a coluna) e a linha onde estava antes. Porém como você pode não estar em J em algum momento **a soma da coluna não tem obrigação de dar 1**. A soma pode inclusive ser maior que 1 ou menor que 1. A imagem abaixo demonstra isso bem.

> Visualizando essas regras em um grafo, a soma de todas as arestas que saem de um nó tem de dar 1, mas a soma das arestas que chegam não.

![](../images/markov1.png)

A matriz da imagem abaixo seria:

$$\begin{bmatrix}
---               & \text{Feliz} & \text{Estressado} & \text{Triste} \\
\text{Feliz}      & 0            & 0.4               & 0.6 \\
\text{Estressado} & 0.2          & 0.5               & 0.3 \\
\text{Triste}     & 0.1          & 0.4               & 0.5
\end{bmatrix}$$

### Relação entre Matriz de Transição e Matriz de Adjacência

Em teoria dos grafos, a matriz de transição P é formalmente a **Matriz de Adjacência Ponderada e Normalizada por Linha** do grafo de estados. Essa perspectiva topológica permite analisar propriedades da cadeia usando conceitos clássicos de grafos:

- **Componentes Fortemente Conectados:** É possível chegar em qualquer nó saindo de qualquer outro.
- **Estados Absorventes:** Um nó só tem aresta de saída para ele mesmo. Uma vez que entra nele nunca mais sai.
- **Período e Ciclos:** O período de um estado é o máximo divisor comum (MDC) do comprimento de todos os caminhos fechados (ciclos) que retornam a ele. Se o MDC for 1, o estado é **Aperiódico**.
- **Ergodicidade:** Quando é fortemente conectados e aperiódico o grafo garante a existência de uma única distribuição estacionária global, independentemente do estado inicial $p^{(0)}$.

## Evolução do Estado em N Passos

Se conhecemos a distribuição de probabilidade inicial do sistema no instante 0, representada por um vetor linha $p^{(0)}$, a distribuição de probabilidade no instante $1$ é dada pelo produto vetorial-matricial:

$p^{(1)} = p^{(0)} P$

Aonde P é a nossa matriz de transição.

Do mesmo modo, no momento 2 após ter realizado uma segunda ação a distribuição será:

$p^{(1)} = p^{(0)} P*P$

Pois teremos feito 2 ações (representado pela matriz). Como a matriz é a probabilidade de cada ação ser tomada, a minha posição após 2 ações é a posição inicial vezes 2 vezes a matriz de probabilidades.

Portanto a distribuição de probabilidade após N passos é a distribuição inicial vezes n-ésima potência da matriz de transição:

$$p^{(n)} = p^{(0)} P^n$$

Ao elevar a matriz por N temos a matriz de probabilidades de sairmos de qualquer posição e terminarmos em outra em N passos.

> Elevar a matriz a N é diferente de elevar seus valores a N. Você tem realmente de fazer matriz * matriz N-1 vezes.

## O Problema da Distribuição Estacionária (p)

Conforme o número de passos N vai para o infinito, muitas cadeias de markov se estabilizam. O sistema atinge um equilíbrio estatístico onde a distribuição de probabilidade entre os estados não muda mais ao aplicar a transição. Esse estado de equilíbrio é chamado de **Distribuição Estacionária** (p):

$$p^P = p$$

Significa que p é um **autovetor à esquerda** da matriz P associado ao autovalor $\lambda = 1$. Encontrar essa distribuição é fundamental para entender o comportamento de longo prazo do sistema.

## PREMISSAS

Para que uma Cadeia de Markov padrão (de primeira ordem e homogênea no tempo) seja aplicada validamente, as seguintes premissas devem ser satisfeitas:

1. **Perda de Memória:** O histórico passado não ajuda a prever o futuro além daquela já contida no estado presente.
2. **Homogeneidade Temporal:** As probabilidades de transição $P_{ij}$ são constantes ao longo do tempo (não mudam do passo t para o passo $t+k$).
3. **Espaço de Estados Discreto e Definido:** Todos os estados possíveis do sistema devem ser conhecidos e bem delimitados.

Ou seja, suas premissas são as que tão ligadas a sua estrutura e como funcionam.

## ENTRADAS E SAÍDAS

Para configurar e executar uma Cadeia de Markov, define-se:

O que ela recebe de entrada:

- **Espaço de Estados (S):** O conjunto de estados discretos.
- **Matriz de Transição (P):** Matriz NxN com as probabilidades condicionais $P_{ij}$.
- **Vetor de Estado Inicial ($p^{(0)}$):** Distribuição de probabilidade de onde o sistema começa no tempo t=0.
- **Número de Passos (t):** A quantidade de transições temporais a simular.

O que ela dá como saída:

- **Distribuição de Probabilidade Futura ($p^{(t)}$):** A chance do sistema estar em cada estado no instante t.
- **Distribuição Estacionária (p):** As probabilidades de longo prazo (quando t = infinito).
- **Sequência Simulada de Estados:** Uma trajetória estocástica gerada via amostragem monte carlo ao longo do grafo.

Essa última ligada a Monte Carlo é só uma simulação de qual os movimentos mais prováveis a cada passo para dar uma resposta mais rica.

## MATEMÁTICA

### Probabilidade Condicional e Equação da Cadeia

A definição formal da Propriedade de Markov (falta de memória) de Primeira Ordem em tempo discreto é expressa por:

$$P(X_{t+1} = x_{t+1} \mid X_t = x_t, X_{t-1} = x_{t-1}, \dots, X_0 = x_0) = P(X_{t+1} = x_{t+1} \mid X_t = x_t)$$

Pela regra da cadeia de probabilidade, a probabilidade conjunta de observar uma sequência específica de estados $x_0, x_1, \dots, x_T$ simplifica-se para:

$$P(X_0 = x_0, X_1 = x_1, \dots, X_T = x_T) = P(X_0 = x_0) \prod_{t=1}^{T} P(X_t = x_t \mid X_{t-1} = x_{t-1})$$

### Equações de Chapman-Kolmogorov

Para calcular a probabilidade de transitar do estado $i$ para o estado $j$ em $m + n$ passos, somamos as probabilidades sobre todos os estados intermediários possíveis $k$:

$$P_{ij}^{(m+n)} = \sum_{k \in S} P_{ik}^{(m)} P_{kj}^{(n)}$$

Em notação matricial, isso equivale diretamente à multiplicação de matrizes: $P^{(m+n)} = P^{m} \cdot P^{n}$.

### Cálculo da Distribuição Estacionária via Sistema Linear

Para encontrar o vetor estacionário $p = [p_1, p_2, \dots, p_N]$, resolvemos o sistema linear derivado de $p^P = p$ com a restrição de normalização probabilística:

$$\begin{cases} 
p^(P - I) = \mathbf{0} \\
\sum_{i=1}^{N} p_i = 1 
\end{cases}$$

Onde $I$ é a matriz identidade de ordem $N$. Pelo **Teorema de Perron-Frobenius**, para matrizes estocásticas irredutíveis e aperiódicas, o autovalor dominante é sempre $\lambda_1 = 1$, e seu autovetor associado (normalizado) é a distribuição estacionária única.

## RELAÇÃO COM MODELOS DE IA: QUEM USA, COMO E POR QUE

As Cadeias de Markov são um dos pilares da Inteligência Artificial moderna. Elas aparecem desde modelos clássicos até as arquiteturas generativas de ponta.

### Modelos Ocultos de Markov (Hidden Markov Models - HMM)

- **Quem usa:** Reconhecimento de voz clássico (Siri inicial, Kaldi, HTK), Processamento de Linguagem Natural (POS Tagging, Reconhecimento de Entidades Nomeadas), Bioinformática (alinhamento de sequências de DNA/Proteínas).
- **Como usa:** Assume-se que o sistema possui uma Cadeia de Markov subjacente de estados **ocultos** (não observáveis diretamente), mas cada estado oculto emite um símbolo **observável** de acordo com uma distribuição de probabilidade de emissão. Usa-se o **Algoritmo de Viterbi** para encontrar a sequência de estados mais provável e o **Algoritmo de Baum-Welch (EM)** para treinar as transições.
- **Por que usa:** Permite inferir dados a partir de dados temporais ruidosos ou indiretos (ex: inferir as palavras faladas a partir das ondas sonoras).

### Aprendizado por Reforço (MDPs e POMDPs)

- **Quem usa:** AlphaGo / AlphaZero (DeepMind), agentes de robótica, algoritmos de controle (PPO, SAC, Q-Learning), sistemas de direção autônoma.
- **Como usa:** O ambiente de interação do agente é formalizado como um **Processo de Decisão de Markov (MDP)**. A dinâmica de transição de estados $P(S' \mid S, a)$ depende do estado atual S e da ação a tomada pelo agente, incorporando uma função de recompensa R(S, a).
- **Por que usa:** Fornece a base matemática estrita para provar a convergência da **Equação de Bellman** e garantir que o agente consiga aprender uma política ótima de longo prazo sob incerteza.

### Modelos Generativos Baseados em Difusão (Diffusion Models)

- **Quem usa:** Stable Diffusion, Midjourney, DALL-E 3, Sora (OpenAI).
- **Como usa:** A geração de imagens e vídeos é modelada como o processo inverso de uma Cadeia de Markov. No **Forward Process**, adiciona-se ruído gaussiano incrementalmente à imagem ao longo de T passos até que ela se torne ruído puro. A Rede Neural (U-Net/Transformer) é treinada para aprender o **Reverse Process** — estimar a transição de des-ruidificação $q(x_{t-1} \mid x_t)$ a cada passo da cadeia.
- **Por que usa:** Quebrar a tarefa impossível de gerar uma imagem complexa de uma só vez em uma sequência de T pequenos passos simples, estáveis e matematicamente tratáveis.

### Markov Chain Monte Carlo (MCMC)

- **Quem usa:** IA Bayesiana, PyMC, Stan, Aprendizado Profundo Probabilístico, Física Computacional.
- **Como usa:** Para dados com distribuições de probabilidade complexas e muitas variáveis X (onde fazer a integral de P(X) é inviável), constrói-se uma Cadeia de Markov cuja **distribuição estacionária** projetada seja exatamente a distribuição alvo desejada. Algoritmos como **Metropolis-Hastings** e **Gibbs Sampling** navegam nessa cadeia.
- **Por que usa:** Permite usar modelos Bayesianos complexos substituindo o cálculo impossível da evidência.

### Modelos de Linguagem N-grama e Autoregressivos Básicos

- **Quem usa:** Teclados preditivos de celular (Gboard, SwiftKey), corretores ortográficos, tokenizadores, geradores de texto estatísticos baseline.
- **Como usa:** Modelos de linguagem baseados em N-gramas assumem uma **Cadeia de Markov de Ordem $N-1$**. A probabilidade da próxima palavra depende apenas das $N-1$ palavras imediatamente anteriores no texto: $P(w_t \mid w_{t-1}, w_{t-2}, \dots, w_{t-N+1})$.
- **Por que usa:** Extrema velocidade de inferência, baixíssimo consumo de memória e treinamento instantâneo através de simples contagem de frequências no corpus.

### PageRank (Busca e Recomendação em Grafos)

- **Quem usa:** Motor de busca do Google, recomendadores de conexões (LinkedIn, Twitter/X), algoritmos de centralidade em grafos de conhecimento.
- **Como usa:** O comportamento de um "navegador aleatório" clicando em links na web é modelado como uma Cadeia de Markov Ergódica em um grafo gigante. O vetor de **distribuição estacionária** p resultante define a relevância/importância de cada página web.
- **Por que usa:** Fornece uma medida global de autoridade imune a manipulações locais e altamente escalável via métodos de potência matricial.

## COMO FUNCIONA

A execução de uma Cadeia de Markov para inferência e previsão ocorre nas seguintes etapas:

1. **Modelagem e Extração de Frequências:**
   - Define-se o conjunto de estados S.
   - A partir de dados calcula-se quantas transições de $S_i$ para $S_j$ teve e normaliza-se pelo total da linha para formar a matriz P.
2. **Definição da Condição Inicial:**
   - Define-se $p^{(0)}$ (ex: se sabemos que o sistema começou no estado 1, $p^{(0)} = [1, 0, ..., 0]$).
3. **Propagação Temporal (Multiplicação Matricial):**
   - Para prever o próximo passo: $p^{(1)} = p^{(0)} P$.
   - Para prever N passos à frente: multiplica-se iterativamente por P ou calcula-se a potência $P^n$.
4. **Análise de Convergência de Longo Prazo:**
   - Calcula-se o autovetor dominante de P para determinar o comportamento do sistema em regime permanente.

## VARIAÇÕES DAS CADEIAS DE MARKOV

Para contornar as limitações da versão básica, a literatura desenvolveu diversas extensões sofisticadas:

- **Cadeias de Markov de Ordem Superior**
  - O próximo estado depende dos últimos k estados: $P(X_{t+1} \mid X_t, X_{t-1}, \dots, X_{t-k+1})$.
  - **Quando usar:** Quando dependências de curto-médio prazo existem (ex: Modelos N-grama com $N > 2$).
- **Cadeias de Markov Não-Homogêneas no Tempo**
  - A matriz de transição P(t) varia com o tempo.
  - **Quando usar:** Sistemas com sazonalidade ou degradação temporal (ex: probabilidade de falha de equipamento aumentando com a idade).
- **Cadeias de Markov em Tempo Contínuo (CTMC)**
  - As transições ocorrem em qualquer instante de tempo real contínuo $t \in R^+$, governadas por uma **Matriz de Taxas de Transição Q** (Gerador Infinitesimal) e distribuição exponencial de tempos de permanência.
  - **Quando usar:** Teoria de Filas, Modelagem Epidêmica (SIR), Reações Químicas Estocásticas.
- **Processos de Decisão de Markov Parcialmente Observáveis (POMDP)**
  - O agente não conhece o estado exato S, mantendo apenas uma distribuição de crença sobre os estados com base em observações incompletas.
  - **Quando usar:** Robótica autônoma com sensores ruidosos/limitados.
- **Cadeias de Markov Monte Carlo (MCMC)**
  - Métodos algoritmos de amostragem (Metropolis-Hastings, Gibbs) que constroem cadeias propositadamente para simular distribuições complexas.
  - **Quando usar:** Inferência Bayesiana e estimativa de integrais multidimensionais.

### Quando Usar Cada Uma (Resumo Prático)

- Dependência Estritamente Local / 1 Passo: Cadeia de Markov de 1ª Ordem
- Dependência de Janela Curta (ex: 3 palavras): Cadeia de Markov de 2ª ou 3ª Ordem (levando em conta o passo atual e os antigos)
- Estados Não Visíveis Diretamente: Modelo Oculto de Markov (HMM)

## Exemplo

Imagine que observamos o clima por 15 dias seguidos e vimos que só teve 2 estados (C - chuva e S - sol). A sequência de dias foi: S -> S -> C -> C -> C -> S -> S -> S -> C -> S -> S -> C -> C -> S -> S.

Com isso nosso grafo terá só 2 estados (S e C). A tabela é feita a partir das 14 transições que vemos nas medidas.

- S -> S: 5 vezes
- S -> C: 3 vezes
- C -> C: 3 vezes
- C -> S: 3 vezes

Ignorando o primeiro dia (porque não temos o valor anterior a ele) tivemos a presença de 8 S e 6 C. O primeiro deve ser descartado pois só contabilizamos os casos que entram na tabela (que sabemos o estado anterior de onde veio). Com isso podemos medir a frequência que cada um apareceu e montar a tabela

$$\begin{bmatrix}
-      & \text{S} & \text{C} \\
\text{S} & 5/8      & 3/8 \\
\text{C} & 3/6      & 3/6
\end{bmatrix}$$

**Se hoje é chuva (C), qual o clima para amanhã e depois de amanhã?**

hoje = C = $p_0$ = [0, 1] (segunda coluna é 1 pq Chuva é a 2ª coluna da matriz). Multiplicando o vetor hoje pela matriz

$p_1 = [0*5/8 + 1*3/6, 0*3/8 + 1*3/6] = [3/6, 3/6]$

Podemos apenas olhar para linha de C e dizer que ela é a resposta para amanhã.

Para depois de amanhã usamos o vetor de $p_1$ para calcular $p_2$.

$p_2 = [3/6, 3/6] P = [3/6*5/8 + 3/6*3/6, 3/6*3/8 + 3/6*3/6] = [0.5625, 0.4375]$

**Qual a chance de daqui 3 dias está chovendo se hoje está sol?**

$$M^3 = \begin{bmatrix}
-      & \text{S} & \text{C} \\
\text{S} & 5/8      & 3/8 \\
\text{C} & 3/6      & 3/6
\end{bmatrix} * \begin{bmatrix}
-      & \text{S} & \text{C} \\
\text{S} & 5/8      & 3/8 \\
\text{C} & 3/6      & 3/6
\end{bmatrix} * \begin{bmatrix}
-      & \text{S} & \text{C} \\
\text{S} & 5/8      & 3/8 \\
\text{C} & 3/6      & 3/6
\end{bmatrix}$$

Lembrando que $M^3$ é diferente de elevar seus valores ao cubo! $M^3 = M^2 * M$ e $M^2 = M*M$.

$$M^2 = M*M = \begin{bmatrix}
-      & \text{S} & \text{C} \\
\text{S} & 0,578      & 0,422 \\
\text{C} & 0,422      & 0,271
\end{bmatrix}$$

$$M^3 = M^2*M = \begin{bmatrix}
-      & \text{S} & \text{C} \\
\text{S} & 0,572      & 0,428 \\
\text{C} & 0,399      & 0,294
\end{bmatrix}$$

Portanto a probabilidade de sair dum dia de sol (hoje) e ir para chuva daqui 3 dias é a linha sol e coluna chuva, 0,428.