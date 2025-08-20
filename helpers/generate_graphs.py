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
    'SAT': 'yellowgreen',
    'UNSAT': 'lightcoral',
    'TIMEOUT': 'sandybrown',
    'UNKNOWN': 'slateblue',
    'VERIFICATION FAILED (SAT)': 'yellowgreen',
    'VERIFICATION SUCCESSFUL (UNSAT)': 'lightcoral',
}

# Shape mapping for different files/verifiers in comparison plot
FILE_SHAPES = ['o', 's', '^', 'D', 'v', '<', '>']

# List of all verifier types for combined mode
ALL_VERIFIER_TYPES = ['smt', 'sv', 'vnn']

def setup_directories(verifier_type=None):
    # Create the required directory structure if it doesn't exist.
    if verifier_type:
        output_dir = GRAPHS_DIR / verifier_type
    else:
        output_dir = GRAPHS_DIR  # For combined, use root graphs dir
    output_dir.mkdir(parents=True, exist_ok=True)
    return output_dir

def convert_runtime(runtime_str):
    # Convert runtime string (e.g., '900s') to float seconds.
    try:
        return float(runtime_str.replace('s', ''))
    except:
        return None

def get_verifier_name(filename: str) -> str:
    prefixes = ['vnn_result_', 'sv_result_', 'smt_result_']
    for prefix in prefixes:
        if filename.startswith(prefix):
            name_with_extension = filename[len(prefix):]
            # Remove file extension if present
            name = name_with_extension.split('.')[0]
            return name
    return filename  # Fallback if no prefix matched

def read_and_process_data(csv_files, verifier_type=None):
    # Read and process data from CSV files.
    data_dict = {}
    for csv_file in csv_files:
        csv_path = RESULTS_DIR / csv_file
        try:
            df = pd.read_csv(csv_path, skiprows=2)  # Skip Solver and Version headers
            df['RuntimeSeconds'] = df['Runtime'].apply(convert_runtime)
            df['Color'] = df['Actual Result'].map(RESULT_COLORS)
            if verifier_type:
                df['VerifierType'] = verifier_type
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
        plt.title(f'Parameter Count vs Runtime for {get_verifier_name(file_name)}')
        plt.xlabel('Parameter Count')
        plt.ylabel('Runtime (seconds)')
        plt.legend(title='Actual Result')
        plt.grid(True)
        output_file = output_dir / f"{verifier_type}_{get_verifier_name(file_name)}_plot.png"
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
                label=f'{get_verifier_name(file_name)} - {result}',
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
                c=s['Color'].iloc[0],
                label=actual_result,
                edgecolors='black',
                s=100
            )
        plt.title(f'{verifier_type.upper()} - Expected {expected_result} Results with Actual Results')
        plt.xlabel('Parameter Count')
        plt.ylabel('Runtime (seconds)')
        plt.legend(title='Actual Result')
        plt.grid(True)
        output_file = output_dir / f"{verifier_type}_{get_verifier_name(file_name)}_expected_{expected_result.lower()}_plot.png"
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
        plt.title(f'{verifier_type.upper()} - Cumulative Runtime Increase per Instance Index - {get_verifier_name(file_name)}')
        plt.xlabel('Instance Index (Sorted by Parameter Count)')
        plt.ylabel('Cumulative Runtime (seconds)')
        plt.legend()
        plt.grid(True)
        output_file = output_dir / f'{verifier_type}_{get_verifier_name(file_name)}_runtime_increase.png'
        plt.savefig(output_file)
        plt.close()
        print(f"Saved cumulative runtime increase plot to {output_file}")

def plot_combined_results(output_dir):
    # Combine data from all verifier types for cumulative line graph
    all_data_dict = {}
    for v_type in ALL_VERIFIER_TYPES:
        csv_files = [f for f in os.listdir(RESULTS_DIR) if f.startswith(v_type) and f.endswith('.csv')]
        if not csv_files:
            print(f"No CSV files found for {v_type}")
            continue
        type_data_dict = read_and_process_data(csv_files, verifier_type=v_type)
        all_data_dict.update(type_data_dict)
    if not all_data_dict:
        print("No data available for combined plot.")
        return
    # Generate combined line graph
    plt.figure(figsize=(14, 10))
    colors = plt.cm.tab10(np.linspace(0, 1, len(all_data_dict)))  # Unique colors for each line
    color_idx = 0
    for file_name, df in all_data_dict.items():
        # Extract verifier name from filename pattern _*result_*.csv
        # Assuming format like smt_result_z3.csv -> label 'z3'
        if '_result_' in file_name:
            verifier_label = file_name.split('_result_')[1].replace('.csv', '')
        else:
            verifier_label = file_name.replace('.csv', '')  # Fallback
        # Sort by Parameter Count and drop NaN runtimes
        sorted_df = df.dropna(subset=['RuntimeSeconds']).sort_values(by='Parameter Count').reset_index(drop=True)
        if sorted_df.empty:
            continue
        # Add index and cumulative runtime
        sorted_df['Index'] = sorted_df.index
        sorted_df['CumulativeRuntime'] = sorted_df['RuntimeSeconds'].cumsum()
        x = sorted_df['Index'].values
        y = sorted_df['CumulativeRuntime'].values
        if len(sorted_df) < 2:
            plt.plot(x, y, marker='o', linestyle='None', color=colors[color_idx], label=verifier_label)
        else:
            # Create smooth spline
            x_smooth = np.linspace(x.min(), x.max(), 300)
            spline = make_interp_spline(x, y, k=3)  # Cubic spline
            y_smooth = spline(x_smooth)
            plt.plot(x_smooth, y_smooth, '-', color=colors[color_idx], label=verifier_label)
            plt.plot(x, y, 'o', color=colors[color_idx])  # Original points
        color_idx += 1
    plt.title('Combined Cumulative Runtime Across All Verifiers (smt, sv, vnn)')
    plt.xlabel('Instance Index (Sorted by Parameter Count per Verifier)')
    plt.ylabel('Cumulative Runtime (seconds)')
    plt.legend(title='Verifier', bbox_to_anchor=(1.05, 1), loc='upper left')
    plt.grid(True)
    plt.tight_layout()
    output_file = output_dir / 'combined_cumulative_plot.png'
    plt.savefig(output_file)
    plt.close()
    print(f"Saved combined cumulative plot to {output_file}")

def generate_bar_graph(data_dict, output_dir, verifier_type=None):
    # Generate bar graph for number of instances per actual result (SAT, UNSAT, UNKNOWN, TIMEOUT)
    counts = {}
    for file_name, df in data_dict.items():
        verifier_name = get_verifier_name(file_name)
        if verifier_name not in counts:
            counts[verifier_name] = {'SAT': 0, 'UNSAT': 0, 'UNKNOWN': 0, 'TIMEOUT': 0}
        if verifier_type == "sv":
            # For SV, we need to handle the specific result types
            df['Actual Result'] = df['Actual Result'].replace({
                'VERIFICATION FAILED (SAT)': 'SAT',
                'VERIFICATION SUCCESSFUL (UNSAT)': 'UNSAT'
            })
        for result in ['SAT', 'UNSAT', 'UNKNOWN', 'TIMEOUT']:
            count = (df['Actual Result'] == result).sum()
            counts[verifier_name][result] += count

    if not counts:
        print("No data available for bar graph.")
        return

    verifiers = list(counts.keys())
    sat_counts = [counts[v]['SAT'] for v in verifiers]
    unsat_counts = [counts[v]['UNSAT'] for v in verifiers]
    unknown_counts = [counts[v]['UNKNOWN'] for v in verifiers]
    timeout_counts = [counts[v]['TIMEOUT'] for v in verifiers]

    bar_width = 0.2
    x = np.arange(len(verifiers))

    plt.figure(figsize=(12, 7))
    plt.bar(x - 1.5*bar_width, sat_counts, width=bar_width, color=RESULT_COLORS.get('SAT', 'gray'), label='SAT')
    plt.bar(x - 0.5*bar_width, unsat_counts, width=bar_width, color=RESULT_COLORS.get('UNSAT', 'gray'), label='UNSAT')
    plt.bar(x + 0.5*bar_width, unknown_counts, width=bar_width, color=RESULT_COLORS.get('UNKNOWN', 'gray'), label='UNKNOWN')
    plt.bar(x + 1.5*bar_width, timeout_counts, width=bar_width, color=RESULT_COLORS.get('TIMEOUT', 'gray'), label='TIMEOUT')

    plt.xlabel('Verifier')
    plt.ylabel('Number of Instances')
    if verifier_type:
        plt.title(f'{verifier_type.upper()} Verifiers - Number of Instances per Actual Result')
        output_filename = f"{verifier_type}_bar_graph.png"
    else:
        plt.title('Combined Verifiers - Number of Instances per Actual Result')
        output_filename = "combined_bar_graph.png"
    plt.xticks(x, verifiers, rotation=45, ha='right')
    plt.legend()
    plt.tight_layout()

    output_file = output_dir / output_filename
    plt.savefig(output_file)
    plt.close()
    print(f"Saved bar graph to {output_file}")

def plot_verifier_results_with_extra(verifier_type, combined=False):
    if combined:
        output_dir = setup_directories()  # Use root graphs dir for combined
        print("Generating combined results plot across all verifiers (smt, sv, vnn)")
        plot_combined_results(output_dir)
        # Generate combined bar graph
        all_data_dict = {}
        for v_type in ALL_VERIFIER_TYPES:
            csv_files = [f for f in os.listdir(RESULTS_DIR) if f.startswith(v_type) and f.endswith('.csv')]
            if not csv_files:
                print(f"No CSV files found for {v_type}")
                continue
            type_data_dict = read_and_process_data(csv_files, verifier_type=v_type)
            all_data_dict.update(type_data_dict)
        generate_bar_graph(all_data_dict, output_dir)
        return  # Skip other operations in combined mode

    # Single verifier mode
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

    print(f"Generating bar graph for {verifier_type}")
    generate_bar_graph(data_dict, output_dir, verifier_type)

if __name__ == "__main__":
    parser = argparse.ArgumentParser(description='Plot verifier results')
    parser.add_argument('--verifier', type=str, default='smt',
                        help='Verifier type prefix for CSV files (ignored in --combined mode)')
    parser.add_argument('--combined', action='store_true',
                        help='Generate combined graph across all verifiers (smt, sv, vnn)')
    args = parser.parse_args()
    plot_verifier_results_with_extra(args.verifier, combined=args.combined)
