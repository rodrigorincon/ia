# MÍNIMOS QUADRADOS ORDINARIOS (OLS)

É um algoritmo de otimização matemática usado para minimizar o erro de uma equação. É usado para calcular os parâmetros da regressão linear. É importante entender o que é cada um exatamente e onde cada um começa e termina para não confundir os dois.

Também é chamado de OLS. Cada variação desse algoritmo é chamado por uma sigla diferente.

## Diferença entre os termos

### Regressão Linear

É um modelo que tenta definir a relação entre um conjunto de variáveis/características X a uma única variável/característica independente Y. Todas as variáveis devem ser numéricas e contínuas. Para tanto a regressão linear transforma a relação entre as variáveis em uma equação linear, resumindo as relações em uma linha reta. Isso torna possível encontrar o valor final fazendo 1 única equação.

**Objetivo**: transformar as relações entre as variáveis numa reta do tipo Y = aX + b.

Para transformar a relação entre as variáveis em uma linha reta ele usa os mínimos quadrados. A regressão é `O QUE` faz.

### Mínimos Quadrados

É um algoritmo de otimização matemática que minimiza a soma dos quadrados dos erros. Para tanto ele testa diversas combinações de pesos diferentes e vai mudando até achar os pesos que formam a linha reta com o menor erro possível. Ela é o `COMO` faz. 

**Objetivo**: encontrar os pesos que fazem a reta ter a menor soma de erros possível. 

### Em Resumo

A regressão linear define a reta, e os mínimos quadrados calculam exatamente qual é a melhor posição dessa reta no gráfico.

BOTAR A IMAGEM DO FLUXO AQUI

## Importância do Erro

`Erro (ou resíduo) é a diferença entre o valor real e o valor da reta/estimado (valor da regressão). Ele mede a distância de cada ponto verdadeiro da reta.`

Já que os mínimos quadrados definem a melhor reta que descreve os pontos, a que melhor se aproxima, ela não é perfeita. Impossível passar em cima de todos os pontos sendo uma reta. Assim, alguns pontos podem passar exatamente em cima da reta, mas a maioria vai passar próximo. A distância do ponto (dado real usado para criar a reta) da reta para o mesmo X é o erro ou resíduo.

**O objetivo dos mínimos quadrados é definir a reta com menor erro médio possível**. Ou seja, a **dispersão dos pontos em volta da reta** tem de ser a mínima possível. Isso significa ter a menor variância dos resíduos/erros.

e = real - previsto = y - ŷ

## Relação com a correlação

Uma das formas de calcular os mínimos quadrados usa a correlação como base, pois calcula a correlação entre as vars independentes com a dependentes e das vars independentes com elas mesmas (variância). Ou seja, calcula a variância de todas as vars independentes e delas com a dependente.

Em todas as vertentes dos mínimos quadrados `o que buscamos é encontrar os coeficientes aonde o quadrado dos erros é o menor possível (por isso o nome)`. Em todas suas versões dos mínimos quadrados queremos elevar cada erro ao quadrado (variância) e somar todos eles.

Lembrando que isso nada mais é que a variância sem a divisão pelos graus de liberdade, pois o erro é a diferença entre o valor real e a média (ou valor esperado pela regressão). **A soma dos quadrados sempre pode ser entendido como a variância ou a dispersão dos dados**, seja a dispersão em volta da média ou em volta do valor esperado (reta da regressão). Daí vem o uso da correlação na equação dos coeficientes.

### TERMOS COMUNS

Alguns trechos do cálculo recebem nomes para limpar a equação e facilitar o entendimento. A maioria deles está dentro da fórmula da correlação.

$S_{xx} = \sum{ (x_i - media_x)^2 }$ mede a variância de alguma var X (porém sem a divisão por N-1). Também chamado de **soma dos quadrados de X**.

$S_{yy} = \sum{ (y_i - media_y)^2 }$ mede a variância da var dependente Y (porém sem a divisão por N-1). Também chamado de **soma dos quadrados de Y**.

$S_{xy} = \sum{ (x_i - media_y)(y_i - media_y) }$ mede a variância entre as vars X e Y. Mede a dispersão dos pontos no gráfico. Também chamado de **soma dos quadrados de X e Y**.

Com isso podemos escrever a correlação como:

$r = \frac{S_{xy}}{\sqrt{S_{xx}S_{yy}}}$

e como correlação é a covariância dividido pelo produto dos desvios padrões podemos chamar a covariância de $S_{xy}$.

## COMO FUNCIONA

O algoritmo `busca encontrar os coeficientes aonde o quadrado dos erros é o menor possível (por isso o nome)`. Por isso seu passo-a-passo é bem simples.

- Calcula a soma de todos os valores de cada variável X e de Y
- Calcula a soma dos quadrados de X e a soma da multiplicação entre X e Y
- Aplica essas somas na fórmula dos coeficientes

$$a = \frac{n \sum xy - \sum x \sum y}{n \sum x^2 - (\sum x)^2}$$

$$b = \frac{\sum y - a \sum x}{n}$$

## PROVA

Eu posso calcular os mínimos quadrados de duas formas diferentes, através da correlação ou através de derivada. As duas chegam na mesma equação final. Podemos provar a equação dos mínimos quadrados tanto usando a fórmula da correlação e da covariância quanto via derivada que ambas encontram a mesma fórmula. Irei provar ambas abaixo.

### Usando correlação

Para isso precisamos saber que a inclinação de uma reta é sempre definida pela correlação e a divisão dos desvios padrões. A correlação determina a inclinação da reta e a divisão dos desvios dá a unidade de medida.

$$a = r \frac{Desvio_y}{Desvio_x}$$

Vamos expandir a equação da correlação

$r = \frac{\sum (x_i - \bar{x})(y_i - \bar{y})}{\sqrt{S_{xx}} \sqrt{S_{yy}}}$

E o desvio padrão pode ser reescrito da seguinte forma

$Desvio_x = \sqrt{S_{xx}}{n-1}$

Portanto a equação da inclinação A pode ser reescrita como

$a = \frac{S_{xy}}{ \sqrt{S_{xx}} \sqrt{S_{yy}} } \frac{ \sqrt{ \frac{S_{yy}}{n-1} } }{ \sqrt{ \frac{S_{xx}}{n-1} } }$

Cancelamos n-1 em cima e embaixo, ficando

$a = \frac{S_{xy}}{ \sqrt{S_{xx}} \sqrt{S_{yy}} } \frac{ \sqrt{ S_{yy} } }{ \sqrt{ S_{xx} } }$

Juntamos as 2 frações e cancelamos $S_{yy}$, ficando 

$a = \frac{S_{xy}}{ \sqrt{S_{xx}} \sqrt{ S_{xx} } } = \frac{S_{xy}}{ S_{xx} }$

Com isso encontramos que o coeficiente A é a divisão do somatório de x * y pela soma dos quadrados de x. Retornando a notação original encontramos a equação do mínimo quadrado.

$$a = \frac{ \sum (x - \bar{x})(y - \bar{y}) }{\sum (x - \bar{x})^2 }$$

### Usando derivada

Lembrando que os mínimos quadrados quer minimizar a soma do quadrados dos erros, fazemos literalmente isso. Minimizar significa encontrar o ponto onde essa relação (equação) tem seu menor valor, ou seja, onde sua derivada é 0. Para isso temos de definir a equação que deve ser derivada.

A função a derivar é a soma do quadrado dos erros $f(a,b) = e_1^2 + e_2^2 ... e_n^2$. Sendo o erro a diferença entre o valor medido (ax + b com A e B a definir) menos o valor verdadeiro (y). Com isso escrevemos nossa função sendo

$$f(a,b) = \sum (y_i - ax_i - b)^2$$

Derivando a função por A e B fica:

$\frac{\partial{F}}{\partial{A}} = -2 \sum x_i(y_i - ax_i - b) = 0$ para o cálculo do coeficiente.

$\frac{\partial{F}}{\partial{B}} = -2 \sum (y_i - ax_i - b) = 0$ para o cálculo do intercepto.

Separando os somatórios em partes diferentes e dividindo por -2 fica

$\frac{\partial{F}}{\partial{A}} = \sum xy - \sum ax^2 -  \sum xb = 0$ para o cálculo do coeficiente.

$\frac{\partial{F}}{\partial{B}} = \sum y - \sum ax - \sum_{i=1}^n b = 0$ para o cálculo do intercepto.

Sabendo que $\sum_{i=1}^n b = nb$ temos

$\frac{\partial{F}}{\partial{A}} = \sum xy - \sum ax^2 - b \sum x = 0$ para o cálculo do coeficiente.

$\frac{\partial{F}}{\partial{B}} = \sum y - a \sum x - nb = 0$ para o cálculo do intercepto.

---

Isolando B na equação do intercepto fica

$b = \frac{\sum y - a \sum x}{n} = \frac{\sum y}{n} - \frac{a \sum x}{n} = \bar{y} - a \bar{x}$

Veja que encontramos a equação para o intercepto

$$b = \bar{y} - a \bar{x}$$

Ou 

$$b = \frac{S_y - a S_x}{n}$$

Lembrando que $S_x$ significa a soma de todos os x (somatório) e o mesmo com y.

---

Agora substituindo B na na equação da deriada de A fica

$\sum xy - \sum ax^2 - (\bar{y} - a \bar{x}) \sum x = 0$ 

$\sum xy - \sum ax^2 - \bar{y} \sum x + a \bar{x} \sum x = 0$

Isolando A temos

$a \sum x^2 - a \bar{x} \sum x = - \sum xy + \bar{y} \sum x$

$a \sum x(x - \bar{x}) = \sum x(-y + \bar{y})$

$$a = \frac{\sum x(y - \bar{y})}{\sum x(x - \bar{x})}$$

Ou

$$a = \frac{n S_{xy} - S_xS_y}{n S_{xx} - (S_x)^2}$$

Os n aparecem porque desfazemos a fórmula da média.

# MÍNIMOS QUADRADOS MÚLTIPLOS

Essa explicação foi para o caso mais simples, com apenas 1 variável X. Na vida real temos vários X afetando nosso Y. O cálculo para vários X é o mesmo, muda nada. Porém é muito mais fácil fazer esses cálculos todos quando transformamos em matrizes.

Com uma única variável como foi até o momento a equação final é 

$y = A_0 + A_1X + erro$

E nos mínimos quadrados só temos que achar a soma dos quadrados de x e de xy. Quando temos vários Xs

$y = A_0 + A_1X_1 + A_2X_2 + A_3X_3 + ... + A_kX_k + erro$

precisamos calcular A1, A2, A3... $A_k$ e nos mínimos quadrados temos de achar a soma dos quadrados de X1, X2... $X_k$ e de cada um deles com Y ($X_1Y, X_2Y, X_3Y...$). Isso começa a ficar trabalhoso tanto de escrever como de calcular. Por sorte podemos usar notação matricial para escrever todas essas multiplicações e somatórios de uma única vez.

> A matriz une soma de multiplicações (multiplicamos todos os valores de uma linha por todos de uma coluna e somamos), por isso quando temos somatórios de coisas sendo multiplicadas a matriz é uma excelente forma de simplificar a conta.

Repare que **para encontrar cada Y eu preciso usar todos os coeficientes**. Isso também acontece na versão simples, aonde $y_1 = a_0 + a_1x$. Por ser o único y que tínhamos essa relação não era tão óbvia.

Essa equação não define o coeficiente, mas define como Y (que nós conhecemos) é definido por eles. Como temos k variáveis dessa, podemos organizar todas em uma única matriz.

$\begin{bmatrix} 
y_1 \\
y_2 \\
y_3 \\
... \\
y_k
\end{bmatrix} = \begin{bmatrix}
1 & x_{1,1} & x_{2,1} & ... & x_{n,1} \\
1 & x_{1,2} & x_{2,2} & ... & x_{n,2} \\
1 & x_{1,3} & x_{2,3} & ... & x_{n,3} \\
... & ... & ... & ... & ... \\
1 & x_{1,k} & x_{2,k} & ... & x_{k,k}
\end{bmatrix} * \begin{bmatrix}
A_0 \\
A_1 \\
A_2 \\
... \\
A_k
\end{bmatrix} + \begin{bmatrix}
erro_0 \\
erro_1 \\
erro_2 \\
... \\
erro_k \\
\end{bmatrix}
$

A primeira coluna ser toda 1 é para termos o intercepto (A0) em todas as equações.

A matriz acima pode ser resumida na equação abaixo

$$Y = X * A + E$$

Aonde

- Y é a lista de todos os valores de y
- X é a matriz com todos os dados de todos os X
- A são os coeficientes que queremos definir (a1, a2, a3...)
- E são os nossos erros (resíduos)

A matriz é só uma forma mais organizada de resumir o sistema linear que temos, de k equações com k variáveis. Poderíamos fazer também no seguinte formato:

$Y_1 = A_0 + A_1X_{1,1} + A_2X_{2,1} ... + A_nX{n,1} + erro_1$

$Y_2 = A_0 + A_1X_{1,2} + A_2X_{2,2} ... + A_nX{n,2} + erro_2$

$Y_k = A_0 + A_1X_{1,k} + A_2X_{2,k} ... + A_nX{n,k} + erro_k$

Lembrando que as únicas variáveis que não sabemos os valores os os coeficientes A. 

### Conceito dos mínimos quadrados

Como nos mínimos quadrados queremos encontrar a menor soma dos quadrados dos erros, isolamos o erro na equação. **Lembrando que a matriz dos erros já é a soma de todos os erros**.

$E = Y - X * A$

Elevando ao quadrado fica

$E * E^T = (Y - X * A) * (Y - X * A)^T$

Lembrando que em matrizes para elevar algo ao quadrado precisamos multiplicar a matriz pela sua versão transversal. Assim $E^2$ vira $E * E^T$. O mesmo vale para o outro lado da equação.

Fazendo a multiplicação fica

$E * E^T = YY^T - 2X^TYA + XX^TAA^T$

### Derivada para encontrar o mínimo

Até então temos a soma dos quadrados dos erros, mas não encontramos o valor mínimo deles. Falta o mínimo do mínimos quadrados. **Para encontrar o menor valor fazemos a derivada e igualamos a 0**. Como queremos encontrar os coeficientes A derivamos em relação a eles.

$\frac{\partial{E}}{\partial{A}} = -2X^TY + 2XX^TA = 0$

Isolando A temos

$$A = (XX^T)^{-1} * X^TY$$

Com essa equação conseguimos calcular todos os coeficientes da regressão.

### Em resumo

> A regressão com matrizes não é outra coisa. É exatamente o mesmo cálculo e a mesma fórmula, porém escrita de outro modo para deixar mais simples e enxuto.

# Variações

Existem diversas variações desse algoritmo para quando não cumpre as premissas de normalidade ou homocedasticidade ou para muitas variáveis.

- Mínimos quadrados ordinais (OLS)
  - Padrão
  - **Quando usar**: resíduos normais, homoscedasticidade dos erros e variáveis não são auto-correlacionadas
- Mínimos quadrados ponderados (WLS)
  - Cada ponto tem um peso
  - Outliers tem peso próximo de 0, diminuindo sua influência no cálculo
  - **Quando usar**: resíduos tem **heteroscedasticidade** (variância nos erros)
  - **Uso ideal**: quando conhecemos previamente as incertezas dos dados
    - Senão teremos de ter de calculá-los manualmente e acabamos ficando mais parecido com o GLS
  - Ex: medições feitas com instrumentos de diferentes precisões ou bases de dados com características diferentes, onde a incerteza de cada medição é previamente conhecida
- Mínimos quadrados generalizados (GLS)
  - Usa uma matriz de covariância no lugar dos pesos
  - Generalização do ponderado, trocando pesos por uma matriz das covariâncias
  - **Quando usar**: resíduos tem **multicolinearidade e heterocedasticidade** (variáveis X correlacionadas)
- Mínimos quadrados Robustas (RLS)
  - Semelhante ao ponderado, porém dá os pesos dos pontos de forma iterativa
    - Iterativo: recalcula a reta toda vez que encontra um ponto muito discrepante
  - **Quando usar**: resíduos tem **heteroscedasticidade** (variância nos erros) e **não conhecemos previamente as incertezas** dos dados
  - **Uso ideal**: quando **não conhecemos previamente as incertezas** dos dados
  - Ex: dados possuem erros de medição, de digitação ou outros que distorçam gravemente
- Mínimos quadrados não lineares (NLS)
  - Quando os dados são **polinomiais**
  - Usa métodos numéricos iterativos (outros algoritmos) para convergir ao menor erro
  - Não será analisado aqui por fugir do escopo
- Mínimos quadrados parciais (PLS)
  - Quando tenho **mais variáveis do que dados** ou tenho **multicolinearidade**
  - Todos os outros exigem que a amostra seja maior que o número de variáveis, esse não
  - Reduz as vars, eliminando as correlacionadas, até ter um número aceitável

## Quando Usar Cada Um

- Heterocedasticidade: mínimos ponderados ou robustos (a depender do conhecimento prévio dos dados)
- Não normalidade: mínimos robustos
- Multicolinariedade: mínimos generalizados
- Muitas vars e poucos dados: mínimos parciais

# Sobre os exercícios

Podemos encontrar aqui um exemplo de como implementar os mínimos quadrados ordinários manualmente e como usá-lo com bibliotecas já prontas. Além disso vemos outras variações do algoritmo nas respectivas pastas. A explicação de seus funcionamentos e exemplos estão nas pastas.