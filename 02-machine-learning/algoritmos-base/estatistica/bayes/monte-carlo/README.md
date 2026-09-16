# MÉTODO DE MONTE CARLO

É um grupo de algoritmos que utilizam **amostragem aleatória repetida** para obter resultados numéricos determinísticos ou estimar quantidades matemáticas complexas (como integrais de alta dimensão, esperanças e distribuições de probabilidade) que seriam intratáveis ou impossíveis de calcular de forma analítica. 

Ou seja, são **métodos que calculam operações matemáticas impossíveis de fazer por vias comuns** (ex: integrais e distribuições de probabilidade) ou **calcular números sem nenhum acaso e retorne sempre os mesmos valores**.

Em inteligência artificial o Método de Monte Carlo **não é um modelo preditivo** por si só, mas sim um **paradigma de inferência, amostragem e otimização estocástica** que atua como o **motor de simulação** para algoritmos de busca, aprendizado por reforço, modelos variacionais e redes neurais Bayesianas.

Para se ter em mente, o método substitui o cálculo exato de uma integral contínua complexa sobre várias variáveis X pela **média aritmética de amostras geradas aleatoriamente a partir de uma distribuição de probabilidade**.

## História do nome

Pode ser chamado de Método ou Simulação de Monte Carlo. Foi criado durante a 2ª guerra mundial (durante o projeto Manhatan) por John Von Newmann e um outro cara para melhorar a tomada de decisões sob condições incertas. O nome é em homenagem a um famoso cassino na cidade de Mônaco. A associação se deve a aleatoriedade ser um pilar do método e lembrar jogo de roletas.

## Amostragem aleatória repetitiva

"Amostragem aleatória repetitiva" significa que ele pega diversas amostras de dados, não tendo nenhum problema em repetir algum dado nessas repetições.

Exemplo: tenho mil dados sobre o clima. Pego 100 e calculo o que eu quero saber (média, mediana, regressão, teste de hipótese...), devolvo os 100 dados pro grupo total e pego mais 100 (sem me importar se vai repetir dado). Calculo novamente o que quero saber e repito essa ação N vezes. Ao final terei, a partir da minha amostra de mil, N sub-amostras de 100 (e é a partir delas que trabalharei).

### Por que usar várias amostras menores ao invés de 1 grande?

O motivo vem do Bootstrap e da lei dos grandes números. Ao usar uma única amostra teremos um nível de confiança e uma margem de erro para trabalhar. Ao fazer a medição com sub-amostras (amostras menores tiradas da amostra maior) em tese teríamos um nível de confiança ainda menor. Porém ao fazer milhares de medições em grupos pequenos temos uma distribuição desse dado. A lei dos grandes números nos garante que essa distribuição das milhares de mini amostras é a distribuição real da população e a métrica medida é muito próxima da métrica real da população. Esse processo se chama Bootstrap.

Em resumo, fazemos Bootstrap na amostra para reduzir ao máximo a margem de erro e chegar o mais próximo possível do valor verdadeiro. Se repetirmos a opração infinitas vezes teremos exatamente a métrica real, porém fazemos muitas e muitas vezes para já chegar perto o suficiente.

## Glossário

### Lei dos Grandes Números

É o pilar conceitual do Monte Carlo. É ele que garante que a média de milhares de amostras convergem para o valor da população e que isso ocorre para qualquer métrica (média, desvio, regressão, teste de hipótese...). `Ela é que justifica a substituição do cálculo infinitesimal por operações aritméticas iterativas`.

**Objetivo**: Garantir a precisão e a convergência do estimador estocástico para o valor real.

### Processo Estocástico

É o processo de mapear e descobrir o comportamento de uma população a partir da amostra. Para tanto ele sorteia um pedaço da amostra diversas vezes e as analisa. Juntando todas as análises ele consegue mapear toda a população. Ou seja, o `processo estocástico é o motor do Monte Carlo` (que é o motor de diversos sistemas de simulação) e se baseia na lei dos grandes números.

**Objetivo**: Mapear o comportamento global de um sistema complexo através do sorteio e da avaliação de um número finito de pontos amostrais.

### Espaço de Configuração

É o conjunto de todos os valores possíveis que um sistema pode ter.

### Amostragem Estocástica

É a formalização da geração de sequências de números aleatórios (ou pseudo-aleatórios) $X_1, X_2, ..., X_N$ seguindo uma distribuição de  probabilidade p(x). É como números aleatórios são gerados garantindo que estão todos dentro do nosso espaço de configuração e seguindo a distribuição.

### Simulação (Rollout)

É cada iteração do algoritmo.

## Descrição Resumida

> ## Monte Carlo é trocar operações matemáticas impossíveis ou gerar sequências de números fixos por Bootstrap.

## Matemática

### O Estimador da Média de Monte Carlo ($\hat{I}_N$)

Considere que você quer calcular o valor de uma função f(x) em relação a uma distribuição de probabilidade p(x), o que equivale a resolver a integral:

$$I = \int_{\Omega} f(x) p(x) \, dx$$

O estimador não-viesado de Monte Carlo para $I$ utilizando N amostras $X_1, X_2, \dots, X_N$ sorteadas de p(x), é dado por:

$$\hat{I}_N = \frac{1}{N} \sum_{i=1}^{N} f(X_i)$$

Ou seja, trocamos uma integral impossível pelo somatório da função e dividimos pelo número de repetições (média dos valores de f(x)).

### Propriedades fundamentais do Estimador de Monte Carlo

1. **Não-viesado:** O valor esperado do estimador é exatamente o valor real da integral
2. **Consistência:** Pela Lei Forte dos Grandes Números, $\lim_{N \to \infty} \hat{I}_N = I$ com probabilidade 1.

### A Variância do Estimador e o Erro Padrão

A variância do estimador $\hat{I}_N$ quantifica a incerteza ou ruído da estimativa e é expressa por:

$$\text{Var}(\hat{I}_N) = \text{Var}\left(\frac{1}{N} \sum_{i=1}^{N} f(X_i)\right) = \frac{1}{N^2} \sum_{i=1}^{N} \text{Var}(f(X_i)) = \frac{\sigma^2}{N}$$

Onde $\sigma^2 = é a variância da função sob a distribuição $p(x)$. Ou seja, a variância também pode ser estimada igualmente por esse método.

O Erro Padrão (e) da estimativa também pode ser estimada igualmente:

$$e = \sqrt{\text{Var}(\hat{I}_N)} = \frac{\sigma}{\sqrt{N}}$$

## Imunidade à Maldição da Dimensionalidade na Taxa de Erro

Uma das propriedades mais poderosas do Método de Monte Carlo é que sua taxa de erro é de ordem $O(1/\sqrt{N})$. Ou seja, depende só do número de amostras N.

Diferente das técnicas de quadratura numéricas determinísticas (como a regra dos Trapézios ou de Simpson), cujo erro cresce com o N e exponencialmente com o número de variáveis X usadas ($O(N^{-k/X})$), **o erro do Método de Monte Carlo depende exclusivamente do número de amostras N e da variância $\sigma^2$, sendo completamente independente da variáveis X**. Ou seja, podemos usar com qualquer número de variáveis X (colunas) que não impacta na qualidade da resposta.

### Técnicas de Redução de Variância

Porém apesar de absurdamente melhor que os métodos determinísticos, essa taxa de erro ainda não é perfeita. Como a taxa $O(1/\sqrt{N})$ exige quadruplicar o número de amostras N para reduzir o erro pela metade, se tivermos muitos N o processamento explode ainda assim. 

Por isso, utilizam-se técnicas de **Redução de Variância** para diminuir o parâmetro $\sigma$:

1. **Amostragem por Importância:** 

Muda-se a distribuição de amostragem de p(x) para uma distribuição alternativa q(x) que concentra amostras nas regiões onde |f(x)|p(x) é grande. A integral é reescrita como:
   
$I = \int_{\Omega} f(x) \frac{p(x)}{q(x)} q(x) \, dx = E_{x \sim q(x)} [ f(x) w(x) ]$
   
Onde $w(x) = \frac{p(x)}{q(x)}$ são os **pesos de importância**. Se $q(x) \propto |f(x)|p(x)$, a variância do estimador pode ser reduzida a zero.

---

2. **Variáveis Antitéticas:**

Gera-se pares de amostras negativamente correlacionadas $(X_i, X_i')$. Se a correlação entre $f(X_i)$ e $f(X_i')$ for negativa, a variância delas se cancelam, diminuindo a variância total:
   
$Var(\frac{f(X_i) + f(X_i')}{2}) = \frac{1}{4} [ Var(f(X_i)) + Var(f(X_i')) + 2Cov(f(X_i), f(X_i')) ]$

---

3. **Amostragem Estratificada:**

Divide-se todo o espaço de configuração (De quanto a quanto os valores podem ir) em fatias e tira amostras de cada fatia, eliminando a variação entre estratos.

## PARA QUE SERVE

O Método de Monte Carlo é indispensável em qualquer domínio que enfrente **alta dimensionalidade** (muitas variáveis X), **incerteza estocástica** ou **ausência de equações em forma fechada**.

### Finanças Quantitativas e Engenharia Financeira
- **Cenário:** Precificação de ações e gestão de risco de portfólios.
- **Como é usado:** Simula-se milhares de trajetórias futuras possíveis para o preço de ativos usando Movimento Browniano Geométrico (SDEs).

### Física Computacional, Nuclear e de Partículas
- **Cenário:** Transporte de nêutrons em reatores nucleares, física de altas energias, meteorologia e mecânica estatística quântica.
- **Como é usado:** Usado no CERN pata modelar a trajetória e a colisão de partículas individuais, amostrando distâncias livres e ângulos de espalhamento.

### Computação Gráfica e Renderização Fotorrealista
- **Cenário:** Iluminação em cenas 3D com materiais reflexivos, refratários e sombras suaves.
- **Como é usado:** Algoritmos de **Path Tracing** e **Ray Tracing estocástico** disparam raios de luz a partir da câmera e amostram aleatoriamente as direções de reflexão e refração nas superfícies.

### Engenharia, Confiabilidade e Análise de Risco
- **Cenário:** Avaliar probabilidade de falha em estruturas (pontes, barragens, aeronaves) quando recebem cargas incertas.
- **Como é usado:** Amostra-se variáveis de entrada aleatórias (resistência do material, vento, tremores) e calcula-se a porcentagem de simulações em que a estrutura colapsa.
- **Aplicação:** Testes de estresse de redes elétricas, análises de segurança aeroespacial e estudos hidrológicos de enchentes.

## RELAÇÃO COM MODELOS DE IA: QUEM USA, COMO E POR QUE

Monte Carlo é a espinha dorsal de algoritmos que precisam **tomar decisões sob incerteza** extrema ou otimizar **espaços de busca gigantescos** que crecem em forma de análise combinatória.

### Busca em Árvore Monte Carlo (Monte Carlo Tree Search - MCTS)

- **Quem usa:** jogos como AlphaGo, AlphaZero e Leela Chess Zero, arquiteturas de raciocínio lógico em LLMs.
- **Como usa:** Combina a exploração de uma árvore de decisões com simulações de Monte Carlo (rollouts aleatórios ou guiados por redes neurais). O MCTS executa 4 fases iterativas:

1. **Seleção:** Navega pela árvore usando critérios de limite de confiança superior.
2. **Expansão:** Adiciona um novo nó folha à árvore.
3. **Simulação (Rollout):** Executa uma simulação estocástica (Monte Carlo) até o fim do jogo/tarefa a partir do novo nó para estimar o valor final.
4. **Retropropagação (Backpropagation):** Atualiza as estatísticas de vitória/recompensa de todos os nós visitados na trajetória.

- **Por que usa:** A árvore completa de jogos como Go ou Xadrez possui milhões de ramificações, tornando a busca exaustiva (Minimax) inviável. Monte Carlo permite avaliar a qualidade de uma posição **amostrando seletivamente** os caminhos mais promissores. Em LLMs exploram multiplos caminhos para onde pode levar um raciocínio antes de dar uma resposta definitiva.

### Aprendizado por Reforço Baseado em Monte Carlo (Monte Carlo RL)

- **Quem usa:** Algoritmos de On-Policy e Off-Policy clássicos, otimização de políticas em robótica, RL com feedback humano.
- **Como usa:** Em contraste com a Programação Dinâmica, que exige o conhecimento perfeito do modelo de transição do ambiente, o Monte Carlo aprende as funções de valor diretamente dos dados de amostragem
- **Por que usa:** Não exige conhecimento prévio sobre as leis da física ou regras explícitas do ambiente, basta interagir com o ambiente e calcular a média dos retornos observados.

### Autoencoders Variacionais (VAEs) e Otimização Variacional

- **Quem usa:** Autoencoders Variacionais (VAEs), DALL-E, modelos generativos, redes neurais Bayesianas.
- **Como usa:** Usa-se para calcular a esperança da distribuição variacional.
- **Por que usa:** Permite treinar redes neurais generativas com variáveis contínuas via gradiente descendente estocástico (SGD).

### Monte Carlo Dropout (MC Dropout) para Estimativa de Incerteza

- **Quem usa:** Redes Neurais Bayesianas, IA Médica (diagnóstico por imagem), Condução Autônoma, Sistemas Críticos de Decisão.
- **Como usa:** O Dropout (desligar aleatoriamente alguns neurônios em cada passo) é tradicionalmente usado apenas durante o treinamento como regularizador. No MC Dropout, o Dropout é mantido ativo no momento da inferência (teste). A rede realiza N passadas para frente para o mesmo dado de entrada, gerando N saídas ligeiramente diferentes. A variância entre essas N saídas fornece uma estimativa da incerteza do modelo.
- **Por que usa:** Transforma qualquer rede neural treinada com Dropout em uma aproximação prática de um Processo Gaussiano ou Rede Neural Bayesiana sem custo de re-treinamento.

### Algoritmos MCMC e Modelos Generativos de Difusão

- **Quem usa:** Stable Diffusion, Midjourney, DALL-E, Inferência Bayesiana.
- **Como usa:** Calcular integrais de normalização (P(X)).

### Avaliação e Métricas de Modelos Gerativos

- **Quem usa:** Validação de LLMs, avaliação de GANs e modelos de difusão (métrica FID).
- **Como usa:** Estima-se a divergência de distribuições de alta dimensão extraindo amostras e calculando distâncias estocásticas via estimadores Monte Carlo.
- **Por que usa:** O espaço de dados reais (imagens/textos) é contínuo e infinito; a amostragem Monte Carlo é a única forma viável de estimar a fidelidade e a diversidade gerativa.

## PREMISSAS

Para que o Monte Carlo seja válida as seguintes premissas devem ser atendidas:

1. **Geração Valida de Números Aleatórios:** Acesso a um gerador de números pseudo-aleatórios de alta qualidade.
2. **Variância Finita ($\sigma^2 < \infty$):** A função f(x) integrada deve possuir variância finita sob a distribuição p(x). Caso contrário, o Teorema do Limite Central falha e a taxa de convergência se desfaz.
3. **Amostragem Representativa:** O suporte da distribuição de amostragem q(x) deve cobrir todo o suporte de p(x) onde $f(x) \neq 0$.
4. **Independência das Amostras (sem multicolinearidade):** As amostras $X_i$ devem ser independentes (ou, no caso de MCMC, ter tempo de mistura suficiente para garantir amostragem da distribuição estacionária).

## ENTRADAS E SAÍDAS

O que ele recebe de entrada:

- **Domínio ou Espaço de Estados ($\Omega$):** A região limite da busca ou da integral.
- **Distribuição de Amostragem p(x):** A densidade de probabilidade a partir da qual os pontos são sorteados.
- **Função Alvo / Modelo de Avaliação f(x):** O código, equação ou simulador executado para cada amostra.
- **Tamanho da Amostra (N):** O número total de simulações/iterações a executar.

O que ele dá como saída:

- **Estimativa $\hat{I}_N$:** O valor médio aproximado da integral, esperança ou recompensa.
- **Erro Padrão / Variância Amostral:** A medida de incerteza da estimativa obtida.
- **Intervalo de Confiança:** A margem de erro para um nível de confiança (ex: 95%).
- **Histograma:** A representação discreta da densidade de probabilidade da variável de saída.

## COMO FUNCIONA

A execução clássica de um experimento de Monte Carlo segue um ciclo de 5 etapas:

1. **Definição do Domínio e das Variáveis Aleatórias:**
   - Mapeia-se o problema em termos de entradas estocásticas e suas respectivas distribuições de probabilidade p(x).
2. **Geração de Amostras:**
   - Sorteiam-se N pontos independentes $X_1, X_2, ..., X_N$ do domínio de entrada utilizando técnicas de amostragem (Transformação Inversa, Box-Muller, rejection sampling).
3. **Avaliação Determinística:**
   - Computa-se o valor da função ou executa-se o simulador determinístico $f(X_i)$ para cada amostra $X_i$ individualmente.
4. **Média:**
   - Calcula-se a média aritmética dos resultados $f(X_i)$ para obter a estimativa pontual $\hat{I}_N$.
5. **Margem de Erro e Intervalo de Confiança:**
   - Calcula-se a variância amostral $s_N^2$ e o erro padrão $e = s_N / \sqrt{N}$.

## CRITÉRIOS DE CONVERGÊNCIA E ERRO

A precisão do Método de Monte Carlo é definida pela relação entre a variância e o volume de amostras:

- **Taxa Sub-linear de Redução do Erro:** Para reduzir o erro da estimativa por um fator de 10, é necessário multiplicar o número de amostras N por 100.
- **Critério de Parada:** As simulações costumam ser executadas iterativamente até que o erro padrão $s_N / \sqrt{N}$ caia abaixo de um limiar de tolerância pré-definido.
- **Efeito da Variância:** Se a função f(x) possui picos extremamente agudos ou eventos raros, a variância é enorme, exigindo o uso obrigatório de técnicas de redução de variância para obter convergência em tempo prático.

## O que fazer quando não converge

- Aumentar a quantidade de iterações (N). Porém precisa aumentar muito já que o erro é $\frac{1}{\sqrt{N}}$
- Ajustar o tamanho do passo (para MCMC)
- Revisar o gerador de números aleatórios
- Checar a média $\hat{I}_N$ ao longo das iterações para ver se ela oscila muito ou vai estabilizando.


## VARIAÇÕES DO MÉTODO DE MONTE CARLO

- **Markov Chain Monte Carlo (MCMC)**
  - Gera amostras correlacionadas onde o próximo ponto depende do estado atual através de uma Cadeia de Markov.
  - **Quando usar:** Quando a distribuição alvo p(x) é complexa e de alta dimensão.
- **Sequential Monte Carlo (SMC)**
  - Aplica amostragem por importância sequencial com etapas de reamostragem para rastrear distribuições de probabilidade que evoluem no tempo.
  - **Quando usar:** Rastreamento de alvos em tempo real, robótica (Slam) e filtragem de séries temporais não-lineares.
- **Multilevel Monte Carlo (MLMC)**
  - Combina simulações executadas em múltiplos níveis de resolução/discretização para balancear o custo computacional com a precisão.
  - **Quando usar:** Equações Diferenciais Estocásticas (SDEs) e equações diferenciais parciais aleatórias.
- **Quasi-Monte Carlo (QMC)**
  - Utiliza sequências pseudo-aleatórias para preencher o espaço amostral sem aglomerações aleatórias.
  - **Quando usar:** Finanças quantitativas e computação gráfica de média dimensão.

### Quando Usar Cada Uma (Resumo Prático)

- Integração de Alta Dimensão Padrão: Monte Carlo Clássico
- Distribuição Complexa e Não-Normalizada: Markov Chain Monte Carlo (MCMC)
- Séries Temporais e Sistemas Dinâmicos: Sequential Monte Carlo (SMC)
- Aumento da Taxa de Convergência em Média Dimensão: Quasi-Monte Carlo (QMC)
- Modelagem de Equações Diferenciais Estocásticas: Multilevel Monte Carlo (MLMC)
- Busca Combinatória e Jogos com Espaço de Estados Gigante: Monte Carlo Tree Search (MCTS)

## Exemplo

Queremos saber a área da curva X² de 0 a 10. Pelo método de Monte Carlo eu sei se x=10, x²=100, então irei trabalhar com a área do quadrado 10x100. pego N pontos nesse quadrado e vejo quantos deles estão dentro da área de x². Isso me dará a área da curva.

Peguei mil pontos, deles 400 pontos estavam dentro da árva e 600 fora. Portanto a área segundo Monte Carlo é de 400/1000 * área = 0.4 * 1000 = 400.

A área real é de 333.33, logo a simulação não chegou  tão perto do resultado.

Isso foi 1 simulação (N=1). Se fizemos essa simulação 500 vezes e tiramos a média dos resultados teremos algo próximo do valor real.

Nossa taxa de erro (erro padrão) será o desvio padrão dividido por raiz de N ($\frac{\sigma}{\sqrt{N}}$). Pegamos todos os 500 resultados, tiramos o desvio padrão deles e calculamos o erro padrão.