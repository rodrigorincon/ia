import heapq
from dataclasses import dataclass
from typing import List, Dict, Tuple

# cria um novo tipo de variavel para o labirinto (matrix de int)
Labirinto = List[List[int]]

# cria novo tipo de variavel para uma posicao no labirinto
Point = Tuple[int, int]

@dataclass
class Node:
  name: str
  x: int
  y: int
  neighbors: List[Edge]

@dataclass
class Edge:
  target: Node
  weight: int

@dataclass
class Graph:
  nodes: List[Node]

# como não podemos andar na diagonal a distancia euclidiana nao é uma boa opcao. Por isso usamos a distancia Manhattan (soma distancia nos 2 eixos)
def heuristica(a: Node, b: Node) -> float:
  return abs(a.x - b.x) + abs(a.y - b.y)

def reconstruct_path(previous: Dict[str, Node], start: Node, goal: Node) -> List[Node]:
  if start == goal:
    return [start]

  if goal.name not in previous:
    return []

  path = []
  current = goal
  while current != start:
    path.append(current)
    current = previous[current.name]

  path.append(start)
  path.reverse()
  return path

def dijkstra(graph: Graph, start: Node, goal: Node) -> Tuple[float, List[Node], int]:
  # dist[n] = menor custo conhecido da origem até o nó n
  dist = {node.name: float("inf") for node in graph.nodes}
  # dicionario para guardar o nó que leva até tal posicao com menor caminho. Chave: nome do nó destino, Valor: o nó q leva a ele
  # ao achar uma rota menor até um nó ja presente a sobrescrita é fácil, pois é só acessar a posição pelo nome e alterar o valor
  previous: Dict[str, Node] = {}
  dist[start.name] = 0

  fila_prior: List[Tuple[int, str, Node]] = []
  heapq.heappush(fila_prior, (0, start.name, start)) # heapq.heappush adiciona um nó a fila de prioridade
  visited = set()

  while fila_prior:
    current_dist, _, current_node = heapq.heappop(fila_prior)
    if current_node.name in visited:
      continue

    visited.add(current_node.name)
    if current_node == goal:
      break

    for edge in current_node.neighbors:
      neighbor = edge.target
      weight = edge.weight
      new_dist = current_dist + weight
      if new_dist < dist[neighbor.name]:
        dist[neighbor.name] = new_dist
        previous[neighbor.name] = current_node
        heapq.heappush(fila_prior, (new_dist, neighbor.name, neighbor))

  path = reconstruct_path(previous, start, goal)
  if not path:
    return float('inf'), [], len(visited)

  return dist[goal.name], path, len(visited)

def a_star(graph: Graph, start: Node, goal: Node) -> Tuple[float, List[Node], int]:
  # g(n) = custo acumulado desde a origem
  # h(n) = distância euclidiana até o destino (previsão de custo até o destino)
  # f(n) = g(n) + h(n)

  # g_score[n] = menor custo conhecido da origem até o nó n
  g_score = {node.name: float('inf') for node in graph.nodes}
  # dicionario para guardar o nó que leva até tal posicao com menor caminho. Chave: nome do nó destino, Valor: o nó q leva a ele
  # ao achar uma rota menor até um nó ja presente a sobrescrita é fácil, pois é só acessar a posição pelo nome e alterar o valor
  previous: Dict[str, Node] = {}
  g_score[start.name] = 0

  fila_prior: List[Tuple[int, int, str, Node]] = [] 
  heapq.heappush(fila_prior, (heuristica(start, goal), 0, start.name, start)) # heapq.heappush adiciona um nó a fila de prioridade
  # ele verifica qual objeto deve ficar na frente seguindo a ordem da tupla. 
  # Caso o 1º argumento (peso_total) seja igual verifica o 2º argumento como desempate (distancia ate o objetivo)
  visitados = set()

  while fila_prior:
    current_h, current_g, _, current_node = heapq.heappop(fila_prior)

    if current_node.name in visitados:
      continue

    if current_node == goal:
      return g_score[goal.name], reconstruct_path(previous, start, goal), len(visitados)

    visitados.add(current_node.name)

    for edge in current_node.neighbors:
      neighbor = edge.target
      if neighbor.name in visitados:
        continue

      tentative_g = g_score[current_node.name] + edge.weight
      if tentative_g < g_score[neighbor.name]:
        g_score[neighbor.name] = tentative_g
        previous[neighbor.name] = current_node
        custo_total = tentative_g + heuristica(neighbor, goal)
        heapq.heappush(fila_prior, (custo_total, tentative_g, neighbor.name, neighbor))

  return float('inf'), [], len(visitados)

# transforma o mapa em um grafo (com todos os espacos livres sendo nodes)
# retorna alem disso um dicionario com todos os nodes usando a coordenada como chave para encontrar facil o node inicial e final depois
def transformar_mapa_em_grafo(labirinto: Labirinto) -> Tuple[Graph, Dict[Point, Node]]:
  rows = len(labirinto)
  cols = len(labirinto[0]) if rows else 0
  nodes: Dict[Point, Node] = {} # usa point como chave para pesquisar rapido se existe um node nessa coordenada na hora de criar as arestas

  # cria um node para cada posicao vazia no labirinto. Nao é o ideal, q seria só ter node no fim de beco sem saida ou encruzilhada 
  # mas assim consigo desenhar todo o percurso no mapa mais facil e interpretar mais facil
  # esse metodo menor eh bom quando nao conhecemos o mapa inteiro, só onde ja passamos
  for row in range(rows):
    for col in range(cols):
      if labirinto[row][col] == 0:
        name = f"{col},{row}"
        nodes[(col, row)] = Node(name, col, row, [])

  # cria as arestas (conecta com todos os nodes a ate 1 de distancia)
  # se fosse no metodo de 1 node só nos cruzamentos teria de todar uma busca em profundidade a cada node pra encontrar os vizinhos
  for (col, row), node in nodes.items():
    for dist_col, dist_row in ((1, 0), (-1, 0), (0, 1), (0, -1)):
      new_col = col + dist_col
      new_row = row + dist_row
      if (new_col, new_row) in nodes: # checa se existe algum node na lista com essas coordenadas
        node.neighbors.append(Edge(nodes[(new_col, new_row)], 1)) # como os nodes representam 1 casa no mapa, a distancia entre eles eh sempre 1

  graph = Graph(list(nodes.values()))
  return graph, nodes

def print_labirinto(labirinto: Labirinto, path: List[Node], start: Node, goal: Node) -> None:
  rows = len(labirinto)
  cols = len(labirinto[0]) if rows else 0

  # preenche o labirinto
  mark = []
  for row in range(rows):
    filled_row = ['#' if labirinto[row][col] == 1 else '.' for col in range(cols)]
    mark.append(filled_row)

  # preenche o caminho feito no labirinto
  for node in path:
    mark[node.y][node.x] = '*'

  # marca os pontos de inicio e fim
  mark[start.y][start.x] = 'S'
  mark[goal.y][goal.x] = 'G'

  # Imprime o labirinto
  for row in mark:
    print(' '.join(row))

def make_labyrinths() -> List[Tuple[Labirinto, Point, Point]]:
  # 0 livre, 1 ocupado
  # Labirinto 1
  lab1 = [
    [0,0,0,0,0,0,0],
    [0,1,1,1,0,1,0],
    [0,1,0,1,0,1,0],
    [0,1,0,0,0,1,0],
    [0,1,1,1,0,0,0],
    [0,0,0,1,1,1,0],
    [0,1,0,0,0,0,0],
  ]
  start1 = (0,0)
  goal1 = (6,6)

  # Labirinto 2
  lab2 = [
    [0,0,0,0,0,0,0,0,0],
    [0,1,1,1,1,1,0,1,0],
    [0,1,0,0,0,1,0,1,0],
    [0,1,0,1,0,1,0,1,0],
    [0,1,0,1,0,0,0,0,0],
    [0,0,0,1,1,1,1,1,0],
    [0,1,0,0,0,0,0,1,0],
    [0,1,1,1,1,1,0,1,0],
    [0,0,0,0,0,0,0,0,0],
  ]
  start2 = (1,0)
  goal2 = (7,8)

  # Labirinto 3
  lab3 = [
    [0,1,0,0,0,1,0,0],
    [0,1,0,1,0,1,1,0],
    [0,0,0,1,0,0,0,0],
    [1,1,0,1,1,1,0,1],
    [0,0,0,0,0,0,0,0],
  ]
  start3 = (0,0)
  goal3 = (7,4)

  return [(lab1, start1, goal1), (lab2, start2, goal2), (lab3, start3, goal3)]

lista_labirintos = make_labyrinths()
for i, (labirinto, start_tupla, goal_tupla) in enumerate(lista_labirintos):
  graph, nodes = transformar_mapa_em_grafo(labirinto)
  start = nodes.get(start_tupla)
  goal = nodes.get(goal_tupla)

  print(f"\n================== Labirinto {i} ==================")
  custo_dji, path_dji, total_visitas = dijkstra(graph, start, goal)
  print('\nDijkstra:')
  if path_dji:
    print("Caminho:", " -> ".join(node.name for node in path_dji))
    print(f"Custo total: {custo_dji:.2f}")
    print(f'Num nós visitados: {total_visitas}')
    print_labirinto(labirinto, path_dji, start, goal)
  else:
    print('Nao foi encontrado um caminho')

  custo_a, path_a, total_visitas = a_star(graph, start, goal)
  print('\nA*:')
  if path_a:
    print("Caminho:", " -> ".join(node.name for node in path_a))
    print(f"Custo total: {custo_a:.2f}")
    print(f'Num nós visitados: {total_visitas}')
    print_labirinto(labirinto, path_a, start, goal)
  else:
    print('Nao foi encontrado um caminho')
