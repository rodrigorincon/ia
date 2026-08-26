from dataclasses import dataclass
from typing import List, Tuple, Dict, Optional
import heapq # fila de prioridade

# cria um novo tipo para o quadro do jogo
Board = Tuple[int, ...]  # 9 elementos, 0 representa o espaço vazio
# cria novo tipo para um nó, com um quadro e a contagem de h e g dele
# tupla = (f, g, board) = (peso final, nº acoes feitas até esse board, board atual)
Node = Tuple[int, int, Board]

def count_pecas_erradas(board: Board, goal: Board) -> int:
  num_pecas_erradas = 0
  for i in range(len(board)):
    if(board[i] != 0 and board[i] != goal[i]):
      num_pecas_erradas += 1
  return num_pecas_erradas

def neighbors(board: Board) -> List[Board]:
  # os vizinhos (Movimentos possiveis) são encontrados movendo o espaço vazio (0) movendo para os 4 lados
  zero_pos = board.index(0)
  neigh = []
  row, col = divmod(zero_pos, 3) # pega a linha e a coluna que o zero está fazendo divisao modular

  moves = [(-1, 0), (1, 0), (0, -1), (0, 1)] # movimenta uma casa pra cima, baixo, esquerda e direita
  for move_row, move_col in moves:
    new_0row = row + move_row
    new_0col = col + move_col
    if 0 <= new_0row < 3 and 0 <= new_0col < 3: # ignora movimentos impossiveis
      new_pos = new_0row * 3 + new_0col
      new_board = list(board)
      numero_a_trocar_de_pos = new_board[zero_pos]
      new_board[zero_pos] = new_board[new_pos]
      new_board[new_pos] = numero_a_trocar_de_pos
      neigh.append(tuple(new_board))

  return neigh


def reconstruct_path(board_prev: Dict[Board, Optional[Board]], start: Board, goal: Board) -> List[Board]:
  path = []
  current = goal
  if current not in board_prev:
    return []
  while current is not None:
    path.append(current)
    current = board_prev.get(current)
  path.reverse()
  return path

"""Resolve o puzzle usando A* com f = g + h onde:
g é o nº de acoes feitas
h é número de peças fora do lugar.
Retorna (caminho_de_boards, numero_de_nos_expandidos)
"""
def solve_a_star(start: Board, goal: Board, max_expansions: int = 100_000) -> Tuple[List[Board], int]:
  # usado para reconstruir o caminho final. Guarda qual foi o board que levou a cada um
  board_prev: Dict[Board, Optional[Board]] = {start: None}

  # heap de prioridades por f = g + h
  # Node: (peso total, num passos, board)
  num_pecas_erradas_inicial = count_pecas_erradas(start, goal)
  fila_quadros: List[Node] = []
  heapq.heappush(fila_quadros, (num_pecas_erradas_inicial, 0, start)) # heapq.heappush adiciona um nó a fila de prioridade

  num_nodes_analisados = 0
  # guarda o menor nº passos conhecido para cada possibilidade de board (para evitar reprocessar piores caminhos)
  menor_caminho: Dict[Board, int] = {start: 0}

  while fila_quadros:
    _, num_jogadas, current = heapq.heappop(fila_quadros)

    if current == goal:
      path = reconstruct_path(board_prev, start, goal)
      return path, num_nodes_analisados

    # pequeno corte para evitar expansões excessivas
    if num_nodes_analisados >= max_expansions:
      break

    num_nodes_analisados += 1
    for board_vizinho in neighbors(current):
      num_jogadas_vizinho = num_jogadas + 1
      if board_vizinho not in menor_caminho or num_jogadas_vizinho < menor_caminho[board_vizinho]:
        menor_caminho[board_vizinho] = num_jogadas_vizinho
        board_prev[board_vizinho] = current

        num_pecas_erradas = count_pecas_erradas(board_vizinho, goal)
        peso_total_vizinho = num_jogadas_vizinho + num_pecas_erradas
        heapq.heappush(fila_quadros, (peso_total_vizinho, num_jogadas_vizinho, board_vizinho)) # adiciona na fila prioritaria

  return [], num_nodes_analisados


def print_board(board: Board) -> str:
  print("\n".join([f"{board[0]} {board[1]} {board[2]}", f"{board[3]} {board[4]} {board[5]}", f"{board[6]} {board[7]} {board[8]}"]))


# Exemplo: estado inicial e estado objetivo
# Estado objetivo padrão: 1..8 com 0 no final
goal: Board = (1, 2, 3, 4, 5, 6, 7, 8, 0)

# Exemplo de início (pode ser substituído)
# este exemplo tem solução simples:
start: Board = (5, 3, 8, 7, 1, 2, 6, 0, 4)

print("Estado inicial:")
print_board(start)
print("\nObjetivo:")
print_board(goal)

path, num_nos_expandidos = solve_a_star(start, goal)

if not path:
  print("\nNenhuma solução encontrada (ou limite de expansões atingido).")
else:
  print(f"\nSolução encontrada em {len(path)-1} movimentos (expandindo {num_nos_expandidos} nós):\n")
  for step, b in enumerate(path):
    if(step == 0):
      print('Estado inicial:')
    else:
      print(f"Passo {step}:")
    print_board(b)
    print("")
