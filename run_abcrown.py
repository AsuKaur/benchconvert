import os
import subprocess
import csv
import time
import tempfile

# === Config ===
VERIFIER = "abcrown"
ONNX_DIR = "onnx"
VNNLIB_DIR = "vnnlib"
CSV_FILE = f"vnn_result_{VERIFIER}.csv"

ABCROWN_PY = "/Users/asukaur/Softwares/AlphaBetaCrown/alpha-beta-CROWN/complete_verifier/abcrown.py"
VENV_PYTHON = "/Users/asukaur/myenv311/bin/python"
YAML_TEMPLATE = "/Users/asukaur/Softwares/AlphaBetaCrown/alpha-beta-CROWN/complete_verifier/exp_configs/tutorial_examples/onnx_with_one_vnnlib.yaml"

# === Helper to get expected result from filename ===
def get_expected_result(filename):
    filename = filename.lower()
    if "unsat" in filename:
        return "UNSAT"
    elif "sat" in filename:
        return "SAT"
    return "UNKNOWN"

# === Parse output to find result and runtime ===
def parse_output(output):
    decision = "UNKNOWN"
    runtime = "N/A"

    # Try to find "Result:" line or "verified_status"
    for line in output.splitlines():
        l = line.lower()
        if "result:" in l:
            if "unsat" in l:
                decision = "UNSAT"
            elif "sat" in l:
                decision = "SAT"
            elif "timeout" in l:
                decision = "TIMEOUT"
            else:
                decision = "UNKNOWN"
        if "verified_status" in l:
            if "true" in l:
                decision = "UNSAT"
            elif "false" in l:
                decision = "SAT"

        # Extract runtime from lines with "Time:" or "time:"
        if "time:" in l:
            import re
            # Search for something like 0.123 or 0.1234 seconds
            match = re.search(r"time:\s*([0-9.]+)", l)
            if match:
                runtime = f"{match.group(1)}s"

    return decision, runtime

# === Patch YAML file with correct onnx and vnnlib paths ===
def make_temp_yaml(onnx_path, vnnlib_path):
    import yaml

    with open(YAML_TEMPLATE, "r") as f:
        cfg = yaml.safe_load(f)

    cfg["model"]["onnx_path"] = onnx_path
    cfg["specification"]["vnnlib_path"] = vnnlib_path

    tmpf = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml")
    yaml.dump(cfg, tmpf)
    tmpf.close()
    return tmpf.name

def get_verifier_version():
    try:
        result = subprocess.run([VENV_PYTHON, ABCROWN_PY, "--version"], capture_output=True, text=True, timeout=10)
        return result.stdout.strip() or result.stderr.strip()
    except Exception:
        return "Version info not available"

def run_vnn_verifier():
    results = []

    onnx_files = sorted([f for f in os.listdir(ONNX_DIR) if f.endswith(".onnx")])

    for onnx_file in onnx_files:
        base = os.path.splitext(onnx_file)[0]
        vnnlib_file = base + ".vnnlib"

        onnx_path = os.path.abspath(os.path.join(ONNX_DIR, onnx_file))
        vnnlib_path = os.path.abspath(os.path.join(VNNLIB_DIR, vnnlib_file))

        if not os.path.exists(vnnlib_path):
            print(f"⚠️ Skipping {onnx_file} – matching VNNLIB file not found.")
            continue

        temp_yaml = make_temp_yaml(onnx_path, vnnlib_path)

        cmd = [VENV_PYTHON, ABCROWN_PY, "--config", temp_yaml]

        print(f"🔍 Running {VERIFIER} on: {onnx_file} + {vnnlib_file}")
        try:
            start = time.time()
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=300)
            end = time.time()

            output = proc.stdout + proc.stderr

            decision, runtime_str = parse_output(output)
            # fallback to measured time if parsing fails
            if runtime_str == "N/A":
                runtime_str = f"{round(end - start, 4)}s"

            expected = get_expected_result(base)

            results.append([
                base,
                expected,
                decision,
                runtime_str,
                " ".join(cmd)
            ])

        except subprocess.TimeoutExpired:
            print(f"⏳ Timeout: {onnx_file}")
            results.append([base, get_expected_result(base), "TIMEOUT", "300.0s", " ".join(cmd)])
        except Exception as e:
            print(f"❌ Error running {onnx_file}: {e}")
            results.append([base, get_expected_result(base), f"ERROR: {e}", "N/A", " ".join(cmd)])

        finally:
            os.remove(temp_yaml)

    version_info = get_verifier_version()
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Verifier: {VERIFIER}"])
        writer.writerow([f"Version: {version_info}"])
        writer.writerow(["File Name", "Expected Result", "Actual Result", "Runtime", "Command"])
        writer.writerows(results)

    print(f"\n✅ Results saved to {CSV_FILE}")

if __name__ == "__main__":
    run_vnn_verifier()
