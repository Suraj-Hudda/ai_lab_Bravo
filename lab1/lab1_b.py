from collections import deque

class GameSolver:
    def __init__(self, initial, target):
        self.initial_state = initial
        self.final_state = target

    def is_transition_valid(self, current, next_state):
        current_empty_idx = current.index(0)
        next_empty_idx = next_state.index(0)

        
        if abs(current_empty_idx - next_empty_idx) > 2:
            return False
        if next_empty_idx < 0 or next_empty_idx >= len(current):
            return False
        if (current[next_empty_idx] == -1 and current_empty_idx <= next_empty_idx) or \
           (current[next_empty_idx] == 1 and current_empty_idx >= next_empty_idx):
            return False
        return True

    def get_successors(self, state):
        possible_moves = [-2, -1, 1, 2]
        empty_position = state.index(0)
        successors = []

        for move in possible_moves:
            new_position = empty_position + move
            if 0 <= new_position < len(state):
                new_state = list(state)
                new_state[empty_position], new_state[new_position] = new_state[new_position], new_state[empty_position]
                new_state_tuple = tuple(new_state)
                if self.is_transition_valid(state, new_state_tuple):
                    successors.append(new_state_tuple)
        return successors

    def breadth_first_search(self):
        queue = deque([(self.initial_state, [])])
        visited_states = set()

        while queue:
            current_state, path = queue.popleft()

            if current_state in visited_states:
                continue

            visited_states.add(current_state)
            successors = self.get_successors(current_state)

            for successor in successors:
                if successor == self.final_state:
                    return path + [current_state, successor]
                queue.append((successor, path + [current_state]))

        return None

def main():
    start_state = (-1, -1, -1, 0, 1, 1, 1)
    goal_state = (1, 1, 1, 0, -1, -1, -1)

    solver = GameSolver(start_state, goal_state)
    solution_path = solver.breadth_first_search()

    if solution_path:
        for state in solution_path:
            print(state)
    else:
        print("No solution found")

if __name__ == "__main__":
    main()
