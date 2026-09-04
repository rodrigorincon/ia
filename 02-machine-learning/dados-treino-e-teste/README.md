# SEPARAÇÃO DE DADOS (TREINO E TESTE)

A separação dos dados em dois grupos (treino e teste) serve para poder testar se o modelo realmente funciona para prever novos dados. Ao usar somente um pedaço dos dados para treinar você tem dados nunca vistos pelo modelo que serão usados para testar a precisão dele. O motivo de usar dados diferentes para testar vem do fato que se você usar os mesmos dados corre o risco do modelo só tá repetindo o que já viu antes (decorando) e não realmente aprendendo padrões. Usando os mesmos dados você não vai saber se ele aprendeu ou só decorou.

Exemplo: se você vai fazer uma prova de matemática e estuda resolvendo as provas de anos anteriores, o que acontece se o professor aplicar exatamente a mesma prova na sala? Você vai tirar 10. Mas isso significa que você é um gênio da matemática ou que você apenas decorou o gabarito daquela folha? 

Em Machine Learning a separação de dados serve exatamente para resolver esse dilema: garantir que o seu modelo realmente **aprendeu a lógica** do problema e não apenas **decorou os dados** que você entregou a ele.

## O Problema: Vício nos Dados

Quando você entrega todos os dados disponíveis para um algoritmo treinar, ele vai tentar traçar a reta (ou curva) perfeita que passe por todos os pontos. Isso muitas vezes cria um modelo excessivamente complexo que acerta 100% no passado, mas erra feio no futuro, pois ele capturou até os ruídos e exceções aleatórias. Esse fenômeno é o terror da ciência de dados, conhecido como **Overfitting** (Sobreajuste).

Um erro comum no machine learning é olhar para o "Erro de Treino". Um erro baixo nos dados que o modelo já viu não tem valor científico nenhum, pois ele já conhece as respostas. Por isso pegamos parte dos dados que nunca foram vistos antes pelo modelo e usamos como uma régua para medir a precisão.

Como temos os dados sabemos qual tem de ser a saída pra esses valores, assim medidos o valor dado pela IA e o valor real da saída daquele dado e temos o erro.

## Proporções

> A proporção mais usada é de **80% para treino e 20% para teste**.

## Divisão Simples

A divisão mais simples e geralmente feita em exemplos é apenas cortar os dados em 2 grupos: um maior (80%) para treino e um menor (20%) para teste. Esse método é chamado de **Holdout Simples**. Essa `divisão deve ser aleatória`. A alatoriedade é fundamental para que sua base de treino não tenha só 1 tipo de dado e a de teste outro.

Nesse modelo os dados de teste ficam guardados até o fim do treinamento para que sejam então usados. Como o treinamento pode demorar horas ou dias, uma opção é marcar no banco de dados quais linhas são de treino e teste ou salvar em um arquivo temporário os dados de teste ou mesmo usar um banco temporário (como Redis) para guardá-los.

## TÉCNICAS AVANÇADAS DE SEPARAÇÃO

Outras técnicas mais complexas foram criadas para **evitar concentração de algum tipo de dado** em um dos grupos. Algumas das técnicas também permite ter certeza que seus **valores finais são mais estáveis**, não fruto duma amostra aleatória, checando se os retornos variam caso a base de treino mude muito. Essas técnicas muitas vezes acabam por **evitar overfitting** ao usar mais de uma base de treino, forçando o modelo a ser mais generalista ao sempre mostrar dados diferentes.

### Validação Cruzada K-Fold

É o padrão ouro da avaliação de modelos. Em vez de dividir a base em treino e teste uma única vez, o K-Fold faz isso K vezes, garantindo que todos os dados sejam usadas como teste e como treino pelo menos uma vez.

**Passo-a-passo**:
1. Embaralhe os dados.
2. Divida os dados em K partes (folds) do mesmo tamanho. Geralmente K=5 ou K=10.
3. Na Rodada 1: Use o Fold 1 como TESTE. Junte todos os outros (Folds 2 a K) para TREINO. Calcule o erro.
4. Na Rodada 2: Use o Fold 2 como TESTE. Junte o restante para TREINO. Calcule o erro.
5. Repita até a Rodada K.
6. A performance real do seu modelo será a **média** dos K erros.

> **Quando usar**: Na grande maioria dos projetos normais de Machine Learning e modelagem preditiva. É o método mais seguro e balanceado matematicamente.

Repare que desse modo não necessariamente a parte de teste será 20%. Se k=10 o grupo de teste será 10%. Porém a verdade é que toda a base será usada como teste em algum momento. Mas mesmo usando tudo como treino não causa overfitting pois não é tudo usado ao mesmo tempo. Se quiser manter a proporção de 20% de teste use K=5.

### K-Fold Estratificado

Uma evolução direta do K-Fold normal, focado em resolver problemas de **categorias desbalanceadas**.

Imagine que você tem 1.000 pacientes: 990 saudáveis e apenas 10 doentes. Se você usar um K-Fold normal (cortando os dados cegamente), pode ser que uma das partes de teste caia com 0 doentes. O modelo vai ser avaliado de forma totalmente distorcida nessa rodada.

**Como funciona**

O K-Fold Estratificado força uma regra matemática durante o sorteio das fatias: **a proporção original das categorias deve ser mantida em TODOS os folds**. Se na base original 1% é doente, cada parte (fold) de teste e cada pedaço de treino terá exatamente 1% de doentes.

> **Quando usar**: Sempre que estiver trabalhando com classificação onde as categorias não são perfeitamente iguais (ex: fraude em cartão de crédito, diagnóstico de doenças raras, conversão de vendas).

### Leave-One-Out

É o caso extremo e absoluto do K-Fold. O nome significa "Deixe Um de Fora". Se você tem um dataset com N linhas (ex: 50 pacientes), o Leave-One-Out é literalmente um K-Fold onde K = N (50-Fold).

**Como funciona**

Ele usa N-1 dados para treinar o modelo e usa apenas **1 único dado para testar**. Ele repete isso N vezes, de forma que o modelo é exaustivamente testado em cada indivíduo de forma isolada. 

**O grande gargalo**: Se você tem 1 milhão de clientes, ele vai ter que criar, treinar e jogar fora 1 milhão de modelos de Machine Learning diferentes. É um pesadelo computacional quase impossível na prática moderna para bases médias/grandes. Fora que os modelos vão ser todos muito parecidos entre si. Vai gastar muito tempo e energia para chegar praticamente no mesmo lugar.

> **Quando usar**: Exclusivamente quando você tem conjuntos de dados minúsculos (ex: 30 casos clínicos).

### Validação Cruzada Aninhada (Nested Cross-Validation)

Este é o método mais rigoroso que existe. Ele resolve um problema muito sutil chamado **Data Leakage (Vazamento de Dados) nos Hiperparâmetros**.

Quando você afina um modelo, definindo algum de seus parâmetros (escolhe a profundidade de uma árvore, a taxa de aprendizado, etc), você geralmente roda um K-Fold para descobrir quais hiperparâmetros dão a melhor nota. Mas se você usar essa mesma nota final para relatar a performance do modelo, você está mentindo! O modelo já foi "otimizado" para aqueles dados de validação específicos.

**Como funciona (Um K-Fold dentro de um K-Fold)**:
1. **Loop Externo (Para Avaliar o Modelo)**: Divide os dados em K Folds. Pega o Fold 1 e guarda (Teste Verdadeiro).
2. **Loop Interno (Para Afinar o Modelo)**: Pega os demais Folds restantes e aplica um NOVO K-Fold neles (ex: K-2 folds internos). Ele treina várias vezes só aqui dentro para achar os hiperparâmetros perfeitos.
3. **Avaliação Final**: Com os hiperparâmetros perfeitos descobertos no Loop Interno, ele treina o modelo inteiro nos K-1 Folds e testa, pela primeira vez, naquele Fold 1 que estava separado para o teste final.
4. Repete o Loop Externo inteiro para todos os K folds.

> **Quando usar**: Sempre que você for fazer "Hyperparameter Tuning" (busca em grade/grid search) E precisar relatar uma estimativa de erro matematicamente honesta e imparcial. É muito cobrado em artigos acadêmicos rigorosos de Machine Learning.

É o mais pesado e demorado de todos.

## RESUMO: QUAL DEVO ESCOLHER?

| Método | Quando Aplicar | Desvantagem Principal |
| :--- | :--- | :--- |
| **Holdout** | Quando a base de dados é na casa dos milhões de linhas e o custo de treinar K vezes é inviável por tempo e custo. | Muito dependente da "sorte" no sorteio da divisão. |
| **K-Fold Normal** | O padrão da indústria. Para regressões e bases de dados com distribuições homogêneas. | Pode criar folds desbalanceados em classificações. |
| **K-Fold Estratificado** | Para previsões de classificação (fraudes, diagnósticos, churn) com dados desbalanceados. | Pouco útil para problemas contínuos (Regressão). |
| **Leave-One-Out (LOO)** | Quando o seu banco de dados é minúsculo (ex: $N < 100$) e cada dado importa muito no treino. | Custo computacional absurdo, inviável para bases normais. |
| **CV Aninhado** | Quando você faz otimização de parâmetros (ex: Grid Search) e precisa validar a performance final sem vieses. | Demora absurdamente mais, pois multiplica o número de modelos a treinar. |
