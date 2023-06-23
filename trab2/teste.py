import random
import math
import matplotlib.pyplot as plt

def rastrigin(x, y):
    return 20 + x**2 - 10 * math.cos(2 * math.pi * x) + y**2 - 10 * math.cos(2 * math.pi * y)

def hill_climbing():
    restarts = 20
    iterations = 1000
    restart_iter = 50
    
    best_solution = None
    best_fitness = float('inf')
    
    for restart in range(restarts):
        x = random.uniform(-5.12, 5.12)
        y = random.uniform(-5.12, 5.12)
        
        for iteration in range(iterations):
            current_fitness = rastrigin(x, y)
            
            if current_fitness < best_fitness:
                best_solution = (x, y)
                best_fitness = current_fitness
            
            # Produzir vizinho
            delta_x = random.gauss(0, 0.1)
            delta_y = random.gauss(0, 0.1)
            neighbor_x = x + delta_x
            neighbor_y = y + delta_y
            
            if -5.12 <= neighbor_x <= 5.12 and -5.12 <= neighbor_y <= 5.12:
                neighbor_fitness = rastrigin(neighbor_x, neighbor_y)
                
                if neighbor_fitness < current_fitness:
                    x = neighbor_x
                    y = neighbor_y
        
            # Realizar restart
            if iteration % restart_iter == 0:
                x = random.uniform(-5.12, 5.12)
                y = random.uniform(-5.12, 5.12)
    
    return best_solution

# Execução do Hill-Climbing
solution_hc = hill_climbing()
print("Hill-Climbing Solution:", solution_hc)
