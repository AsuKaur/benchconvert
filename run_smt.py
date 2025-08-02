import os
import subprocess
import csv
import time
import re


SOLVER = "bitwuzla"  # "z3" or "cvc5" or "algaroba"
SMT_FOLDER = "smt"
CSV_FILE = "smt_result_" + SOLVER + ".csv"
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


def count_parameters_in_smt(path):
    with open(path, 'r') as file:
        content = file.read()

    # Count weights: fp.mul with a neuron or input as second argument
    weight_matches = re.findall(
        r'\(fp\.mul\s+roundNearestTiesToEven\s+\([^)]+\)\s+(X_\d+|H_\d+_\d+)\)',
        content
    )
    weight_count = len(weight_matches)

    # Counting wrong bias
    bias_exprs = re.findall(
    r'\(assert\s+\(=\s+(H_\d+_\d+)\s+(\(let\s+\(\([^)]+\)\)\s+)?(.+?)\)\)', 
    content, 
    re.DOTALL)

    bias_count = len(set(bias_exprs))

    print(f"Weights: {weight_count}, Biases: {bias_count}")
    return weight_count + bias_count

def run_solver_on_smt_files():
    results = []

    smt_files = sorted([f for f in os.listdir(SMT_FOLDER) if f.endswith(".smt2")])
    # smt_files=["sat_v2_c1.smt2"]


    for smt_file in smt_files:
        smt_path = os.path.join(SMT_FOLDER, smt_file)
        param_count = count_parameters_in_smt(smt_path)  # Count parameters

        cmd = [SOLVER, smt_path]

        print(f"🔍 Running {SOLVER} on: {smt_file}")
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
            print(f"⏳ Timeout: {smt_file}")
            results.append([
                smt_file,
                param_count,
                get_expected_result(smt_file),
                "TIMEOUT",
                f"{TIMEOUT}s",
                " ".join(cmd)
            ])
        except Exception as e:
            print(f"❌ Error running {smt_file}: {e}")
            results.append([
                smt_file,
                param_count,
                get_expected_result(smt_file),
                f"ERROR: {e}",
                "N/A",
                " ".join(cmd)
            ])

    solver_version = get_solver_version(SOLVER)
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Solver: {SOLVER}"])
        writer.writerow([f"Version: {solver_version}"])
        writer.writerow(["File Name", 
                         "Parameter Count", 
                         "Expected Result", 
                         "Actual Result", 
                         "Runtime", 
                         "Command"])
        writer.writerows(results)

    print(f"\n✅ Results saved to {CSV_FILE}")

if __name__ == "__main__":
    run_solver_on_smt_files()
