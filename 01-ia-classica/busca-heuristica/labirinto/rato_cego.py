'''
Rato cego é um desafio de IA aonde deve-se programar um rato cego para encontrar a saída de um labirinto. Ele não conhece nada do
labirinto alem do local onde está agora e de onde já passou, tendo de mapear o labirinto enquanto anda.
'''
from dataclasses import dataclass
from typing import List, Dict, Tuple, Set

# cria um novo tipo de variavel para o labirinto (matriz de int)
Labirinto = List[List[int]]

# cria novo tipo de variavel para uma posicao no labirinto
Point = Tuple[int, int]

@dataclass
class Node:
  name: str
  x: int
  y: int
  neighbors: List[Edge]

  def get_point(self):
    return (self.x, self.y)

@dataclass
class Edge:
  target: Node
  weight: int

@dataclass
class Graph:
  nodes: List[Node]

  def print(self):
    for node in self.nodes:
      print('-----------')
      print(f'{node.name}. Arestas:')
      for edge in node.neighbors:
        print(f"  {node.name} -> {edge.target.name} (peso={edge.weight})")


class ExploradorLabirinto:
  def __init__(self, labirinto: Labirinto, ponto_ini: Point, ponto_fim: Point):
    self.labirinto = labirinto
    self.num_rows = len(labirinto)
    self.num_cols = len(labirinto[0]) if self.num_rows else 0
    self.nodes: Dict[Point, Node] = {}
    self.total_passos = 0

    self.graph = Graph([])
    self.visitados: Set[Point] = set()
    self.start: Point = ponto_ini
    self.goal: Point = ponto_fim
    self.add_node(self.start)

  def add_node(self, point: Point) -> Node:
    if point in self.nodes:
      return self.nodes[point]

    col, row = point
    node = Node(f"{col},{row}", col, row, [])
    self.nodes[point] = node
    self.graph.nodes.append(node)
    return node

  def adicionar_aresta(self, origem: Point, destino: Point, dist: int = 1) -> None:
    if origem not in self.nodes or destino not in self.nodes:
      return

    origem_node = self.nodes[origem]
    destino_node = self.nodes[destino]

    # garante nao colocar a mesma aresta 2x
    if all(edge.target != destino_node for edge in origem_node.neighbors):
      origem_node.neighbors.append(Edge(destino_node, dist))

    # grafo bidirecional, add a aresta no sentido contrario
    if all(edge.target != origem_node for edge in destino_node.neighbors):
      destino_node.neighbors.append(Edge(origem_node, dist))

  # verifica se o ponto nao existe (vai pra fora dos limites do mapa) ou se o ponto é uma parede
  def ignorar_ponto(self, novo_ponto: Point):
    new_col, new_row = novo_ponto
    ponto_inexistente = new_col < 0 or new_col >= self.num_cols or new_row < 0 or new_row >= self.num_rows
    if(ponto_inexistente): return True
    parede = self.labirinto[new_row][new_col] == 1
    return parede

  def pontos_vizinhos_livres(self, ponto: Point):
    ponto_acima: Point = (ponto[0], ponto[1]-1)
    ponto_abaixo: Point = (ponto[0], ponto[1]+1)
    ponto_direita: Point = (ponto[0]+1, ponto[1])
    ponto_esquerda: Point = (ponto[0]-1, ponto[1])
    pontos_livres = []
    for ponto_vizinho in [ponto_acima, ponto_direita, ponto_abaixo, ponto_esquerda]:
      if(not self.ignorar_ponto(ponto_vizinho)):
        pontos_livres.append(ponto_vizinho)
    return pontos_livres

  def dar_passo(self, ponto: Point, penultimo_ponto: Point | None, ultimo_node: Node, num_passos: int):
    caminhos_possiveis = self.pontos_vizinhos_livres(ponto)

    # checa se é um cruzamento (tem 3 ou mais possibilidades de caminhos a partir dele, por onde veio e mais 2)
    if( len(caminhos_possiveis) >= 3 ):
      self.add_node(ponto) # se ja existe um node pra esse ponto o metodo só ignora
      if(ultimo_node):
        self.adicionar_aresta(ponto, ultimo_node.get_point(), num_passos)
      ultimo_node = self.nodes[ponto]
      num_passos = 0

    for novo_ponto in caminhos_possiveis:
      # se o ponto vizinho é a saída, cria um node pra ele e encerra a exploracao
      if novo_ponto == self.goal:
        self.add_node(novo_ponto)
        self.adicionar_aresta(ultimo_node.get_point(), novo_ponto, num_passos+1)
        self.total_passos += 1
        return True

      # ignora o ponto de onde veio (impede de ficar indo e voltando nos mesmos 2 pontos)
      if(penultimo_ponto and novo_ponto in self.visitados and penultimo_ponto == novo_ponto):
        continue

      # anotar que ja passou nesse ponto
      if novo_ponto not in self.visitados:
        self.visitados.add(novo_ponto)

      # se a casa atual ja é um ponto mapeado (um node no grafo), cria a aresta e segue por outro caminho
      if novo_ponto in self.nodes:
        self.adicionar_aresta(ultimo_node.get_point(), novo_ponto, num_passos)
        continue

      self.total_passos += 1
      achei_saida = self.dar_passo(novo_ponto, ponto, ultimo_node, num_passos+1)
      if(achei_saida): return True
    # se saiu do loop foi porque chegou em um beco sem saída. Somamos os passos de volta até o último node
    self.total_passos += 1
    return False

  def explorar(self) -> Tuple[Graph, Node, Node]:
    self.visitados.add(self.start)
    return self.dar_passo(self.start, None, self.nodes[self.start], 0)

def print_labirinto(labirinto: Labirinto, path: List[Point], start: Point, goal: Point) -> None:
  rows = len(labirinto)
  cols = len(labirinto[0]) if rows else 0

  # preenche o labirinto
  mark = []
  for row in range(rows):
    filled_row = ['#' if labirinto[row][col] == 1 else '.' for col in range(cols)]
    mark.append(filled_row)

  # preenche o caminho feito no labirinto
  for node in path:
    mark[node[1]][node[0]] = '*'

  # marca os pontos de inicio e fim
  mark[start[1]][start[0]] = 'S'
  mark[goal[1]][goal[0]] = 'G'

  for row in mark:
    print(' '.join(row))

def make_labyrinths() -> List[Tuple[Labirinto, Point, Point]]:
  # 0 livre, 1 ocupado
  # Labirinto 1
  lab1 = [
    [1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,1],
    [1,0,1,1,1,0,0,0,1],
    [1,0,0,0,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1]
  ]
  start1 = (1,1)
  goal1 = (7,7)

  # Labirinto 2
  lab2 = [
    [1,1,1,1,1,1,1,1,1,1,1],
    [1,0,0,0,0,0,0,0,0,0,1],
    [1,0,1,1,1,1,1,0,1,0,1],
    [1,0,1,0,0,0,1,0,1,0,1],
    [1,0,1,0,1,0,1,0,1,0,1],
    [1,0,1,0,1,0,0,0,0,0,1],
    [1,0,0,0,1,1,1,1,1,0,1],
    [1,0,1,0,0,0,0,0,1,0,1],
    [1,0,1,1,1,1,1,0,1,0,1],
    [1,0,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1,1]
  ]
  start2 = (2,1)
  goal2 = (8,9)

  # Labirinto 3
  lab3 = [
    [1,1,1,1,1,1,1,1,1,1],
    [1,0,1,0,0,0,1,0,0,1],
    [1,0,1,0,1,0,1,1,0,1],
    [1,0,0,0,1,0,0,0,0,1],
    [1,1,1,0,1,1,1,0,1,1],
    [1,0,0,0,0,0,0,0,0,1],
    [1,1,1,1,1,1,1,1,1,1]
  ]
  start3 = (1,1)
  goal3 = (8,5)

  # Labirinto 4
  lab4 = [
    [0,0,0,0, 0,0,0,0,0, 0,1, 0,0,0, 0,0,0],
    [0,1,1,0, 1,1,1,1,1, 0,1, 0,1,1, 1,1,0],
    [0,1,1,0, 1,0,0,0,1, 0,1, 0,0,0, 1,1,0],
    [0,1,1,0, 1,0,1,0,1, 0,1, 1,1,1, 1,1,0],
    [0,0,1,0, 1,0,1,0,0, 0,0, 0,0,0, 0,0,0],
    [0,1,1,0, 1,1,1,1,1, 0,1, 1,1,1, 0,1,0],
    [0,1,1,0, 0,0,0,0,0, 0,1, 0,0,1, 0,1,0],
    [0,1,1,0, 1,1,1,1,1, 0,1, 0,1,1, 0,1,0],
    [0,1,1,0, 0,0,1,1,1, 0,1, 0,0,0, 0,1,1],
    [0,1,1,0, 1,1,1,1,1, 0,1, 1,1,1, 0,1,1],
    [0,0,0,0, 0,0,0,0,0, 0,1, 1,1,1, 0,1,1],
    [1,1,1,1, 1,1,1,1,1, 1,1, 1,1,1, 0,1,1],
    [0,0,0,0, 0,0,0,0,0, 0,0, 0,0,0, 0,1,1],
    [0,1,1,1, 1,1,1,1,1, 1,0, 1,1,1, 1,1,1],
    [0,1,1,1, 1,1,0,1,1, 1,0, 1,1,1, 1,1,1],
    [0,1,1,1, 0,1,0,1,1, 1,0, 1,1,1, 1,1,1],
    [0,1,1,1, 0,1,0,0,0, 0,0, 1,1,1, 1,1,1],
    [0,1,1,1, 0,1,1,1,1, 1,0, 1,1,1, 1,1,1],
    [0,0,0,0, 0,0,0,0,0, 0,0, 1,1,1, 1,1,1],
  ]
  start4 = (1,10)
  goal4 = (12,6)

  return [(lab1, start1, goal1), (lab2, start2, goal2), (lab3, start3, goal3), (lab4, start4, goal4)]

lista_labirintos = make_labyrinths()
for i, (labirinto, ponto_ini, ponto_fim) in enumerate(lista_labirintos):
  explorer = ExploradorLabirinto(labirinto, ponto_ini, ponto_fim)
  achei_saida = explorer.explorar()
  print(f"\n================== Labirinto {i} ==================")
  print('Inicio', ponto_ini)
  print('Saida', ponto_fim)
  print_labirinto(labirinto, explorer.visitados, ponto_ini, ponto_fim)
  print('\nEncontrei a saida: ', achei_saida)
  print('Num de passos dados: ', explorer.total_passos, 'Num de casas em que passou: ', len(explorer.visitados))
  print('******* GRAFO *******')
  explorer.graph.print()
