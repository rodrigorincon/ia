from abc import ABC, abstractmethod
from typing import List, Tuple
import copy

Position = Tuple[int, int]
TabRow = List[str]
Tabuleiro = List[TabRow]

class JogoVelha: # IA é sempre O e o jogador é sempre X
  tabuleiro: Tabuleiro
  pos_vazia: str = '.'

  def __init__(self):
    linha_vazia = [self.pos_vazia, self.pos_vazia, self.pos_vazia]
    self.tabuleiro = [linha_vazia, linha_vazia.copy(), linha_vazia.copy()]

  def tabuleiro_todo_preenchido(self):
    return all(all(val != self.pos_vazia for val in linha) for linha in self.tabuleiro)

  # retorna o simbolo do vencedor ou None caso nao haja um vencedor ainda
  def winner(self):
    # testa se tem alguma linha q todos os valores sejam iguais e q esse valor nao seja celula vazia
    for linha in self.tabuleiro:
      if( all(val == linha[0] and val != self.pos_vazia for val in linha) ): return linha[0]
    # testa se tem alguma coluna q todos os valores sejam iguais e q esse valor nao seja celula vazia
    for col in range(len(self.tabuleiro)):
      col_igual = all(self.tabuleiro[linha][col] == self.tabuleiro[0][col] and self.tabuleiro[linha][col] != self.pos_vazia for linha in range(len(self.tabuleiro)))
      if(col_igual): return self.tabuleiro[0][col]
    # testa as diagonais
    if(self.tabuleiro[0][0] == self.tabuleiro[1][1] == self.tabuleiro[2][2] and self.tabuleiro[0][0] != self.pos_vazia): return self.tabuleiro[0][0]
    if(self.tabuleiro[2][0] == self.tabuleiro[1][1] == self.tabuleiro[0][2] and self.tabuleiro[2][0] != self.pos_vazia): return self.tabuleiro[2][0]
    return None

  def print_winner(self):
    vencedor = self.winner()
    if(vencedor == 'O'): print('Você perdeu!')
    elif(vencedor == 'X'): print('Parabéns, você ganhou!')
    else: print('Empate!')

  def jogo_encerrado(self):
    return self.tabuleiro_todo_preenchido() or self.winner() != None

  def empate(self):
    return self.tabuleiro_todo_preenchido() and self.winner() == None

  def jogadas_possiveis(self) -> List[Position]:
    return [(lin,col) for lin in range(len(self.tabuleiro)) for col in range(len(self.tabuleiro)) if(self.tabuleiro[lin][col] == self.pos_vazia) ]

  def play_ia(self):
    jogadas = self.jogadas_possiveis()
    if not jogadas: return
    _, proxima_jogada = self.minimax(jogadas, True, 6)
    self.tabuleiro[proxima_jogada[0]][proxima_jogada[1]] = 'O'

  #### ---------------------------- AQUI COMECA MINIMAX ----------------------------

  # Minimax, faz uma árvore com todas as possibilidades e fica com a que der a melhor pontuação dentre os nós filhos
  # É recursiva, dada node fica com a melhor (ou pior) opção dentre os filhos
  # A cada rodada ele testa todas as jogadas de um dos jogadores. Quando está testando uma jogada sua, fica com a melhor opção dentre os nodes filhos
  # Quando está testando uma jogada do adversario, fica com a pior opção dentre os nodes. Isso faz com que ele sempre escolha a melhor jogada dele e a melhor do adversário (que pra ele será a pior)
  # Como a melhor jogada pro adversário será a pior pra ele, escolhe a com pior nota, pois significa que trará o pior resultado pra ele
  # Por isso o minimax sempre considera o PIOR CASO. Isso pode fazer ele podar caminhos que começam mal mas melhoram depois mas evita o pior possivel
  def minimax(self, jogadas_possiveis: List[Position], vez_ia: bool, maxdepth: int) -> Tuple[int, Position | None]:
    # testa se o jogo ja acabou nesse node
    marca_vencedor = self.winner()
    deu_empate = self.empate()
    if(deu_empate): return 0, None
    elif(marca_vencedor): # jogo acabou e alguem venceu
      if(marca_vencedor == 'X'): return 999, None # jogador ganhou
      return -999, None # IA ganhou
    if(maxdepth == 0): return self.heuristica(vez_ia), None
    
    melhor_jogada = None
    ponto_melhor_jogada_vez_ia = float('inf')
    ponto_melhor_jogada_vez_jogador = float('-inf')

    # testa todas as jogadas e escolhe aquela com melhor score
    for jogada in jogadas_possiveis:
      novo_jogo = self.faz_jogada(jogada, vez_ia)
      jogadas_filhas = novo_jogo.jogadas_possiveis()
      ponto_minimax, _ = novo_jogo.minimax(jogadas_filhas, not vez_ia, maxdepth-1)
      if(vez_ia and ponto_minimax < ponto_melhor_jogada_vez_ia):
        ponto_melhor_jogada_vez_ia = ponto_minimax
        melhor_jogada = jogada
      elif(not vez_ia and ponto_minimax > ponto_melhor_jogada_vez_jogador):
        ponto_melhor_jogada_vez_jogador = ponto_minimax
        melhor_jogada = jogada

    val_to_return = ponto_melhor_jogada_vez_ia if vez_ia else ponto_melhor_jogada_vez_jogador
    return val_to_return, melhor_jogada

  def heuristica(self, vez_ia) -> int:
    # heuristica para medir quao perto eu to de ganhar: contar quantos desenhos meus tem em cada caminho que ainda é possivel ganhar
    # menos quantos desenhos do oponente tem em cada caminho que ele ainda pode ganhar
    # com isso, se tiver algum caminho que os 2 ja tenham marcado, esse caminho é ignorado, pra contar só pode ter marca de 1 jogador e espaço vazio
    # quanto maior, mais chances eu tenho de vencer
    # a funcao considera o vez_ia pra saber quem é o jogador atual e quem é o oponente, podendo calcular para ambos os jogadores como exige o minimax
    counter = 0
    marca_atual = self.get_marca(vez_ia)
    marca_oponente = self.get_marca(not vez_ia)
    for line in range(len(self.tabuleiro)):
      if(all(self.tabuleiro[line][col] != marca_oponente for col in range(len(self.tabuleiro)))):
        counter += self.tabuleiro[line].count(marca_atual)**2    
    for col in range(len(self.tabuleiro)):
      if(self.tabuleiro[0][col] != marca_oponente and self.tabuleiro[1][col] != marca_oponente and self.tabuleiro[2][col] != marca_oponente):
        counter += self.tabuleiro[line].count(marca_atual)**2
    if(self.tabuleiro[0][0] != marca_oponente and self.tabuleiro[1][1] != marca_oponente and self.tabuleiro[2][2] != marca_oponente):
      counter += self.tabuleiro[line].count(marca_atual)**2
    if(self.tabuleiro[2][0] != marca_oponente and self.tabuleiro[1][1] != marca_oponente and self.tabuleiro[0][2] != marca_oponente):
      counter += self.tabuleiro[line].count(marca_atual)**2

    for line in range(len(self.tabuleiro)):
      if(all(self.tabuleiro[line][col] != marca_atual for col in range(len(self.tabuleiro)))):
        counter -= self.tabuleiro[line].count(marca_oponente)**2
    for col in range(len(self.tabuleiro)):
      if(self.tabuleiro[0][col] != marca_atual and self.tabuleiro[1][col] != marca_atual and self.tabuleiro[2][col] != marca_atual):
        counter -= self.tabuleiro[line].count(marca_oponente)**2
    if(self.tabuleiro[0][0] != marca_atual and self.tabuleiro[1][1] != marca_atual and self.tabuleiro[2][2] != marca_atual):
      counter -= self.tabuleiro[line].count(marca_oponente)**2
    if(self.tabuleiro[2][0] != marca_atual and self.tabuleiro[1][1] != marca_atual and self.tabuleiro[0][2] != marca_atual):
      counter -= self.tabuleiro[line].count(marca_oponente)**2

    return counter;

  # cria uma copia do jogo e do tabuleiro para poder altera-lo e testar a jogada possivel sem alterar o original
  # o motivo de copiar a classe toda ao inves de só o tauleiro é pq vai precisar chamar as funções da classe pro tabuleiro alterado
  def faz_jogada(self, jogada: Position, vez_ia: bool):
    copia_jogo = copy.deepcopy(self)
    copia_jogo.tabuleiro[jogada[0]][jogada[1]] = self.get_marca(vez_ia)
    return copia_jogo
  
  def get_marca(self, vez_ia: bool):
    return 'O' if vez_ia else 'X'

#### ---------------------------- AQUI ACABA MINIMAX ----------------------------

  def print_tabuleiro(self):
    [ print(' '.join(linha)) for linha in self.tabuleiro]

  def get_player_coord(self) -> Position | None:
    texto = input("Digite aonde irá jogar: ")
    try:
      lin, col = [int(coord.strip()) for coord in texto.split(',')[:2]]
      if( lin < 0 or lin > 2 or col < 0 or col > 2 ):
        print('Posição inválida, digite outra')
        return None
      elif(self.tabuleiro[lin][col] != self.pos_vazia ):
        print('Posição já ocupada, digite outra')
        return None
      return (lin, col)
    except ValueError:
      print('Posição inválida, digite outra')
      return None

  def play(self):
    turno_jogador = True
    while not self.jogo_encerrado():
      if(turno_jogador):
        player_pos = self.get_player_coord()
        if not player_pos: continue
        self.tabuleiro[player_pos[0]][player_pos[1]] = 'X'
      else:
        self.play_ia()
      self.print_tabuleiro()
      print('------------')
      turno_jogador = not turno_jogador

jogo = JogoVelha()
print('\nVocê é a peça X. Ao informar aonde que jogar, escra o número da posição (de 0 a 2) separado por uma virgula. O primeiro número deve ser a linha e a segunda a coluna.')
jogo.play()
jogo.print_winner()