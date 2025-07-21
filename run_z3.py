import os
import subprocess

def run_smt2_files_with_z3(smt_folder='smt'):
    # Ensure the folder exists
    if not os.path.isdir(smt_folder):
        print(f"Error: Folder '{smt_folder}' does not exist.")
        return

    smt_files = [f for f in os.listdir(smt_folder) if f.endswith('.smt2')]

    if not smt_files:
        print(f"No .smt2 files found in '{smt_folder}'")
        return

    for filename in smt_files:
        filepath = os.path.join(smt_folder, filename)
        print(f"\nRunning Z3 on: {filename}")
        try:
            result = subprocess.run(['z3', filepath], capture_output=True, text=True, timeout=30)
            print("Result:")
            print(result.stdout.strip() if result.stdout else "(No output)")
            if result.stderr:
                print("Errors:")
                print(result.stderr.strip())
        except subprocess.TimeoutExpired:
            print("Error: Z3 timed out.")
        except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == '__main__':
    run_smt2_files_with_z3()
