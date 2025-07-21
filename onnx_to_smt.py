# ONNX to SMT-LIB Converter

# This script converts neural network models from ONNX format along with their
# verification specifications (vnnlib files) into SMT-LIB format for formal
# verification using SMT solvers like Z3, CVC5, etc.

# The conversion process:
# 1. Parses the vnnlib file to extract input/output variable names and constraints
# 2. Loads the ONNX model and extracts weights/biases from each layer
# 3. Generates SMT-LIB assertions that encode the neural network computation
# 4. Adds the original verification constraints from vnnlib
# 5. Outputs a complete SMT-LIB file ready for solver verification

# Folder Structure:
#     onnx/           - Input ONNX model files
#     vnnlib/         - Input vnnlib files for ONNX
#     smt/            - Output SMT files for the ONNX + VNNLIB files

# Usage:
#     python onnx_to_smt.py <onnx_filename>           # Convert single file
#     python onnx_to_smt.py --all                     # Convert all ONNX files



import sys
import argparse
from pathlib import Path
import onnx
from onnx import numpy_helper
import re

# Directory structure for organizing input and output files
ONNX_DIR = Path("onnx")        # Directory containing .onnx model files
VNNLIB_DIR = Path("vnnlib")    # Directory containing .vnnlib specification files
SMT_DIR = Path("smt")          # Directory for output .smt2 files

def setup_directories():
    # Create the required directory structure if it doesn't exist.
    # This ensures we have organized locations for input ONNX files,
    # vnnlib specification files, and output SMT-LIB files.

    ONNX_DIR.mkdir(exist_ok=True)
    VNNLIB_DIR.mkdir(exist_ok=True)
    SMT_DIR.mkdir(exist_ok=True)

def parse_vnnlib(vnnlib_path):
    # Parse a vnnlib (verification neural network library) file to extract:
    # 1. Input variable declarations (typically X_0, X_1, ... or similar)
    # 2. Output variable declarations (typically Y_0, Y_1)
    # 3. Verification constraints (assert statements)
    
    # vnnlib format uses S-expressions similar to SMT-LIB:
    # - (declare-const X_0 Real) declares an input variable
    # - (declare-const Y_0 Real) declares an output variable  
    # - (assert (>= X_0 0.0)) adds a constraint
    
    # Args:
    #     vnnlib_path: Path to the .vnnlib file
        
    # Returns:
    #     tuple: (input_vars, output_vars, constraints)
    #            - input_vars: list of input variable names
    #            - output_vars: list of output variable names  
    #            - constraints: list of constraint strings

    input_vars = []
    output_vars = []
    constraints = []

    with open(vnnlib_path, "r") as f:
        for line in f:
            line = line.strip()
            
            # Skip empty lines and comments (lines starting with ;)
            if not line or line.startswith(";"):
                continue
                
            # Parse variable declarations
            if line.startswith("(declare-const"):
                # Extract variable name from declaration
                # Example: "(declare-const X_0 Real)" -> parts = ["declare-const", "X_0", "Real"]
                parts = line.replace("(","").replace(")","").split()
                varname = parts[1]
                
                # Classify variables as input or output based on naming conventions
                # Input variables typically start with X, in, I
                # Output variables typically start with Y, out, O
                if varname.startswith("X") or varname.startswith("in") or varname.startswith("I"):
                    input_vars.append(varname)
                elif varname.startswith("Y") or varname.startswith("out") or varname.startswith("O"):
                    output_vars.append(varname)
                else:
                    # Fallback heuristic: alternate between input and output
                    # if naming convention is unclear
                    if len(input_vars) <= len(output_vars):
                        input_vars.append(varname)
                    else:
                        output_vars.append(varname)
                        
            # Collect all constraint assertions
            elif line.startswith("(assert"):
                constraints.append(line)

    return input_vars, output_vars, constraints

def onnx_to_smt(onnx_path, vnnlib_path, smt_path):
    # Main conversion function that transforms an ONNX neural network model
    # and its vnnlib specification into SMT-LIB format.
    
    # The SMT-LIB encoding process:
    # 1. Parse vnnlib to get variable names and constraints
    # 2. Load ONNX model and extract layer parameters (weights, biases)
    # 3. Create SMT variables for each layer's neurons
    # 4. Generate assertions encoding the forward pass computation
    # 5. Apply ReLU activations (except on output layer)
    # 6. Bind output variables to final layer outputs
    # 7. Add original vnnlib constraints
    
    # Args:
    #     onnx_path: Path to input .onnx file
    #     vnnlib_path: Path to input .vnnlib file  
    #     smt_path: Path to output .smt2 file

    # First, parse the vnnlib file to understand the verification problem
    input_vars, output_vars, vnn_constraints = parse_vnnlib(vnnlib_path)
    print(f"\n✔ Processing: {onnx_path.name}")
    print(f" - Input vars: {input_vars}")
    print(f" - Output vars: {output_vars}")

    # Load the ONNX model and extract initialized parameters (weights & biases)
    model = onnx.load(onnx_path)
    
    # Convert ONNX tensor initializers to numpy arrays for easier manipulation
    # Initializers contain the learned parameters (weights and biases) of the network
    initializers = {init.name: numpy_helper.to_array(init) for init in model.graph.initializer}

    print(f" - Found initializers: {[name for name in initializers]}")

    # Extract unique layer names by removing .weight/.bias suffixes
    # Example: "layer1.weight" and "layer1.bias" both belong to "layer1"
    layer_names = sorted(set(re.sub(r'\.(weight|bias)$','', name) for name in initializers))

    # Start building the SMT-LIB file
    # QF_NRA = Quantifier-Free Nonlinear Real Arithmetic
    # (supports real numbers, multiplication, but no quantifiers)
    smt = ["(set-logic QF_NRA)"]

    # Declare input variables as real numbers in SMT-LIB
    for name in input_vars:
        smt.append(f"(declare-const {name} Real)")

    # Keep track of variables from the previous layer
    # Initially, these are the input variables
    previous_vars = input_vars.copy()

    # Process each layer of the neural network
    for layer_idx, layer in enumerate(layer_names):
        # Extract weight matrix W and bias vector B for this layer
        W = initializers[f"{layer}.weight"]  # Shape: (output_neurons, input_neurons)
        B = initializers[f"{layer}.bias"]    # Shape: (output_neurons,)

        # Create variable names for this layer's outputs
        # Format: H_<layer_name>_<neuron_index>
        current_vars = [f"H_{layer}_{i}" for i in range(B.shape[0])]
        
        # Declare each neuron output as a real variable
        for var in current_vars:
            smt.append(f"(declare-const {var} Real)")

        # Generate assertions for each neuron in this layer
        for i, bias in enumerate(B):
            # Compute linear transformation: sum(W[i][j] * input[j]) + bias
            # Create terms for the weighted sum
            terms = " ".join([f"(* {prev} {W[i][j]})" for j, prev in enumerate(previous_vars)])
            expr = f"(+ {terms} {bias})"
            
            # Apply activation function
            # ReLU for hidden layers: max(0, x) implemented as (ite (>= x 0) x 0)
            # Linear activation for output layer (no activation)
            if layer != layer_names[-1]:  # Hidden layer - apply ReLU
                smt.append(f"(assert (= {current_vars[i]} (ite (>= {expr} 0) {expr} 0)))")
            else:  # Output layer - linear activation
                smt.append(f"(assert (= {current_vars[i]} {expr}))")

        # Update for next iteration: current layer outputs become next layer inputs
        previous_vars = current_vars

    # Bind the output variables from vnnlib to the final layer outputs
    # This connects the neural network computation to the verification variables
    for i, out in enumerate(output_vars):
        smt.append(f"(declare-const {out} Real)")
        # Assert that output variable equals the corresponding final layer neuron
        smt.append(f"(assert (= {out} {previous_vars[i]}))")

    # Add the original verification constraints from the vnnlib file
    # These define the property we want to verify (e.g., robustness, safety)
    smt.extend(vnn_constraints)

    # Add SMT solver commands
    smt.append("(check-sat)")    # Check if the formula is satisfiable
    smt.append("(get-model)")    # If SAT, get a model (counterexample)

    # Write the complete SMT-LIB file
    with open(smt_path, "w") as f:
        f.write("\n".join(smt))

    print(f" - SMT-LIB saved to: {smt_path}")

def process_single(name):
    # Process a single ONNX+vnnlib pair by name.
    
    # Looks for files:
    # - onnx/{name}.onnx
    # - vnnlib/{name}.vnnlib
    
    # Generates:
    # - smt/{name}.smt2
    
    # Args:
    #     name: Base name of the files (without extension)

    onnx_path = ONNX_DIR / f"{name}.onnx"
    vnnlib_path = VNNLIB_DIR / f"{name}.vnnlib"
    smt_path = SMT_DIR / f"{name}.smt2"

    # Verify both input files exist
    if not onnx_path.exists() or not vnnlib_path.exists():
        print(f"✗ Missing files: {onnx_path} or {vnnlib_path}")
        return

    onnx_to_smt(onnx_path, vnnlib_path, smt_path)

def process_all():
    # Batch process all matching ONNX and vnnlib file pairs.
    
    # Finds all .onnx files in the onnx/ directory and .vnnlib files
    # in the vnnlib/ directory, then processes every pair that has
    # matching base names.

    # Build dictionaries mapping base names to file paths
    onnx_files = {p.stem: p for p in ONNX_DIR.glob("*.onnx")}
    vnnlib_files = {p.stem: p for p in VNNLIB_DIR.glob("*.vnnlib")}
    
    # Find files that exist in both directories (intersection of keys)
    common_names = onnx_files.keys() & vnnlib_files.keys()
    total_count = len(common_names)
    
    if not common_names:
        print("✗ No matching ONNX and vnnlib files found.")
        return

    # Process each matching pair
    for name in sorted(common_names):
        onnx_path = onnx_files[name]
        vnnlib_path = vnnlib_files[name]
        smt_path = SMT_DIR / f"{name}.smt2"
        onnx_to_smt(onnx_path, vnnlib_path, smt_path)

    print(f"\nConversion Summary:")
    print(f"  📊 Total pairs processed: {total_count}")
    print(f"  📁 Output directory: {SMT_DIR}")

def main():
    # Main entry point. Sets up directories and handles command line arguments.
    
    # Usage:
    #     python onnx_to_smt.py model           # Convert specific model (without extension)
    #     python onnx_to_smt.py --all           # Convert all matching pairs

    # Set up command line argument parsing with detailed help
    parser = argparse.ArgumentParser(
        description="Convert ONNX + vnnlib pairs to SMT-LIB format for formal verification",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Directory Structure:
  onnx/           - Place your ONNX model files here
  vnnlib/         - Place your vnnlib specification files here  
  smt/            - Generated SMT-LIB files will be saved here

Examples:
  python onnx_to_smt.py model      # Convert onnx/model.onnx + vnnlib/model.vnnlib -> smt/model.smt2
  python onnx_to_smt.py --all      # Convert all matching ONNX+vnnlib pairs
        """
    )
    
    # Main argument group - mutually exclusive options
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument(
        'model_name',
        nargs='?',
        help='Name of model files (without extension, e.g., "model" for model.onnx + model.vnnlib)'
    )
    
    group.add_argument(
        '--all',
        action='store_true',
        help='Convert all matching ONNX+vnnlib file pairs'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true', 
        help='Enable verbose output during conversion'
    )
    
    args = parser.parse_args()
    
    # Setup directories
    setup_directories()
    
    # Convert all files mode
    if args.all:
        print("Converting all matching ONNX+vnnlib pairs...")
        # Process all files
        process_all()
        return 0
    
    # Convert single file mode  
    if args.model_name:
        process_single(args.model_name)
        
        print("\n✓ Conversion completed successfully!")
        print(f"Generated SMT-LIB file: smt/{args.model_name}.smt2")
        return 0
    
    # No arguments provided - show help
    parser.print_help()
    return 1

if __name__ == "__main__":
    sys.exit(main())