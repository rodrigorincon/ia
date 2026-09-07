# MULTIPLICADORES DE LAGRANGE

Os Multiplicadores de Lagrange são uma das ferramentas mais elegantes e essenciais do cálculo diferencial multivariável. Eles pertencem totalmente ao universo da otimização matemática, sendo usados extensivamente na física, economia e machine learning.

O que ele faz é `encontrar os pontos de máximo e mínimo de uma função sujeita a restrições`. Ou seja, o método define os pontos ótimos (mais altos ou mais baixos) **que satisfazem uma condição específica**. O sistema olha para a equação, recorta os espaços permitidos pela restrição e define o melhor ponto dentro desse espaço.

## Restrição/Regra

Em otimização, o melhor resultado nem sempre é absoluto, muitas vezes ele é relativo ao que você pode fazer (ex: ponto de partida). A restrição é justamente a fronteira ou o limite do seu problema. Significa encontrar a melhor solução **dado um orçamento, material ou limite físico**. É exatamente o que essa parte do cálculo faz: mede onde a curva da sua função objetivo se alinha perfeitamente com a curva da sua restrição.

## Diferenças de igualar a derivada a zero

Igualar a derivada a zero calcula o pico absoluto (ou vale) de uma função. Nesse cenário não existe regras ou restrições. O Multiplicador de Lagrange é para quando há um muro: **a partir de um limite imposto, qual é o ponto máximo ou mínimo que consigo alcançar?**

- **Derivada igual a zero**: função objetivo = ponto ótimo global/local
- **Multiplicador de Lagrange**: função objetivo + restrição = ponto ótimo local

Assim, ao invés de buscar a inclinação zero absoluta como na derivada, o método de Lagrange cria uma nova função e busca o ponto onde as curvas de nível da sua função e da sua restrição são paralelas (tangentes).

> OBS: É possível mostrar que igualar a derivada a zero é só um caso especial e simplificado da otimização de Lagrange. Partindo da premissa que a restrição não é "ativa" (ou seja, o orçamento é infinito ou a restrição não afeta o resultado), o valor do multiplicador vira zero e a equação matemática volta a ser a exata mesma equação da derivada simples.

### Explicação Visual

Os dois têm o mesmo objetivo inicial (encontrar máximos e mínimos), mas o fazem em cenários totalmente diferentes. Enquanto igualar a derivada a zero (otimização irrestrita) foca em encontrar o topo da montanha, os Multiplicadores de Lagrange mudam a pergunta: eles buscam o ponto mais alto da montanha **pelo qual uma estrada específica (sua restrição) passa**.

### Exemplo Prático

Você pode querer a proporção ótima das matérias primas para uma liga metálica, porém tem um limite de orçamento que pode tornar proibitivo a opção perfeita. Pode encontrar os tamanhos que dão a maior área possível porém não tem dinheiro para cercar tudo. Ou se essa área for para a base de um prédio mas não tem dinheiro para isso tudo de cimento.

Um exemplo matemático é querer encontrar o maior valor da equação para X > 0 ou para 30 < X < 50. 

## Onde Usar

Os Multiplicadores de Lagrange são utilizados praticamente em **todos os lugares onde os recursos são finitos** ou há **leis físicas invioláveis**. Também são usados em diversos algoritmos modernos de **aprendizado de máquina**.

- **Economia**: Maximização de utilidade sujeita a um orçamento.
- **Machine Learning**: Máquinas de Vetores de Suporte (SVM), onde maximizamos a margem de separação sujeita a classificar os dados corretamente.
- **Física**: Princípio da mínima ação para sistemas restritos (mecânica analítica).
- **Engenharia**: Alocação de recursos (ex: maximizar a resistência de uma viga sujeita a um limite de peso).

## PREMISSAS

- **Funções Diferenciáveis**: Diferente de métodos heurísticos (que testam valores cegamente), Lagrange exige que tanto a função objetivo quanto a função de restrição sejam contínuas e tenham derivadas (sejam suaves).
- **Qualificação da Restrição**: O gradiente (as derivadas) da função de restrição **não pode ser zero no ponto ótimo**.
- **Igualdade**: O método clássico de Lagrange só funciona para restrições de igualdade ($g(x,y) = c$). Para restrições de desigualdade (ex: gastar até R$ 100, mas não obrigatoriamente tudo), tem de usar uma expansão do método (Condições KKT).

## MATEMÁTICA

Se você quer maximizar uma função $f(x, y)$ enquanto está preso a uma restrição $g(x, y) = c$, `o ponto máximo ocorre exatamente quando os gradientes (os vetores que apontam para onde a função cresce mais rápido) de ambas as funções são paralelos`. A equação fundamental é:

$$\nabla f(x,y) = \lambda \nabla g(x,y)$$

Onde $\lambda$ (Lambda) é o Multiplicador de Lagrange. Ele é uma constante que ajusta o tamanho dos vetores para que eles se igualem.

Exemplo: Se você quer maximizar a área de um retângulo ($A = x * y$) com um perímetro fixo ($2x + 2y = 100$), a função objetivo é a Área e a restrição é o Perímetro.

### O "Truque" da Função Lagrangiana (L)

Lidar com a restrição isoladamente é complicado e muitas vezes impossível de substituir numa equação. Para um computador ou um humano resolver o problema analiticamente, trabalhar com restrições soltas é muito trabalhoso e gera um inferno algébrico.

Para resolver isso existe a **Função Lagrangiana ($L$)**. A regra mágica do multiplicador é que ele embute a restrição dentro da função original. Chamamos isso de relaxamento lagrangiano.

$$L(x, y, \lambda) = f(x, y) - \lambda (g(x, y) - c)$$

Com isso `trocamos um problema de otimização COM restrição por um problema de otimização SEM restrição`. Após isso derivamos a Função Lagrangiana em relação a todas as variáveis (incluindo o $\lambda$) e igualamos a zero para encontrar os pontos críticos. Queremos derivar tudo porque queremos o ponto (valor) onde as curvas se tangenciam.

> `O pulo do gato`: Quando derivamos a Função Lagrangiana em relação a $\lambda$ e igualamos a zero, o que sobra é exatamente a equação da nossa restrição ($g(x, y) - c = 0$). Trocamos um problema de geometria pesada por derivadas simples.

### Atenção com a derivada

Ao usarmos a Função Lagrangiana para estimar 2 ou mais variáveis e o $\lambda$, temos de ter atenção com as derivadas parciais. Primeiramente a gente deriva a função $L$ em relação a $x$, considerando os outros constantes. Depois derivamos em relação a $y$, com os demais constantes. E finalmente em relação a $\lambda$.

Perceba que ao fazer isso a gente deriva a função em relação a variáveis diferentes, com isso a **equação retornada pela derivada é diferente para cada parâmetro**, formando um sistema linear ou não-linear.

> Não cometa o erro de esquecer de derivar em relação ao próprio $\lambda$!

---

**Exemplo**: Função $f(x,y) = xy$ e a restrição é $x + y = 100$. 

Função de Lagrange: $L = xy - \lambda(x + y - 100)$.

Derivada para $x$:

$\frac{\delta L}{\delta x} = y - \lambda = 0$

Derivada para $y$:

$\frac{\delta L}{\delta y} = x - \lambda = 0$

Derivada para $\lambda$:

$\frac{\delta L}{\delta \lambda} = -(x + y - 100) = 0$

## PASSO-A-PASSO (COMO EXECUTAR)

A receita de bolo dos Multiplicadores de Lagrange é sempre a mesma:

1. **Defina a Função Objetivo**: Identifique quem é a função objetivo $f(x,y)$.
2. **Defina a Função Restrição**: Identifique quem é a função da regra $g(x,y) = c$
3. **Monte a Equação (Lagrangiano)**: Escreva $L(x, y, \lambda) = f(x, y) - \lambda(g(x, y) - c)$.
4. **Calcule as Derivadas**: Faça as derivadas parciais de $L$ para todas as variáveis ($x$, $y$) e para $\lambda$.
5. **Encontre o Máximo/Mínimo**: Iguale todas essas derivadas parciais a zero, criando um sistema de equações.

Isso te dará as coordenadas $(x, y)$ exatas do seu ponto ótimo e o valor de $\lambda$.

## Condições Karush-Kuhn-Tucker (KKT)

As condições KKT são uma generalização dos Multiplicadores de Lagrange para cenários aonde a função restrição não é igual (=), podendo ser um "maior que" ou "menor que" (< ou >). 

Ex: gastar $\le$ 100 em vez de obrigatoriamente gastar $=$ 100. 

Elas nada mais são que o método de Lagrange com multiplicadores adicionais e regras de folga. Portanto, na prática, as condições KKT e os multiplicadores de Lagrange, mesmo sendo para escopos diferentes, formam a mesma base teórica da otimização não-linear.

A lógica é que o $\lambda$ para uma desigualdade deve ser maior ou igual a zero (indicando se a restrição é ativa ou inativa):

$\lambda \ge 0$ e $\lambda(g(x) - c) = 0$

Onde:
- Se a restrição não afeta o máximo, $\lambda = 0$ (otimização irrestrita).
- Se a restrição impede você de subir mais a montanha, $\lambda > 0$ (otimização de Lagrange original).
