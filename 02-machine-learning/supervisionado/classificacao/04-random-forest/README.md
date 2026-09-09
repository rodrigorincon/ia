# RANDOM FOREST (FLORESTA ALEATÓRIA)

É um algoritmo baseado nas árvores de decisão, muito visto como sua evolução. Ele constroi dezenas de árvores de decisão (por isso floresta) aond seus resultados são combinados para gerar uma previsão final. Ela surge para **diminuir o overfitting** das árvores de decisão, sendo vista como uma evolução do mesmo por resolver esse problema.

O algoritmo baseado no conceito de **ensemble** (aprendizado em conjunto), pois cada árvore sozinha é ruim em prever os valores, mas juntas conseguem prever bem. Cada árvore é treinada com um pedaço dos dados de treino, sendo burra e míope, mas unindo o todo como uma floresta ela é **muito mais robusta, estável e precisa** do que a de uma única árvore treinada com todos os dados.

Para se ter em mente, imagine que você precisa tomar uma decisão financeira importante. Em vez de consultar apenas um especialista (que pode ter seus próprios vieses ou cometer erros bobos), você consulta 100 especialistas independentes e toma a decisão com base no **voto da maioria** (ou na **média das opiniões**). O Random Forest faz exatamente isso com os dados.

Ela brinca com a lei dos grandes números, onde centenas de pessoas chutam valores aleatórios e de algum modo a média sai muito próxima do valor real. As florestas aleatórias usam esse conceito mesmo que o voto de cada árvore não seja um chute aleatório.

> É considerado um dos algoritmos de uso geral mais versáteis e robustos da Ciência de Dados.

## Floresta não te dá um diagrama visível

Apesar de ser a união de várias árvores de decisão (e inclusive até por causa disso) a floresta não te dá um modelo visual nem facilmente explicativo como as árvores individuais são. Esse modelo é um dos mais abstratos e difíceis de explicar como seus dados dados são processados internamente, bem ao contrário da árvore de decisão. Importante saber que ao final você **não terá uma árvore de decisão gigante nem uma colagem ou ponderação de várias delas**. Você tem ao invés disso é um sistema de votação, não diferente de uma votação para presidente, onde cada árvore diz a categoria que previu e a mais votada ganha. A lei dos grande números entra aí para nos dar confiança que com centenas ou milhares de árvores teremos confiança na votação.

## Diminuição do Overfitting

O Random Forest resolve o overfitting introduzindo a **aleatoriedade** no processo de construção de cada árvore, dando a cada uma partes diferente dos dados e só algumas variáveis, garantindo que elas sejam diferentes entre si e que os **erros individuais de cada uma se cancelem no resultado final**.

Árvores de decisão possuem **alta variância** (são instáveis). Qualquer **pequena alteração nos dados de treino pode mudar drasticamente toda a estrutura da árvore**. A floresta por lidar com várias análises de amostras diferentes dos dados de treino cria uma versão mais genérica e menos enviesada, pois não seguiu a base inteira de uma vez. Pela lei dos grandes números a média ou o voto majoritário de um conjunto diversificado de modelos reduz drasticamente a variância do sistema sem aumentar o viés.

## O Conceito de Bagging e Bootstrap

Para que o ensemble funcione, as **árvores não podem ser idênticas**. Se todas treinarem com os mesmos dados, todas darão as mesmas respostas. O Random Forest utiliza o conceito de **Bagging** (Bootstrap Aggregating). Ou seja, ele usa 2 conceitos novos para sua fundamentação.

```
Dataset Original (N linhas)
   ├── Amostra Bootstrap 1 ──> Árvore 1
   ├── Amostra Bootstrap 2 ──> Árvore 2
   └── Amostra Bootstrap K ──> Árvore K
```

### Bootstrap (Amostragem com Reposição)

Para cada árvore da floresta, o algoritmo cria um subconjunto de treino extraindo amostras aleatórias do dataset de treino original **com reposição**. Isso significa que cada árvore da floresta trabalha com uma amostra do todo (no caso nosso todo é uma amostra de algo ainda maior, mas ainda assim já nos permite usar a estatística amostral a nosso favor).

Por padrão, cada árvore (amostra Bootstrap) tem o mesmo número de linhas do dataset original. Ou seja, o tamanho dos dados das árvores é igual ao tamanho do todo, mas como temos repetição podemos ter o mesmo dado várias vezes repetido na mesma árvore e inclusive sendo usado em árvores diferentes. Cerca de **36.8% das linhas ficam de fora da árvore** (conhecidas como dados Out-Of-Bag ou OOB).

### Bagging (Agregação das Previsões)

Significa treinar um modelo para cada árvore e agrupar (agregar) suas respostas na fase de inferência. Ou seja, usar a saída de cada árvore para montar a resposta final (através de votação).

## Atributos por Árvore (Feature Space Randomization)

Se usássemos apenas o Bootstrap (embaralhar as linhas do dataset), árvores individuais ainda poderiam ficar muito parecidas se o dataset tivesse uma **variável muito dominante** (uma feature muito forte que sempre seria escolhida no topo de todas as árvores).

Para evitar isso, o Random Forest insere um segundo nível de aleatoriedade: a **Divisão por Subconjuntos de Atributos** (Random Subspace Method). Em cada árvore variáveis (colunas do dataset) diferentes serão usadas para o treino e das demais serão jogadas fora. Ou seja, **cada árvore usa só algumas linhas e algumas colunas**.

- Para **classificação** seleciona-se $\sqrt{M}$ variáveis (M é o número total de variáveis no dataset).
- Para **Regressão** seleciona-se $\frac{M}{3}$ variáveis.

Isso força as árvores a explorarem atributos secundários, tirando o poder de uma variável numa escala muito maior ou que tem muito mais relevância ao ponto de esconder a importância das outras. Isso também garante que as árvores são **descorrelacionadas**.

## Como as Respostas São Combinadas

Após todas as K árvores serem treinadas de forma independente, a previsão para um novo dado x ocorre combinando o resultado de cada árvore individual $H_k(x)$:

```
           ┌── Árvore 1 ──> Classe A ──┐
Entrada ───┼── Árvore 2 ──> Classe B ──┼──> Voto Majoritário ──> Classe A
           └── Árvore 3 ──> Classe A ──┘
```

Essa forma de combinação muda se for para classificação ou regressão.

### Para Classificação: Votação Majoritária

É feito uma eleição e o mais votado é escolhido como resposta final do modelo. Exitem 2 tipos de votação:

- **Hard Voting (Voto Direto):** Cada árvore dá um "voto" em uma classe. A classe com o maior número de votos vence.
    - É o mais parecido com nossas eleições
- **Soft Voting (Média de Probabilidades):** Cada árvore calcula a probabilidade do novo valor pertencer a cada uma das classe. O algoritmo calcula a média dessas probabilidades e escolhe a classe com maior probabilidade média.
    - Cada árvore dá uma lista de probabilidades. Ex: azul 30%, vermelho 50%, verde 20%.
    - Tira a **média de cada categoria** e escolhe a maior. Não confundir com a soma das probabilidades, **precisa ser a média**.

$$\hat{y} = \arg\max_c \frac{1}{K} \sum_{k=1}^{K} P_k(y = c \mid x)$$

### Para Regressão: Média Aritmética

Cada árvore prevê um valor numérico contínuo. A resposta do Random Forest é simplesmente a **média aritmética** de todas as previsões individuais:

$$\hat{y} = \frac{1}{K} \sum_{k=1}^{K} H_k(x)$$

## PREMISSAS

O Random Forest é um dos algoritmos com **menos premissas rígidas** no aprendizado de máquina:

**Independência dos Erros (Diversidade):** As árvores individuais precisam ter erros o mais descorrelacionados possível para que a agregação funcione bem (**resolvido embaralhando as colunas**).

O embaralhamento (Bootstrap) e a votação resolvem a maioria dos problemas que costumam ser premissas. Abaixo é explicado como eles resolvem diversos problemas.

- **Não exige normalização/padronização:** a votação e o embaralhamento das colunas faz com que dados em escalar maiores não quebrem o modelo.
- **Imune a Multicolinearidade:** O sorteio de variáveis em cada árvore lida com a redundância.
- **Robusto a Outliers e Ruídos:** Outliers impactam apenas as árvores específicas onde caem, sem puxar o modelo inteiro.

## Tipos de Dados Suportados

- **Variáveis Numéricas:** Contínuas e discretas (comportam-se perfeitamente de forma nativa).
- **Variáveis Categóricas:** Árvores nativas dividem categorias facilmente, mas a maioria das implementações (como o Scikit-Learn) exige que se faça uma transformação antes de usar o modelo (One-Hot Encoding ou Ordinal Encoding).
- **Dados Faltantes (Missing Values):** Algumas implementações (como XGBoost ou H2O) lidam nativamente com dados ausentes. No Scikit-Learn é recomendada removê-los antes.

## Testes de Hipótese

Diferente de modelos estatísticos clássicos, o Random Forest não se baseia em testes de hipótese nem devolve coeficientes a serem testados.

Porém alguns testes de hipótese podem ser usados para comparar 2 florestas diferentes ou até uma floresta com outros modelos de outros tipos. Esses testes servem para comparar quaisquer modelos de classificação independente de como foram treinados.

- **Teste de McNemar:** Para comparar dois modelos de classificação na mesma base de teste (avalia a matriz de discrepância de erros).
- **Teste de Wilcoxon Signed-Rank:** Para comparar o desempenho de dois modelos através de múltiplos folds de validação cruzada.
- **Teste de Friedman (com Pós-hoc de Nemenyi):** Utilizado para comparar três ou mais modelos/configurações de hiperparâmetros em múltiplos datasets ou folds.

## Formas de Validação

Além dos métodos tradicionais (MAE, MAPE, MRSE, matriz de confução, precisão, F1 score, AUC, acurácia...) o random forest tem alguns métodos exclusivos dele.

### Erro Out-Of-Bag (OOB Error)

Como cada árvore treina com cerca de 63.2% dos dados, os **36.8% restantes (OOB)** não usados nessa árvore podem ser usados como um conjunto de teste extra.

O erro OOB calcula a performance média avaliando cada dado apenas nas árvores que não a utilizaram durante o treino.Ele funciona como um **substituto da Validação Cruzada (K-Fold)**, reduzindo tempo computacional.

### Métricas de Classificação e Regressão

Algumas das métricas tradicionais só servem para classificação enquanto outras são específicas para regressão.

#### Métricas de Classificação

*   **Acurácia**
*   **Matriz de Confusão**
*   **Precision, Recall e F1-Score**
*   **ROC-AUC**: Plotar a métrica de erro em função do número de árvores. Identifica-se o ponto onde o erro estabiliza (geralmente entre 100 e 500 árvores) para evitar custo computacional desnecessário.

### Métricas de Regressão
*   **MAE, MAPE e RMSE**
*   **R² e R² ajustado**

## Definindo Número de Árvores

Para encontrar o número ideal de árvores comece com poucas e vá aumentando até o erro OOB estabilizar. Importante deixar claro que não há risco de overfitting ao aumentar o número de árvores, apenas desperdício de tempo e processamento.

## Gradient Boosting

É outro tipo de aprendizado supervisionado que usa Bootstrap e árvores de decisão, porém `ao invés de várias árvores em paralelo ele as coloca em forma sequencial`.

Na floresta as árvores são independentes e rodam em paralelo, nenuma afeta a outra. No gradient boosting por outro lado cada árvore é calculada de uma vez, seus resíduos (erros) são calculados com OOB, derivados através de alguma função de custo (por isso o nome gradiente) e então a derivada do erro é passada para a árvore seguinte para ser um pouco melhor que a anterior. O erro dela também será medido e derivado e passado para a próxima árvore que será um pouco mais precisa.

> Esse loop de árvores de decisão em sequência lembra o gradiente descendente, aonde a função de otimização é a árvore de decisão.

Porém além de mais lento esse métodos também causa mais overfitting, pois não resolve o problema que a floresta resolve, além de exigir mais ajustes nos hiper-parâmetros. Seu único lado positivo é que para dados mais estruturados (como tabelas e bancos de dados relacionais) ele tem maior acurácia.