import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path

SCRIPT_DIR = Path(__file__).parent
RESULTS_DIR = SCRIPT_DIR.parent / "results"
GRAPHS_DIR = SCRIPT_DIR.parent / "graphs"

# Color mapping for actual results
RESULT_COLORS = {
    'SAT': 'green',
    'UNSAT': 'red',
    'TIMEOUT': 'orange',
    'UNKNOWN': 'blue',
    'VERIFICATION FAILED (SAT)': 'green',
    'VERIFICATION SUCCESSFUL (UNSAT)': 'red',
}

# Shape mapping for different files/verifiers in comparison plot
FILE_SHAPES = ['o', 's', '^', 'D', 'v', '<', '>']

def setup_directories(verifier_type):
    # Create the required directory structure if it doesn't exist.
    output_dir = GRAPHS_DIR / verifier_type
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def convert_runtime(runtime_str):
    # Convert runtime string (e.g., '900s') to float seconds.
    try:
        return float(runtime_str.replace('s', ''))
    except:
        return None


def read_and_process_data(csv_files):
    # Read and process data from CSV files.
    data_dict = {}
    for csv_file in csv_files:
        csv_path = RESULTS_DIR / csv_file
        try:
            df = pd.read_csv(csv_path, skiprows=2)  # Skip Solver and Version headers
            df['RuntimeSeconds'] = df['Runtime'].apply(convert_runtime)
            df['Color'] = df['Actual Result'].map(RESULT_COLORS)
            data_dict[csv_file] = df
        except Exception as e:
            print(f"Error reading {csv_file}: {e}")
    return data_dict


def generate_individual_plots(data_dict, output_dir, verifier_type):
    # Generate individual scatter plots for each file.
    for file_name, df in data_dict.items():
        plt.figure(figsize=(10, 6))
        for result in df['Actual Result'].unique():
            subset = df[df['Actual Result'] == result]
            plt.scatter(
                subset['Parameter Count'],
                subset['RuntimeSeconds'],
                c=subset['Color'].iloc[0],
                label=result,
                edgecolors='black',
                s=100
            )
            # Add labels for expected result
            for i, row in subset.iterrows():
                plt.text(
                    row['Parameter Count'],
                    row['RuntimeSeconds'],
                    row['Expected Result'],
                    fontsize=8,
                    ha='right'
                )
        plt.title(f'Verifier Results: Parameter Count vs Runtime for {file_name}')
        plt.xlabel('Parameter Count')
        plt.ylabel('Runtime (seconds)')
        plt.legend(title='Actual Result')
        plt.grid(True)
        output_file = output_dir / f"{verifier_type}_{file_name}_plot.png"
        plt.savefig(output_file)
        plt.close()
        print(f"Saved individual plot to {output_file}")

def generate_comparison_plot(data_dict, output_dir, verifier_type):
    # Generate comparison scatter plot across all files.
    plt.figure(figsize=(12, 8))
    shape_idx = 0
    for file_name, df in data_dict.items():
        marker = FILE_SHAPES[shape_idx % len(FILE_SHAPES)]
        for result in df['Actual Result'].unique():
            subset = df[df['Actual Result'] == result]
            plt.scatter(
                subset['Parameter Count'],
                subset['RuntimeSeconds'],
                c=subset['Color'].iloc[0],
                label=f'{file_name} - {result}',
                marker=marker,
                edgecolors='black',
                s=100
            )
            # Add labels for expected result
            for i, row in subset.iterrows():
                plt.text(
                    row['Parameter Count'],
                    row['RuntimeSeconds'],
                    row['Expected Result'],
                    fontsize=8,
                    ha='right'
                )
        shape_idx += 1
    plt.title(f'Comparison of Parameter Count vs Runtime Across {verifier_type.upper()} Files (Colored by Actual Result)')
    plt.xlabel('Parameter Count')
    plt.ylabel('Runtime (seconds)')
    plt.legend(title='File/Verifier - Actual Result', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    output_file = output_dir / f"{verifier_type}_comparison_plot.png"
    plt.savefig(output_file)
    plt.close()
    print(f"Saved comparison plot to {output_file}")

def plot_verifier_results(verifier_type):
    csv_files = [f for f in os.listdir(RESULTS_DIR) if f.startswith(verifier_type) and f.endswith(".csv")]
    if not csv_files:
        print(f"No CSV files found for verifier type: {verifier_type}")
        return
    
    print(f"Found {len(csv_files)} CSV files for verifier type: {verifier_type}")
    data_dict = read_and_process_data(csv_files)
    output_dir = setup_directories(verifier_type)
    
    print("Generating individual plots")
    generate_individual_plots(data_dict, output_dir, verifier_type)
    print("Generating comparison plot")
    generate_comparison_plot(data_dict, output_dir, verifier_type)
    
    print(f"Graphs generated and saved in {output_dir}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot verifier results')
    parser.add_argument('--verifier', type=str, default='smt', 
                        help='Verifier type prefix for CSV files')
    args = parser.parse_args()
    VERIFIER_TYPE = args.verifier
    plot_verifier_results(VERIFIER_TYPE)
