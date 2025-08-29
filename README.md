# BenchConvert: Cross-Format Neural Network Verification Benchmarks

BenchConvert is a toolset designed to provide cross-format benchmarks for neural network verification. It generates benchmarks starting from DIMACS format, converts them to ONNX and VNNLIB formats (compatible with VNN-COMP standards), and further translates them into formats suitable for software verifiers (e.g., C-based) and SMT solvers. This enables easy comparison and evaluation across different verification tools and formats. The pipeline also includes scripts to run various verifiers on these benchmarks and analyze results.

The benchmarks focus on neural network verification tasks, such as checking satisfiability (SAT/UNSAT) of properties on feedforward neural networks. BenchConvert supports conversion to multiple formats and evaluation using tools like SMT solvers (e.g., Bitwuzla), software verifiers (e.g., CBMC, ESBMC), and neural network-specific verifiers (e.g., Marabou, alpha-beta-CROWN).

## Features

-   Generate DIMACS benchmarks from predefined instances.
-   Convert DIMACS to ONNX models.
-   Generate VNNLIB properties for ONNX models.
-   Convert ONNX to C code for software verification (SV) tools.
-   Convert ONNX to SMT2 format for SMT solvers.
-   Run verifiers on the generated benchmarks and save results as CSV files.
-   Analyze ONNX model metrics (e.g., parameter counts, layer structures).
-   Preprocess and combine C files for verification.
-   Provide cross-format benchmarks for easy comparison across verification paradigms.
-   Generate graphs and statistics from verification results.

### 1. Generate Benchmarks

-   **Generate DIMACS files**: Run `python generate_dimacs.py` to create CNF files in the `dimacs`.
-   **Convert DIMACS to ONNX**: Run `python dimacs_to_onnx.py` to generate ONNX models in the `onnx` directory.
-   **Generate VNNLIB properties**: Run `python generate_vnnlib.py` to create property files in the `vnnlib` directory.
-   **Run entire workflow**: Run `python generate_properties_.py` to run the above scripts in the given order for genration of dimacs, onnx and vnnlib.

### 2. Convert to Other Formats

-   **Convert ONNX to C (for SV tools)**:

    -   Run `python onnx_to_c.py` to generate network C files in `c_network`.
    -   Run `python generate_c_prop.py` to generate property C files in `c_prop`.
    -   Run `python generate_c.py` to combine them into the above two and additionally generate combined and preprocessed c files.

-   **Convert ONNX to SMT2**: Run `python onnx_to_smt.py` (or `onnx_to_smt_real.py` for real arithmetic) to generate SMT files in the `smt` directory.

### 3. Run Verifiers

Scripts are located in the `verifiers` folder. Results are saved in CSV files in the `results` directory.

-   **SMT Solvers**: `python verifiers/run_smt.py <solver>` (e.g., `bitwuzla`, `z3`, `cvc5`). Runs on files in `smt`.
-   **Software Verifiers (SV)**: `python verifiers/run_sv.py <verifier>` (e.g., `cbmc` or `esbmc`). Runs on files in `c_prop` and `c_network`.
-   **VNN Verifiers**: `python verifiers/run_vnn.py <verifier>` (e.g., `marabou`). Runs on files in `onnx` and `vnnlib`.
-   **alpha-beta-CROWN**: `python verifiers/run_abcrown.py` (no arguments needed). Runs on files in `onnx` and `vnnlib`. Requires YAML config in `extern/abcrown.yaml`.

### 4. Analyze ONNX Models

-   Run `python helpers/onnx_metrics.py` to validate and print metrics (e.g., parameter counts, layers) for models in `onnx`.

### 5. Other Utilities

-   `diff_test.py`: Tests differences between formats or runs (usage: `python diff_test.py`).
-   `helpers/generate_graphs.py`: To generate graphs from the results and store it in the `graphs`.
-   `helpers/c_ops.py`: To convert c files to a combined and preprocessed c files (usage: `python c_ops.py`).
-   `app.py`: To run the entire workflow of generating dimacs conversion to onnx and vnnlib, onnx conversion to c and smt.

## Directory Structure

```
.
├── __pycache__                         # Python cache files
├── app.py                              # Main script
├── c                                   # Combined C files (network + properties)
├── c_network                           # Generated C network code from ONNX
├── c_preprocessed                      # Preprocessed .i files for SV tools
├── c_preprocessed_float32              # Preprocessed .i files for SV tools
├── c_prop                              # Generated C property files
├── diff_test.py                        # Script for testing differences
├── dimacs                              # Generated DIMACS CNF files
├── dimacs_to_onnx.py                   # Converts DIMACS to ONNX
├── extern                              # External headers/configs (e.g., abcrown.yaml and verifier_functions.h)
│   ├── abcrown.yaml
│   └── verifier_functions.h
├── generate_c_prop.py                  # Generates C properties
├── generate_c.py                       # Script to run ONNX to C conversion and other C operations
├── generate_dimacs.py                  # Generates DIMACS benchmarks
├── generate_properties.py              # Script to generate DIMACS, and convert to ONNX and VNNLIB files
├── generate_vnnlib.py                  # Generates VNNLIB files
├── graphs                              # Store generated graphs
│   ├── smt
│   ├── sv
│   └── vnn
├── helpers                             # Helper scripts/modules
│   ├── c_ops.py                         Script to generate combined and preprocessed C files
│   ├── conversion_stats.py
│   ├── generate_graphs.py
│   ├── onnx_metrics.py                 # Analyzes ONNX models
│   ├── parameter_count.py
│   └── sort_files.py
├── install.sh                          # Installation/setup script
├── instances.csv                       # CSV of benchmark instances
├── jobs                                # Jobs to run on HPC CSF3
├── LICENSE                             # License file
├── onnx                                # Generated ONNX models
├── onnx_to_c.py                        # Converts ONNX to C
├── onnx_to_smt_real.py                 # Converts ONNX to SMT (real arithmetic)
├── onnx_to_smt.py                      # Converts ONNX to SMT
├── README.md
├── results                             # CSV results from verifiers
├── smt                                 # Generated SMT2 files
├── verifiers                           # Verifier runner scripts (e.g., run_smt.py, run_sv.py, run_vnn.py, run_abcrown.py)
│   ├── run_abcrown.py
│   ├── run_smt.py
│   ├── run_sv.py
│   └── run_vnn.py
└── vnnlib                              # Generated VNNLIB property files
```

## License

This project is licensed under the terms in `LICENSE` (e.g., MIT License). See the file for details.
