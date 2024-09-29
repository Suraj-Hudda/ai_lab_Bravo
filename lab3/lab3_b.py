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
        satisfied_clauses = [clause for clause in k_sat if any((literal > 0) == solution[abs(literal)] for literal in clause)]
        
        if len(satisfied_clauses) == len(k_sat):
            return solution  
        
        
        for var in solution.keys():
            new_solution = solution.copy()
            new_solution[var] = not new_solution[var]
            if any(len([clause for clause in k_sat if any((literal > 0) == new_solution[abs(literal)] for literal in clause)]) == len(k_sat)):
                return new_solution  
    return None  

if __name__ == "__main__":
    k = 3  
    m = 5  
    n = 4  

    k_sat_problem = generate_k_sat(k, m, n)
    print("Generated k-SAT Problem:", k_sat_problem)

    print("\n--- Hill Climbing ---")
    start_time = time.time()
    hill_climbing_solution = hill_climbing(k_sat_problem)
    print("Solution found by Hill Climbing:" if hill_climbing_solution else "No solution found.")
    print("Time taken: {:.6f} seconds".format(time.time() - start_time))

    print("\n--- Beam Search ---")
    start_time = time.time()
    beam_search_solution = beam_search(k_sat_problem)
    print("Solution found by Beam Search:" if beam_search_solution else "No solution found.")
    print("Time taken: {:.6f} seconds".format(time.time() - start_time))

    print("\n--- Variable Neighborhood Descent ---")
    start_time = time.time()
    vnd_solution = variable_neighborhood_descent(k_sat_problem)
    print("Solution found by Variable Neighborhood Descent:" if vnd_solution else "No solution found.")
    print("Time taken: {:.6f} seconds".format(time.time() - start_time))
