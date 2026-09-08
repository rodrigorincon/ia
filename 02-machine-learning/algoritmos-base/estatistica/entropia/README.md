# ENTROPIA

A entropia é uma das teorias mais fundamentais e transformadoras da ciência moderna. Originalmente nascida na termodinâmica, foi redefinida por Claude Shannon em 1948 para seu uso na Teoria da Informação, sendo essa versão usada na computação e no aprendizado de máquina.

No contexto do aprendizado de máquina a entropia mede o **grau de aleatoriade/imprevisibilidade** (também chamado de incerteza, desordem ou impureza) contido em um conjunto de dados ou em uma distribuição de probabilidade. Ou seja, quão variado são o conjunto de dados. **A entropia cresce conforme temos variação de dados e fica mais difícil prever uma jogada**.

O sistema analisa uma variável aleatória e quantifica a quantidade média de "surpresa" ou informação necessária para descrever seus possíveis resultados. **Quanto mais imprevisível for o resultado, maior será a sua entropia**. Por conta disso uma distribuição uniforme, que faz todos os dados terem a mesma chance de sair, é a mais aleatória de todas e com isso, a com maior entropia.

> Se todos os dados tiverem a mesma categoria ou mesmo valor a entropia é mínima (0), se os dados tiverem cada um um valor ou categoria diferente a entropia será máxima (1). 

Com isso, incerteza/desordem/impureza quer dizer o **quão aleatório os dados são**. Quanto maior a dispersão e o desvio padrão, maior a entropia.

## Como Interpretar Entropia

> **Entropia = aleatoriedade = imprevisibilidade**.

Você pode chamar entropia como aleatoriedade ou imprevisibilidade. Também pode chamá-la de incerteza, desordem ou impureza. Todos esses nomes são muito usados para se referir a entropia mas querem dizer a mesma coisa. É tudo sinônimo.

## Incerteza e Surpresa

Em Teoria da Informação, eventos muito prováveis carregam pouca informação, pois trazem pouca "surpresa". Se você sabe que o sol vai nascer amanhã, essa informação não adiciona conhecimento novo. No entanto, um evento muito raro carrega uma quantidade enorme de "surpresa" (informação). Podemos dizer que dezenas de dados iguais só tem 1 única informação repetida. Informação seria dados novos e diferentes dos anteriores.

A entropia é a **média ponderada da surpresa** de todos os eventos possíveis em uma distribuição.

- **Evento Certo (P = 1)**: Surpresa nula. Entropia = 0
- **Evento Improvável (P = 0.01)**: Surpresa altíssima. Entropia próxima de 0 pois ele quase nunca ocorre.
- **Distribuição Uniforme**: Todos os eventos são igualmente prováveis. Incertitude máxima. Entropia máxima = 1 (pois todos os valores ocorrem muitas vezes)

### Uniformidade e Incerteza

Uniformidade pode ser entendido de duas formas opostas: todos os dados serem iguais (minha amostra ser uniforme por ter só 1 valor) ou todos os dados terem a mesma probabilidade (distribuição uniforme).

A surpresa quando todos seus dados são iguais é 0, portanto a entropia é 0. Isso acontece porque não há dados diferentes, você só tem 1 única informação repetida. **Não existe desordem se tudo é igual e o resultado final é determinístico**.

A surpresa quando todos seus dados são diferentes (tem 1 de cada, como por exemplo os lados de um dado) ou todos tem a mesma probabilidade é máxima, portanto a entropia é 1. Distribuição uniforme = máxima incerteza de qual resultado acontecerá, portanto máxima entropia. Não há nada determinístico.

Pensando em um cenário intermediário: Se eu tenho 999 bolas vermelhas e 1 azul existe alguma incerteza, uma leve pitada de caos, portanto há um pouco de entropia. Porém é quase certo que sairá azul, é quase determinístico. Por isso a entropia é próxima de zero.

### DIFERENÇA PARA A VARIÂNCIA

Enquanto a **variância mede o espalhamento de dados numéricos** em relação à média (sendo sensível a valores discrepantes e à escala), a entropia mede o grau de incerteza/aleatoriedade de uma distribuição de probabilidades, funcionando perfeitamente para variáveis categóricas e não-lineares (que a variância não conseguiria medir). Podemos encarar a **entropia como a variância para dados categóricos**.

- **Variância**: Foca em distância geométrica e amplitude escalar ($\sigma^2 = \frac{\sum (x_i - \mu)^2}{N}$).
- **Entropia**: Foca na distribuição de probabilidade e imprevisibilidade dos estados ($-\sum P(x_i) \log_2 P(x_i)$).

## Semelhanças e Diferenças para a Entropia na Física

A entropia do aprendizado de máquina (Entropia de Shannon) compartilha raízes conceituais e matemáticas diretas com a entropia da física (Entropia Termodinâmica), mas aplica-se a objetos de estudo diferentes.

### Semelhanças

1. **Formulação Matemática Idêntica**: A equação de Boltzmann para entropia física na mecânica estatística ($S = -k_B \sum p_i \ln p_i$) possui exatamente a mesma estrutura funcional que a equação de Shannon ($H = -\sum p_i \log_2 p_i$).
2. **Conceito de Desordem/Incerteza**: Na física, mede a quantidade de microestados compatíveis com um macroestado (quanto mais arranjos possíveis, maior a desordem). Na computação, mede a quantidade de valores que uma variável pode assumir (quanto mais **valores equiprováveis**, maior a incerteza).

### Diferenças

As diferença estão todas ligadas ao fato do objeto de estudo serem diferentes.

1. **Objetos de estudo diferentes**: na física medidos calor, energia e partículas. Na computação medimos dados, mensagens e distribuição de probabilidade.
2. **Unidade de medida**: na física é Joule por Kelvin (J/K). Na computação é Bits (se usar log na base 2), Nats (se for log na base e) ou Bans (se for log na base 10).
3. **Leis físicas**: Na computação, por usar apenas métricas matemáticas e não precisar seguir restrições físicas como seu homônimo físico, não possui suas constantes nem segue a 2ª lei da termodinâmica.

Inclusive considerando o que significa a 2ª lei da termodinâmica (incerteza/aleatoriedade sempre cresce se não houver forças agindo para manter tudo organizado), ela não se aplica na computação. Tudo fica parado onde está se não houver novos dados entrando ou sendo alterados.

> **Curiosidade Histórica**: O nome "Entropia" foi sugerido a Claude Shannon por John von Neumann, que disse: *"Você deve chamá-la de entropia por duas razões. Primeiro, sua função de incerteza já é usada na mecânica estatística sob esse nome. Segundo, e mais importante, ninguém sabe o que a entropia realmente é, então em uma discussão você sempre terá a vantagem!"*

## Premissas e Tipos de Dados

Para que a entropia possa ser calculada e aplicada com precisão em algoritmos de Machine Learning, certas premissas devem ser respeitadas:

### Tipos de Dados Aplicáveis

1. **Dados Categóricos/Discretos**: Aplicação nativa clássica. Mede a aleatoriedade de classes (ex: "Sim" ou "Não", "Maçã", "Banana" ou "Laranja").
2. **Dados Contínuos (Entropia Diferencial)**: Pode ser estendida para variáveis contínuas por meio da integração de funções de densidade de probabilidade (PDF), embora exija cuidados devido à possibilidade de valores negativos na versão contínua.
3. **Matrizes de Confusão e Distribuições de Softmax**: Amplamente empregada para avaliar saídas de modelos probabilísticos.

### Premissas

- **Distribuição de Probabilidade Válida**: A soma das probabilidades de todos os eventos possíveis deve ser exatamente igual a 1 ($\sum P(x_i) = 1$).
- **Suporte de Amostragem Adequado**: Para estimar as probabilidades empiricamente (total da categoria / tamanho da amostra), a quantidade de dados deve ser grande o suficiente para evitar probabilidades nulas inconsistentes.
- **Independência das Observações**: Na entropia simples, assume-se que as ocorrências são independentes. Quando há dependência temporal ou sequencial, utiliza-se a *Taxa de Entropia* ou *Entropia Condicional*.

## Onde Usar

A entropia é a espinha dorsal de diversos algoritmos de aprendizado de máquina:

- **Árvores de Decisão (ID3, C4.5)**: Utilizada como critério de divisão de nós para selecionar o atributo que melhor separa as classes.
- **Redes Neurais e Classificação**: A **Entropia Cruzada (*Cross-Entropy Loss*)** é a função de perda padrão em problemas de classificação binária e multiclasse.
- **Modelos Generativos e Variacionais (VAEs, GANs)**: A **Divergência de Kullback-Leibler (KL Divergence)**, derivada direta da entropia, mede a distância entre a distribuição aprendida pelo modelo e a distribuição real dos dados.
- **Processamento de Linguagem Natural (NLP)**: A métrica de **Perplexidade** (usada para avaliar modelos de linguagem como GPT e BERT) é calculada diretamente como o exponencial da entropia.
- **Aprendizado por Reforço (RL)**: Utilizada como termo de regularização (*Entropy Regularization*) em algoritmos como SAC e PPO para encorajar a exploração do ambiente e evitar convergência prematura.

### Como Usar

O algoritmo mapeia as frequências relativas das classes presentes em um grupo de dados, converte essas frequências em probabilidades e aplica a equação logarítmica para estimar a entropia. Valores próximos de zero indicam baixa aleatoriedade (dados homogêneos), enquanto valores altos indicam alta desordem (dados heterogêneos).

## MATEMÁTICA

A equação clássica da Entropia de Shannon para uma variável aleatória X e probabilidades $P(x_i)$ é definida como:

$$H(X) = - \sum_{i=1}^{n} P(x_i) \log_b P(x_i)$$

Onde:
- $H(X)$ é a entropia da variável $X$.
- $P(x_i)$ é a probabilidade do evento $x_i$ ocorrer.
- $\log_b$ é o logaritmo na base $b$.

Portanto a **entropia é a soma das probabilidades de cada categoria acontecer vezes suas surpresas (imprevisibilidade)**. O tipo de log depende do contexto avaliado (mais comum é 2 ou e).

### Surpresa

A **quantidade de informação (surpresa)** contida em um único evento $x_i$ é dada por:

$$I(x_i) = \log_b \left( \frac{1}{P(x_i)} \right) = - \log_b P(x_i)$$

É daí que vem o log da fórmula. O valor negativo vem simplesmente de descer o expoente do log (-1) multiplicando. A fórmula nada mais é que a probabilidade vezes quão imprevisível ela é (surpresa).

Podemos entender a entropia como o **valor esperado** (esperança) da informação própria.

### O papel da Base do Logaritmo

- **Base 2 ($\log_2$)**: Unidade medida em **bits** (ou *shannons*). É a base mais utilizada em aprendizado de máquina e computação.
- **Base Euleriana ($\ln$ ou $\log_e$)**: Unidade medida em **nats**. Muito comum na formulação matemática de redes neurais e funções de perda.
- **Base 10 ($\log_{10}$)**: Unidade medida em **bans** ou **dits**.

### Propriedades Fundamentais

1. **Não-negatividade**: $H(X) \ge 0$.
2. **Convenção de Limite**: Por convenção matemática, $0 \cdot \log_b(0) = 0$.

## PASSO-A-PASSO (COMO EXECUTAR)

Para calcular a entropia de um conjunto de dados siga o roteiro abaixo:

1. **Contar as Ocorrências**: Conte o número total de elementos ($N$) e o número de ocorrências de cada categoria ($n_i$).
2. **Calcular as Probabilidades**: Divida a contagem de cada classe pelo total de elementos: $P(x_i) = \frac{n_i}{N}$.
3. **Calcular a Surpresa**: Calcule $-\log_2(P(x_i))$.
4. **Ponderar pelas Probabilidades**: Multiplique a probabilidade de cada classe pela sua respectiva surpresa: $-P(x_i) \log_2(P(x_i))$.
5. **Somar os Resultados**: Somatório de todos os valores ponderados.

