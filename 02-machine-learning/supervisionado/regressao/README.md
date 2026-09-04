# REGRESSÃO

O aprendizado supervisionado pode ser dividido em dois grupos: regressão e classificação. A regressão busca prever valores numéricos e contínuos enquanto a classificação busca definir a qual categoria um dado pertence (é gato ou cachorro, sim ou não, aprovado ou reprovado...). 

A regressão serve perfeitamente para contextos matemáticos ou quando estamos modelar matematicamente algo. Se quisermos transformar algo em uma equação, é ele que usamos. Por isso ele só se enciaxa se puder transformar os dados e as respostas em algo numérico. 

## Resposta contínua

Como a resposta pode ser qualquer valor dos números reais, a regressão forma uma equação contínua. Se a resposta só pudesse ser valores inteiros (1, 2, 3) seria uma classificação, onde cada número representa uma categoria.

## Tipos

- Regressão linear: cria uma equação de primeiro grau (uma linha ou plano) que representa seus dados
- Regressão polinomial: cria uma equação de qualquer grau que representa seus dados

A grande verdade é que regressão polinomial não é muito usada, pois é muito complexa de modelar e aumenta e muito os cálculos necessários. O mais comum é usar transformação nos dados para linearizá-los e depois aplicar a regressão linear. Outros métodos como redes neurais também são mais recomendáveis para modelar nesses casos.

Não existe regressões que tentam modelar outras relações (como raiz quadrada, seno...), para esses casos também é preferível outros métodos como redes neurais.

### Transformação dos dados

Uma transformação muda a escala dos dados, tornando dados exponenciais mais lineares (log) ou eliminar a dispersão, deixando-os mais unidos (z-score). Em todos eles a escala de medida muda, portanto se você aplica transformação nas vars de saída (Y) no treino, ao prever e nos testes precisa aplicar a operação inversa para trazes a resposta de volta a escala original e ser compreensível e comparável com os dados de teste.

Você pode ver mais sobre transformação nos meus estudos sobre estatística no capítulo 10, [clicando aqui](https://github.com/rodrigorincon/statistics/tree/main/10-correlacao-e-transformacao).

## Fórmulas

1. **Regressão Linear Simples**

$y = a*x + b$

- Cria uma equação linear com apenas 1 var independente
- Só tem 1 único X

2. **Regressão Linear Múltipla**

$y = a_1*x_1 + a_2*x_2 ... + a_n*x_n + b$

- Cria uma equação linear com 2 ou mais vars independentes
- Simples com vários X

Porém usar essa fórmula nos dia-a-dia pode ser muito trabalhoso. O que de fato é feito para simplificar é reescrever essa mesma equação em formato de matriz, o que facilita tanto para o programador entender quanto agiliza o cálculo pela máquina. Mas a equação é a mesma e nenhuma relação é perdida. Só a forma de escrever que muda.
 
3. **Regressão Polinomial**

$y = a_1*x + a_2*x^2 + a_3*x^3 ... + a_n*x^n + b$

- Cria uma equação exponencial
- Tenta descobrir o coeficiente de cada expoente e quantos expoentes tem (se acaba no elevado a 3 ou no elevado a 10)
- Não envolve raiz quadrada, elevado a números fracionados ou negativoss
- Pode ter diversas variáveis independentes (X)
- É preciso ter uma amostra com no mínimo N dados (o máximo de expoentes que consegue definir é o tamanho da amostra)
- Fácil de causar overfitting quando tem alto grau (elevado a 3 ou mais)
- Árvores e decisão e Redes Neurais são mais eficientes que a regressão polinomial. Se a relação é muito complexa que precisa de vários polinômios, essas soluções de IA são mais precisas

> Conforme falado, a regressão polinomial não é recomendável, sendo prevferível usar redes neurais ou outros métodos para modelar esses casos mais complexos.

## DIFERENÇA ENTRE CORRELAÇÃO E REGRESSÃO

- Correlação analisa os dados passados
- Regressão tenta prever o futuro (criando uma equação que melhor represente os dados)
- Correlação é a base para regressão
- Regressão é uma versão mais avançada e poderosa da correlação

## O QUE REGRESSÃO MEDE A MAIS

Além de **tudo que a correlação mede** (se são relacionadas, direção e força), a regressão também mede: 

- Quanto uma var muda se aumentarmos/diminuirmos outra
- Prever/estimar o valor final da variável para cada valor da outra
- Quais vars formam o melhor modelo (quais descrevem melhor o comportamento de Y)

### PONTOS DE ATENÇÃO

- A regressão não indica relação causa x efeito (correlação não é causalidade)
- A regressão não ajuda a encontrar variáveis ocultas 
 - As vezes há outras vars influenciando além das usadas ou mesmo uma que define o comportamento das suas

## NOMENCLATURA

- Var Independente (ou explicativa)
  - São o que causa mudança na var estudada
  - Podem ser várias
  - É o nosso X da equação
- Var Dependente (ou resposta)
  - É influenciada pelas demais variáveis
  - Só temos 1
  - É o nosso Y da equação

## PREMISSAS

Além dos dados de entrada e saída terem de ser números reais, para dizer que a regressão é confiável 4 condições tem de ser seguidas pelos resíduos:

- Erros serem normais
- Variância dos erros constante (homocedasticidade)
- Erros independentes (para séries temporais)
- Vars independentes não devem ser correlacionadas (sem multicolinariedade, para regressão múltipla)

Como testes de hipótese, análise de dados e explicação de resíduos não fazem parte do escopo daqui (aqui foco nos algoritmos e fluxos de trabalho), a descrição completa de todos eles e como aplicá-los também será dado nos meus estudos sobre estatística no capítulo 11, [clicando aqui](https://github.com/rodrigorincon/statistics/blob/main/11-regressao-linear/02-como-fazer.md).

### CHECKLIST DE TODOS OS TESTES A PASSAR

Juntando os testes das premissas com o da própria regressão, esta é a lista de testes a serem executadas para regressões simples ou múltiplas.

- Anova
  - Teste T como post hoc
- Jarque-Bera
- Breusch-Pagan
- Durbin-Watson (para séries temporais)
- Matriz de correlação ou VIF (não são testes de hipóteses, mas tem de testar)
