from mst import *

# matrix = np.array([
#     [0, 10, 15, 20, 25],
#     [10, 0, 35, 25, 30],
#     [15, 35, 0, 30, 5],
#     [20, 25, 30, 0, 40],
#     [25, 30, 5, 40, 0]
# ])

# print(mst(matrix, [1,2,3]))

matrix = np.load("./instances/adjacency_matrices/03_adjacency.npy")
# print(matrix)
print("Iniciando testes")
initial_path = list(range(len(matrix)))
initial_path.append(initial_path[0])  # Complete the cycle

best_distance, _ = two_opt(initial_path, matrix)
print("Distancia 2opt:", best_distance)

# Chamar a função MST
origin = list(range(matrix.shape[0]))  # Todos os nós
cost_path, total_distance = nearest_neighbor_tsp(matrix, 0)

mst_edges, total_cost = mst(matrix, origin)
tsp_tour = mst_to_tsp(mst_edges, len(origin))
tsp_cost = calculate_tour_cost(tsp_tour, matrix)
print("TSP Tour:", tsp_tour)
print("TSP Cost:", tsp_cost)
print("Arestas:", mst_edges)
print("Custo Total:", total_cost)

i, j = maximum_cost_indexes(matrix)

closest_neighbors_data = closest_neighbors(matrix,i, j)

for value in closest_neighbors_data.values():
    _, cost = mst(matrix,value)
    print("Custo total MST", cost)

