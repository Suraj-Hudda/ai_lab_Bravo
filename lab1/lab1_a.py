from collections import deque

class RabbitState:
    def __init__(self, configuration):
        self.configuration = configuration

    def __eq__(self, other):
        return self.configuration == other.configuration

    def __hash__(self):
        return hash(self.configuration)

    def __repr__(self):
        return str(self.configuration)


class RabbitProblemSolver:
    def __init__(self, start_config, end_config):
        self.start_state = RabbitState(start_config)
        self.end_state = RabbitState(end_config)

    def is_valid_move(self, current_state, new_state):
        current_empty_idx = current_state.configuration.index(0)
        new_empty_idx = new_state.configuration.index(0)
        
       
        if abs(current_empty_idx - new_empty_idx) > 2:
            return False
        if new_empty_idx < 0 or new_empty_idx >= len(current_state.configuration):
            return False
        if (current_state.configuration[new_empty_idx] == -1 and current_empty_idx <= new_empty_idx) or \
           (current_state.configuration[new_empty_idx] == 1 and current_empty_idx >= new_empty_idx):
            return False
        return True

    def get_successor_states(self, state):
        possible_moves = [-2, -1, 1, 2]
        successors = []
        empty_index = state.configuration.index(0)
        
        for move in possible_moves:
            new_index = empty_index + move
            if 0 <= new_index < len(state.configuration):
                new_config = list(state.configuration)
                new_config[empty_index], new_config[new_index] = new_config[new_index], new_config[empty_index]
                new_state = RabbitState(tuple(new_config))
                if self.is_valid_move(state, new_state):
                    successors.append(new_state)
        return successors

    def breadth_first_search(self):
        queue = deque([(self.start_state, [])])
        visited_states = set()
        
        while queue:
            current_state, path = queue.popleft()
            
            if current_state in visited_states:
                continue
            
            visited_states.add(current_state)
            for successor in self.get_successor_states(current_state):
                if successor == self.end_state:
                    return path + [current_state.configuration, successor.configuration]
                queue.append((successor, path + [current_state.configuration]))
        
        return None


def main():
    initial_configuration = (-1, -1, -1, 0, 1, 1, 1)
    goal_configuration = (1, 1, 1, 0, -1, -1, -1)
    
    solver = RabbitProblemSolver(initial_configuration, goal_configuration)
    result_path = solver.breadth_first_search()
    
    if result_path:
        for state in result_path:
            print(state)
    else:
        print("No solution found.")


if __name__ == "__main__":
    main()
