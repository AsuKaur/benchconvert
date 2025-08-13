import onnx
import re


# Count the number of parameters in an ONNX model
def count_parameters_onnx(onnx_path):
    try:
        model = onnx.load(onnx_path)
        param_count = 0
        for tensor in model.graph.initializer:
            dims = tensor.dims
            count = 1
            for d in dims:
                count *= d
            param_count += count
        return param_count
    except Exception as e:
        print(f"Failed to count parameters for {onnx_path}: {e}")
        return "N/A"

# Count the number of parameters of the model in an SMT file
def count_parameters_smt(smt_file_path):
    with open(smt_file_path, 'r') as file:
        content = file.read()

    # Count input features (X_i)
    input_matches = re.findall(r'\(declare-fun X_(\d+) ', content)
    num_inputs = len(set(input_matches)) 

    # Count hidden units (from H_0_j declarations)
    hidden_matches = re.findall(r'\(declare-fun H_0_(\d+) ', content)
    num_hidden = len(set(hidden_matches))

    # Count output units (from Y_k declarations)
    output_matches = re.findall(r'\(declare-fun Y_(\d+) ', content)
    num_outputs = len(set(output_matches))

    # Calculate parameters
    # Input to hidden: weights + biases
    input_to_hidden = (num_inputs * num_hidden) + num_hidden
    # Hidden to output: weights + biases
    hidden_to_output = (num_hidden * num_outputs) + num_outputs
    total_parameters = input_to_hidden + hidden_to_output

    return total_parameters

# Count parameters in a C file 
def count_parameters_c(file_path):
    weight_pattern = re.compile(r'static\s+const\s+float\s+(\w*weight\w*)\s*\[(.*?)\]\s*=')
    bias_pattern = re.compile(r'static\s+const\s+float\s+(\w*bias\w*)\s*\[(.*?)\]\s*=')

    total_params = 0

    with open(file_path, "r") as f:
        data = f.read()

    # Find all weight arrays
    weights = weight_pattern.findall(data)
    for name, dims in weights:
        count = 1
        for dim in dims.split("]["):
            dim_clean = dim.replace("[","").replace("]","").strip()
            count *= int(dim_clean)
        print(f"Found weight {name} with {count} parameters")
        total_params += count

    # Find all bias arrays
    biases = bias_pattern.findall(data)
    for name, dims in biases:
        count = 1
        for dim in dims.split("]["):
            dim_clean = dim.replace("[","").replace("]","").strip()
            count *= int(dim_clean)
        print(f"Found bias {name} with {count} parameters")
        total_params += count

    return total_params
