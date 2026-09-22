# K-NEAREST NEIGHBORS (KNN)

É um algoritmo que serve tanto para **regressão como para classificação**. Recebe esse nome pois se baseia literalmente no conceito de consultar os **K vizinhos mais próximos** de um novo dado para realizar uma predição. É um dos algoritmos de aprendizado de máquina mais intuitivos e simples de entender.

Diferente da Regressão Logística ou da Regressão Linear, o KNN é um algoritmo **não-paramétrico e baseado em instâncias** (frequentemente chamado de lazy learning ou aprendizado preguiçoso). Isso significa que ele **não tem uma fase de treinamento** tradicional onde aprende uma fórmula matemática ou encontra coeficientes ajustados. Em vez disso, ele **memoriza todo o conjunto de dados de treino** e realiza todo o trabalho computacional no exato momento em que precisa fazer uma previsão. Isso o torna **muito lento para dar uma resposta**.

## Estrutura

A premissa fundamental do KNN é a **proximidade geográfica/espacial**: assume-se que dados que possuem características (variáveis X) parecidas estarão próximos uns dos outros no espaço vetorial e, portanto, tendem a compartilhar a mesma categoria ou um valor numérico similar (variável Y).

Um ótimo exemplo é estimar o valor de aluguel com base na sua área e número de quartos ($X_1, X_2$). O KNN busca os K imóveis do banco de dados que possuem a área e a quantidade de quartos mais parecidas com as do imóvel em questão e usa esses vizinhos para definir o preço estimado.

### O Princípio de Funcionamento

O objetivo do KNN é medir a distância entre o novo ponto não rotulado e todos os pontos já existentes na base histórica, selecionar os K pontos mais próximos e agregar suas respostas.

> O KNN não aprende uma função de decisão f(x) durante o treino. Toda a inteligência do modelo reside na busca de vizinhos dentro do espaço métrico no momento da consulta. Como não há ajustes de pesos (w) via gradiente descendente nem suposições sobre a distribuição dos dados, o modelo é extremamente flexível, mas exige atenção rigorosa em relação à escala das variáveis X.

## Componentes Principais

O funcionamento do KNN é sustentado por três pilares fundamentais:

1. **Hiperparâmetro K**: O número de vizinhos que serão consultados para tomar a decisão.
2. **Métrica de Distância**: A função matemática usada para medir quão "perto" ou "longe" dois pontos estão no espaço de atributos (ex: distância euclidiana).
3. **Regra de Agregação**: Como o algoritmo combina a informação dos K vizinhos para gerar a predição final (classe mais repetida para classificação ou média para regressão).

## PREMISSAS

- **Dados numéricos**:
   - Todas as variáveis X devem ser numéricas.
- **Transformação dos Dados**:
  - O KNN é extremamente sensível à escala das variáveis. Se a variável $X_1$ for o salário (variando de 1.000 a 50.000) e $X_2$ for a idade em anos (variando de 18 a 70), a distância matemática será 99.9% dominada pelo salário, tornando a idade irrelevante.
- **Ausência de Variáveis Irrelevantes**:
  - Variáveis que não possuem relação com Y adicionam ruído às distâncias e prejudicam gravemente a qualidade dos vizinhos selecionados.
  - Deve-se usar PCA, VIF ou Matriz de Correlação para remover variáveis que não forem úteis.
- **Não Sofrer com a "Maldição da Dimensionalidade"**:
  - Quando a quantidade de variáveis X é muito alta, os pontos no espaço tornam-se extremamente esparsos e equidistantes uns dos outros. Em dimensões elevadas, o conceito de "vizinho próximo" deixa de existir, pois todos os pontos ficam a distâncias semelhantes.
  - Uso de PCA se torna essencial para esse cenário.

> Ou seja, é preciso fazer **transformação nos dados, PCA e opcionalmente VIF ou matriz de correlação** antes do KNN para preparar os dados.

## Métricas de Distância

Para determinar quais pontos são os vizinhos mais próximos, o algoritmo calcula a distância entre o ponto de teste p e cada ponto de treino q.

### Distância Euclidiana (Mais Comum)

É a distância em linha reta entre dois pontos em um espaço n-dimensional (decorrente do Teorema de Pitágoras).

$$d(p, q) = \sqrt{\sum_{i=1}^{n} (p_i - q_i)^2}$$

### Distância de Manhattan (L1 / City Block)

Mede a soma das diferenças absolutas de suas coordenadas. Útil para cenários onde as variáveis representam rotas em grade (como quarteirões de uma cidade). A característica dele é não poder se mover em diagonal.

$$d(p, q) = \sum_{i=1}^{n} |p_i - q_i|$$

### Distância de Minkowski (Generalização)

É a fórmula geral que une a distância Euclidiana (r=2) e a Manhattan (r=1).

$$d(p, q) = \left( \sum_{i=1}^{n} |p_i - q_i|^r \right)^{\frac{1}{r}}$$

## Escolha do Valor K

O parâmetro K dita o nível de flexibilidade do modelo:

* **K muito pequeno (ex: K=1)**: O modelo consulta apenas 1 vizinho. Fica extremamente sensível a ruídos e outliers na base de dados, gerando **overfitting** (fronteiras de decisão altamente recortadas e instáveis).
* **K muito grande (ex: K=N)**: O modelo consulta quase a base inteira. A resposta será sempre a classe majoritária do dataset inteiro, gerando **underfitting** e ignorando os padrões locais.

> **Regra prática**: Para problemas de classificação binária, costuma-se escolher um número **ÍMPAR** para evitar empates na decisão da categoria.

## Y Previsto

### Classificação

Quando Y que precisamos prever é categórico, a classe prevista ŷ é a classe mais repetida entre os K vizinhos. Também é possível calcular a probabilidade da classe C como a proporção de vizinhos pertencentes a ela:

$$P(Y = C | X) = \frac{1}{K} \sum_{i \in \text{Vizinhos}} I(y_i = C)$$

### Regressão

O valor previsto ŷ é dado pela **média aritmética** dos valores Y dos K vizinhos mais próximos:

$$ŷ = \frac{1}{K} \sum_{i=1}^{K} y_i$$

Nota: Em ambas as abordagens, é possível aplicar uma **ponderação pelo inverso da distância** ($w_i = \frac{1}{d(p, q_i)}$), fazendo com que vizinhos que estejam muito mais perto do ponto de teste tenham maior peso no resultado final do que aqueles mais afastados.

## Passo-a-Passo do Algoritmo

1. **Coletar e Preparar os Dados**:
   * Garantir que todas as variáveis explicativas X sejam numéricas.
   * **Padronizar ou Normalizar** obrigatoriamente as variáveis X.
   * Remover variáveis pouco correlacionadas.
2. **Definir os Hiperparâmetros**:
   * Escolher o valor de K e a métrica de distância (ex: Euclidiana).
3. **Receber um Novo Ponto de Consulta**:
   * Para cada ponto i existente na base de treino:
     * Calcular a distância matemática entre o novo ponto e $X_i$.
   * Ordenar todas as distâncias calculadas em ordem crescente.
   * Selecionar os K pontos que possuem as menores distâncias.
4. **Gerar a Predição**:
   * Se Classificação: Contar os votos de cada classe nos K vizinhos e retornar a classe mais votada.
   * Se Regressão: Calcular e retornar a média dos valores Y dos K vizinhos.

## QUANDO NÃO USAR

- **Bases de Dados Muito Grandes (Muitas Linhas)**: Como o KNN precisa calcular a distância para **todos** os pontos do conjunto de treino a cada nova inferência, a complexidade no momento do teste é $O(N * D)$, tornando o modelo extremamente lento em termos de memória e tempo de execução.
- **Muitas Dimensões/Colunas ($D > 50$)**: A menos que seja aplicada uma técnica prévia de redução de dimensionalidade (como PCA).
- **Problemas com Latência Crítica de Predição em Tempo Real**: Quando se exige respostas em milissegundos para grande volume de requisições.
- **Bases de Dados com Grande Desbalanceamento de Classes**: Se uma classe representar $95\%$ dos dados, os vizinhos mais próximos quase sempre serão dessa classe majoritária.

## MÉTRICAS E AJUSTE DE HIPERPARÂMETROS

Os principais hiperparâmetros a serem testados via validação cruzada (*GridSearchCV* ou *RandomSearchCV*) são:

1. **Número de Vizinhos (K)**: Geralmente avaliado em um intervalo (ex: de 1 a 30).
2. **Métrica de Distância**: `euclidean`, `manhattan`, `minkowski` ou `cosine`.
3. **Ponderação dos Vizinhos ($w$)**:
   - `'uniform'`: Todos os $K$ vizinhos têm o mesmo peso na decisão.
   - `'distance'`: Vizinhos mais próximos possuem maior impacto no voto ou na média do que vizinhos mais distantes.

## Exemplos

### Classificação (K=3)

**Objetivo**: Prever se um aluno será **Aprovado (1)** ou **Reprovado (0)** com base em duas variáveis já padronizadas: $X_1$ (Horas de Estudo) e $X_2$ (Faltas).

**Base de Treino**:

| Aluno | $X_1$ (Estudo) | $X_2$ (Faltas) | Status ($Y$) |
| :--- | :--- | :--- | :--- |
| A    | 2    | 8    | Reprovado (0) |
| B    | 8    | 1    | Aprovado (1) |
| C    | 7    | 3    | Reprovado (0) |
| D    | 3    | 6    | Reprovado (0) |
| E    | 6    | 2    | Aprovado (1) |

**Novo Aluno (Consulta)**: P = (6, 3)

#### Passo 1: Calcular as Distâncias Euclidianas de $P$ até cada Aluno

$d(A, P) = \sqrt{(2 - 6)^2 + (8 - 3)^2} = \sqrt{(-4)^2 + (5)^2} = \sqrt{16 + 25} = \sqrt{41} \approx \mathbf{6.40}$

$d(B, P) = \sqrt{(8 - 6)^2 + (1 - 3)^2} = \sqrt{(2)^2 + (-2)^2} = \sqrt{4 + 4} = \sqrt{8} \approx \mathbf{2.83}$

$d(C, P) = \sqrt{(7 - 6)^2 + (3 - 3)^2} = \sqrt{(1)^2 + (0)^2} = \sqrt{1 + 0} = \sqrt{1} = \mathbf{1}$

$d(D, P) = \sqrt{(3 - 6)^2 + (6 - 3)^2} = \sqrt{(-3)^2 + (3)^2} = \sqrt{9 + 9} = \sqrt{18} \approx \mathbf{4.24}$

$d(E, P) = \sqrt{(6 - 6)^2 + (2 - 3)^2} = \sqrt{(0)^2 + (-1)^2} = \sqrt{0 + 1} = \sqrt{1} = \mathbf{1.00}$

#### Passo 2: Selecionar os K=3 Vizinhos Mais Próximos

1. **Aluno C** (Distância: 1.00) $\rightarrow$ Status: **Reprovado (0)**
2. **Aluno E** (Distância: 1.00) $\rightarrow$ Status: **Aprovado (1)**
3. **Aluno B** (Distância: 2.83) $\rightarrow$ Status: **Aprovado (1)**

Como a maioria dos vizinhos são Aprovados (2 de 3), o novo aluno é classificado como **Aprovado** (com 66% de probabilidade).

### Exemplo 2: Regressão (K=3)

**Objetivo**: Estimar o **Preço em R$ (Y)** de um imóvel com base em seus atributos padronizados $X_1$ (Área em m²) e $X_2$ (Número de Quartos).

**Base de Treino**:

| Imóvel | $X_1$ (Área padronizada) | $X_2$ (Quartos padronizados) | Preço Real (Y) |
| :--- | :--- | :--- | :--- |
| A | 1.0 | 1.0 | 200.000 |
| B | 4.0 | 3.0 | 500.000 |
| C | 2.0 | 2.0 | 320.000 |
| D | 3.0 | 2.0 | 380.000 |
| E | 2.5 | 2.0 | 350.000 |

**Novo Imóvel (Consulta)**: P = (2.2, 2.0)

#### Passo 1: Calcular as Distâncias Euclidianas de $P$ até cada Imóvel

$d(A, P) = \sqrt{(1.0 - 2.2)^2 + (1.0 - 2.0)^2} = \sqrt{(-1.2)^2 + (-1.0)^2} = \sqrt{1.44 + 1.00} = \sqrt{2.44} \approx \mathbf{1.56}$

$d(B, P) = \sqrt{(4.0 - 2.2)^2 + (3.0 - 2.0)^2} = \sqrt{(1.8)^2 + (1.0)^2} = \sqrt{3.24 + 1.00} = \sqrt{4.24} \approx \mathbf{2.06}$

$d(C, P) = \sqrt{(2.0 - 2.2)^2 + (2.0 - 2.0)^2} = \sqrt{(-0.2)^2 + (0)^2} = \sqrt{0.04 + 0} = \sqrt{0.04} = \mathbf{0.20}$

$d(D, P) = \sqrt{(3.0 - 2.2)^2 + (2.0 - 2.0)^2} = \sqrt{(0.8)^2 + (0)^2} = \sqrt{0.64 + 0} = \sqrt{0.64} = \mathbf{0.80}$

$d(E, P) = \sqrt{(2.5 - 2.2)^2 + (2.0 - 2.0)^2} = \sqrt{(0.3)^2 + (0)^2} = \sqrt{0.09 + 0} = \sqrt{0.09} = \mathbf{0.30}$

#### Passo 2: Selecionar os K=3 Vizinhos Mais Próximos

1. **Imóvel C** (Distância: $0.20$) $\rightarrow$ Preço: R$ 320.000
2. **Imóvel E** (Distância: $0.30$) $\rightarrow$ Preço: R$ 350.000
3. **Imóvel D** (Distância: $0.80$) $\rightarrow$ Preço: R$ 380.000

#### Passo 3: Agregação por Média Aritmética

$$ŷ = \frac{320.000 + 350.000 + 380.000}{3} = \frac{1.050.000}{3} = \mathbf{350.000}$$

**Resultado da Regressão**: O valor estimado para o novo imóvel é de **R$ 350.000**.
