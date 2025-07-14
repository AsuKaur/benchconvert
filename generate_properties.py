# The file is taken from https://github.com/emanino/neurocodebench
import os
import sys
import csv
import random
import numpy as np

from generate_dimacs import print_dimacs, generate_sat, generate_unsat
from dimacs_to_onnx import cnf_to_nn_params, nn_params_to_torch
from dimacs_to_onnx import write_torch_to_onnx_file
from generate_vnnlib import vnnlib_lines

def remake_dir(path):
    if os.path.exists(path):
        for f in os.listdir(path):
            os.remove(os.path.join(path, f))
        os.rmdir(path)
    os.makedirs(path)

N_BENCH_PAIRS = 5 # number of SAT/UNSAT instance pairs
N_VAR_MIN = 2 # minimum number of network input variables
N_VAR_MAX = 10 # maximum number of network input variables
X_CLAUSE_MIN = 1 # CNF clauses: minimum variable multiplier
X_CLAUSE_MAX = 5 # CNF clauses: maximum variable multiplier
VNN_COMP_TIMEOUT = 100

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python generate_properties.py <RANDOM_SEED>")
        sys.exit(1)
    
    remake_dir("dimacs")
    remake_dir("onnx")
    remake_dir("vnnlib")
    
    instance_data = []
    
    # set the seed for reproducibility reasons
    # numpy random functions are used during CNF generation
    seed_val = int(sys.argv[1])
    random.seed(seed_val)
    np.random.seed(seed=seed_val)
    
    # the benchmark generation has the following workflow:
    # - a pair of CNF formulae (SAT, UNSAT) in Dimacs format
    # - convert them into the equivalent ONNX neural networks
    # - write the corresponding VNN-LIB properties
    for i in range(N_BENCH_PAIRS):
    
        # select a random number of variables and clauses in the specified ranges
        # the clause range is a multiplier since we want n_clause >= n_var
        n_var = random.randint(N_VAR_MIN, N_VAR_MAX)
        n_clause = random.randint(n_var * X_CLAUSE_MIN, n_var * X_CLAUSE_MAX)
        
        # always generate a pair of SAT and UNSAT formulae
        sat_formula = generate_sat(n_var, n_clause)
        unsat_formula = generate_unsat(n_var, n_clause)
        
        # read the actual number of clauses generated in the previous step
        # as it might be less than n_clauses due to duplicate removal
        n_sat_clauses = sat_formula[0]["clauses"]
        n_unsat_clauses = unsat_formula[0]["clauses"]
        
        # shared file names (Dimacs, ONNX, VNN-LIB)
        sat_name = "sat_v" + str(n_var) + "_c" + str(n_sat_clauses)
        unsat_name = "unsat_v" + str(n_var) + "_c" + str(n_unsat_clauses)
        
        # save them in Dimacs format for reference
        print_dimacs("./dimacs/" + sat_name + ".dimacs",
                     *sat_formula, verdict="Sat")
        print_dimacs("./dimacs/" + unsat_name + ".dimacs",
                     *unsat_formula, verdict="Unsat")
        
        # convert CNF formulae to neural networks
        sat_net = nn_params_to_torch(*cnf_to_nn_params(*sat_formula))
        unsat_net = nn_params_to_torch(*cnf_to_nn_params(*unsat_formula))
        
        # save networks in ONNX format
        write_torch_to_onnx_file(sat_net, "./onnx/" + sat_name + ".onnx")
        write_torch_to_onnx_file(unsat_net, "./onnx/" + unsat_name + ".onnx")
        
        # prepare two identical VNN-LIB properties apart from their verdict
        sat_vnnlib = vnnlib_lines(n_var, "SAT")
        unsat_vnnlib = vnnlib_lines(n_var, "UNSAT")
        
        # save the VNN-LIB files
        with open("./vnnlib/" + sat_name + ".vnnlib", "w") as f:
            f.writelines(line + "\n" for line in sat_vnnlib)
        with open("./vnnlib/" + unsat_name + ".vnnlib", "w") as f:
            f.writelines(line + "\n" for line in unsat_vnnlib)
        
        # keep track of all instances generated so far
        sat_instance = ["onnx/" + sat_name + ".onnx",
                        "vnnlib/" + sat_name + ".vnnlib",
                        VNN_COMP_TIMEOUT]
        unsat_instance = ["onnx/" + unsat_name + ".onnx",
                          "vnnlib/" + unsat_name + ".vnnlib",
                          VNN_COMP_TIMEOUT]
        instance_data.append(sat_instance)
        instance_data.append(unsat_instance)
    
    # save the ONNX/VNN-LIB instance pairs in the required CSV file
    with open('instances.csv', 'w', encoding='UTF8', newline='') as f:
        writer = csv.writer(f)
        writer.writerows(instance_data)
