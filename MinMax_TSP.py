import os
import numpy as np
from haversine import haversine, Unit
from mst_test import *  
import time

# Função para extrair coordenadas EUC_2D
def euclidean_conversion(content):
    data = []
    in_node_section = False
    for line in content.splitlines():
        if "NODE_COORD_SECTION" in line:
            in_node_section = True
            continue
        if "EOF" in line:
            break
        if in_node_section:
            parts = line.split()
            if len(parts) >= 3:
                _, x, y = parts
                data.append((float(x), float(y)))
    return data

# Função para extrair coordenadas GEO
def haversine_conversion(content):
    coordinates = []
    in_node_section = False
    for line in content.splitlines():
        if "NODE_COORD_SECTION" in line:
            in_node_section = True
            continue
        if "EOF" in line:
            break
        if in_node_section:
            parts = line.split()
            if len(parts) >= 3:
                _, latitude, longitude = parts
                coordinates.append((float(latitude), float(longitude)))
    return coordinates

# Função para calcular matriz de adjacência
def calculate_distance_matrix(nodes, weight_type):
    n = len(nodes)
    matrix = np.zeros((n, n))
    for i in range(n):
        for j in range(i + 1, n):
            if weight_type == "EUC_2D":
                x1, y1 = nodes[i]
                x2, y2 = nodes[j]
                dist = np.sqrt((x2 - x1) ** 2 + (y2 - y1) ** 2)
            elif weight_type == "GEO":
                dist = haversine(nodes[i], nodes[j], unit=Unit.KILOMETERS)
            else:
                raise ValueError(f"Tipo de peso desconhecido: {weight_type}")
            matrix[i][j] = dist
            matrix[j][i] = dist
    return matrix

# Função para processar e transformar os dados
def data_transformation(content):
    weight_type = [
        line.split(":")[1].strip()
        for line in content.splitlines()
        if "EDGE_WEIGHT_TYPE" in line
    ]
    if weight_type:
        weight_type = weight_type[0]
    else:
        raise ValueError("Tipo de peso não encontrado no arquivo.")
    
    if weight_type == "EUC_2D":
        nodes = euclidean_conversion(content)
    elif weight_type == "GEO":
        nodes = haversine_conversion(content)
    else:
        raise ValueError(f"Tipo de peso desconhecido: {weight_type}")
    
    distance_matrix = calculate_distance_matrix(nodes, weight_type)
    return distance_matrix

# Função para ler as instâncias, gerar matrizes de adjacência e calcular a AGM
def read_instances(path):
    output_dir = os.path.join(path, "adjacency_matrices")
    os.makedirs(output_dir, exist_ok=True)
    files = [f for f in os.listdir(path) if f.endswith(".ins")]
    for file in sorted(files):
        file_path = os.path.join(path, file)
        try:
            with open(file_path, "r") as f:
                content = f.read()
                distance_matrix = data_transformation(content)
                
                # Salvar a matriz de adjacência em arquivo .npy
                output_file = os.path.join(output_dir, f"{os.path.splitext(file)[0]}_adjacency.npy")
                np.save(output_file, distance_matrix)
                print(f"Matriz de adjacência gerada e salva para {file}")

                # Chamar a função MST
                origin = list(range(distance_matrix.shape[0]))  # Todos os nós
                mst_edges, total_cost = mst(distance_matrix, origin)
                print("Arestas:", mst_edges)
                print("Custo Total:", total_cost)
        
        except Exception as e:
            print(f"Erro ao processar o arquivo {file}: {e}")

# Função principal
def main():
    input_path = "./instances"

    start_time = time.time()
    read_instances(input_path)
    end_time = time.time()
    execution_time = end_time - start_time
    print(f"Tempo total de execução: {execution_time:.4f} segundos")


if __name__ == "__main__":
    main()
