# MODELO DE MISTURA GAUSSIANA (GMM)

O GMM é um algoritmo de agrupamento (clustering) baseado em modelos probabilísticos. Enquanto o K-Means e K-Medoids realizam agrupamento rígido, onde cada dado pertence estritamente a um único cluster, o GMM realiza **agrupamento suave**, atribuindo a cada ponto uma **probabilidade de pertencer a cada um dos K clusters**.

O GMM assume que todos os pontos do dataset foram gerados a partir de uma mistura de K distribuições normais com parâmetros desconhecidos. O objetivo do algoritmo é estimar a posição, o formato e o tamanho dessas distribuições para modelar a densidade dos dados. Por isso esse modelo é essencialmente ligado à distribuição normal. O objetivo dele é definir quais são as distribuições normai que geram esses dados e, portanto, irão gerar os dados futuros. Em outras palavras, ele diz que **um comportamento no mundo real pode ser expresso como um conjunto de distribuições normais**.

Ele funciona através do algoritmo **Maximização da Expectativa (EM)**. Ele alterna entre calcular a probabilidade de cada ponto pertencer a cada componente Gaussiana (**Passo E**) e recalcular a média, a variância/covariância e o peso de cada Gaussiana com base nessas probabilidades (**Passo M**), até que a verossimilhança do modelo atinja a convergência. O EM é sua função de otimização, enquanto a Máxima Verossimilhança é sua função de custo.

## Estrutura e Conceitos Principais

O GMM fundamenta-se na combinação de K distribuições Gaussianas no espaço multidimensional:

### 1. Distribuição Gaussiana Multivariada

Cada cluster k é modelado como uma distribuição normal com duas propriedades geométricas fundamentais:
- **Vetor de Médias ($\mu_k$):** Define o centro geométrico do cluster no espaço $p$-dimensional.
- **Matriz de Covariância ($\Sigma_k$):** Define o formato, a orientação e a dispersão (volume) do cluster.

A função de densidade de probabilidade $N(x_i \mid \mu_k, \Sigma_k)$ para um dado $x_i$ em d dimensões é dada por:

$$N(x_i \mid \mu_k, \Sigma_k) = \frac{1}{(2\pi)^{d/2} \vert{}\Sigma_k\vert{}^{1/2}} \exp (( -\frac{1}{2} (x_i - \mu_k)^T \Sigma_k^{-1} (x_i - \mu_k) ))$$

### 2. Pesos de Mistura ($p_k$)

Cada componente Gaussiano k possui uma proporção/peso de mistura $p_k$, representando a probabilidade a priori de um ponto aleatório ter sido gerado por aquela Gaussiana. A soma de todos os pesos deve ser igual a 1:

$$\sum_{k=1}^{K} p_k = 1 \quad \text{com } 0 \le p_k \le 1$$

A densidade de probabilidade total de um ponto $x_i$ no dataset é a soma ponderada de todas as componentes:

$$p(x_i) = \sum_{k=1}^{K} p_k N(x_i \mid \mu_k, \Sigma_k)$$

### 3. Responsabilidade ($\gamma_{ik}$) — Soft Clustering

A **responsabilidade** $\gamma_{ik}$ é a probabilidade a posteriori de que o ponto $x_i$ pertença ao cluster k. Utilizando o Teorema de Bayes:

$$\gamma_{ik} = P(\text{cluster}_k \mid x_i) = \frac{p_k N(x_i \mid \mu_k, \Sigma_k)}{\sum_{j=1}^{K} p_j N(x_i \mid \mu_j, \Sigma_j)}$$

## Passo-a-Passo (Algoritmo EM)

O GMM utiliza o método de otimização **Maximização da Expectativa (EM)** para encontrar os parâmetros que maximizam a verossimilhança dos dados:

1. **Inicialização:**
   - Escolhem-se previamente o número K de componentes.
   - Inicializam-se os parâmetros de cada curva normal:
     - Define as médias iniciais rodando o K-Means algumas vezes.
     - Define as covariâncias iniciais como matrizes identidade ou covariância global.
     - Define os pesos de mistura como 1/K.

2. **Passo E (Expectativa):**
   - Para cada ponto $x_i$ e para cada cluster k, calcula-se a responsabilidade $\gamma_{ik}$ (a probabilidade de $x_i$ ter sido gerado pela normal k).

3. **Passo M (Maximização):**
   - Atualizam-se os parâmetros de todos os K componentes utilizando os valores de responsabilidade $\gamma_{ik}$ calculados no Passo E:

   - **Número efetivo de pontos alocados ao cluster k ($N_k$):**
     $$N_k = \sum_{i=1}^{N} \gamma_{ik}$$

   - **Nova Média ($\mu_k^{\text{novo}}$):**
     $$\mu_k^{\text{novo}} = \frac{1}{N_k} \sum_{i=1}^{N} \gamma_{ik} x_i$$

   - **Nova Matriz de Covariância ($\Sigma_k^{\text{novo}}$):**
     $$\Sigma_k^{\text{novo}} = \frac{1}{N_k} \sum_{i=1}^{N} \gamma_{ik} (x_i - \mu_k^{\text{novo}})(x_i - \mu_k^{\text{novo}})^T$$

   - **Novo Peso de Mistura ($p_k^{\text{novo}}$):**
     $$p_k^{\text{novo}} = \frac{N_k}{N}$$

4. **Verificação de Convergência (Máxima Verossimilhança):**
   - Calcula-se a Log-Verossimilhança total do dataset:
   
     $$\ln P(X \mid \mu, \Sigma, p) = \sum_{i=1}^{N} \ln \left( \sum_{k=1}^{K} p_k N(x_i \mid \mu_k, \Sigma_k) \right)$$
   
   - Se o ganho na Log-verossimilhança entre as iterações for menor que uma tolerância e, o algoritmo convergiu e encerra a execução. Caso contrário, retorna-se ao **Passo E**.

## Exemplo

Considere N=4 compras aonde X é o valor gasto em R$:

- $x_1 = 1$
- $x_2 = 2$
- $x_3 = 8$
- $x_4 = 10$

Queremos agrupar os clientes em K = 2 grupos.

A função normal é:

$$N(x \mid \mu, \sigma^2) = \frac{1}{\sqrt{2\pi \sigma^2}} \exp\left( -\frac{(x - \mu)^2}{2\sigma^2} \right)$$

### Passo 1: Inicialização dos Parâmetros

- **Gaussiana 1:** $\mu_1 = 2$, $\sigma_1^2 = 1$, $p_1 = 0.5$
- **Gaussiana 2:** $\mu_2 = 8$, $\sigma_2^2 = 1$, $p_2 = 0.5$

Variância = Matriz identidade = 1 (já que só temos 1 variável). P = 1/2 e média vem de executar o K-means.

### Passo 2: 1ª Iteração - Passo E (Cálculo das Responsabilidades)

Calculamos a densidade de probabilidade para cada ponto em relação a cada função normal:

- **Para $x_1 = 1$:**
  - $N(1 \mid 2, 1) = \frac{1}{\sqrt{2\pi}} e^{-0.5} \approx 0.3989 \cdot 0.6065 \approx 0.2420$
  - $N(1 \mid 8, 1) = \frac{1}{\sqrt{2\pi}} e^{-24.5} \approx 0.0000$
  - Responsabilidades: $\gamma_{11} \approx 1.0$, $\gamma_{12} \approx 0.0$

- **Para $x_2 = 2$:**
  - $N(2 \mid 2, 1) = \frac{1}{\sqrt{2\pi}} e^{0} \approx 0.3989$
  - $N(2 \mid 8, 1) = \frac{1}{\sqrt{2\pi}} e^{-18} \approx 0.0000$
  - Responsabilidades: $\gamma_{21} \approx 1.0$, $\gamma_{22} \approx 0.0$

- **Para $x_3 = 8$:**
  - $N(8 \mid 2, 1) = \frac{1}{\sqrt{2\pi}} e^{-18} \approx 0.0000$
  - $N(8 \mid 8, 1) = \frac{1}{\sqrt{2\pi}} e^{0} \approx 0.3989$
  - Responsabilidades: $\gamma_{31} \approx 0.0$, $\gamma_{32} \approx 1.0$

- **Para $x_4 = 10$:**
  - $N(10 \mid 2, 1) = \frac{1}{\sqrt{2\pi}} e^{-32} \approx 0.0000$
  - $N(10 \mid 8, 1) = \frac{1}{\sqrt{2\pi}} e^{-2} \approx 0.3989 \cdot 0.1353 \approx 0.0540$
  - Responsabilidades: $\gamma_{41} \approx 0.0$, $\gamma_{42} \approx 1.0$

### Passo 3: 1ª Iteração - Passo M (Atualização dos Parâmetros)

1. **Número Efetivo de Pontos ($N_k$):**
   - $N_1 = \gamma_{11} + \gamma_{21} + \gamma_{31} + \gamma_{41} = 1.0 + 1.0 + 0.0 + 0.0 = 2.0$
   - $N_2 = \gamma_{12} + \gamma_{22} + \gamma_{32} + \gamma_{42} = 0.0 + 0.0 + 1.0 + 1.0 = 2.0$

2. **Novas Médias ($\mu_k$):**
   - $\mu_1^{\text{novo}} = \frac{1.0(1) + 1.0(2) + 0(8) + 0(10)}{2.0} = \frac{3}{2} = 1.5$
   - $\mu_2^{\text{novo}} = \frac{0(1) + 0(2) + 1.0(8) + 1.0(10)}{2.0} = \frac{18}{2} = 9.0$

3. **Novas Variâncias ($\sigma_k^2$):**
   - $\sigma_1^{2, \text{novo}} = \frac{1.0(1 - 1.5)^2 + 1.0(2 - 1.5)^2}{2.0} = \frac{0.25 + 0.25}{2.0} = 0.25$
   - $\sigma_2^{2, \text{novo}} = \frac{1.0(8 - 9.0)^2 + 1.0(10 - 9.0)^2}{2.0} = \frac{1.0 + 1.0}{2.0} = 1.0$

4. **Novos Pesos ($\pi_k$):**
   - $\pi_1^{\text{novo}} = \frac{2}{4} = 0.5$
   - $\pi_2^{\text{novo}} = \frac{2}{4} = 0.5$

Nas iterações seguintes, o algoritmo refinará ligeiramente as densidades até estabilizar. **O modelo não apenas separou os grupos em $\{1, 2\}$ e $\{8, 10\}$, mas também estimou a incerteza de cada atribuição e o formato interno dos dados**.

## Tipos de Matriz de Covariância

A grande vantagem do GMM em relação ao K-Means é a flexibilidade geométrica proporcionada pela escolha do tipo da matriz de covariância ($\Sigma$):

1. **`spherical` (Esférico):**
   - Cada cluster possui formato circular/esférico, mas com raio diferente. É o comportamento mais próximo do K-Means.
2. **`diag` (Diagonal):**
   - Os clusters formam elipses alinhadas paralelamente aos eixos das coordenadas.
3. **`tied` (Vinculado):**
   - Todos os K clusters compartilham exatamente o mesmo formato e orientação elíptica.
4. **`full` (Completo - Padrão):**
   - Cada cluster pode ter qualquer orientação, formato elíptico e volume independentes no espaço. É o modelo mais genérico e poderoso.

## PREMISSAS

- **Distribuição normal dos Dados:** Assume-se que a distribuição subjacente dos dados dentro de cada subgrupo segue uma curva normal.
   - Para confirmar pode rodar o teste de Shapiro-Wilk em cada grupo.
- **Variáveis Numéricas Contínuas:** Os dados devem ser numéricos e contínuos para o cálculo das funções de densidade de probabilidade.
- **Volume Suficiente de Dados:** Como calcula matrizes de covariância completas, exige uma quantidade razoável de dados para evitar problemas de matrizes singulares/não-invertíveis.

## QUANDO USAR

- **Atribuição Probabilística:** Quando um registro pode pertencer a mais de um grupo e o negócio precisa quantificar a dúvida/incerteza (ex: um cliente que compra tanto artigos esportivos quanto eletrônicos).
- **Grupos com tamanhos e formatos diversos:** Onde o K-Means falha por assumir apenas esferas de tamanhos iguais.
- **Estimação de Densidade:** Quando o objetivo vai além do agrupamento e busca-se modelar a distribuição contínua dos dados.

## QUANDO NÃO USAR

- **Clusters com Formatos Arbitrários:** Para agrupamentos em formato de arco, espiral ou anel, o GMM falhará (prefira **DBSCAN** ou **HDBSCAN**).
- **Bases com Múltiplas Variáveis Categóricas:** A função normal não é funciona com dados categóricos.
- **Muitas Dimensões com Poucas Amostras (p $\gg$ N):** Pode levar à singularidade da matriz de covariância (divisão por zero no determinante).
- **Necessidade de Extrema Velocidade:** O algoritmo EM é computacionalmente mais custoso e lento que o K-Means.

## COMO DETERMINAR O NÚMERO DE COMPONENTES K

Como aumentar K e aumentar a complexidade da covariância sempre aumentam a verossimilhança (causando overfitting), utilizam-se métricas que penalizam a complexidade (AIC e BIC).

### 1. BIC (Bayesian Information Criterion)

$$\text{BIC} = -2 \ln(L) + p_{\text{par}} \ln(N)$$

### 2. AIC (Akaike Information Criterion)

$$\text{AIC} = -2 \ln(L) + 2 p_{\text{par}}$$

Onde L é a verossimilhança, N é o número de amostras e $p_{\text{par}}$ é o número de colunas.

**Regra de Decisão:** Escolha K que tenha o **menor BIC ou AIC**.
