# APRENDIZADO POR REFORÇO

O Aprendizado por Reforço (Reinforcement Learning ou RL) é a vertente do Machine Learning voltada para a **tomada de decisões sequenciais**. Diferente do aprendizado supervisionado e do não supervisionado o Aprendizado por Reforço aprende por **tentativa e erro** através da **interação direta com um ambiente dinâmico**.

Se no aprendizado supervisionado nós damos um livro com perguntas e gabarito, e no não supervisionado entregamos apenas o livro sem respostas, no aprendizado por reforço nós colocamos o algoritmo em um robô ou videogame e dizemos: "Seus pontos sobem quando você faz algo bom e caem quando faz algo ruim. Descubra sozinho como tirar a pontuação máxima."

A melhor analogia é ver a IA como um bebê. A IA aprende como um bebê explorando o mundo e interagindo com ele, descobrindo que é bom e o que é ruim pelas recompensas que o mundo lhe dá. Ele começa como uma tela em branco e vai descobrindo o que é vantajoso ou não a cada vez que faz algo. Esse método é super semelhante a vida real e muito natural, porém é muito fácil de gerar resultados absurdos, por isso é comum ter de testar diversos hiper-parâmetros, treinando a IA dezenas de vezes até achar os hiper-parâmetros que o fazem aprender corretamente sem algum comportamento bizarro.

> Ex: uma IA de explorar um ambiente pode preferir ficar parada porque todas as casas em volta são piores que a atual (ser acomodar). Um carro pode aprender a andar em círculos para nunca bater em uma parede (comportamento vicioso). Uma IA pode descobrir um bug no jogo que o faz atravessar paredes ou mesmo só jogar abaixado para reduzir risco de ser acertado.

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

## Modelando Estado

O ambiente precisa ser modelado de alguma forma para que possamos aprender com ele. Com isso surge um problema: definir os estados. Cada estado é uma forma que o ambiente e a IA pode estar nele. Por exemplo, os 4 cenários a seguir são considerados estados diferentes, pois ou o ambiente muda (chão limpo ou sujo) ou como a IA está nele muda (sua posição e local):

- Robô em pé no meio da sala com chão sujo
- Robô deitado no meio da sala com chão sujo 
- Robô em pé no canto da sala com chão sujo
- Robô em pé no canto da sala com chão limpo

Modelar o que é um estado e o que e como devem interferi-lo é a peça chave dos algoritmos por reforço. Quais características afetam o comportamento da IA e o quanto cada uma deve ser relevante? Ao definir que algo afeta o comportamento, modelar o como afeta também é crucial, tornando essa parte da construção da IA desafiadora.

> Exemplo prático: no jogo Snake a posição entre a cabeça da cobra e a comida e também quais casas a sua volta estão livres definem o estado. Porém podemos definir que só as casas vizinhas importam ou todas as casas do jogo.

Repare que como você definir o estado, a quantidade de estados podem ser infinitas! Imagine que cada milímetro que o robô andar para o lado for considerado um estado novo, ou cada 0.001 graus que a temperature aumente seja um estado novo. A **quantidade de estados possíveis é chamado de dimensionalidade**. Quando se tem milhares de dimensões alguns algoritmos podem quebrar, por isso a modelagem do que deve ser considerado como parte do estado e quão pequena suas variações tem de ser é muito importante na hora da escolha do algoritmo.

Algumas decisões que podem ser feitas são:

- Eliminar uma variável, não a considerando para as escolhas da IA (ex: não considerar a bateria do robô)
- Considerar o tamanho da mudança para ser um novo estado (estar 1 milímetro pro lado é um novo estado?)

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

Cada interação gera uma tupla de transição: $(S_t, A_t, R_{t+1}, S_{t+1})$. Assim como não há a matriz X, também **não existe os valores Y**. Como não há comparação entre valor previsto e esperado (seja durante o treino como no supervisionado ou pós treino como no não supervisionado), os valores Y perdem todo o sentido de existir. Não existe um valor a ser alcançado ou comparado nesse cenário.

- **Algoritmos On-Policy:** Usam os dados da transição instantaneamente para atualizar o modelo e depois os **descartam os dados após o uso**. Apenas interações geradas pela política atual são válidas (como em uma Cadeia de Markov tradicional).
- **Algoritmos Off-Policy:** Armazenam tabelas ou tuplas passadas em uma memória chamada **Replay Buffer** (D) e fazem amostragem em mini-lotes para treinar, alcançando o objetivo em menos passos.

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

## Componentes Principais

### Recompensa

A cada ação que fazemos recebemos uma recompensa, que nos diz o quão boa foi essa ação. A recompensa pode ser tardia (faço a ação agora mas só vou descobrir se ela foi boa depois). Mas o importante é entender que agir no ambiente significa ganhar ou perder pontos conforme a ação foi benéfica ou não. 

Diferentes ações e/ou consequências podem dar recompensas diferentes. Ex: bater o carro na parede pode dar -1000 de recompensa enquanto pegar um tanque de combustível dá 100 e se afastar da linha de chegada dá a distância que se está do destino. Um dos desafios do aprendizado por reforço é criar pontuações que reflitam os pesos dessas ações. Uma pontuação desbalanceada fará seu modelo aprender errado e priorizar comportamentos diferentes do esperado. Ex: ele pode escolher ficar parado porque é mais seguro que correr o risco de bater na parede. 

Ficar atento ao valor e a diferença entre eles é essencial. No exemplo do carro, se a pista de corrida tem 10km, andar 1 metro na direção certa e ganhar 1 ponto pode afetar muito pouco perante o risco de batida, merecendo um valor maior por metro.

> **Importante**: uma característica vital do aprendizado por reforço é que **não devemos criar código proibindo certas ações danosas** (ex: ficar indo e voltando sempre para o mesmo ponto). Ao invés disso devemos permitir, porém dar uma recompensa negativa ao fazer essa ação. Assim a IA aprende a não fazê-la (que é o objetivo do ML afinal) e mantemos o código enxuto.

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

#### Como Calcular

É usado a equação da entropia de Shannon, que soma a probabilidade de cada ação ser tomada em cada estado e tira a média total. Ou seja, ele tira a **média das probabilidades de explotação** (ignora as ações tomadas por exploração). O cálculo é

$H = \frac{\sum_s - \sum_a P(a | s) log_2( P(a | s) )}{N_s}$

Aonde:
- s é cada estado
- a é cada ação
- $N_s$ é o número de estados
- P(a | s) é a probabilidade de tomar uma determinada ação nesse estado

Toda ação de exploração é considerada entropia e um pouco das de explotação também (pois até o modelo está plenamente treinado tem um resíduo de aleatoriedade nas escolhas). O passo-a-passo para calcular a entropia de uma episódio é:
- Considera toda a taxa de exploração como entropia (portanto todos os cálculos seguintes são feitos considerando só a porcentagem restante - explotação)
- Para cada estado S 
  - Calcula-se a probabilidade de cada ação ser feita (número de vezes que ela foi escolhida dividido pelo total de ações)
  - Soma as probabilidades de todas as ações para aquele estado segundo a equação de Shannon $-\sum_a P(a | s) log_2( P(a | s)$
  - Calcula a média de todos os estados

#### O Que a Faz Diminuir

- Diminuir a taxa de exploração (e) a cada episódio
  - Quanto maior a taxa de exploração, maior a entropia (e menor a explotação - tomada de decisão inteligente)
  - A probabilidade de cada ação dado o estado é considerado apenas dentro da fatia de explotação. Toda a porcentagem de exploração é considerada entropia
- Modelo bem treinado
  - Faz as escolhas tomadas pela explotação serem menos aleatórias
  - Melhora P(a | s)

### Memória

Cada tipo de RL tem mecanismos de memória diferente ligada a família do algoritmo. Esse mecanismo de memória começa zerado e vai sendo preenchido a cada passo em todos os episódios/simulações. Conforme vai explorando o ambiente e descobrindo sobre o mesmo, preenche-se essa estrutura de dados que guarda a memória. É essa memória que é usada para tomada de decisão. 

Importante ter em mente que a memória **não deve ser apagada ao iniciar uma nova simulação!** Se apagar você perde todo o ganho de conhecimento que teve com as outras simulações e joga todo o tempo e esforço no lixo. Por não apagar a memória que as últimas simulações convergem mais rápido e já fazem decisões mais acertadas. Também é o que nos permite ir abaixando a entropia aos poucos ao longo das simulações (outra variável que se altera entre as simulações).

A estrutura que armazena a memória é:

- Baseados em Valor: tabela Q ou função de valor
- Baseados em Política: parâmetros internos da política $\theta$ (pesos da rede neural)
- Baseados em Modelo: Modelo do Ambiente

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
  - Pontua quão bom é cada ação em cada estado e escolhe o estado disponível com maior ponto.
  - Usa Tabela Q (Q(s,a)) ou função de valor (V(s)).
2. **Baseados em Política (Policy-Based):** Otimizam a política $p_\theta(a|s)$ diretamente, sem precisar de uma tabela Q ou função de valor.
  - Busca os parâmetros internos $\theta$ (parâmetros da função política) que dão o melhor retorno.
3. **Ator-Crítico (Actor-Critic):** Mistura dos 2 tipos acima.
  - O Ator atualiza a política e o Crítico avalia a qualidade da ação.
4. **Baseados em Modelo (Model-Based):** Cria uma versão interna do mundo real (modelo) para planejar ações futuras antes de executá-las
  - Simula o mundo real e treina nele (carros autônomos, IAs que jogam xadrez para aprender...).
  - Ex: AlphaZero.

Na literatura você encontra muito a divisão entre os baseado em modelo e todo o resto, como se valor, política e ator fossem sub-tipos do tipo "sem modelo".

### Baseado em valor (Value-Based)

Estes algoritmos não aprendem a ação diretamente. Eles aprendem a prever o valor Q(s, a) para cada par estado-ação e, no momento da decisão, simplesmente escolhem a ação com maior Q ($\arg\max_a Q(s,a)$). Ou seja, calculam quão bom é tomar uma ação em determinado estado e passam a depois só escolher sempre a melhor opção.

Os algoritmos dessa família usam como **política uma tabela-Q**, que também é sua memória e aprendizado. É nela que fica guardado o conhecimento aprendido (qual o valor de cada ação em cada estado). Cada estado é uma tabela e cada ação é uma coluna. Assim, se quiser saber quão bom é uma ação A em um estado S é só olhar a linha e coluna respectivos. **A forma de preencher essa tabela muda entre os algoritmos**.

Principais algoritmos:
- Q-learning
- Sarsa
- DQN

### Baseado em políticas (Policy-Based)

Esses algoritmos tomam a decisão de qual ação fazer ao otimizar uma política do agente. Essa política pode ser uma função que recebe parâmetros ou uma rede neural. Conforme vai explorando o mundo (passando os passos) vai alterado os parâmetros de entrada, tornado a escolha da ação mais precisa. 

Essa política (função ou rede neural) **calcula probabilidades de tomar cada ação**, sem a necessidade da tabela Q. De forma técnica, estes algoritmos otimizam os parâmetros $\theta$ de uma política $P_\theta(a|s)$ **diretamente**.

Eles possuem uma fraqueza fatal: seu treinamento é lento e instável. A instabilidade significa que ele aprende e desaprende o tempo todo. O desaprender vem de fazer alterações grandes nos parâmetros da política, tirando ela do seu curso. Isso se deve a eles usarem a recompensa acumulada do episódio para ajustar o peso (recompensa tardia). Isso levou a criação da família ator-crítico, que use essa família com as value-based.

Principais algoritmos:
- Reinforce

### Ator-Crítico (Actor-Critic)

Em algoritmos do tipo Ator-Crítico a rede Ator representa a Política (decide a ação) e atualiza a política na direção indicada pelo Crítico. Já a rede Crítico representa a Função de Valor (avalia se a decisão da política foi boa ou ruim). Eles conseguem aproveitar as vantagens do policy (atuar em altas dimensões e ambientes aleatórios) sem suas desvantagens (lentidão de convergência e desaprender).

Principais algoritmos:
- A3C
- PPO
- TRPO
- SAC

### Baseado em modelos (Model-Based)

Esses algoritmos constroem ou utilizam uma representação interna das dinâmicas do ambiente (um "modelo") que prevê as probabilidades de mudança de estado e as recompensas. Ou seja, ele recria todo o ambiente internamente e **faz simulações para aprender ao invés de interagir com o mundo real**. 

Enquanto os modelos anteriores apenas reagem ao estado, os algoritmos baseado em modelos tentam **aprender as leis do ambiente e a função de recompensa**. Com isso, eles conseguem simular o futuro em suas "mentes" antes de agir no mundo real. Aprender as leis do ambiente (regras ou leis físicas) é feito através de redes neurais e dados sintéticos produzidos por modelos já conhecidos do mundo. Aprender as recompensas vai pela mesma linha. Ter de descobrir quantos pontos dar ou tirar, além de descobrir como o mundo funciona tornam essa família consideravelmente mais complexa que os demais.

Principais algoritmos:
- MCTS (usado no AlphaZero)
- Dyna-Q
- MBPO
- Dreamer

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

A cada passo devemos escolher entre um dos dois. Existem diversos algoritmos que define qual dos dois será usado no passo atual. Cada um será melhor detalhado na pasta `05-exploracao-explotacao`.

- Epsilon-Greedy
- Bônus de Entropia
- Softmax
- Limite Superior de Confiança (UCB)
- Amostragem de Thompson (abordagem bayesiana)

## Métricas de Qualidade e Comparação entre Modelos

Métricas tradicionais Acurácia, R² ou Erro Quadrático Médio não funcionam aqui. Para medir o sucesso global da política, o aprendizado por reforço utiliza métricas únicas.

### 1. Recompensa Acumulada/Total

É a soma das recompensas obtidas ao longo dos episódios. A cada episódio calcula a recompensa total que teve até alcançar o objetivo (ou estourar o limite). A recompensa acumulada nos dá quão bem a IA foi na exploração, se escolheu bons caminhos ou se cometeu muitos erros. **Quanto maior a recompensa acumulada, melhor**.

### 2. Curva de Aprendizado

É o gráfico da métrica anterior, mostrando como ela mudou ao longo do treino. Podemos plotar o gráfico da recompensa acumulada em cada episódio e ver se seu comportamento. Como em cada episódio ela é zerada, se o valor do episódio seguinte for maior é sinal que ele aprendeu a tomar boas decisões. O esperado é que ele **vá crescendo e de preferência com a menor flutuação possível**.

- **Modelo Bom:** Apresenta uma curva ascendente estável que atinge um patamar alto (convergência).

- **Modelo Instável:** Apresenta oscilações drásticas (o agente aprende, desaprende e despenca o desempenho).

### 3. Número de Passos

Mede **quantos passos (interação no ambiente)** o modelo precisou para atingir uma determinada pontuação. Isso significa que ele **alcançou o objetivo mais rápido que os demais** e que não estourou o limite máximo de passos.

- Em robótica real ou simuladores lentos, o algoritmo com **menor número de passos é o vencedor**, mesmo que demore mais tempo computacional por passo. **O importante é tomar menos ações, não gastar menos tempo**.

### 4. Entropia da Política

Mede a entropia, ou seja, o grau de incerteza que a política tem sobre o que fazer. Calculamos com a equação de Shannon como explicado no tópico de Entropia. Nós anotamos a entropia de cada episódio e plotamos o gráfico de sua mudança ao final.

**Um bom modelo vai aprendendo gradualmente, portanto a entropia deve cair lentamente e finalizar em um valor baixo ESTÁVEL.** Um modelo ruim pode acontecer uma dessas 3 coisas:

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

| Algoritmo | Espaço de Ações | Número de Passos | Estabilidade de Treino | Casos de Uso Principais | Observação |
| :--- | :--- | :--- | :--- | :--- | :--- |
| **Q-Learning** | Discreto | Baixa | Alta | Problemas de grid simples | **Didático** |
| **DQN** | Discreto | Média | Média | Jogos retrô, decisões discretas | --- |
| **REINFORCE** | Discreto / Contínuo | Muito Baixa | Baixa | Problemas simples de controle | **Didático** |
| **PPO** | Discreto / Contínuo | Média | **Muito Alta** | **Padrão da Indústria, Robótica, RLHF** | **Estado da arte** |
| **SAC** | Contínuo | **Muito Alta** | Alta | Robótica real, controle de precisão | --- |
| **AlphaZero** | Discreto | Alta (com simulador) | Alta | Jogos de tabuleiro (Go, Xadrez) | --- |