# ONNX to SMT-LIB Converter with Floating-Point Arithmetic

# This enhanced version converts neural network models from ONNX format along with 
# vnnlib verification specifications into SMT-LIB format using IEEE 754 floating-point
# arithmetic instead of real numbers. This provides more accurate modeling of actual
# neural network behavior since real implementations use finite-precision arithmetic.

# The conversion process:
# 1. Parses vnnlib to extract variables and constraints
# 2. Loads ONNX model and validates it
# 3. Processes ONNX graph nodes (Gemm, ReLU operations)
# 4. Generates SMT-LIB with floating-point variables and operations
# 5. Translates constraints to floating-point comparisons
# 6. Outputs complete SMT-LIB file for solver verification

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
import numpy as np
import z3

# Directory structure for organizing input and output files
ONNX_DIR = Path("onnx")        # Directory containing .onnx model files
VNNLIB_DIR = Path("vnnlib")    # Directory containing .vnnlib specification files
SMT_DIR = Path("smt")          # Directory for output .smt2 files

def setup_directories():
    # Create the required directory structure if it doesn't exist.
    # Ensures organized storage for input ONNX models, vnnlib specifications,
    # and generated SMT-LIB output files.

    ONNX_DIR.mkdir(exist_ok=True)
    VNNLIB_DIR.mkdir(exist_ok=True)
    SMT_DIR.mkdir(exist_ok=True)

def float_to_bv32(f):
    # Convert a Python float to a Z3 32-bit IEEE 754 floating-point value.
    
    # This function handles the conversion from Python's native float representation
    # to Z3's floating-point representation that matches IEEE 754 single precision.
    # This is crucial for accurate modeling since neural networks typically use
    # 32-bit floats in practice.
    
    # Args:
    #     f: Input float value (can be numpy floating type or regular float)
        
    # Returns:
    #     z3.FPVal: Z3 floating-point value in Float32 format (8-bit exponent, 24-bit significand)

    # Ensure we have a standard Python float (handles numpy types)
    f = float(f) if isinstance(f, np.floating) else f
    return z3.FPVal(f, z3.Float32())

def parse_vnnlib(vnnlib_path):
    # Parse a vnnlib file to extract input/output variables and their constraints.
    
    # This enhanced parser separates input and output constraints for better
    # organization and more accurate constraint handling. It distinguishes between:
    # - Input constraints: bounds on network inputs 
    # - Output constraints: properties to verify on network outputs
    
    # vnnlib format uses S-expressions:
    # - (declare-const X_0 Real) declares an input variable
    # - (declare-const Y_0 Real) declares an output variable  
    # - (assert (<= X_0 1.0)) adds an input constraint
    # - (assert (>= Y_0 0.5)) adds an output constraint
    
    # Args:
    #     vnnlib_path: Path to the .vnnlib specification file
        
    # Returns:
    #     tuple: (input_vars, output_vars, input_constraints, output_constraints)
    #            - input_vars: list of input variable names
    #            - output_vars: list of output variable names
    #            - input_constraints: list of constraint strings for inputs
    #            - output_constraints: list of constraint strings for outputs

    input_vars = []
    output_vars = []
    input_constraints = []   # Constraints on input variables 
    output_constraints = []  # Constraints on output variables 

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
                parts = line.replace("(", "").replace(")", "").split()
                varname = parts[1]
                
                # Classify variables based on naming conventions
                # Input: X*, in*, I* | Output: Y*, out*, O*
                if varname.startswith("X") or varname.startswith("in") or varname.startswith("I"):
                    input_vars.append(varname)
                elif varname.startswith("Y") or varname.startswith("out") or varname.startswith("O"):
                    output_vars.append(varname)
                else:
                    # Fallback: alternate assignment if naming is unclear
                    if len(input_vars) <= len(output_vars):
                        input_vars.append(varname)
                    else:
                        output_vars.append(varname)
                        
            # Parse constraint assertions and categorize them
            elif line.startswith("(assert"):
                # Parse assertion structure: (assert (op var value))
                expr = line[1:-1].split()  # Remove outer parentheses and split
                if expr[0] == "assert":
                    # Check if constraint applies to input or output variable
                    variable_in_constraint = expr[2]  # Usually the variable name
                    if variable_in_constraint in input_vars:
                        input_constraints.append(line)
                    elif variable_in_constraint in output_vars:
                        output_constraints.append(line)

    return input_vars, output_vars, input_constraints, output_constraints

def onnx_to_smt(onnx_path, vnnlib_path, smt_path):
    # Convert ONNX neural network model and VNNLIB constraints to SMT-LIB format
    # using IEEE 754 floating-point arithmetic for accurate modeling.
    
    # This function uses QF_BVFP logic (Quantifier-Free Bit-Vectors and Floating-Point)
    # which supports:
    # - IEEE 754 floating-point arithmetic operations
    # - Bit-precise modeling of float32 computations
    # - Rounding modes for floating-point operations
    # - More accurate representation than real arithmetic
    
    # The conversion process:
    # 1. Parse vnnlib to understand the verification problem
    # 2. Load and validate ONNX model structure
    # 3. Process each ONNX graph node sequentially
    # 4. Generate SMT variables and constraints for each layer
    # 5. Translate vnnlib constraints to floating-point logic
    
    # Args:
    #     onnx_path: Path to input .onnx model file
    #     vnnlib_path: Path to input .vnnlib specification file
    #     smt_path: Path to output .smt2 file

    # Parse VNNLIB file to extract verification specification
    input_vars, output_vars, input_constraints, output_constraints = parse_vnnlib(vnnlib_path)
    print(f"\n✔ Processing: {onnx_path.name}")
    print(f" - Input vars: {input_vars}")
    print(f" - Output vars: {output_vars}")

    # Load and validate ONNX model
    model = onnx.load(onnx_path)
    # Validate model structure to catch malformed ONNX files early
    onnx.checker.check_model(model)

    # Extract model parameters (weights and biases) from initializers
    # Convert to float32 for consistency with typical neural network precision
    initializers = {init.name: numpy_helper.to_array(init).astype(np.float32) 
                   for init in model.graph.initializer}
    print(f" - Found initializers: {[name for name in initializers]}")

    # Start building SMT-LIB file with floating-point logic
    # QF_BVFP = Quantifier-Free Bit-Vectors and Floating-Point
    # Supports IEEE 754 operations without quantifiers
    smt = ["(set-logic QF_BVFP)"]

    # Create Z3 floating-point variables for inputs
    # Float32 = 8-bit exponent + 24-bit significand (IEEE 754 single precision)
    input_fp_vars = [z3.FP(f"{name}", z3.Float32()) for name in input_vars]
    for var in input_fp_vars:
        # Declare each input as a floating-point function returning Float32
        smt.append(f"(declare-fun {var.decl().name()} () (_ FloatingPoint 8 24))")

    # Translate input constraints from vnnlib to floating-point SMT-LIB
    for constraint in input_constraints:
        # Parse constraint structure: (assert (op var value))
        expr = constraint[1:-1].split()  # Remove parentheses and split
        var = expr[2]           # Variable name (e.g., "X_0")
        op = expr[1].replace('(', '')  # Operator (e.g., "<=", ">=")
        value = float(expr[3].replace(')', ''))  # Constraint value
        
        # Find corresponding floating-point variable
        var_idx = input_vars.index(var)
        var_fp = input_fp_vars[var_idx]
        
        # Generate floating-point comparison
        if op == "<=":
            smt.append(f"(assert (fp.leq {var_fp.sexpr()} {float_to_bv32(value).sexpr()}))")
        elif op == ">=":
            smt.append(f"(assert (fp.geq {var_fp.sexpr()} {float_to_bv32(value).sexpr()}))")
        elif op == "<":
            smt.append(f"(assert (fp.lt {var_fp.sexpr()} {float_to_bv32(value).sexpr()}))")
        elif op == ">":
            smt.append(f"(assert (fp.gt {var_fp.sexpr()} {float_to_bv32(value).sexpr()}))")
        elif op == "==":
            smt.append(f"(assert (fp.eq {var_fp.sexpr()} {float_to_bv32(value).sexpr()}))")

    # Process ONNX computational graph node by node
    # Track intermediate variables and current layer outputs
    intermediate_vars = {}  # Maps ONNX tensor names to Z3 variables
    current_input = input_fp_vars  # Variables from previous layer
    node_count = 0  # Counter for generating unique variable names

    # Iterate through ONNX graph nodes in execution order
    for node in model.graph.node:
        
        # Handle General Matrix Multiplication (Gemm) operation
        # Gemm computes: Y = α * A * B + β * C (typically α=β=1, C=bias)
        if node.op_type == "Gemm":
            # Extract input tensor names
            input_name = node.input[0]    # Input tensor (from previous layer)
            weight_name = node.input[1]   # Weight matrix
            bias_name = node.input[2]     # Bias vector
            output_name = node.output[0]  # Output tensor name
            
            # Get weight matrix and bias vector from initializers
            W = initializers.get(weight_name)
            b = initializers.get(bias_name)
            if W is None or b is None:
                print(f"Error: Weight {weight_name} or bias {bias_name} not found")
                sys.exit(1)

            # Handle weight matrix transposition if specified
            # Check ONNX node attributes for transB flag
            for attr in node.attribute:
                if attr.name == "transB" and attr.i == 1:
                    W = W.T  # Transpose weight matrix

            # Determine output dimension
            out_dim = W.shape[1] if len(W.shape) > 1 else 1
            # Create output variables for this layer
            y = [z3.FP(f"H_{node_count}_{i}", z3.Float32()) for i in range(out_dim)]
            
            for var in y:
                smt.append(f"(declare-fun {var.decl().name()} () (_ FloatingPoint 8 24))")

            # Generate matrix multiplication constraints
            # For each output neuron: y[i] = Σ(w[j,i] * input[j]) + bias[i]
            for i in range(out_dim):
                # Get bias value for this output neuron
                bias_val = float(b[i]) if len(b.shape) > 0 else float(b)
                sum_expr = float_to_bv32(bias_val)  # Start with bias
                
                # Add weighted inputs: Σ(weight * input)
                for j in range(len(current_input)):
                    w_ij = float(W[j, i]) if len(W.shape) > 1 else float(W[j])
                    # Floating-point multiplication and addition with rounding
                    # RNE = Round to Nearest Even (IEEE 754 default rounding mode)
                    sum_expr = z3.fpAdd(z3.RNE(), sum_expr, 
                                       z3.fpMul(z3.RNE(), float_to_bv32(w_ij), current_input[j]))                    

                # Assert that output variable equals computed expression
                smt.append(f"(assert (= {y[i].sexpr()} {sum_expr.sexpr()}))")

            # Store intermediate results and update current layer
            intermediate_vars[output_name] = y
            current_input = y
            node_count += 1

        # Handle Rectified Linear Unit (ReLU) activation function
        # ReLU(x) = max(0, x) = x if x >= 0, else 0
        elif node.op_type == "Relu":
            input_name = node.input[0]    # Input tensor name
            output_name = node.output[0]  # Output tensor name
            inputs = intermediate_vars[input_name]  # Get input variables
            
            # Create output variables for ReLU layer
            y = [z3.FP(f"H_{node_count}_{i}", z3.Float32()) for i in range(len(inputs))]
            for var in y:
                smt.append(f"(declare-fun {var.decl().name()} () (_ FloatingPoint 8 24))")

            # Generate ReLU constraints for each neuron
            # Use conditional (ite) expression: if input >= 0 then input else 0
            for i in range(len(inputs)):
                zero = float_to_bv32(0.0)  # Floating-point zero
                # ReLU: output = (input >= 0) ? input : 0
                smt.append(f"(assert (= {y[i].sexpr()} "
                          f"(ite (fp.geq {inputs[i].sexpr()} {zero.sexpr()}) "
                          f"{inputs[i].sexpr()} {zero.sexpr()})))")

            # Update intermediate variables and current layer
            intermediate_vars[output_name] = y
            current_input = y
            node_count += 1
            
        # Additional node types (Conv2D, MaxPool, etc.) could be handled here
        # Each would require specific logic for their mathematical operations

    # Bind output variables from vnnlib to final network layer outputs
    # This assumes the final layer output tensor is named "7" (ONNX-specific)
    output_fp_vars = intermediate_vars.get("7")
    if not output_fp_vars or len(output_fp_vars) != len(output_vars):
        print("Error: Output tensor '7' not found or incorrect shape")
        print(f"Available tensors: {list(intermediate_vars.keys())}")
        print(f"Expected {len(output_vars)} outputs, found {len(output_fp_vars) if output_fp_vars else 0}")
        sys.exit(1)

    # Create connections between vnnlib output variables and network outputs
    for i, out in enumerate(output_vars):
        smt.append(f"(declare-fun {out} () (_ FloatingPoint 8 24))")
        # Assert equality between vnnlib output var and network output
        smt.append(f"(assert (= {out} {output_fp_vars[i].sexpr()}))")

    # Translate output constraints from vnnlib to floating-point SMT-LIB
    for constraint in output_constraints:
        # Parse output constraint structure
        expr = constraint[1:-1].split()
        var = expr[2]           # Output variable name
        op = expr[1].replace('(', '')  # Comparison operator
        value = float(expr[3].replace(')', ''))  # Constraint value
        
        # Generate floating-point constraint
        if op == "<=":
            fp_op = 'fp.leq'
        elif op == ">=":
            fp_op = 'fp.geq'
        elif op == "<":
            fp_op = 'fp.lt'
        elif op == ">":
            fp_op = 'fp.gt'
        elif op == "==":
            fp_op = 'fp.eq'
        
        smt.append(f"(assert ({fp_op} {var} {float_to_bv32(value).sexpr()}))")

    # Add SMT solver commands
    smt.append("(check-sat)")    # Check satisfiability of all constraints
    smt.append("(get-model)")    # If SAT, retrieve variable assignments

    # Write complete SMT-LIB file
    with open(smt_path, "w") as f:
        f.write("\n".join(smt))

    print(f" - SMT-LIB saved to: {smt_path}")

def process_single(name, smt_dir):
    # Process a single ONNX+vnnlib pair by base name.
    
    # Locates the corresponding .onnx and .vnnlib files, validates their
    # existence, and converts them to SMT-LIB format.
    
    # Args:
    #     name: Base name of the files (without extensions)

    onnx_path = ONNX_DIR / f"{name}.onnx"
    vnnlib_path = VNNLIB_DIR / f"{name}.vnnlib"
    smt_path = smt_dir / f"{name}.smt2"

    # Verify required input files exist
    if not onnx_path.exists() or not vnnlib_path.exists():
        print(f"✗ Missing files: {onnx_path} or {vnnlib_path}")
        return

    # Perform the conversion
    onnx_to_smt(onnx_path, vnnlib_path, smt_path)

def process_all(smt_dir):
    # Batch process all matching ONNX and vnnlib file pairs.
    
    # Discovers all .onnx files in the onnx/ directory and .vnnlib files
    # in the vnnlib/ directory, then processes every pair with matching
    # base names. Provides a summary of the batch conversion results.

    # Build file inventories
    onnx_files = {p.stem: p for p in ONNX_DIR.glob("*.onnx")}
    vnnlib_files = {p.stem: p for p in VNNLIB_DIR.glob("*.vnnlib")}
    
    # Find matching pairs (intersection of base names)
    common_names = onnx_files.keys() & vnnlib_files.keys()
    total_count = len(common_names)

    if not common_names:
        print("✗ No matching ONNX and vnnlib files found.")
        return

    # Process each matching pair
    for name in sorted(common_names):
        onnx_path = onnx_files[name]
        vnnlib_path = vnnlib_files[name]
        smt_path = smt_dir / f"{name}.smt2"
        onnx_to_smt(onnx_path, vnnlib_path, smt_path)

    # Provide batch conversion summary
    print(f"\nConversion Summary:")
    print(f"  📊 Total pairs processed: {total_count}")
    print(f"  📁 Output directory: {smt_dir}")

def main():
    # Main entry point with enhanced command line interface.
    
    # Provides a user-friendly interface for converting neural network
    # verification problems from ONNX+vnnlib format to SMT-LIB format
    # with floating-point precision modeling.

    # Set up comprehensive argument parsing
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

    # Create mutually exclusive argument groups
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
    
    # Additional options
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output during conversion'
    )

    parser.add_argument(
    '--o', '--output',
    dest='output_dir',
    type=str,
    help='Directory to save the generated SMT-LIB files (overrides default smt/)'
    )


    args = parser.parse_args()
    
    # Initialize directory structure
    setup_directories()

    # Use provided output directory if specified
    smt_dir = Path(args.output_dir) if args.output_dir else SMT_DIR
    smt_dir.mkdir(exist_ok=True)

    # Handle batch processing mode
    if args.all:
        print("Converting all matching ONNX+vnnlib pairs...")
        process_all(smt_dir)
        return 0

    # Handle single file processing mode
    if args.model_name:
        process_single(args.model_name, smt_dir)
        print("\n✓ Conversion completed successfully!")
        print(f"Generated SMT-LIB file: {smt_dir}/{args.model_name}.smt2")
        return 0

    # No arguments provided - show help
    parser.print_help()
    return 1

if __name__ == "__main__":
    sys.exit(main())