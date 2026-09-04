# GRADIENTE DESCENDENTE ESTOCÁSTICO (SGD)

O Gradiente Descendente é como descer uma montanha de olhos vendados, tateando a inclinação do chão a cada passo para encontrar o vale mais profundo (o erro mínimo). O Gradiente Descendente Estocástico (SGD) mantém essa mesma lógica, mas muda drasticamente como e com qual velocidade processamos a informação do "chão".

Enquanto o gradiente descendente tradicional olha para a montanha inteira antes de dar um único passo, o Estocástico toma decisões rápidas e caóticas olhando apenas para a ponta do seu pé.

## Problema

No Gradiente Descendente normal, para calcular a direção do próximo passo (a derivada do erro), o algoritmo precisa somar o erro de **TODAS** as linhas do seu banco de dados. 

Se você tem um dataset com 5 milhões de imagens, o computador precisa processar as 5 milhões de imagens, calcular 5 milhões de erros, tirar a média de tudo isso, para dar **apenas um único passo** na atualização dos pesos. Isso acontece pois a função de custo calcula a partir de todos os X que você tem.

O que inviabiliza o modelo tradicional não é a matemática, é a falta de memória RAM e o tempo absurdo de processamento para bases de dados gigantes. Além disso, por calcular a média perfeita sempre, ele traça um caminho tão "liso" que tem uma facilidade enorme de ficar preso em buracos rasos (mínimos locais) achando que chegou no fundo absoluto da montanha.

**Objetivo**: atualizar os pesos da equação de forma muito mais rápida, sem precisar processar o dataset inteiro a cada milissegundo.

## Solução

A palavra "Estocástico" significa aleatório. A sacada do SGD é simples: **abandone a média perfeita**. Em vez de olhar para os 5 milhões de dados para dar um passo, o SGD sorteia aleatoriamente apenas **UMA única linha de dado**, calcula o gradiente só para ela, e já atualiza os pesos na mesma hora.

Isso faz com que a descida seja muito mais ruidosa, cheia de vai e vem, mas também evita mínimos locais. Só fica preso em um mínimo local se ele for bem mais fundo.

**Objetivo**: trocar a precisão e suavidade do caminho tradicional por uma velocidade brutal de aprendizado e eficiência de memória.

## O QUE MUDA NA PRÁTICA (E NA MATEMÁTICA)

A fórmula de atualização dos pesos (W) continua visualmente idêntica:

$W_{novo} = 	W_{velho} - \alpha * \delta F(W)$

A diferença monumental está no que compõe o cálculo do Gradiente:

- **No Tradicional (Batch)**: $\delta F = \frac{1}{N} \sum_{i=1}^{N} \delta F_i$
  - Ele calcula o gradiente exato: a média de todas as observações de $1$ a $N$

- **No Estocástico (SGD)**: $\delta F = \delta F_i$
  - Ele calcula uma estimativa do gradiente usando apenas a observação aleatória i

### O Caminho do Bêbado

Como o SGD olha para apenas uma observação por vez, ele sofre muita influência de dados ruidosos (outliers e minorias). Se ele pegar uma linha de dado que diz "a descida é para a esquerda", ele vai para a esquerda, mesmo que o resto do dataset dissesse "é para a direita". 

Isso faz com que a descida do SGD não seja uma linha reta e elegante, mas sim um zigue-zague caótico, como os passos de um bêbado descendo a montanha. 

**A grande vantagem do "Bêbado"**: Esse ruído (zigue-zague) é o que salva as Redes Neurais complexas. O passo cego e caótico joga o algoritmo para fora do vale do mínimo local (se não for fundo demais), permitindo que ele continue até achar o verdadeiro mínimo global. O modelo tradicional, por ser perfeitinho demais, ficaria preso.

## PASSO-A-PASSO

No tradicional, 1 passo = 1 leitura da base toda (1 Época). No Estocástico, a dinâmica muda:

1. **Embaralhar (Shuffle)**: Misturamos aleatoriamente todas as linhas do banco de dados (para não criar vícios sequenciais).
2. **Loop por observação**: Pegamos a linha i = 1.
3. **Cálculo isolado**: Calculamos o erro e a derivada apenas para a linha i = 1.
4. **Atualização imediata**: Atualizamos os pesos da equação.
5. **Próxima linha**: Pegamos a linha i = 2 e repetimos o processo.

Quando ele terminar de passar pelas 5 milhões de linhas, dizemos que ele completou **1 Época**. A diferença é que, ao final dessa 1 época, o SGD já atualizou os pesos do seu modelo **5 milhões de vezes**, enquanto o modelo tradicional teria atualizado apenas **1 vez**.

## O MEIO-TERMO: Mini-Batch SGD

O SGD puro (olhando 1 dado por vez) perde um pouco do poder dos processadores modernos, pois placas de vídeo (GPUs) são desenhadas para fazer matrizes andarem juntas em paralelo.

Por isso, na vida real nós não usamos nem "Tudo" (Tradicional) e nem "Um só" (Estocástico puro). Nós usamos o **Mini-Batch SGD**.

Em vez de pegar 1 linha, nós pegamos pequenos "lotes" de dados aleatórios (ex: 32, 64 ou 256 linhas por vez). 
- Ele é tão rápido de alocar na memória quanto o SGD.
- Ele se beneficia da velocidade de processamento paralelo das GPUs.
- O caminho fica um pouco menos "bêbado", facilitando que o modelo finalmente pare quieto quando chegar no fundo do vale.

### Resumo das Diferenças

| Característica | Gradiente Tradicional (Batch) | Estocástico Puro (SGD) | Mini-Batch SGD |
| :--- | :--- | :--- | :--- |
| **Uso de dados por passo** | 100% do Dataset | Apenas 1 linha | Lotes (ex: 32 a 256 linhas) |
| **Velocidade de atualização** | Extremamente lenta | Extremamente rápida | Muito rápida |
| **Caminho da descida** | Suave, sem desvios | Caótico, zigue-zague forte | Leve zigue-zague |
| **Fugir de mínimos locais** | Péssimo | Excelente | Muito bom |
| **Uso de Memória RAM** | Altíssimo (carrega tudo) | Quase zero | Baixo e controlado |
