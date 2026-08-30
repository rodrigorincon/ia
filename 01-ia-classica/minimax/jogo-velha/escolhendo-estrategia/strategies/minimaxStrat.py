import types
from typing import List, Tuple
import copy
import random

Position = Tuple[int, int]
TabRow = List[str]
Tabuleiro = List[TabRow]

def jogar_minimax(self, jogadas: List[Position]) -> Position:
  _, jogada_escolhida = self.minimax(jogadas, True, 9)
  return jogada_escolhida

def setMinimaxStrat(self):
  self.minimax = types.MethodType(minimax, self)
  self.heuristica = types.MethodType(heuristica, self)
  self.faz_jogada = types.MethodType(faz_jogada, self)
  self.get_marca = types.MethodType(get_marca, self)
  self.definir_proxima_jogada = types.MethodType(jogar_minimax, self)

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