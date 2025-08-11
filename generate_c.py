# This script automates the process of converting ONNX models to C source files. 

import sys
import subprocess
import os
from pathlib import Path

# Helper function to run a Python script as a subprocess and capture its output.
def run_script(script_name, args=None):
    # Default to empty list if no arguments are provided
    args = args or []
    
    # Run the script using the current Python executable
    result = subprocess.run([sys.executable, script_name] + args, capture_output=True, text=True)
    
    # Print a header for clarity on which script is being run
    print(f"Running {script_name} with args: {args}")
    
    # Print the standard output from the script
    print(result.stdout)
    
    # If there is any error output, print it for debugging
    if result.stderr:
        print(f"Error/Warnings from {script_name}:\n{result.stderr}")
    
    # Check if the script failed (non-zero exit code) and handle it by exiting
    if result.returncode != 0:
        print(f"{script_name} failed with exit code {result.returncode}")
        sys.exit(result.returncode)

def main():
    # Step 1: Convert ONNX models to C source files
    # This runs the onnx_to_c.py script with '--all' to process all ONNX files in the 'onnx' directory
    run_script('onnx_to_c.py', ['--all'])

    # Step 2: Generate C property files for the converted networks
    # This runs the generate_c_prop.py script with '--all' to create property files for all C files in 'c_network'
    run_script('generate_c_prop.py', ['--all'])

    # Step 3: Combine and Preprocess the c files
    # This runs the c_ops.py script to combine property and network files, then preprocess them
    run_script('c_ops.py')


if __name__ == "__main__":
    main()
