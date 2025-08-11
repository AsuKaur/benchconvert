import os
import subprocess
import csv
import time
import re
import sys

SMT_FOLDER = "smt"
TIMEOUT = 900

def get_solver_version(solver):
    try:
        result = subprocess.run([solver, "--version"], capture_output=True, text=True)
        return result.stdout.strip() or result.stderr.strip()
    except Exception as e:
        return f"Could not retrieve version: {e}"

def parse_solver_output(output):
    for line in output.strip().splitlines():
        line = line.strip().lower()
        if line in ["sat", "unsat", "unknown"]:
            return line.upper()
    return "UNKNOWN"

def get_expected_result(filename):
    if "unsat" in filename.lower():
        return "UNSAT"
    elif "sat" in filename.lower():
        return "SAT"
    return "UNKNOWN"

def count_parameters_in_smt(smt_file_path):
    with open(smt_file_path, 'r') as file:
        content = file.read()

    # Count input features (X_i)
    input_matches = re.findall(r'\(declare-fun X_(\d+) ', content)
    num_inputs = len(set(input_matches)) 

    # Count hidden units (from H_0_j declarations)
    hidden_matches = re.findall(r'\(declare-fun H_0_(\d+) ', content)
    num_hidden = len(set(hidden_matches))

    # Count output units (from Y_k declarations)
    output_matches = re.findall(r'\(declare-fun Y_(\d+) ', content)
    num_outputs = len(set(output_matches))

    # Calculate parameters
    # Input to hidden: weights + biases
    input_to_hidden = (num_inputs * num_hidden) + num_hidden
    # Hidden to output: weights + biases
    hidden_to_output = (num_hidden * num_outputs) + num_outputs
    total_parameters = input_to_hidden + hidden_to_output

    return total_parameters

def run_solver_on_smt_files(solver):
    CSV_FILE = "results/smt_result_" + solver + ".csv"
    
    results = []

    smt_files = sorted([f for f in os.listdir(SMT_FOLDER) if f.endswith(".smt2")])

    for smt_file in smt_files:
        smt_path = os.path.join(SMT_FOLDER, smt_file)
        param_count = count_parameters_in_smt(smt_path) 

        cmd = [solver, smt_path]

        print(f"Running {solver} on: {smt_file}")
        try:
            start = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
            end = time.time()

            output = result.stdout + result.stderr
            actual_result = parse_solver_output(output)
            runtime = round(end - start, 4)
            expected = get_expected_result(smt_file)

            results.append([
                smt_file,
                param_count,        
                expected,
                actual_result,
                f"{runtime}s",
                " ".join(cmd)
            ])

        except subprocess.TimeoutExpired:
            print(f"Timeout: {smt_file}")
            results.append([
                smt_file,
                param_count,
                get_expected_result(smt_file),
                "TIMEOUT",
                f"{TIMEOUT}s",
                " ".join(cmd)
            ])
        except Exception as e:
            print(f"Error running {smt_file}: {e}")
            results.append([
                smt_file,
                param_count,
                get_expected_result(smt_file),
                f"ERROR: {e}",
                "N/A",
                " ".join(cmd)
            ])

    solver_version = get_solver_version(solver)
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Solver: {solver}"])
        writer.writerow([f"Version: {solver_version}"])
        writer.writerow(["File Name", 
                         "Parameter Count", 
                         "Expected Result", 
                         "Actual Result", 
                         "Runtime", 
                         "Command"])
        writer.writerows(results)

    print(f"\nSaved to {CSV_FILE}")

if __name__ == "__main__":
    if len(sys.argv) < 2:
        print("Usage: python script.py <solver_name>")
        print("Example: python script.py bitwuzla")
        sys.exit(1)
    
    solver = sys.argv[1]
    run_solver_on_smt_files(solver)
