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

def heuristica(tabuleiro):
	if tabuleiro.is_checkmate():
		if tabuleiro.turn == AI_COLOR:
			return 9999  # IA deu mate
		else:
			return -9999 # adversario deu mate
	if tabuleiro.is_stalemate() or tabuleiro.is_insufficient_material():
		return 0

	# conta a pontuação a partir do num de peças de cada lado
	pontuacao = 0
	for peca in tabuleiro.piece_map().values():
		valor = VALORES_PECAS[peca.piece_type]
		if peca.color == AI_COLOR:
			pontuacao -= valor
		else:
			pontuacao += valor
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