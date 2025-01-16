import os
from haversine import haversine, Unit

def haversine_conversion(content):

    coordinates = []  # Lista para armazenar as coordenadas
    in_node_section = False  # Flag para verificar se estamos na seção de nós
    
    for line in content.splitlines():
        if "NODE_COORD_SECTION" in line:  # Marca o início da seção de coordenadas
            in_node_section = True
            continue
        if "EOF" in line:  # Marca o final da seção
            break
        if in_node_section:
            parts = line.split()
            if len(parts) >= 3:  
                _, x, y = parts
                coordinates.append((float(x), float(y)))
    
    # Calcula as distâncias usando Haversine
    distances = []
    for i in range(len(coordinates)):
        for j in range(i + 1, len(coordinates)):
            dist = haversine(coordinates[i], coordinates[j], unit=Unit.KILOMETERS)
            distances.append((i + 1, j + 1, dist))
    
    print("Distâncias calculadas (em km):")
    for i, j, dist in distances:
        print(f"Entre {i} e {j}: {dist:.2f} km")

def data_transformation(content):

    weight_type = [
        line.split(":")[1].strip() 
        for line in content.splitlines() 
        if "EDGE_WEIGHT_TYPE" in line
    ]
    if weight_type and weight_type[0] == "GEO":
        haversine_conversion(content)

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
   
    path = "./instances"
    read_instances(path)

if __name__ == "__main__":
    main()
