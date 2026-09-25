# PCA

O **PCA (Principal Component Analysis)** é o principal algoritmo não supervisionada de **redução de dimensionalidade** e transformação linear de dados. Enquanto algoritmos de agrupamento (como K-Means ou DBSCAN) buscam separar registros em grupos, o PCA busca **reorganizar e simplificar a estrutura das variáveis X (colunas)**, reduzindo um conjunto grande de atributos correlacionados em um número menor de variáveis não correlacionadas chamadas **Componentes Principais (PCs)**.

Diferente de métodos de transformaçã tradicionais (como log ou z-score) que alteram os valores nas variáveis X (colunas), o PCA altera a quantidade de variáveis X, resumindo e simplificando eles em poucas colunas, mas buscando manter as dispersões. Ao fazer isso no final você fica com poucas colunas para processar.

O objetivo do PCA é projetar os dados em um novo sistema de coordenadas de modo que o primeiro componente principal capture a **maior quantidade possível de variância (informação)** dos dados originais, o segundo capture a segunda maior variância ortogonal ao primeiro, e assim por diante.

## Por Que Usar

O motivo de usar isso é a **maldição da dimensionalidade**. Quando o número de variáveis é muito alto o espaço entre os dados tente a ficar absurdamente alto (virtualmente infinito). Isso ocorre porque quando se tem milhares de dimensões (cada variável/coluna é uma dimensão) é esperado que pelo menos em 1 delas os dados terão um valor absurdamente diferente. Assim todos os dados estarão infinitamente distantes de todos, **sendo impossível qualquer algoritmo de cluster funcionar**.

## Importância da Dispersão dos Dados em Cada Coluna

O PCA assume que **a variância é o equivalente matemático da informação**. Isso significa dizer que os valores em si não são importantes, mas sim a distância entre os dados. Falar que a força é 50 newtowns não é informativo, mas dizer que ela é 10x maior que a força para segurar uma maçã sim é significativo. Do mesmo modo, saber que X=5 não é importante, o que importa é saber que a média é 10 e o desvio padrão é 3. Só então sabemos que esse X significa algo baixo.

Logo, a premissa básica do PCA é que a distribuição de cada coluna é toda informação que precisamos. Com isso podemos **eliminar dimensões com baixa dispersão ou que variam sempre juntas (alta covariância)**, pois se tudo é muito parecido suas mudanças não afetam o resultado final.

Falando de forma mais formal: ao girar os eixos do espaço vetorial para alinhá-los com as direções de maior dispersão dos dados, o PCA permite descartar as dimensões com menor variância (ruído/redundância), reduzindo a dimensão do dataset com a menor perda possível de informação.

## Estrutura e Conceitos Principais

Como queremos diminuir o número de variáveis X (colunas), é importante definir que **P é o número de colunas originais e K é o número de colunas finais**.

O PCA baseia-se na álgebra linear e na estatística multivariada. O seu funcionamento apoia-se em quatro pilares:

### 1. Matriz de Covariância

A **covariância mede a relação linear entre duas variáveis**. Se duas variáveis $X_j$ e $X_k$ crescem juntas, a covariância é positiva; se uma cresce e a outra diminui, é negativa. Ou seja, se ambas são muito correlacionadas, é **informação redundante que deve ser eliminado**.

Dada uma base de dados padronizada com P variáveis, a matriz de covariância M (de dimensão PxP) resume todas as relações de redundância entre os pares de variáveis:

$M = \frac{1}{N - 1} X^T X$

Isso significa elevar a matriz de variáveis X ao quadrado e dividir pelo número de linhas -1.

- Os elementos da diagonal principal representam a **variância** de cada variável X.
- Os elementos fora da diagonal representam a **covariância** entre variáveis distintas (o quanto variam juntas). 
> - São os elementos fora da diagonal (covariância) que devem ser eliminados por representarem redundância.

### 2. Autovetores e Autovalores

A decomposição da matriz de covariância revela as direções principais da estrutura dos dados:

- **Autovetores ($v_k$):** São os vetores de direção que definem a orientação dos novos eixos (os Componentes Principais). Eles indicam os "pesos" ou combinações lineares das variáveis originais.
- **Autovalores ($\lambda_k$):** São escalares numéricos associados a cada autovetor. O autovalor representa a **quantidade de variância total** explicada por aquele componente principal específico.

Pela equação característica da álgebra linear:

$M v_k = \lambda_k v_k$

Ou seja, a **matriz de covariância é nossa lista de autovalores**.

### 3. Variância Explicada

A proporção de informação capturada pelo k-ésimo componente principal é dada pela razão entre seu autovalor $\lambda_k$ e a soma de todos os P autovalores:

Variância Explicada da coluna nova K: $(PC_k) = \frac{\lambda_k}{\sum_{j=1}^{p} \lambda_j}$

A soma acumulada das variâncias explicadas de todas as colunas novas permite decidir quantos componentes manter para preservar, por exemplo, 80% ou 90% da informação original.

### 4. Ortogonalidade e Não-Correlação

Todos os autovetores gerados pelo PCA são **perpendicularmente ortogonais entre si** ($v_j * v_k = 0$ para $j \neq k$). Isso garante que os novos componentes principais tenham **covariância zero**, eliminando completamente o problema de multicolinearidade.

Ou seja, cada coluna nova raz informações 100% novas, sem nenhuma correlação com as colunas antigas.

## Passo-a-Passo

O PCA transforma linearmente um espaço p-dimensional para um subespaço k-dimensional (k < p) através das seguintes etapas:

1. **Padronização dos Dados (Obrigatória):**
   - Transforma-se cada variável $X_j$ para ter média 0 e desvio padrão 1 (Z-score):
   
      $Z = \frac{X - \mu}{\sigma}$

   - Isso elimina problemas de escala e mantém o que realmente importa: as proporções.

2. **Cálculo da Matriz de Covariância:**
   - Calcula-se a matriz de covariância PxP a partir dos dados padronizados Z.

3. **Decomposição em Autovalores e Autovetores:**
   - Resolve-se a equação $M v = \lambda v$ utilizando decomposição espectral ou Decomposição em Valores Singulares (**SVD**).

   - É aqui que a magia acontece.
   
4. **Cálculo da variância explicada para cada K**
   - Calcula a variância explicada para cada coluna nova que vamos fazer.
   - Calcula a partir dos autovalores.

   $(PC_k) = \frac{\lambda_k}{\sum_{j=1}^{p} \lambda_j}$

5. **Ordenação dos Componentes:**
   - Ordenam-se os pares (autovetor, autovalor) em ordem decrescente de autovalor:
   
     $\lambda_1 \ge \lambda_2 \ge \dots \ge \lambda_p$

6. **Seleção dos k Primeiros Autovetores:**
   - Selecionam-se os k autovetores com maiores autovalores para construir a **Matriz de Projeção** W (de dimensão PxK).
   - A matriz de projeção W nada mais é que a lista dos maiores autovetores.
   - Pega os K maiores autovetores porque queremos k colunas no final.

7. **Projeção dos Dados Original no Novo Subespaço:**
   - Multiplica-se a matriz de dados padronizada Z pela matriz de peso W:
   
     $X_{\text{PCA}} = Z * W$

   - $X_{\text{PCA}}$ é a nova base de dados reduzida, de dimensão NxK.

## Exemplo

Considere uma base de dados com N=4 linhas e 2 colunas ($X_1$ e $X_2$). Para facilitar as colunas já estão padronizadas com z-score.

- $X_1$: Frequência relativa de compras
- $X_2$: Valor médio relativo das compra

### Passo 1: Base de Dados Padronizada

| Cliente | $X_1$ | $X_2$ | Coordenada $(X_1, X_2)$ |
| :--- | :--- | :--- | :--- |
| **C1** | $-2$ | $-2$ | $(-2, -2)$ |
| **C2** | $-1$ | $-1$ | $(-1, -1)$ |
| **C3** | $1$ | $1$ | $(1, 1)$ |
| **C4** | $2$ | $2$ | $(2, 2)$ |

Portanto Z é:

$Z = \begin{bmatrix} -2 & -2 \\ -1 & -1 \\ 1 & 1 \\ 2 & 2 \\ \end{bmatrix}$

### Passo 2: Cálculo da Matriz de Covariância M

Com N=4 (usando a fórmula com divisor N-1 = 3):

- $\text{Var}(X_1) = \frac{(-2)^2 + (-1)^2 + 1^2 + 2^2}{3} = \frac{4 + 1 + 1 + 4}{3} = \frac{10}{3} \approx 3.33$

- $\text{Var}(X_2) = \frac{(-2)^2 + (-1)^2 + 1^2 + 2^2}{3} = \frac{10}{3} \approx 3.33$

- $\text{Cov}(X_1, X_2) = \frac{(-2)(-2) + (-1)(-1) + (1)(1) + (2)(2)}{3} = \frac{10}{3} \approx 3.33$

A Matriz de Covariância é:

$M = \begin{bmatrix} 3.33 & 3.33 \\ 3.33 & 3.33 \end{bmatrix}$

### Passo 3: Cálculo dos Autovalores e Autovetores

Resolvendo a determinante $\det(M - \lambda I) = 0$:

$(3.33 - \lambda)^2 - 3.33^2 = 0 \implies \lambda_1 = 6.67, \quad \lambda_2 = 0$

Calculando os autovetores unitários correspondentes:

- Para $\lambda_1$ = 6.67: $v_1 = \begin{bmatrix} \frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} \end{bmatrix} \approx \begin{bmatrix} 0.707 \\ 0.707 \end{bmatrix}$ (Direção diagonal de máxima variação)

- Para $\lambda_2$ = 0: $v_2 = \begin{bmatrix} -\frac{1}{\sqrt{2}} \\ \frac{1}{\sqrt{2}} \end{bmatrix} \approx \begin{bmatrix} -0.707 \\ 0.707 \end{bmatrix}$ (Direção ortogonal com zero variância)

### Passo 4: Variância Explicada

- **Variância do $PC_1$:** $\frac{6.67}{6.67 + 0} = 100$%
- **Variância do $PC_2$:** $\frac{0}{6.67 + 0} = 0$%

Como $PC_1$ captura **100% da informação**, podemos descartar $PC_2$ sem perder dado nenhum!

### Passo 5 e 6: Seleciona os K maiores autovalores

Queremos k=1, logo pegamos apenas o maior autovalor ($\lambda_1$).

$W = \lambda_1 = \begin{bmatrix} 0.707 \\ 0.707 \end{bmatrix}$

### Passo 7: Projeção dos Pontos no $PC_1$ (Redução para 1D)

A equação de transformação para $PC_1$ é $PC_1 = Z[0] * W[0] = 0.707 \cdot X_1 + 0.707 \cdot X_2$:

- **C1:** $0.707(-2) + 0.707(-2) = -1.414 - 1.414 = \mathbf{-2.83}$
- **C2:** $0.707(-1) + 0.707(-1) = -0.707 - 0.707 = \mathbf{-1.41}$
- **C3:** $0.707(1) + 0.707(1) = 0.707 + 0.707 = \mathbf{1.41}$
- **C4:** $0.707(2) + 0.707(2) = 1.414 + 1.414 = \mathbf{2.83}$

**Resultado:** Reduzimos com sucesso a base de 2 variáveis para 1 única dimensão sintética ($PC_1$) mantendo a totalidade da informação original!

## PREMISSAS

- **Linearidade:** Assume que as relações fundamentais entre as variáveis originais são lineares.
- **Padronização de Escala (Obrigatória):** Evita que variáveis em escala maior tomem conta do sistema.
   - Ex: Renda tem variância enorme (de 1500 até 30mil) comparada Idade (de 0 a 100).
- **Variância como Informação:** O algoritmo assume que quanto maior a variância em uma direção, mais relevante é o sinal, e direções com pouca variância são ruídos.
- **Dados numéricos e contínuos:** Exige variáveis numéricas contínuas para o cálculo de médias, variâncias e matrizes de covariância.

## QUANDO USAR

- **Redução da Maldição da Dimensionalidade:** Quando há centenas ou milhares de variáveis (ex: dados genômicos, processamento de imagens, embeddings) que deixam os modelos lentos ou sujeitos ao overfitting.
- **Eliminação de Multicolinearidade:** Como pré-processamento para algoritmos de regressão ou modelos lineares sensíveis a atributos fortemente correlacionados.
- **Visualização de Dados:** Reduzir um dataset para até 2 ou 3 colunas permitindo gerar gráficos de dispersão e inspecionar a separabilidade natural dos dados.
- **Compressão e Desempenho:** Reduzir o uso de memória e acelerar o tempo de treinamento de modelos de Machine Learning.

## QUANDO NÃO USAR

- **Relações Não-Lineares Complexas:** Se os dados formarem estruturas curvas ou variedades não-lineares (ex: padrão em caracol ou superfície em "S"), o PCA falhará em capturar a estrutura (prefira **Kernel PCA**, **t-SNE** ou **UMAP**).
- **Exigência de Interpretabilidade:** Se o negócio precisa saber exatamente "qual o efeito do atributo Idade", o PCA impede essa leitura direta.
- **Dados Predominantemente Categóricos Nominais:** A variância e covariância não fazem sentido para dados categóricos (prefira **Análise de Correspondência Múltipla - MCA**).

## COMO DETERMINAR O NÚMERO DE COMPONENTES (k)

### 1. Variância Explicada Acumulada

Soma-se a variância explicada de cada componente e seleciona-se o menor k que atinja o a porcentagem limite de perda de informação (geralmente entre **80% e 95%** de variância acumulada).

### 2. Gráfico do Inflexão / Scree Plot

Plota-se o autovalor ou a variância explicada de cada componente em ordem decrescente:

- **Critério do Cotovelo:** Escolhe-se o ponto de inflexão ("cotovelo") da curva, onde a adição de novos componentes traz ganhos marginais irrisórios.
- **Critério de Kaiser:** Retém-se apenas os componentes principais cujos autovalores sejam **maiores que 1.0** (considerando dados padronizados com variância unitária), garantindo que o componente explica mais variância do que uma única variável original isolada.

## COMPARATIVO: PCA vs. t-SNE / UMAP

| Característica | PCA | t-SNE / UMAP |
| :--- | :--- | :--- |
| **Abordagem** | Cria novas variáveis (combinações lineares) | Projeção Não-Linear baseada em grafos/distribuições |
| **Interpretabilidade** | Baixa (variáveis abstratas $PC_k$) | Muito Baixa (eixos não possuem significado) |
| **Tipo de Relação** | **Linear** | **Não-Linear** |
| **Uso Principal** | Compressão, descorrelação e aceleração | Visualização de dados em 2D ou 3D |
| **Custo Computacional** | Baixo a Médio ($O(p^3)$ na decomposição) | Alto / Muito Alto em grandes bases |
