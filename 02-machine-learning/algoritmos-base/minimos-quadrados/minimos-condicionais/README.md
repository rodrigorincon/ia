# MÍNIMOS QUADRADOS CONDICIONAIS (CLS)

É uma técnica de estimação de parâmetros fortemente utilizada na modelagem de **séries temporais** (como modelos ARMA, ARIMA e GARCH). Enquanto o OLS, WLS e GLS lidam com a estrutura dos erros no espaço, os Mínimos Quadrados Condicionais (Conditional Least Squares - CLS) lidam com o fato de que, em dados sequenciais, o presente **depende do passado**. Portanto ele é utilizado quando temos **forte autocorrelação**.

Na modelagem de séries temporais, obter a estimativa perfeita (como a Máxima Verossimilhança Exata) costuma ser um pesadelo matemático e computacional, pois o primeiro ponto da série não tem um "passado" para se apoiar. O CLS surge como a solução prática: ele "condiciona" o cálculo aos primeiros valores observados, simplificando drasticamente a matemática ao tratar esses valores iniciais como constantes fixas. Portanto ele é uma solução mais simples e rápida de calcular os coeficientes da regressão.

## O Problema e a Solução

### Dependência Temporal e Valores Iniciais

Em modelos de séries temporais (ex: um modelo Autoregressivo onde $Y_t$ depende de $Y_{t-1}$), cada ponto de dado carrega a inércia do ponto anterior. Se tentarmos calcular a soma dos quadrados dos erros clássica, esbarramos num paradoxo logo no início: como calcular o erro do instante t=1 se ele depende do instante t=0 (que nós não temos)? 

Calcular a distribuição conjunta exata de todos os pontos exigiria integrais complexas e suposições fortes sobre o início dos tempos. É `O QUE` torna a estimação de séries temporais matematicamente pesada.

**Objetivo**: encontrar um meio-termo que seja computacionalmente leve, mas que ainda consiga estimar os coeficientes de dependência do passado com precisão.

### O Condicionamento (A Solução)

A solução do CLS é simples: **desista de prever o começo**. Em vez de tentar modelar toda a série desde um passado infinito, nós *condicionamos* a nossa análise às primeiras observações. Tratamos os primeiros "p" valores (onde "p" é o número de defasagens) não como variáveis aleatórias que precisam ser explicadas, mas como **fatos fixos e dados**. O CLS ajusta a curva apenas para os pontos **após esses valores iniciais**.

> Ou seja, a regressão é condicionada aos primeiros p valores. Ignoramos a dependência deles de dados ainda mais antigos.

**Objetivo**: simplificar a função a ser minimizada, focando apenas nos erros que podem ser calculados a partir das informações já observadas no passado imediato (a esperança condicional).

## COMO FUNCIONA

O algoritmo `busca encontrar os coeficientes minimizando a soma dos quadrados dos erros, mas apenas para os valores onde a previsão pode ser condicionada ao passado conhecido`.

- Definimos a quantidade de defasagens (lags) que o modelo possui (ex: depende do dia anterior, então $p=1$)
- Ignoramos o erro dessa primeira observação (ou a fixamos com um valor arbitrário para os erros iniciais)
   - Geralmente definimos como zero, igual ao primeiro valor ou a média dos primeiros p valores
- A partir de $t = p+1$, calculamos o erro como a diferença entre o valor real e o valor esperado
- Minimizamos a soma desses erros ao quadrado

> Ou seja, `o "Condicional" no nome significa que estamos otimizando os parâmetros sob a CONDIÇÃO de que os valores iniciais já aconteceram e são conhecidos`.

## MATEMÁTICA E PROVA

Imagine um modelo Autoregressivo de ordem 1, o AR(1), onde o valor de hoje ($Y_t$) é um coeficiente ($\phi$) vezes o valor de ontem ($Y_{t-1}$) mais um erro aleatório ($e_t$).

$$Y_t = \phi Y_{t-1} + e_t$$

No OLS tradicional, tentaríamos minimizar $E^T E$ para todos os instantes de t=1$até T. Mas em t=1 precisaríamos de $Y_0$ que não temos.

### A Função Objetivo Condicional

A esperança (valor esperado) de $Y_t$ é o valor da nossa previsão que é condicionada à informação disponível no instante anterior (denotada por $F_{t-1}$).

$$E(Y_t | F_{t-1}) = \phi Y_{t-1}$$

O erro condicional é a diferença entre o valor observado e esse valor esperado:

$$e_t = Y_t - E(Y_t | F_{t-1}) = Y_t - \phi Y_{t-1}$$

A função objetivo que o Mínimo Quadrado Condicional quer minimizar (Soma dos Quadrados Condicionais - $S_c$) é o somatório desses erros ao quadrado, **começando do instante $t=2$**:

$$S_c(\phi) = \sum_{t=2}^{T} (Y_t - \phi Y_{t-1})^2$$

Aonde:

- Y é o dado real
- $\phi$ é o coeficiente ligado a cada momento da nossa janela (chamado de A nos outros mínimos)

Como nesse exemplo a janela tem tamanho 1 só temos 1 $\phi$, mas caso nossa janela tenha tamanho k teremos de $\phi_1$ até $\phi_k$. O vetor de coeficientes A que queremos encontrar em todo método de mínimos quadrados são esses $\phi$. Muda-se os nomes, mas é a mesma coisa.

$A = [\phi_1, \phi_2, ... \phi_k]$

### Derivada para encontrar o mínimo

Para encontrar o coeficiente $\phi$ que minimiza essa soma, fazemos a derivada de $S_c$ em relação a $\phi$ e igualamos a zero:

$$\frac{\partial S_c}{\partial \phi} = -2 \sum_{t=2}^{T} Y_{t-1} (Y_t - \phi Y_{t-1}) = 0$$

Dividindo por -2 e separando a soma:

$$\sum_{t=2}^{T} Y_{t-1} Y_t - \phi \sum_{t=2}^{T} Y_{t-1}^2 = 0$$

Isolando o coeficiente $\phi$, chegamos na fórmula do estimador CLS para o AR(1):

$$\phi = \frac{\sum_{t=2}^{T} Y_{t-1} Y_t}{\sum_{t=2}^{T} Y_{t-1}^2}$$

Se você reparar bem, **isso é matematicamente idêntico à fórmula do OLS**, mas com o vetor de dados (X) "cortado". 

> Em modelos apenas Autoregressivos (AR), o CLS é literalmente um OLS onde a variável dependente é $Y_t$ e a variável independente é $Y_{t-1}$, removendo a primeira linha dos dados.

No entanto, para modelos de Médias Móveis (MA), onde a equação depende de erros passados ($e_{t-1}$), a derivada não pode ser resolvida de forma direta assim, exigindo métodos numéricos iterativos (como Newton-Raphson) para encontrar o mínimo, já que o erro de hoje depende do erro de ontem estimado.

## PREMISSAS, VANTAGENS E DESVANTAGENS

### Premissas

- **Estacionariedade**: A série temporal não pode ter tendências explosivas (a média e a variância devem ser constantes no tempo).
- **Autocorrelação**: Os dados de hoje devem depender dos dados dos dias anteriores.
- Os erros ($e_t$) devem ser "ruído branco": independentes, com média zero e variância constante.

### Vantagens
- **Simplicidade Computacional**: É infinitamente mais rápido e fácil de calcular do que a Máxima Verossimilhança Exata.
- **Robustez**: Em grandes amostras, os resultados do CLS convergem assintoticamente para os resultados da Máxima Verossimilhança. A perda de informação por ignorar os primeiros dados é irrelevante se você tem centenas de pontos.
- **Fácil implementação**: Para modelos puramente autorregressivos, pode ser feito com as mesmas funções de álgebra linear do OLS comum.

### Desvantagens
- **Ruim para amostras pequenas**: Se a sua série de dados for muito curta (ex: 20 períodos), jogar fora o primeiro dado ou assumir que o erro inicial é zero causa um viés grande na estimativa.
- Não é o estimador mais eficiente possível para modelos com Médias Móveis (MA) se a raiz do polinômio estiver perto de 1 (não invertível).

## DIFERENÇAS PARA O MÍNIMOS QUADRADOS ORDINÁRIOS (OLS)

| Característica | OLS (Ordinários) | CLS (Condicionais) |
| :--- | :--- | :--- |
| **Foco principal** | Relações espaciais (X explica Y no mesmo instante). | Relações temporais (O passado explica o presente). |
| **Premissa de Independência** | Assume que cada linha de dados é independente das outras. | **Abraça a dependência**. Assume que a linha atual depende das linhas anteriores. |
| **Uso dos dados** | Usa 100% da matriz de dados. | "Descarta" ou fixa os primeiros $p$ dados para conseguir calcular a inércia temporal. |
| **Solução Matemática** | Solução exata via matrizes sempre ($A = (X^TX)^{-1} X^TY$). | Exata para modelos AR e iterativa (via software) para modelos com Médias Móveis (MA). |

## PASSO-A-PASSO

Vamos supor que você queira executar um CLS na prática para um modelo AR(2) — onde hoje depende de ontem e anteontem:

1. **Defina a ordem do modelo (p)**: Vamos usar p=2.

2. **Organize os dados**: Pegue sua série temporal $Y = [Y_1, Y_2, Y_3, ..., Y_T]$.

3. **Crie a Matriz de Defasagens (Lags)**:

- Crie uma coluna para $Y_{t-1}$ empurrando os dados um dia pra frente.
- Crie uma coluna para $Y_{t-2}$ empurrando os dados dois dias pra frente.

4. **Corte o início da amostra**:

- Para que todas as linhas tenham dados válidos (sem "NaN" ou valores vazios), exclua as duas primeiras linhas do seu dataset. Sua análise começará de t=3.

5. **Calcule a regressão**:

- Agora basta aplicar a fórmula clássica matricial sobre esses dados cortados: $A = (X^TX)^{-1} X^TY$, onde Y é a série de t=3 até T, e X é a matriz contendo os p valores anteriores de Y.

6. **Se houver termo de Média Móvel - MA (OPCIONAL)**:

- Se o modelo for um ARMA, o passo 5 não pode ser resolvido com uma equação simples. Você precisará definir os erros iniciais ($e_1$ e $e_2$). Geralmente 0, mas uma outra opção mais complexa é calcular os erros iterativamente pela série toda, e usar um algoritmo de otimização (como `scipy.optimize` no Python) para ir ajustando os chutes até a soma dos quadrados ser a menor possível.

### Exemplo

Para p=2 e uma amostra com 5 dados (T1, T2, T3, T4 e T5) teremos os seguintes X e Y.

$X = \begin{bmatrix}
t_1 & t_2 \
t_2 & t_3  \
t_3 & t_4  
\end{bmatrix}$

$Y = [t_3, t_4, t_5]$

