import numpy as np
import random
import math

class JigsawPiece:
    def __init__(self, top, right, bottom, left):
        self.edges = [top, right, bottom, left]  

class JigsawPuzzle:
    def __init__(self, pieces, grid_size):
        self.pieces = pieces  
        self.grid_size = grid_size  

    def initial_state(self):
        return np.random.permutation(self.pieces).reshape(self.grid_size, self.grid_size)

    def energy(self, state):
        mismatch_count = 0
        for i in range(self.grid_size):
            for j in range(self.grid_size):
                piece = state[i][j]
                if j < self.grid_size - 1:
                    right_neighbor = state[i][j + 1]
                    if piece.edges[1] != right_neighbor.edges[3]:  
                        mismatch_count += 1
               
                if i < self.grid_size - 1:
                    bottom_neighbor = state[i + 1][j]
                    if piece.edges[2] != bottom_neighbor.edges[0]:  
                        mismatch_count += 1
        return mismatch_count

    def random_neighbor(self, state):
       
        new_state = state.copy()
        i1, j1, i2, j2 = random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1), \
                         random.randint(0, self.grid_size - 1), random.randint(0, self.grid_size - 1)
        new_state[i1][j1], new_state[i2][j2] = new_state[i2][j2], new_state[i1][j1]
        return new_state

    def simulated_annealing(self, initial_temp, cooling_rate):
        current_state = self.initial_state()
        current_energy = self.energy(current_state)
        temperature = initial_temp

        while temperature > 1:
            new_state = self.random_neighbor(current_state)
            new_energy = self.energy(new_state)

            
            if new_energy < current_energy:
                current_state, current_energy = new_state, new_energy
            else:
                acceptance_prob = math.exp((current_energy - new_energy) / temperature)
                if random.uniform(0, 1) < acceptance_prob:
                    current_state, current_energy = new_state, new_energy

            
            temperature *= cooling_rate

        return current_state, current_energy


pieces = [
    JigsawPiece(0, 1, 2, 3),
    JigsawPiece(2, 3, 0, 1),
    JigsawPiece(1, 2, 3, 0),
    JigsawPiece(3, 0, 1, 2),
    JigsawPiece(0, 2, 1, 3),
    JigsawPiece(2, 1, 3, 0),
    JigsawPiece(3, 0, 2, 1),
    JigsawPiece(1, 3, 0, 2),
    JigsawPiece(2, 1, 3, 0)
]  

grid_size = 3  
puzzle = JigsawPuzzle(pieces, grid_size)

print("Solving Jigsaw Puzzle using Simulated Annealing...")
solved_state, final_energy = puzzle.simulated_annealing(initial_temp=1000, cooling_rate=0.995)

print("Final energy (number of mismatches):", final_energy)
