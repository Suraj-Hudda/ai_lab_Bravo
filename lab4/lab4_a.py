import numpy as np
import matplotlib.pyplot as plt
import random

locations = {
    'Jaipur': (26.9124, 75.7873),
    'Udaipur': (24.5710, 73.6915),
    'Jaisalmer': (26.9157, 70.9164),
    'Jodhpur': (26.2389, 73.0243),
    'Ajmer': (26.4499, 74.6399),
    'Pushkar': (26.4880, 74.5558),
    'Bikaner': (28.0216, 73.3118),
    'Chittorgarh': (24.8792, 74.6310),
    'Mount Abu': (24.5920, 72.7022),
    'Ranthambore': (26.0155, 76.3632),
    'Kota': (25.2138, 75.8648),
    'Alwar': (27.5521, 76.6012),
    'Sikar': (27.6091, 75.1392),
    'Tonk': (26.0638, 75.6104),
    'Neemrana': (27.1002, 76.4310),
    'Mandawa': (27.1544, 75.1364),
    'Dausa': (26.8702, 75.2499),
    'Barmer': (25.7500, 71.3928),
    'Sawai Madhopur': (25.9984, 76.3680),
    'Jhalawar': (23.5962, 76.1665)
}

def calculate_distance_matrix(locations):
    n = len(locations)
    distance_matrix = np.zeros((n, n))
    location_list = list(locations.values())
    
    for i in range(n):
        for j in range(n):
            if i != j:
                distance = np.sqrt((location_list[i][0] - location_list[j][0]) ** 2 +
                                   (location_list[i][1] - location_list[j][1]) ** 2)
                distance_matrix[i][j] = distance
    return distance_matrix

def simulated_annealing(distance_matrix, initial_temp=1000, cooling_rate=0.995, num_iterations=10000):
    n = len(distance_matrix)
    current_solution = np.random.permutation(n)
    current_cost = calculate_cost(current_solution, distance_matrix)
    
    best_solution = np.copy(current_solution)
    best_cost = current_cost
    
    temperature = initial_temp
    
    for iteration in range(num_iterations):
        new_solution = np.copy(current_solution)
        i, j = random.sample(range(n), 2)
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        
        new_cost = calculate_cost(new_solution, distance_matrix)
        
        if new_cost < current_cost or random.uniform(0, 1) < np.exp((current_cost - new_cost) / temperature):
            current_solution = new_solution
            current_cost = new_cost
            
            if current_cost < best_cost:
                best_solution = np.copy(current_solution)
                best_cost = current_cost
        
        temperature *= cooling_rate
    
    return best_solution, best_cost

def calculate_cost(solution, distance_matrix):
    total_cost = 0
    for i in range(len(solution)):
        total_cost += distance_matrix[solution[i], solution[(i + 1) % len(solution)]]
    return total_cost

def plot_route(solution, locations):
    location_list = list(locations.keys())
    route = [location_list[i] for i in solution] + [location_list[solution[0]]]
    
    x = [locations[city][0] for city in route]
    y = [locations[city][1] for city in route]
    
    plt.figure(figsize=(10, 6))
    plt.plot(x, y, marker='o')
    plt.title('Optimal Route in Rajasthan')
    plt.xlabel('Latitude')
    plt.ylabel('Longitude')
    for i, city in enumerate(route[:-1]):
        plt.text(x[i], y[i], city, fontsize=9)
    plt.show()

distance_matrix = calculate_distance_matrix(locations)
best_solution, best_cost = simulated_annealing(distance_matrix)
print("Best Route:", [list(locations.keys())[i] for i in best_solution])
print("Minimum Cost:", best_cost)

plot_route(best_solution, locations)
