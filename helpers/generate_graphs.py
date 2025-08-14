import os
import sys
import argparse
import pandas as pd
import matplotlib.pyplot as plt
from pathlib import Path
import numpy as np
from scipy.interpolate import make_interp_spline

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

def plot_expected_results(data_dict, output_dir, verifier_type, expected_result):
    # Plot graphs for expected SAT or expected UNSAT
    for file_name, df in data_dict.items():
        subset = df[df['Expected Result'] == expected_result]
        if subset.empty:
            print(f"No data for expected {expected_result} in {file_name}")
            continue
        plt.figure(figsize=(10, 6))
        for actual_result in subset['Actual Result'].unique():
            s = subset[subset['Actual Result'] == actual_result]
            plt.scatter(
                s['Parameter Count'],
                s['RuntimeSeconds'],
                c=s['Color'],
                label=actual_result,
                edgecolors='black',
                s=100
            )
            for i, row in s.iterrows():
                plt.text(row['Parameter Count'], row['RuntimeSeconds'], row['Actual Result'], fontsize=8, ha='right')
        plt.title(f'{verifier_type.upper()} - Expected {expected_result} Results with Actual Results')
        plt.xlabel('Parameter Count')
        plt.ylabel('Runtime (seconds)')
        plt.legend(title='Actual Result')
        plt.grid(True)
        output_file = output_dir / f"{verifier_type}_{file_name}_expected_{expected_result.lower()}_plot.png"
        plt.savefig(output_file)
        plt.close()
        print(f"Saved expected {expected_result} plot to {output_file}")

def create_summary_table(data_dict):
    # Create a table showing count of expected results and false results for each verifier file
    table_data = []
    for file_name, df in data_dict.items():
        expected_sat = df[df['Expected Result'] == 'SAT']
        expected_unsat = df[df['Expected Result'] == 'UNSAT']
        # Count how many SAT expected and how many actual results differ (false results)
        sat_correct = (expected_sat['Actual Result'] == 'SAT').sum()
        sat_false = (expected_sat['Actual Result'] != 'SAT').sum()
        unsat_correct = (expected_unsat['Actual Result'] == 'UNSAT').sum()
        unsat_false = (expected_unsat['Actual Result'] != 'UNSAT').sum()
        total = len(df)
        table_data.append({
            'Verifier File': file_name,
            'Total Instances': total,
            'Expected SAT Count': len(expected_sat),
            'Correct SAT Results': sat_correct,
            'False SAT Results': sat_false,
            'Expected UNSAT Count': len(expected_unsat),
            'Correct UNSAT Results': unsat_correct,
            'False UNSAT Results': unsat_false,
        })
    summary_df = pd.DataFrame(table_data)
    return summary_df

def plot_runtime_increase(data_dict, output_dir, verifier_type):
    for file_name, df in data_dict.items():
        # Sort by Parameter Count and drop NaN runtimes
        sorted_df = df.dropna(subset=['RuntimeSeconds']).sort_values(by='Parameter Count').reset_index(drop=True)
        if sorted_df.empty:
            print(f"Skipping plot for {file_name} due to no valid runtime data.")
            continue
        
        # Add index and cumulative runtime
        sorted_df['Index'] = sorted_df.index
        sorted_df['CumulativeRuntime'] = sorted_df['RuntimeSeconds'].cumsum()
        
        x = sorted_df['Index'].values
        y = sorted_df['CumulativeRuntime'].values
        
        plt.figure(figsize=(10, 6))
        
        if len(sorted_df) < 2:
            print(f"Skipping smoothing for {file_name} due to insufficient data points.")
            # Just plot points if too few for spline
            plt.plot(x, y, marker='o', linestyle='None', label='Original Data')
        else:
            # Create smooth spline
            x_smooth = np.linspace(x.min(), x.max(), 300)
            spline = make_interp_spline(x, y, k=3)  # Cubic spline
            y_smooth = spline(x_smooth)
            plt.plot(x, y, 'o', label='Original Data')  # Original points
            plt.plot(x_smooth, y_smooth, '-', label='Smoothed Curve')  # Smoothed line
        
        plt.title(f'{verifier_type.upper()} - Cumulative Runtime Increase per Instance Index - {file_name}')
        plt.xlabel('Instance Index (Sorted by Parameter Count)')
        plt.ylabel('Cumulative Runtime (seconds)')
        plt.legend()
        plt.grid(True)
        output_file = output_dir / f'{verifier_type}_{file_name}_runtime_increase.png'
        plt.savefig(output_file)
        plt.close()
        print(f"Saved cumulative runtime increase plot to {output_file}")

def plot_verifier_results_with_extra(verifier_type):
    csv_files = [f for f in os.listdir(RESULTS_DIR) if f.startswith(verifier_type) and f.endswith('.csv')]
    if not csv_files:
        print(f'No CSV files found for verifier type: {verifier_type}')
        return
    data_dict = read_and_process_data(csv_files)
    output_dir = setup_directories(verifier_type)
    
    print("Generating individual plots for all data")
    generate_individual_plots(data_dict, output_dir, verifier_type)
    
    print("Generating comparison plot for all data")
    generate_comparison_plot(data_dict, output_dir, verifier_type)
    
    print(f"Generating expected SAT plots for {verifier_type}")
    plot_expected_results(data_dict, output_dir, verifier_type, 'SAT')
    
    print(f"Generating expected UNSAT plots for {verifier_type}")
    plot_expected_results(data_dict, output_dir, verifier_type, 'UNSAT')
    
    print("Generating runtime increase plots")
    plot_runtime_increase(data_dict, output_dir, verifier_type)
    
    print("Creating summary table for expected and false results")
    summary_df = create_summary_table(data_dict)
    summary_table_path = output_dir / f'{verifier_type}_summary_results.csv'
    summary_df.to_csv(summary_table_path, index=False)
    print(f"Summary table saved to {summary_table_path}")

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot verifier results')
    parser.add_argument('--verifier', type=str, default='smt', 
                        help='Verifier type prefix for CSV files')
    args = parser.parse_args()
    VERIFIER_TYPE = args.verifier
    plot_verifier_results_with_extra(VERIFIER_TYPE)
