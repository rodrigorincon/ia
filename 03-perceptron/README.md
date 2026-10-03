# PERCEPTRON

O perceptron é o primeiro modelo de **"neurônio artificial" treinável**, simulado em 1957 e formalizado no artigo publicado em 1958. Sua ideia era simular um neurônio humano e replicar como nosso cérebro funciona biologicamente. A função desse modelo inicial era apenas classificar dados, não fazia regressões.

Seu funcionamento acontecia dando pesos diferentes para cada entrada e atualizando os pesos. Ou seja, sua premissa de inteligência era descobrir o peso para cada entrada.

Assim como a regressão logística, é um **classificador binário linear**: separa dados em 2 categorias usando uma reta (ou hiperplano, em mais dimensões). A diferença central é como ele aprende os pesos dessa reta.

Ele é considerado a ponte entre os modelos estatísticos clássicos e as redes neurais modernas: a mesma estrutura de somar entradas ponderadas e aplicar uma função de ativação.

## O Primeiro Neurônio

Sua primeira implementação (perceptron simples) em 1958 era um computador analógico conectado a uma câmera de retícula 20x20 (400 pixels). Os pesos não eram variáveis salvas na memória RAM, mas sim potenciômetros motores (resistores variáveis ajustados por motores elétricos).

Sua função era apenas reconhecer imagens de 20x20 pixels, identificando se era um objeto A ou B. Ele não conseguia tratar outros tipos de dados ou separar entre 3 ou mais categorias.

O perceptron simples só conseguia fazer classificação e apenas entre 2 categorias diferentes ("é ou não é algo"). Ele se assemelha muito a regressão logística, sendo a diferença crucial a atualização dos pesos. Na regressão o peso é atualizado mesmo que se acerte a categoria daquele dado, no **perceptron simples o peso só é atualizado se errar a categoria**.

Sua maior restrição, além de só resolver classificações binárias, é **só funcionar para casos onde os dados são linearmente separáveis**. Como o SVM sem kernel, ele não consegue classificar se os dados formam curvas ou forma círculos cocêntricos.

Devido a essas limitações ele foi desacreditado e esquecido por décadas, até a invenção do backpropagation, que permitia a criação de vários neurônios encadeados, criando redes neurais propriamente ditas. Por isso hoje ele não é usado e só é ensinado com fins didáticos.

## Estrutura de um Neurônio

O perceptron refletia diretamente o funcionamento de um neurônio real. Por isso ele era dividido em 4 partes:

### Sinais de Entrada (Dendritos)

Na biologia os dendritos são as ramificações que recebem os impulsos elétricos vindos de outros neurônios. No perceptron são as entradas X. Cada linha X é uma entrada e recebem um peso exclusivo. O peso serve para dizer o quanto aquela entrada deve ser levada em consideração.

### Corpo do neurônio

Faz a soma ponderada de todas as entradas. É aonde Z é calculado. 

$$z = w_1x_1 + w_2x_2 + ... + w_nx_n + b$$

O termo b é o intercepto (viés).

Podemos reescrever essa equação em forma de matriz da seguinte forma:

$$z = w^T x + b$$

O corpo tem esse comportamento pois é onde todos os dentritos se encontram e o processamento é feito, portanto toda a lógica pesada fica nele. Ele representa a voltagem total no neurônio.

> Repare que z é exatamente a mesma equação linear usada na regressão logística. A diferença entre os dois modelos não está em como calculam z, e sim no que fazem com ele depois.

A terceira parte também faz parte do corpo: a função de ativação.

### Função de Ativação

A segunda metade do corpo, **verifica se a soma das entradas (voltagem total) ultrapassa um certo limiar biológico (threshold). Se ultrapassar um certo valor o neurônio é ativado. Caso contrário, permanece em repouso.**

Isso significa que se a voltagem for alta o suficiente ele passa o sinal para frente e se for baixa não passa sinal nenhum adiante.

No perceptron original essa função de ativação é a função degrau. Enquanto a regressão logística passa z pela sigmoide (gerando uma probabilidade entre 0 e 1), o perceptron usa a **função degrau**: um corte seco que devolve apenas duas saídas possíveis, sem meio-termo. O threshold da função degrau é 0: tudo abaixo dele é uma categoria e tudo acima dele é outra.

$$\hat{y} = \begin{cases} +1, & \text{se } z \geq 0 \\ -1, & \text{se } z < 0 \end{cases}$$

Ainde +1 significa "classificou corretamente" e -1 significa "classificou errado". Repare que a **resposta não tem um significado como "1 é categoria X e -1 é categoria Y"**. Eles **significam "acertou" e "errou"**. Na literatura a função de atvação é chamada de f(z).

Não existe "70% de chance de ser da classe 1" no perceptron. Ou o ponto está de um lado do hiperplano, ou está do outro. Essa é a limitação que motivaram a substituição da degrau por funções suaves (sigmoide, ReLU) no futuro: uma **função de ativação diferenciável é obrigatória para o backpropagation funcionar**. A degrau tem derivada zero em quase todo ponto (e indefinida em z=0), então não dá para fazer o gradiente descendente através dela.

### Saída do Neurônio (Axônio)

Na biologia, o axônio é a fibra longa que transmite o sinal elétrico do neurônio para fora do corpo celular, enviando a informação para os próximos neurônios ou órgãos efetores. No perceptron ele é simplesmente o resultado final da função de ativação.

Aqui nenhuma conta é feita, só retorna a saída final do corpo.

## Perceptron Multicamadas

O Perceptron Multicamadas (MLP, de *Multi-Layer Perceptron*) é uma rede neural formada por camadas de neurônios enfileiradas: uma camada de entrada, uma ou mais **camadas ocultas** e uma camada de saída. 

Ele é a evolução direta do perceptron simples, colocando vários deles em enfileirados para resolver problemas que ele não conseguia. Essa evolução do perceptron simples retirou um modelo que havia caído em descrédito e o colocou como o modelo de ponta da área inteira. Um único neurônio só desenha uma reta e, por isso, não resolve problemas complexos. **Cada camada adicionada funciona como uma dimensão extra, permitindo separar dados muito intriados, funcionando como o kernel do SVM**.

Cada neurônio do MLP continua sendo um perceptron (soma ponderada + bias + ativação), mas com duas mudanças. A primeira é enfileirar neurônios em camadas, de modo que a camada oculta transforma o espaço dos dados e a camada de saída separa o resultado dessa transformação. A segunda é trocar a função degrau por uma ativação suave e diferenciável (a sigmoide), o que permite treinar a rede inteira com **backpropagation** (retropropagação do erro) e gradiente descendente.

Ele é um modelo de **aprendizado supervisionado** que serve tanto para **classificação (com quantas categorias quiser) quanto para regressão**. Ele é extremamente customizável e **é o modelo base de rede neural**, sendo amplamente usado até hoje.

Ele também é chamado de redes feedfoward ou de rede neural vanilla.