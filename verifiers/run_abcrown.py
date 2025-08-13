import os
import subprocess
import csv
import time
import tempfile
import onnx 
import sys
from pathlib import Path

# Add parent directory to Python path to import from helpers
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
sys.path.insert(0, str(ROOT_DIR))

# Import custom sorting function from helpers (now in root directory)
from helpers.sort_files import sort_files_by_v_c
from helpers.parameter_count import count_parameters_onnx

VERIFIER = "abcrown"
ONNX_DIR = ROOT_DIR / "onnx"
VNNLIB_DIR = ROOT_DIR / "vnnlib"
RESULT_DIR = ROOT_DIR / "results"
CSV_FILE = RESULT_DIR / f"vnn_result_{VERIFIER}.csv"
TIMEOUT = 900

# ABCROWN_PY = "/Users/asukaur/Softwares/AlphaBetaCrown/alpha-beta-CROWN/complete_verifier/abcrown.py"
# VENV_PYTHON = "/Users/asukaur/myenv311/bin/python"
# YAML_TEMPLATE = "/Users/asukaur/Softwares/AlphaBetaCrown/alpha-beta-CROWN/complete_verifier/exp_configs/tutorial_examples/onnx_with_one_vnnlib.yaml"
YAML_TEMPLATE = ROOT_DIR / "extern" / "abcrown.yaml"

ABCROWN_PY = "/mnt/iusers01/fse-ugpgt01/compsci01/e80540ak/software/abcrown/alpha-beta-CROWN/complete_verifier/abcrown.py"
VENV_PYTHON = "/mnt/iusers01/fse-ugpgt01/compsci01/e80540ak/envs/alpha-beta-crown/bin/python"
# YAML_TEMPLATE = "/mnt/iusers01/fse-ugpgt01/compsci01/e80540ak/software/abcrown/alpha-beta-CROWN/complete_verifier/exp_configs/tutorial_examples/onnx_with_one_vnnlib.yaml"

def run_with_live_output(cmd, timeout):
    # Run cmd, stream stdout/stderr live, and return combined output string.
    proc = subprocess.Popen(
        cmd,
        stdout=subprocess.PIPE,
        stderr=subprocess.STDOUT,
        text=True,
        bufsize=1 
    )
    output_lines = []
    start = time.time()
    try:
        for line in proc.stdout:
            print(line, end="")        
            sys.stdout.flush()
            output_lines.append(line) 
        proc.wait(timeout=timeout)
    except subprocess.TimeoutExpired:
        proc.kill()
        print(f"Timeout after {timeout}s")
    end = time.time()
    return "".join(output_lines), round(end - start, 4)

def get_expected_result(filename):
    filename = filename.lower()
    if "unsat" in filename:
        return "UNSAT"
    elif "sat" in filename:
        return "SAT"
    return "UNKNOWN"

def parse_output(output):
    decision = "UNKNOWN"
    runtime = "N/A"

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
        if "time:" in l:
            import re
            match = re.search(r"time:\s*([0-9.]+)", l)
            if match:
                runtime = f"{match.group(1)}s"

    return decision, runtime

# Patch YAML file with correct onnx and vnnlib paths
def make_temp_yaml(onnx_path, vnnlib_path):
    import yaml

    with open(YAML_TEMPLATE, "r") as f:
        cfg = yaml.safe_load(f)

    cfg["model"]["onnx_path"] = str(onnx_path)
    cfg["specification"]["vnnlib_path"] = str(vnnlib_path)
    cfg["bab"]["timeout"] = TIMEOUT

    tmpf = tempfile.NamedTemporaryFile(mode="w", delete=False, suffix=".yaml")
    yaml.dump(cfg, tmpf)
    tmpf.close()
    return tmpf.name


def get_verifier_version():
    try:
        result = subprocess.run([VENV_PYTHON, ABCROWN_PY, "--version"], capture_output=True, text=True, timeout=TIMEOUT)
        output = result.stdout.strip() or result.stderr.strip()
        if "error" in output.lower():
            return "No version found"
        return output
    except Exception:
        return "Version info not available"

def run_vnn_verifier():
    results = []

    onnx_files = sort_files_by_v_c([f for f in os.listdir(ONNX_DIR) if f.endswith(".onnx")])

    for onnx_file in onnx_files:
        base = os.path.splitext(onnx_file)[0]
        vnnlib_file = base + ".vnnlib"

        onnx_path = ONNX_DIR / onnx_file
        vnnlib_path = VNNLIB_DIR / vnnlib_file

        if not vnnlib_path.exists():
            print(f"Skipping {onnx_file}, matching VNNLIB file not found.")
            continue

        param_count = count_parameters_onnx(onnx_path)

        temp_yaml = make_temp_yaml(onnx_path, vnnlib_path)

        cmd = [VENV_PYTHON, ABCROWN_PY, "--config", temp_yaml]

        print(f"Running {VERIFIER} on: {onnx_file} + {vnnlib_file}")
        try:
            start = time.time()
            proc = subprocess.run(cmd, capture_output=True, text=True, timeout=TIMEOUT)
            output = proc.stdout + proc.stderr
            # output, elapsed = run_with_live_output(cmd, TIMEOUT)

            end = time.time()

            decision, runtime_str = parse_output(output)
            # fallback to measured time if parsing fails
            if runtime_str == "N/A":
                runtime_str = f"{round(end - start, 4)}s"

            expected = get_expected_result(base)

            results.append([
                base,
                param_count,         
                expected,
                decision,
                runtime_str,
                " ".join(cmd)
            ])

        except subprocess.TimeoutExpired:
            print(f"Timeout: {onnx_file}")
            results.append([base, param_count, get_expected_result(base), "TIMEOUT", f"{TIMEOUT}s", " ".join(cmd)])
        except Exception as e:
            print(f"Error running {onnx_file}: {e}")
            results.append([base, param_count, get_expected_result(base), f"ERROR: {e}", "N/A", " ".join(cmd)])

        finally:
            os.remove(temp_yaml)

    version_info = get_verifier_version()
    with open(CSV_FILE, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Verifier: {VERIFIER}"])
        writer.writerow([f"Version: {version_info}"])
        writer.writerow(["File Name", "Parameter Count", "Expected Result", "Actual Result", "Runtime", "Command"])
        writer.writerows(results)

    print(f"\nSaved to {CSV_FILE}")

if __name__ == "__main__":
    RESULT_DIR.mkdir(exist_ok=True)
    run_vnn_verifier()
