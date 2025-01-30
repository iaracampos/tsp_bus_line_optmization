TSP Solver - Caixeiro Viajante

Este projeto implementa uma solução para o problema do Caixeiro Viajante (TSP) utilizando técnicas de otimização, incluindo um algoritmo guloso aprimorado e o método de busca local 2-opt para refinamento das soluções.
Descrição

O objetivo do algoritmo é resolver instâncias do problema TSP, onde o objetivo é determinar o menor caminho que visita todas as cidades exatamente uma vez e retorna à cidade inicial. O projeto foi desenvolvido para processar instâncias em formatos com coordenadas geográficas (GEO) ou coordenadas euclidianas (EUC_2D), calculando as distâncias entre os nós e buscando uma solução eficiente.

O algoritmo implementa as seguintes etapas:

    Algoritmo Guloso (Optimized Greedy): Um algoritmo de aproximação que constrói um tour inicial escolhendo aleatoriamente entre os melhores candidatos com base na distância máxima.
    Refinamento com 2-opt: Um processo de otimização local que melhora o tour, tentando inverter segmentos de caminho e avaliando as melhorias. O refinamento é repetido várias vezes para melhorar a solução.

Funcionalidades

    Leitura de instâncias: Suporta arquivos de instâncias no formato .ins, com suporte para diferentes tipos de distâncias (EUC_2D ou GEO).
    Cálculo de matriz de distâncias: Gera a matriz de distâncias entre os nós usando distância euclidiana ou Haversine para coordenadas geográficas.
    Algoritmo Guloso: Aplica um algoritmo guloso otimizado para encontrar uma solução inicial.
    Refinamento 2-opt: Melhora a solução inicial trocando segmentos do tour, repetindo até alcançar a melhor solução possível dentro de um limite de tentativas.
    Gravação de soluções: Gera soluções em arquivos de texto, informando a distância máxima, tempo de execução e economia percentual.

Instalação

Clone este repositório para o seu ambiente local:

git clone https://github.com/iaracampos/tsp_bus_line_optmization
cd tsp_bus_line_optmization

O script vai:

    Ler os arquivos de instâncias localizados na pasta ./instances.
    Resolver cada instância usando o algoritmo guloso otimizado e 2-opt.
    Salvar as soluções no diretório ./tsp_solutions e exibir os resultados no terminal.

Exemplo de Execução

Instância 01:
 - Distância Máxima: 5572.5 (Alvo: 3986)
 - Tempo: 7.744s
 - Economia: -39.8%

Instância 02:
 - Distância Máxima: 1341.4 (Alvo: 1289)
 - Tempo: 16.145s
 - Economia: -4.1%

Dependências

    numpy: Para cálculos e manipulação de dados em arrays.
    haversine: Para cálculo de distâncias geográficas com a fórmula de Haversine.

Instale as dependências com o comando:

pip install numpy haversine


Colaboradores  Iara Campos 
Gabriel Camargos Alves

