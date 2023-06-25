# -*- coding: utf-8 -*-
"""trab2.ipynb

Automatically generated by Colaboratory.

Original file is located at
    https://colab.research.google.com/drive/1qXrIu487fQq9OqR1JWD0nMYQo-K0toXx

# Trabalho 2 - Erikson Ferreira

## Importações
"""

# Manipulação de dados
import numpy as np
import pandas as pd

# Geração de números aleatórios
import random

# Geração de gráficos
import matplotlib.pyplot as plt
import seaborn as sns
import plotly.express as px
import plotly.graph_objects as go
import math
from tqdm import tqdm
"""## Funções Auxiliares

### Solução Aleatória
"""

# Cria uma solucao inicial com as cidades em um ordem aleatoria

def solucao_aleatoria(tsp):
    cidades = list(tsp.keys())
    solucao = []

    # as 3 linhas abaixo não são estritamente necessarias, servem
    # apenas para fixar a primeira cidade da lista na solução
    cidade = cidades[0]
    solucao.append(cidade)
    cidades.remove(cidade)

    for _ in range(0,len(cidades)):
        #print(_, cidades, solucao)
        cidade = random.choice(cidades)

        solucao.append(cidade)
        cidades.remove(cidade)

    return solucao

"""### Calcula Custo"""

# Função Objetivo: calcula custo de uma dada solução.
# Obs: Neste caso do problema do caixeiro viajante (TSP problem),
# o custo é o comprimento da rota entre todas as cidades.
def calcula_custo(tsp, solucao):

    N = len(solucao)
    custo = 0

    for i in range(N):

        # Quando chegar na última cidade, será necessário
        # voltar para o início para adicionar o
        # comprimento da rota da última cidade
        # até a primeira cidade, fechando o ciclo.
        #
        # Por isso, a linha abaixo:
        k = (i+1) % N
        cidadeA = solucao[i]
        cidadeB = solucao[k]

        custo += tsp.loc[cidadeA, cidadeB]

        #print(tsp.loc[cidadeA, cidadeB], cidadeA,cidadeB)

    return custo

"""### Gera Vizinhos

Obs: a função `obtem_vizinhos` descrita abaixo foi gerada de forma simplificada, pois ela assume que todos os vizinhos possuem rota direta entre si. Isto tem caráter didático para simplifcar a solução. Observe que na prática isso nem sempre existe rotas diretas entre todas as cidades e, em tais casos, pode ser necessário modificar a função para corresponder a tais restrições.
"""

# A partir de uma dada solução, gera diversas variações (vizinhos)
def gera_vizinhos(solucao):

    N = len(solucao)
    for i in range(1, N):       # deixa o primeiro fixo
        for j in range(i + 1, N):
            vizinho = solucao.copy()
            vizinho[i] = solucao[j]
            vizinho[j] = solucao[i]

            yield(vizinho)

"""### Seleciona Melhor Vizinho"""

def obtem_melhor_vizinho(tsp, solucao):
    melhor_custo = calcula_custo(tsp, solucao)
    melhor_vizinho = solucao

    for vizinho in gera_vizinhos(solucao):
        custo_atual = calcula_custo(tsp, vizinho)
        if custo_atual < melhor_custo:
            melhor_custo = custo_atual
            melhor_vizinho = vizinho

    return melhor_vizinho, melhor_custo

"""### Random-Walk - clássico"""

def obtem_vizinho_aleatorio(tsp, solucao):

    vizinhos = list(gera_vizinhos(solucao))

    aleatorio_vizinho  = random.choice(vizinhos)
    aleatorio_custo    = calcula_custo(tsp, aleatorio_vizinho)

    return aleatorio_vizinho, aleatorio_custo

def random_walk(tsp):
    solucao_inicial = solucao_aleatoria(tsp)

    atual_solucao, atual_custo = obtem_vizinho_aleatorio(tsp, solucao_inicial)

    for _ in range(30):
        atual_solucao, atual_custo = obtem_vizinho_aleatorio(tsp, atual_solucao)

    return atual_custo, atual_solucao

"""### Hill-Climbing - clássico"""

def hill_climbing(tsp):
    history = []
    # solucao inicial
    solucao_inicial = solucao_aleatoria(tsp)
    # print(solucao_inicial)
    # melhor solucao ate o momento
    solucao_melhor, custo_melhor = obtem_melhor_vizinho(tsp, solucao_inicial)


    while True:

        # tenta obter um candidato melhor
        candidato_atual, custo_atual = obtem_melhor_vizinho(tsp, solucao_melhor)
        #print(custo_melhor, custo_atual)

        if custo_atual < custo_melhor:
            custo_melhor   = custo_atual
            solucao_melhor = candidato_atual
            history.append(solucao_melhor)
        else:
            history.append(solucao_melhor)
            break   # custo nao melhorou, entao sai do while

    return custo_melhor, solucao_melhor, history

"""### Hill-Climbing - Restart"""

def hill_climbing_restart(tsp, restarts=50):

    # solucao inicial
    history = []


    solucao_melhor = solucao_aleatoria(tsp)
    custo_melhor = float("inf")


    for _ in range(restarts):

        # tenta obter um candidato melhor
        candidato_atual, custo_atual = obtem_melhor_vizinho(tsp, solucao_melhor)
        # print(custo_atual, custo_melhor)
        if custo_atual < custo_melhor:
            custo_melhor   = custo_atual
            solucao_melhor = candidato_atual
            # print(custo_melhor)
            history.append(solucao_melhor)


    return custo_melhor, solucao_melhor, history

"""### Simulated Annealing"""

def calculate_distance(city_a, city_b):
    return np.linalg.norm(city_a - city_b)

def total_distance(solucao, tsp):
    solucao = ['A' + str(num) for num in solucao]
    N = len(solucao)
    # print(N)
    custo = 0
    for i in range(N):
        k = (i+1) % N
        cidadeA = solucao[i]
        cidadeB = solucao[k]
        # print(cidadeA, cidadeB)
        custo += tsp.loc[cidadeA, cidadeB]
    # print(custo)
    return custo

def generate_neighbor(route):
    new_route = route.copy()
    index_a = random.randint(0, len(route) - 1)
    index_b = random.randint(0, len(route) - 1)
    new_route[index_a], new_route[index_b] = new_route[index_b], new_route[index_a]
    return new_route

def acceptance_probability(current_distance, new_distance, temperature):
    if new_distance < current_distance:
        return 1.0
    else:
        return math.exp((current_distance - new_distance) / temperature)

def simulated_annealing(cities, initial_temperature = 1000, cooling_rate=0.90, iterations=50):
    cities_df = cities.copy()
    cities = cities.to_numpy()
    num_cities = len(cities)
    distance_matrix = np.zeros((num_cities, num_cities))

    for i in range(num_cities):
        for j in range(num_cities):
            distance_matrix[i, j] = calculate_distance(cities[i], cities[j])

    current_route = np.arange(num_cities)
    best_route = current_route.copy()

    current_distance = total_distance(current_route, cities_df)
    best_distance = current_distance

    temperature = initial_temperature

    #-----------------------------------------------
    iteration_list = []
    best_distances = []
    distance_list  = []
    accept_p_list  = []
    temperat_list  = []
    #-----------------------------------------------

    for iteration in range(iterations):
        new_route = generate_neighbor(current_route)
        new_distance = total_distance(new_route, cities_df)

        acceptance_prob = acceptance_probability(current_distance, new_distance, temperature)

        #print(acceptance_prob)

        if random.random() < acceptance_prob:
            current_route = new_route
            current_distance = new_distance

        if new_distance < best_distance:
            best_route = new_route
            best_distance = new_distance
            # print(best_distance)

        temperature *= cooling_rate

        #-----------------------------------------------
        iteration_list += [iteration]
        best_distances += [best_distance]
        distance_list  += [current_distance]
        accept_p_list  += [acceptance_prob]
        temperat_list  += [temperature]

        #-----------------------------------------------


    # plt.show()

    best_route = ['A' + str(num) for num in best_route]
    history = [best_route,{
        'iteration_list': iteration_list,
        'best_distances': best_distance,
        'distance_list': current_distance,
        'accept_p_list': accept_p_list,
        'temperature': temperature
    }]
    return best_distance, best_route, history

"""### Genetic Algorithm"""

def generate_initial_population(cities, population_size):
    population = []
    for _ in range(population_size):
        path = random.sample(sorted(cities), len(cities))
        population.append(path)
    return population

def selection(population, cities):
    tournament_size = 5
    selected = []

    while len(selected) < len(population):
        tournament = random.sample(population, tournament_size)
        best_path = min(tournament, key=lambda path: calculate_total_distance(path, cities))
        selected.append(best_path)

    return selected

def crossover(population):
    new_population = []
    for i in range(0, len(population), 2):
        parent1 = population[i]
        parent2 = population[i+1]
        child1 = order_crossover(parent1, parent2)
        child2 = order_crossover(parent1, parent2)
        new_population.extend([child1, child2])
    return new_population

def order_crossover(parent1, parent2):
    start_index, end_index = sorted(random.sample(range(len(parent1)), 2))
    child = [-1] * len(parent1)

    # Copia a parte selecionada do pai 1 para o filho
    child[start_index:end_index + 1] = parent1[start_index:end_index + 1]

    # Preenche o restante do filho com as cidades do pai 2
    remaining_cities = [city for city in parent2 if city not in child]

    j = 0
    for i in range(len(parent1)):
        if child[i] == -1:
            child[i] = remaining_cities[j]
            j += 1

    return child

def mutation(population, mutation_rate):
    mutated_population = []
    for path in population:
        if np.random.rand() < mutation_rate:
            mutated_path = path.copy()
            # Escolhe aleatoriamente duas posições diferentes no trajeto
            idx1, idx2 = np.random.choice(len(mutated_path), size=2, replace=False)
            # Troca as posições das cidades
            mutated_path[idx1], mutated_path[idx2] = mutated_path[idx2], mutated_path[idx1]
            mutated_population.append(mutated_path)
        else:
            mutated_population.append(path)
    return mutated_population

def calculate_distance(city_a, city_b):
    return np.linalg.norm(np.array(city_a) - np.array(city_b))

def calculate_total_distance(solucao, tsp):
    # solucao = ['A' + str(num) for num in solucao]
    N = len(solucao)
    # print(N)
    custo = 0
    for i in range(N):
        k = (i+1) % N
        cidadeA = solucao[i]
        cidadeB = solucao[k]
        # print(cidadeA, cidadeB)
        custo += tsp.loc[cidadeA, cidadeB]
    # print(custo)
    return custo

def tsp_genetic(cities, population_size=100, num_generations=50, mutation_rate=0.15):

    history = []
    population = generate_initial_population(cities, population_size)

    for _ in range(num_generations):
        population = selection(population, cities)
        history.append(len(population))
        population = crossover(population)
        history.append(len(population))
        population = mutation(population, mutation_rate)
        history.append(len(population))
        # print(population)


    best_path = min(population, key=lambda path: calculate_total_distance(path, cities))
    best_distance = calculate_total_distance(best_path, cities)

    return best_distance, best_path, history

"""### Cálculo da Matriz de Distâncias"""

from math import sqrt

# distancia Euclidiana entre dois pontos
def distancia(x1,y1,x2,y2):
    dx = x2 - x1
    dy = y2 - y1
    return sqrt(dx**2 + dy**2)

# Calcula matriz de distancias.
#
# OBS:  Não é estritamente necessario calculá-las a priori.
#       Foi feito assim apenas para fins didáticos.
#       Ao invés, as distâncias podem ser calculadas sob demanda.

def gera_matriz_distancias(Coordenadas):

    n_cidades = len(Coordenadas)
    dist = np.zeros((n_cidades,n_cidades), dtype=float)

    for i in range(0, n_cidades):
        for j in range(i+1, n_cidades):
            x1,y1 = Coordenadas.iloc[i]
            x2,y2 = Coordenadas.iloc[j]

            dist[i,j] = distancia(x1,y1,x2,y2)
            dist[j,i] = dist[i,j]

    return dist

"""### Gerador de Problemas Aleatórios"""

# Gera aleatoriamente as coordenadas de N cidades.
# Obs: esta informação geralmente é fornecida como entrada do problema.

def gera_coordenadas_aleatorias(n_cidades):
    minimo = 10
    maximo = 90
    escala = (maximo-minimo)-1

    # gera n coordenadas (x,y) aleatorias entre [min, max]
    X = minimo + escala * np.random.rand(n_cidades)
    Y = minimo + escala * np.random.rand(n_cidades)
    coordenadas = {'X':X, 'Y': Y}

    cidades = ['A'+str(i) for i in range(n_cidades)]

    df_cidades = pd.DataFrame(coordenadas, index=cidades)
    df_cidades.index.name = 'CIDADE'

    return df_cidades

# Recebe uma lista com as coordenadas reais de uma cidade e
# gera uma matriz de distancias entre as cidades.
# Obs: a matriz é simetrica e com diagonal nula
def gera_problema_tsp(df_cidades):
    # nomes ficticios das cidades
    cidades = df_cidades.index

    # calcula matriz de distancias
    distancias = gera_matriz_distancias(df_cidades)

    # cria estrutura para armazena as distâncias entre todas as cidades
    tsp = pd.DataFrame(distancias, columns=cidades, index=cidades)

    return tsp

"""### Plota Rotas"""

# Plota a solução do roteamento das cidades
# usando a biblioteca PLOTLY
def plota_rotas(df_cidades, ordem_cidades):
    df_solucao = df_cidades.copy()
    df_solucao = df_solucao.reindex(ordem_cidades)

    X = df_solucao['X']
    Y = df_solucao['Y']
    cidades = list(df_solucao.index)

    # cria objeto gráfico
    fig = go.Figure()

    fig.update_layout(autosize=False, width=500, height=500, showlegend=False)

    # gera linhas com as rotas da primeira ate a ultima cidade
    fig.add_trace(go.Scatter(x=X, y=Y,
                             text=cidades, textposition='bottom center',
                             mode='lines+markers+text',
                             name=''))

    # acrescenta linha da última para a primeira para fechar o ciclo
    fig.add_trace(go.Scatter(x=X.iloc[[-1,0]], y=Y.iloc[[-1,0]],
                             mode='lines+markers', name=''))

    fig.show()


# Cria estruta de dados (DataFrame) para armazenar vários resultados
# diferentes e visualizá-los através de estatísticas

def cria_df_custos(algoritmos, n_vezes):

    nomes_algoritmos  = algoritmos.keys()

    n_lin = len(nomes_algoritmos)
    n_col = n_vezes

    df_results = pd.DataFrame(np.zeros((n_lin,n_col)),
                              index=nomes_algoritmos)
    df_results.index.name='ALGORITMO'

    return df_results

# Executa N vezes para gerar estatísticas da variável custo
# Executa N vezes para gerar estatísticas da variável custo
def executa_n_vezes(tsp, algoritmos, n_vezes):
    
    # Cria DataFrame para armazenar os resultados
    df_custo = cria_df_custos(algoritmos, n_vezes)
    df_history = pd.DataFrame(columns=algoritmos.keys())
    df_solucao = pd.DataFrame()
    df_hill_climbing = pd.DataFrame()
    df_hill_climbing_restart = pd.DataFrame()
    df_genetic_algorithm = pd.DataFrame()
    df_genetic_algorithm_population = pd.DataFrame()
    df_simulated_annealing = pd.DataFrame()
    df_simulated_annealing_history = pd.DataFrame()
    for algoritmo, funcao_algoritmo in algoritmos.items():

        print(algoritmo)

        for i, count in zip(range(n_vezes), tqdm(range(n_vezes))):
            df = None
            # if algoritmo != 'Genetic Algorithm':
            custo, solucao, historico = funcao_algoritmo(tsp)
            df_temp = pd.DataFrame(solucao)
         
            
            if algoritmo == 'Hill-Climbing':
                df_hill_climbing = pd.concat([df_hill_climbing, df_temp.T], axis =0).reset_index(drop=True)
            
            elif algoritmo == 'Hill-Climbing Restart':
                df_hill_climbing_restart = pd.concat([df_hill_climbing_restart, df_temp.T], axis =0).reset_index(drop=True)
            
            elif algoritmo == 'Genetic Algorithm':
                df_genetic_algorithm = pd.concat([df_genetic_algorithm, df_temp.T], axis =0).reset_index(drop=True)
                df  = pd.DataFrame([historico])
                df_genetic_algorithm_population = pd.concat([df_genetic_algorithm_population, df], axis =0).reset_index(drop=True)

            elif algoritmo == 'Simulated Annealing':
                df  = pd.DataFrame([historico[1]], columns=historico[1].keys())
                df_simulated_annealing = pd.concat([df_simulated_annealing, df], axis =0).reset_index(drop=True)
                df_simulated_annealing_history = pd.concat([df_simulated_annealing_history, df_temp.T], axis =0).reset_index(drop=True)
            
    
            df_custo.loc[algoritmo,i] = custo
     
            # else:
                # custo, solucao = funcao_algoritmo(df_coord)
                # df_custo.loc[algoritmo,i] = custo

            # print(f'{custo:10.3f}  {solucao}')

    return df_custo, df_history, df_hill_climbing, df_hill_climbing_restart, df_simulated_annealing, df_simulated_annealing_history, df_genetic_algorithm, df_genetic_algorithm_population


# Dicionario com Nomes dos modelos e suas respectivas variantes
# Tuple: (Algoritmo, Variante): funcao_algoritmo
algoritmos = {

    'Hill-Climbing': hill_climbing,
    'Hill-Climbing Restart': hill_climbing_restart,
    'Simulated Annealing': simulated_annealing,
    'Genetic Algorithm': tsp_genetic,

}

"""#### PROBLEMA GERADO ALEATORIAMENTE"""

###################################
# PROBLEMA GERADO ALEATORIAMENTE  #
###################################

# cria instancia do problema com n cidades

n_cidades=30
df_coordenadas = gera_coordenadas_aleatorias(n_cidades)
df_coordenadas.to_csv("df_coordenadas.csv", sep=",")
tsp = gera_problema_tsp(df_coordenadas)
tsp.to_csv("tsp.csv", sep=",")



# numero de vezes que executará cada algoritmo
n_vezes = 1000

# Executa N vezes para gerar estatísticas da variável custo
df_custo, df_history, df_hill_climbing, df_hill_climbing_restart, df_simulated_annealing, df_simulated_annealing_history, df_genetic_algorithm, df_genetic_algorithm_population = executa_n_vezes(tsp, algoritmos, n_vezes)

###################################
# EXPORTANDO RESULTADOS PARA CSV  #
###################################

df_custo.to_csv("custo", sep=",")
df_history.to_csv("historico", sep=",")
df_hill_climbing.to_csv("hill_climbing", sep=",")
df_hill_climbing_restart.to_csv("hill_climbing_restart", sep=",")
df_simulated_annealing.to_csv("simulated_annealing_info", sep=",")
df_simulated_annealing_history.to_csv("simulted_annealing", sep=",")
df_genetic_algorithm.to_csv("genetic_algorithm", sep=",")
df_genetic_algorithm_population.to_csv("genetic_algorithm_population", sep=",")
