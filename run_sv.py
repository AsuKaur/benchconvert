import os
import subprocess
import csv
import time

# === CONFIGURATION ===
VERIFIER = "cbmc"  # Changed from "esbmc" to "cbmc"

PROP_DIR = "c_prop"
NET_DIR = "c_network"
OUTPUT_CSV = "sv_result_" + VERIFIER + ".csv"

FLAGS = [
    "--no-bounds-check",
    "--no-pointer-check",
    "--unwind", "10",
    "-Iextern"
] if  VERIFIER == "cbmc" else [
    "--floatbv",
    "--no-bounds-check",
    "--no-pointer-check",
    "--no-div-by-zero-check",
    "--k-induction",
    "--unwind", "10",
    "-Iextern"
] 

# === FUNCTIONS ===

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

def run_verifier():
    results = []
    for prop_file in sorted(os.listdir(PROP_DIR)):
        if not prop_file.endswith(".c"):
            continue

        base_name = prop_file.replace("prop_", "")
        net_file = base_name

        prop_path = os.path.join(PROP_DIR, prop_file)
        net_path = os.path.join(NET_DIR, net_file)

        if not os.path.exists(net_path):
            print(f"⚠️ Skipping {prop_file} – network file not found.")
            continue

        cmd = [VERIFIER, prop_path, net_path] + FLAGS
        print(f"🔍 Running {VERIFIER} on: {prop_file} + {net_file}")

        try:
            start_time = time.time()  # Start timer
            result = subprocess.run(cmd, capture_output=True, text=True, timeout=900)
            elapsed_time = time.time() - start_time  # In seconds
            output = result.stdout + result.stderr
            actual_result, runtime, solver = parse_verifier_output(output)

            # Decide expected result based on prop filename
            expected_result = "UNSAT" if "unsat" in prop_file.lower() else "SAT"

            results.append([
                prop_file,
                expected_result,
                actual_result,
                runtime if VERIFIER != "cbmc" else f"{elapsed_time:.4f}s",
                solver,
                " ".join(FLAGS)
            ])
        except subprocess.TimeoutExpired:
            print(f"⏳ Timeout: {prop_file}")
            results.append([
                prop_file,
                "UNSAT" if "unsat" in prop_file.lower() else "SAT",
                "TIMEOUT",
                "TIMEOUT",
                "UNKNOWN",
                " ".join(FLAGS)
            ])
        except Exception as e:
            print(f"❌ Error running {prop_file}: {e}")
            results.append([
                prop_file,
                "UNSAT" if "unsat" in prop_file.lower() else "SAT",
                f"ERROR: {e}",
                "ERROR",
                "UNKNOWN",
                " ".join(FLAGS)
            ])

    verifier_version = get_verifier_version(VERIFIER)
    with open(OUTPUT_CSV, mode="w", newline="") as f:
        writer = csv.writer(f)
        writer.writerow([f"Verifier: {VERIFIER}"])
        writer.writerow([f"Version: {verifier_version}"])
        writer.writerow([
            "File Name",
            "Expected Result",
            "Actual Result",
            "Runtime decision procedure" if VERIFIER == "esbmc" else "Runtime",
            "Solver Used",
            "Flags Used"
        ])
        writer.writerows(results)

    print(f"\n✅ Results saved to {OUTPUT_CSV}")

# === MAIN ===

if __name__ == "__main__":
    run_verifier()
