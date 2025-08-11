import os
import subprocess
import csv
import time
import onnx
import sys
from pathlib import Path


RESULT_DIR = Path("results")
ONNX_DIR = "onnx"
VNNLIB_DIR = "vnnlib"
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


def count_parameters(onnx_path):
    try:
        model = onnx.load(onnx_path)
        param_count = 0
        for tensor in model.graph.initializer:
            dims = tensor.dims
            count = 1
            for d in dims:
                count *= d
            param_count += count
        return param_count
    except Exception as e:
        print(f"Failed to count parameters for {onnx_path}: {e}")
        return "N/A"


def run_vnn_verifier(verifier):
    results = []
    csv_file = RESULT_DIR / f"vnn_result_{verifier.lower()}.csv"
    onnx_files = sorted([f for f in os.listdir(ONNX_DIR) if f.endswith(".onnx")])

    for onnx_file in onnx_files:
        base = os.path.splitext(onnx_file)[0]
        vnnlib_file = base + ".vnnlib"

        onnx_path = os.path.join(ONNX_DIR, onnx_file)
        vnnlib_path = os.path.join(VNNLIB_DIR, vnnlib_file)

        if not os.path.exists(vnnlib_path):
            print(f"Skipping {onnx_file}, matching VNNLIB file not found.")
            continue

        param_count = count_parameters(onnx_path)

        cmd = [verifier, onnx_path, vnnlib_path]

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
        print("Usage: python run_vnn.py <verifier_name>")
        print("Example: python run_vnn.py marabou")
        sys.exit(1)
    
    verifier = sys.argv[1]
    run_vnn_verifier(verifier)
