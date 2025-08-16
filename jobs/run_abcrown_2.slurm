#!/bin/bash
#SBATCH --job-name=vnn_abcrown
#SBATCH --output=vnn_abcrown.out
#SBATCH --error=vnn_abcrown.err
#SBATCH --time=26:00:00       # hh:mm:ss
#SBATCH --partition=gpuV      # GPU partition; confirm availability with sinfo
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4     # For multi-threaded parts of ABCrown
#SBATCH --mem=46G             # Increased for FP/NN verification spikes
#SBATCH --gres=gpu:1          # Request 1 GPU; adjust to 2+ if needed (e.g., for multi-GPU runs)
#SBATCH --mail-type=ALL
#SBATCH --mail-user=asu.kaur@postgrad.manchester.ac.uk

# Go to the directory containing the script
cd $HOME/asukaur/benchmark/benchconvert/verifiers

# Log start time and mark the beginning of the job
echo "Job started at: $(date)"
start_time=$(date +%s)

python run_abcrown.py 2

# Log end time and calculate duration
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "Job ended at: $(date)"
echo "Total job runtime: $duration seconds"

