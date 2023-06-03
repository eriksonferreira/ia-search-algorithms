
import random

from collections import deque
from viewer import MazeViewer
from math import inf, sqrt
import time
import math
import pandas as pd 


def gera_labirinto(n_linhas, n_colunas, inicio, goal):
    # cria labirinto vazio
    labirinto = [[0] * n_colunas for _ in range(n_linhas)]

    # adiciona celulas ocupadas em locais aleatorios de
    # forma que 25% do labirinto esteja ocupado
    numero_de_obstaculos = int(0.50 * n_linhas * n_colunas)
    for _ in range(numero_de_obstaculos):
        linha = random.randint(0, n_linhas-1)
        coluna = random.randint(0, n_colunas-1)
        labirinto[linha][coluna] = 1

    # remove eventuais obstaculos adicionados na posicao
    # inicial e no goal
    labirinto[inicio.y][inicio.x] = 0
    labirinto[goal.y][goal.x] = 0

    return labirinto


class Celula:
    def __init__(self, y, x, anterior, estimativa):
        self.y = y
        self.x = x
        self.anterior = anterior
        self.estimativa = 0


def distancia(celula_1, celula_2):
    dx = celula_1.x - celula_2.x
    dy = celula_1.y - celula_2.y
    return sqrt(dx ** 2 + dy ** 2)


def esta_contido(lista, celula):
    for elemento in lista:
        if (elemento.y == celula.y) and (elemento.x == celula.x):
            return True
    return False


def custo_caminho(caminho):
    if len(caminho) == 0:
        return inf

    custo_total = 0
    for i in range(1, len(caminho)):
        custo_total += distancia(caminho[i].anterior, caminho[i])

    return custo_total


def obtem_caminho(goal):
    caminho = []

    celula_atual = goal
    while celula_atual is not None:
        caminho.append(celula_atual)
        celula_atual = celula_atual.anterior

    # o caminho foi gerado do final para o
    # comeco, entao precisamos inverter.
    caminho.reverse()

    return caminho


def celulas_vizinhas_livres(celula_atual, labirinto):
    # generate neighbors of the current state
    vizinhos = [
        Celula(y=celula_atual.y-1, x=celula_atual.x-1, anterior=celula_atual, estimativa=0),
        Celula(y=celula_atual.y+0, x=celula_atual.x-1, anterior=celula_atual, estimativa=0),
        Celula(y=celula_atual.y+1, x=celula_atual.x-1, anterior=celula_atual, estimativa=0),
        Celula(y=celula_atual.y-1, x=celula_atual.x+0, anterior=celula_atual, estimativa=0),
        Celula(y=celula_atual.y+1, x=celula_atual.x+0, anterior=celula_atual, estimativa=0),
        Celula(y=celula_atual.y+1, x=celula_atual.x+1, anterior=celula_atual, estimativa=0),
        Celula(y=celula_atual.y+0, x=celula_atual.x+1, anterior=celula_atual, estimativa=0),
        Celula(y=celula_atual.y-1, x=celula_atual.x+1, anterior=celula_atual, estimativa=0),
    ]

    # seleciona as celulas livres
    vizinhos_livres = []
    for v in vizinhos:
        # verifica se a celula esta dentro dos limites do labirinto
        if (v.y < 0) or (v.x < 0) or (v.y >= len(labirinto)) or (v.x >= len(labirinto[0])):
            continue
        # verifica se a celula esta livre de obstaculos.
        if labirinto[v.y][v.x] == 0:
            vizinhos_livres.append(v)

    return vizinhos_livres


def breadth_first_search(labirinto, inicio, goal,
                        #   viewer
                          ):
    print("Iniciando BFS")
    # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):

        # seleciona o no mais antigo para ser expandido
        no_atual = fronteira.popleft()

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        #viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos


def depth_first_search(labirinto, inicio, goal,
                        # viewer
                        ):
    print("Iniciando DFS*")
     # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):

        # seleciona o no mais antigo para ser expandido
        no_atual = fronteira.pop()

        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            else:
                if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                    fronteira.append(v)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        # viewer.pause()
        # break

    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos




def a_star_search(labirinto, inicio, goal,
                    # viewer
                   ):
    print("Iniciando A*")

 
     # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Variavel para armazenar o custo acumulado
    custos_acumulados = {inicio: 0}

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):

        # seleciona o no com menor custo acumulado
        # fronteira = sorted(fronteira)
        # print(fronteira)
        no_atual = None
        for f in fronteira:
            # print(f.estimativa)
            if no_atual == None:
                no_atual = f
            elif f.estimativa < no_atual.estimativa:
                no_atual = f    
            # print(f.estimativa)
        # print(fronteira)
        fronteira.remove(no_atual)
        # print(fronteira)
        # fronteira = sorted(fronteira)
        # fronteira = fronteira.append(fronteira)
        # no_atual = fronteira.popleft()
        # print(no_atual.estimativa)
        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            caminho = obtem_caminho(v)
            # print(custos_acumulados[no_atual])
            novo_custo = custos_acumulados[no_atual] +1

            if v not in expandidos or novo_custo < custos_acumulados[v]:
                custos_acumulados[v] = novo_custo
                estimativa_custo_total = novo_custo + distancia(v, goal) #heurística
                v.estimativa = estimativa_custo_total
                # print(custos_acumulados[no_atual])
           
            # else:
            if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                fronteira.append(v)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        #viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos


def uniform_cost_search(labirinto, inicio, goal,
                    # viewer
                   ):
    print("Iniciando UCS")

     # nos gerados e que podem ser expandidos (vermelhos)
    fronteira = deque()
    # nos ja expandidos (amarelos)
    expandidos = set()

    # adiciona o no inicial na fronteira
    fronteira.append(inicio)

    # variavel para armazenar o goal quando ele for encontrado.
    goal_encontrado = None

    # Variavel para armazenar o custo acumulado
    custos_acumulados = {inicio: 0}

    # Repete enquanto nos nao encontramos o goal e ainda
    # existem para serem expandidos na fronteira. Se
    # acabarem os nos da fronteira antes do goal ser encontrado,
    # entao ele nao eh alcancavel.
    while (len(fronteira) > 0) and (goal_encontrado is None):

        # seleciona o no mais antigo para ser expandido
        # fronteira = sorted(fronteira)
        # print(fronteira)
        no_atual = None
        for f in fronteira:
            # print(f.estimativa)
            if no_atual == None:
                no_atual = f
            elif f.estimativa < no_atual.estimativa:
                no_atual = f    
            # print(f.estimativa)
        # print(fronteira)
        fronteira.remove(no_atual)
        # print(fronteira)
        # fronteira = sorted(fronteira)
        # fronteira = fronteira.append(fronteira)
        # no_atual = fronteira.popleft()
        # print(no_atual.estimativa)
        # busca os vizinhos do no
        vizinhos = celulas_vizinhas_livres(no_atual, labirinto)

        # para cada vizinho verifica se eh o goal e adiciona na
        # fronteira se ainda nao foi expandido e nao esta na fronteira
        for v in vizinhos:
            if v.y == goal.y and v.x == goal.x:
                goal_encontrado = v
                # encerra o loop interno
                break
            novo_custo = custos_acumulados[no_atual]

            if v not in expandidos or novo_custo < custos_acumulados[v]:
                
                custos_acumulados[v] = novo_custo 
                estimativa_custo_total = novo_custo #unica diferença é o fato de não ter a heurística.
                caminho = obtem_caminho(v)
                v.estimativa = custo_caminho(caminho) + novo_custo
                # print(v.estimativa)
                # print(custos_acumulados[no_atual])
           
            # else:
            if (not esta_contido(expandidos, v)) and (not esta_contido(fronteira, v)):
                fronteira.append(v)

        expandidos.add(no_atual)

        # viewer.update(generated=fronteira,
        #               expanded=expandidos)
        #viewer.pause()


    caminho = obtem_caminho(goal_encontrado)
    custo   = custo_caminho(caminho)

    return caminho, custo, expandidos


#-------------------------------


def main():
    statistics_df = pd.DataFrame(columns=['algorithm', 'time', 'nodes_expanded', 'total_path_cost', 'n_steps'])
    while True:
        SEED = 42  # coloque None no lugar do 42 para deixar aleatorio
        random.seed(SEED)
        N_LINHAS  = 300
        N_COLUNAS = 300
        INICIO = Celula(y=0, x=0, anterior=None, estimativa=0)
        GOAL   = Celula(y=N_LINHAS-1, x=N_COLUNAS-1, anterior=None, estimativa=0)


        """
        O labirinto sera representado por uma matriz (lista de listas)
        em que uma posicao tem 0 se ela eh livre e 1 se ela esta ocupada.
        """
        labirinto = gera_labirinto(N_LINHAS, N_COLUNAS, INICIO, GOAL)

        # viewer = MazeViewer(labirinto, INICIO, GOAL,
        #                     step_time_miliseconds=20, zoom=20)

        #----------------------------------------
        # BFS Search
        #----------------------------------------
        init_bfs = time.time()
        # viewer._figname = "BFS"
        caminho, custo_total, expandidos = \
                breadth_first_search(labirinto, INICIO, GOAL, 
                                    # viewer
                                     )
        end_bfs = time.time()
        bfs_time_spent = end_bfs - init_bfs

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")
        temp_df = {'algorithm':'BFS', 'time_in_sec': bfs_time_spent, 'nodes_expanded': len(expandidos),'total_path_cost': custo_total, 'n_steps': (len(caminho)-1)}
        statistics_df = pd.concat([statistics_df,pd.DataFrame([temp_df])], ignore_index = True)
        print(
            f"BFS:"
            f"\tTempo decorrido em seg: {bfs_time_spent}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"    
        )

        # viewer.update(path=caminho)
        # viewer.pause()


        #----------------------------------------
        # DFS Search
        #----------------------------------------
        init_dfs = time.time()
        # viewer._figname = "BFS"
        caminho, custo_total, expandidos = \
                depth_first_search(labirinto, INICIO, GOAL, 
                                #    viewer
                                   )
        end_dfs = time.time()
        dfs_time_spent = end_dfs - init_dfs

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")

        temp_df = {'algorithm':'DFS', 'time': dfs_time_spent, 'nodes_expanded': len(expandidos),'total_path_cost': custo_total, 'n_steps': (len(caminho)-1)}
        statistics_df = pd.concat([statistics_df,pd.DataFrame([temp_df])], ignore_index = True)
        print(
            f"DFS:"
            f"\tTempo decorrido em seg: {dfs_time_spent}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"  
        )

        # viewer.update(path=caminho)
        # viewer.pause().

        #----------------------------------------
        # A-Star Search
        #----------------------------------------
        init_A_star = time.time()
        # viewer._figname = "A*"
        caminho, custo_total, expandidos = \
                a_star_search(labirinto, INICIO, GOAL,
                            #    viewer
                               )
        end_A_star = time.time()
        A_star_time_spent = end_A_star - init_A_star

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")
        temp_df = {'algorithm':'A-STAR', 'time': A_star_time_spent, 'nodes_expanded': len(expandidos),'total_path_cost': custo_total, 'n_steps': (len(caminho)-1)}
        statistics_df = pd.concat([statistics_df,pd.DataFrame([temp_df])], ignore_index = True)
        print(
            f"A*:"
            f"\tTempo decorrido em seg: {A_star_time_spent}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"  
        )

        # viewer.update(path=caminho)
        # viewer.pause()
       
        #----------------------------------------
        # Uniform Cost Search (Obs: opcional)
        #----------------------------------------
        init_ucs = time.time()
        # viewer._figname = "UCS"
        caminho, custo_total, expandidos = \
                uniform_cost_search(labirinto, INICIO, GOAL,
                                # viewer
                               )
        end_ucs = time.time()
        ucs_time_spent = end_ucs - init_ucs

        if len(caminho) == 0:
            print("Goal é inalcançavel neste labirinto.")
        temp_df = {'algorithm':'UCS', 'time': ucs_time_spent, 'nodes_expanded': len(expandidos),'total_path_cost': custo_total, 'n_steps': (len(caminho)-1)}
        statistics_df = pd.concat([statistics_df,pd.DataFrame([temp_df])], ignore_index = True)
        print(
            f"UCS:"
            f"\tTempo decorrido em seg: {ucs_time_spent}.\n"
            f"\tNumero total de nos expandidos: {len(expandidos)}.\n"
            f"\tCusto total do caminho: {custo_total}.\n"
            f"\tNumero de passos: {len(caminho)-1}.\n"  
        )

        # viewer.update(path=caminho)
        # viewer.pause()
        break

    print(statistics_df)
    print(statistics_df.describe())
    print("OK! Pressione alguma tecla pra finalizar...")
    input()


if __name__ == "__main__":
    main()
