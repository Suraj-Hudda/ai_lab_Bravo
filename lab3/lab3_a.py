import random
import time

def generate_k_sat(k, m, n):
    """
    Generate a random k-SAT problem.
    
    Parameters:
    k (int): Number of literals per clause.
    m (int): Number of clauses.
    n (int): Number of variables.
    
    Returns:
    list: A list of clauses representing the k-SAT problem.
    """
    clauses = []
    for _ in range(m):
        clause = set()
        while len(clause) < k:
            var = random.randint(1, n)  
            negated = random.choice([True, False])
            literal = -var if negated else var
            clause.add(literal)
        clauses.append(clause)
    return clauses

def hill_climbing(k_sat, max_iterations=1000):
    """
    Hill-Climbing algorithm to solve the k-SAT problem.
    
    Parameters:
    k_sat (list): The k-SAT problem as a list of clauses.
    max_iterations (int): Maximum number of iterations to run.
    
    Returns:
    dict: A solution if found, else None.
    """
    n = max(abs(literal) for clause in k_sat for literal in clause)  
    solution = {var: random.choice([True, False]) for var in range(1, n + 1)}

    for _ in range(max_iterations):
        satisfied_clauses = [clause for clause in k_sat if any((literal > 0) == solution[abs(literal)] for literal in clause)]
        
        if len(satisfied_clauses) == len(k_sat):
            return solution  
        
        var_to_flip = random.choice(list(solution.keys()))
        solution[var_to_flip] = not solution[var_to_flip]

    return None  

def beam_search(k_sat, beam_width=3, max_iterations=1000):
    """
    Beam Search algorithm to solve the k-SAT problem.
    
    Parameters:
    k_sat (list): The k-SAT problem as a list of clauses.
    beam_width (int): The width of the beam.
    max_iterations (int): Maximum number of iterations to run.
    
    Returns:
    dict: A solution if found, else None.
    """
    n = max(abs(literal) for clause in k_sat for literal in clause)
    current_solutions = [{var: random.choice([True, False]) for var in range(1, n + 1)}]

    for _ in range(max_iterations):
        next_solutions = []
        
        for solution in current_solutions:
            for var in solution.keys():
               
                new_solution = solution.copy()
                new_solution[var] = not new_solution[var]
                next_solutions.append(new_solution)

        
        next_solutions = sorted(next_solutions, key=lambda sol: sum(1 for clause in k_sat if any((literal > 0) == sol[abs(literal)] for literal in clause)), reverse=True)

        
        current_solutions = next_solutions[:beam_width]

        if any(len([clause for clause in k_sat if any((literal > 0) == sol[abs(literal)] for literal in clause)]) == len(k_sat) for sol in current_solutions):
            return current_solutions[0]  

    return None  

def variable_neighborhood_descent(k_sat, max_iterations=1000):
    """
    Variable Neighborhood Descent algorithm to solve the k-SAT problem.
    
    Parameters:
    k_sat (list): The k-SAT problem as a list of clauses.
    max_iterations (int): Maximum number of iterations to run.
    
    Returns:
    dict: A solution if found, else None.
    """
    n = max(abs(literal) for clause in k_sat for literal in clause)
    solution = {var: random.choice([True, False]) for var in range(1, n + 1)}

    for _ in range(max_iterations):
       
        satisfied_count = sum(1 for clause in k_sat if any((literal > 0) == solution[abs(literal)] for literal in clause))
        
        
        for var in solution.keys():
            new_solution = solution.copy()
            new_solution[var] = not new_solution[var]
            new_satisfied_count = sum(1 for clause in k_sat if any((literal > 0) == new_solution[abs(literal)] for literal in clause))
            
            if new_satisfied_count > satisfied_count:
                solution = new_solution
                satisfied_count = new_satisfied_count

        if satisfied_count == len(k_sat):
            return solution  

    return None  

def heuristic_satisfied_clauses(solution, k_sat):
    """
    Count the number of satisfied clauses for the given solution.
    
    Parameters:
    solution (dict): Current variable assignments.
    k_sat (list): The k-SAT problem as a list of clauses.
    
    Returns:
    int: Number of satisfied clauses.
    """
    return sum(1 for clause in k_sat if any((literal > 0) == solution[abs(literal)] for literal in clause))

def heuristic_unsatisfied_clauses(solution, k_sat):
    """
    Count the number of unsatisfied clauses for the given solution.
    
    Parameters:
    solution (dict): Current variable assignments.
    k_sat (list): The k-SAT problem as a list of clauses.
    
    Returns:
    int: Number of unsatisfied clauses.
    """
    return sum(1 for clause in k_sat if not any((literal > 0) == solution[abs(literal)] for literal in clause))

def test_algorithms(k, m, n):
    k_sat_problem = generate_k_sat(k, m, n)
    print("Testing k-SAT Problem:", k_sat_problem)

    start_time = time.time()
    hill_climbing_solution = hill_climbing(k_sat_problem)
    hill_climbing_time = time.time() - start_time
    print("Hill-Climbing Solution:", hill_climbing_solution)
    print("Satisfied Clauses (Hill-Climbing):", heuristic_satisfied_clauses(hill_climbing_solution, k_sat_problem) if hill_climbing_solution else None)

    start_time = time.time()
    beam_search_solution = beam_search(k_sat_problem, beam_width=3)
    beam_search_time = time.time() - start_time
    print("Beam Search Solution:", beam_search_solution)
    print("Satisfied Clauses (Beam Search):", heuristic_satisfied_clauses(beam_search_solution, k_sat_problem) if beam_search_solution else None)

    start_time = time.time()
    variable_neighborhood_solution = variable_neighborhood_descent(k_sat_problem)
    variable_neighborhood_time = time.time() - start_time
    print("Variable Neighborhood Descent Solution:", variable_neighborhood_solution)
    print("Satisfied Clauses (Variable Neighborhood Descent):", heuristic_satisfied_clauses(variable_neighborhood_solution, k_sat_problem) if variable_neighborhood_solution else None)

if __name__ == "__main__":
    for k, m, n in [(3, 5, 4), (3, 10, 6), (3, 15, 8)]:
        print(f"\n--- Testing with k={k}, m={m}, n={n} ---")
        test_algorithms(k, m, n)
