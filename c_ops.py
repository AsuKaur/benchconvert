# Convert C files from c_network and c_prop directories into combined .c files,
# then preprocess them using gcc to generate .i files.

import os
import subprocess

C_NETWORK_DIR = 'c_network'           # Original network source files
C_PROP_DIR = 'c_prop'                 # Property files prefixed with "prop_"
EXTERN_DIR = 'extern'                 # Headers for preprocessing
COMBINED_C_DIR = 'c'                  # Directory to save combined .c files
PREPROCESSED_DIR = 'c_preprocessed'   # Directory to save preprocessed .i files

# Ensure output directories exist
os.makedirs(COMBINED_C_DIR, exist_ok=True)
os.makedirs(PREPROCESSED_DIR, exist_ok=True)

def combine_files():
    # Combine .c files from c_prop and c_network directories.
    # For each file in c_network, find corresponding `prop_` prefixed file in c_prop.
    # Combine: property file content first, then network file content.
    # Save combined file in 'c' directory.
    for network_filename in os.listdir(C_NETWORK_DIR):
        if not network_filename.endswith('.c'):
            continue

        prop_filename = "prop_" + network_filename  

        network_c_path = os.path.join(C_NETWORK_DIR, network_filename)
        prop_c_path = os.path.join(C_PROP_DIR, prop_filename)
        combined_c_path = os.path.join(COMBINED_C_DIR, network_filename)  

        # Read property C content if it exists
        prop_c_content = ""
        if os.path.exists(prop_c_path):
            with open(prop_c_path, 'r') as f_prop:
                prop_c_content = f_prop.read()
        else:
            print(f"Property .c file '{prop_filename}' not found in '{C_PROP_DIR}'")

        # Read network C content
        try:
            with open(network_c_path, 'r') as f_net:
                network_c_content = f_net.read()
        except Exception as e:
            print(f"Error reading network file '{network_filename}': {e}")
            continue

        combined_content = (
            f"// Combined source of '{network_filename}' from '{prop_filename}' and '{network_filename}'\n\n"
            + prop_c_content
            + "\n\n// Network source \n\n"
            + network_c_content
        )

        # Write combined content
        with open(combined_c_path, 'w') as f_combined:
            f_combined.write(combined_content)

        print(f"Combined .c file saved: {combined_c_path}")

def preprocess_combined_files():
    # Preprocess combined .c files from the 'c' directory using gcc -E.
    # Save the preprocessed output as .i files in 'c_preprocessed'.
    for filename in os.listdir(COMBINED_C_DIR):
        if not filename.endswith('.c'):
            continue

        combined_c_path = os.path.join(COMBINED_C_DIR, filename)
        base_name = os.path.splitext(filename)[0]
        output_i_path = os.path.join(PREPROCESSED_DIR, base_name + '.i')

        print(f"Preprocessing {filename}")

        cmd = ['gcc', '-E', '-I', EXTERN_DIR, combined_c_path]

        try:
            completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
            preprocessed_content = completed.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error preprocessing '{filename}': {e}")
            continue

        with open(output_i_path, 'w') as f_out:
            f_out.write(preprocessed_content)

        print(f"Preprocessed .i file saved: {output_i_path}")

def main():
    print("Starting combination of c_network and c_prop files")
    combine_files()
    print("\nStarting preprocessing of combined files in 'c' directory")
    preprocess_combined_files()

if __name__ == '__main__':
    main()
