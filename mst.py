import numpy as np

def maximum_cost_indexes(matrix):
    return np.unravel_index(np.argmax(matrix), matrix.shape)

def closest_neighbors(matrix):
    neighbors = {}
    # Guardando os indices em que foi encontrado o maior custo entre as arestas
    i,j = maximum_cost_indexes(matrix)
    threshold = 100
    for index in [i,j]:
        # Ordena os indices dos pontos mais próximos para os mais distantes
        closest_neighbors_data = np.argsort(matrix[index])

        # Remove o próprio ponto da lista de vizinhos mais próximos
        closest_neighbors_data = closest_neighbors_data[closest_neighbors_data != index]

        # Guarda os N vizinhos mais próximos
        neighbors[index] = closest_neighbors_data[:threshold]

    return neighbors

    # Recebe uma matriz de adjacência e um ponto de origem
def mst(matrix, origin):
    # Recebe uma matriz de adjacência e um ponto de origem
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
