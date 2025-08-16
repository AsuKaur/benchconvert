import os
import csv
import re
from collections import defaultdict
from pathlib import Path


# Set up directories
SCRIPT_DIR = Path(__file__).parent
ROOT_DIR = SCRIPT_DIR.parent
RESULT_DIR = ROOT_DIR / "results"


def merge_chunk_files():
    # Dictionary to group files by their base name (without _chunkN)
    groups = defaultdict(list)
    
    # Regex to match files like x_result_type_chunkN.csv where N is 1-10
    pattern = re.compile(r'^(.*)_chunk(\d+)\.csv$')
    
    for file in os.listdir(RESULT_DIR):
        match = pattern.match(file)
        if match:
            base_name = match.group(1)
            chunk_num = int(match.group(2))
            groups[base_name].append((chunk_num, file))
    
    for base_name, chunks in groups.items():
        # Sort chunks by chunk number
        chunks.sort(key=lambda x: x[0])
        
        # Output file: base_name.csv
        output_file = RESULT_DIR / f"{base_name}.csv"
        
        # List to hold all data rows
        all_data = []
        header_written = False
        solver_verifier = None
        version = None
        column_headers = None
        
        for chunk_num, chunk_file in chunks:
            chunk_path = RESULT_DIR / chunk_file
            with open(chunk_path, mode='r', newline='') as f:
                reader = csv.reader(f)
                rows = list(reader)
            
            if not header_written:
                # Take the first two rows (Solver/Verifier and Version) from the first chunk
                if rows:
                    solver_verifier = rows[0]
                if len(rows) > 1:
                    version = rows[1]
                if len(rows) > 2:
                    column_headers = rows[2]
                data_start = 3
                header_written = True
            else:
                # For subsequent chunks, skip the first three rows (headers)
                data_start = 3
            
            # Append data rows
            all_data.extend(rows[data_start:])
        
        # Write to output file
        with open(output_file, mode='w', newline='') as f:
            writer = csv.writer(f)
            if solver_verifier:
                writer.writerow(solver_verifier)
            if version:
                writer.writerow(version)
            if column_headers:
                writer.writerow(column_headers)
            writer.writerows(all_data)
        
        print(f"Merged chunks for {base_name} into {output_file}")
        
        # Optionally, delete the chunk files after merging
        # for _, chunk_file in chunks:
        #     os.remove(RESULT_DIR / chunk_file)
        #     print(f"Deleted {chunk_file}")


if __name__ == "__main__":
    RESULT_DIR.mkdir(exist_ok=True)
    merge_chunk_files()
