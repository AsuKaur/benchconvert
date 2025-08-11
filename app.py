# This script executes other Python scripts in sequence to generate
# dimacs files, ONNX and VNNLIB files, ONNX to C conversion and it's 
# corresponding files, and ONNX to SMT conversion.

import subprocess
import sys

def run_script(script, args=[]):
    result = subprocess.run([sys.executable, script] + args)
    if result.returncode != 0:
        sys.exit(result.returncode)

def main():
    seed = sys.argv[1] if len(sys.argv) > 1 else "2"
    
    run_script("generate_properties.py", [seed])
    run_script("generate_c.py")
    run_script("onnx_to_smt.py", ["--all"])
    
    print("All files have been generated successfully.")

if __name__ == "__main__":
    main()
