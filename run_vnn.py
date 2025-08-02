import os
import subprocess
import csv
import time
import onnx

VERIFIER = "marabou"
ONNX_DIR = "onnx"
VNNLIB_DIR = "vnnlib"
CSV_FILE = "vnn_result_" + VERIFIER + ".csv"
TIMEOUT = 900

# === Get verifier version ===
def get_verifier_version(verifier):
    try:
        result = subprocess.run([verifier, "--version"], capture_output=True, text=True)
        return result.stdout.strip() or result.stderr.strip()
    except Exception:
        return "Version info not available"

# === Determine expected result from filename ===
def get_expected_result(filename):
    filename = filename.lower()
    if "unsat" in filename:
        return "UNSAT"
    elif "sat" in filename:
        return "SAT"
    return "UNKNOWN"

# Count parameters of ONNX model
def count_parameters(onnx_path):
    try:
        model = onnx.load(onnx_path)
        param_count = 0
        for tensor in model.graph.initializer:
            dims = tensor.dims
            # Multiply dimensions to get total params in this tensor
            count = 1
            for d in dims:
                count *= d
            param_count += count
        return param_count
    except Exception as e:
        print(f"⚠️ Warning: Failed to count parameters for {onnx_path}: {e}")
        return "N/A"

# === Run verifier on each ONNX+VNNLIB pair ===
def run_vnn_verifier():
    results = []

    onnx_files = sorted([f for f in os.listdir(ONNX_DIR) if f.endswith(".onnx")])

    for onnx_file in onnx_files:
        base = os.path.splitext(onnx_file)[0]
        vnnlib_file = base + ".vnnlib"

        onnx_path = os.path.join(ONNX_DIR, onnx_file)
        vnnlib_path = os.path.join(VNNLIB_DIR, vnnlib_file)

        if not os.path.exists(vnnlib_path):
            print(f"⚠️ Skipping {onnx_file} – matching VNNLIB file not found.")
            continue

        # Count parameters for this ONNX model
        param_count = count_parameters(onnx_path)

        cmd = [VERIFIER, onnx_path, vnnlib_path]

        print(f"🔍 Running {VERIFIER} on: {onnx_file} + {vnnlib_file}")
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
                param_count,          # parameter count as second column
                expected,
                decision,
                f"{runtime}s",
                " ".join(cmd)
            ])

        except subprocess.TimeoutExpired:
            print(f"⏳ Timeout: {onnx_file}")
            results.append([base, param_count, get_expected_result(base), "TIMEOUT",f"{TIMEOUT}s", " ".join(cmd)])
        except Exception as e:
            print(f"❌ Error running {onnx_file}: {e}")
            results.append([base, param_count, get_expected_result(base), f"ERROR: {e}", "N/A", " ".join(cmd)])

    # Write CSV
    version_info = get_verifier_version(VERIFIER)
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Verifier: {VERIFIER}"])
        writer.writerow([f"Version: {version_info}"])
        writer.writerow(["File Name", "Parameter Count", "Expected Result", "Actual Result", "Runtime", "Command"])
        writer.writerows(results)

    print(f"\n✅ Results saved to {CSV_FILE}")

# === Run ===
if __name__ == "__main__":
    run_vnn_verifier()
