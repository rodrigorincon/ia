# XGBoost

O XGBoost (Extreme Gradient Boost) é uma implementação otimizada, de alto desempenho e escalável do algoritmo de **Gradient Boosting**. Ele busca tornar os algoritmos de aprendizado supervisionado mais poderosos. Se o Random Forest evoluiu a Árvore de Decisão criando várias árvores independentes em paralelo (Bagging), o XGBoost leva o conceito de Boosting ao limite, construindo árvores de forma sequencial, onde cada nova árvore é criada especificamente para **corrigir os erros (resíduos) cometidos pelas árvores anteriores**.

## Gradient Boosting

É uma técnica de aprendizado de máquina baseada no conceito de aprendizado sequencial. Ele usa algum outro algoritmo de machine learning como seu motor principal (SVM, knn ou árvores de decisão) e executa em cima dele uma estratégia de gradiente para otimizá-lo. Ou seja, ele por si só não é um algoritmo pleno, mas sim uma abordagem de como usar os algoritmos que existem.

**Ele executa o algoritmo escolhido diversas vezes e em sequência**, usando o erro (resíduo) da etapa anterior como entrada para a nova etapa. Seu passo-a-passo é:

1. O algoritmo é executado

Na primeira rodada executa o algorimo normalmente.

2. Calcula-se o erro (tudo com os dados de treino)

Compara o resultado da IA com o valor real do dado e mede a diferença para cada dado. Para cada dado (linha) terá um erro diferente.

3. Repete o algoritmo usando o dado corrigido 

Ao invés de usar o dado original, usa o dado - erro

4. Corrige o retorno do algoritmo pelo erro das rodadas anteriores
	
$$Y_t = Y_{t-1} + \alpha * w_{t-1} * \text{erro}_t$$

Aonde:

- $\alpha$ é a taxa de aprendizado
- w é o peso que se dá para cada etapa anterior (pode-se dar maior peso para as mais atuais enquanto as primeiras valem menos)
- Y é o valor previsto em cada etapa
- Erro é o valor original menos a previsão da etapa atual ($Y_{\text{original}} - Y_t$)

Com isso a categoria atual é sempre a **categoria que o algoritmo previu nessa rodada corrigido pelo erro da última rodada**.

---

> A próxima iteração **não tenta prever a resposta final, mas sim corrigir os erros acumulados pelas etapas anteriores**.

Importante reinterar que todo o proesso **usa apenas os dados de treino**. Toda a parte de verificar o erro é medir o erro da regressão ou da categorização nos próprios dados de treino. Gradient Boost em nenhum momento usa dados novos.

Uma forma de visualizar o agoritmo é imaginar uma tacada de golfe. Na 1ª tacada, você tenta acertar o buraco a 100 metros e a bola para a 10 metros de distância (esse é o primeiro erro). Na 2ª tacada você faz a tacada de onde a bola parou e precisa apenas ajustar a força e a direção para cobrir os 10 metros que faltavam. O processo segue a cada nova tacada.

Como todo gradiente o algoritmo encerra se ultrapassar um limite de passos ou se o erro ficar muito curto. Apesar de focar na atualização dos valores Y, o gradient boost também executa uma derivada de sua função de custo para minimzar o erro. Pense nele como um gradiente descendente que usa um algoritmo de ML entre os gradientes.

Uma desvantagem dessa técnica é gerar **muito overfitting**, pois está repetidamente buscando os valores de treino ao tentar sempre minimizar os erros.

---

### Exemplo

Estamos usando regressão para prever o salário de uma pessoa (Y) a partir da idade (X). Nossa taxa de aprendizado é 0,5.

Valores iniciais:

|Pessoa| Idade (X)| Salário (Y) |
|:---  | :--- 		| :---				|
| A    | 	20			|	2000		|
| B    |	30			|	4000		|
| C    |	50			|	9000		|

Na primeira rodada a IA deu os seguintes salários

- A: 5000
- B: 4000
- C: 5000

Portanto o erro da etapa 1 é:

- A: 2000 - 5000 = -3000
- B: 4000 - 4000 = 0
- C: 9000 - 5000 = 4000

O algoritmo da etapa 2 usa como Y dos dados os erros da etapa anterior:

|Pessoa| Idade (X)| Salário ($Y_1$) |
|:---  | :--- 		| :---				|
| A    | 	20			|	-3000		|
| B    |	30			|	0		|
| C    |	50			|	4000		|

**A 2ª etapa treina com essa tabela, usando os erros, não mais o valor real**. Digamos que a IA retornou esses valores:

- A: -2000
- B: -2000
- C: 4000

Agora corrigimos a saída da IA pela taxa de aprendizado (e pelo peso caso haja).

- A = 5000 (previsão da rodada anterior) + 0.5 * (-2000) (previsão dessa rodada) = 4000
- B = 0 + 0.5 * (-2000) = -1000
- C = 5000 + 0.5 * 4000 = 7000

Portanto o erro da etapa 2 é:

- A: 2000 - 4000 = -2000
- B: 4000 + 1000 = 5000
- C: 9000 - 7000 = 2000

## Diferença para o Random Forest

Para entender o XGBoost, vale relembrar a diferença fundamental em relação ao Random Forest:

- **Random Forest (Bagging):** Várias árvores **independentes** treinadas em paralelo. A previsão final é o voto da maioria ou a média simples. Reduz a **variância** (overfitting).
- **Gradient Boosting (Boosting):** Árvores **dependentes** construídas em sequência. Cada árvore aprende com os resíduos da soma das árvores anteriores. Reduz o **viés** (underfitting).

```
[Entrada x] ──> Árvore 1 ──> Previsão 1 ──> Resíduo 1 (Erro)
                                                 │
                                                 ▼
            Árvore 2 (Treinada com o Resíduo 1) ──> Previsão 2 ──> Resíduo 2
                                                                       │
                                                                       ▼
                                  Árvore 3 (Treinada com o Resíduo 2) ──> Previsão 3 ...
```

## Extreme Gradient Boosting

O **XGBoost ("Extreme")** aprimora esse processo tradicional através de avanços matemáticos e computacionais:

1. **Otimização por Gradiente de Segunda Ordem:** Enquanto o Gradient Boosting padrão utiliza apenas a primeira derivada (gradiente) da função de perda, o XGBoost usa a **primeira derivada (Gradiente - g)** e a **segunda derivada (Hessiana - h)** (expansão de Taylor de 2ª ordem). Isso permite uma convergência muito mais rápida e precisa em direção ao mínimo global.
2. **Regularização Embutida:** Diferente do Boosting comum, o XGBoost inclui termos de penalização L1 (Lasso) e L2 (Ridge) na própria função de custo do modelo. Isso **evita o overfitting característico do boosting**.
3. **Processamento Paralelo e em Bloco:** Embora o algoritmo seja conceitualmente sequencial (uma etapa depende da anterior), a **alguns algoritmos conseguem paralelizar a execução do algoritmo em si, não a parte sequencial**.
4. **Sparsity-Aware (Tratamento de Dados Esparsos/Ausentes):** O XGBoost possui um algoritmo nativo para aprender a melhor "direção padrão" para tratar dados nulos.

## Aplicação nos Paradigmas do Aprendizado de Máquina

Apesar de o XGBoost ser fundamentalmente um algoritmo de **Aprendizado Supervisionado**, seus conceitos e arquitetura podem ser estendidos ou integrados aos demais paradigmas:

### Aprendizado Supervisionado (Uso Nativo)
É onde o XGBoost brilha nativamente, pois exige um sinal claro de supervisão (rótulo Y ou alvo contínuo) para calcular a função de perda e seus resíduos.
- **Classificação Binária e Multiclasse:** Previsão de churn, detecção de fraudes, diagnósticos médicos.
- **Regressão:** Previsão de preços de imóveis, demanda de estoque, séries temporais (com engenharia de *lag features*).
- **Rankeamento:** Ordenação de resultados de busca, recomendações baseadas em rankings (ex: XGBoost com função de perda `rank:pairwise` ou `rank:ndcg`).

### Aprendizado Não Supervisionado (Uso Indireto / Híbrido)
O XGBoost **não realiza** agrupamentos ou redução de dimensionalidade de forma nativa e isolada, pois não possui uma estrutura de rótulo Y para calcular resíduos. No entanto, é amplamente utilizado em pipelines não supervisionados:
- **Detecção de Anomalias Pseudo-Supervisionada:** Dados não rotulados são submetidos a algoritmos como Isolation Forest ou One-Class SVM para gerar rótulos sintéticos de "normal vs anômalo". Em seguida, o XGBoost é treinado para criar um classificador de anomalias escalável e explicável.
- **Apredizado Semi-Supervisionado:** Treina-se o XGBoost com a fração de dados rotulados, prevê-se os rótulos dos dados não rotulados com alto grau de confiança e adiciona-se esses dados no re-treinamento iterativo.

### Aprendizado por Reforço (Reinforcement Learning - RL)
O XGBoost **não é um agente de RL**, mas atua como um **Aproximador de Funções** dentro do ciclo de decisão de algoritmos por reforço:
- **Aproximação da Função Q (Q-Learning de Tabelas para Ambientes Contínuos):** Em vez de utilizar Redes Neurais Profundas (DQN), o XGBoost pode ser usado como o modelo que prevê o retorno esperado Q(s, a) dado um estado s e uma ação a.
- **Sistemas de Recomendação Dinâmicos:** Em problemas de *Multi-Armed Bandits*, o XGBoost estima a taxa de clique/recompensa para cada ação (ex: exibir determinado anúncio) com base no contexto do usuário e atualiza as estimativas conforme novas recompensas retornam.

## Vantagens e Desvantagens do XGBoost

### Vantagens

- **Desempenho de Ponta em Dados Estruturados**
- **Controle de Overfitting Nativo:** Possui regularização L1 ($\alpha$) e L2 ($\lambda$) incorporada na função de otimização, impedindo que as árvores cresçam excessivamente.
- **Tratamento Nativo de Missing Values:** Não exige imputação prévia (como Média, Mediana ou KNN). O modelo aprende automaticamente para qual nó enviar valores ausentes para otimizar o ganho de informação.
- **Alta Velocidade de Treinamento e Otimização:** Graças à estrutura de dados em blocos e à aproximação por histograma (*hist tree method*), é ordens de grandeza mais rápido que o Gradient Boosting tradicional.
- **Flexibilidade de Funções de Custo:** Permite ao usuário definir **funções de perda customizadas** (desde que possuam primeira e segunda derivadas contínuas).

### Desvantagens

- **Sensível a Hiperparâmetros:** Ao contrário do Random Forest (que funciona muito bem com as configurações padrão), o XGBoost exige ajuste fino de vários hiperparâmetros (`learning_rate`, `max_depth`, `subsample`, `colsample_bytree`, `gamma`, etc.) para atingir alta performance sem sobreajustar.
- **Risco de Overfitting Maior que o Random Forest:** Por focar sequencialmente na correção dos erros, ele pode acabar decorando o ruído dos dados de treino se a taxa de aprendizado (`learning_rate`) for muito alta ou o número de árvores (`n_estimators`) for excessivo.
- **Caixa Preta (Difícil Interpretação Direta)** 
- **Ineficiente para Dados Não Estruturados:** Não é adequado para imagens, áudio ou texto bruto (onde arquiteturas de Deep Learning e Transformers dominam).
- **Consumo de Memória:** Para datasets massivos, guardar a estrutura de blocos e matrizes de gradiente pode exigir quantidade significativa de memória RAM.

## 4. Quando Faz e Não Faz Sentido Usá-lo

```
                            ┌────────────────────────┐
                            │    Seu Dataset é...    │
                            └───────────┬────────────┘
                                        │
           ┌────────────────────────────┴────────────────────────────┐
           ▼                                                         ▼
   [Dados Tabulares/Bancos]                                 [Texto / Imagem / Áudio]
           │                                                         │
           ├─► Requer alta precisão? ──► [XGBoost]                   └─► [Deep Learning / Transformers]
           │
           ├─► Precisa de um baseline rápido
           │   ou resiliência total a tuning? ──► [Random Forest]
           │
           └─► Exige explicabilidade regulatória
               estrita (ex: Regra SE/ENTÃO)? ──► [Árvore de Decisão / Regressão Linear]
```

### Quando FAZ SENTIDO usar o XGBoost?

1.  **Datasets Tabulares Estruturados:** Dados provenientes de bancos de dados relacionais, planilhas, arquivos CSV/Parquet contendo variáveis numéricas e categóricas mistas.
2.  **Foco Principal em Precisão do Modelo:** Quando a métrica de desempenho (AUC, F1-Score, RMSE) for a maior prioridade do projeto.
3.  **Presença de Dados Ausentes:** Quando o dataset possui lacunas estruturais que seriam difíceis de imputar sem gerar viés artificial.
4.  **Problemas com Desbalanceamento de Classes:** Através de parâmetros como `scale_pos_weight`, o XGBoost ajusta o peso dos gradientes para dar atenção especial à classe minoritária.
5.  **Dados de Médio a Grande Porte:** Datasets com dezenas de milhares a alguns milhões de linhas onde uma árvore simples seria insuficiente e modelos estatísticos clássicos teriam alto viés.

### Quando NÃO FAZ SENTIDO usar o XGBoost?

1.  **Dados Não Estruturados (Visão Computacional, PNL, Áudio):** O XGBoost não consegue capturar dependências espaciais (como redes convolucionais) ou contextuais sequenciais profundas (como modelos baseados em *Attention*).
2.  **Datasets Extremamente Pequenos (Ex: < 100-500 amostras):** O poder do boosting em aprender resíduos fará com que ele decore o ruído muito rapidamente. Nesses casos, modelos mais simples (Regressão Linear/Lógica, Naive Bayes ou Random Forest com poucas árvores) performam melhor.
3.  **Ambientes de Extrema Baixa Latência / Dispositivos Embarcados (Edge):** Avaliar centenas de árvores sequenciais no momento da inferência pode ser mais lento do que uma simples multiplicação de matrizes de um modelo linear ou de uma pequena rede neural.
4.  **Quando a Explicabilidade Direta é uma Exigência Legal Rígida:** Se o seu modelo precisa ser auditado por um órgão regulador que exige um fluxograma simples e totalmente transparente (ex: concessão de crédito em certos mercados), uma **Árvore de Decisão individual** ou uma **Regressão Logística** serão exigidas.
5.  **Pouco Tempo para Ajuste de Parâmetros:** Se você precisa de um modelo rápido, estável e que entregue resultados razoáveis sem a necessidade de passar horas buscando hiperparâmetros, o **Random Forest** costuma ser uma escolha inicial mais simples e segura.