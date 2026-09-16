# REDES BAYESIANAS

É um modelo probabilístico que representa um conjunto de variáveis e suas dependências através de um grafo. Em machine learning é usado para **modelar incertezas e relações de causa e efeito** em um sistema complexo. É importante entender que **ela não é apenas uma "caixa preta" que prevê valores, mas sim um mapa estruturado do conhecimento humano (ou dos dados)**, permitindo entender como uma variável afeta a outra.

Para se ter em mente, o modelo não apenas prevê um resultado final. Ele permite que você brinque com os cenários: "E se o paciente tiver febre, como isso muda a probabilidade de ser gripe ou dengue?". É uma máquina de raciocínio lógico sob incerteza.

## Estrutura

Uma Rede Bayesiana é dividida em duas partes principais: a estrutura (o grafo) e os números (as probabilidades).

### O Grafo (esqueleto)

A rede é formada por um **Grafo Acíclico Direcionado (DAG)**.  Ou seja, o grafo é unidirecional e não pode haver ciclos dentro dele (A->B->C->A).

- **Nós:** Representam as variáveis X. Podem ser coisas observáveis ou hipóteses.
- **Arestas:** São as setas que ligam os nós. Elas representam a relação direta de influência ou causalidade. Uma seta de A -> B significa que A influencia B (A é "pai" de B).
- **Acíclico:** O grafo não pode ter loops. A causa não pode ser causada pelo próprio efeito.

### Tabelas de Probabilidade Condicional - CPTs (recheio)

Cada nó possui uma tabela interna que diz o quão forte é a relação entre ele e seus "pais" (os nós cujas setas apontam para ele).

Se o nó não tiver pais (um nó raiz), sua tabela contém apenas probabilidades a priori. Se tiver pais, a tabela mostra a probabilidade de cada estado do nó dado **todas as combinações possíveis** dos estados dos pais.

**Objetivo Geral**: Capturar a representação completa do mundo modelado usando muito menos memória do que calcular todas as combinações de variáveis de uma vez.

A rede bayesiana lembra de longe a lógica de predicados (como em Prolog), aonde definimos causas e consequências e tudo é definido por como as coisas se relacionam/afetam. Porém diferente da lógica de predicados aonde o programador precisa conhecer todas as relações previamente, a rede bayesiana as descobre olhando para os dados. Além disso ela também traz um nível de incerteza, dando a probabilidade de algo acontecer dado que outras coisas aconteceram. Muito melhor que os predicados que são determinísticos.

---

#### EXEMPLO

O nó raiz teria a probabilidade a priori "Probabilidade de sair para jogar bola em um dia qualquer" e ele representa a variável chuva. Seu filho teria a probabilidade "Probabilidade de sair para jogar bola dado que está chovendo" ou "não está chovendo".

Tabela raíz:

| Entrada A | Entrada B | P(sair) | P(não sair) |
|  :--:     |  :--:     |   :--:  |   :--:      |
|   -       |   -       |   0.7   |   0.3       |

Tabela filho:

| Chuva | P(sair) | P(não sair) |
|  :--: | :--:    |   :--:  |
|   Sim | 0.1     |   0.9   |
|   Não | 0.7     |   0.3   |

Outro nó tem 2 pais: chuva, e brigou com a esposa. Sua tabela teria as probabilidades "Probabilidade de sair para jogar bola dado que não está chovendo e não briguei com a mulher", "não está chovendo e briguei", "está chovendo e não briguei" e "está chovendo e briguei".

Tabela outro nó:

| Chuva | Briga | P(sair) | P(não sair) |
|  :--: | :--:  | :--:    |   :--:      |
|   Não | Não   |   0.7   |     0.3     |
|   Não | Sim   |   0.4   |    0.6      |
|   Sim | Não   |   0.1   |   0.9       |
|   Sim | Sim   |   0.01  |  0.99       |

## Quando Usar

As Redes Bayesianas brilham quando temos **informações incompletas** e precisamos tomar decisões racionais. Diferente de um modelo tradicional que precisa de todas as entradas preenchidas, a Rede Bayesiana **consegue prever coisas mesmo se faltar dado**. Ela também é **facilmente compreendida e explicável**, sendo junto com as árvores de decisão métodos mais fáceis de entender o que está acontecendo.

- **Diagnóstico Médico:** Variáveis para sintomas, doenças e resultados de exames. Dado que o paciente tosse (efeito), qual a probabilidade de ter pneumonia (causa)?
- **Análise de Risco (Finanças):** Avaliar a chance de inadimplência baseada no contexto econômico e no histórico do cliente.
- **Sistemas de Diagnóstico de Falhas:** Na engenharia para descobrir qual componente quebrou a partir de alertas no painel.
- **Bioinformática:** Mapeamento de redes regulatórias genéticas.

## Rede Bayesiana vs. Naive Bayes

O Naive Bayes (Bayes Ingênuo) é a versão mais simples, "burra" e restrita de uma Rede Bayesiana.

No **Naive Bayes** existe um nó central (a Classe) que aponta para todas as outras variáveis (Features). E a grande premissa é: **todas as features são completamente independentes umas das outras**. Ele acha que a palavra "dinheiro" e "urgente" em um email de spam aparecem de forma totalmente desconectada.

Na **Rede Bayesiana**, as relações entre as variáveis são respeitadas. Ela entende que "Chuva" afeta "Pista Molhada", que afeta "Acidentes". Ela modela o mundo real de forma muito mais complexa e interligada.

> Use o Naive Bayes apenas para problemas rápidos de classificação com muitos dados simples.

## Rede Bayesiana vs. Rede Neural Bayesiana (BNN)

A Rede Bayesiana é um grafo que mapeias as relações entre as variáveis. A rede neural bayesiana é uma rede neural profunda tradicional. Portanto ambos são duas coisas bem diferentes com estruturas totalmente diferentes.

A rede bayesiana foca em interpretabilidade e causalidade. Cada nó é uma variável do mundo real (ex: idade, pressão, salário).

A rede neural foca em padrões densos e os nós são apenas neurônios matemáticos sem sentido no mundo real. A diferença dela para redes neurais normais é que ao invés de cada "peso" (w) da rede ser um número fixo (ex: 0.5), o peso é uma **distribuição de probabilidade** (ex: uma curva normal). Isso serve para a Rede Neural conseguir dizer "não tenho certeza" quando se depara com dados anômalos.

## PREMISSAS

Para a Rede Bayesiana funcionar corretamente os dados precisam respeitar regras matemáticas rígidas:

- **Grafo Acíclico (DAG):** Não podem existir dependências circulares.
- **Propriedade de Markov Local:** A premissa de ouro. Um nó é independente de todos que não forem seus pais (seus antepassados distantes e ramos colaterais), dado o conhecimento sobre os seus pais imediatos. Ou seja, toda a influência do passado passa estritamente através dos pais. `Se você sabe a condição dos pais com 100% de certeza, saber sobre os avós não muda nada na sua previsão`.
  - Repare que a propriedade de Markov local lembra séries temporais com autocorrelação p=1, onde só o último dado afeta o atual.
- **Dados discretos:** A maioria das implementações padrão exige que as variáveis sejam discretas (Sim/Não, Baixo/Médio/Alto). Para trabalhar com variáveis contínuas, usa-se **Redes Bayesianas Gaussianas** ou deve-se segmentar os dados contínuos.

Para testar a propriedade de Markov local usa-se o **teste de independência condicional**. Porém como o grafo inteiro é construído seguindo essa premissa ela sempre dará certo. Ao invés de testá-la na rede final fazemos testes de qualidade padrão (BIC, log-loss, acurácia, precisão, F1-Score e matriz de confusão) na rede final para ver se ela realmente acerta.

### Teste de Independência Condicional

Testa se as variáveis são condicionalmente independentes dado as outras variáveis.

- H0: As variáveis X e Y **são independentes (não têm relação direta)** quando definimos o valor da variável Z. Ou seja, saber o valor de X não ajuda a prever o valor de Y se você já tem o valor de Z.
  - P(X $\cap$ Y | Z) = P(X | Z) * P(Y | Z)

- H1: As variáveis X e Y continuam dependentes mesmo após mudar a variável Z. Ou seja, existe uma relação entre X e Y que não é explicada apenas pela presença de Z.

O cálculo do p-valor é feito com o teste Qui-Quadrado usando o valor dessa equação e graus de liberdade igual ao número de categorias da variável Z.

## A MATEMÁTICA

A magia da Rede Bayesiana é a economia de cálculos através da **Independência Condicional** e do **Teorema de Bayes**.

### A Regra da Cadeia (Probabilidade Conjunta)

Se quisermos saber a probabilidade de todo o sistema acontecer ao mesmo tempo (ex: P(Chuva, Trânsito, Atraso, Acidente)), teríamos que calcular combinações astronômicas. Mas, graças ao grafo, a matemática diz que só precisamos multiplicar a probabilidade de cada nó dados os seus pais diretos.

$$P(X_1, X_2, ..., X_n) = \prod_{i=1}^{n} P(X_i | Pais(X_i))$$

Se "Atraso" só depende do "Trânsito", ignoramos as outras variáveis na hora de calcular sua tabela. Essa simplificação é o que torna o algoritmo viável para problemas complexos.

## Passo-a-Passo

A construção e uso da rede ocorrem em três fases distintas:

### Passo 1: Aprendizado da Estrutura (Construção do Grafo)

Aqui descobrimos quais variáveis se ligam a quais. Exitem 2 formas de se fazer esse passo:

1. **Abordagem Baseada em Restrições**: O algoritmo que faz essa execução é o **Algoritmo PC**. Ele roda centenas de testes estatísticos, pois testa todas as variáveis com todas as outras, o que o torna lento. Cresce de forma exponencial.
  - Todas as variáveis (nós do grafo) começam ligadas com todos os outros. 
  - Para cada variável testamos sua relação com todas as outras (via **teste qui-quadrado de independência ou correlação**) e removemos as ligações que não passarem. 
  - As arestas restantes fazem o teste de independência condicional e, caso seja, independentes ao adicionar uma 3ª variável, a aresta é removida. 
  - Busca-se ciclos e estruturas em V para remover ciclos e nós bidirecionais.

Essa opção é mais demorada mas testa todas as opções e dá um grafo ideal.

2. **Abordagem Baseada em Pontuação (Score-based)**: Evita o crescimento exponencial listando todos os grafos possíveis e expandindo apenas os mais promissores. Para isso usa o BIC como métrica de quão bom é o gráfico.
  - Cria um grafo inicial com todos os nós e sem nenhuma aresta.
  - Usa o algoritmo subida de encosta (Hill Climbing) fazer alterações minúsculas no grafo a cada passo (adicionar, remover e inverter a direção de uma aresta). Todas as alterações possíveis são testadas, criando uma árvore de possibilidades.
  - Calcula-se o BIC para cada alteração e segue pelo caminho com menor valor. O BIC usa verossimilhança e um termo de penalidade que evita overfitting.
  - O algoritmo para quando não há nenhum passo que dê um BIC menor que o atual.

Essa opção é mais rápido mas pode cair num máximo local ou ficar preso em vales.

---

#### Exemplo da abodagem por Score

Temos um grafo com 3 nós: fumar, câncer e tossa. O grafo começa sem aresta (nenhuma variável afeta a outra) com BIC 1500.

Fazemos todas as alterações possíveis (no caso, adicionar arestas). 

- Fumar -> câncer. BIC 1200
- Fumar -> tosse. BIC 1450
- Tosse -> câncer. BIC 1700
- Tosse -> fumar. BIC 2300
- Câncer -> fumar. BIC 2500
- Câncer -> tosse. BIC 2400

Seguimos pelo ramo fumar -> câncer pois tem o menor BIC (1200). Damos mais um passo: adicionar mais setas ou inverter a atual

- Câncer -> fumar (inverter a seta). BIC 2500
- Fumar -> tosse. BIC 1100
- Câncer -> tosse. BIC 950
- Tosse -> câncer. BIC 1500
- Tosse -> fumar. BIC 1800

Seguimos pelo ramo Câncer -> tosse. Damos mais um passo.

- Fumar -> tosse. BIC 980
- Tosse -> fumar. BIC 2000

Nenhuma opção é melhor que a atual, então encerramos.

---

### Passo 2: Aprendizado dos Parâmetros (Preenchendo as Tabelas)

Com o grafo pronto, precisamos das tabelas de probabilidades (CPTs).

- Se tivermos muitos dados, o algoritmo faz simples **contagem (Máxima Verossimilhança)**: De todas as vezes que choveu, quantas vezes houve trânsito? E coloca essa porcentagem na tabela.
- Para evitar tabelas com 0% (se um evento nunca ocorreu nos dados de treino, mas pode ocorrer), usa-se a **Estimativa Bayesiana** (como a Correção de Laplace), que adiciona "pesos fantasmas" para impedir certezas absolutas equivocadas.

### Passo 3: Inferência

Agora a rede está pronta. Inserimos um dado de treino (ex: o usuário marcou `Atraso = Sim`). O algoritmo propaga essa informação no grafo para atualizar as probabilidades de todas as outras variáveis.

- **Inferência Exata:** Métodos como Eliminação de Variáveis ou Árvore de Junção (Junction Tree). Eles calculam a matemática com precisão absoluta, mas explodem a memória se o grafo for gigante e interligado. **Usar apenas em grafos pequenos**.
- **Inferência Aproximada:** Quando o grafo é muito grande usa-se simulação estocástica como **MCMC (Monte Carlo com Cadeias de Markov)** ou **Amostragem de Gibbs**. O computador passeia aleatoriamente pelo grafo milhares de vezes jogando dados (literalmente) com as probabilidades viciadas das tabelas. No final, ele conta a porcentagem dos resultados para dar uma probabilidade aproximada.

Essa fase é nossa função de otimização, que vai corrigindo as probabilidades da tabela usando os dados de treino.

## MÉTRICAS DE QUALIDADE

Como a rede faz duas coisas diferentes (tem estrutura e também prevê), ela tem formas distintas de ser avaliada:

### Métricas da Qualidade da Estrutura

Servem para garantir que não fizemos um grafo cheio de setas inúteis.

- **BIC (Bayesian Information Criterion) e AIC:** São pontuações que medem quão bem o grafo se ajusta aos dados, mas **aplicam uma multa pesada** para cada seta (parâmetro) extra que o grafo tem. Quanto menor, melhor. Isso impede o overfitting na topologia.

### Métricas de Predição

Avalia se as conclusões dela estão certas para um nó alvo que queremos adivinhar (uma doença, por exemplo).

- **Log-Loss (Entropia Cruzada):** É a principal. Diferente da acurácia simples, a Log-Loss **pune o modelo pelo quão confiante ele estava no erro**. Se ele disse que tinha 99% de certeza que era Dengue e não era, a multa é altíssima.
- **Acurácia, Precisão, F1-Score, Matriz de confusão e AUC-ROC:** Usadas normalmente se o objetivo final for apenas classificar (transformando a maior probabilidade em uma resposta cravada Sim ou Não).

### LOG LOSS

O log-loss, também chamado de perda logaritmica, é uma métrica de qualidade para modelos de classificação. Importante saber que ele **serve tanto para modelos frequentistas como bayesianos**. Podemos usá-lo em regressão logística, rede neurais e gradient boosting. No frequentista ele é chamado de cross-entropy (entropia cruzada) e também é muito próximo do conceito de máxima log-verossimilhança.

> Log-Loss = Entropia Cruzada = - Log-Verossimilhança/N

Ao invés de apenas checar se o modelo acertou ou errou, o log-loss mede o quão confiante o modelo estava ao fazer a previsão. Quanto mais confiante ele tava desse resultado, mais punido ele é por errar. Se ele disse que tinha 99% de certeza que era Dengue e não era, a punição é altíssima, se ele disse que era 51% de certeza, a punição é pouca.

Portanto o nível de confiança do modelo serve como peso para a função de perda. Os modelos sempre tentam internamente minimizar o log-loss.

A função do log-loss (entropia cruzada) para uma classificação binária é:

log-loss = $-(y * ln(p) + (1-y)ln(1-p))$ 

Equação vinda do log da função de Bernoulli. Aonde **y é 0 ou 1** (tem ou não tem, sim ou não) e p é a probabilidade calculada pelo modelo (**p é o nível de confiança** que o valor é esse).

#### Exemplo

A rede mediu a probabilidade de 3 pacientes terem câncer. Para o 1º deu 80% de chances de tá com câncer, para o 2º 90% de chances de tá doente e para o 3ª 51%. Com y sendo a resposta do modelo (1 = tem, 0 = não tem). 

Porém apenas o primeiro e o terceiro de fato tem câncer. Calculando o log-loss deles temos.

$y_1=1$, $y_2=0$ e $y_3=1$

Log-Loss1 = $-(y_1 * ln(p_1) + (1-y_1)ln(1-p_1)) = -(1 * ln(0.8) + (1-1)ln(1-0.8)) = -ln(0.8) = 0.223$

Log-Loss2 = $-(y_2 * ln(p_2) + (1-y_2)ln(1-p_2)) = -(0 * ln(0.9) + (1-0)ln(1-0.9)) = -ln(0.1) = 2.302$

Log-Loss3 = $-(y_3 * ln(p_3) + (1-y_3)ln(1-p_3)) = -(1 * ln(0.51) + (1-1)ln(1-0.51)) = -ln(0.5) = 0.673$

Ou seja, como acertou o primeiro a penalização foi pequena (penalização 0 só se der 100% de certeza). O terceiro acertou mas tinha tão pouca certeza que levou uma penalização muito maior. E como errou o segundo e ainda deu uma confiança absurda o erro foi enorme.