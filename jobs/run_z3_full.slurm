#!/bin/bash
#SBATCH --job-name=smt_z3_full
#SBATCH --output=smt_z3_full.out
#SBATCH --error=smt_z3_full.err
#SBATCH --time=26:00:00       # hh:mm:ss
#SBATCH --partition=multicore
#SBATCH --ntasks=1
#SBATCH --cpus-per-task=4
#SBATCH --mem=32G
#SBATCH --mail-type=ALL
#SBATCH --mail-user=asu.kaur@postgrad.manchester.ac.uk


# Log start time and mark the beginning of the job
echo "Job started at: $(date)"
start_time=$(date +%s)

# Define the input directory and results file
INPUT_DIR="$HOME/asukaur/benchmark/benchconvert/smt"
RESULTS_FILE="$HOME/asukaur/benchmark/benchconvert/results/z3_results.csv"

# Clear the results file if it exists, or create it
> "$RESULTS_FILE"

# Get Z3 version
z3_version=$(z3 -version 2>&1)

# Add solver and version to CSV
echo "Solver: z3" >> "$RESULTS_FILE"
echo "Version: $z3_version" >> "$RESULTS_FILE"

# Add CSV header
echo "File Name,Result,Runtime,Command" >> "$RESULTS_FILE"

# Collect and sort files by variable count then clause count
declare -a file_list
for file in "$INPUT_DIR"/*; do
    if [ -f "$file" ]; then
        var_count=$(grep -c '(declare-const\|(declare-fun' "$file")
        clause_count=$(grep -c '(assert ' "$file")
        file_list+=("$var_count $clause_count $file")
    fi
done

# Sort by var_count (numeric, field 1) then clause_count (numeric, field 2)
mapfile -t sorted_files < <(printf '%s\n' "${file_list[@]}" | sort -n -k1 -k2 | awk '{print substr($0, index($0,$3))}')

# Loop over sorted files
for file in "${sorted_files[@]}"; do
    filename=$(basename "$file")
    echo "Processing file: $filename"

    # Define the command
    command="z3 -smt2 \"$file\" memory_max_size=8589934592 timeout=900000"

    # Measure start time
    file_start_time=$(date +%s.%N)

    # Run the z3 command with external timeout and capture output
    result=$(timeout 900 z3 -smt2 "$file" memory_max_size=8589934592 timeout=900000 2>&1)
    status=$?

    # Measure end time and calculate duration
    file_end_time=$(date +%s.%N)
    duration=$(echo "$file_end_time - $file_start_time" | bc)
    runtime=$(printf "%.4f" "$duration")

    # Parse based on status
    if [ $status -eq 124 ]; then
        actual_result="TIMEOUT"
        runtime_str="900.0000s"
    elif [ $status -ne 0 ]; then
        result="${result//$'\n'/ }"
        escaped_result="${result//\"/\"\"}"
        actual_result="ERROR: $escaped_result"
        runtime_str="N/A"
    else
        parsed=$(echo "$result" | tr '[:upper:]' '[:lower:]' | grep -E '^(sat|unsat|unknown)$' | head -1 | tr '[:lower:]' '[:upper:]')
        actual_result=${parsed:-UNKNOWN}
        runtime_str="${runtime}s"
    fi

    # Escape actual_result for CSV (in case)
    escaped_actual="${actual_result//\"/\"\"}"

    # Append to results file as CSV row
    echo "\"$filename\",\"$escaped_actual\",\"$runtime_str\",\"$command\"" >> "$RESULTS_FILE"
done

# Log end time and calculate total duration
end_time=$(date +%s)
duration=$((end_time - start_time))
echo "Job ended at: $(date)"
echo "Total job runtime: $duration seconds"
echo "Results stored in: $RESULTS_FILE"
