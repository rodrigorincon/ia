# MÍNIMOS QUADRADOS PONDERADOS (WLS)

É uma extensão do algoritmo de Mínimos Quadrados Ordinários (OLS) usado para minimizar o erro de uma equação quando as observações não possuem a mesma confiabilidade. É muito usado quando os dados apresentam variâncias diferentes (heterocedasticidade). É importante entender por que precisamos adicionar um "peso" na equação original para não confundir os dois.

Os mínimos quadrados ordinários tratam todo ponto como tendo a mesma relevância, porém pontos cujos as medições são mais dispersas são menos confiáveis e podem distorcer nossa reta. Os mínimos quadrados ponderados dão prioridade na reta para os pontos que têm menos dispersão.

## O Problema e a Solução

### Heterocedasticidade

É o nome feio que damos quando o erro (a dispersão dos dados em volta da reta) não é constante. Na regressão linear padrão, nós assumimos que todos os pontos têm a mesma variância (homocedasticidade). Mas na vida real, às vezes, à medida que o valor de X aumenta, a dispersão de Y também aumenta (pense no salário vs. gastos: quem ganha pouco gasta quase o mesmo de forma previsível, quem ganha muito pode gastar muito ou pouco, a variância do erro é bem maior). 

A heterocedasticidade é `O QUE` quebra a precisão do nosso modelo tradicional.

**Objetivo**: corrigir a influência desigual que pontos muito dispersos (e menos confiáveis) têm na inclinação da reta final.

### Ponderação (Os Pesos)

Para resolver isso, o algoritmo atribui um peso (W) para cada observação. Pontos que sabemos que têm menor variância (são mais precisos/confiáveis) recebem um peso maior. Pontos com muita variância (muita incerteza) recebem um peso menor. A matriz de pesos é o `COMO` ele conserta o problema.

**Objetivo**: penalizar os erros de pontos mais confiáveis para forçar a reta a passar mais perto deles, permitindo que a reta ignore um pouco os pontos mais caóticos.

## Importância do Peso (W)

`Peso (W) é a importância ou relevância dada a cada erro na hora de calcular a soma total. Ele atua como um multiplicador do resíduo de cada ponto verdadeiro para a reta.`

Já que os mínimos quadrados definem a melhor reta minimizando a soma dos quadrados dos erros, na versão ordinária nós apenas somamos todos eles: $e_1^2 + e_2^2 + ... + e_n^2$. Na versão ponderada (WLS - Weighted Least Squares), nós multiplicamos cada erro pelo seu peso correspondente antes de somar.

$e = w_1*e_1^2 + w_2*e_2^2 + ... + w_n*e_n^2$

O objetivo dos mínimos quadrados ponderados é definir a reta com menor erro ponderado possível. Ou seja, `errar em um ponto de peso alto "custa" muito mais caro para o algoritmo do que errar num ponto de peso baixo`. 

Soma dos Erros Ponderados = $\sum w_i e_i^2$

## COMO FUNCIONA

O algoritmo `busca encontrar os coeficientes aonde a soma dos quadrados dos erros multiplicados pelos seus pesos é a menor possível`. Por isso seu passo-a-passo é bem parecido com o anterior, apenas com a inclusão de uma variável extra.

- Define-se o peso $w_i$ para cada observação X e Y. Geralmente $w_i = \frac{1}{\sigma_i^2}$ (inverso da variância daquele ponto), mas o critério pode mudar.
- Multiplica-se cada erro ao quadrado por esse peso.
- Aplica-se a minimização (derivada) sobre essa nova soma para encontrar os coeficientes ponderados.

> Ou seja, `não precisamos descobrir os pesos`. Os pesos são simplesmente o inverso da variância das medições. Os únicos valores a descobrir continuam sendo os coeficientes.

## PROVA (EM MATRIZES)

Como vimos na explicação dos mínimos quadrados múltiplos, fazer as contas de regressão com muitas variáveis e agora com *pesos* diferentes para cada observação torna o cálculo puramente algébrico um pesadelo e muito repetitivo. Por isso, a demonstração e o uso prático dos mínimos quadrados ponderados é praticamente sempre feito através de matrizes.

Lembrando a nossa equação matricial:

$$Y = X * A + E$$

Isolando os erros fica:

$$E = Y - X * A$$

### Adicionando a Matriz de Pesos (W)

No OLS, queríamos minimizar $E * E^T$. Agora, nós introduzimos uma matriz diagonal $W$ (matriz de pesos), onde a diagonal principal contém os pesos $w_1, w_2, ... w_n$ de cada observação e o resto é tudo zero.

$W = \begin{bmatrix}
w_1 & 0 & 0 & ... & 0 \
0 & w_2 & 0 & ... & 0 \
0 & 0 & w_3 & ... & 0 \
... & ... & ... & ... & ... \
0 & 0 & 0 & ... & w_n
\end{bmatrix}$

Nossa nova função a ser minimizada (Soma dos Quadrados dos Erros Ponderados) se torna a multiplicação do erro transposto, pela matriz de pesos, pelo erro:

$F(A) = E^T * W * E$

Substituindo $E$ pela equação isolada do erro:

$F(A) = (Y - X * A)^T * W * (Y - X * A)$

### Derivada para encontrar o mínimo

Expandindo essa multiplicação (lembrando das propriedades de transposição de matrizes onde $(XA)^T = A^TX^T$ e que, como $W$ é uma matriz diagonal, ela é simétrica $W = W^T$):

$F(A) = Y^TWY - 2A^TX^TWY + A^TX^TWXA$

Até então temos a soma dos erros ponderados. **Para encontrar o menor valor fazemos a derivada em relação a A e igualamos a 0**, exatamente igual fizemos no OLS.

$\frac{\partial{F}}{\partial{A}} = -2X^TWY + 2X^TWXA = 0$

Isolando A temos:

$2X^TWXA = 2X^TWY$

Dividindo os dois lados por 2, chegamos na base da equação:

$X^TWXA = X^TWY$

Passando o termo do X para o outro lado invertido:

$$A = (X^TWX)^{-1} * X^TWY$$

Com essa equação conseguimos calcular todos os coeficientes da regressão ponderada.

### Em resumo

A regressão ponderada não é bicho de sete cabeças. É exatamente o mesmo cálculo matricial, a mesma lógica e o mesmo conceito, mas nós colocamos um "recheio" no meio (a matriz W) multiplicando o X e o Y para garantir que os dados bons puxem a reta para si.
 
Repare na semelhança:

> Simples: $A = (X^TX)^{-1} * X^TY$
>
> Ponderado: $A = (X^TWX)^{-1} * X^TWY$

## Calculando os pesos

O peso é definido pela variância e a variância é o quão dispersos os dados estão da reta. Então `como definir os pesos se ainda não temos a reta?`

A resposta é fazer 2 regressões: uma normal (OLS) para criar a reta sem pesos e a partir dela medir a variância. Olhar os resíduos dessa regressão nos diz o quanto os valores X estão distantes a reta criada pelo OLS. Lembrando que resíduo = erro. Esses erros ao quadrado serão nossa variância e então podemos fazer **1 / variância** para calcular os pesos.

Uma vez com os pesos podemos fazer os mínimos quadrados ponderados, pois sabemos quais pesos usar para cada ponto ao ver o quanto eles fugiram da reta inicial.

## Semlhança com Generalizado (GLS)

Os mínimos quadrados ponderados e generalizados são quase iguais. A diferença está na matriz de pesos (no generalizado chamado matriz de covariância). Enquanto no ponderado apenas a diagona possui valores e o resto da matriz é 0, no generalizado ela pode ter valores em todos os campos.

Isso acontece porque o peso é uma matriz e essa matriz dos pesos na verdade é a **matriz de covariância** super simplificada. A matriz de covariância mede o quanto cada variável X está correlacionada com todas as outras vars X, por isso todos os valores da matriz são preenchidos. No caso mais simplificado dos mínimos ponderados apenas a diagonal é preenchida, ou seja, as correlações entre as variáveis X é ignorada e considerada apenas a correlação de cada variável consigo mesma (diagonais da matriz). Como a **covariância de uma var com ela mesma é igual a variância**, ao definirmos o peso a partir da variância estamos na verdade fazendo o peso a partir da covariância, já que a covariância e variância podem ser a mesma coisa nesse cenário espcífico.

$Cov(X,X,) = Var(X)$

### Quando usar cada um

Se suas variáveis possuem apenas heterocedasticidade então pode usar os mínimos ponderados que é mais simples. Agora se seus dados tem **heterocedasticidade e autocorrelação** então deve usar a versão mais completa e complexa (generalizada).

Mas o importante é entender que ambas são a mesma coisa, só que a ponderada é uma versão enxugada da generalizada e que a generalizada serve para todos os casos da ponderada e mais outros.