#!/bin/bash
#SBATCH --job-name=smt_bitwuzla_9
#SBATCH --output=smt_bitwuzla.out
#SBATCH --error=smt_bitwuzla.err
#SBATCH --time=26:00:00       # hh:mm:ss
#SBATCH --partition=himem     # Switch to himem for high memory and idle nodes
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=8     # 8 cores for headroom (adjust to 4 if mem is low)
#SBATCH --mem=64G             # Safe for himem; increase to 128G if needed
#SBATCH --mail-type=ALL
#SBATCH --mail-user=asu.kaur@postgrad.manchester.ac.uk


# Go to the directory containing the script
cd $HOME/asukaur/benchmark/benchconvert/verifiers


# Log start time and mark the beginning of the job
echo "Job started at: $(date)"
start_time=$(date +%s)

python run_smt.py bitwuzla 9

# Log end time and calculate duration
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "Job ended at: $(date)"
echo "Total job runtime: $duration seconds"
