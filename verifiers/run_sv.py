import os
import subprocess
import csv
import time
import re
import sys
from pathlib import Path

# Add parent directory to Python path to import from helpers
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

# Import custom sorting function from helpers (now in root directory)
from helpers.sort_files import sort_files_by_v_c
from helpers.parameter_count import count_parameters_c

RESULT_DIR = ROOT_DIR / "results"
PROP_DIR = ROOT_DIR / "c_prop"
NET_DIR = ROOT_DIR / "c_network"
EXTERN_DIR = ROOT_DIR / "extern"
TIMEOUT = 900

def get_verifier_version(verifier):
    try:
        result = subprocess.run([verifier, "--version"], capture_output=True, text=True)
        first_line = result.stdout.strip() or result.stderr.strip()
        return first_line.strip() if first_line else "Version info not found"
    except Exception as e:
        return f"Could not retrieve version: {e}"

def parse_verifier_output(output):
    result = "UNKNOWN"
    solver = "UNKNOWN"
    runtime = "UNKNOWN"
    bug_trace = ""

    for line in output.splitlines():
        line_lower = line.lower()
        if "verification failed" in line_lower:
            result = "VERIFICATION FAILED (SAT)"
        elif "verification successful" in line_lower:
            result = "VERIFICATION SUCCESSFUL (UNSAT)"
        elif "runtime decision procedure" in line_lower:
            parts = line.split(":")
            if len(parts) > 1:
                runtime = parts[1].strip()
        elif "solving with solver" in line_lower:
            parts = line.split("solving with solver")
            if len(parts) > 1:
                solver = parts[1].strip()
        elif "bug found" in line_lower:
            bug_trace = line.strip()

    if result == "VERIFICATION FAILED (SAT)" and bug_trace:
        result += f" ({bug_trace})"
    return result, runtime, solver


def run_verifier(verifier):
    results = []
    output_csv = RESULT_DIR / ("sv_result_" + verifier + ".csv")

    flags = [
    "--float-overflow-check",
    "--nan-check",
    "--bounds-check",
    "--no-pointer-check",
    "--signed-overflow-check",
    "--no-div-by-zero-check",
    # "--unwind 200",
    "--round-to-nearest",
    "--fpa",
    "--trace",
    f"-I{EXTERN_DIR}"
    ] if  verifier == "cbmc" else [
    # f"--timeout {TIMEOUT}s", 
    "--floatbv", 
    "--nan-check", 
    "--overflow-check", 
    "--no-bounds-check",  
    # "--unwind 200",  
    "--no-pointer-check", 
    "--no-div-by-zero-check", 
    "--k-induction",
    "--no-slice",
    f"-I{EXTERN_DIR}"
    ]
    for prop_file in sort_files_by_v_c(os.listdir(PROP_DIR)):
        if not prop_file.endswith(".c"):
            continue

        base_name = prop_file.replace("prop_", "")
        net_file = base_name

        prop_path = PROP_DIR / prop_file
        net_path = NET_DIR / net_file

        if not net_path.exists():
            print(f"Skipping {prop_file}, network file not found.")
            continue

        param_count = count_parameters_c(net_path)

        cmd = [verifier, str(prop_path), "--include", str(net_path)] + flags
        print(f"Command: {' '.join(cmd)}")
        print(f"Running {verifier} on: {prop_file} + {net_file}")

        try:
            start_time = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
            elapsed_time = time.time() - start_time
            output = result.stdout + result.stderr
            print("Output:\n", output)
            actual_result, runtime, solver = parse_verifier_output(output)

            expected_result = "UNSAT" if "unsat" in prop_file.lower() else "SAT"

            results.append([
                prop_file,
                param_count,          
                expected_result,
                actual_result,
                f"{elapsed_time:.4f}s",
                solver,
                " ".join(flags)
            ])
        except subprocess.TimeoutExpired:
            print(f"Timeout: {prop_file}")
            results.append([
                prop_file,
                param_count,
                "UNSAT" if "unsat" in prop_file.lower() else "SAT",
                "TIMEOUT",
                f"{TIMEOUT}s",
                "UNKNOWN",
                " ".join(flags)
            ])
        except Exception as e:
            print(f"Error running {prop_file}: {e}")
            results.append([
                prop_file,
                param_count,
                "UNSAT" if "unsat" in prop_file.lower() else "SAT",
                f"ERROR: {e}",
                "ERROR",
                "UNKNOWN",
                " ".join(flags)
            ])

    verifier_version = get_verifier_version(verifier)
    with open(output_csv, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Verifier: {verifier}"])
        writer.writerow([f"Version: {verifier_version}"])
        writer.writerow([
            "File Name",
            "Parameter Count",
            "Expected Result",
            "Actual Result",
            "Runtime",
            "Solver Used",
            "Flags Used"
        ])
        writer.writerows(results)

    print(f"\nSaved to {output_csv}")

if __name__ == "__main__":
    RESULT_DIR.mkdir(exist_ok=True)
    if len(sys.argv) < 2:
        print("Usage: python run_sv.py <verifier_name>")
        print("Example: python run_sv.py cbmc")
        sys.exit(1)
    
    verifier = sys.argv[1]
    run_verifier(verifier)
