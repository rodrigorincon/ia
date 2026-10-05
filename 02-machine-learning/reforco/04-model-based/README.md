# APRENDIZADO POR REFORÇO: FAMÍLIA MODEL-BASED

A família model-based (baseados em modelo) constrói ou utiliza uma representação interna das dinâmicas do ambiente (um "modelo") que prevê as probabilidades de mudança de estado e as recompensas. Ou seja, ele recria todo o ambiente internamente e **faz simulações para aprender ao invés de interagir com o mundo real**. 

Ele é especial quando é muito caro ou difícil testar no mundo real (ex: IA de um satélite, robô que será mandado para o espaço ou carro autônomo). **Ele aprende com a simulação e depois que aprendeu é colocado no mundo real**. Por isso o modelo precisa ser o máximo preciso, pois qualquer mínima diferença entre o modelo e a vida real pode ensinar a IA a agir errado, esperando comportamentos diferentes.

Isso também dá a essa família uma vantagem de **alcançar o objetivo com muito menos passos que os anteriores**.

## Diferença Para as Demais Famílias

Enquanto os modelos anteriores apenas reagem ao estado, os algoritmos baseado em modelos tentam **aprender as leis do ambiente e a função de recompensa**. Com isso, eles conseguem simular o futuro em suas "mentes" antes de agir no mundo real. Aprender as leis do ambiente (regras ou leis físicas) é feito através de redes neurais e dados sintéticos produzidos por modelos já conhecidos do mundo. Aprender as recompensas vai pela mesma linha. Ter de descobrir quantos pontos dar ou tirar, além de descobrir como o mundo funciona tornam essa família consideravelmente mais complexa que os demais.

## Diferença Entre os Algoritmos

As diferenças entre os algoritmos está em como consegue o modelo do ambiente e como o planejamento é executado. 

Quando o modelo do ambiente é conhecido de antemão (como as regras do xadrez ou Go) algoritmos de busca em árvore como o **Monte Carlo Tree Search (MCTS)** (usado no AlphaZero) exploram trajetórias futuras para selecionar a melhor ação. 

Quando o ambiente é desconhecido, redes neurais são usadas para aprender a física do mundo a partir de observações (como simulador de clima em meteorologia). Variações como o **MBPO** usam o modelo aprendido para gerar dados sintéticos e treinar agentes de política.

Outras variações baseadas em world models, como o **Dreamer**, aprendem representações em espaços latentes para prever o futuro e otimizar ações completamente "dentro de um sonho", permitindo resolver tarefas visuais complexas com um número reduzido de interações reais.

### AlphaZero / MCTS (Monte Carlo Tree Search)

Combina redes neurais profundas com a busca em árvore de Monte Carlo (MCTS). A rede neural prevê os valores dos estados e as probabilidades de jogada, enquanto a árvore MCTS realiza milhares de simulações do jogo para frente a partir do estado atual para selecionar o melhor movimento.

- **Quando usar:** Jogos determinísticos de informação perfeita com regras claras (Xadrez, Go, Shogi).
- **Tipo:** Model-Based / Planejamento por Busca em Árvore.
- **Pontos Negativos:**
  - Exige um simulador perfeito e determinístico do ambiente para realizar a busca na árvore.
  - Custo computacional de inferência extremamente alto por jogada.

### Dyna-Q e World Models (MBPO - Model-Based Policy Optimization)

O algoritmo aprende um modelo do mundo simultaneamente enquanto interage com o ambiente real. Em seguida, ele gera "experiências imaginárias" usando esse modelo interno para treinar o agente sem precisar gastar tempo no ambiente real.

- **Quando usar:** Quando interagir com o ambiente real é extremamente caro, perigoso ou demorado (ex: desgaste mecânico de robôs caros, testes clínicos).
- **Pontos Negativos:**
  - **Exploitation do Modelo:** Se o modelo do mundo aprendido cometer um pequeno erro, o agente aprenderá a explorar essa falha do modelo ("trapaceando" na simulação) e falhará miseravelmente quando testado no ambiente real.

