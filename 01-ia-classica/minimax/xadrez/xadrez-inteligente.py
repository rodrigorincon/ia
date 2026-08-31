import chess

# PEÇAS valem centenas de vezes mais que todos os outros pesos
# Casa que a peça ocupa pontua de -50 até 50 (penaliza pessimas posições e dá um empurrão para colocar nas melhores posições)
# A mobilidade é o que vale menos, na escala de casas pouco recomendadas mas não chega a ser péssima ideia
# Vale menos porque cada peça terá várias opções de mobilidade, então elas vem em grupo e no total somam tanto ou um pouco mais que uma casa ótima

# Valores das peças (Escala x100 para evitar floats lentos no Minimax)
VALORES_PECAS = {
	chess.PAWN: 100,
	chess.KNIGHT: 320,  # Cavalos valem um pouco mais que 3 peões pelo potencial tático
	chess.BISHOP: 330,  # Bispos em geral valem ligeiramente mais que cavalos (par de bispos/longo alcance)
	chess.ROOK: 500,
	chess.QUEEN: 900,
	chess.KING: 20000   # Valor massivo para evitar sacrifícios absurdos
}
AI_COLOR = chess.BLACK

# MATRIZES POSICIONAIS (PIECE-SQUARE TABLES). Dão o valor de cada peça em cada posição. 
# Algumas peças valem mais em certas posições, enquanto outras valem muito mas assumindo outros lugares no tabuleiro, por isso precisa
# de uma tabela para cada peça
# As tabelas estão orientadas do ponto de vista das Brancas (linha 1 a 8). 
# Para as Pretas, o algoritmo espelha essas matrizes verticalmente.

PAWN_TABLE = [
	0,  0,  0,  0,  0,  0,  0,  0,  # Linha 1 (Inalcançável para peões)
	5, 10, 10,-20,-20, 10, 10,  5,  # Linha 2 (Proteção do rei nas alas, evita avanços prematuros)
	5, -5,-10,  0,  0,-10, -5,  5,  # Linha 3
	0,  0,  0, 25, 25,  0,  0,  0,  # Linha 4 (Bônus forte por ocupar o centro)
	5,  5, 10, 30, 30, 10,  5,  5,  # Linha 5 (Peões centrais avançados sufocam o oponente)
	10, 10, 20, 35, 35, 20, 10, 10,  # Linha 6 (Proximidade de promoção)
	50, 50, 50, 50, 50, 50, 50, 50,  # Linha 7 (Peão na sétima é quase uma dama)
	0,  0,  0,  0,  0,  0,  0,  0   # Linha 8
]
KNIGHT_TABLE = [
	-50,-40,-30,-30,-30,-30,-40,-50, # Linha 1 (Cavalos na borda são uma desgraça)
	-40,-20,  0,  5,  5,  0,-20,-40, # Linha 2
	-30,  5, 10, 15, 15, 10,  5,-30, # Linha 3 (Ativos, mirando o centro)
	-30,  0, 15, 25, 25, 15,  0,-30, # Linha 4 (Postos avançados no centro)
	-30,  5, 15, 25, 25, 15,  5,-30, # Linha 5
	-30,  0, 10, 15, 15, 10,  0,-30, # Linha 6
	-40,-20,  0,  0,  0,  0,-20,-40, # Linha 7
	-50,-40,-30,-30,-30,-30,-40,-50  # Linha 8
]
BISHOP_TABLE = [
	-20,-10,-10,-10,-10,-10,-10,-20,
	-10,  5,  0,  0,  0,  0,  5,-10, # Linha 2 (Fianchetto nas alas b e g é incentivado, tomando as diagonais maiores do tabuleiro)
	-10, 10, 10, 10, 10, 10, 10,-10, # Linha 3 (Desenvolvimento ativo)
	-10,  0, 10, 15, 15, 10,  0,-10, # Linha 4 (Controlando diagonais centrais)
	-10,  5,  5, 10, 10,  5,  5,-10, # Linha 5
	-10,  0,  5,  5,  5,  5,  0,-10, # Linha 6
	-10, -5, -5, -5, -5, -5, -5,-10, # Linha 7 (Evita subir demais sem necessidade)
	-20,-10,-10,-10,-10,-10,-10,-20
]
ROOK_TABLE = [
	0,  0,  0,  5,  5,  0,  0,  0, # Linha 1 (Prefere colunas centrais d e e)
	5, 10, 10, 10, 10, 10, 10,  5, # Linha 2
	-5,  0,  0,  0,  0,  0,  0, -5,
	-5,  0,  0,  0,  0,  0,  0, -5,
	-5,  0,  0,  0,  0,  0,  0, -5,
	-5,  0,  0,  0,  0,  0,  0, -5,
	20, 20, 20, 20, 20, 20, 20, 20, # Linha 7 (Torre na sétima fileira é taticamente devastadora)
	0,  0,  0,  0,  0,  0,  0,  0
]
QUEEN_TABLE = [
	-20,-10,-10, -5, -5,-10,-10,-20, # Linha 1 (Não deve sair cedo)
	-10,  0,  5,  0,  0,  0,  0,-10,
	-10,  5,  5,  5,  5,  5,  5,-10,
	-5,  0,  5,  5,  5,  5,  0, -5, # Meio do tabuleiro moderado
	0,  0,  5,  5,  5,  5,  0, -5,
	-10,  5,  5,  5,  5,  5,  5,-10,
	-10,  0,  0,  0,  0,  0,  0,-10,
	-20,-10,-10, -5, -5,-10,-10,-20
]
# considera apenas o meio de jogo. Se fosse fazer uma tabela para inicio, meio e fim ficaria muito complexo
KING_MIDDLEGAME_TABLE = [
	20, 30, 10,  0,  0, 10, 30, 20, # Linha 1 (Roque grande ou pequeno altamente valorizado)
	20, 20,  0,  0,  0,  0, 20, 20, # Linha 2 (Protegido por peões)
	-10,-20,-20,-20,-20,-20,-20,-10,
	-20,-30,-30,-40,-40,-30,-30,-20,
	-30,-40,-40,-50,-50,-40,-40,-30, # Ir para o centro no meio de jogo é suicídio
	-30,-40,-40,-50,-50,-40,-40,-30,
	-30,-40,-40,-50,-50,-40,-40,-30,
	-30,-40,-40,-50,-50,-40,-40,-30
]
MAPA_MATRIZES = {
	chess.PAWN: PAWN_TABLE,
	chess.KNIGHT: KNIGHT_TABLE,
	chess.BISHOP: BISHOP_TABLE,
	chess.ROOK: ROOK_TABLE,
	chess.QUEEN: QUEEN_TABLE,
	chess.KING: KING_MIDDLEGAME_TABLE
}

# o que muda uma IA boa da ruim é sua função heuristica. Enquanto a anterior só coniderava as peças, essa considera suas posições e quantidade de movimento que podem fazer
def heuristica(tabuleiro):
	if tabuleiro.is_checkmate():
		if tabuleiro.turn == AI_COLOR:
			return 9999  # IA deu mate
		else:
			return -9999 # adversario deu mate
	if tabuleiro.is_stalemate() or tabuleiro.is_insufficient_material():
		return 0

	pontuacao_material = 0
	pontuacao_posicional = 0

	# pontua pelas peças que tem e pela posição delas no tabuleiro (considera bem posicionado se tiver no centro)
	for num_casa, peca in tabuleiro.piece_map().items():
		# Valor base da peça
		valor = VALORES_PECAS[peca.piece_type]
		
		# Mapeia o índice da matriz de acordo com a perspectiva da cor
		# Brancas = OPONENTE (not AI_COLOR) leem a tabela normalmente de 0 a 63. Pretas precisam espelhar.
		if peca.color != AI_COLOR:
				indice_tabela = num_casa
				pontuacao_material -= valor
				pontuacao_posicional -= MAPA_MATRIZES[peca.piece_type][indice_tabela]
		else:
				# Espelha verticalmente para as pretas (inverte as linhas)
				linha = chess.square_rank(num_casa)
				coluna = chess.square_file(num_casa)
				indice_tabela = (7 - linha) * 8 + coluna
				pontuacao_material += valor
				pontuacao_posicional += MAPA_MATRIZES[peca.piece_type][indice_tabela]

	# Mobilidade Controlada (+2 pontos por casa disponível)
	# No xadrez real, mobilidade demais sem controle gera caos. 
	# Damos um peso sutil (2 pontos por movimento) para incentivar o desenvolvimento sem desequilibrar o material
	fator_mobilidade = 2
	mobilidade_jogador_corrente = tabuleiro.legal_moves.count()

	# Para descobrir a mobilidade do próximo a jogar, alteramos temporariamente o turno
	tabuleiro.turn = not tabuleiro.turn
	mobilidade_prox_jogador = tabuleiro.legal_moves.count()
	tabuleiro.turn = not tabuleiro.turn # Restaura o turno original

	pontuacao_mobilidade = 0
	if tabuleiro.turn == AI_COLOR:
			pontuacao_mobilidade += (mobilidade_jogador_corrente - mobilidade_prox_jogador) * fator_mobilidade
	else:
			pontuacao_mobilidade -= (mobilidade_jogador_corrente - mobilidade_prox_jogador) * fator_mobilidade

	# Retorna a soma de todos os fatores estratégicos
	return pontuacao_material + pontuacao_posicional + pontuacao_mobilidade

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