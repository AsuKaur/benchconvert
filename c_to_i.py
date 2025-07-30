import os
import subprocess

# Directory paths for inputs and outputs
c_network_dir = 'c_network'
c_prop_dir = 'c_prop'
extern_dir = 'extern'
preprocessed_dir = 'c_preprocessed'

# Ensure output directory exists
os.makedirs(preprocessed_dir, exist_ok=True)

def preprocess_and_combine():
    """
    Preprocess C source files from c_network directory, optionally append
    corresponding property file content, and save combined output as .i files.

    Steps:
    1. For each C file in c_network:
       - Run the C preprocessor (gcc -E) including extern folder for headers.
    2. Read the matching .prop file from c_prop if it exists.
    3. Append the property content as a C-style comment to the preprocessed C code.
    4. Write the combined content into a single .i file in the preprocessed folder.

    This prepares files suitable for verification tools that require
    preprocessed C source and related property info in one place.

    Note:
    - This approach merges the property file content into the .i file as comments.
    - Ensure the .c files include the helper header verifier_function.h from extern.
    """

    # Iterate over all files in the c_network directory
    for filename in os.listdir(c_network_dir):
        # Process only C source files
        if not filename.endswith('.c'):
            continue

        # Get base filename without extension (e.g., "file" from "file.c")
        base_name = os.path.splitext(filename)[0]

        # Construct full paths for C file, property file, and output file
        c_file_path = os.path.join(c_network_dir, filename)
        prop_file_path = os.path.join(c_prop_dir, base_name + '.prop')
        output_i_path = os.path.join(preprocessed_dir, base_name + '.i')

        print(f"Processing {filename}...")

        # Step 1: Preprocess the C file using gcc -E with extern include path
        cmd = ['gcc', '-E', '-I', extern_dir, c_file_path]
        try:
            # Run command and capture the preprocessed C code output
            completed = subprocess.run(cmd, check=True, capture_output=True, text=True)
            preprocessed_c_content = completed.stdout
        except subprocess.CalledProcessError as e:
            print(f"Error preprocessing {filename}: {e}")
            continue

        # Step 2: Read .prop file if it exists and prepare it as a comment block
        prop_content = ""
        if os.path.exists(prop_file_path):
            with open(prop_file_path, 'r') as prop_file:
                prop_content = prop_file.read()
            # Wrap property content inside a multiline C comment
            prop_content = "\n/*\nProperty file content:\n" + prop_content + "\n*/\n"
        else:
            print(f"Warning: No property file found for {filename}")

        # Step 3: Write combined content into the output .i file
        with open(output_i_path, 'w') as out_file:
            out_file.write(preprocessed_c_content)
            out_file.write(prop_content)

        print(f"Saved combined .i file: {output_i_path}")

if __name__ == '__main__':
    preprocess_and_combine()
