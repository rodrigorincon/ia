from sklearn.feature_extraction.text import CountVectorizer
from sklearn.naive_bayes import MultinomialNB

# dados com a frase e sua categoria (1 = positivo, 0 = negativo)
comentarios_positivos = [
  ("Eu adoro este produto", 1),("Muito bom, ficou ótimo em mim", 1),("Gostei demais, uso sempre", 1),("Foi um achado, produto incrível", 1),
  ("Produto incrível", 1),("Maravilhoso, super recomendo", 1),("Amei, super econômico", 1),("Uso bastente, gostei", 1),
  ("Excelente qualidade e durabilidade", 1),("Atendeu todas as minhas expectativas", 1),("Muito prático e eficiente", 1),
  ("Ótimo custo-benefício", 1),("Acabamento impecável", 1),("Super recomendo para amigos e família", 1),
  ("Entrega rápida e produto perfeito", 1),("Design elegante e funcional", 1),("Excelente atendimento ao cliente", 1),
  ("Fácil de usar e limpar", 1),("Vale cada centavo", 1),("Material de alta qualidade", 1),("Recomendo fortemente este produto", 1),
  ("Satisfeito com a compra", 1),("Funciona exatamente como descrito", 1),("Uso diariamente, excelente", 1),("Muito confortável e bonito", 1),
  ("A embalagem chegou em ótimo estado", 1),("Perfeito para o que eu precisava", 1),("Acabamento e performance excelentes", 1),
  ("Superou minhas expectativas", 1),("Produto muito bem construído", 1),("Entrega antes do prazo", 1),("Ótimo suporte pós-venda", 1),
  ("Estou muito satisfeito", 1),("Ideal para presente", 1),("Compra certeira, recomendo", 1),("Excelente custo x benefício", 1),
  ("Amei, uso sempre", 1),("O produto é maravilhoso e lindo", 1),("É lindo, ficou perfeito na estante", 1),("Usarei todos os dias", 1),
]
comentarios_negativos = [
  ("Muito ruim, quebrou no primeiro uso", 0),("Péssima qualidade, não recomendo", 0),("Decepcionante e frágil", 0),
  ("Material barato e mal acabado", 0),("Não funciona como anunciado", 0),("Produto chegou danificado", 0),("Atendimento ruim e sem solução", 0),
  ("Demorou muito para entregar", 0),("Arrependi da compra", 0),("Barulho estranho ao usar", 0),("Tamanho diferente do anunciado", 0),
  ("Não vale o preço", 0),("Acabamento péssimo", 0),("Muito desconfortável", 0),("Bateria não dura nada", 0),("Instruções confusas e incompletas", 0),
  ("Recursos limitados, pouco útil", 0),("Produto horrível, não comprem", 0),("Não satisfeito com a compra", 0),("Produto falsificado", 0),
  ("Cheiro forte e desagradável", 0),("Péssima experiência de compra", 0),("Retorno da assistência técnica lento", 0),
  ("Falha recorrente após poucos dias", 0),("Não recomendo a ninguém", 0),("Qualidade inferior ao esperado", 0),
  ("Desconforto ao usar por muito tempo", 0),("Peças soltas após pouco uso", 0),("Componentes soltos ao desembalar", 0),
  ("Muito pesado e difícil de manusear", 0),("Tela com pixels mortos", 0),("Conexão instável", 0),("Atualizações quebram funcionalidades", 0),
  ("Aplicativo difícil de configurar", 0),("Chegou com cheiro de mofo", 0),("Não atendeu às especificações", 0),("Não gostei", 0),("Produto péssimo", 0),
  ("Muito ruim, nunca mais compro", 0),("Péssimo, estou decepcionado", 0)
]

frases = [item[0] for item in comentarios_positivos] + [item[0] for item in comentarios_negativos]
categorias = [item[1] for item in comentarios_positivos] + [item[1] for item in comentarios_negativos]

# Transformar o texto em números (vetorização), contando a quantidade de vezes que cada palavra aparece nos textos
vetorizador = CountVectorizer()
X_treino = vetorizador.fit_transform(frases)
print(X_treino)

# Usa o Naive Bayes Multinomial para texto
modelo = MultinomialNB()
modelo.fit(X_treino, categorias)

# Testa o modelo com uma nova frase
novas_frases = ["Produto muito bom adorei", "Horrível e de baixa qualidade"]
X_teste = vetorizador.transform(novas_frases)
predicoes = modelo.predict(X_teste)

# Exibir resultados
for frase, pred in zip(novas_frases, predicoes):
  resultado = "Positivo" if pred == 1 else "Negativo"
  print(f'Frase: "{frase}" -> Classificação: {resultado}')
