# MEU ESTUDO SOBRE IA

Este repositório guarda meus estudos sobre IA, com anotações e códigos de cada fase dos estudos. Ele está separado em assuntos, onde cada pasta guarda as anotações sobre cada um.

É considerado IA qualquer programa que execute tarefas associadas à inteligência humana, como **percepção, raciocínio, aprendizado, planejamento, tomada de decisão e geração de conteúdo**. Como isso é muito abstrato, a definição exata pode ser relativa. Assim, uma forma mais simples de definir IA é um sistema que usa algoritmos comuns dessa área.

A grande mudança de paradigma foi sair de sistemas em que o programador especificava explicitamente grande parte do comportamento para sistemas em que **o comportamento é parcialmente aprendido a partir de dados**. Isso fica claro quando vemos algoritmos atuais que se baseiam em grandes massas de dados para aprender um comportamento (machine learning). A análise de dados e estatística substituíram os if-else e a necessidade do programador inserir cada regra no código para um sistema que aprende as regras por observação. A estatística vem como a base matemática que guia o aprendizado, indicando qual funciona melhor e para qual caminho seguir.

Enquanto as IAs clássicas eram estáticas, dando sempre o mesmo resultado para as mesmas entradas, as modernas são mais dinâmicas. Isso ocorre porque as IAs clássicas tinham uma lógica engessada e não aprendiam, enquanto as novas criam sua própria lógica a partir dos dados e podem dar resultados diferentes a partir dos dados e hiper-parâmetros usados no treinamento.

# Estrutura

Cada pasta explica em detalhes o funcionamento de cada tipo de IA, com diagramas e códigos práticos. Para uma compreensão melhor de todo o assunto é recomendado seguir a ordem numérica das pastas para absorver o conteúdo, pois um tipo de IA mais recente muitas vezes usa conhecimento dos anteriores como base.

# Eras da IA

A IA é conhecida por ter tido várias ondas de desenvolvimento. Abaixo listo como foi a evolução da IA desde sua primeira versão.

- **1940–1970**: IA simbólica ou clássica
  - Regras, lógica, símbolos e busca em árvore e grafos
- **1970–1980**: 1º inverno da IA
- **1980–1987**: Sistemas especialistas
  - Mesma coisa, mas com especialistas da área ajudando a modelar
- **1987–1993**: 2º inverno da IA
- **1990–2010**: IA estatística / Machine Learning
  - Uso de estatística e grande massa de dados para criar modelos dinâmicos
- **2010–2017**: Deep Learning
  - Redes neurais com várias camadas e diversas arquiteturas
- **2017–2022**: Transformers
  - Criação da arquitetura de rede neural que mudaria a IA
- **2022–atual**: IA generativa e agentes

## Era 1: IA simbólica (1940–1956)

Em 1943 Warren McCulloch e Walter Pitts publicam um artigo sobre o modelo matemático do neurônio, o que marcou o início da pesquisa em redes neurais artificiais. Aqui ainda usando lógica e álgebra para modelar o comportamento do neurônio. Os algoritmos genéticos também foram criados na década de 1950 mas não recebeu nenhuma atenção.

Em 1950, Alan Turing publicou o trabalho *Computing Machinery and Intelligence* e propôs o conhecido **Imitation Game**, posteriormente chamado de **Teste de Turing**. O objetivo não era criar um produto de IA como conhecemos hoje, mas investigar se uma máquina poderia apresentar um comportamento indistinguível do comportamento humano em uma conversa. 

Nessa época a inteligência e o conhecimento estavam todos no programador que precisava escrever um código que se parecesse inteligente. Aqui todas as regras eram colocadas como if-else no código ou modeladas como grafos ou árvores de decisão. Tentava-se transformar regras do mundo real em regras matemáticas para serem então passadas ao computador e com essas estruturas de dados (árvores e grafos) o programa parecer inteligente.

Nesse período, a preocupação central era:

> **Uma máquina pode apresentar comportamento inteligente?**

A conferência de Dartmouth, em 1956, é tradicionalmente considerada um marco na criação formal da área de IA e quando o termo se popularizou no meio acadêmico. em 1957 é criado o perceptron, o primeiro algoritmo de aprendizado de máquina e que virou base para os neurônios das redes neurais décadas depois.

A ideia era representar explicitamente o conhecimento usando:
- regras, lógica e símbolos;
- árvores de decisão;
- grafos;
- mecanismos de busca;
- inferência através de heurísticas.

Isso só funciona bem quando:
- Problema pequeno
- Regras conhecidas
- Ambiente previsível

### Técnicas

As técnicas mais importantes nessa era foram:

- Máquinas de estado
  - Modelar o comportamento, ambiente e/ou situações como estados e o que causa a mudança entre eles
  - Cada estado era uma situação possível
  - Isso permitia encontrar uma sequência de ações que navegavam entre estados do estado inicial até o desejado
  - Precisa conhecer todas as situações possíveis e ações que podem acontecer e como elas mudam o ambiente
- Árvores de decisão
  - Modela decisões a partir de perguntas/leituras do ambiente
  - Pode ser feito com uma série de if-else ou uma árvore aonde cada nó analisa o ambiente e as arestas direcionam para a próxima análise de acordo com a resposta
  - Exige amplo conhecimento do negócio para mapear todas as leituras a serem feitas e o que fazer após cada uma
- Busca em largura e em profundidade
  - Busca em árvore e grafo que checam todas as possibilidades a partir do estado atual
  - Também lembra uma máquina de estado (apesar de não ser) já que cada nó representa um estado e as arestas uma ação que muda o ambiente
- Busca heurística
  - Atribui pesos a cada aresta da árevore/grafo para representar o quanto vale ou não seguir aquele caminho
  - Não explora cegamente todas as opções, dá preferência por aqueles mais promissores
  - Usa uma função (heurística) que calcula o quanto cada nó tá distante do objetivo final
  - Ter como calcular essa distância do objetivo é essencial para usar esse método
  - Ex: algoritmo A*
- Minimax
  - Tomada de decisão em jogos 1x1
  - Usa árvores de decisão para descrever cada jogada
  - Executa de forma recursiva
  - Funciona quando se conhece por completo o ambiente (como no xadrex)
  - É extremamente custoso. $O(n^m)$
  - Usa a técnica *Poda alfa-beta* para descarta ramos inúteis, tornando-o mais rápido
  - Usado pelo **Deep Blue para ganhar do Kasparov no xadrez**
- Lógica de predicados (sistema formal)
  - Modela todo o sistema através de frases. Cada situação vira uma frase
    - Ex: o robô está com a pá emperrada
  - O sistema testa se essa frase é verdadeira ou não
    - Ex: verifica se a pá está emperrada ou não
  - Uma frase pode usar a resposta de outras frases para criar algo complexo
    - Ex: robô está em um canto e bateria baixa
  - Testar se a frase é verdadeira (executar uma função que retorna true ou false) é uma *regra*
  - Regras são o pilar central em detrimento dos dados (fatos)
    - Regras > Fatos
    - Encadeamento para trás
  - É aqui que entra a linguagem de programação **Prolog**
- Sistema de produção
  - Modela o problema em regras e fatos
  - Fatos são leituras do ambiente e dados de entrada
  - Regras são conjuntos de if-else que criam ou alteram fatos
  - A criação/alteração de fatos por executar regras disparam novas regras
  - Fatos > Regras
    - Essa é sua diferença da lógica de predicados
    - Encadeamento para frente

### Primeiro inverno da IA (1970–1980)

O baixo poder computacional e dificuldade de representar o mundo real e seus estados conforme os algoritmos pediam tornaram impraticável o uso da IA em larga escala. O mundo se mostrou muito complexo, com mil possibilidades que não podiam ser mapeadas e modeladas como esperado. Isso fez o interesse e pesquisas na área congelerem por anos.

Mas não foi uma década sem nada acontecendo. Em 1975 graças ao trabalho de John Holland os algoritmos genéticos receberam holofotes e passaram a ser estudados seriamente.

## Era 2: Sistemas especialistas (1980–1987)

Os sistemas especialistas usavam regras bem definidas por especialistas da área. Os programadores se uniam com especialsitas de uma área para modelar algum problema muito específico e fazer um programa que só resolvia 1 única coisa. Eles usavam as técnicas e algoritmos da IA simbólica, mapeando um contexto muito reduzido com ajuda de especialistas da área.

Um feito digno de nota dessa época foi a criação do algoritmo *backpropagation* em 1980 que viria a revolucionar as redes neurais no futuro.

### Segundo inverno da IA (1987–1993)

Dar manutenção em sistemas especialistas era quase impossível e sofriam dos mesmos males da IA simbólica. Transformar conhecimento humano em milhares de regras era caro e difícil e se o programador saísse da empresa ninguém mais conseguia assumir o projeto.

## Era 3: IA estatística e Machine Learning (1990–2010)

A mudança mais importante foi abandonar a ideia de que todas as regras deveriam ser programadas manualmente. Em Machine Learning, o sistema recebe exemplos e aprende uma função capaz de relacionar entradas e saídas. Tudo isso feito seguindo algoritmos baseados em estatística pesada. O uso de estatística para definir o funcionamento do sistema e guiar a encontrar padrões foi a chave do salto dado.

Porém isso exige uma massa de dados gigantesca para ser feito e toda uma nova área de conhecimento foi criada para encontrar, tratar e disponibilizar esses dados e também para como trabalhar com eles. Métodos de uso desses dados no treinamento e na avaliação do mesmo antes de botar em produção surgiram conforme foi-se evoluindo essa área.

Importante dizer que apesar da ascensão do machine learning a IA clássica ainda encontrava espaço e havia uma certa disposta entre as duas para se provar qual abordagem era melhor. Um feito digno de nota foi a vitória do Deep Blue sobre Kasparov no xadrez em 1997, usando IA clássica.

As redes neurais aqui ainda eram com 1 ou 2 camadas (a inicial e final) e consideradas uma vertente pouco produtiva devido seu alto gasto computacional e necessidade de altos dados. **Perceptrons multicamadas** eram o que se fazia com redes neurais na época. O machine learning usava muito outros algoritmos como regressões, máquinas de vetores de suporte e etc, mas as redes neurais estava lá como mais um concorrente.

### Paradigma

```text
                                        DADOS
                                          │
                                          ▼
                                  ┌─────────────────┐
  diferentes hiper-parâmetros --> │ Algoritmo de ML │
                                  └─┬──────┬──────┬─┘
                                    │      │      │
                                    ▼      ▼      ▼
                                 MODELO MODELO  MODELO
                                    │      │      │
                                    ▼      ▼      ▼
                                   ┌────────────────┐
                                   │ Dados de teste │
                                   └───────┬────────┘
                                           │
                                           ▼
                                      MELHOR MODELO
                                           |
                                           |
                                           ▼
                                    ┌───────────────┐
                                    │   produção    │
                                    └──────┬────────┘
                                           |
                                           ▼
                                    ┌───────────────┐
                                    │  Novos Dados  │
                                    └──────┬────────┘
```

### Técnicas

Os algoritmos de machine learning podem ser divididos em 3 grupos principais. Exitem outras formas de machine learning, mas essas são disparados as principais:

- Aprendizado supervisionado
- Aprendizado não supervisionado
- Aprendizado por reforço

Cada grupo tem seus próprios algoritmos e fluxos de funcionamento. Suas diferenças serão melhor trabalhadas na pasta de machine learning, mas só para citar alguns algoritmos comuns dessa área temos:

- Regressão linear
- Regressão logística
- Gradiente descendente
- Naive Bayes
- k-Nearest Neighbors
- árvores de decisão
- Random Forest
- Support Vector Machines
- Perceptrons multicamadas
- clustering

## Era 3.5: Deep Learning (2010–2017)

Aqui as redes neurais despontaram como a favorita e mais promissora forma de IA. Isso aconteceu graças ao deep learning. Deep Learning é uma subárea de Machine Learning baseada principalmente em **redes neurais com múltiplas camadas**. 

As redes neurais tinham 1 ou 2 camadas e sofriam para ter mais que isso devido ao crescimento exponencial de processamento para processar e convergir todos os pesos quando tinha mais que isso. Com o uso de GPUs maios poderosas e melhoria dos algoritmos isso se tornou possível. O objetivo agora é descobrir quantas camadas uma rede neural deveria ter para dar os resultados mais precisos e como descobrir isso com o menor processamento. Algoritmos genéticos também foram usados junto com as redes neurais para complementar o aprendizado.

Em 2016 o AlphaGo, IA da DeepMind, vence o campeão mundial de Go, marcando outro grande marco na história da IA. Ele usava deep learning e busca em árvore de Monte Carlo. A busca da árvore era aprimorada com aprendizado por reforço.

### Funcionamento de uma rede neural

O funcionamento mais alto nível de uma rede neural é da seguinte maneira.

```text
             ┌───────────────┐
             │ Dados         │
             └───────┬───────┘
                     ▼
             ┌───────────────┐
             │ Rede neural   │
             └───────┬───────┘
                     ▼
                  Predição
                     │
                     ▼
             ┌───────────────┐
             │ Função de     │
             │ perda (loss)  │
             └───────┬───────┘
                     ▼
             Backpropagation
                     │
                     ▼
              Atualizar pesos
                     │
                     └──────────► repetir
```

Aonde a função de perda calcula o quão errado a rede calculou e o backpropagation é o algoritmo criado para recalcular os pesos de cada entrada de cada neurônio de cada camada. A função de perda define o quanto erramos, o backpropagation define o quanto cada neurônio deve ser corrigido para melhorar e então todo o processo é repetido. Internamente o backpropagation usa os algoritmos já conhecidos de machine learning como regressões e gradiente descendente. Outros algoritmos de machine learning são aproveitados nas redes neurais no funcionamento interno do neurônio como regressão logística para função de ativação.

Dando um zoom na rede neural podemos ver como o neurônio funciona.

```text
ENTRADAS

x₁ ──┐
x₂ ──┼──► [Camada 1] ──► [Camada 2] ──► [Camada 3] ──► SAÍDA
x₃ ──┤
x₄ ──┘
```

Aonde X são os dados de treinamento. Cada camada tem vários neurônios e cada neurônio calcula aproximadamente:

```text
z = w₁x₁ + w₂x₂ + ... + wₙxₙ + b

saída = função_de_ativação(z)
```

Os pesos começam com valores aleatórios e a cada rodada são ajustados pelo backpropagation.

### Insight importante

No Machine Learning tradicional, frequentemente o programador precisava definir quais características deveriam ser processadas pela rede neural. No Deep Learning a rede consegue aprender representações progressivamente mais complexas. Cada camada desvenda uma característica específica dos dados, encontrando padrões mais complexos e desvendando mais informações. Com essa habilidade do deep learning foi possível dar um salto que tornou a IA popular no mundo todo e ser assunto dos papos de bar.

Isso também tirou ainda mais da mão do programador a necessidade de conhecer amplamente o contexto, pois a rede neural desvendava sozinha o que precisava desvendar. Isso levou o aprendizado não supervisionado para outro nível e gerou discussões sobre ninguém mais saber para onde a IA estava indo ou o que ela poderia descobrir ou decidir fazer no futuro.

```text
Imagem --> Bordas --> Formas --> Partes de objetos --> Objetos --> Classe
```

---

## Era 3.7: Transformers (2017-2022)

Um transformer é uma arquitetura de rede neural profunda (deep learning) criada em 2017 pelo Google no trabalho *Attention Is All You Need*. Essa arquitetura mudou profundamente o processamento de linguagem natural e posteriormente tornou-se a base de muitos modelos generativos modernos. Ela chama cada unidade de processamento de token e avalia o quanto os tokens se auto referenciam. Antes a rede neural só ligava a palavra com as palavras próximas. Com o conceito de auto referência (atenção) uma palavra poderia estar ligada a outra longe no texto, expandindo a capacidade de entender e criar textos complexos.

Cada token preferenta uma palavra e, dependendo do contexto, pedaços de uma palavra. Representar pedaços de palavra como token permitia à IA entender tempo verbal, formas nominais, singlular e pluras e outras sutilezas da linguagem.

## Era 4: IA generativa — a partir de 2022

Com o aumento do tamanho dos modelos, da quantidade de dados e do poder computacional, tornou-se possível treinar modelos generalistas em grande escala. Esses modelos são frequentemente chamados de **foundation models** (modelos fundacionais). Com esses grandes modelos gerais o teste de Turing foi quebrado e foi-se cogitado se uma AGI (IA de uso geral, que entenda e sirva para qualquer assunto) tenha sido criada. Como um modelo fundacional pode ser usado para diversos fins ao generalizar a ação usando contextos discute-se muito se eles são uma IA de uso geral ou ainda são restritos. As LLM e o ChatGPT foi o primeiro modelo fundacional a ganhar fama.

A ideia do modelo fundacional é:

```text
             GRANDE VOLUME DE DADOS
                       │
                       ▼
              PRÉ-TREINAMENTO
                       │
                       ▼
              MODELO FUNDACIONAL
                       │
          ┌────────────┼─────────────┐
          ▼            ▼             ▼
       texto         código        imagens
          │            │             │
          ▼            ▼             ▼
       tarefas       tarefas       tarefas
```

Em vez de treinar um modelo completamente independente para cada tipo de tarefa, um modelo geral pode ser adaptado ou utilizado em diversos contextos. São redes produndas que usam transformers treinados com uma grande massa de dados e ao receber uma pequena massa de dados específica consegue se reconfigurar para aqueles dados usando a grande massa inicial de dados como insumo base e os dados novos como contexto para saber o que deve fazer.
