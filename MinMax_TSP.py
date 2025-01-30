import os
import numpy as np
from haversine import haversine, Unit
import time
import random

# --------------------------------------------
# Funções de Leitura 
# --------------------------------------------

def vectorized_distance_matrix(nodes, weight_type):
    """Calcula a matriz de distâncias entre os nós, considerando o tipo de peso"""
    if weight_type == "EUC_2D":
        # Calcula distâncias euclidianas entre os nós usando operações vetorizadas
        diffs = nodes[:, np.newaxis] - nodes  # Diferenças entre todos os nós
        return np.sqrt(np.sum(diffs**2, axis=2))  # Distância euclidiana entre os nós
    
    # Para o tipo GEO, utiliza a fórmula de Haversine para calcular distâncias geográficas
    n = nodes.shape[0]  # Número de nós
    matrix = np.zeros((n, n))  # Matriz de distâncias vazia
    for i in range(n):
        for j in range(i+1, n):  # Calcula distâncias apenas uma vez (simétrica)
            matrix[i, j] = matrix[j, i] = haversine(nodes[i], nodes[j], Unit.KILOMETERS)
    return matrix

def data_transformation(content):
    """Transforma os dados de entrada, extraindo as coordenadas dos nós e calculando a matriz de distâncias"""
    # Identifica o tipo de peso a partir do conteúdo da instância (EUC_2D ou GEO)
    weight_type = next(line.split(":")[1].strip() for line in content.splitlines() if "EDGE_WEIGHT_TYPE" in line)
    
    # Extrai as coordenadas dos nós
    coord_lines = []
    in_section = False
    for line in content.splitlines():
        if "NODE_COORD_SECTION" in line:
            in_section = True
            continue
        if "EOF" in line:
            break
        if in_section and line.strip():  # Adiciona as linhas de coordenadas
            coord_lines.append(line)
    
    # Converte as coordenadas para um array NumPy
    nodes = np.array([list(map(float, line.split()[1:3])) for line in coord_lines])
    return vectorized_distance_matrix(nodes, weight_type)

# --------------------------------------------
# Algoritmos para Min-Max
# --------------------------------------------

def optimized_greedy(matrix, start=None, lookahead=50, k_best=5):
    """Algoritmo Guloso otimizado que escolhe aleatoriamente entre os melhores k candidatos"""
    n = matrix.shape[0]  # Número de nós
    start = random.randint(0, n-1) if start is None else start  # Se não especificado, escolhe aleatoriamente o nó de partida
    tour = [start]  # Lista para armazenar o tour
    candidates = set(range(n)) - {start}  # Conjunto de nós candidatos
    current_max = 0  # Distância máxima no tour atual
    
    while candidates:
        current = tour[-1]  # Último nó no tour
        neighbors = np.argsort(matrix[current])[:lookahead]  # Olha os vizinhos mais próximos (lookahead)
        valid_neighbors = [n for n in neighbors if n in candidates]  # Filtra os vizinhos válidos
        
        if not valid_neighbors:
            valid_neighbors = list(candidates)  # Se não houver vizinhos válidos, pega todos os candidatos
        
        # Ordena os vizinhos com base na distância máxima até o nó atual
        sorted_neighbors = sorted(valid_neighbors, 
                                key=lambda x: max(current_max, matrix[current, x]))
        top_candidates = sorted_neighbors[:k_best]  # Seleciona os top k candidatos
        best_next = random.choice(top_candidates) if top_candidates else valid_neighbors[0]  # Escolhe aleatoriamente o melhor próximo nó
        
        tour.append(best_next)
        candidates.remove(best_next)  # Remove o nó escolhido dos candidatos
        current_max = max(current_max, matrix[current, best_next])  # Atualiza a distância máxima
    
    tour.append(start)  # Retorna ao nó inicial
    final_max = max(current_max, matrix[tour[-2], start])  # Distância máxima final
    return tour, final_max

def fast_2opt(tour, matrix, max_attempts=500):
    """Refinamento do tour com a técnica 2-opt para melhorar a solução"""
    best_tour = tour.copy()  # Copia do tour atual
    best_max = max(matrix[tour[i], tour[i+1]] for i in range(len(tour)-1))  # Distância máxima do tour
    improved = True  # Flag para indicar se houve melhoria
    n = len(tour)
    
    while improved:
        improved = False  # Assume-se que não houve melhoria inicialmente
        attempts = 0
        
        while attempts < max_attempts:
            # Escolhe aleatoriamente dois índices para tentar reverter o caminho entre eles
            i, j = random.sample(range(1, n-1), 2)
            if i > j: i, j = j, i  # Garante que i < j
            
            old_max = max(
                matrix[best_tour[i-1], best_tour[i]],
                matrix[best_tour[j], best_tour[j+1]]
            )  # Distância máxima antes da troca
            new_max = max(
                matrix[best_tour[i-1], best_tour[j]],
                matrix[best_tour[i], best_tour[j+1]]
            )  # Distância máxima após a troca
            
            if new_max < old_max:  # Se a troca melhorar o tour
                best_tour[i:j+1] = best_tour[i:j+1][::-1]  # Reverte a parte do tour entre os índices i e j
                best_max = max(best_max, new_max)  # Atualiza a distância máxima
                improved = True  # Indica que houve melhoria
                break
            attempts += 1
            
    return best_tour, best_max

# --------------------------------------------
# Pipeline 
# --------------------------------------------

def solve_instance(content, target):
    """Resolve uma instância do problema, retornando o melhor tour e a distância máxima"""
    matrix = data_transformation(content)  # Convertendo os dados de entrada para a matriz de distâncias
    n = matrix.shape[0]
    
    # Define um número de iterações e lookahead adaptativo
    iterations = min(20, max(5, n//50))  # Limitando as iterações a um intervalo razoável
    lookahead = min(150, max(50, int(n*0.2)))  # Ajustando o lookahead com base no tamanho do problema
    
    best_tour, best_max = None, float('inf')  # Inicializando o melhor tour e a distância máxima
    
    # Loop principal, executa o algoritmo de busca e refinamento várias vezes
    for _ in range(iterations):
        tour, current_max = optimized_greedy(matrix, lookahead=lookahead, k_best=7)  # Gera um tour inicial
        
        # Refinamento do tour com 2-opt
        for _ in range(3):  # Aplica 2-opt até 3 vezes para melhorar a solução
            tour, current_max = fast_2opt(tour, matrix)
        
        if current_max < best_max:  # Se encontrar uma melhor solução, atualiza
            best_tour, best_max = tour, current_max
    
    return best_tour[:-1], best_max  # Retorna o tour sem o nó final (volta ao inicial) e a distância máxima

def process_files(input_path):
    """Processa todos os arquivos da pasta de entrada, resolve e grava as soluções"""
    output_dir = os.path.join(input_path, "tsp_solutions")  # Diretório de saída
    os.makedirs(output_dir, exist_ok=True)  # Cria o diretório de saída se não existir
    
    # Referência de alvos (distâncias ideais para as instâncias)
    reference = {
        '01': 3986, '02': 1289, '03': 1476, '04': 1133, '05': 546,
        '06': 431, '07': 219, '08': 266, '09': 52, '10': 237
    }
    
    # Processa cada arquivo de instância no diretório
    for file in sorted(f for f in os.listdir(input_path) if f.endswith(".ins")):
        instance_id = file.split(".")[0][-2:]  # ID da instância
        target = reference.get(instance_id, float('inf'))  # Alvo da instância (distância ideal)
        
        try:
            with open(os.path.join(input_path, file), "r") as f:
                start = time.time()  # Marca o tempo de início
                tour, max_dist = solve_instance(f.read(), target)  # Resolve a instância
                elapsed = time.time() - start  # Calcula o tempo de execução
                
                # Salva a solução no arquivo de saída
                output_file = os.path.join(output_dir, f"{instance_id}_sol.txt")
                with open(output_file, "w") as sf:
                    sf.write(" ".join(map(str, tour)))
                
                # Exibe os resultados
                print(f"Instância {instance_id}:")
                print(f" - Distância Máxima: {max_dist:.1f} (Alvo: {target})")
                print(f" - Tempo: {elapsed:.3f}s")
                print(f" - Economia: {(target - max_dist)/target*100:.1f}%\n")
        
        except Exception as e:
            print(f"Erro em {file}: {str(e)}")

if __name__ == "__main__":
    process_files("./instances")  
