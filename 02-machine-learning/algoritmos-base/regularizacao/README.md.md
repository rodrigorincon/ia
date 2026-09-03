# REGULARIZAÇÃO DE MODELOS

A regularização é uma técnica para **evitar overfitting e tratar multicolineariedade**. Ele faz isso adicionando uma **penalidade** à Função de Custo.

Para lembrar, em machine learning queremos encontrar os parâmetros (pesos) que minimizem o erro. A Função de Custo mede quão ruim o modelo está se saindo, calculando a diferença entre a previsão e o valor real. Para evitar o overfitting a regularização altera a Função de Custo, adicionando uma **penalidade** à equação original. 

> **Função de Custo Final = Função de Custo Original (ex: MSE) + Penalidade de Regularização**

Além disso a regularização também remedia problemas de otimização, fazendo o gradiente dar saltos para sair de mínimos locais e platôs e explorar uma área maior, resolvendo 2 problemas de uma vez.

**Observação**: `Ao mudar a função de custo mudamos também sua derivada` (que é o que realmente importa).

## Como Evitar Overfitting

A regularização não detecta overfitting. Ao invés disso age diretamente para que ele nem venha a acontecer, matando o mal pela raíz.

Ela faz isso punindo pesos muito altos e forçando os pesos a valores menores. Pesos menores e menos variantes indica maior simplicidade no modelo.

## Constante Lambda

Todas as soluções de regularização usam uma constante lambda ($\lambda$). O **lambda controla a intensidade da penalização**. Quanto maior, mais penaliza pesos grandes e mais simplifica (puxando os pesos para baixo). 

Um lambda muito grande pode tornar o modelo excessivamente restrito e com desempenho ruim por simplificar demais. Por outro lado um lambda muito baixo (seu menor valor é 0) não muda quase nada na função original. 

Encontrar o melhor valor para lambda (nem alto nem baixo demais) envolve tentativa e erro. Geralmente é passado uma lista de valores a serem testados e o que der melhor resultado é escolhido. Isso significa ter de rodar o modelo N vezes a mais só para definir essa variável.

Lambda é sempre maior que 0 e quando se testa vários valores costuma-se que cada uma esteja em uma escala diferente (0.001, 0.01, 0.1, 1, 10, 100...). Assim não perde tempo testando valores próximos e o efeito será bem diferente entre cada um. A faixa de valores que você vai usar **depende muito da magnitude dos seus dados**.

## Ridge (L2)

A regularização Ridge adiciona uma penalidade baseada no **quadrado** da magnitude dos pesos/coeficientes. O objetivo é manter todos os pesos/coeficientes pequenos, mas raramente zerá-los.

$$F_{Ridge} = F_{original} + \lambda \sum W_{i}^2$$

E com isso alterar a função de custo original, usando essa versão no lugar da verdadeira.

Porém repare que com Ridge nenhum peso nunca vai a zero. Ele **DIMINUI a influência dos dados** (diminuindo o peso), mas nunca os remove por completo (zerar o peso).

### Ridge no Gradiente Descendente

A função do Gradiente Descendente é $W_{novo} = W_{atual} - \alpha * \frac{\partial fnCusto}{\partial W}$. 

Com o Ridge a derivada da função de custo muda. Como a função de custo recebeu uma soma que é **constante * somatório dos pesos ao quadrado**, a derivada de $\lambda W^2$, que é $2\lambda W$.

$W_{novo} = W_{atual} - \alpha * (\frac{\delta{F}}{\delta W} + 2\lambda W_{atual})$

Isso significa que, a cada iteração, o peso é matematicamente "encolhido" em direção a zero antes mesmo do gradiente do erro ser aplicado. Isso pois o peso subtrai $\alpha 2 \lambda W$ a cada iteração.

### Ridge no Mínimos Quadrados Ordinários (OLS)

Quando aplicamos o Ridge nos mínimos quadrados adicionamos a penalidade diretamente à matriz inversa. A matriz X ao quadrado invertida é a nossa função de custo, então aplicamos o lambda no quadrado da matriz X antes de inverter tudo. A nova equação se torna:

$$W = (X^T X + \lambda I)^{-1} X^T Y$$

Aonde I é uma matriz identidade para fazermos a soma do lambda com a matriz.

## Lasso (L1)

A regularização Lasso penaliza os pesos com base no seu **valor absoluto**. Diferente do Ridge ela pode reduzir coeficientes de variáveis irrelevantes a exatamente zero, funcionando como um **mecanismo automático de seleção** de features (variáveis).

Ele **REMOVE variáveis** (zerando seu peso) menos importantes, o que faz dele um filtro do que realmente é importante e o que não é. Se uma variável tinha pouco peso comparado as outras ela acaba sendo cortada fora. Isso acontece porque ele não encolhe proporcionalmente o peso, ao invés disso empurra o peso com uma força constante em direção a zero, o que força muitos coeficientes a desaparecerem completamente ao longo das épocas de treinamento.

$$F_{Lasso} = F_{original} + \lambda \sum |W_{i}|$$

### Lasso no Gradiente Descendente

A derivada do valor absoluto |W| é a função sinal: sign(W) (que vale +1 se W for positivo, e -1 se for negativo). Inserindo isso na regra de atualização do gradiente:

$$W_{novo} = W_{atual} - \alpha * (\frac{\delta{F}}{\delta W} \pm \lambda)$$

Com isso ele diminui ($\alpha * \lambda$) dos pesos em toda iteração até acabar ou chegar a zero.

### Lasso nos Mínimos Quadrados Ordinários (OLS)

Como a penalidade de Lasso (valor absoluto) não possui uma derivada suave e contínua em W = 0 **não existe uma solução analítica fechada** na forma matricial. Por isso não podemos usar Lasso nos mínimos quadrados.

## Elastic Net

O Elastic Net combina as penalidades L1 e L2. Ele tenta capturar o melhor dos dois mundos: a seleção de variáveis do Lasso e a estabilidade e encolhimento suave do Ridge.

$$F{ElasticNet} = F_{original} + \lambda_1 \sum |W_i| + \lambda_2 \sum W_i^2$$

No Gradiente Descendente, as duas derivadas são combinadas durante a atualização dos pesos, forçando coeficientes irrelevantes a zero ao mesmo tempo em que controla a magnitude das variáveis correlacionadas que sobrevivem.
