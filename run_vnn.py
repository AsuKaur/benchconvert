import os
import subprocess
import csv
import time

VERIFIER = "marabou"
ONNX_DIR = "onnx"
VNNLIB_DIR = "vnnlib"
CSV_FILE = "vnn_result_" + VERIFIER + ".csv"

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

        cmd = [VERIFIER, onnx_path, vnnlib_path]

        print(f"🔍 Running {VERIFIER} on: {onnx_file} + {vnnlib_file}")
        try:
            start = time.time()
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
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
                expected,
                decision,
                f"{runtime}s",
                " ".join(cmd)
            ])

        except subprocess.TimeoutExpired:
            print(f"⏳ Timeout: {onnx_file}")
            results.append([base, get_expected_result(base), "TIMEOUT", "300.0s", " ".join(cmd)])
        except Exception as e:
            print(f"❌ Error running {onnx_file}: {e}")
            results.append([base, get_expected_result(base), f"ERROR: {e}", "N/A", " ".join(cmd)])

    # Write CSV
    version_info = get_verifier_version(VERIFIER)
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Verifier: {VERIFIER}"])
        writer.writerow([f"Version: {version_info}"])
        writer.writerow(["File Name", "Expected Result", "Actual Result", "Runtime", "Command"])
        writer.writerows(results)

    print(f"\n✅ Results saved to {CSV_FILE}")

# === Run ===
if __name__ == "__main__":
    run_vnn_verifier()
