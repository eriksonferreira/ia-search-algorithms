from cmath import sqrt
from Space import *
from Constants import *
from queue import PriorityQueue
import pygame


def printPath(g: Graph, sc: pygame.Surface, path):
    if (path[g.goal.value] == -1):
        print("No have path")
        return
    temp = []
    goal = g.goal.value
    g.change_color_node_in_grid_cells(g.goal, purple, sc)
    g.change_color_node_in_grid_cells(g.start, orange, sc)

    while (True):
        temp.append(goal)
        goal = path[goal]
        if (goal == g.start.value):
            temp.append(goal)
            break

    for i in temp:
        if i != g.goal.value and i != g.start.value:
            g.change_color_node_in_grid_cells(g.grid_cells[i], grey, sc)
            pygame.draw.line(sc, green, (g.grid_cells[i].x, g.grid_cells[i].y), (
                g.grid_cells[path[i]].x, g.grid_cells[path[i]].y))
            pygame.display.update()
    return


def DFS(g: Graph, sc: pygame.Surface):
    print('Implement DFS algorithm')

    startNode = g.start
    closed_set = []
    open_set = []
    father = [-1]*g.get_len()

    open_set.append(startNode)

    while len(open_set) != 0:
        currentNode = open_set.pop(0)

        if (g.is_goal(currentNode)):
            g.change_color_node_in_grid_cells(currentNode, purple, sc)
            closed_set.append(currentNode)
            break
        if (currentNode.value != g.start.value):
            g.change_color_node_in_grid_cells(currentNode, yellow, sc)

        if (currentNode not in closed_set):
            neighbors = g.get_neighbors(currentNode)
            noConsiderdNeighbors = []
            for neighbor in neighbors:
                if (neighbor not in closed_set and neighbor not in open_set):
                    noConsiderdNeighbors.append(neighbor)
                    g.change_color_node_in_grid_cells(neighbor, red, sc)
                if (neighbor not in closed_set):
                    father[neighbor.value] = currentNode.value

            open_set = noConsiderdNeighbors + open_set
            closed_set.append(currentNode)
            if (currentNode.value != startNode.value):
                g.change_color_node_in_grid_cells(currentNode, blue, sc)
    printPath(g, sc, father)


def BFS(g: Graph, sc: pygame.Surface):
    print('Implement BFS algorithm')

    open_set = [g.start]
    closed_set = []
    father = [-1]*g.get_len()

    while (len(open_set) != 0):
        # Set currentNode
        currentNode = open_set.pop(0)

        # Check if is goal
        if (g.is_goal(currentNode)):
            g.change_color_node_in_grid_cells(currentNode, purple, sc)
            closed_set.append(currentNode)
            break

        if (currentNode.value != g.goal.value and currentNode.value != g.start.value):
            g.change_color_node_in_grid_cells(currentNode, yellow, sc)
        # Add neighbors of currentNode
        neighbors = g.get_neighbors(currentNode)
        for neighbor in neighbors:
            isNotVisited = (
                neighbor not in closed_set) and neighbor not in open_set
            if (isNotVisited):
                open_set.append(neighbor)
                if (neighbor.value != g.goal.value):
                    g.change_color_node_in_grid_cells(neighbor, red, sc)
                father[neighbor.value] = currentNode.value

        if (currentNode.value != g.goal.value and currentNode.value != g.start.value):
            g.change_color_node_in_grid_cells(currentNode, blue, sc)
        closed_set.append(currentNode)
    printPath(g, sc, father)


def calculate_distance(g: Graph, s: int, f: int):
    result = int(((g.grid_cells[s].x - g.grid_cells[f].x) **
                 2 + (g.grid_cells[s].y - g.grid_cells[f].y)**2)**0.5)

    return result


def UCS(g: Graph, sc: pygame.Surface):
    print('Implement UCS algorithm')

    open_set = PriorityQueue()
    open_set.put((0, g.start.value))
    closed_set = []
    father = [-1]*g.get_len()

    while not open_set.empty():
        currentNode = open_set.get()
        if (currentNode[1] != g.start.value):
            g.change_color_node_in_grid_cells(
                g.grid_cells[currentNode[1]], yellow, sc)

        if (g.goal.value == currentNode[1]):
            break

        neighbors = g.get_neighbors(g.grid_cells[currentNode[1]])
        if (len(neighbors) > 0):
            for neighbor in neighbors:
                temp_distance = currentNode[0] + \
                    calculate_distance(g, currentNode[1], neighbor.value)
                isExist = False
                for i in range(len(open_set.queue)):
                    if (open_set.queue[i][1] == neighbor.value):
                        isExist = True
                        break

                if neighbor.value not in closed_set and not isExist:
                    father[neighbor.value] = currentNode[1]
                    open_set.put((temp_distance, neighbor.value))
                    g.change_color_node_in_grid_cells(neighbor, red, sc)
                elif isExist:
                    father[neighbor.value] = currentNode[1]
                    open_set.put((temp_distance, neighbor.value))

        closed_set.append(currentNode[1])
        new_open_set = PriorityQueue()
        for i in range(len(open_set.queue)):
            item = open_set.queue[i]
            if (item[1] != currentNode[1]):
                new_open_set.put((item[0], item[1]))
        if (currentNode[1] != g.start.value):
            g.change_color_node_in_grid_cells(
                g.grid_cells[currentNode[1]], blue, sc)

        open_set = new_open_set
    printPath(g, sc, father)


def AStar(g: Graph, sc: pygame.Surface):
    print('Implement A* algorithm')

    open_set = PriorityQueue()
    open_set.put((0, g.start.value))
    closed_set: list[int] = []
    father = [-1]*g.get_len()

    while not open_set.empty():
        currentNode = open_set.get()
        if (currentNode[1] != g.start.value):
            g.change_color_node_in_grid_cells(
                g.grid_cells[currentNode[1]], yellow, sc)

        if (g.is_goal(g.grid_cells[currentNode[1]])):
            break
        neighbors = g.get_neighbors(g.grid_cells[currentNode[1]])
        for neighbor in neighbors:
            if neighbor.value not in closed_set:
                open_set.put(
                    (calculate_distance(g, g.goal.value, neighbor.value), neighbor.value))

                g.change_color_node_in_grid_cells(neighbor, red, sc)
                father[neighbor.value] = currentNode[1]
                closed_set.append(neighbor.value)

        closed_set.append(currentNode[1])
        if (currentNode[1] != g.start.value):
            g.change_color_node_in_grid_cells(
                g.grid_cells[currentNode[1]], blue, sc)
    printPath(g, sc, father)
