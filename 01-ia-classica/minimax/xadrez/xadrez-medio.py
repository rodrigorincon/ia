import chess

# Valores das peças para a avaliação básica
VALORES_PECAS = {
  chess.PAWN: 1,
  chess.KNIGHT: 3,
  chess.BISHOP: 3,
  chess.ROOK: 5,
  chess.QUEEN: 9,
  chess.KING: 1000
}

AI_COLOR = chess.BLACK

# o que muda uma IA boa da ruim é sua função heuristica. Enquanto a anterior só coniderava as peças, essa considera suas posições e quantidade de movimento que podem fazer
def heuristica(tabuleiro):
	if tabuleiro.is_checkmate():
		if tabuleiro.turn == AI_COLOR:
			return 9999  # IA deu mate
		else:
			return -9999 # adversario deu mate
	if tabuleiro.is_stalemate() or tabuleiro.is_insufficient_material():
		return 0

	# Bônus pela coluna que a peça tá (quanto mais centralizada melhor)
	# Colunas D e E: +3 pontos | Colunas C e F: +1 ponto | Demais (A, B, G, H): 0 pontos
	# Col. A = 0, Col. B = 1 e assim por diante
	BONUS_COLUNA = { 0: 0, 1: 0, 2: 1, 3: 3, 4: 3, 5: 1, 6: 0, 7: 0 }
	pontuacao = 0

	# pontua pelas peças que tem e pela posição delas no tabuleiro (considera bem posicionado se tiver no centro)
	for num_casa, peca in tabuleiro.piece_map().items():
		# Valor base da peça
		valor = VALORES_PECAS[peca.piece_type]
		
		# Bônus por estar nas colunas centrais (D, E) ou semi-centrais (C, F)
		num_coluna = chess.square_file(num_casa)
		bonus_posicao = BONUS_COLUNA[num_coluna]
		
		# O rei é preferível que ele esteja longe do centro, então ele pontua ao contrário (é penalizado quanto mais ao centro está)
		if peca.piece_type == chess.KING:
			bonus_posicao = -bonus_posicao

		valor_total_peca = valor + bonus_posicao
		# soma e/ou tira de acordo se é peça da IA ou do adversario
		if peca.color != AI_COLOR:
			pontuacao -= valor_total_peca
		else:
			pontuacao += valor_total_peca

	# pontua pela quantidade de casas que as peças podem ir. Cada casa soma 0.1
	fator_mobilidade = 0.1
	# Mobilidade do jogador que está jogando agora
	mobilidade_jogador_corrente = tabuleiro.legal_moves.count()

	# Para descobrir a mobilidade do próximo a jogar, alteramos temporariamente o turno
	tabuleiro.turn = not tabuleiro.turn
	mobilidade_prox_jogador = tabuleiro.legal_moves.count()
	tabuleiro.turn = not tabuleiro.turn # Restaura o turno original

	# Aplica os pontos de mobilidade com base em quem é o dono do turno atual
	if tabuleiro.turn == AI_COLOR:
			pontuacao += mobilidade_jogador_corrente * fator_mobilidade
			pontuacao -= mobilidade_prox_jogador * fator_mobilidade
	else:
			pontuacao -= mobilidade_jogador_corrente * fator_mobilidade
			pontuacao += mobilidade_prox_jogador * fator_mobilidade

	return pontuacao

def minimax(tabuleiro, maxdepth, alfa, beta, vez_ia):
	if maxdepth == 0 or tabuleiro.is_game_over():
		return heuristica(tabuleiro)

	ponto_melhor_jogada_vez_ia = float('-inf')
	ponto_melhor_jogada_vez_jogador = float('inf')

	for movimento in tabuleiro.legal_moves:
		tabuleiro.push(movimento)
		aval = minimax(tabuleiro, maxdepth - 1, alfa, beta, not vez_ia)
		tabuleiro.pop() # depois de calcular o resultado desse movimento, desfaz ele
		if vez_ia:
			ponto_melhor_jogada_vez_ia = max(ponto_melhor_jogada_vez_ia, aval)
			alfa = max(alfa, aval)
		else:
			ponto_melhor_jogada_vez_jogador = min(ponto_melhor_jogada_vez_jogador, aval)
			beta = min(beta, aval)
		if beta <= alfa:
			break
	val_to_return = ponto_melhor_jogada_vez_ia if vez_ia else ponto_melhor_jogada_vez_jogador
	return val_to_return

def escolher_melhor_movimento(tabuleiro, profundidade):
	melhor_movimento = None
	melhor_valor = float('-inf')

	for movimento in tabuleiro.legal_moves:
		tabuleiro.push(movimento)
		valor_movimento = minimax(tabuleiro, profundidade-1, float('-inf'), float('inf'), True)
		tabuleiro.pop() # depois de calcular o resultado desse movimento, desfaz ele

		if valor_movimento > melhor_valor:
			melhor_valor = valor_movimento
			melhor_movimento = movimento

	return melhor_movimento

def ia_ganhou(tabuleiro):
	return tabuleiro.turn == AI_COLOR

tabuleiro = chess.Board()
print("Jogo de Xadrez. Você é as peças BRANCAS (letras maiúsculas). \nDigite suas jogadas no formato origem-destino (ex: e2e4, g1f3)\n")

while not tabuleiro.is_game_over():
	print(tabuleiro)
	print('---------------')

	if tabuleiro.turn == AI_COLOR:
		movimento_ia = escolher_melhor_movimento(tabuleiro, 3)
		if movimento_ia:
			tabuleiro.push(movimento_ia)
		else:
			break
	else:
		jogada_valida = False
		while not jogada_valida:
			entrada = input("Digite sua jogada: ").strip()
			try:
				movimento = chess.Move.from_uci(entrada) # converte a entrada para o formato entendido pela biblioteca
				if movimento in tabuleiro.legal_moves:
					tabuleiro.push(movimento)
					print(f"\n    Você jogou: {movimento}")
					jogada_valida = True
				else:
					print("Movimento ilegal! Tente novamente.")
			except ValueError:
				print("Formato inválido! Use o padrão de 4 caracteres (ex: e2e4)")

# Fim de jogo
print("\n=== FIM DE JOGO ===")
print(tabuleiro)
print(f"Resultado: {'você venceu' if ia_ganhou(tabuleiro) else 'você perdeu'}")