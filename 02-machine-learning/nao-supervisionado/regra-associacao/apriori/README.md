# APRIORI

É o algoritmo mais comum para regra de associação. É amplamente usado para análise de carrinho de compras (Market Basket). Esse algoritmo encontra quais combinações de dados/informações são mais encontrados juntos. Ele mede se um certo dado (valor em uma determinada variável) é mais comum quando um outro dado está presente e se o aumento em um deles provoca aumento no outro. 

No exemplo do carrinho de compras isso significa ver quais grupos de produtos são mais vendidos juntos do que sozinho. Isso ajuda a encontrar pares de venda não óbvios (ex: fralda se cerveja) e ajudar o mercado a vender mais fazendo promoções deles juntos ou colocando-os próximos. Também comum para fazer venda casada. Posso encontrar tanto pares de produtos como trios ou mais produtos.

> **Calcula quantas vezes um dado aparece sozinho e quantas vezes aparece com cada outro dado**. 

Monta diversas tabelas, cada uma com uma quantidade de produtos combinados. **A quantidade de produtos na tabela é dada por K**. Assim teremos uma tabela com k=1 produtos (só a contagem de quantas vezes aquele produto aparece), outra com k=2 (quantas vezes 2 produtos aparecem juntos) e assim por diante.

O algoritmo também possui um suporte mínimo, também chamado **valor de corte**. Esse valor de corte diz o mínimo de vezes que um produto deve aparecer para não ser descartado da avaliação. Isso se deve pois como o algoritmo compara todos com todos, tem uma complexidade muito alta $O(2^n)$. Para não rodar infinitamente ele faz uma nota de corte, aonde produtos pouco vendidos são desconsiderados, pois se são pouco vendidos não faz sentido gastar tempo e processamento analisando eles. O valor mínimo para sua nota de corte depende do tamanho da sua massa de dados (quantidade de vendas).

OBS: **O valor de corte é fixo para todas as tabelas**.

### MÉTRICAS

Tem 3 tipos de métrica:

- Suporte: conta todos os casos em q A e B aparecem juntos (A com B = B com A)
- Confiança: AB/A, porcentagem de casos que A e B aparecem juntos dividido pelo total de casos A (aqui A com B é diferente de B com A)
- Lift: o quanto a frequência de B aumenta com a ocorrência de A

## PREMISSAS

- Dados discretos ou categóricos (**NÃO funciona com dados contínuos**)
- Independência de tempo e ordem (os dados e colunas devem ser independentes e descorrelacionados)
  - Se A aconteceu ou foi colocado na cesta antes ou depois de B é irrelevante
  - Uma coluna ou linha não pode causar a outra

## QUANDO USAR 

- Análise de compras
- Recomendação Simples (venda casada, outros produtos que podem ser interessantes, próximo filme a assistir, próximo post a ver)
- Diagnósticos Médicos ou Sintomas (mapeia quão comum sintomas aparecem juntos e/ou sintomas com doenças)
- Quando precisa de alta interpretabilidade (precisa entender o que está acontecendo)
- Bases de dados pequenas

## QUANDO NÃO USAR

- Bases de dados imensas (usar FP-Growth nesse caso)
- Análise de texto (comparar todas as palavras do texto entre si é incabível)
- Dados contínuos
- Quando a ordem dos eventos importa (usar GSP nesse caso)
- Velocidade de resposta for importante

## Passo 1: Definir conjuntos mais vendidos juntos (Suporte)

#### 1.1: porcentagens de venda de cada produto

Divide quantas vendas um produto aparece pelo total de vendas. Essa será nossa **tabela com k=1**.

$S(prod) = N_{prod} / N$

Esse valor de 1 ou conjunto de produtos vendidos dividido pelo total de vendas é chamado de **suporte**. Ele indica a frequência que um produto ou conjunto de produtos aparecem nas compras. Indica a `popularidade da combinação`.

#### 1.2: rodar valor de corte

Verifico quais tem valor menor que o valor de corte. Esses eu removo e não passarei para o próximo loop. Apenas **valores iguais ou maiores continuam**.

#### 1.3: repetir o loop incrementando k

Dentre os produtos restantes, faço todas as combinações entre eles e vejo em quantas vendas eles aparecem e divido pelo total de vendas. O total de vendas é sempre fixo em todos os loops.

$S(prod1, prod2) = N(prod1 ∩ prod2) / N$

Aplica-se a nota de corte novamente e segue para o próximo loop incrementando k.

A partir de k=3 é interessante ver que ao criar uma nova linha estamos fazendo uma união de 2 linhas da tabela anterior que possuem k-2 produto em comum. Isso diminui a quantidade de combinações, evitando analisar combinações inexistentes.

Exemplo: quando k=3, tenho na tabela k=2 os pares "tomate e cerveja" e "arroz e leite", porém nenhum par entre tomate-arroz, tomate-leite, cerveja-arroz ou cerveja-leite. Assim não faz sentido criar um grupo "tomate, cerveja e arroz" nem "tomate, cerveja e leite", pois as linhas tem que ter ao menos k-2 (no caso, 1) produto em comum.

Exemplo2: quando k=4 as linhas da tabela anterior tem que ter ao menos 2 produtos em comum. Se eu tenho "tomate, cerveja, arroz" e "tomate, cerveja, leite", então devo criar na tabela k=4 uma união dessas 2 linhas "tomate, cerveja, arroz, leite".

#### 1.4: critério de parada

Devo continuar criando tabelas até que não haja mais novas combinações entre conjuntos da tabela anterior. Se a **tabela final estiver vazia, termino o loop**.

## Passo 2: Cálculo da Confiança nas combinações

Mede a probabilidade de o item A ser comprado quando o item B já está na cesta. Usamos as combinações sobreviventes e **todas as tabelas** do passo anterior (não apenas da última). Diz quão confiante estou que um produto A será adicionado à cesta quando B está presente, por isso é uma **probabilidade**.

Importante perceber que P(A|B) é diferente de P(B|A). Ou seja, tenho de calcular a confiança de "A,B" e de "B,A".

A confiança de A ser adicionado dado que B está na cesta é calculado assim

$C(A|B) = \frac{S(A,B)}{S(A)}$

E o contrário seria

$C(B|A) = \frac{S(A,B)}{S(B)}$

OBS: `repare que S(A,B) = S(B,A), mas isso não vale para a confiança. C(A|B) != C(B|A)`.

Quando tenho mais produtos fica assim, para um caso que tenho a combinação A,B,C.

$C(a | b,c) = \frac{S(a,b,c)}{S(a)}$

$C(b | a,c) = \frac{S(a,b,c)}{S(b)}$

$C(c | a,b) = \frac{S(a,b,c)}{S(c)}$

$C(a,b | c) = \frac{S(a,b,c)}{S(a,b)}$

$C(a,c | b) = \frac{S(a,b,c)}{S(a,c)}$

$C(b,c | a) = \frac{S(a,b,c)}{S(b,c)}$

Repare que a quantidade de cálculos dispara nessa etapa. É aqui que o algoritmo fica pesado.

Uma **nova nota de corte** é definida, maior que a anterior, para eliminar as combinações fracas.

#### 2.1: Calcula confiança para cada tabela k > 1

A partir de k=2, executa um loop calculando a probabilidade de cada combinação de cada linha dessa tabela. Cada combinação (linha) pode ter diversas combinações (cálculos). Essa quantidade é feita pela binomial.

#### 2.2 Faz análise combinatória de cada linha da tabela

Calcula a probabilidade de cada análise combinatória da linha. Ao final, para cada linha da tabela, teremos diversas confianças, mostrando todas as combinações e a probabilidade de cada uma dada a ordem de compra. Esse processo é feito da segunda até a última tabela.

#### 2.3 Rodar valor de corte

Todas as confianças abaixo do valor de corte são eliminadas. Apenas as confianças com valor igual ou maior permanecem. O valor de corte é o mesmo para todas as tabelas k.

## Passo 3: Cálculo da força da associação (lift)

Semelhante a confiança, ele nos dá a força da confiança calculada. Ou seja, a força dessa proabilidade. O **lift é uma medida mais forte**, pois leva mais coisas em consideração. Ele não é uma probabilidade, podendo ser maior que 1.

O lift é nossa métrica final, usada na tomada de decisão. Quanto maior, mais forte essa relação e mais provável a venda. `Só devemos considerar lifts acima de 1`.

Um lift > 1 mostra que o item **A tem mais probabilidade de ser comprado com B do que sozinho**.

Podemos entender o lift como o tamanho do efeito e a confiança como a probabilidade dos produtos serem vendidos juntos.

Para toda combinação calculada no passo 2, fazemos o cálculo do lift. É um grande repeteco do passo anterior, só que com a fórmula um pouco diferente.

$L(a|b) = \frac{S(a,b)}{S(a)S(b)}$

Quando se tem mais variáveis

$L(a|b,c) = \frac{S(a,b,c)}{S(a)S(b,c)}$

$L(a,b | c) = \frac{S(a,b,c)}{S(a,b)S(c)}$

Ao final, ordenamos as combinações pelo lift para vermos em ordem quais combinações tem maior relevância.

#### Por que muda tanto

Caso haja uma discrepância de venda muito grande entre os produtos, a confiança pode ser muito alta (eles são muito vendido juntos), porém com lift baixo (com pouca relevância). Isso porque um dos produtos é muito pouco vendido e o outro é muito vendido.

Exemplo: sabão em pó é muito vendido, máquina de lavar roupa é muito pouco vendido. Porém quando alguém compra máquina de lavar quase sempre compra sabão em pó junto. Assim a confiança é alta (alta probabilidade de serem vendidos juntos) porém com pouca relevância (não vale esquentar a cabeça com isso).

S(sabão) = 80, S(máquina) = 14, S(sabão, máquina) = 10

Repare que máquina foi vendida 14 vezes, sendo 10 delas acompanhado de sabão. Já sabão vendo muito bem com ou sem máquina.

C(máquina | sabão) = 0,7

L(máquina | sabão) = 0,008

# REFERÊNCIAS

[Um ótimo vídeo explicando o algoritmo é esse](https://www.youtube.com/watch?v=YGEYty0xYc0).
