import os
import subprocess
import csv
import time
import sys
from pathlib import Path

# Add parent directory to Python path to import from helpers
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

# Import custom sorting function from helpers (now in root directory)
from helpers.sort_files import sort_files_by_v_c
from helpers.parameter_count import count_parameters_smt

SMT_FOLDER = ROOT_DIR / "smt"
RESULT_DIR = ROOT_DIR / "results"
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


def run_solver_on_smt_files(solver):
    CSV_FILE = RESULT_DIR / ("smt_result_" + solver + ".csv")
    
    results = []

    smt_files = sort_files_by_v_c([f for f in os.listdir(SMT_FOLDER) if f.endswith(".smt2")])

    for smt_file in smt_files:
        smt_path = SMT_FOLDER / smt_file
        param_count = count_parameters_smt(smt_path) 

        if solver == "z3":
            cmd = [solver, "-smt2", str(smt_path), "-memory:32768", f"-T:{TIMEOUT}"]
        elif solver == "cvc5":
            cmd = [solver, f"--tlimit-per={TIMEOUT*1000}", "--rlimit-per=100000000", "--stats", "--verbosity=2", str(smt_path)]
            # cmd = [solver, f"--tlimit-per={TIMEOUT*1000}", "--produce-models", "--fp-exp", "--fp-lazy-wb", "--stats", "--verbosity=2", str(smt_path)]
        elif solver == "bitwuzla":
            cmd = [solver, str(smt_path)]
            # cmd = [solver, f"--time-limit={TIMEOUT * 1000}", "--sat-solver=cadical", "--nthreads=4", "--memory-limit=8192", str(smt_path)]
            # cmd = [solver, f"--time-limit={TIMEOUT * 1000}", "--produce-models", "--sat-solver=cadical", "--nthreads=4", "--memory-limit=8192", str(smt_path)]

        # cmd = [solver, str(smt_path)]

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
    RESULT_DIR.mkdir(exist_ok=True)
    if len(sys.argv) < 2:
        print("Usage: python run_smt.py <solver_name>")
        print("Example: python run_smt.py bitwuzla")
        sys.exit(1)
    
    solver = sys.argv[1]
    run_solver_on_smt_files(solver)
