# ECLAT (EQUIVALENCE CLASS TRANSFORMATION)

Recebe esse nome pois transforma o problema de mineração de padrões em subproblemas menores através de **classes de equivalência** baseadas em prefixos comuns. Ele serve para encontrar conjuntos de itens frequentes em bases de dados transacionais, porém de forma um pouco diferente do Apriori e FP-Growth. Enquanto o Apriori e o FP-Growth trabalham com o banco de dados na horizontal (onde cada linha é uma transação com vários itens), o ECLAT utiliza a **tabela de dados na vertical (cada linha é um item e as colunas são as transações)**. 

> Ao invés de perguntar "Quais itens estão nesta transação?", o ECLAT pergunta **"Em quais transações este item aparece?"**.

Essa mudança de perspectiva elimina a necessidade de construir estruturas complexas de árvore (como a FP-Tree) e substitui a contagem de frequências por simples **interseções de IDs de transações (TIDs)**.

## Estrutura

O funcionamento do ECLAT assenta em três pilares fundamentais: o **Layout Vertical**, as **Classes de Equivalência** e a **Busca em Profundidade (DFS)**.

### Layout Vertical e TID-list

No layout horizontal tradicional, temos:

* `T1: Leite, Pão`

* `T2: Leite, Manteiga`

No layout vertical, convertemos os dados em TID-lists (listas de identificadores de transação):

* `Leite: {T1, T2}`

* `Pão: {T1}`

* `Manteiga: {T2}`

Portanto, **TID-List é a tabela vertical e TID é a linha da tabela**.

O suporte de qualquer item individual ou conjunto de itens é simplesmente a **quantidade de elementos na sua TID-list** (a cardinalidade do conjunto):

$Suporte(A) = TID(A)$

Para encontrar o suporte da combinação de dois ou mais itens, fazemos a **interseção** das suas listas de TIDs:

$TID(AB) = TID(A) \cap TID(B)$

$Suporte(AB) = TID(AB) = TID(A) \cap TID(B)$

### Classes de Equivalência (Equivalence Classes)

Para evitar comparar itens incompatíveis, o ECLAT agrupa os conjuntos de itens que compartilham o mesmo prefixo. Uma classe de equivalência $C_k$ contém todos os k-conjuntos que possuem os mesmos k-1 itens iniciais.

Por exemplo, a classe com prefixo `Leite` agrupa:

- `{Leite, Pão}`
- `{Leite, Pão, Manteiga}`
- `{Leite, Manteiga}`
- `{Leite, Café}`

E o prefixo `Leite, Pão` agrupa:

- `{Leite, Pão}`
- `{Leite, Pão, Manteiga}`

Como não existe nenhuma transação com `Pão e Café`, nós não criamos esse prefixo. Todos os prefixos criados devem ter ao menos 1 transação nela.

### Busca em Profundidade (DFS - Depth-First Search)

Diferente do Apriori (que opera em largura, nível a nível), o ECLAT explora a árvore de combinações em **profundidade**:

1. Pega um prefixo (ex: `Leite`).

2. Expande para `{Leite, Pão}`.

3. Tenta expandir imediatamente para `{Leite, Pão, Manteiga}`.

4. Quando a combinação esgota ou fica abaixo do min_sup, ele volta um nível e testa o próximo ramo.

Isso permite processar cada classe de equivalência de forma totalmente isolada em memória.

## Passo-a-Passo do Algoritmo

O algoritmo executa os seguintes passos ordenados:

1. **Transformação da matriz:** Converte a base de dados transacional horizontal para vertical (mapeando cada item para sua TID-list).

2. **Filtragem de 1-Itemsets:** Calcula a cardinalidade de cada TID-list. Remove os itens isolados cujo TID < min_sup.

3. **Ordenação:** Ordena os itens mantidos (geralmente por ordem alfabética ou por frequência para otimizar as interseções).

4. **Divisão em Classes de Equivalência:** Agrupa os 1-itemsets em classes com base no prefixo comum.

5. **Mineração Recursiva (DFS):**

   * Para cada classe de equivalência, realiza a interseção das TID-lists dos pares de itens.

   * Se a cardinalidade do resultado for $\ge min_sup$, o novo conjunto é considerado frequente e forma uma nova sub-classe de equivalência.

   * O processo se repete recursivamente até que nenhuma nova interseção válida possa ser feita.

## Como a Árvore de Busca é Construída e Iterada

A árvore no ECLAT não é uma estrutura mantida fisicamente em memória como no FP-Growth, mas sim uma Árvore Implícita de Prefixos (Prefix Tree) percorrida pela pilha de execução da recursão:

```
                      [ Root ]
          /              |              \
     {Leite}           {Pão}         {Manteiga}
     /     \             |
{Leite,Pão} {Leite,Mant} {Pão,Mant}
    |
{Leite,Pão,Mant}

```

### Como a iteração navega na árvore:

1. **Geração do Nó Raiz:** A raiz tem como filhos todos os 1-itemsets frequentes com suas respectivas TID-lists.

2. **Descer um Ramo (Aprofundamento):** O ECLAT seleciona o primeiro item (ex: `Leite`) e o combina com o próximo item do mesmo nível (ex: `Pão`).

   * Calcula $TID(Leite \cap Pão)$.

   * Se $TID \ge min_sup$, declara `{Leite, Pão}` como frequente.

   * **Mergulha imediatamente** para testar as combinações de `{Leite, Pão}` com outros itens (ex: `{Leite, Pão, Manteiga}`).

3. **Poda:** Se a interseção resultar em um número de TIDs menor do que min_sup, aquele nó folha é **podado** e a recursão não avança por aquele caminho.

4. **Subir um Ramo:** Ao finalizar a exploração profunda de um prefixo, o algoritmo desaloca a TID-list intermediária da memória e volta ao nível anterior para processar o próximo par da classe.

## Exemplo

Considerando uma base de dados com 5 transações (N=5) e um suporte mínimo min_sup = 2 (40%).

### Base de Dados Original (Matriz Horizontal)

| ID Transação | Itens Comprados | 
 | ----- | ----- | 
| **T1** | Leite, Pão, Manteiga | 
| **T2** | Leite, Café, Pão | 
| **T3** | Leite, Manteiga | 
| **T4** | Café, Pão | 
| **T5** | Leite, Pão, Manteiga, Café | 

### Passo 1: Conversão para Matriz Vertical (TID-lists)

Mapeando cada item para as transações em que ele ocorre e calculando o suporte inicial:

| Item | TID-list | Suporte ($TID$) | Status (min_sup $\ge$ 2) | 
 | ----- | ----- | ----- | ----- | 
| **Leite** | `{T1, T2, T3, T5}` | 4 | **Frequente** | 
| **Pão** | `{T1, T2, T4, T5}` | 4 | **Frequente** | 
| **Manteiga** | `{T1, T3, T5}` | 3 | **Frequente** | 
| **Café** | `{T2, T4, T5}` | 3 | **Frequente** | 

Todos os 1-itemsets são mantidos.

### Passo 2: Interseção de 2-Itemsets (Classe k=2)

Combinamos os itens par a par realizando a interseção dos seus conjuntos de TIDs:

#### Classe com prefixo `Leite`:

- **`{Leite, Pão}`**: `{T1, T2, T3, T5}` $\cap$ `{T1, T2, T4, T5}` = `{T1, T2, T5}` $\rightarrow$ **Suporte = 3** (Frequente)

- **`{Leite, Manteiga}`**: `{T1, T2, T3, T5}` $\cap$ `{T1, T3, T5}` = `{T1, T3, T5}` $\rightarrow$ **Suporte = 3** (Frequente)

- **`{Leite, Café}`**: `{T1, T2, T3, T5}` $\cap$ `{T2, T4, T5}` = `{T2, T5}` $\rightarrow$ **Suporte = 2** (Frequente)

#### Classe com prefixo `Pão`:

* **`{Pão, Manteiga}`**: `{T1, T2, T4, T5}` $\cap$ `{T1, T3, T5}` = `{T1, T5}` $\rightarrow$ **Suporte = 2** (Frequente)

* **`{Pão, Café}`**: `{T1, T2, T4, T5}` $\cap$ `{T2, T4, T5}` = `{T2, T4, T5}` $\rightarrow$ **Suporte = 3** (Frequente)

#### Classe com prefixo `Manteiga`:

* **`{Manteiga, Café}`**: `{T1, T3, T5}` $\cap$ `{T2, T4, T5}` = `{T5}` $\rightarrow$ **Suporte = 1** (Infrequente $\rightarrow$ **Descartado**)

### Passo 3: Interseção de 3-Itemsets (Aprofundamento DFS)

Agora combinamos os 2-itemsets frequentes que compartilham o mesmo prefixo de tamanho 1:

#### Aprofundando na classe `{Leite}`:

- Combinar `{Leite, Pão}` e `{Leite, Manteiga}` para testar **`{Leite, Pão, Manteiga}`**:
  - $TID(\{Leite, Pão\}) \cap TID(\{Leite, Manteiga\}) = \{T1, T2, T5\} \cap \{T1, T3, T5\} = \{T1, T5\}$
  - **Suporte = 2** (Frequente)
- Combinar `{Leite, Pão}` e `{Leite, Café}` para testar **`{Leite, Pão, Café}`**:
  - $TID(\{Leite, Pão\}) \cap TID(\{Leite, Café\}) = \{T1, T2, T5\} \cap \{T2, T5\} = \{2, T5\}$
  - **Suporte = 2** (Frequente)
- Combinar `{Leite, Manteiga}` e `{Leite, Café}` para testar **`{Leite, Manteiga, Café}`**:
  - $TID(\{Leite, Manteiga\}) \cap TID(\{Leite, Café\}) = \{T1, T3, T5\} \cap \{T2, T5\} = \{T5\}$
  - **Suporte = 1** (Infrequente $\rightarrow$ **Descartado**)

#### Aprofundando na classe `{Pão}`:

- Combinar `{Pão, Manteiga}` e `{Pão, Café}` para testar **`{Pão, Manteiga, Café}`**:
  - $TID(\{Pão, Manteiga\}) \cap TID(\{Pão, Café\}) = \{T1, T5\} \cap \{T2, T4, T5\} = \{T5\}$
  - **Suporte = 1** (Infrequente $\rightarrow$ **Descartado**)

### Passo 4: Interseção de 4-Itemsets

Testamos a combinação dos 3-itemsets que possuam o mesmo prefixo de 2 itens:

- Combinar `{Leite, Pão, Manteiga}` e `{Leite, Pão, Café}` para testar **`{Leite, Pão, Manteiga, Café}`**:
  - $TID(\{Leite, Pão, Manteiga\}) \cap TID(\{Leite, Pão, Café\}) = \{T1, T5\} \cap \{T2, T5\} = \{T5\}$
  - **Suporte = 1** (Infrequente $\rightarrow$ **Descartado**)

Nenhuma nova combinação é válida. A execução é encerrada.

### Resultado Final dos Itemsets Frequentes Extraídos

- **1-itemsets:** `{Leite}` (4), `{Pão}` (4), `{Manteiga}` (3), `{Café}` (3)

- **2-itemsets:** `{Leite, Pão}` (3), `{Leite, Manteiga}` (3), `{Leite, Café}` (2), `{Pão, Manteiga}` (2), `{Pão, Café}` (3)

- **3-itemsets:** `{Leite, Pão, Manteiga}` (2), `{Leite, Pão, Café}` (2)

## PREMISSAS

- **Identificadores Únicos de Transação (TIDs):** Cada transação deve possuir um ID exclusivo (se não tiver, crie).
- **Dados Discretos / Categóricos:** O algoritmo lida com presença ou ausência de itens discretos ou categóricos em transações.

## QUANDO USAR

- **bases de dados de tamanho moderado** 
- **Aplicações MultiThread:** Como as classes de equivalência são completamente independentes umas das outras, cada classe pode ser processada em uma thread/núcleo de CPU diferente sem necessidade de sincronização.
  - Vantagem em relação ao FP-Growth, que não pode ser paralelizado.
- **Código simples e sem estruturas complexas:** Ideal quando se quer uma implementação limpa e de alta velocidade baseada apenas em operações de conjuntos (interseções bitwise ou hash sets).

## QUANDO NÃO USAR

- **Bases com milhões de transações (TIDs gigantes):** Se o número de transações N for enorme, cada TID-list ocupará muitos megabytes/gigabytes. Fazer interseções de listas gigantes consumirá toda a memória RAM e deixará o processo lento.
- **Dados extremamente esparsos com muitos itens únicos:** Gera poucas interseções úteis e gasta processamento alocando conjuntos vazios.

## OTIMIZAÇÃO: DIFFSETS (ECLAT Avançado)

Para solucionar o problema de TID-lists gigantes em bases com muitas transações, existe uma variação do ECLAT que utiliza **Diffsets** (conjuntos de diferença).

Em vez de guardar quais transações contêm a combinação de itens, o Diffset guarda apenas quais transações contêm o prefixo, mas **NÃO contêm** o novo item:

$$Diffset(AB) = \frac{TID(A)}{TID(B)}$$

$$Suporte(AB) = Suporte(A) - Diffset(AB)$$

À medida que o algoritmo aprofunda na árvore e os conjuntos de itens ficam maiores, os Diffsets vão ficando **cada vez menores** (tendendo a zero), reduzindo dramaticamente o uso de memória RAM.

## MÉTRICAS E REGRAS DE ASSOCIAÇÃO

Após a extração dos itemsets frequentes pelo ECLAT, as regras de associação $A \rightarrow B$ são calculadas usando as métricas padrão:

### 1. Suporte

$$Suporte(A \rightarrow B) = \frac{TID(A \cap B)}{N}$$

### 2. Confiança

A razão entre as interseções e o suporte do antecedente A:

$$Confianca(A \rightarrow B) = \frac{TID(A \cap B)}{TID(A)}$$

### 3. Lift

$$Lift(A \rightarrow B) = \frac{Confianca(A \rightarrow B)}{Suporte_{relativo}(B)}$$