import numpy as np
import matplotlib.pyplot as plt
from scipy import io
import random
import math

def load_image(file_path):
    try:
        mat_contents = io.loadmat(file_path)
        image = mat_contents['image']  # Adjust key if necessary
    except:
        raise ValueError("Failed to load the image. Please check the file path and format.")
    return image

def split_image(image, piece_size):
    h, w = image.shape
    pieces = [image[i:i+piece_size, j:j+piece_size] 
              for i in range(0, h, piece_size) 
              for j in range(0, w, piece_size)]
    return pieces

def reconstruct_image(pieces, grid_size):
    return np.block([[pieces[i*grid_size + j] for j in range(grid_size)] 
                     for i in range(grid_size)])

def edge_difference(piece1, piece2, edge):
    if edge == 'right':
        return np.sum(np.abs(piece1[:, -1] - piece2[:, 0]))
    elif edge == 'bottom':
        return np.sum(np.abs(piece1[-1, :] - piece2[0, :]))
    else:
        raise ValueError("Invalid edge")

def calculate_energy(pieces, grid_size):
    energy = 0
    for i in range(grid_size):
        for j in range(grid_size):
            if j < grid_size - 1:
                energy += edge_difference(pieces[i*grid_size + j], 
                                          pieces[i*grid_size + j + 1], 'right')
            if i < grid_size - 1:
                energy += edge_difference(pieces[i*grid_size + j], 
                                          pieces[(i+1)*grid_size + j], 'bottom')
    return energy

def get_neighbors(index, grid_size):
    row, col = divmod(index, grid_size)
    neighbors = []
    if row > 0:
        neighbors.append(index - grid_size)  # Top neighbor
    if row < grid_size - 1:
        neighbors.append(index + grid_size)  # Bottom neighbor
    if col > 0:
        neighbors.append(index - 1)  # Left neighbor
    if col < grid_size - 1:
        neighbors.append(index + 1)  # Right neighbor
    return neighbors

def simulated_annealing(pieces, grid_size, initial_temp, cooling_rate, iterations):
    current_solution = pieces.copy()
    current_energy = calculate_energy(current_solution, grid_size)
    best_solution = current_solution.copy()
    best_energy = current_energy
    temp = initial_temp

    for iter in range(iterations):
        # Choose a random piece and one of its neighbors
        i = random.randint(0, len(pieces) - 1)
        neighbors = get_neighbors(i, grid_size)
        j = random.choice(neighbors) if neighbors else random.randint(0, len(pieces) - 1)

        new_solution = current_solution.copy()
        new_solution[i], new_solution[j] = new_solution[j], new_solution[i]
        new_energy = calculate_energy(new_solution, grid_size)
        
        if new_energy < current_energy or random.random() < math.exp((current_energy - new_energy) / temp):
            current_solution = new_solution
            current_energy = new_energy
            
            if current_energy < best_energy:
                best_solution = current_solution.copy()
                best_energy = current_energy
        
        # Cooling schedule
        temp = initial_temp / (1 + cooling_rate * iter)

        # Reheating mechanism
        if iter % 1000 == 0 and iter > 0:
            temp = min(initial_temp, temp * 2)

    return best_solution, best_energy

def main():
    # Parameters
    file_path = 'reconstructed_lena.mat'
    piece_size = 64  # Adjust based on your puzzle
    grid_size = 8  # 512 / 64 = 8
    initial_temp = 1000  # Increased initial temperature
    cooling_rate = 0.0001  # Slower cooling rate
    iterations = 1000000  # Increased number of iterations

    # Load and process image
    image = load_image(file_path)
    pieces = split_image(image, piece_size)
    random.shuffle(pieces)

    # Solve puzzle
    solved_pieces, final_energy = simulated_annealing(pieces, grid_size, initial_temp, cooling_rate, iterations)

    # Reconstruct and display images
    original_image = reconstruct_image(pieces, grid_size)
    solved_image = reconstruct_image(solved_pieces, grid_size)

    plt.figure(figsize=(12, 6))
    plt.subplot(121)
    plt.imshow(original_image, cmap='gray')
    plt.title('Scrambled Image')
    plt.axis('off')

    plt.subplot(122)
    plt.imshow(solved_image, cmap='gray')
    plt.title(f'Solved Image (Energy: {final_energy})')
    plt.axis('off')

    plt.tight_layout()
    plt.show()

if __name__ == "__main__":
    main()