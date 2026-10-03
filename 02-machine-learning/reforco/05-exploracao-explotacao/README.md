# ESTRATÉGIAS DE EXPLORAÇÃO E EXPLOTAÇÃO

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

A cada passo devemos escolher entre um dos dois. Existem diversos algoritmos que define qual dos dois será usado no passo atual.

## Epsilon-Greedy

É o mais simples de todos e costuma ser usado só para fins didáticos. Para problemas reais ele não é usado justamente por não ser tão bom na prática.

Epsilon (e) é a probabilidade de escolher exploração. Exploração no caso significa escolher aleatoriamente alguma ação (mesmo as ações que já foram feitas nesse cenário). Isso te permite testar caminhos novos quando epsilon é alto, porém por todas as ações terem a mesma chance podemos por azar escolher uma ação já feita nesse estado (caminho já explorado) e não descobrir nada novo. Ele também dá a mesma chance para caminhos bons e sabidamente desastrosos.

Epsilon começa em 1 (100%) e a cada episódio ele diminui. A ideia é que nos primeiros episódios tenhamos muita exploração e nas finais quase nenhuma. A cada episódio o epsilon se mantém o mesmo, sendo atualizado apenas ao final.

Epsilon também tem um valor mínimo, assim ele nunca fica zero, permitindo mesmo no último episódio um leve toque de aleatoriedade.

Quando usar:
- Protótipos e quando se quer manter algo o mais simples possível
- Algoritmos tabulares (Q-learning, SARSA)
- Caso do bandido de muitos braços

## Softmax

Ao invés de selecionar uma ação aleatória de forma uniforme, atribui a cada ação uma probabilidade proporcional à sua estimativa de valor Q, parametrizada por uma temperatura T:

$$P(a | s) = \frac{e^{Q_a/T}}{\sum_i e^{Q_i/T}}$$

Ou seja, ele é **proporcional ao valor já sabido para Q(s,a)**, mas não a simples divisão de seu valor pelo total daquele estado. 

Quanto maior o valor de Q(s,a) - **quanto melhor é aquela ação - maiores a chances dele ser escolhido**. Claro  que se ele for alto e todas as outras opções de ação para esse estado forem ainda mais, sua probabilidade será pequena.

O parâmetro temperatura T define o grau de aleatoriedade. T muito baixo a melhor opção é sempre escolhida (pura explotação) e T muito alto a escolha fica uniforme (pura exploração - igual o epsilon greedy).

Podemos ainda ir diminuindo o valor de T a cada episódio (igual é feito no epsilon greedy) para forçar explotação conforme o tempo passa. Porém isso muitas vezes não é necessário pois conforme vamos explorando e aumentando os valores de Q (que começam em 0, portanto toda vez que é explorado ele aumenta) sua probabilidade de ser escolhido cresce. Assim mesmo sem alterar T vamos rumando para a explotação simplesmente porque a melhor escolha tem maior probabilidade.

Quando usar:
- Recompensas com pouca variação (Se as recompensas variarem muito a função pode explodir ou saturar).

## Bônus de Entropia

**Usado para algoritmos baseado em políticas e ator-crítico**. Diferente dos anteriores, ele não é algo calculado a parte para dar uma probabilidade de fazer exploração. Ao invés disso ele está diretamente ligado ao funcionamento das redes neurais. 

Ao calcular a função de perda é subtraído o valor da equação da entropia de Shannon.

$L_{\text{total}} = L_{\text{politica}} - \beta * \text{Shannon} = L_{\text{politica}} + \beta \sum_a P(a | s) log_2( P(a | s) )$

Aonde $\beta$ é uma penalidade para quando age de forma determinística (escolhe explotação) antes da hora. Assim ele também age evitando mínimos locais. Se for muito alto impede a convergência pro mínimo global por ficar sempre penalizando. Se for muito baixo não impede de parar em mínimos locais.

Ele não precisa ajustar nenhum parâmetro para diminuir a incidência de exploração, a explotação vai aumentando sozinha conforme os parâmetros da rede vão melhorando.

Quando usar:
- Políticas com redes profundas
- PPO, A2C e SAC em ambientes contínuos (alta dimensão)

## Limite Superior de Confiança (UCB)

Baseia-se no princípio de "otimismo diante da incerteza". O agente escolhe a melhor ação considerando uma margem de incerteza (intervalo de confiança):

$$a = \argmax_a \left( Q(a) + c \sqrt{\frac{ln(t)}{N_a}} \right)$$

Ou seja, ele **soma a cada ação disponível uma margem de incerteza e escolhe a melhor ação**. Essa margem de incerteza ($c \sqrt{\frac{ln(t)}{N_a}}$) é definida pelos parâmetros:

- c: grau de exploração.
- $N_a$ é o número de vezes que a ação A foi escolhida (quanto mais vezes já explorou esse caminho menos vai nele, diminui sua margem de interteza).
- $t$ é o número do passo atual (nesse episódio).

A lógica por trás é simples: quanto mais vezes você já fez algo mais convicto você está do que acontece em seguida. Uma ou duas vezes pode ser acaso, mas se você fez essa ação diversas vezes já dá para ter uma boa noção de como ela se comporta.

Ele também não precisa ajustar nenhum parâmetro para diminuir a incidência de exploração, conforme $N_a$ aumenta a incerteza diminui e vai se aproximando do epsilon greedy (mas sem ter de atualizar manualmente o epsilon).

Ele tem uma desvantagem crítica: **não funciona bem com redes neurais profundas ou espaços contínuos**. 

Quando usar:
- Algoritmos tabulares (Q-learning, SARSA)
- Fase de expansão de árvores de busca do MCTS
- Recomendação de conteúdo
- Testes A/B
- Caso do bandido de muitos braços

## Amostragem de Thompson (abordagem bayesiana)

O agente mantém uma distribuição de probabilidade inicial sobre o valor de cada ação. A cada passo o agente pega um valor hipotético de cada distribuição e escolhe a ação com maior valor. Ao receber a recompensa atualiza aquela distribuição escolhida, diminuindo ou aumentando conforme a recompensa. Repare que ela foca nas ações, ignorando o estado. Ela no final só quer saber **o quanto certa ação parece boa independente de contexto**.

Ela é **extremamente boa para ambientes que mudam** e também ignora altas dimensões de estados (mas não de ações). Porém seu lado negativo é ser mais custosa computacionalmente, a **tornando inviável para ser usada com redes profundas**.

Quando usar:
- Alocação de recursos
- Otimização de campanhas de marketing
- Testes A/B
- Ensaios clínicos
- Contextos Bayesianos com poucos dados iniciais
- Caso do bandido de muitos braços

## Resumo Comparativo

| Estratégia | Tipo de Decisão | Ponto Forte | Ponto Fraco |
| :---       | :---            | :---        | :---        |
| Epsilon-Greedy | Probabilística (proporcional ao epsilon) | Simples e fácil de entender. | Usada apenas para fins didáticos. |
| Softmax | Probabilística (proporcional ao Valor) | Atribui probabilidades com base no valor estimado; evita explorar ações sabidamente ruins. | Sensível à escala das recompensas e exige o ajuste fino do parâmetro de Temperatura (T). |
| UCB | Determinística (guiada por Incerteza) | Eficiente; prioriza o que é menos conhecido. | Difícil de escalar para espaços contínuos. |
| Thompson | Probabilística (Bayesiana) | Altamente eficiente no uso de dados. | Requer modelagem matemática das distribuições. |
| Bônus de Entropia | Contínua na Função Objetivo | Padrão da indústria em RL Profundo | Requer ajuste fino do bônus de entropia B |


## Caso do bandido de muitos braços

O Bandido de múltiplos braços (Multi-Armed Bandit) é uma metáfora comum no aprendizado por reforço para ilustrar problemas de **tomada de decisão quando se há muita incerteza**. Você precisa tomar decisão entre continuar num cenário (que pode ser mediano ou até mesmo bom) ou ir para o próximo sem saber se será melhor ou não.

A metáfora é a seguinte: você está em um cassino diante de várias máquinas caça-níqueis. Cada máquina ("braço") tem uma chance diferente e desconhecida de ganhar. Você quer ganhar o máximo possível com um número fixo de jogadas, porém não sabe quais máquinas são mais fáceis de dar prêmio. Você começa em uma aleatória (pois seu conhecimento sobre todas é 0). O dilema é saber quando continuar jogando na máquina que parece dar mais lucro até agora ou testar outras máquinas para ver se alguma paga ainda melhor.

Ela apresenta um dilema palpável entre exploração e explotação: continuar na máquina que está te pagando vez ou outra (explotação) ou tentar a sorte em uma nova não testada ou até em uma que jogou muito pouco e não chegou a uma conclusão (exploração).

> Muita exploração você pode gastar todo o dinheiro explorando máquinas ruins e sair sem nada. Muita explotação você pode ficar preso numa máquina mediana e perder a chance de ganhar muito mais (**mínimo local**).

Os algoritmos que o resolvem (**epsilon-greedy, Thompson e UCB**) são ótimos para recomendação de conteúdos de forma dinâmica. Você começa direcionando conteúdo de forma uniforme e vai alterando conforme um deles se mostra melhor, mas sem nunca optar por só uma opção.

### Exemplos de Uso

1. Teste A/B dinâmicos

  - Ao invés de um teste A/B estático, você pode aumentar o fluxo para uma das opções conforme ela vai se mostrando melhor. Assim evita perder possíveis clientes no teste com a página pior.

2. Sistemas de recomendação

  - A mesma lógica do teste A/B. Podendo servir para filmes, posts em rede social, produtos de mercado, peça de marketing com melhor engajamento.

3. Ensaios clínicos

  - Conforme um tratamento vai se mostrando melhor que outro vai gradualmente mandando novos casos para a opção melhor.

### Bandidos Contextuais

É uma evolução aonde se assume que as máquinas caça-níqueis tem probabilidades de ganhar diferente para quem joga. Você tem 1/10 de chance de ganhar em uma determinada máquina, mas alguém que acabou de chegar no cassino tem 1/3.

Isso pode não fazer sentido pensando em máquinas, mas faz sentido se pensar em bets ou cassinos online, aonde jogadores novos tem maiores probabilidades para engajá-los no jogo. Também faz sentido no mundo real quando pensa que a mudança de probabilidade pode representar grupos diferentes. Jovens tem menos chance de clicar em um anúncio, mas adultos de meia idade tem mais. A mudança pode ser pelo tempo também: um anúncio pode receber mais cliques se for enviado antes da hora do almoço do que no meio da tarde. Podem também ser por algo que a pessoa possua, localidade ou acredite. **O ponto chave é segmentação**.

Nesse caso o algoritmo precisa de um contexto sobre a pessoa: quem é, onde mora, quanto ganha, idade... Todas as informações consideradas importante para o algoritmo escolher entre explotar e explorar. Isso é mais do que só estados diferentes, significa **dar respostas diferentes para estados diferentes num contexto de alta dimensão**. Dar respostas diferentes é ok, como o estado muda (se você é jovem ou meia-idade o estado é diferente) cada um pode ter uma ação melhor, mas a alta dimensionalidade traz problemas de treino. Tanto o UCB quanto o Thompson tem variações para esse cenários de segmentação.

- UCB -> LinUCB
- Amostragem de Thompson -> Amostragem Contextual de Thompson

Essas versões são especialmente melhores quando queremos: 

- **Segmentar os usuários** 
- **Personalizar conteúdo** 
- **Generalizar para casos nunca antes visto**: não temos condição de testar exaustivamente e precisamos de um modelo que generalize para os cenários nunca vistos. Ou quando sabemos que temos centenas de milhares de estados (muitas variáveis X que afetam) e torna impossível explorar tudo.