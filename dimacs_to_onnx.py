# The file is taken from https://github.com/emanino/neurocodebench

# This module converts CNF (Conjunctive Normal Form) boolean satisfiability problems 
# into neural networks. The networks are designed to work with pre-segregated DIMACS files
# that are already classified as SAT or UNSAT.

# The neural network uses specific weight/bias patterns to process boolean logic:
# - OR operations use ReLU activations with clause-specific encoding
# - AND operations use weighted summation in the output layer  
# - Variable assignments become network inputs

# The resulting neural network outputs two scores that can be interpreted based on 
# the training data distribution from pre-classified SAT/UNSAT instances.

# MATHEMATICAL FOUNDATION:
# =======================
# CNF Formula: (x₁ ∨ ¬x₂ ∨ x₃) ∧ (¬x₁ ∨ x₂) ∧ (x₂ ∨ x₃)

# Neural Network Architecture:
# 1. Each clause becomes a weighted sum with ReLU activation
# 2. Output layer combines all clause outputs with learned weights
# 3. Two output neurons provide classification scores

# OR Gate Implementation:
# For clause (x₁ ∨ ¬x₂ ∨ x₃):
# - Weight matrix: [-1, 1, -1] (negative for positive literals, positive for negated literals)
# - Bias: 1 - (number of negated literals) = 1 - 1 = 0
# - ReLU(−x₁ + x₂ − x₃ + 0) creates a feature for this clause

# AND Gate Implementation:
# - Combines clause features using learned weights (initially negative)
# - Bias adjustment allows for threshold-based classification
# - Final output depends on training with SAT/UNSAT labeled data


import csv 
import numpy as np
import torch

def weak_dimacs_parser(filepath):
    # Parse a DIMACS CNF file and extract the boolean formula.
    
    # DIMACS format specification:
    # - Comment lines start with 'c'
    # - Problem line: 'p cnf <num_vars> <num_clauses>'
    # - Clause lines: space-separated literals ending with '0'
    # - Positive integers = variables, negative integers = negated variables
    
    # Example DIMACS file:
    # c This is a comment
    # p cnf 3 2
    # 1 -2 0
    # -1 3 0
    
    # This represents: (x₁ ∨ ¬x₂) ∧ (¬x₁ ∨ x₃)
    
    # Args:
    #     filepath (str): Path to the DIMACS file (assumed to be pre-classified as SAT/UNSAT)
        
    # Returns:
    #     tuple: (info_dict, cnf_list) where:
    #         - info_dict contains metadata ('vars', 'clauses')
    #         - cnf_list contains clauses as lists of integers

    info = {}  # Dictionary to store metadata (number of variables and clauses)
    cnf = []   # List to store clauses, each clause is a list of literals
    
    with open(filepath, "r") as csvfile:
        # Use space delimiter to parse DIMACS format
        csvreader = csv.reader(csvfile, delimiter=' ')
        
        for row in csvreader:
            # Skip empty rows that might occur due to formatting
            if not row or not row[0]:
                continue
                
            # Skip comment lines
            if row[0] == "c":
                continue
            
            # Parse metadata line, e.g. "p cnf 3 2"
            # Format: p <format> <variables> <clauses>
            elif row[0] == "p":
                assert(row[1] == "cnf") # Only CNF format supported 
                assert(len(row) == 4)   # Must have exactly 4 elements: p, cnf, vars, clauses
                
                info["vars"] = int(row[2])     # Number of boolean variables in the formula
                info["clauses"] = int(row[3])  # Number of clauses in the formula
            
            # Parse clause lines
            # Each clause is a disjunction (OR) of literals
            else:
                assert(row[-1] == "0") # DIMACS clauses must end with '0' as terminator
                
                # Convert string literals to integers, excluding the terminal '0'
                # Filter out empty strings that might occur from extra spaces
                clause = [int(elem) for elem in row[:-1] if elem]
                cnf.append(clause)
    
    return info, cnf

def cnf_to_nn_params(info, cnf):
    # Convert a CNF formula into neural network parameters.
    
    # The neural network architecture creates features from CNF clauses:
    
    # Input Layer: Boolean variables (0 or 1, or continuous values during training)

    # Hidden Layer: Three components stacked vertically
    # │ ├─ Clause features (one per clause) - weighted combinations of literals
    # │ ├─ Pass-through (identity for variables) - preserves original variable values
    # │ └─ Nonlinearity features (based on 2x-1 transform) - captures variable interactions
    
    # ReLU activation

    # Output Layer: Two neurons
    # │ ├─ Classification score - combines clause features for SAT/UNSAT prediction
    # │ └─ Auxiliary score - combines variable and nonlinearity features
    
    # Mathematical formulation:
    
    # CLAUSE FEATURE DESIGN:
    # For clause (x₁ ∨ ¬x₂ ∨ x₃), create feature ReLU(−x₁ + x₂ − x₃ + bias) where:
    # - Positive literals get weight -1
    # - Negated literals get weight +1  
    # - Bias = 1 - (number of negated literals)
    
    # CLASSIFICATION LAYER DESIGN:
    # Initially combines clause features with negative weights and positive bias.
    # During training with SAT/UNSAT labeled data, these weights adjust to learn
    # the correct classification boundaries.
    
    # Args:
    #     info (dict): Metadata from DIMACS parser containing 'vars' and 'clauses'
    #     cnf (list): List of clauses from DIMACS parser, each clause is list of literals
        
    # Returns:
    #     tuple: (W_1, b_1, W_2, b_2) - initial weights and biases for 2-layer network
    #         W_1: First layer weight matrix [hidden_size, input_size]
    #         b_1: First layer bias vector [hidden_size]
    #         W_2: Second layer weight matrix [output_size, hidden_size]  
    #         b_2: Second layer bias vector [output_size]
    
    n_var = info["vars"]      # Number of boolean variables
    n_clause = info["clauses"] # Number of clauses
    
    # Sanity check: number of parsed clauses should match metadata
    assert(len(cnf) == n_clause)
    
    # ===== LAYER 1 COMPONENT 1: CLAUSE FEATURES =====
    # Each row creates a feature from one clause
    # Weight matrix encodes literal patterns within clauses
    
    # Initialize weight and bias matrices for clause feature layer
    W_or = np.zeros([n_clause, n_var])  # Shape: [#clauses, #variables]
    b_or = np.zeros(n_clause)           # Bias for each clause feature
    
    # Process each clause to create corresponding feature
    for i in range(n_clause):
        clause = np.array(cnf[i])  # Convert clause to numpy array for easier manipulation
        
        # Convert DIMACS 1-based indexing to 0-based Python indexing
        # DIMACS uses 1,2,3,... for variables, Python uses 0,1,2,...
        pos_ids = clause[clause > 0] - 1  # Positive literals: x₁, x₂, etc.
        neg_ids = -clause[clause < 0] - 1  # Negated literals: ¬x₁, ¬x₂, etc.
        
        # Clause feature encoding using specific weight pattern
        # Mathematical form: ReLU(∑(-w_i * x_i) + bias)
        # 
        # For clause (x₁ ∨ ¬x₂ ∨ x₃):
        # - Positive literals get weight -1 
        # - Negated literals get weight +1 
        # - Bias = 1 - (number of negated literals)
        
        W_or[i, pos_ids] = -1  # Weights for positive literals
        W_or[i, neg_ids] = 1   # Weights for negated literals  
        b_or[i] = 1 - len(neg_ids)  # Bias adjustment based on negated literal count
    
    # ===== LAYER 1 COMPONENT 2: PASS-THROUGH =====
    # Identity matrix to pass variables unchanged to next layer
    # This allows the output layer to access original variable values
    # for direct variable-based features and constraints
    
    W_pass = np.eye(n_var)    # n_var × n_var identity matrix
    b_pass = np.zeros(n_var)  # No bias needed for identity transformation
    
    # ===== LAYER 1 COMPONENT 3: NONLINEARITY FEATURES =====
    # Create additional features based on 2x-1 transformation
    # These capture nonlinear variable interactions
    
    # For each variable x, create feature: ReLU(2x - 1)
    # This transformation creates features that activate differently
    # for different variable value ranges

    # These features can be used by the output layer to detect
    # variable value patterns and constraints
    
    W_down = 2 * np.eye(n_var)  # Weight matrix: 2 on diagonal, 0 elsewhere
    b_down = -np.ones(n_var)    # Bias vector: -1 for each variable
    
    # ===== COMBINE LAYER 1 COMPONENTS =====
    # Stack all three components vertically to create the full first layer
    # The hidden layer structure:
    # [indices 0 to n_clause-1]: Clause features
    # [indices n_clause to n_clause+n_var-1]: Variable pass-through  
    # [indices n_clause+n_var to end]: Nonlinearity features
    
    W_1 = np.vstack([W_or, W_pass, W_down])        # Vertical stack of weight matrices
    b_1 = np.concatenate([b_or, b_pass, b_down])   # Concatenate bias vectors
    
    # Total hidden layer size: n_clause + n_var + n_var = n_clause + 2*n_var
    
    # ===== LAYER 2: OUTPUT CLASSIFICATION =====
    # The output layer combines hidden layer features to produce classification scores
    # Two output neurons provide different types of information
    
    n_hidden = len(b_1)  # Total number of hidden units
    W_2 = np.zeros([2, n_hidden])  # 2 output neurons, n_hidden inputs
    b_2 = np.zeros(2)              # Bias for each output neuron
    
    # OUTPUT NEURON 0: PRIMARY CLASSIFICATION SCORE
    # Combines clause features using initially negative weights
    # The network learns appropriate weights during training with SAT/UNSAT data
    # 
    # Initial configuration uses negative weights on clause features:
    # Score = -clauseFeature₁ - clauseFeature₂ - ... + bias
    # This creates an initial scoring function that training can refine
    
    W_2[0, :n_clause] = -1  # Initial negative weights for clause features
    b_2[0] = 1              # Initial positive bias
    
    # During training, these weights will adjust to learn the correct mapping
    # from clause feature activations to SAT/UNSAT classification
    
    # OUTPUT NEURON 1: AUXILIARY SCORE
    # Combines variable pass-through and nonlinearity features
    
    # Pass-through section: indices [n_clause : n_clause+n_var]
    # Nonlinearity section: indices [n_clause+n_var : n_clause+2*n_var]
    
    W_2[1, n_clause:n_clause+n_var] = 1     # Positive weights on pass-through
    W_2[1, n_clause+n_var:n_hidden] = -1    # Negative weights on nonlinearity features
    b_2[1] = 0                               # No initial bias
    
    # This creates an auxiliary score:
    # Score = ∑(x_i) - ∑(ReLU(2x_i - 1))
    # 
    # The behavior depends on variable values:
    # - Binary variables (x_i ∈ {0,1}): different contributions based on value
    
    return (W_1, b_1, W_2, b_2)

def nn_params_to_torch(W_1, b_1, W_2, b_2):
    # Convert numpy weight matrices into a PyTorch neural network.
    
    # Creates a 2-layer feedforward network with ReLU activation:
    # - Layer 1: Linear transformation + ReLU activation
    # - Layer 2: Linear transformation (no activation for raw classification scores)
    
    # The network processes CNF formulas by creating features from clauses and variables.
    
    # Network usage patterns:
    # 1. Training: Use labeled SAT/UNSAT instances to learn classification weights
    # 2. Inference: Input variable assignments to get classification scores
    # 3. Optimization: Use gradients to find variable assignments that maximize scores
    
    # Args:
    #     W_1, b_1 (numpy.ndarray): First layer weights and biases
    #         W_1 shape: [hidden_size, input_size] where input_size = number of variables
    #         b_1 shape: [hidden_size]
    #     W_2, b_2 (numpy.ndarray): Second layer weights and biases  
    #         W_2 shape: [2, hidden_size] (2 outputs: primary score, auxiliary score)
    #         b_2 shape: [2]
        
    # Returns:
    #     torch.nn.Sequential: Neural network ready for training/inference with SAT/UNSAT data
    
    # Create layer objects with appropriate dimensions
    # Input dimension: number of boolean variables
    # Hidden dimension: number of clause features + 2*(number of variables)
    # Output dimension: 2 (primary classification score, auxiliary score)
    
    layer_1 = torch.nn.Linear(W_1.shape[1], W_1.shape[0])  # Input to hidden layer
    activ_1 = torch.nn.ReLU()                              # ReLU activation for feature creation
    layer_2 = torch.nn.Linear(W_2.shape[1], W_2.shape[0])  # Hidden to output layer
    
    # Initialize weights and biases with our computed initial values
    # PyTorch requires gradients to be disabled during parameter initialization
    with torch.no_grad():
        # PyTorch Linear layers expect (out_features, in_features) weight shape
        layer_1.weight = torch.nn.Parameter(torch.Tensor(W_1))
        layer_1.bias = torch.nn.Parameter(torch.Tensor(b_1))
        
        layer_2.weight = torch.nn.Parameter(torch.Tensor(W_2))
        layer_2.bias = torch.nn.Parameter(torch.Tensor(b_2))
    
    # Assemble the complete network pipeline
    # Sequential container applies layers in order: input → linear → ReLU → linear → output
    net = torch.nn.Sequential(layer_1, activ_1, layer_2).to("cpu")
    
    return net

def write_torch_to_onnx_file(net, filepath):
    # Export a PyTorch neural network to ONNX format.
    
    # Args:
    #     net (torch.nn.Sequential): The trained neural network to export
    #     filepath (str): Output path for the ONNX file (should end in .onnx)
 
    
    # Create a dummy input tensor for tracing the network computation graph
    # Shape: (batch_size, n_variables) where batch_size=1 for example
    
    n = net[0].weight.shape[1]  # Number of input features (boolean variables)
    x = torch.zeros(1, n)       # Example input: single instance, all variables set to 0
    
    # Export the network with computation graph tracing
    torch.onnx.export(
        net,                    # The trained model to export
        x,                      # Example input tensor (used for tracing operations)
        filepath,               # Output file path
        verbose=True,           # Print conversion details for debugging
    )
    
