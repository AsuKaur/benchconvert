# The file is taken from https://github.com/emanino/neurocodebench
# The file is unchanged from the original repository, just detailed comments have been added
# for understanding the code and its functionality.

# This script generates CNF formulas in DIMACS format for SAT and UNSAT problems.

import csv
import random
import numpy as np

def print_dimacs(filepath, info, cnf, verdict="Unsat"):
    # Write a CNF formula to a file in DIMACS format.
    
    # DIMACS is the standard format for representing boolean satisfiability problems.
    # Format specification:
    # - Comment lines start with 'c'
    # - Problem line: 'p cnf <num_vars> <num_clauses>'
    # - Each clause is a line of space-separated literals ending with '0'
    # - Positive integers represent variables, negative integers represent negated variables
    
    # Args:
    #     filepath (str): Output file path
    #     info (dict): Dictionary containing 'vars' and 'clauses' counts
    #     cnf (list): List of clauses, where each clause is a list of literals
    #     verdict (str): Expected satisfiability verdict ("Sat" or "Unsat")
    
    with open(filepath, "w", newline='') as csvfile:
        # Using csv.writer with space delimiter to properly format DIMACS output
        csvwriter = csv.writer(csvfile, delimiter=' ')
        
        # Write comment line with metadata about the formula
        csvwriter.writerow(["c", "NeuroCodeBench", "2.0", "CNF", "formula", "with", "verdict", verdict])
        
        # Write problem specification line: p cnf <variables> <clauses>
        csvwriter.writerow(["p", "cnf", str(info["vars"]), str(info["clauses"])])
        
        # Write each clause as a row of literals terminated by '0'
        for clause in cnf:
            clause_list = [str(lit) for lit in clause] + ["0"]
            csvwriter.writerow(clause_list)

def generate_sat(n_var, n_clause, max_fail = 100):
    # Generate a satisfiable (SAT) CNF formula using a constructive approach.
    
    # Strategy: Start with a random truth assignment, then generate clauses that
    # are satisfied by this assignment. This guarantees the formula is satisfiable.
    
    # Args:
    #     n_var (int): Number of boolean variables (1 to n_var)
    #     n_clause (int): Target number of clauses to generate
    #     max_fail (int): Maximum consecutive failures before giving up
    
    # Returns:
    #     tuple: (info_dict, cnf_list) where info_dict contains metadata
    #            and cnf_list contains the clauses
    
    cnf = []  # List to store generated clauses
    n_fail = 0  # Counter for consecutive generation failures
    
    # Generate a random truth assignment for all variables
    truth = np.random.rand(n_var) < 0.5  # True/False for each variable
    while len(cnf) < n_clause and n_fail < max_fail:
        # Randomly select a subset of variables for this clause
        v = np.random.choice(n_var, size=np.random.randint(0, n_var), replace=False)
        
        # Randomly choose polarity (positive/negative) for each selected variable
        t = np.random.rand(len(v)) < 0.5  # True = positive literal, False = negative
        
        # Check if this clause would be satisfied by our truth assignment
        # A clause is satisfied if at least one literal matches the truth assignment
        if (truth[v] == t).any():
            # Convert to DIMACS format (1-based indexing)
            # Positive literals: variable indices + 1
            pos_v = v[t] + 1
            # Negative literals: -(variable indices + 1)
            neg_v = -v[np.logical_not(t)] - 1
            
            # Combine positive and negative literals into a single clause
            cnf.append(list(np.concatenate([pos_v, neg_v])))
            n_fail = 0  # Reset failure counter on success
        else:
            # This clause would not be satisfied by our truth assignment
            # Increment failure counter and try again
            n_fail = n_fail + 1
            
    # Remove duplicate clauses by converting to set of tuples and back
    # This is important because duplicate clauses don't add logical content
    cnf = list(set(tuple(clause) for clause in cnf))
    
    # Metadata about the generated formula
    info = {"vars": n_var, "clauses": len(cnf)}
    
    return info, cnf

def generate_unsat(n_var, n_clause, max_fail = 100):
    # Generate an unsatisfiable (UNSAT) CNF formula using resolution-based expansion.
    
    # Strategy: Start with a simple contradiction (x1 ∧ ¬x1), then expand it by
    # adding new variables through resolution. This maintains unsatisfiability.
    
    # The expansion works by taking a clause C and creating two new clauses:
    # C ∨ x_new and C ∨ ¬x_new, where x_new is a fresh variable.
    # This preserves unsatisfiability because any satisfying assignment must
    # satisfy both clauses, but x_new can't be both true and false.
    
    # Args:
    #     n_var (int): Number of boolean variables (1 to n_var)
    #     n_clause (int): Target number of clauses to generate
    #     max_fail (int): Maximum consecutive failures before giving up
    
    # Returns:
    #     tuple: (info_dict, cnf_list) where info_dict contains metadata
    #            and cnf_list contains the clauses
    
    cnf = []  # List to store generated clauses
    n_fail = 0  # Counter for consecutive generation failures
    
    # Ensure we have enough variables and clauses for the basic contradiction
    assert(n_var >= 1 and n_clause >= 2)
    
    # Start with a simple contradiction: x1 ∧ ¬x1
    # This is unsatisfiable since x1 cannot be both true and false
    cnf.append([+1])  # x1
    cnf.append([-1])  # ¬x1
    
    while len(cnf) < n_clause and n_fail < max_fail:
        # Select an existing clause to expand, with bias toward shorter clauses
        freq = 1 / np.array([len(clause) for clause in cnf])
        i = int(np.random.choice(len(cnf), size=1, p=freq / np.sum(freq))[0])
        clause = cnf[i]
        
        # Find variables not already in the selected clause
        in_set = {abs(v) for v in clause}  # Variables already in the clause
        out_set = [j + 1 for j in range(n_var) if j + 1 not in in_set]
        
        # Expand the clause by adding a new variable in both polarities
        if len(out_set) > 0:
            new_var = random.choice(out_set)
            # Replace the original clause with C ∨ x_new
            cnf[i] = clause + [new_var]
            # Add a new clause C ∨ ¬x_new
            cnf.append(clause + [-new_var])
            n_fail = 0  # Reset failure counter on success
        else:
            # No available variables to add to this clause
            # Increment failure counter and try a different clause
            n_fail = n_fail + 1
    
    # Remove duplicate clauses to clean up the formula
    # Duplicates can occur due to the random selection process
    cnf = list(set(tuple(clause) for clause in cnf))
    
    # Metadata about the generated formula
    info = {"vars": n_var, "clauses": len(cnf)}
    
    return info, cnf
