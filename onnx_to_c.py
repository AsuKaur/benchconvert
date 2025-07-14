
# ONNX to C Converter Script using onnx2c

# This script converts ONNX model files to C source code using the onnx2c tool.

# Folder Structure:
#     onnx/           - Input ONNX model files
#     c_network/      - Output C source files

# Usage:
#     python onnx_to_c.py <onnx_filename>           # Convert single file
#     python onnx_to_c.py --all                     # Convert all ONNX files


import sys
import os
import argparse
import subprocess
from pathlib import Path
import shutil
import onnx

ONNX_DIR = Path("onnx")
C_NETWORK_DIR = Path("c_network")


def check_onnx2c_executable():
    # Check if onnx2c executable is available.
    
    # Returns:
    #    str: Path to onnx2c executable if found, None otherwise

    # Check in current directory first
    local_onnx2c = Path("./onnx2c")
    if local_onnx2c.exists() and local_onnx2c.is_file():
        return str(local_onnx2c)
    
    # Check in PATH
    onnx2c_path = shutil.which("onnx2c")
    if onnx2c_path:
        return onnx2c_path
    
    # Check common build locations
    build_paths = [
        "./onnx2c/build/onnx2c",
        "../onnx2c/build/onnx2c",
        "./build/onnx2c"
    ]
    
    for path in build_paths:
        if Path(path).exists():
            return str(Path(path).resolve())
    
    return None


def setup_directories():
    # Ensure required directories exist.
    
    # Returns:
    #     tuple: (onnx_dir, c_network_dir) paths

    onnx_dir = ONNX_DIR
    c_network_dir = C_NETWORK_DIR
    
    # Create directories if they don't exist
    onnx_dir.mkdir(exist_ok=True)
    c_network_dir.mkdir(exist_ok=True)
    
    return onnx_dir, c_network_dir


def validate_onnx_model(onnx_path):
    # Validate that the ONNX model is well-formed and supported.
    
    # Args:
    #     onnx_path (str): Path to the ONNX model file
        
    # Returns:
    #     bool: True if model is valid, False otherwise

    try:
        # Load the ONNX model
        model = onnx.load(onnx_path)
        
        # Check if the model is valid
        onnx.checker.check_model(model)
        
        print(f"✓ ONNX model validation passed: {onnx_path}")
        
        # Print model info
        print(f"  - IR version: {model.ir_version}")
        print(f"  - Producer: {model.producer_name} {model.producer_version}")
        print(f"  - Graph inputs: {len(model.graph.input)}")
        print(f"  - Graph outputs: {len(model.graph.output)}")
        print(f"  - Graph nodes: {len(model.graph.node)}")
        
        return True
        
    except Exception as e:
        print(f"✗ ONNX model validation failed: {e}")
        return False


def convert_onnx_to_c(onnx_filename, onnx_dir, c_network_dir, onnx2c_path):
    # Convert ONNX model to C source code using onnx2c.
    
    # Args:
    #     onnx_filename (str): Name of the ONNX file (without path)
    #     onnx_dir (Path): Path to onnx directory
    #     c_network_dir (Path): Path to c_network directory
    #     onnx2c_path (str): Path to onnx2c executable
        
    # Returns:
    #     bool: True if conversion successful, False otherwise

    # Construct full paths
    onnx_path = onnx_dir / onnx_filename
    
    # Validate input file exists
    if not onnx_path.exists():
        print(f"Error: Input file not found: {onnx_path}")
        return False
    
    # Generate output filename
    input_stem = onnx_path.stem
    output_path = c_network_dir / f"{input_stem}.c"
    
    # Validate ONNX model first
    if not validate_onnx_model(str(onnx_path)):
        return False
    
    try:
        print(f"Converting {onnx_path} to {output_path}...")
        
        # Run onnx2c command
        # Usage: ./onnx2c [options] model.onnx > output.c
        with open(output_path, 'w') as output_file:
            result = subprocess.run(
                [onnx2c_path, str(onnx_path)],
                stdout=output_file,
                stderr=subprocess.PIPE,
                text=True,
                timeout=300  # 5 minute timeout
            )
        
        if result.returncode != 0:
            print(f"✗ onnx2c failed with return code {result.returncode}")
            if result.stderr:
                print(f"Error output: {result.stderr}")
            return False
        
        # Check if output file was created and has content
        if not output_path.exists() or output_path.stat().st_size == 0:
            print(f"✗ Output file was not created or is empty: {output_path}")
            return False
        
        print(f"✓ Successfully converted to C: {output_path}")
        print(f"  - Output file size: {output_path.stat().st_size} bytes")
        
        # Print any warnings from stderr
        if result.stderr:
            print(f"  - Warnings: {result.stderr.strip()}")
        
        return True
        
    except subprocess.TimeoutExpired:
        print(f"✗ Conversion timed out after 5 minutes")
        return False
    except Exception as e:
        print(f"✗ Conversion failed: {e}")
        print(f"Error type: {type(e).__name__}")
        return False


def convert_all_onnx_files(onnx_dir, c_network_dir, onnx2c_path):
    # Convert all ONNX files in the onnx directory.
    
    # Args:
    #     onnx_dir (Path): Path to onnx directory
    #     c_network_dir (Path): Path to c_network directory
    #     onnx2c_path (str): Path to onnx2c executable
        
    # Returns:
    #     tuple: (success_count, total_count)

    # Find all ONNX files
    onnx_files = list(onnx_dir.glob("*.onnx"))
    
    if not onnx_files:
        print(f"No ONNX files found in {onnx_dir}")
        return 0, 0
    
    print(f"Found {len(onnx_files)} ONNX files to convert:")
    for f in onnx_files:
        print(f"  - {f.name}")
    print()
    
    success_count = 0
    total_count = len(onnx_files)
    
    for onnx_file in onnx_files:
        print(f"Processing {onnx_file.name}...")
        if convert_onnx_to_c(onnx_file.name, onnx_dir, c_network_dir, onnx2c_path):
            success_count += 1
            print("Moving on....")
    
    return success_count, total_count


def list_files_in_directories():
    # List files in both onnx and c_network directories.
    onnx_dir, c_network_dir = setup_directories()
    
    print("Current directory structure:")
    print(f"\n📁 {onnx_dir}/ (ONNX input files):")
    onnx_files = list(onnx_dir.glob("*.onnx"))
    if onnx_files:
        for f in onnx_files:
            print(f"  📄 {f.name}")
    else:
        print("  (empty - place your .onnx files here)")
    
    print(f"\n📁 {c_network_dir}/ (C output files):")
    c_files = list(c_network_dir.glob("*.c"))
    if c_files:
        for f in c_files:
            print(f"  📄 {f.name}")
    else:
        print("  (empty - converted files will appear here)")
    print()


def main():
    # Main function to handle command line arguments and execute conversion.
    parser = argparse.ArgumentParser(
        description="Convert ONNX models to C source code using onnx2c",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Directory Structure:
  onnx/           - Place your ONNX model files here
  c_network/      - Generated C files will be saved here
  onnx2c          - The onnx2c executable (build separately)

Examples:
  python onnx_to_c.py model.onnx        # Convert onnx/model.onnx -> c_network/model.c
  python onnx_to_c.py --all             # Convert all ONNX files in onnx/ folder
  python onnx_to_c.py --list            # List files in both directories
  python onnx_to_c.py --validate model.onnx  # Only validate model
        """
    )
    
    # Main argument group
    group = parser.add_mutually_exclusive_group()
    
    group.add_argument(
        'onnx_file',
        nargs='?',
        help='Name of ONNX file in onnx/ directory (e.g., model.onnx)'
    )
    
    group.add_argument(
        '--all',
        action='store_true',
        help='Convert all ONNX files in onnx/ directory'
    )
    
    group.add_argument(
        '--list',
        action='store_true',
        help='List files in onnx/ and c_network/ directories'
    )
    
    parser.add_argument(
        '--validate',
        action='store_true',
        help='Only validate the ONNX model without converting'
    )
    
    parser.add_argument(
        '--verbose',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--onnx2c-path',
        type=str,
        help='Path to onnx2c executable (if not in current directory or PATH)'
    )
    
    args = parser.parse_args()
    
    # Setup directories
    onnx_dir, c_network_dir = setup_directories()
    
    # Set verbosity
    if args.verbose:
        print("Verbose mode enabled")
    
    # List files mode
    if args.list:
        list_files_in_directories()
        return 0
    
    # Check for onnx2c executable
    onnx2c_path = args.onnx2c_path or check_onnx2c_executable()
    if not onnx2c_path:
        print("❌ onnx2c executable not found!")
        print("\nonnx2c is required but not installed or not in PATH.")
        return 1
    
    print(f"Using onnx2c: {onnx2c_path}")
    
    # Validate only mode
    if args.validate and args.onnx_file:
        onnx_path = onnx_dir / args.onnx_file
        if validate_onnx_model(str(onnx_path)):
            print("Model validation completed successfully")
            return 0
        else:
            print("Model validation failed")
            return 1
    
    # Convert all files mode
    if args.all:
        print("Converting all ONNX files...")
        success_count, total_count = convert_all_onnx_files(onnx_dir, c_network_dir, onnx2c_path)
        
        print(f"\nConversion Summary:")
        print(f"  ✓ Successful: {success_count}")
        print(f"  ✗ Failed: {total_count - success_count}")
        print(f"  📊 Total: {total_count}")
        
        return 0 if success_count == total_count else 1
    
    # Convert single file mode
    if args.onnx_file:
        success = convert_onnx_to_c(args.onnx_file, onnx_dir, c_network_dir, onnx2c_path)
        
        if success:
            print("\n✓ Conversion completed successfully!")
            print(f"Generated files are in: {c_network_dir}")
            return 0
        else:
            print("\n✗ Conversion failed!")
            return 1
    
    # No arguments provided
    parser.print_help()
    return 1


if __name__ == "__main__":
    sys.exit(main())