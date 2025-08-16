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
from helpers.parameter_count import count_parameters_onnx


RESULT_DIR = ROOT_DIR / "results"
ONNX_DIR = ROOT_DIR / "onnx"
VNNLIB_DIR = ROOT_DIR / "vnnlib"
TIMEOUT = 900


def get_verifier_version(verifier):
    try:
        result = subprocess.run([verifier, "--version"], capture_output=True, text=True)
        return result.stdout.strip() or result.stderr.strip()
    except Exception:
        return "Version info not available"


def get_expected_result(filename):
    filename = filename.lower()
    if "unsat" in filename:
        return "UNSAT"
    elif "sat" in filename:
        return "SAT"
    return "UNKNOWN"



def run_vnn_verifier(verifier, chunk=None):
    if chunk is None:
        csv_file = RESULT_DIR / f"vnn_result_{verifier.lower()}.csv"
    else:
        csv_file = RESULT_DIR / f"vnn_result_{verifier.lower()}_chunk{chunk}.csv"
    results = []
    all_files = [f for f in os.listdir(ONNX_DIR) if f.endswith(".onnx")]
    sorted_files = sort_files_by_v_c(all_files)
    
    if chunk is None:
        onnx_files = sorted_files
    else:
        start_idx = (chunk - 1) * 10
        end_idx = chunk * 10
        onnx_files = sorted_files[start_idx:end_idx]


    for onnx_file in onnx_files:
        base = os.path.splitext(onnx_file)[0]
        vnnlib_file = base + ".vnnlib"


        onnx_path = ONNX_DIR / onnx_file
        vnnlib_path = VNNLIB_DIR / vnnlib_file


        if not vnnlib_path.exists():
            print(f"Skipping {onnx_file}, matching VNNLIB file not found.")
            continue


        param_count = count_parameters_onnx(onnx_path)


        if verifier == "Marabou":
            cmd = [verifier, str(onnx_path), str(vnnlib_path), f"--timeout={TIMEOUT}", "--num-workers=4", "--snc", "--tightening-strategy=deeppoly", "--branch=relu-violation", "--verbosity=2"]
        else:
            cmd = [verifier, str(onnx_path), str(vnnlib_path)]


        print(f"Running {verifier} on: {onnx_file} + {vnnlib_file}")
        try:
            start = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
            end = time.time()


            output = result.stdout + result.stderr
            decision = "UNKNOWN"
            for line in output.strip().splitlines():
                if "sat" in line.lower():
                    decision = "SAT"
                    break
                elif "unsat" in line.lower():
                    decision = "UNSAT"
                    break


            runtime = round(end - start, 4)
            expected = get_expected_result(base)


            results.append([
                base,
                param_count,         
                expected,
                decision,
                f"{runtime}s",
                " ".join(cmd)
            ])


        except subprocess.TimeoutExpired:
            print(f"Timeout: {onnx_file}")
            results.append([base, param_count, get_expected_result(base), "TIMEOUT",f"{TIMEOUT}s", " ".join(cmd)])
        except Exception as e:
            print(f"Error running {onnx_file}: {e}")
            results.append([base, param_count, get_expected_result(base), f"ERROR: {e}", "N/A", " ".join(cmd)])


    version_info = get_verifier_version(verifier)
    with open(csv_file, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Verifier: {verifier}"])
        writer.writerow([f"Version: {version_info}"])
        writer.writerow(["File Name", "Parameter Count", "Expected Result", "Actual Result", "Runtime", "Command"])
        writer.writerows(results)


    print(f"\nSaved to {csv_file}")


if __name__ == "__main__":
    RESULT_DIR.mkdir(exist_ok=True)
    if len(sys.argv) < 2:
        print("Usage: python run_vnn.py <verifier_name> [chunk_number]")
        print("Example: python run_vnn.py marabou 1")
        print("If chunk_number is provided, it must be an integer from 1 to 10")
        print("If chunk_number is not provided, runs on all files")
        sys.exit(1)
    
    verifier = sys.argv[1]
    chunk = None
    if len(sys.argv) == 3:
        try:
            chunk = int(sys.argv[2])
            if chunk < 1 or chunk > 10:
                raise ValueError
        except ValueError:
            print("chunk_number must be an integer from 1 to 10")
            sys.exit(1)
    
    run_vnn_verifier(verifier, chunk)
