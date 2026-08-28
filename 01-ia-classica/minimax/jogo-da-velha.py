from abc import ABC, abstractmethod
from typing import List, Tuple
import random

Position = Tuple[int, int]
TabRow = List[str]
Tabuleiro = List[TabRow]

class StrategyInterface(ABC):
  @abstractmethod
  def escolher_prox_jogada(self, tabuleiro: Tabuleiro, jogadas_possiveis: List[Position]) -> Position:
    pass

class RandomStrat(StrategyInterface):
  def escolher_prox_jogada(self, tabuleiro: Tabuleiro, jogadas_possiveis: List[Position]) -> Position:
    return random.choice(jogadas_possiveis)

class JogoVelha: # IA é sempre O e o jogador é sempre X
  tabuleiro: Tabuleiro
  strat: StrategyInterface
  pos_vazia: str = '.'

  def __init__(self, strat: StrategyInterface):
    linha_vazia = [self.pos_vazia, self.pos_vazia, self.pos_vazia]
    self.tabuleiro = [linha_vazia, linha_vazia.copy(), linha_vazia.copy()]
    self.strat = strat

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

  def jogadas_possiveis(self) -> List[Position]:
    return [(lin,col) for lin in range(len(self.tabuleiro)) for col in range(len(self.tabuleiro)) if(self.tabuleiro[lin][col] == self.pos_vazia) ]

  def play_ia(self):
    jogadas = self.jogadas_possiveis()
    if not jogadas: return
    proxima_jogada = self.strat.escolher_prox_jogada(self.tabuleiro, jogadas)
    self.tabuleiro[proxima_jogada[0]][proxima_jogada[1]] = 'O'

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

jogo = JogoVelha(RandomStrat())
print('\nVocê é a peça X. Ao informar aonde que jogar, escra o número da posição (de 0 a 2) separado por uma virgula. O primeiro número deve ser a linha e a segunda a coluna.')
jogo.play()
jogo.print_winner()