import pandas as pd
import platform
import psutil
import matplotlib.pyplot as plt
from pandas.plotting import table

def generate_results_table(results):#mudar se necessario 
    """
    Gera uma tabela de resultados computacionais.

    Parâmetros:

        results: nao sabemos em que formato estarao os resultados

    Retorna:
        foto tabela
    """
    # Configurações do computador
    system_info = platform.uname()
    memory_info = psutil.virtual_memory()

    config = {
        "Sistema Operacional": system_info.system,
        "Versão do SO": system_info.version,
        "Processador": system_info.processor,
        "Memória Total (GB)": round(memory_info.total / (1024 ** 3), 2),
    }

    # Criar da tabela
    df = pd.DataFrame(results)
    df["Desvio Inicial (%)"] = 100 * (df["Solução Inicial"] - df["Solução Final"]) / df["Solução Inicial"]
    df["Configuração do Computador"] = [config for _ in range(len(df))]

    # Salvar a tabela como CSV
    df.to_csv("results_table.csv", index=False)
    print("Tabela salva como 'results_table.csv'")

    # Criar a imagem da tabela
    fig, ax = plt.subplots(figsize=(10, 4)) 
    ax.axis('off')  # Desligar os eixos
    tbl = table(ax, df, loc='center', cellLoc='center', colWidths=[0.1] * len(df.columns))  
    tbl.auto_set_font_size(False)  
    tbl.set_fontsize(10) 
    tbl.scale(1.2, 1.2)  

    # Salvar a tabela como imagem
    plt.savefig("results_table.png", bbox_inches='tight', dpi=300)
    print("Tabela salva como 'results_table.png'")

    return df
