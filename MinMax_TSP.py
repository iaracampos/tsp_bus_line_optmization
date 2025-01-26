import os
from haversine import haversine, Unit

# extraindo cordenadas transformando em float 
def euclidean_conversion(content):
    data = []  
    in_node_section = False  # flag para verificar se estamos na seção de nós
    
    # Extração das coordenadas
    for line in content.splitlines():
        if "NODE_COORD_SECTION" in line:  # marca o início da seção de coordenadas
            in_node_section = True 
            continue
        if "EOF" in line:  # fim da seção de coordenadas
            break
        if in_node_section:
            parts = line.split()
            if len(parts) >= 3:  # verifica se tem três colunas
                _, x, y = parts 
                data.append((float(x), float(y)))  # armazena as coordenadas como tupla (x, y)
    
    return data

# função para extrair as coordenadas em instâncias do tipo GEO (latitude, longitude)
def haversine_conversion(content):
    coordinates = []  
    in_node_section = False  # flag para verificar se estamos na seção de nós
    

    for line in content.splitlines():
        if "NODE_COORD_SECTION" in line:  # marca o início da seção de coordenadas
            in_node_section = True 
            continue
        if "EOF" in line:  # fim da seção de coordenadas
            break
        if in_node_section:
            parts = line.split()
            if len(parts) >= 3:  # verifica se tem três colunas
                _, latitude, longitude = parts 
                coordinates.append((float(latitude), float(longitude)))  # armazena coordenadas geográficas
    
    # calcula distâncias usando Haversine
    distances = []
    for i in range(len(coordinates)):  # percorre as coordenadas
        for j in range(i + 1, len(coordinates)):
            dist = haversine(coordinates[i], coordinates[j], unit=Unit.KILOMETERS)  # calcula distância entre os pontos
            distances.append((i + 1, j + 1, dist))  # armazena o resultado em uma tupla
    
    return distances


# Função para transformar os dados e separar por tipo de peso
def data_transformation(content):
    weight_type = [
        line.split(":")[1].strip() 
        for line in content.splitlines() 
        if "EDGE_WEIGHT_TYPE" in line
    ]
    
    geo_data = []  # Para armazenar as distâncias GEO
    euclidean_data = []  # Para armazenar as coordenadas EUC_2D
    
    if weight_type[0] == "EUC_2D":
        euclidean_data = euclidean_conversion(content)  # chama a conversão para o tipo EUC_2D
    elif weight_type[0] == "GEO":
        geo_data = haversine_conversion(content)  # chama a conversão para o tipo GEO
    
    return geo_data, euclidean_data

# função para ler as instâncias 
def read_instances(path):
    
    files = [
        f for f in os.listdir(path) if f.endswith(".ins") 
    ]
    
    for file in sorted(files):
        file_path = os.path.join(path, file)
        try:
            with open(file_path, "r") as f:
                content = f.read()
                data_transformation(content)
            
        except Exception as e:
            print(f"Erro ao ler o arquivo {file}: {e}")

def main():
    input_path = "./instances"
    read_instances(input_path)
    print('ok')

if __name__ == "__main__":
    main()
