import os
import subprocess

# Define the folder path
jobs_folder = 'jobs'

# Get a list of all .slurm files in the jobs folder
files = [f for f in os.listdir(jobs_folder) if os.path.isfile(os.path.join(jobs_folder, f)) and f.endswith('.slurm')]

# Sort the files alphabetically (optional, for consistent order)
files.sort()

# Run each .slurm file one by one using sbatch
for file in files:
    file_path = os.path.join(jobs_folder, file)
    print(f"Submitting {file_path} with sbatch...")
    try:
        # Run sbatch on the file
        result = subprocess.run(['sbatch', file_path], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"Successfully submitted {file}. Output:\n{result.stdout}")
        else:
            print(f"Error submitting {file}. Error:\n{result.stderr}")
    except Exception as e:
        print(f"Failed to submit {file}: {str(e)}")
    print("-" * 40)  # Separator for clarity
