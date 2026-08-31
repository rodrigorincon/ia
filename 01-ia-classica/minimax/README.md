# ALGORITMO MINIMAX

O algoritmo minimax é um algoritmo de IA usado em jogos de turnos aonde um joga contra o outro. É o algoritmo principal usado em xadrez, por exemplo. Ele pode ser usado em qualquer situação de `tomada de decisão onde você precisa se proteger contra o pior cenário possível` provocado por um oponente ou pela incerteza.

Isso acontece porque como o algoritmo é feito na base de uma disputa entre 2 lados e ambos os lados sempre assumem que o adversário fará a melhor escolha para si. Assim se torna uma ferramento muito boa para se proteger para o pior cenário, garantindo que no pior caso tomará a melhor decisão. Manter o algoritmo atualizado com o ambiente atual faz com que ele se adapte e mude as escolhas de acordo com a mudança de ambiente.

## Funcionamento

O algoritmo cria uma árvore, aonde cada nó é um cenário do jogo. Cada nó é uma cópia do nó pai com 1 jogada feita, assim o número de nós filhos é a quantidade de todas as jogadas possíveis a partir daquele cenário. Por isso ele se encaixa tão bem em jogos, pois sabemos muito bem todas as possibilidades de ação e por ter turnos.

Ele vai fazendo nós até que encontre um fim de jogo ou até uma profundidade limite. Quando encontra um fim de jogo o algoritmo retorna 1 caso a IA ganhe (ou quem ele queira que vença), 0 em caso de empate ou -1 caso a IA perca. Esse valor pode mudar caso o cálculo da função heurística dê valores em outra escala.

### Turnos e pontuação

Como o algoritmo simula um jogo por turnos, a cada nível da árvore é simulado a jogada de um jogador diferente (camada da IA, camada do jogador, camada da IA, camda do jogador...). Em cada nível é escolhido a jogada que mais beneficia o jogador da vez. Na camada da IA é escolhido a jogada com maior pontuação e na jogada do jogador adversário é escolhido a jogada com menor pontuação. Isso significa que na vez da IA ela escolhe a jogada que lhe dá o melhor resultado e na vez do adversário a jogada que lhe dá o pior resultado. Por isso ele é considerado um **algoritmo de soma zero** e lembre muito teoria dos jogos.

O valor de um nó é dado pelos nós filhos. Será o maior ou menor valor de seus filhos (como explicado acima). Isso faz os caminhos retornarem recursivamente seus resultados e revezar entre pegar o melhor e pior. Isso faz que uma vitória certa não seja escolhida de cara porque (ao assumir que o adversário é o melhor possível e sempre faz as melhores jogadas) o adversário não permitirá que você faça a jogada decisiva. Por isso podemos considerar o minimax um **algoritmo pessimista, que no mínimo garante um empate**.

Por fim, as folhas dão o valor conforme escrito no tópico anterior, quando encontram um fim de jogo ou chegando na profundidade máxima, retornando o valor calculado pela função heurística.

### Heurística

Quando se define uma profundidade máxima a ser vasculhada (para evitar processar infinitamente ou não gastar muito tempo para responder) e a alcança chamamos a função heurística. Ela será um chute de quão perto ou longe a IA está de vencer o jogo. 

A inteligência da IA está toda na função heurística, pois é ela que define se um nó interediário é melhor que outro e define em números o quão perto estamos de ganhar. Por isso se chama heurística, ela tenta inventar um jeito de calcular a distância até o objetivo final (vitória).

A função heuristica é **o que diferencia os algoritmos do mesmo jogo um do outro** (um nível fácil de um nível difícil por exemplo ou 2 bots diferentes do mesmo nível). É só isso que faz um ser melhor que o outro. Para jogos muito complexos e que podem ter milhares de níveis a parada por profundidade e a heurística é obrigatória. Supor um valor a partir de um jogo no meio é o real desafio de fazer a IA.

Perceba que quanto menor a profundidade máxima melhor precisa ser a heurística.

## Poda alfa-beta

A poda alfa-beta é uma otimização do algoritmo, tornando-o mais rápido ao não perder tempo analisando caminhos que não dão em nada. Uma das formas de otimização é definir uma profundidade máxima conforma já explicado, porém a poda alfa-beta não se resume a ela.

A poda funciona interrompendo a avaliação dos nós de um ramo ao encontrar um caso que garanta que nenhum nó desse ramo será escolhido pelo nó pai. Assim que encontra toda aquele ramo é encerrado e passa ao próximo ramo irmão.

Ex: O nó pai é a rodada MAX (escolhe o maior valor), portanto seus nós filhos estão na rodada MIN (escolhem o menor valor). O 1º nós filho tem valor 2. Ao avaliar os ramos do 2º nó filho encontramos -10 em um dos netos, significando que o 2º nó filho terá no melhor cenário valor -10. Portanto podemos encerrar o 2º ramo e ir ao terceiro, pois o 2º nó filho precisa escolher o menor valor dentre os netos e já tem -10, significando que será de -10 para baixo seu valor (menor que o valor 2 do outro ramo). E como o nó pai é MAX, 2 sobressairá sobre qualquer valor do 2º filho.

Para tanto o valor de comparação a ser usado nas rodadas MAX é o alfa e o valor a ser comparado nas rodadas MIN é o beta. Assim a cada rodada temos de passar os 2 valores recursivamente para a camada abaixo saber qual valor devem parar ao encontrar.

A título de curiosidade, veja a diferença de nós visitados na versão com e sem poda do jogo da velha:

- Sem poda: 63.905 nós no 1º lance e 1.229 no 2º lance
- Com poda: 1.514 nós no 1º lance

## Minimax e teoria dos jogos

Minimax aplica-se apenas a jogos com as seguintes características:

- Informação perfeita: onde se conhece todo o ambiente, pode-se ver todo o tabuleiro
- Soma zero: onde o ganho de um jogador é a perda do outro
- Baixa probabiliade: pouco efeito de aleatoriedade

Segundo o teorema minimax (von Neumann), em jogos de soma zero existe uma estratégia mista que minimiza a perda máxima. A limitação é em cenários que não são soma zero, não se conhece todo o ambiente ou que possua alta aleatoriedade (como poker) probabilidades. Nesses casos usa-se variantes como **expectimax** ou soluções da teoria dos jogos mais gerais.

## Áreas de Aplicação

- Cibersegurança: ajuda a planejar defesas de redes de computadores. **Assume que um hacker tentará causar o maior dano possível**.
- Economia e Finanças: usado na gestão de riscos de investimentos. Serve para escolher ativos que **reduzem as perdas** em uma crise grave.- Machine Learning: aplicado em redes neurais do tipo GAN (Redes Adversariais Generativas). Duas partes competem entre si para melhorar a criação de dados ou imagens falsas.
- Negócios e Estratégia: ajuda empresas a antecipar os passos de concorrentes. **Evita que a companhia tome um prejuízo máximo** se o mercado piorar.
- Engenharia e Automação: usado no controle robusto de robôs ou fábricas. Garante o **funcionamento seguro mesmo com falhas** ou ventos fortes inesperados.

# Programas Presentes

Aqui temos 2 projetos usando minimax: jogo da velha e xadrez. No jogo da velha começamos com um projeto sem usar IA (o computador escolhe aleatoriamente onde jogará dentro as posições possíveis) e depois temo um arquivo usando minimax. Podemos olhar o projeto sem IA para enteder a estrutura do sistema e ver os pontos aonde a IA encaixa. A classe jogo da velha foi pensada para o algoritmo da IA ser o mais desacoplado possível, podendo trocar entre diferentes opções implementadas. Na pasta "escolhendo estratégia" isso é implementado, pois é criado um módulo de algoritmos para resolver o jogo da velha, podendo importar a versão que quer e encaixar na classe. Ao criar um algoritmo novo, basta criar um arquivo novo no módulo, importá-lo na classe principal e setá-lo na classe através do método `set_strategy`. Para tanto o novo algoritmo precisa implementar 2 métodos: `set_strategy e definir_proxima_jogada` respeitando a assinatura do método.

Para o xadrez é preciso instalar a biblioteca chasse com o comando `pip install chess`. A biblioteca já entrega funções prontas para controlar e ler o tabuleiro, saber se o jogo acabou, se é vitória ou empate e quais jogadas são possíveis. Usa-se um nível de profundidade baixo, pois a quantidade de filhos é entre 30 e 40, fazendo que se analisar só 3 jogadas afrente já serão 27mil análises. Por isso o número de profundidade precisa ser baixo e todas implementam poda alfa-beta.

Há 3 arquivos diferentes para ele, cada um com uma IA com nível de dificuldade diferente. Todo o código das 3 IAs do xadrez é igual, exceto a função heurística. Foram criadas uma heurística super simples (burra), uma mais rebuscada (médio) e uma que leva em conta muito mais coisas (inteligente).