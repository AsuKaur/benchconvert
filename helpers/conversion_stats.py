import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path


SCRIPT_DIR = Path(__file__).parent
RESULTS_DIR = SCRIPT_DIR.parent / "results"
GRAPHS_DIR = SCRIPT_DIR.parent / "graphs"

# Function to process the CSV files and generate a summary CSV with file counts and mean conversion times by size range.
# Parameters:
#   onnx_to_c_path: Path to the ONNX to C CSV file.
#   onnx_to_smt_path: Path to the ONNX to SMT CSV file.
#   output_csv: Path to save the output summary CSV (default: 'conversion_time_summary_by_size.csv').
# Returns: The summary DataFrame.
def process_conversion_times(onnx_to_c_path, onnx_to_smt_path, output_csv= GRAPHS_DIR / 'conversion_time_summary.csv'):
    # Load the data from the CSV files
    onnx_to_c = pd.read_csv(onnx_to_c_path)
    onnx_to_smt = pd.read_csv(onnx_to_smt_path)
    
    # Define a helper function to categorize parameter counts into size ranges
    def size_range(param_count):
        if param_count <= 10000:
            return 'Small'
        elif param_count <= 25000:
            return 'Medium'
        else:
            return 'Large'
    
    # Add the size range column to both DataFrames
    onnx_to_c['Size Range'] = onnx_to_c['Parameter Count'].apply(size_range)
    onnx_to_smt['Size Range'] = onnx_to_smt['Parameter Count'].apply(size_range)
    
    # Adjust the file names in the ONNX to SMT DataFrame to match the format in ONNX to C for merging
    onnx_to_smt['File Name'] = onnx_to_smt['File Name'].apply(lambda x: 'onnx/' + x + '.onnx')
    
    # Merge the two DataFrames on the 'File Name' column
    merged = pd.merge(onnx_to_c, onnx_to_smt, on='File Name', suffixes=('_onnx_to_c', '_onnx_to_smt'))
    
    # Create a unified 'Size Range' column (using the one from ONNX to C, as they should match)
    merged['Size Range'] = merged['Size Range_onnx_to_c']
    
    # Group by size range and calculate the number of files and mean conversion times
    summary = merged.groupby('Size Range').agg(
        Number_of_Files=('File Name', 'count'),
        Mean_Conversion_Time_ONNX_to_C=('Time Taken (s)_onnx_to_c', 'mean'),
        Mean_Conversion_Time_ONNX_to_SMT=('Time Taken (s)_onnx_to_smt', 'mean')
    ).reset_index()
    
    # Save the summary to the specified CSV file
    summary.to_csv(output_csv, index=False)
    
    return summary


# Function to generate a single linear (line) plot combining both conversion times vs. parameter counts.
# Parameters:
#   onnx_to_c: DataFrame containing ONNX to C data.
#   onnx_to_smt: DataFrame containing ONNX to SMT data.
# Saves the plot as 'combined_conversion_time_plot.png'.
def plot_conversion_times(onnx_to_c, onnx_to_smt):
    # Sort data by parameter count for smooth line plots
    onnx_to_c_sorted = onnx_to_c.sort_values('Parameter Count')
    onnx_to_smt_sorted = onnx_to_smt.sort_values('Parameter Count')
    
    # Create a single figure for the combined plot
    plt.figure(figsize=(12, 7))
    
    # Plot ONNX to C as a line with markers
    plt.plot(onnx_to_c_sorted['Parameter Count'], onnx_to_c_sorted['Time Taken (s)'], 
             label='ONNX to C', color='slateblue', marker='o')
    
    # Plot ONNX to SMT as a line with markers
    plt.plot(onnx_to_smt_sorted['Parameter Count'], onnx_to_smt_sorted['Time Taken (s)'], 
             label='ONNX to SMT', color='yellowgreen', marker='o')
    
    plt.title('Conversion Time vs Parameter Count')
    plt.xlabel('Parameter Count')
    plt.ylabel('Time Taken (s)')
    plt.grid(True)
    plt.legend()
    plt.tight_layout()
    plt.savefig(GRAPHS_DIR / 'conversion_time_plot.png')  # Save the plot as a PNG image


def main():
    # Define paths to the input CSV files (adjust if needed)
    onnx_to_c_path = RESULTS_DIR / 'onnx_to_c.csv'
    onnx_to_smt_path = RESULTS_DIR / 'onnx_to_smt.csv'
    
    # Process the data and generate the summary CSV
    process_conversion_times(onnx_to_c_path, onnx_to_smt_path)
    
    # Load data for plotting (reloading to avoid dependency on processed DataFrames)
    onnx_to_c = pd.read_csv(onnx_to_c_path)
    onnx_to_smt = pd.read_csv(onnx_to_smt_path)
    
    # Generate and save the plots
    plot_conversion_times(onnx_to_c, onnx_to_smt)

# Entry point to run the main function when the script is executed
if __name__ == '__main__':
    main()
