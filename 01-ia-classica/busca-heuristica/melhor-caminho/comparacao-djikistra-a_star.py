import math
from dataclasses import dataclass

@dataclass
class Node:
    name: str
    x: int
    y: int
    neighbors: [Edge]

@dataclass
class Edge:
    target: Node
    weight: int

@dataclass
class Graph:
    nodes: [Node]

def heuristica(a, b):
    # h(n): distância euclidiana do nó atual até o destino.
    return math.sqrt((a.x - b.x) ** 2 + (a.y - b.y) ** 2)

def reconstruct_path(previous, start, goal):
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

def dijkstra(graph, start, goal):
    # dist[n] = menor custo conhecido da origem até o nó n
    dist = {node.name: float("inf") for node in graph.nodes}
    # dicionario para guardar o nó que leva até tal posicao com menor caminho. Chave: nome do nó destino, Valor: o nó q leva a ele
    # ao achar uma rota menor até um nó ja presente a sobrescrita é fácil, pois é só acessar a posição pelo nome e alterar o valor
    previous = {}
    dist[start.name] = 0

    queue = [(0, start)]
    visited = set()

    while queue:
        queue.sort(key=lambda item: item[0])
        current_dist, current_node = queue.pop(0)

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
                queue.append((new_dist, neighbor))

    path = reconstruct_path(previous, start, goal)
    if len(path) == 0:
        return float("inf"), []

    return dist[goal.name], path, len(visited)

def a_star(graph, start, goal):
    # g(n) = custo acumulado desde a origem
    # h(n) = distância euclidiana até o destino (previsão de custo até o destino)
    # f(n) = g(n) + h(n)

    # g_score[n] = menor custo conhecido da origem até o nó n
    g_score = {node.name: float("inf") for node in graph.nodes}
    # dicionario para guardar o nó que leva até tal posicao com menor caminho. Chave: nome do nó destino, Valor: o nó q leva a ele
    # ao achar uma rota menor até um nó ja presente a sobrescrita é fácil, pois é só acessar a posição pelo nome e alterar o valor
    previous = {}
    g_score[start.name] = 0

    # array de tuplas com os seguintes valores nessa ordem: (h(n), g(n), n)
    open_set = [(heuristica(start, goal), 0, start)]
    closed_set = set()

    while open_set:
        open_set.sort(key=lambda item: item[0])
        current_h, current_g, current_node = open_set.pop(0)

        if current_node.name in closed_set:
            continue

        if current_node == goal:
            return g_score[goal.name], reconstruct_path(previous, start, goal), len(closed_set)

        closed_set.add(current_node.name)

        for edge in current_node.neighbors:
            neighbor = edge.target
            weight = edge.weight
            if neighbor.name in closed_set:
                continue

            tentative_g = g_score[current_node.name] + weight
            if tentative_g < g_score[neighbor.name]:
                g_score[neighbor.name] = tentative_g
                previous[neighbor.name] = current_node

                h = heuristica(neighbor, goal)
                f = tentative_g + h
                open_set.append((f, tentative_g, neighbor))

    return float("inf"), [], len(closed_set)

# CRIA OS NÓS DO GRAFO
A = Node("A", 0, 0, [])
B = Node("B", 2, 4, [])
C = Node("C", 5, 2, [])
D = Node("D", 7, 6, [])
E = Node("E", 10, 4, [])
F = Node("F", 12, 8, [])

# ADICIONA AS ARESTAS (LIGAM OS NÓS) E INFORMA OS PESOS DE CADA ARESTA
A.neighbors.append(Edge(B, 5))
A.neighbors.append(Edge(C, 3))
B.neighbors.append(Edge(D, 4))
B.neighbors.append(Edge(C, 2))
C.neighbors.append(Edge(D, 6))
C.neighbors.append(Edge(E, 7))
D.neighbors.append(Edge(E, 2))
D.neighbors.append(Edge(F, 5))
E.neighbors.append(Edge(F, 3))

# CRIA NOSSO GRAFO, ADICIONANDO OS NÓS NELE
graph = Graph([A, B, C, D, E, F])

# DEFINE O PONTO INICIAL E FINAL
start = A
goal = F
print(f"Origem: {start.name}")
print(f"Destino: {goal.name} \n")

# IMPRIME O GRAFO
print("Grafo:")
for node in graph.nodes:
    print('-----------')
    print(f'{node.name}: heuristica={heuristica(node, goal):.2f} \nArestas:')
    for edge in node.neighbors:
        print(f"  {node.name} -> {edge.target.name} (peso={edge.weight})")


# CALCULA OS CAMINHOS  ---------------------------------------
custo_dji, path_dji, total_visitas = dijkstra(graph, start, goal)
print('\nDijkstra')
print("Caminho:", " -> ".join(node.name for node in path_dji))
print(f"Custo total: {custo_dji:.2f}")
print(f'Num nós visitados: {total_visitas}')

custo_a, path_a, total_visitas = a_star(graph, start, goal)
print('\nA*')
print("Caminho:", " -> ".join(node.name for node in path_a))
print(f"Custo total: {custo_a:.2f}")
print(f'Num nós visitados: {total_visitas}')
