# MÍNIMOS QUADRADOS GENERALIZADOS (GLS)

É a versão definitiva e mais completa das variações do algoritmo de Mínimos Quadrados Ordinários (OLS). Ele é usado para estimar os coeficientes de uma regressão quando os dados sofrem de **heterocedasticidade** (variâncias diferentes) E **autocorrelação** (as variáveis são correlacionados entre si). É a evolução natural dos Mínimos Quadrados Ponderados (WLS).

Os mínimos quadrados ordinários tratam todo ponto como independente e com a mesma variância. Os ponderados (WLS) resolvem a variância diferente, mas ainda assumem que um ponto não tem nada a ver com o outro. Os mínimos quadrados generalizados resolvem o pacote completo: lidam com pontos de diferentes confiabilidades e que influenciam uns aos outros.

## O Problema e a Solução

### Autocorrelação (e Heterocedasticidade)

Enquanto a heterocedasticidade é a variância inconstante do erro, a **autocorrelação** acontece quando o erro de uma observação está ligado ao erro de outra. Isso é muito comum em séries temporais (o preço de uma ação hoje depende muito do preço de ontem) ou dados espaciais. A relação entre os erros acontece porque as variáveis são correlacionadas. A variável "gastos com sorvete" e "gastos com energia" podem estar relacionados entre si (ambos aumentam no calor).

Na regressão padrão, assumimos que os erros são totalmente independentes. Quando eles não são, o modelo se engana achando que tem mais informações "novas" do que realmente tem, deixando a estimativa dos coeficientes ineficiente e os testes de validade furados. 

A autocorrelação somada à heterocedasticidade é `O QUE` destrói completamente a validade do nosso modelo tradicional (OLS).

**Objetivo**: corrigir tanto a influência desigual de pontos com variâncias diferentes quanto a redundância de informações gerada pela correlação entre os pontos.

### A Matriz de Covariância (A Solução)

Para resolver isso, o GLS abandona a ideia de usar apenas "pesos" isolados para cada ponto e introduz a **Matriz de Covariância dos Erros** (normalmente chamada de $\Omega$ ou $V$). Essa matriz mapeia não apenas a variância individual de cada erro (na sua diagonal principal), mas também o quanto o erro de um ponto se move junto com o erro de outro ponto (nos outros espaços da matriz). A matriz de covariância invertida ($\Omega^{-1}$) é o `COMO` ele conserta o problema.

**Objetivo**: transformar os dados originais levando em conta essas relações e variâncias, filtrando o "ruído correlacionado" para que a reta possa ser ajustada de forma limpa.

## Importância da Matriz de Covariância ($\Omega$)

`A matriz de covariância atua como uma lente corretiva completa. Ela ajusta o peso dos erros (como no WLS) e desconta as informações repetidas causadas pela correlação entre os dados.`

No modelo tradicional, nós minimizamos a soma dos quadrados dos erros assumindo que eles não têm relação: $E^T * E$. No modelo generalizado, nós avaliamos o erro através do inverso da matriz de covariância ($\Omega^{-1}$). Se dois erros estão muito correlacionados, a matriz "pune" essa sobreposição, garantindo que o algoritmo não dê importância em dobro para a mesma tendência.

Soma dos Erros Generalizados = $E^T * \Omega^{-1} * E$

O objetivo do GLS é encontrar a reta que minimize esse erro transformado. Ou seja, `errar em pontos altamente confiáveis e independentes custa caro, enquanto errar em pontos barulhentos e altamente dependentes de outros custa mais barato para o algoritmo`.

## COMO FUNCIONA

O algoritmo `busca encontrar os coeficientes aonde a soma dos quadrados dos erros filtrados pela matriz de covariância é a menor possível`. O passo-a-passo lógico é uma extensão direta do modelo ponderado:

- Define-se a estrutura da matriz de covariância $\Omega$ para os erros das observações.
- Calcula-se a inversa dessa matriz ($\Omega^{-1}$), que servirá como nossa "matriz de pesos suprema".
- Executa-se o cálculo da equação derivada com a matriz de covariância invertida presente.

> Ou seja, `não multiplicamos apenas o erro por um peso isolado`. Nós multiplicamos os erros pela matriz completa de relações antes de minimizá-los. 

## PROVA (EM MATRIZES)

Fazer essas contas à mão com as covariâncias cruzadas é um pesadelo absurdo, por isso a demonstração do GLS é feita puramente através de matrizes de forma muito elegante.

Lembrando a nossa equação matricial do erro:

$$E = Y - X * A$$

### Adicionando a Matriz de Covariância ($\Omega^{-1}$)

No WLS, queríamos minimizar introduzindo uma matriz diagonal $W$. No GLS, nós introduzimos a inversa da matriz de covariância $\Omega^{-1}$. Enquanto $W$ era cheia de zeros fora da diagonal, $\Omega^{-1}$ pode ter valores em todos os campos, mapeando a correlação de todo mundo com todo mundo.

Nossa nova função a ser minimizada se torna a multiplicação do erro transposto, pela matriz de covariância invertida, pelo erro:

$F(A) = E^T * \Omega^{-1} * E$

Substituindo $E$ pela equação isolada do erro:

$F(A) = (Y - X * A)^T * \Omega^{-1} * (Y - X * A)$

### Derivada para encontrar o mínimo

Expandindo essa multiplicação e lembrando das propriedades onde, como a matriz de covariância (e sua inversa) é simétrica, $\Omega^{-1} = (\Omega^{-1})^T$:

$F(A) = Y^T \Omega^{-1} Y - 2A^T X^T \Omega^{-1} Y + A^T X^T \Omega^{-1} X A$

Até então temos a soma dos erros generalizados. **Para encontrar o menor valor fazemos a derivada em relação a A e igualamos a 0**, exatamente como no WLS.

$\frac{\partial{F}}{\partial{A}} = -2X^T \Omega^{-1} Y + 2X^T \Omega^{-1} X A = 0$

Isolando A temos:

$2X^T \Omega^{-1} X A = 2X^T \Omega^{-1} Y$

Dividindo os dois lados por 2, chegamos na base da equação:

$X^T \Omega^{-1} X A = X^T \Omega^{-1} Y$

Passando o termo do X para o outro lado invertido:

$$A = (X^T \Omega^{-1} X)^{-1} * X^T \Omega^{-1} Y$$

Com essa equação conseguimos calcular todos os coeficientes da regressão generalizada, isolando o ruído de variância e de correlação. Se trocarmos ômega por W temos exatamente a mesma equação dos mínimos ponderados.

### Em resumo

A beleza da álgebra linear é que as fórmulas são conceitualmente idênticas. O GLS é simplesmente o caso mais abrangente possível da regressão linear, e os outros são apenas simplificações dele.

Repare na evolução matemática:

> **Simples (OLS)**: $A = (X^T X)^{-1} * X^T Y$
> *(Assume matriz identidade: variâncias iguais, zero correlação)*
>
> **Ponderado (WLS)**: $A = (X^T W X)^{-1} * X^T W Y$
> *(Usa matriz diagonal $W$: variâncias diferentes, zero correlação)*
>
> **Generalizado (GLS)**: $A = (X^T \Omega^{-1} X)^{-1} * X^T \Omega^{-1} Y$
> *(Usa matriz completa $\Omega^{-1}$: variâncias diferentes, com autocorrelação)*

## Calculando a matriz $\Omega$

Assim como no WLS definíamos os pesos a partir da variância, surge a pergunta: `como definir a covariância dos erros se ainda não temos a reta para saber os erros?`

O processo prático mais comum para resolver isso é chamado de **FGLS** (Feasible Generalized Least Squares, ou Mínimos Quadrados Generalizados Factíveis):

- Fazemos uma regressão normal (OLS) "ingênua".
- Pegamos os resíduos (erros) dessa regressão.
- Usamos esses resíduos para estimar como os erros variam e se relacionam no tempo/espaço (calculamos a estrutura de $\Omega$).
- Com $\Omega$ pronta, invertemos a matriz e jogamos na fórmula do GLS para calcular a reta definitiva.

Dá mais trabalho, mas garante que os coeficientes encontrados ignorem as "armadilhas" de dados viciados e auto-correlacionados, entregando a melhor precisão matemática possível.
