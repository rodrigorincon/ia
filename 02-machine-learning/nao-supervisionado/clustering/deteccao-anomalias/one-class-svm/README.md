# ONE-CLASS SVM 

O One-Class SVM (Máquina de Vetores de Suporte para Uma Classe) é uma adaptação **não supervisionada** (ou semi-supervisionada) do algoritmo SVM clássico, projetada especificamente para **detecção de anomalias, detecção de novidades e outliers**.

Enquanto o SVM tradicional (SVC) busca encontrar um hiperplano que maximize a margem de separação entre duas ou mais classes distintas, o One-Class SVM aprende a fronteira de decisão utilizando **apenas dados de uma única classe "normal"**.

> O One-Class SVM cria um hiperplano ajustado ao redor da densidade dos dados normais no espaço transformado. Tudo o que fica dentro desse espaço é classificado como **normal (+1)**; qualquer ponto fora dele é ejetado como **Outlier / Anomalia (-1)**.

## Aplicações

- Detecção de fraudes
- Falha em máquinas
- Ataque a um servidor/rede
- Golpe financeiro ou lavagem de dinheiro
- Comportamento anômalo
- Princípio de infarto, AVC ou outro problema de saúde
- Detectar novas tendências e comportamentos (novidade positiva)
- Detecção de outliers

## O que Muda em Relação ao SVM Tradicional?

O One-Class SVM, por ser **não supervisionado**, não tem rótulos que separe os dados em grupos e as mudanças todas partem daí. Ele passa então a considerar **que todos os dados pertencem a uma única categoria** (normal) e **cria uma fronteira** a partir deles que **tudo que estiver fora dela é considerado anormal** (outlier, anomalia).

Essa fronteira pode ser feita de 2 formas: determinar um ponto de origem no hiperplano longe de todos os dados (geralmente o ponto 0) ou envolver todos os dados em uma esfera com o menor raio possível (o desafio passa a ser encontrar o centro da esfera e seu raio).

## A Representação Geométrica

Como o One-Class SVM não possui uma segunda classe para se afastar, ele precisa de um "ponto de referência" fictício para criar a margem. Existem duas abordagens diferentes mas que chegam exatamente no mesmo lugar se utilizar o Kernel RBF:

### 1. Afastamento da Origem

Nesta formulação, o algoritmo trata o **ponto zero em todas as dimensões (0, 0, ..., 0)** no espaço de atributos transformado pelo Kernel como se fosse a "única amostra da classe negativa". 

O objetivo é encontrar um hiperplano que maximize a distância entre a massa dos dados normais e a origem. Os dados normais ficam de um lado do hiperplano, enquanto a origem fica do outro.

```
                  [ Espaço Transformado pelo Kernel ]

                       ( Normal )   ( Normal )
                            ( * Support Vectors * )
  -------------------------[ Hiperplano / Fronteira ]-------------------------
                                   |
                                   |  Margem (ρ)
                                   v
                             ( Origem (0,0) ) -> Marcado como "Anomalia"
```

### 2. SVDD (Hiperesfera de Raio Mínimo)

Conhecida como Support Vector Data Description (SVDD), essa visão tenta encontrar a **hiperesfera de menor raio R** centrada em A que consiga envolver a maior quantidade possível de pontos de treino.

Quando aplicamos o **Kernel Gaussiano (RBF)**, todos os vetores são projetados na superfície de uma esfera unitária. Por isso, separar a massa de dados da origem (método 1) torna-se **matematicamente idêntico** a envolver os dados em uma hiperesfera!

## Novos Hiperparâmetros ($\nu$ (Nu) e Kernel)

No SVM tradicional, o parâmetro C controla a penalidade por invasão da margem. No One-Class SVM temos no lugar o hiperparâmetro $\nu$ (se pronuncia Nu). Esse parâmetro é maior que 0 e $\le$ 1 (não pode ser 0 nunca e pode ser igual a 1).

### 1. O Hiperparâmetro $\nu$ (Nu)

O $\nu$ desempenha 2 papeis no modelo:

1. **Limite Superior de Outliers:** Define a fração máxima de outliers que o modelo pode deixar fora da fronteira.
2. **Limite Inferior de Vetores de Suporte:** Define a fração mínima de pontos do dataset que atuarão como **Vetores de Suporte** para sustentar o formato da curva (fronteira).

**Exemplo:** Se você define $\nu = 0.05$, está dizendo que aceita que até 5% dos dados de treino sejam tratados como ruído (fora da margem) e que até 5% dos dados serão vetores de suporte para construir a fronteira.

### 2. A Necessidade do Kernel RBF (Radial Basis Function)

Diferente do SVM tradicional (onde um Kernel Linear costuma funcionar bem para dados linearmente separáveis) o **One-Class SVM quase sempre exige o Kernel RBF**. 

Se usarmos um Kernel Linear, o hiperplano será uma reta/plano rígido tentando separar os pontos da origem. Isso gera uma fronteira extremamente fraca que não envelopa os dados. O Kernel RBF permite criar **fronteiras de decisão não linear** ao redor da densidade dos dados.

Escolher o hiper-parâmetro gama para o RBF se torna essencial para um bom modelo.

- **$\gamma$ (Gama) Alto:** A fronteira se ajusta excessivamente a cada ponto individual (overfitting). Gera "ilhas" fechadas demais.
- **$\gamma$ (Gama) Baixo:** A fronteira torna-se muito suave e abrangente (underfitting) Considera anomalias como normais.

## Matemática

### 1. O Problema Primal

O One-Class SVM resolve o seguinte problema de otimização convexa:

$$\min_{w, \xi, p} \frac{1}{2} \|w\|^2 + \frac{1}{\nu N} \sum_{i=1}^{N} \xi_i - p$$

Sujeito às restrições:

$$\langle w, \Phi(x_i) \rangle \ge p - \xi_i, \quad \xi_i \ge 0, \quad \forall i = 1, ..., N$$

Onde:
- w é o vetor de pesos no espaço de atributos.
- $\rho$ (Rho) é o deslocamento (offset/margem) em relação à origem.
- $\xi_i$ são as variáveis de folga para permitir que alguns pontos violem a fronteira.
- N é o número total de amostras de treino.

### 2. A Função de Decisão Dual

Após resolver o problema dual utilizando Multiplicadores de Lagrange ($\alpha_i$), calculamos a função de decisão para qualquer novo ponto x:

$$f(x) = \text{sign} ( \sum_{i=1}^{N} \alpha_i K(x_i, x) - \rho )$$

- Se $f(x) \ge 0 \implies \mathbf{+1}$ **(Inlier / Dado Normal)**
- Se $f(x) < 0 \implies \mathbf{-1}$ **(Outlier / Anomalia)**

## Passo-a-Passo

1. **Pré-processamento (Padronização Z-Score):**
   - Como o algoritmo se baseia em distâncias e produto interno (Kernel), os dados **devem obrigatoriamente ser normalizados**.

2. **Mapeamento via Kernel:**
   - Aplica-se a função de Kernel escolhida (ex: RBF) para projetar os dados normais em um espaço de alta dimensão.

3. **Otimização de Lagrange / SMO:**
   - Encontra-se o vetor de multiplicadores de Lagrange $\alpha$ e o limiar p que maximizam a margem em relação à origem, respeitando as restrições impostas por $\nu$ (porcentagem de limite máximo de outliers).

4. **Identificação dos Vetores de Suporte:**
   - Pontos com $\alpha_i > 0$ tornam-se os **Vetores de Suporte**. Eles ficam exatamente na borda da densidade de dados normais e são os únicos necessários para armazenar o modelo.

5. **Inspecionar e Avaliar:**
   - Para novos dados de teste $x_{\text{novo}}$, calcula-se $f(x_{\text{novo}})$. Pontos que caem fora da margem sustentada pelos vetores de suporte recebem a classe -1.

## Exemplo

Imagine um sistema de monitoramento de transações bancárias com as transações de um de cliente.

### Base de Treinamento (Apenas Transações Normais):

| Transação | Horário Relativo ($X_1$) | Valor ($X_2$) |
| :--- | :--- | :--- |
| **T1** | $0.1$ | $10$ |
| **T2** | $0.2$ | $12$ |
| **T3** | $0.15$ | $11$ |
| **T4** | $0.3$ | $15$ |

1. **Treinamento:** O One-Class SVM mapeia esses pontos via Kernel RBF e cria uma fronteira circular ao redor do cluster central $(X_1 \approx 0.18, X_2 \approx 12)$.
2. **Definição de p:** O limiar p é ajustado com base no $\nu$ escolhido (ex: $\nu = 0.01$).
3. **Teste de Novas Transações:**
   * **Nova Transação A:** $(X_1 = 0.2, X_2 = 13) \implies$ Fica dentro do envelope. $f(A) = +1$ **(Normal)**.
   * **Nova Transação B (Tentativa de Fraude):** $(X_1 = 3.5, X_2 = 5000) \implies$ Fica muito distante do envelope de densidade. $f(B) = -1$ **(Anomalia Detectada)**.

## PREMISSAS

- **Maioria de Dados Normais no Treino:** O modelo pressupõe que a base de treino seja **quase exclusivamente por dados normais** (pode conter uma taxa residual de ruído controlada por $\nu$).
- **Necessidade de Padronização:** Como calcula distâncias euclidianas no espaço transformado pelo Kernel, variáveis em escalas diferentes distorcem a fronteira.
- **Atributos Numéricos Contínuos:** Exige que os dados X sejam numéricos e contínuos.

## QUANDO USAR

- **Cenários de Desbalanceamento Extremo (Assimetria Severa):** Quando você possui 99.9% de dados normais e 0.1% de anomalias (ex: detecção de fraudes financeiras, falhas raras em turbinas de avião).
- **Detecção de Novidades:** Quando as anomalias futuras podem assumir formatos imprevisíveis ou inéditos, impossibilitando treinar de um classificador supervisionado por não saber como pode ser a anomalia futura.
- **Monitoramento de Saúde de Sistemas:** Para aprender o padrão de funcionamento "saudável" de servidores, motores ou sensores e disparar alarmes ao menor desvio.

## QUANDO NÃO USAR

- **Quando Tem Amostras Rotuladas de Ambas as Classes:** Se você possui uma boa quantidade de exemplos das anomalias e rotuladas, prefira **SVC tradicional, XGBoost ou Random Forest**.

- **Bases Multimodais com Densidades Muito Diferentes:** Se os seus dados formarem vários clusters com densidades drasticamente diferentes, um único valor de $\gamma$ e $\nu$ pode falhar em envelopar todos os grupos adequadamente (prefira **Isolation Forest** ou **LOF - Local Outlier Factor**).

- **Volumes de Dados Massivos (N > 100.000):** O custo computacional do treinamento cresce entre $O(N^2)$ e $O(N^3)$ devido ao cálculo da matriz de Kernel.

## COMPARATIVO: SVM Tradicional vs. One-Class SVM vs. Isolation Forest

| Característica | SVM Tradicional (SVC) | One-Class SVM | Isolation Forest |
| :--- | :--- | :--- | :--- |
| **Abordagem** | Classificação Supervisionada | Fronteira de Densidade de 1 Classe | Isolamento por Particionamento de Árvores |
| **Rótulos Exigidos** | Duas ou mais classes | Apenas a classe normal | Nenhum rótulo (Não supervisionado) |
| **Eficácia com Alta Dimensão** | Excelente | Excelente (graças ao Kernel) | Moderada |
| **Sensibilidade a Escala** | Alta (Exige Padronização) | **Alta (Exige Padronização)** | Nenhuma (baseado em árvores) |
| **Complexidade de Tempo** | $O(N^2)$ a $O(N^3)$ | $O(N^2)$ a $O(N^3)$ | **$O(N \log N)$ (Muito mais rápido)** |
