#!/bin/bash
#SBATCH --job-name=sv_cbmc_6
#SBATCH --output=sv_cbmc_6.out
#SBATCH --error=sv_cbmc_6.err
#SBATCH --time=26:00:00       # hh:mm:ss
#SBATCH --partition=himem  # For symbolic execution memory
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=1
#SBATCH --mem=64G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=asu.kaur@postgrad.manchester.ac.uk

# Go to the directory containing the script
cd $HOME/asukaur/benchmark/benchconvert/verifiers

# Log start time and mark the beginning of the job
echo "Job started at: $(date)"
start_time=$(date +%s)

python run_sv.py cbmc 6

# Log end time and calculate duration
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "Job ended at: $(date)"
echo "Total job runtime: $duration seconds"

