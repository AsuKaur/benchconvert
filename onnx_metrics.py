# This script validates and analyses ONNX models.

import os
import onnx
import numpy as np

ONNX_DIR = "onnx"  

def size_of_file(num):
    for unit in ['B','KB','MB','GB']:
        if abs(num) < 1024.0:
            return "%3.1f %s" % (num, unit)
        num /= 1024.0
    return "%.1f %s" % (num, 'TB')

def analyze_onnx_model(model_path):
    print(f"\nModel: {model_path}")

    file_size = os.path.getsize(model_path)
    print(f"File size: {file_size} bytes ({size_of_file(file_size)})")

    # Load the ONNX model
    model = onnx.load(model_path)
        
    # Check if the model is valid
    onnx.checker.check_model(model)
    graph = model.graph

    print(f"ONNX model validation passed: {model_path}")
        
    # Print model info
    print(f"  - IR version: {model.ir_version}")
    print(f"  - Producer: {model.producer_name} {model.producer_version}")
    print(f"  - Graph inputs: {len(model.graph.input)}")
    print(f"  - Graph outputs: {len(model.graph.output)}")
    print(f"  - Graph nodes: {len(model.graph.node)}")

    # Input/Output
    input_names = [i.name for i in graph.input]
    output_names = [o.name for o in graph.output]
    print("Inputs:", input_names)
    print("Outputs:", output_names)

    # Count layers (nodes)
    all_layer_types = [node.op_type for node in graph.node]
    print("Total layers (nodes):", len(all_layer_types))
    print("Layer types:", set(all_layer_types))

    # Collect hidden layers: nodes that are not directly connected to input/output
    hidden_layers = []
    input_set = set(input_names)
    output_set = set(output_names)
    for node in graph.node:
        # check if node is not direct input or output, i.e., is internal computation
        if not (any(inp in input_set for inp in node.input) or any(out in output_set for out in node.output)):
            hidden_layers.append(node)

    print(f"Possible hidden layers: {len(hidden_layers)}")
    # Layers (by name/type)
    for idx, node in enumerate(hidden_layers):
        print(f"  Hidden Layer {idx+1}: Name: {node.name or '(no name)'} Type: {node.op_type}")

    # Try to extract linear/gemm layers' weight matrix sizes to estimate neurons
    neuron_by_layer = []
    for node in graph.node:
        if node.op_type in ("Gemm", "MatMul", "Conv"):
            weight_names = node.input[1:] # skip input[0] which is layer input
            weights = [init for init in graph.initializer if init.name in weight_names]
            for arr in weights:
                shape = tuple(dim for dim in arr.dims)
                neuron_by_layer.append((node.name, node.op_type, shape))
    if neuron_by_layer:
        print("Hidden layer sizes (according to Gemm/MatMul/Conv):")
        for name, op_type, shape in neuron_by_layer:
            print(f"  Layer {name or '(no name)'}, Type: {op_type}, Weights shape: {shape}")

    # Count total parameters
    total_params = 0
    for initializer in graph.initializer:
        arr = onnx.numpy_helper.to_array(initializer)
        total_params += arr.size
    print(f"Total number of parameters: {total_params}")

    # Print input/output dimension details
    try:
        for inp in graph.input:
            dims = [dim.dim_value for dim in inp.type.tensor_type.shape.dim]
            print(f"Input {inp.name} shape: {dims}")
        for out in graph.output:
            dims = [dim.dim_value for dim in out.type.tensor_type.shape.dim]
            print(f"Output {out.name} shape: {dims}")
    except Exception:
        print("Couldn't parse input/output shapes.")

    # Print the total number and names of initializers (parameters)
    print(f"Number of initializers (weight/bias tensors): {len(graph.initializer)}")
    # List the initializer names/sizes
    # for init in graph.initializer:
    #     print(f"{init.name}: shape {init.dims}")

def main():
    for filename in sorted(os.listdir(ONNX_DIR)):
        if filename.endswith('.onnx'):
            model_path = os.path.join(ONNX_DIR, filename)
            try:
                analyze_onnx_model(model_path)
            except Exception as e:
                print(f"Error loading {filename}: {e}")

if __name__ == '__main__':
    main()
