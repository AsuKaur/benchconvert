# This script performs differential testing between an ONNX model, 
# its SMT implementation, and its C implementation.
# 
# PURPOSE: Validates that three different representations of the same neural network
# (ONNX, SMT-LIB, and C) produce equivalent outputs for the same inputs,
# ensuring correctness across different verification and execution environments.

import numpy as np
import onnxruntime as ort  
from z3 import *  
import uuid            
import re               
import subprocess       
import os                
import tempfile 
import argparse

def parse_vnnlib_constraints(vnnlib_file_path, var_prefix='X'):
    # Parses the VNNLIB file to extract variable constraints for inputs or outputs.
    
    # Supports simple range constraints of the form:
    #     (assert (<= {var_prefix}_i upper_bound))    # Upper bound constraint
    #     (assert (>= {var_prefix}_i lower_bound))    # Lower bound constraint
    # or combined as:
    #     (assert (and (<= {var_prefix}_i upper_bound) (>= {var_prefix}_i lower_bound)))
    
    # Args:
    #     vnnlib_file_path (str): Path to the VNNLIB file containing constraints
    #     var_prefix (str): Variable prefix - 'X' for inputs, 'Y' for outputs
    
    # Returns:
    #     list: List of tuples (lower_bound, upper_bound) sorted by variable index
    #           Each tuple represents the valid range for that variable

    bounds = {} 
    
    try:
        with open(vnnlib_file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        raise ValueError(f"Failed to read VNNLIB file: {str(e)}")

    # Parse each line looking for constraint patterns
    for line in lines:
        line = line.strip()
        
        # Match upper bound constraints: (assert (<= X_i value))
        m_le = re.match(rf'\(assert \(<= ({var_prefix}_\d+) ([^\)]+)\)\)', line)
        # Match lower bound constraints: (assert (>= X_i value))
        m_ge = re.match(rf'\(assert \(>= ({var_prefix}_\d+) ([^\)]+)\)\)', line)
        # Match combined constraints: (assert (and (<= X_i upper) (>= X_i lower)))
        m_and = re.match(rf'\(assert \(and \(<= ({var_prefix}_\d+) ([^\)]+)\) \(>= \1 ([^\)]+)\)\)\)', line)

        # Handle combined constraint
        if m_and:
            var = m_and.group(1)           # Variable name (e.g., X_0)
            upper = float(m_and.group(2))  # Upper bound value
            lower = float(m_and.group(3))  # Lower bound value
            bounds[var] = (lower, upper)
            continue

        # Handle individual upper bound constraint
        if m_le:
            var = m_le.group(1)
            upper = float(m_le.group(2))
            # Initialize bounds if not exists, then set upper bound
            if var not in bounds:
                bounds[var] = [float('-inf'), float('inf')]
            bounds[var][1] = upper
            continue

        # Handle individual lower bound constraint
        if m_ge:
            var = m_ge.group(1)
            lower = float(m_ge.group(2))
            # Initialize bounds if not exists, then set lower bound
            if var not in bounds:
                bounds[var] = [float('-inf'), float('inf')]
            bounds[var][0] = lower
            continue

    # Sort variables by their numeric index (X_0, X_1, X_2, ...)
    sorted_keys = sorted(bounds.keys(), key=lambda v: int(v.split('_')[1]))
    sorted_bounds = [bounds[key] for key in sorted_keys]

    return sorted_bounds

def run_onnx_model(onnx_model_path, inputs_np):
    # Runs the ONNX model with the given inputs using ONNXRuntime.
    
    # Args:
    #     onnx_model_path (str): Path to the ONNX model file (.onnx)
    #     inputs_np (np.ndarray): Input array for the ONNX model (shape: [1, n])
    #                            Batch size of 1 with n input features
    
    # Returns:
    #     tuple: (outputs, error) where:
    #            - outputs: List of output values from the model, or None if failed
    #            - error: Error message string, or None if successful

    try:
        # Create an inference session - this loads and optimizes the model
        session = ort.InferenceSession(onnx_model_path)
        
        # Get the name of the first input tensor
        input_name = session.get_inputs()[0].name
        
        # Run inference: session.run(output_names, input_dict)
        outputs = session.run(None, {input_name: inputs_np})[0][0]
        
        return outputs.tolist(), None
    except Exception as e:
        return None, f"ONNX inference failed: {str(e)}"

def run_smt_model(smt_content, inputs, input_size, output_size):
    # Evaluates the SMT model with the given concrete inputs using Z3 solver.
    
    # Args:
    #     smt_content (str): Modified SMT-LIB content (without input/output constraints)
    #     inputs (list): List of concrete input values to test
    #     input_size (int): Number of input variables expected
    #     output_size (int): Number of output variables expected
    
    # Returns:
    #     tuple: (outputs, sat_result, error) where:
    #            - outputs: List of output floats, or None if failed
    #            - sat_result: "sat"/"unsat"/"unknown" from Z3 solver
    #            - error: Error message string, or None if successful

    
    def fp_to_float(fp_val):
        # Converts Z3 floating-point values to Python floats.

        if fp_val is None:
            return None
        
        try:
            fp_str = str(fp_val)
            # print(f"SMT: fp_str={fp_str}")
            
            # Handle special floating-point values
            if 'NaN' in fp_str:
                return float('nan')
            if 'oo' in fp_str or 'inf' in fp_str.lower():
                return float('inf') if '+' in fp_str or not fp_str.startswith('-') else float('-inf')
            
            # Handle scientific notation with powers of 2: "1.5*(2**3)" format
            match = re.match(r'([-+]?\d*\.?\d*)\*\(2\*\*([-+]?\d+)\)', fp_str)
            if match:
                coeff = float(match.group(1))  # Coefficient
                exp = float(match.group(2))    # Exponent
                return coeff * (2 ** exp)
            
            # Handle standard decimal notation
            return float(fp_str)
        except Exception as e:
            print(f"SMT: Error converting FP to float: {str(e)}, fp_val={fp_val}")
            return None

    # Create Z3 solver specifically for quantifier-free bitvector + floating-point logic
    solver = SolverFor("QF_BVFP")
    set_option(precision=30)  # Set high precision for floating-point operations
    
    try:
        # Load the SMT-LIB content into the solver
        solver.from_string(smt_content)
    except Exception as e:
        return None, "unknown", f"Failed to parse SMT content: {str(e)}"
    
    # Use solver stack to allow rollback if needed
    solver.push()
    
    try:
        # Create input variables as 32-bit floating-point numbers
        input_vars = [FP(f'X_{i}', Float32()) for i in range(input_size)]
        
        # Constrain each input variable to its concrete value
        for i, val in enumerate(inputs):
            input_real = RealVal(float(val))  # Convert to Z3 real value
            # print(f"SMT: input{i}_real type={type(input_real)}, value={input_real}")
            # Convert real to floating-point with round-nearest-even
            solver.add(input_vars[i] == fpRealToFP(RNE(), input_real, Float32()))
    except Exception as e:
        solver.pop()
        return None, "unknown", f"SMT constraint setup failed: {str(e)}"
    
    # Check if the constraints are satisfiable
    sat_result = solver.check()
    print(f"SMT: Solver check result={sat_result}")
    
    if sat_result == sat:
        # If satisfiable, extract the output values from the model
        model = solver.model()
        output_vars = [FP(f'Y_{i}', Float32()) for i in range(output_size)]
        outputs = [fp_to_float(model[var]) for var in output_vars]
        solver.pop()
        return outputs, str(sat_result), None
    else:
        # If unsatisfiable or unknown, return appropriate error
        solver.pop()
        print(f"SMT: Solver returned UNSAT, assertions={solver.assertions()}")
        return None, str(sat_result), "SMT solver returned UNSAT"

def run_c_model(c_file_path, inputs, output_size):
    # Tests the C implementation generated by onnx2c with concrete inputs.
    
    # This function modifies existing C code generated by onnx2c to:
    # 1. Replace nondeterministic input assignments with concrete values
    # 2. Remove verification assumptions and assertions
    # 3. Add print statements to capture outputs
    # 4. Compile and execute the modified code
    
    # Args:
    #     c_file_path (str): Path to the C file (generated by onnx2c)
    #     inputs (list): List of float input values
    #     output_size (int): Expected number of output values
    
    # Returns:
    #     tuple: (outputs, error) where:
    #            - outputs: List of output floats, or None if failed
    #            - error: Error message string, or None if successful

    
    try:
        with open(c_file_path, 'r') as f:
            c_lines = f.readlines()
    except Exception as e:
        return None, f"Failed to read C file: {str(e)}"
    
    # Start building modified C code with necessary includes
    modified_lines = ['#include <stdio.h>\n'] 
    in_main = False
    input_size = len(inputs)
    
    # Process each line of the original C file
    for line in c_lines:
        stripped = line.strip()
        
        # Track when we enter the main function
        if stripped.startswith('int main()'):
            in_main = True
        
        # Replace nondeterministic input assignments with concrete values
        # Look for patterns like: tensor_onnx__Gemm_0[0][i] = __VERIFIER_nondet_float();
        if in_main and '__VERIFIER_nondet_float()' in line and 'tensor_onnx__Gemm_0' in line:
            # Extract the array index from the assignment
            match = re.search(r'tensor_onnx__Gemm_0\[0\]\[(\d+)\]', line)
            if match:
                idx = int(match.group(1))
                if idx < input_size:
                    # Replace with concrete input value
                    modified_lines.append(f"    tensor_onnx__Gemm_0[0][{idx}] = {inputs[idx]}f;\n")
                    continue
        
        # Skip verification assumptions 
        if in_main and stripped.startswith('__VERIFIER_assume('):
            continue
        
        # Replace assertions with print statements to capture outputs
        # Assumptions: outputs are in tensor_7[0][j] for j in range(output_size)
        if in_main and stripped.startswith('__VERIFIER_assert('):
            for j in range(output_size):
                modified_lines.append(f"    printf(\"%f\\n\", tensor_7[0][{j}]);\n")
            continue
        
        # Keep all other lines unchanged
        modified_lines.append(line)
    
    modified_content = ''.join(modified_lines)
    
    # Use temporary directory for compilation and execution
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_c_path = os.path.join(tmpdirname, 'temp_test.c')
        temp_exe_path = os.path.join(tmpdirname, 'temp_test')
        
        # Write modified C code to temporary file
        with open(temp_c_path, 'w') as f:
            f.write(modified_content)
        
        # Compile the C code
        # -Iextern: Include directory for header files (verifier_functions.h)
        # -lm: Link math library
        compile_cmd = ['gcc', temp_c_path, '-o', temp_exe_path, '-Iextern', '-lm']
        
        try:
            subprocess.check_call(compile_cmd)
        except subprocess.CalledProcessError as e:
            # If compilation fails, capture detailed error information
            result = subprocess.run(compile_cmd, capture_output=True, text=True)
            error_msg = f"Compilation failed: {str(e)}\nStdout: {result.stdout}\nStderr: {result.stderr}"
            return None, error_msg
        
        # Execute the compiled program
        try:
            result = subprocess.run([temp_exe_path], capture_output=True, text=True, check=True)
            output_lines = result.stdout.strip().split('\n')
            
            # Parse floating-point outputs from program output
            c_outputs = [float(line) for line in output_lines if line]
            
            # Verify we got the expected number of outputs
            if len(c_outputs) != output_size:
                return None, "Unexpected output length from C execution"
            
            return c_outputs, None
            
        except subprocess.CalledProcessError as e:
            return None, f"Execution failed: {str(e)}"

def differential_test_onnx_smt_c(onnx_model_path, smt_file_path, vnnlib_file_path, c_file_path, num_tests=5, tolerance=1e-5):
    # Performs comprehensive differential testing between ONNX, SMT, and C implementations.
    
    # This is the main testing function that orchestrates the entire differential testing process:
    # 1. Parses input/output constraints from VNN-LIB files
    # 2. Generates random test inputs within specified bounds
    # 3. Executes all three implementations (ONNX, SMT, C) with same inputs
    # 4. Compares outputs for consistency within specified tolerance
    # 5. Verifies that outputs satisfy VNN-LIB constraints
    
    # Args:
    #     onnx_model_path (str): Path to the ONNX model file
    #     smt_file_path (str): Path to the SMT-LIB file
    #     vnnlib_file_path (str): Path to the VNN-LIB constraint file
    #     c_file_path (str): Path to the C file generated by onnx2c
    #     num_tests (int): Number of random test cases to generate
    #     tolerance (float): Maximum allowed difference between implementations
    
    # Returns:
    #     dict: Comprehensive test results including:
    #           - test_id: Unique identifier for this test run
    #           - tests: List of individual test results
    #           - all_passed: Boolean indicating if all tests passed

    
    # Initialize results structure
    results = {
        "test_id": str(uuid.uuid4()),  # Unique ID for this test session
        "tests": [],                   # Individual test results
        "all_passed": True             # Overall success flag
    }
    
    print(f"Z3 version: {z3.get_version()}")
    
    # Parse and prepare SMT content by removing input/output constraints
    try:
        with open(smt_file_path, 'r') as f:
            smt_lines = f.readlines()
        
        smt_content = []
        for line in smt_lines:
            # Filter out floating-point constraint assertions for inputs (X_*) and outputs (Y_*)
            # These use fp.leq (<=) and fp.geq (>=) operators
            if not (re.match(r'\s*\(assert\s*\(fp\.(leq|geq)\s*(X_[0-9]+|Y_[0-9]+)\s*', line)):
                smt_content.append(line)
        
        smt_content = ''.join(smt_content)
    except Exception as e:
        results["error"] = f"Failed to parse SMT file: {str(e)}"
        return results
    
    # Parse input bounds and output constraints from VNN-LIB file
    input_bounds = parse_vnnlib_constraints(vnnlib_file_path, 'X')       # Input variable bounds
    output_constraints = parse_vnnlib_constraints(vnnlib_file_path, 'Y') # Output variable constraints
    input_size = len(input_bounds)
    output_size = len(output_constraints)
    
    print(input_bounds)       # Show parsed input bounds
    print(output_constraints) # Show parsed output constraints
    
    # Run the specified number of test cases
    for i in range(num_tests):
        test_result = {"test_number": i + 1}
        
        # Generate random inputs within the specified bounds
        inputs = [np.random.uniform(low, high) for low, high in input_bounds]
        inputs_np = np.array(inputs, dtype=np.float32).reshape(1, -1)  # Shape for ONNX: [batch_size, features]
        
        # Test 1: Run ONNX model
        onnx_outputs, onnx_error = run_onnx_model(onnx_model_path, inputs_np)
        if onnx_error:
            test_result["error"] = onnx_error
            results["tests"].append(test_result)
            results["all_passed"] = False
            continue
        
        test_result["onnx_inputs"] = inputs
        test_result["onnx_outputs"] = onnx_outputs
        
        # Test 2: Run SMT model
        smt_outputs, smt_sat, smt_error = run_smt_model(smt_content, inputs, input_size, output_size)
        if smt_error:
            test_result["error"] = smt_error
            results["tests"].append(test_result)
            results["all_passed"] = False
            continue
        
        test_result["smt_sat"] = smt_sat
        test_result["smt_outputs"] = smt_outputs
        
        # Test 3: Run C model
        c_outputs, c_error = run_c_model(c_file_path, inputs, output_size)
        if c_error:
            test_result["error"] = c_error
            results["tests"].append(test_result)
            results["all_passed"] = False
            continue
        
        test_result["c_outputs"] = c_outputs
        
        # Compare outputs if all models executed successfully
        if smt_sat == "sat" and smt_outputs is not None and c_outputs is not None:
            
            # Calculate pairwise differences between all implementations
            # ONNX vs SMT comparison
            onnx_smt_diff = [
                abs(onnx_outputs[j] - smt_outputs[j]) if smt_outputs[j] is not None and not np.isnan(smt_outputs[j]) else float('inf')
                for j in range(output_size)
            ]
            
            # ONNX vs C comparison  
            onnx_c_diff = [
                abs(onnx_outputs[j] - c_outputs[j]) for j in range(output_size)
            ]
            
            # SMT vs C comparison
            smt_c_diff = [
                abs(smt_outputs[j] - c_outputs[j]) if smt_outputs[j] is not None and not np.isnan(smt_outputs[j]) else float('inf')
                for j in range(output_size)
            ]
            
            test_result["onnx_smt_diff"] = onnx_smt_diff
            test_result["onnx_c_diff"] = onnx_c_diff
            test_result["smt_c_diff"] = smt_c_diff
            
            # Check if all outputs are within tolerance
            outputs_match = (
                all(diff <= tolerance for diff in onnx_smt_diff) and
                all(diff <= tolerance for diff in onnx_c_diff) and
                all(diff <= tolerance for diff in smt_c_diff)
            )
            test_result["outputs_match"] = outputs_match
            
            # Check if outputs are valid
            constraints_satisfied = True
            for j in range(output_size):
                # Check SMT outputs
                smt_output = smt_outputs[j]
                if smt_output is None or np.isnan(smt_output):
                    constraints_satisfied = False
                
                # Check C outputs
                c_output = c_outputs[j]
                if np.isnan(c_output):
                    constraints_satisfied = False
                    
            test_result["constraints_satisfied"] = constraints_satisfied
            
            # Overall test passes if outputs match AND constraints are satisfied
            test_result["passed"] = test_result["outputs_match"] and constraints_satisfied
            
            print(f"\nTest {test_result['test_number']}:")
            print(f"  Inputs: {test_result['onnx_inputs']}")
            print(f"  ONNX Outputs: {test_result['onnx_outputs']}")
            print(f"  SMT Outputs: {test_result.get('smt_outputs', 'Not available (SMT failed)')}")
            print(f"  C Outputs: {test_result.get('c_outputs', 'Not available (C failed)')}")
            print(f"  ONNX-SMT Differences: {test_result.get('onnx_smt_diff', 'Not available')}")
            print(f"  ONNX-C Differences: {test_result.get('onnx_c_diff', 'Not available')}")
            print(f"  SMT-C Differences: {test_result.get('smt_c_diff', 'Not available')}")
            print(f"  Outputs Match: {test_result.get('outputs_match', 'Not available')}")
            print(f"  Constraints Satisfied: {test_result.get('constraints_satisfied', 'Not available')}")
            print(f"  Test Passed: {test_result.get('passed', 'Not available')}")
            print("\n")
        else:
            # If any model failed to produce valid outputs, test fails
            test_result["outputs_match"] = False
            test_result["constraints_satisfied"] = False
            test_result["passed"] = False
        
        results["tests"].append(test_result)
        results["all_passed"] = results["all_passed"] and test_result["passed"]
    
    return results


if __name__ == "__main__":
    parser = argparse.ArgumentParser(description="Run differential testing on ONNX, SMT, and C models.")
    parser.add_argument('model_name', help='Name of the model (e.g., unsat_v2_c3)')
    args = parser.parse_args()

    model_name = args.model_name
    onnx_model_path = f"onnx/{model_name}.onnx"      # ONNX neural network model
    smt_file_path = f"smt/{model_name}.smt2"         # SMT-LIB encoding of the model
    vnnlib_file_path = f"vnnlib/{model_name}.vnnlib" # VNN-LIB property specification
    c_file_path = f"c/{model_name}.c"                # C implementation from onnx2c
    
    # Run differential testing
    results = differential_test_onnx_smt_c(onnx_model_path, smt_file_path, vnnlib_file_path, c_file_path)
    
    # Print comprehensive results
    print(f"Test ID: {results['test_id']}")
    print(f"All Tests Passed: {results['all_passed']}")
    
    # Print detailed results for each individual test
    # for test in results["tests"]:
    #     print(f"\nTest {test['test_number']}:")
    #     print(f"  Inputs: {test['onnx_inputs']}")
    #     print(f"  ONNX Outputs: {test['onnx_outputs']}")
    #     print(f"  SMT Outputs: {test.get('smt_outputs', 'Not available (SMT failed)')}")
    #     print(f"  C Outputs: {test.get('c_outputs', 'Not available (C failed)')}")
    #     print(f"  ONNX-SMT Differences: {test.get('onnx_smt_diff', 'Not available')}")
    #     print(f"  ONNX-C Differences: {test.get('onnx_c_diff', 'Not available')}")
    #     print(f"  SMT-C Differences: {test.get('smt_c_diff', 'Not available')}")
    #     print(f"  Outputs Match: {test.get('outputs_match', 'Not available')}")
    #     print(f"  Constraints Satisfied: {test.get('constraints_satisfied', 'Not available')}")
    #     print(f"  Test Passed: {test.get('passed', 'Not available')}")
    #     if "error" in test:
    #         print(f"  Error: {test['error']}")
