from asyncio.windows_events import INFINITE

import numpy as np

def maximum_cost_indexes(matrix):
    return np.unravel_index(np.argmax(matrix), matrix.shape)

def closest_neighbors(matrix, i, j):
    neighbors = {}
    # Guardando os indices em que foi encontrado o maior custo entre as arestas
    threshold = 100
    for index in [i,j]:
        # Ordena os indices dos pontos mais próximos para os mais distantes
        closest_neighbors_data = np.argsort(matrix[index])

        # Remove o próprio ponto da lista de vizinhos mais próximos
        closest_neighbors_data = closest_neighbors_data[closest_neighbors_data != index]

        # Guarda os N vizinhos mais próximos
        neighbors[index] = closest_neighbors_data[:]

    return neighbors

    # Recebe uma matriz de adjacência e um ponto de origem
def mst(matrix, origin):
    # Recebe uma matriz de adjacência e um ponto de origem
    graph = matrix
    if isinstance(origin, np.ndarray):
        graph = matrix[origin, :][:, origin]

    # Recebe a quantidade de vértices
    vertix_amount = graph.shape[0]

    # Inicializa a estrutura de dados que guarda os vértices já visitados
    mst_structure = [False] * vertix_amount

    # Inicializa a estrutura de dados que guarda as arestas de menor custo
    minimum_edge = [(float('inf'), None)] * vertix_amount

    # Inicializa a aresta de menor custo para o vértice de origem
    minimum_edge[0] = (0, -1)

    # Inicializa a estrutura de dados que guarda as arestas da AGM
    mst_edges = []

    # Variavel para armazenar o custo total da AGM
    cost = 0

    # Algoritmo de Prim
    for _ in range(vertix_amount):
        u = -1
        for v in range(vertix_amount):
            # Encontra o vértice de menor custo que ainda não foi visitado
            if not mst_structure[v] and (u == -1 or minimum_edge[v][0] < minimum_edge[u][0]):
                u = v

        # Marca o vértice como visitado
        mst_structure[u] = True

        # Atualiza o custo total da AGM
        cost += minimum_edge[u][0]

        # Adiciona a aresta de menor custo na AGM
        if minimum_edge[u][1] != -1:
            mst_edges.append((minimum_edge[u][1], u, minimum_edge[u][0]))

        # Atualiza a estrutura de dados que guarda as arestas de menor custo
        for v in range(vertix_amount):
            if not mst_structure[v] and graph[u][v] < minimum_edge[v][0]:
                minimum_edge[v] = (graph[u][v], u)

    return mst_edges, cost

def dfs(graph, start, visited, tour):
    visited[start] = True
    tour.append(start)
    for neighbor, weight in graph[start]:
        if not visited[neighbor]:
            dfs(graph, neighbor, visited, tour)

def mst_to_tsp(mst_edges, num_vertices):
    # Cria o grapho da AGM
    mst_graph = [[] for _ in range(num_vertices)]
    for u, v, weight in mst_edges:
        mst_graph[u].append((v, weight))
        mst_graph[v].append((u, weight))

    # Faz uma busca em profundidade para gerar o tour
    visited = [False] * num_vertices
    tour = []
    dfs(mst_graph, 0, visited, tour)
    tour.append(tour[0])  # Retorna ao ponto inicial

    return tour

def calculate_tour_cost(tour, matrix):
    cost = 0
    for i in range(len(tour) - 1):
        cost += matrix[tour[i], tour[i + 1]]
    return cost


def nearest_neighbor_tsp(matrix, origin):
    # Recebe uma matriz de adjacência e um ponto de origem
    n = matrix.shape[0]
    # Inicializa a estrutura de dados que guarda os vértices já visitados
    visited = [False] * n
    # Inicializa a estrutura de dados que guarda o caminho percorrido
    path = [origin]
    # Marca o vértice de origem como visitado
    visited[origin] = True
    # Inicializa a variável que guarda o custo total do caminho
    total_cost = 0

    # Inicializa o vértice atual
    current_node = origin
    # Enquanto houver vértices não visitados
    for _ in range(n - 1):
        nearest_node = -1
        min_distance = float('inf')

        for neighbor in range(n):
            # Encontra o vértice mais próximo que ainda não foi visitado
            if not visited[neighbor] and matrix[current_node][neighbor] < min_distance:
                # Atualiza o vértice mais próximo
                min_distance = matrix[current_node][neighbor]
                nearest_node = neighbor

        # Adiciona o vértice mais próximo ao caminho percorrido
        path.append(nearest_node)
        # Marca o vértice mais próximo como visitado
        visited[nearest_node] = True

        # Atualiza o custo total do caminho e o vértice atual
        total_cost += min_distance
        current_node = nearest_node

    total_cost += matrix[current_node][origin]
    path.append(origin)

    return path, total_cost

def two_opt_change(route, first, second):
    new_route = np.zeros(len(route), dtype=int)
    new_route[:first] = route[:first]
    new_route[first:second] = route[first:second][::-1]
    new_route[second:] = route[second:]
    return new_route

def path_cost_from_distance_matrix(matrix, path):
    cost = 0
    for i in range(len(path) - 1):
        cost += matrix[path[i], path[i + 1]]
    return cost

def two_opt(path, matrix):
    best_distance = path_cost_from_distance_matrix(matrix, path)
    present_route = path.copy()
    for i in range(len(path) - 2):
        for j in range(i + 1, len(path) - 1):
            new_route = two_opt_change(present_route, i, j)
            new_distance = path_cost_from_distance_matrix(matrix, new_route)
            if new_distance < best_distance:
                best_distance = new_distance
                present_route = new_route
    return best_distance, present_route