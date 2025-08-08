import numpy as np
import onnxruntime as ort
from z3 import *
import uuid
import re
import subprocess
import os
import tempfile


def parse_vnnlib_constraints(vnnlib_file_path, var_prefix='X'):
    """
    Parses the VNNLIB file to extract variable constraints for inputs or outputs.
    Supports simple range constraints of the form:
        (assert (<= {var_prefix}_i upper_bound))
        (assert (>= {var_prefix}_i lower_bound))
    or combined as:
        (assert (and (<= {var_prefix}_i upper_bound) (>= {var_prefix}_i lower_bound)))

    Args:
        vnnlib_file_path (str): Path to the VNNLIB file.
        var_prefix (str): 'X' for inputs or 'Y' for outputs.

    Returns:
        list: List of tuples (lower_bound, upper_bound) sorted by variable index.
    """
    bounds = {}
    try:
        with open(vnnlib_file_path, 'r') as f:
            lines = f.readlines()
    except Exception as e:
        raise ValueError(f"Failed to read VNNLIB file: {str(e)}")

    for line in lines:
        line = line.strip()
        m_le = re.match(rf'\(assert \(<= ({var_prefix}_\d+) ([^\)]+)\)\)', line)
        m_ge = re.match(rf'\(assert \(>= ({var_prefix}_\d+) ([^\)]+)\)\)', line)
        m_and = re.match(rf'\(assert \(and \(<= ({var_prefix}_\d+) ([^\)]+)\) \(>= \1 ([^\)]+)\)\)\)', line)

        if m_and:
            var = m_and.group(1)
            upper = float(m_and.group(2))
            lower = float(m_and.group(3))
            bounds[var] = (lower, upper)
            continue

        if m_le:
            var = m_le.group(1)
            upper = float(m_le.group(2))
            if var not in bounds:
                bounds[var] = [float('-inf'), float('inf')]
            bounds[var][1] = upper
            continue

        if m_ge:
            var = m_ge.group(1)
            lower = float(m_ge.group(2))
            if var not in bounds:
                bounds[var] = [float('-inf'), float('inf')]
            bounds[var][0] = lower
            continue

    # Sort by variable index (e.g., X_0, X_1, ...)
    sorted_keys = sorted(bounds.keys(), key=lambda v: int(v.split('_')[1]))
    sorted_bounds = [bounds[key] for key in sorted_keys]

    return sorted_bounds


def run_onnx_model(onnx_model_path, inputs_np):
    """
    Runs the ONNX model with the given inputs.
    
    Args:
        onnx_model_path (str): Path to the ONNX model file.
        inputs_np (np.ndarray): Input array for the ONNX model (shape: [1, n]).
    
    Returns:
        tuple: (outputs, error) where outputs is the model output or None, and error is an error message or None.
    """
    try:
        session = ort.InferenceSession(onnx_model_path)
        input_name = session.get_inputs()[0].name
        outputs = session.run(None, {input_name: inputs_np})[0][0]
        return outputs.tolist(), None
    except Exception as e:
        return None, f"ONNX inference failed: {str(e)}"


def run_smt_model(smt_content, inputs, input_size, output_size):
    """
    Evaluates the SMT model with the given concrete inputs using Z3.
    
    Args:
        smt_content (str): Modified SMT-LIB content (without input/output constraints).
        inputs (list): List of input values.
        input_size (int): Number of input variables.
        output_size (int): Number of output variables.
    
    Returns:
        tuple: (outputs, sat_result, error) where outputs is list of floats or None, sat_result is "sat"/"unsat",
               and error is an error message or None.
    """
    def fp_to_float(fp_val):
        if fp_val is None:
            return None
        try:
            fp_str = str(fp_val)
            print(f"SMT: fp_str={fp_str}")  # Debug: Print raw string
            if 'NaN' in fp_str:
                return float('nan')
            if 'oo' in fp_str or 'inf' in fp_str.lower():
                return float('inf') if '+' in fp_str or not fp_str.startswith('-') else float('-inf')
            match = re.match(r'([-+]?\d*\.?\d*)\*\(2\*\*([-+]?\d+)\)', fp_str)
            if match:
                coeff = float(match.group(1))
                exp = float(match.group(2))
                return coeff * (2 ** exp)
            return float(fp_str)
        except Exception as e:
            print(f"SMT: Error converting FP to float: {str(e)}, fp_val={fp_val}")
            return None

    solver = SolverFor("QF_BVFP")
    set_option(precision=30)
    
    try:
        solver.from_string(smt_content)
    except Exception as e:
        return None, "unknown", f"Failed to parse SMT content: {str(e)}"
    
    solver.push()
    try:
        input_vars = [FP(f'X_{i}', Float32()) for i in range(input_size)]
        for i, val in enumerate(inputs):
            input_real = RealVal(float(val))
            print(f"SMT: input{i}_real type={type(input_real)}, value={input_real}")
            solver.add(input_vars[i] == fpRealToFP(RNE(), input_real, Float32()))
    except Exception as e:
        solver.pop()
        return None, "unknown", f"SMT constraint setup failed: {str(e)}"
    
    sat_result = solver.check()
    if sat_result == sat:
        model = solver.model()
        output_vars = [FP(f'Y_{i}', Float32()) for i in range(output_size)]
        outputs = [fp_to_float(model[var]) for var in output_vars]
        print(f"SMT: model={model}")
        solver.pop()
        return outputs, str(sat_result), None
    else:
        solver.pop()
        print(f"SMT: Solver returned UNSAT, assertions={solver.assertions()}")
        return None, str(sat_result), "SMT solver returned UNSAT"


def run_c_model(c_file_path, inputs, output_size):
    """
    Tests the C implementation generated by onnx2c with concrete inputs.
    Modifies the existing C code to set concrete inputs, removes assumes and asserts,
    adds print statements for outputs, then compiles and runs it.
    
    Args:
        c_file_path (str): Path to the C file (e.g., sat_v2_c1.c or combined).
        inputs (list): List of float inputs.
        output_size (int): Number of output values.
        extern_dir (str): Relative path to the 'extern' folder containing verifier_functions.h (default 'extern').
    
    Returns:
        tuple: (outputs, error) where outputs is list of floats or None, and error is an error message or None.
    """
    try:
        with open(c_file_path, 'r') as f:
            c_lines = f.readlines()
    except Exception as e:
        return None, f"Failed to read C file: {str(e)}"
    
    modified_lines = ['#include <stdio.h>\n']  # Ensure stdio.h is included for printf
    in_main = False
    input_size = len(inputs)
    for line in c_lines:
        stripped = line.strip()
        
        # Detect start of main
        if stripped.startswith('int main()'):
            in_main = True
        
        # Replace nondet assignments with concrete values (generalized for any number of inputs)
        if in_main and '__VERIFIER_nondet_float()' in line and 'tensor_onnx__Gemm_0' in line:
            # Parse the index from the line, e.g., tensor_onnx__Gemm_0[0][i]
            match = re.search(r'tensor_onnx__Gemm_0\[0\]\[(\d+)\]', line)
            if match:
                idx = int(match.group(1))
                if idx < input_size:
                    modified_lines.append(f"    tensor_onnx__Gemm_0[0][{idx}] = {inputs[idx]}f;\n")
                    continue
        
        # Skip assume statements
        if in_main and stripped.startswith('__VERIFIER_assume('):
            continue
        
        # Replace assert with print statements (generalized for output_size)
        if in_main and stripped.startswith('__VERIFIER_assert('):
            for j in range(output_size):
                modified_lines.append(f"    printf(\"%f\\n\", tensor_7[0][{j}]);\n")
            continue
        
        modified_lines.append(line)
    
    modified_content = ''.join(modified_lines)
    
    with tempfile.TemporaryDirectory() as tmpdirname:
        temp_c_path = os.path.join(tmpdirname, 'temp_test.c')
        temp_exe_path = os.path.join(tmpdirname, 'temp_test')
        
        with open(temp_c_path, 'w') as f:
            f.write(modified_content)
        
        # For debugging: Print the modified C content
        print("Temporary C File Content:\n", modified_content)
        
        compile_cmd = ['gcc', temp_c_path, '-o', temp_exe_path, '-Iextern', '-lm']
        try:
            subprocess.check_call(compile_cmd)
        except subprocess.CalledProcessError as e:
            result = subprocess.run(compile_cmd, capture_output=True, text=True)
            error_msg = f"Compilation failed: {str(e)}\nStdout: {result.stdout}\nStderr: {result.stderr}"
            return None, error_msg
        
        try:
            result = subprocess.run([temp_exe_path], capture_output=True, text=True, check=True)
            output_lines = result.stdout.strip().split('\n')
            c_outputs = [float(line) for line in output_lines if line]
            if len(c_outputs) != output_size:
                return None, "Unexpected output length from C execution"
            return c_outputs, None
        except subprocess.CalledProcessError as e:
            return None, f"Execution failed: {str(e)}"


def differential_test_onnx_smt_c(onnx_model_path, smt_file_path, vnnlib_file_path, c_file_path, num_tests=10, tolerance=1e-5):
    """
    Performs differential testing between an ONNX model, its SMT implementation, and its C implementation.
    Verifies VNN-LIB properties and compares outputs for concrete inputs.
    
    Args:
        onnx_model_path (str): Path to the ONNX model file.
        smt_file_path (str): Path to the SMT-LIB file.
        vnnlib_file_path (str): Path to the VNN-LIB file.
        c_file_path (str): Path to the C file generated by onnx2c.
        num_tests (int): Number of concrete input tests to run.
        tolerance (float): Tolerance for floating-point output comparison.
    
    Returns:
        dict: Results of the tests, including pass/fail status and details.
    """
    results = {
        "test_id": str(uuid.uuid4()),
        "tests": [],
        "all_passed": True
    }
    
    print(f"Z3 version: {z3.get_version_string()}")
    
    try:
        with open(smt_file_path, 'r') as f:
            smt_lines = f.readlines()
        smt_content = []
        for line in smt_lines:
            if not (re.match(r'\s*\(assert\s*\(fp\.(leq|geq)\s*(X_[0-9]+|Y_[0-9]+)\s*', line)):
                smt_content.append(line)
        smt_content = ''.join(smt_content)
    except Exception as e:
        results["error"] = f"Failed to parse SMT file: {str(e)}"
        return results
    
    input_bounds = parse_vnnlib_constraints(vnnlib_file_path, 'X')
    output_constraints = parse_vnnlib_constraints(vnnlib_file_path, 'Y')
    input_size = len(input_bounds)
    output_size = len(output_constraints)
    print(input_bounds)
    print(output_constraints)
    
    for i in range(num_tests):
        test_result = {"test_number": i + 1}
        
        inputs = [np.random.uniform(low, high) for low, high in input_bounds]
        inputs_np = np.array(inputs, dtype=np.float32).reshape(1, -1)
        
        onnx_outputs, onnx_error = run_onnx_model(onnx_model_path, inputs_np)
        if onnx_error:
            test_result["error"] = onnx_error
            results["tests"].append(test_result)
            results["all_passed"] = False
            continue
        
        test_result["onnx_inputs"] = inputs
        test_result["onnx_outputs"] = onnx_outputs
        
        smt_outputs, smt_sat, smt_error = run_smt_model(smt_content, inputs, input_size, output_size)
        if smt_error:
            test_result["error"] = smt_error
            results["tests"].append(test_result)
            results["all_passed"] = False
            continue
        
        test_result["smt_sat"] = smt_sat
        test_result["smt_outputs"] = smt_outputs
        
        c_outputs, c_error = run_c_model(c_file_path, inputs, output_size)
        if c_error:
            test_result["error"] = c_error
            results["tests"].append(test_result)
            results["all_passed"] = False
            continue
        
        test_result["c_outputs"] = c_outputs
        
        if smt_sat == "sat" and smt_outputs is not None and c_outputs is not None:
            # Compare ONNX vs SMT
            onnx_smt_diff = [
                abs(onnx_outputs[j] - smt_outputs[j]) if smt_outputs[j] is not None and not np.isnan(smt_outputs[j]) else float('inf')
                for j in range(output_size)
            ]
            # Compare ONNX vs C
            onnx_c_diff = [
                abs(onnx_outputs[j] - c_outputs[j]) for j in range(output_size)
            ]
            # Compare SMT vs C
            smt_c_diff = [
                abs(smt_outputs[j] - c_outputs[j]) if smt_outputs[j] is not None and not np.isnan(smt_outputs[j]) else float('inf')
                for j in range(output_size)
            ]
            
            test_result["onnx_smt_diff"] = onnx_smt_diff
            test_result["onnx_c_diff"] = onnx_c_diff
            test_result["smt_c_diff"] = smt_c_diff
            
            outputs_match = (
                all(diff <= tolerance for diff in onnx_smt_diff) and
                all(diff <= tolerance for diff in onnx_c_diff) and
                all(diff <= tolerance for diff in smt_c_diff)
            )
            test_result["outputs_match"] = outputs_match
            
            constraints_satisfied = True
            for j in range(output_size):
                # Check SMT outputs
                smt_output = smt_outputs[j]
                lower, upper = output_constraints[j]
                if smt_output is None or np.isnan(smt_output) or not (lower <= smt_output <= upper):
                    constraints_satisfied = False
                # Check C outputs
                c_output = c_outputs[j]
                if np.isnan(c_output) or not (lower <= c_output <= upper):
                    constraints_satisfied = False
            test_result["constraints_satisfied"] = constraints_satisfied
            
            test_result["passed"] = test_result["outputs_match"] and constraints_satisfied
        else:
            test_result["outputs_match"] = False
            test_result["constraints_satisfied"] = False
            test_result["passed"] = False
        
        results["tests"].append(test_result)
        results["all_passed"] = results["all_passed"] and test_result["passed"]
    
    return results


if __name__ == "__main__":
    onnx_model_path = "onnx/unsat_v2_c3.onnx"
    smt_file_path = "smt/unsat_v2_c3.smt2"
    vnnlib_file_path = "vnnlib/unsat_v2_c3.vnnlib"
    c_file_path = "c/unsat_v2_c3.c"  # Adjust to your C file path (e.g., sat_v2_c1.c or combined)
    results = differential_test_onnx_smt_c(onnx_model_path, smt_file_path, vnnlib_file_path, c_file_path)
    
    print(f"Test ID: {results['test_id']}")
    print(f"All Tests Passed: {results['all_passed']}")
    for test in results["tests"]:
        print(f"\nTest {test['test_number']}:")
        print(f"  Inputs: {test['onnx_inputs']}")
        print(f"  ONNX Outputs: {test['onnx_outputs']}")
        print(f"  SMT Outputs: {test.get('smt_outputs', 'Not available (SMT failed)')}")
        print(f"  C Outputs: {test.get('c_outputs', 'Not available (C failed)')}")
        print(f"  ONNX-SMT Differences: {test.get('onnx_smt_diff', 'Not available')}")
        print(f"  ONNX-C Differences: {test.get('onnx_c_diff', 'Not available')}")
        print(f"  SMT-C Differences: {test.get('smt_c_diff', 'Not available')}")
        print(f"  Outputs Match: {test.get('outputs_match', 'Not available')}")
        print(f"  Constraints Satisfied: {test.get('constraints_satisfied', 'Not available')}")
        print(f"  Test Passed: {test.get('passed', 'Not available')}")
        if "error" in test:
            print(f"  Error: {test['error']}")
