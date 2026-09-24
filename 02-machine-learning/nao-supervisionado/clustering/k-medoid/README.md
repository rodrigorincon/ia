# K-MEDOID

É uma **variação robusta do K-Means**, projetada para resolver a alta sensibilidade que o K-Means possui em relação a outliers. A diferença fundamental está na definição do centro do grupo: enquanto no K-Means o centroide (centro do grupo) pode não ser igual a nenhum ponto e ficar flutuando entre eles, o K-Medoid define como centro de cada grupo um **ponto real pertencente ao conjunto de dados**.

No Kmeans a gente chama o centro de centróide, no Kmedoid o nome é **medóide**.

O K-Medoid busca minimizar a soma das dissimilaridades entre os pontos e o seu medoide correspondente. O seu processo iterativo funciona testando **trocas de pontos**: ele seleciona medoides iniciais reais, atribui cada dado ao medoide mais próximo e avalia se substituir um medoide por outro ponto qualquer da base reduz o custo total do agrupamento.

## Mudanças na estrutura

### Medoide (vs. Centroide)

O medoide é o membro de um cluster cuja média de dissimilaridade (ou distância) em relação a todos os outros pontos do mesmo grupo é mínima. 

Por ser um registro real presente na base de dados, o medoide traz interpretabilidade direta ao negócio (ex: o **cliente medoide é o "cliente típico"** real daquele segmento, e não uma média hipotética de compras).

Dado um cluster $C_j$, o seu medoide $m_j$ é o ponto que satisfaz:

$$m_j = \arg\min_{y \in C_j} \sum_{x_i \in C_j} d(x_i, y)$$

### Função de Custo: Erro Absoluto Total

A **função de custo** do K-Medoid avalia a soma de todas as distâncias de cada ponto até o medoide do seu respectivo cluster:

$$\text{Custo Total} = \sum_{j=1}^{K} \sum_{x_i \in C_j} d(x_i, m_j)$$

Ele se diferencia do WCSS ao não elevar os erros ao quadrado, dando valores muito menores. Ele também é menos sensível a outliers que o WCSS e é mais ligado à mediana que a média.

O objetivo do algoritmo é encontrar a combinação de K medoides que minimize essa soma total. 

## Passo-a-Passo (PAM)

O algoritmo clássico para implementar o K-Medoid é o **PAM (Partitioning Around Medoid)**, dividido em duas fases (build e swap):

1. **Inicialização (Fase build):**
- Escolhem-se K pontos reais do dataset para atuarem como os medoides iniciais $m_1, m_2, ..., m_K$.

2. **Atribuição Inicial:**
- Para cada ponto $x_i$ da base de dados, calcula-se a distância até todos os K medoides.
- O ponto $x_i$ é alocado ao cluster do medoide mais próximo.
- Calcula-se o **Custo Total Inicial** do modelo.

3. **Etapa de Troca (Fase swap / Atualização):**
- Para cada medoide $m_j$ e para cada ponto não-medoide O do grupo:
  - Simula-se a **troca** do medoide $m_j$ pelo ponto O.
  - Reatribuem-se todos os pontos da base aos novos medoides temporários.
  - Recalcula-se o Custo Total.
  - Calcula-se a variação de custo $\Delta S = \text{Custo}_{\text{novo}} - \text{Custo}_{\text{atual}}$.

4. **Decisão de Troca:**
- Se a melhor troca encontrada resultar em redução do custo ($\Delta S < 0$), a troca é mantida permanentemente e o ponto O vira o novo medoide.

5. **Verificação de Convergência (Condição de Parada):**
- Repete-se a etapa de troca até que nenhuma substituição de medoide consiga reduzir o Custo Total da partição.

## PREMISSAS

- **Padronização de Escala:** Assim como no K-Means, se for utilizada uma métrica geométrica (Manhattan ou Euclidiana), variáveis com escalas maiores dominam o cálculo de distância.
- **Formatos de Clusters Esféricos/Globulares:** Assume que os grupos possuem densidade e volume homogêneos ao redor de cada medoide.

## QUANDO USAR

- **Presença de Outliers e Ruído:** É a alternativa ideal ao K-Means quando a base possui valores extremos, pois a escolha de um ponto real minimiza a distorção gerada por *outliers*.
- **Necessidade de Interpretabilidade Real:** Quando o negócio exige que o centro do grupo seja um elemento real (ex: selecionar um produto real representativo de uma categoria para vitrine de e-commerce).
- **Métricas de Distância Não-Euclidianas:** Quando a natureza dos dados exige métricas como Manhattan, Mahalanobis ou matrizes de dissimilaridade customizadas.

## QUANDO NÃO USAR

- **Bases de Dados Muito Grandes (muitas linhas):** A fase de troca do algoritmo PAM possui complexidade computacional elevada ($O(K * (N - K)^2)$ por iteração). Para grandes volumes de dados, utilize variações otimizadas como **CLARA** (Clustering Large Applications) ou **CLARANS**.
- **Clusters com Formatos Arbitrários:** Se a estrutura dos dados apresentar formatos não convexos (ex: espirais, linhas conectadas), prefira algoritmos de densidade como **DBSCAN** ou **HDBSCAN**.
- **Dados Estritamente Categóricos Nominais:** Embora aceite distâncias categóricas, o **K-Modes** costuma ser mais performático para bases 100% categóricas.

## OTIMIZAÇÕES PARA BIG DATA: CLARA e CLARANS

Como o K-Medoid original (PAM) é computacionalmente pesado para bases grandes, existem duas variantes principais:

1. **CLARA (Clustering Large Applications):**
   * Retira **amostras aleatórias** do dataset original.
   * Aplica o algoritmo PAM em cada amostra para encontrar os medoides.
   * Seleciona o conjunto de medoides que apresentar o menor custo para todo o dataset completo.

2. **CLARANS (Clustering Large Applications based upon Randomized Search):**
   * Funciona como uma busca em grafo na qual cada nó é um conjunto de K medoides.
   * Avalia um subconjunto aleatório de vizinhos (trocas possíveis) em vez de testar todas as combinações do dataset, reduzindo drasticamente o tempo de processamento.
