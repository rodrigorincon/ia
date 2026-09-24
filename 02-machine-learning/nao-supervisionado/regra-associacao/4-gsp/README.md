# GSP (GENERALIZED SEQUENTIAL PATTERN)

Recebe esse nome pois generaliza a mineração de padrões para **sequências temporais e ordenadas**. Ele serve para **encontrar sequências de itens ou eventos frequentes ao longo do tempo** em bases de dados transacionais associadas a entidades (como clientes, usuários ou máquinas).

Enquanto algoritmos como Apriori, FP-Growth e ECLAT analisam apenas o que é comprado **junto em uma única transação** (sem noção de tempo), o GSP analisa o histórico de compras de uma mesma entidade **ao longo de múltiplas transações ordenadas no tempo**. Assim, se você compra A e depois de uma semana compra B, esse algoritmo descobre enquanto os demais não. Da mesma forma, ele consegue descobrir se um item ser colocado no carrinho induz o cliente a colocar outro também.

## Diferença Essencial para o Apriori

No Apriori, FP-Growth e Eclat a ordem não importa ({A, B} = {B, A}) e trabalham com conjuntos de itens. No GSP a ordem é crucial ({A, B} $\ne$ {B, A}) e trabalha com sequência de conjuntos de itens (lista de conjuntos ordenados no tempo).

> **Exemplo:**  
> * **Apriori:** Quem compra Pão também compra Manteiga no mesmo caixa.
> * **GSP:** Quem compra uma Câmera no mês 1, compra um Cartão de Memória no mês 2 e um Tripé no mês 3.

## Estrutura e Notação

O GSP utiliza uma notação formal específica para definir os eventos ordenados:

* **Item:** A menor unidade discreta de dado (ex: produto $A$, página $B$).
* **Evento / Elemento (Itemset):** Conjunto não ordenado de itens que ocorreram **no mesmo instante de tempo**. É representado por chaves {}.
* **Sequência:** Uma lista **ordenada no tempo** de eventos/elementos. É representada por parêntesis ().

**Exemplo de Notação**: S = ( \{A, B\}, \{C\}, \{D, E\} )

Isso significa que a entidade realizou três eventos sequenciais:
1. No primeiro momento, adquiriu os itens $A$ e $B$ juntos.
2. Em um segundo momento posterior, adquiriu o item $C$.
3. Em um terceiro momento posterior, adquiriu os itens $D$ e $E$ juntos.

## Suporte da Sequência

O suporte de uma sequência $S$ é o número (ou percentual) de entidades distintas cuja história de eventos contém $S$ como uma **subsequência**:

Suporte(S) = Contagem de Entidades contendo S

Suporte relativo(S) = $\frac{\text{Contagem de Entidades contendo } S}{N_{totalEntidades}}$

## Passo-a-Passo

O GSP opera em uma abordagem nível a nível, gerando candidatos de tamanho k a partir de sequências frequentes de tamanho k-1:

1. **Primeira Varredura (Contagem de 1-Itens):**
  - Varre o histórico de todas as entidades e conta em quantas entidades cada item individual aparece.
  - Filtra os itens com Suporte < min_sup.

2. **Geração de 1-Sequências Frequentes ($L_1$):**
  - Transforma cada item aprovado em uma sequência de comprimento 1: ({A}), ({B}), etc.

3. **Loop Principal (Geração de k-Sequências):**
  - **Passo de Junção:** Gera candidatos k-sequências ($C_k$) combinando pares de (k-1)-sequências frequentes de $L_{k-1}$.
    - Ou seja, junta sequências de tamanho 1 para formar sequêncis de tamanho 2. Depois sequências de tamanho 2 para formar sequêncis de tamanho 3 até o tamanho máximo K.
  - **Passo de Poda:** Remove qualquer candidato de $C_k$ que possua pelo menos uma subsequência de tamanho k-1 que **não** seja frequente em $L_{k-1}$.
  - **Varredura e Contagem:** Varre a base de dados temporal para calcular o suporte real dos candidatos sobreviventes em $C_k$.
  - **Filtragem:** Mantém apenas os candidatos com Suporte $\ge$ min_sup, formando o conjunto $L_k$.

4. **Condição de Parada:** O algoritmo encerra quando nenhum novo candidato frequente for gerado ($L_k$ = {}).

## Como Funciona a Geração de Candidatos e Poda

A fase de junção no GSP é mais complexa do que no Apriori porque um novo item pode ser adicionado de duas formas: **no mesmo evento** ou **em um novo evento separado**.

### Regra de Junção entre $S_1$ e $S_2$:
Duas sequências de tamanho k-1 ($S_1$ e $S_2$) podem se unir se a subsequência obtida ao **remover o primeiro item de $S_1$** for idêntica à subsequência obtida ao **remover o último item de $S_2$**. Ou seja, as 2 sequências tem de ser iguais exceto pelo primeiro item de S1 e o último de S2.

Ao realizar a união, o último item de $S_2$ é anexado a $S_1$:
1. **Como novo evento separado**, se ele estava em um evento separado em $S_2$.
2. **Dentro do último evento de $S_1$**, se ele fazia parte de um evento com múltiplos itens em $S_2$.

### Regra de Poda:

Uma k-sequência candidata é sumariamente descartada se **qualquer uma** de suas (k-1)-subsequências não estiver presente no conjunto $L_{k-1}$ de sequências frequentes do nível anterior.

## PREMISSAS

- **Entidade Identificável:** Os dados devem conter um ID claro de cliente/transação.
- **Marcação Temporal / Ordenação:** Cada transação da entidade deve possuir uma data, hora ou número de sequência relativo.
- **Dados Discretos:** Cada item deve ser categórico ou discreto.

## QUANDO USAR

- **Análise da Jornada do Cliente:** Entender os passos sequenciais que levam um cliente à conversão ou ao cancelamento.
- **Análise de Navegação Web (Clickstream):** Mapear as rotas de páginas navegadas pelos usuários antes de realizar uma compra.
- **Medicina e Saúde:** Identificar sequências de exames, tratamentos e evolução de sintomas em prontuários de pacientes.
- **Manutenção Preditiva Industrial:** Detectar sequências de pequenos alertas de sensores que precedem a quebra completa de um equipamento.
- **E-commerce / Sistemas de Recomendação:** Recomendar o "próximo produto lógico" com base no histórico recente do usuário.

## QUANDO NÃO USAR

- **Cesta de Compras sem Tempo:** Quando o objetivo é apenas saber o que é comprado junto no mesmo instante
- **Sequências de Texto Contínuo ou Genétca:** Para mineração de DNA ou linguagem natural, algoritmos específicos para cadeias de caracteres são incomparavelmente mais eficientes.
- **Bases Massivas sem Restrição de Tempo:** Sem definir limites como `maxgap` (tempo máximo entre transações), a geração de candidatos em bases gigantes pode sofrer com explosão combinatória.

## CONCEITOS AVANÇADOS: PARÂMETROS TEMPORAIS DO GSP

Para evitar sequências irrelevantes e controlar a explosão combinatória, o GSP permite configurar três parâmetros temporais fundamentais:

1. **`maxgap` (Intervalo Máximo):** O tempo máximo permitido entre dois eventos consecutivos da sequência.
  - Exemplo: Se maxgap = 30 dias, comprar um item 6 meses depois não conta como continuação da mesma sequência.

2. **`mingap` (Intervalo Mínimo):** O tempo mínimo necessário entre dois eventos para que sejam considerados separados.
  - Exemplo: Evita contar dois cliques acidentais seguidos no mesmo segundo como eventos sequenciais distintos.

3. **`window size` (ws- Janela de Agrupamento):** Define um intervalo de tempo dentro do qual compras realizadas em datas ligeiramente diferentes podem ser tratadas como pertencentes ao **mesmo evento**.
  - Exemplo: Se ws = 7 dias, compras feitas na segunda e na quarta-feira da mesma semana são tratadas conjuntamente como {Pão, Leite}.

## Exemplo

Considerando que temos N=3 transações e um suporte mínimo min_sup = 2 (66.6%).

### Histórico dos Clientes (Layout Temporal)

| Cliente | Transação 1 ($t_1$) | Transação 2 ($t_2$) | Transação 3 ($t_3$) | Sequência do Cliente |
| :---    | :---                | :---                | :---                | :--- |
| **C1**  | {A}                 | {B, C}              | {D}                 | ({A},{B, C},{D} ) |
| **C2**  | {A, B}              | {C}                 | {D}                 | ({A, B},{C},{D} ) |
| **C3**  | {A}                 | {B}                 | {E}                 | ({A},{B},{E} ) |

### Passo 1: Contagem de 1-Itens e Filtragem

Contamos em quantos clientes cada item aparece pelo menos uma vez:

* **A:** Presente em C1, C2, C3 $\rightarrow$ **Suporte = 3**
* **B:** Presente em C1, C2, C3 $\rightarrow$ **Suporte = 3**
* **C:** Presente em C1, C2 $\rightarrow$ **Suporte = 2**
* **D:** Presente em C1, C2 $\rightarrow$ **Suporte = 2**
* **E:** Presente em C3 $\rightarrow$ **Suporte = 1** (Infrequente: 1 < min_sup $\rightarrow$ **Descartado**)

### 1-Sequências Frequentes ($L_1$):

$L_1$ = { ({A}), ({B}), ({C}), ({D}) }

### Passo 2: Gerando 2-Sequências Candidatas ($C_2$)

Combinando os elementos de $L_1$ tanto em **eventos separados** quanto no **mesmo evento**:

- **Mesmo Evento:** ({A,B}), ({A,C}), ({A,D}), ({B,C}), ({B,D}), ({C,D})
- **Eventos Separados:** ({A},{A}), ({A},{B}), ({A},{C}), ({A},{D}), ({B},{A}), ({B},{B}), ({B},{C}), ({B}, {D}), ({C}, {A}), ({C}, {B}), ({C}, {C}), ({C}, {D}), ({D}, {A}), ({D}, {B}), ({D}, {C}), ({D}, {D}).

#### Contagem de Suporte para Candidatos Relevantes de $C_2$:

- **({A,B}):** Presente apenas em C2 ({A,B} no $t_1$) $\rightarrow$ **Suporte = 1** (Descartado)
- **({A},{B}):**
  - C1: {A} em $t_1$, {B, C} em $t_2 \rightarrow$ **Sim**
  - C2: {A, B} em $t_1$ (pode conter a ordem temporal se consideramos que o evento contém A e B) / em C2 temos {A} em $t_1$ e {C} em $t_2$. Mas analisando transações estritamente posteriores:
    - C1 tem {A} em $t_1$ e {B} em $t_2$.
    - C3 tem {A} em $t_1$ e {B} em $t_2$.
  - Suporte em C1 e C3 $\rightarrow$ **Suporte = 2** (Frequente)
- **({B}, {C}):**
  - C1: {B,C}$ no mesmo $t_2$ (não é posterior) — mas C1 tem {B} em $t_2$ e C no mesmo evento.
  - C2: {A,B} em $t_1$, {C} em $t_2$ $\rightarrow$ **Sim**
  - C3: Não tem C.
  - Suporte em C1 (se o mesmo evento contar como ocorrência) ou C2 $\rightarrow$ **Suporte = 2**
- **({A},{C}):**
  - C1: {A} em $t_1$, {C} em $t_2$ $\rightarrow$ **Sim**
  - C2: {A} em $t_1$, {C} em $t_2$ $\rightarrow$ **Sim**
  - Suporte em C1 e C2 $\rightarrow$ **Suporte = 2** (Frequente)
- **({C},{D}):**
  - C1: {C} em $t_2$, {D} em $t_3$ $\rightarrow$ **Sim**
  - C2: {C} em $t_2$, {D} em $t_3$ $\rightarrow$ **Sim**
  - Suporte em C1 e C2 $\rightarrow$ **Suporte = 2** (Frequente)
- **({B},{D}):**
  - C1: {B} em $t_2$, {D} em $t_3$ $\rightarrow$ **Sim**
  - C2: {B} em $t_1$, {D} em $t_3$ $\rightarrow$ **Sim**
  - Suporte em C1 e C2 $\rightarrow$ **Suporte = 2** (Frequente)

### 2-Sequências Frequentes Selecionadas ($L_2$):

$L_2$ = {({A},{B}), ({A},{C}), ({B},{C}), ({B},{D}), ({C},{D})}

### Passo 3: Gerando 3-Sequências Candidatas ($C_3$) e Poda

Unindo elementos de $L_2$:

1. Unindo $S_1$ = ({A}, {B}) e $S_2$ = ({B}, {C}):
  - Removendo o 1º item de $S_1 \rightarrow$ ({B}).
  - Removendo o último item de $S_2 \rightarrow$ ({B}).
  - As subsequências intermediárias são iguais!
  - **Candidato Gerado:** ({A}, {B}, {C}).

2. Unindo $S_1$ = ({B}, {C}) e $S_2$ = ({C}, {D}):
  - **Candidato Gerado:** ({B}, {C}, {D}).

3. Unindo $S_1$ = ({A}, {C}) e $S_2$ = ({C}, {D}):
  - **Candidato Gerado:** ({A}, {C}, {D}).

#### Teste de Suporte para $C_3$:

- **({A}, {B}, {C}):**
  - C1: {A} em $t_1$, {B} em $t_2$, mas C está no mesmo $t_2$ (não estritamente posterior).
  - C2: {A, B} em $t_1$, {C} em $t_2 \rightarrow$ Possui a sequência ({A}, {C}), mas para ({A}, {B}, {C}) necessita de B antes de C.
  - **Suporte = 1** (Infrequente $\rightarrow$ **Descartado**)

- **({B}, {C}, {D}):**
  - C1: {B} em $t_2$, {C} em $t_2$, {D} em $t_3$.
  - C2: {B} em $t_1$, {C} em $t_2$, {D} em $t_3$ $\rightarrow$ **Sim**
  - C1 (com suporte a sub-eventos no mesmo instante) e C2 possuem o padrão $\rightarrow$ **Suporte = 2** (Frequente)

- **({A}, {C}, {D}):**
  - C1: {A} em $t_1$, {C} em $t_2$, {D} em $t_3$ $\rightarrow$ **Sim**
  - C2: {A}$ em $t_1$, {C}$ em $t_2$, {D}$ em $t_3$ $\rightarrow$ **Sim**
  - **Suporte = 2** (Frequente)

### 3-Sequências Frequentes Selecionadas ($L_3$):

$L_3 = {({B}, {C}, {D} ), ( {A}, {C}, {D} ) }$

### Passo 4: Tentativa de Gerar 4-Sequências ($C_4$)

Tentar unir ({A}, {C}, {D} ) e ({B}, {C}, {D}):

- Ao remover os extremos, as subsequências resultantes não coincidem perfeitamente para permitir uma união válida sem violar as regras de poda de $L_3$.
- Nenhuma 4-sequência candidata atinge min_sup.

**Execução Encerrada!**
