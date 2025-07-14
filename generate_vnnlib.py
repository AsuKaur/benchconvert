# The file is taken from https://github.com/emanino/neurocodebench

def vnnlib_lines(n_var, verdict):
    # Generate VNNLIB format lines for neural network verification.
    
    # VNNLIB is a standard format used for specifying neural network verification
    # problems. It uses SMT-LIB syntax to define input/output variables and constraints.
    
    # Args:
    #     n_var (int): Number of input variables (X_0, X_1, ..., X_{n_var-1})
    #     verdict (str): Expected satisfiability result, either "SAT" or "UNSAT"
    #                   - SAT: There exists an input that satisfies all constraints
    #                   - UNSAT: No input can satisfy all constraints simultaneously
    
    # Returns:
    #     list: List of strings representing lines in VNNLIB format

    lines = []
    
    # Initial comment line "; NeuroCodeBench 2.0: 
    # SAT ReLU instance with <variables> and <clause>"
    lines.append("; NeuroCodeBench 2.0: SAT ReLU instance with " +
                 str(n_var) + " variables and " + verdict + " verdict")
    lines.append("")  # Empty line for readability
    
    # Variables must be explicitly declared before use.
    # Input variables represent the neural network's input layer.
    # Each variable X_i corresponds to one input neuron/feature.
    lines.append("; Input Variables")
    for i in range(n_var):
        # SMT-LIB syntax: (declare-const <name> <type>)
        lines.append("(declare-const X_" + str(i) + " Real)")
    lines.append("")  # Separator for readability
    
    # Output variables represent the neural network's final layer outputs.
    # This example assumes a binary classification network with 2 output neurons.
    # Y_0 and Y_1 typically represent confidence scores or logits for each class.
    lines.append("; Output Variables")
    lines.append("(declare-const Y_0 Real)")  # Output neuron 0 
    lines.append("(declare-const Y_1 Real)")  # Output neuron 1
    lines.append("")
    
    # Define the valid input space by constraining each input variable.
    lines.append("; Input Constraints")
    for i in range(n_var):
        # Upper bound: X_i <= 1.0 (input cannot exceed 1.0)
        lines.append("(assert (<= X_" + str(i) + " 1.0))")
        # Lower bound: X_i >= 0.0 (input cannot be negative)
        lines.append("(assert (>= X_" + str(i) + " 0.0))")
    lines.append("")
    
    # Define the property we want to verify about the network's behavior.
    lines.append("; Output Constraints")
    
    # Y_0 >= 1.0: First output must be at least 1.0
    lines.append("(assert (>= Y_0 1.0))")
    
    # Y_1 <= 0.0: Second output must be at most 0.0  
    # Combined with above: we want Y_0 high AND Y_1 low
    lines.append("(assert (<= Y_1 0.0))")
    
    return lines

