import numpy as np
import matplotlib.pyplot as plt
import h5py
from scipy.io import loadmat

def load_mat_file(file_path):
    try:
        # Attempt to load as a standard .mat file
        data = loadmat(file_path)
        print("Loaded .mat file using scipy.")
    except ValueError:
        # If that fails, attempt to load as an HDF5 file
        print("Standard loadmat failed. Attempting to load as HDF5...")
        with h5py.File(file_path, 'r') as f:
            # Assuming the image data is stored under a specific key; adjust as needed
            data = {key: np.array(f[key]) for key in f.keys()}
            print("Loaded .mat file using h5py.")
    return data

def display_image(image, title):
    plt.imshow(image, cmap='gray')
    plt.title(title)
    plt.axis('off')
    plt.show()

# Load the scrambled image
file_path = 'scrambled_lena.mat'  # Update with the correct path to your .mat file
data = load_mat_file(file_path)

# Print the keys in the data to understand its structure
print("Keys in the loaded data:", list(data.keys()))

# Check for common keys in MATLAB files
# Adjust this key based on your file's structure
image_key = 'image' if 'image' in data else list(data.keys())[0]  # Change this if needed
scrambled_image = data[image_key]

# Display the scrambled image
display_image(scrambled_image, "Scrambled Image")

# Simulated Annealing Parameters
initial_temp = 1000
final_temp = 1
alpha = 0.95
max_iterations = 1000

def objective_function(arrangement):
    """ Calculate the dissimilarity of the arrangement of image patches. """
    reshaped_image = arrangement.reshape(scrambled_image.shape)
    return np.sum((reshaped_image - scrambled_image) ** 2)  # Dissimilarity measure

def simulated_annealing(initial_arrangement):
    """ Simulated annealing algorithm to find the optimal arrangement of the image. """
    current_solution = initial_arrangement
    current_cost = objective_function(current_solution)

    temperature = initial_temp
    while temperature > final_temp:
        for _ in range(max_iterations):
            new_solution = current_solution.copy()
            i, j = np.random.choice(len(new_solution), size=2, replace=False)
            new_solution[i], new_solution[j] = new_solution[j], new_solution[i]

            new_cost = objective_function(new_solution)

            if new_cost < current_cost or np.random.rand() < np.exp((current_cost - new_cost) / temperature):
                current_solution = new_solution
                current_cost = new_cost

        temperature *= alpha

    return current_solution

# Initialize the arrangement (flattened)
initial_arrangement = np.random.permutation(scrambled_image.flatten())

# Solve the puzzle using simulated annealing
solved_image = simulated_annealing(initial_arrangement)

# Display the solved image
display_image(solved_image.reshape(scrambled_image.shape), "Solved Image")
