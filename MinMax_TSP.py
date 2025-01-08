import os

def read_instances(path):
     files = [f for f in os.listdir(path) if f.endswith(".ins")]#Pega nome das instancias


     #Fazendo leitura
     for file in sorted(files):  # Ordena os arquivos por nome
        file_path = os.path.join(path, file)
        try:
            with open(file_path, "r") as f:
                content = f.read()
                print(f"Conteúdo de {file}:")
                print(content)
                print("-" * 50)  # Separador entre arquivos
        except Exception as e:
            print(f"Erro ao ler o arquivo {file}: {e}")


def main():

    name_file = input()
    path = "./instances"

    read_instances(path)

if __name__ == "__main__":
    main()
