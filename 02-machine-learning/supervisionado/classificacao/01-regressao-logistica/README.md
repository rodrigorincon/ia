# REGRESSÃO LOGÍSTICA

Recebe esse nome pois usa uma regressão linear internamente. Ela serve para **categorizar dados em apenas 2 grupos**, sendo um **classificador binário**.

Ele também é o modelo de classificação mais simples (por só ter 2 opções) e é o primeiro a ser ensinado para dar uma noção. Isso não significa que ele só sirva para didática, tem real valor e é bastante usado.

## Estrutura

A regressão logística, semelhante a linear, tem várias variáveis independentes (X) e 1 única variável dependente (Y). Isso significa que vários fatores X influenciam Y (que é a categoria que queremos dar aos dados). X são numéricos e Y é categórico. 

Um ótimo exemplo é ver se um aluno passou de ano ou não dado as notas em 2 provas. Cada prova é uma variável X (prova1 é X1 e prova2 é X2) e a aprovação é a variável Y (passou ou não passou).

A base da regressão logística é a regressão linear, portanto o **objetivo da regressão logística é encontrar os coeficientes da regressão linear**. 

Porém a regressão linear dá uma reta que vai de -infinito a +infinito, ou seja, nosso Y varia de -infinito a +infinito. Porém na logística nosso valor só pode ser de 0 a 1. Essa diferença é crucial e o cerne da matemática desse modelo.

Para transformar infinitos em uma escala de 0 a 1 é usado uma equação chamada sigmoide, que recebe um X que pode ser qualquer valor e a resposta é entre 0 e 1. Essa transformação sigmoide é essencial para poder classificar os dados. Essa transformação é o primeiro passo do modelo, pois os dados tem de estar transformados para serem trabalhados pelos passos seguintes.

Além da transformação sigmoide temos a função de custo que é a Máxima Log-Verossimilhança (também chamada de entropia cruzada) e o gradiente descendente como otimizador.

### Regressão linear

Como o objetivo final é encontrar os coeficientes da regressão linear usada internamente, **os pesos atualizados a cada iteração pelo gradiente descendente são os pesos da regressão linear**.

Diferente dos mínimos quadrados que fazem um cálculo direto para achar esse coeficiente final, aqui a gente define um valor aleatório inicial para ir atualizando e convergindo ao valor verdadeiro a cada loop do gradiente.

> Assim, a cada loop a gente não calcula a regressão, a gente usa a regressão com os coeficientes que já temos (supomos que esses valores são os certos). Depois fazemos a função de custo para ver se eram ou não os pesos certos.

Isso significa que a gente simplesmente faz o cálculo da equação linear ($a_0 + a_1w_1 + a_2w_2...$) em cada loop assumindo que esses pesos tão certos e se não tiverem (segundo a função de custo) os atualizamos com a equação do gradiente e recomeçamos.

### Sigmoide

A transformação sigmoide é o coração da regressão logística, junto com o gradiente descendente. O sigmoide é o que tranforma os dados X de infinito para algo entre 0 e 1. Isso é essencial pois precisamos dar uma porcentagem de chance de um dado estar em uma certa categoria (categoria Y=1).

No fim o que `calculamos é a probabilidade de um dado ser da categoria 1`, por isso Y precisa ser entre 0 e 1 e devemos prestar atenção em qual categoria colocamos como sendo 0 e qual como sendo 1, pois isso será crucial para interpretarmos o resultado final.

Para fazer essa tranformação usamos a equação sigmoide, uma equação que recebe valores de -infinito a +infinito e devolve um valore entre 0 e 1. **Essa conversão é a base de tudo**!

$$sigmoide = \frac{1}{1 + e^{-y_i}}$$

Aonde y é a previsão calculada pela regressão linear (com os pesos aleatórios que vem sendo atualizados a cada iteração). Y é portanto a equação da reta usano os pesos atuais. Então podemos reescrever a equação como:

$sigmoide = \frac{1}{1 + e^{-(w_0 + w_1x_1 + w_2x_2... + w_nx_n)}}$

O gráfico da sigmoide é esse mostrado abaixo, que sempre expreme os valores infinitos de Y entre 0 e 1. 

Repare que se Y for -infinito, $e^{-(-infinito)} = e^{infinito} = infinito$ e portanto $sig = \frac{1}{infinito} = 0$. Se Y for +infinito $e^{-infinito} = 0$, portanto $sig = \frac{1}{1+0} = 1$. Se Y = 0 $e^{0} = 1$, portanto $sig = \frac{1}{1+1} = 1/2$.

![](../images/log_reg.png)

### Logit

O logit nada mais é que o inverso da sigmoide. Enquanto a sigmoide transforma valores infinitos para o intervalo de 0 a 1, o logit faz o oposto, pega valores de 0 a 1 e transforma de -infinito a +infinito. Isso acontece pois o logit é o logaritmo da razão das chances (odds ratio). 

$$logit(p) = ln( \frac{p}{1-p} )$$

A razão das chances é a divisão de duas probabilidades (que variam de 0 a 1). Se a probabilidade p for muito próximo de 1 então a razão fica 1/0 = infinito e seu log também será infinito. Se p for muito próximo de 0 a razão fica 0/1 = 0 e seu log é - infinito. Se p = 0.5 a razão fica 1 e o log de 1 é 0.

### Função de Perda (Entropia Cruzada)

A função de perda é a Entropia Cruzada. Ele é o negativo da Máxima Log-verossimilhança dividido por N, por isso muitas vezes é simplesmente chamado de máxima log-verossimilhança devido a proximidade. Basta calcular a log-verossimilhança, dividir por N e inverter o sinal.

Essa função de perda funciona pois a entropia cruzada calcula justamente a diferença média entre os dados reais e as previsões. A máxima log-verossimilhança encontra os coeficientes que fazem os dados reais mais se encaixarem em uma determinada curva (no caso, Bernoulli), como derivamos e igualamos a zero, temos seu máximo. Invertemos o sinal para ter o mínimo que é o desejo da função de perda. A questão dos sinais é melhor explicado no arquivo da máxima verossimilhança e gradiente descendente.

### Função de Otimização (Gradiente Descendente)

É o esqueleto da regressão. Ele quem faz o loop de atualização dos coeficientes e chama a função de custo para ver se tá perto de convergir ou não. Ele dá a estrutura da regressão, bastando dar o encherto com a função de custo e com o sigmoide e logit.

## Passo-a-Passo

- Coletar e tratar os dados
- Análise Exploratória dos dados
- Define pesos aleatórios iniciais para os coeficientes da regressão linear
- Definimos qual categoria será a 1
- Executa o gradiente descendente
  - Calcula os valores de y previsto de acordo com a reta aleatória inicial (dada pelo pesos aleatórios)
  - Faz transformação sigmoide
  - Calcula a função de custo
  - Atualiza os coeficientes da reg linear com a fórmula do gradiente descendente
  - Repete até convergir

## PREMISSAS

- Independência dos dados
  - Ausência de multicolinearidade (VIF)
- Var dependente **Y categórica ordinal**
- Linearidade das variáveis X com o log das chances de Y
  - Y deve ter formato de sigmoide
  - Passar no teste Box-Tidwell (p-valor > alfa)
- **Não ter outliers**
- Amostra grande

### NÃO PRECISA SEGUIR ESSAS REGAS

Por outro lado a regressão não precisa seguir as seguintes regras:

- Seguir a distribuição normal
- Não precisa ter homocedasticidade (variância igual dos erros)

> Ou seja, não precisa testar os resíduos.

## QUANDO NÃO USAR

- Quando houver risco de, por puro acaso, pegar 2x o mesmo dado para análise (independência dos dados)
- Quando os dados forem pareados (antes/depois) (independência dos dados)
- Encontrar forte correlação entre as variáveis independentes (multicolinearidade)
- Não conseguir fazer uma regressão linear entre os dados e o log da probabilidade de Y
- Categorias de Y não puderem ser ordenadas/rankeadas

## TAMANHO MÍNIMO DA AMOSTRA

Para a regressão logística ser precisa é preciso um número grande de amostras. A regra geral é pelo menos 10 amostras na cateogria menos frequente para cada X. Ou seja, a equação para a o tamanho mínimo é:

$n = \frac{10k}{p_m}$

Aonde

- k é o número de variáveis independentes X
- $p_m$ é a probabilidade da categoria menos provável

## MÉTRICAS DE QUALIDADE

A regressão logística precisa passar os testes de hipótese de Box-Tidwell (teste de linearidade do logit), no VIF (ver se as variáveis não possuem multicolinearidade), no teste de Wald (testa se cada coeficiente é estatisticamente diferente de 0) e no teste de razão de verossimilhança (testa se o modelo é estatisticamente melhor que um chute).

- Box-Tidwell testa uma regra para que o logit possa ser usado. Se não passar a regressão logística não faz sentido para aqueles dados.
- VIF garante que não há multicolinearidade nos dados. Se houver também não faz sentido usar regressão logística para esses dados. Precisa eliminar alguns dados ou usar regularização para diminuir essa influência.
- Wald checa cada um dos coeficientes e vê se são próximos o suficiente de 0 para que se possa dizer que eliminá-los da regressão não faria diferença. Caso não passe remova-os do modelo.
- **Teste de razão de verossimilhança compara dos modelos e diz qual é melhor**. No caso nosso modelo é comparado com um aleatório (cara ou coroa). Podemos usar tanto sozinho (comparando com o aleatório) quanto para comparar 2 modelos criados (com dados ou hiper-parâmetros diferentes).

> Teste todos, mas dentre todos guarde o teste de razão de verossimilhança mais no coração pelo poder de avaliar 2 modelos e dizer qual é melhor. Na vida real sempre testamos várias opções e essa ferramenta será muito útil.