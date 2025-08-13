import re

def sort_files_by_v_c(file_names):
    # Sorts a list of file names based on the 'v' value extracted from the name,
    # and if 'v' values are the same, sorts by the 'c' value.
    
    # Assumes file names contain patterns like 'name_v<number>_c<number>'.
    # - Extracts integers after 'v' and '_c' using regex.
    # - If no match, defaults to v=0, c=0.
    # - Sorts in ascending order: smaller v first, then smaller c.
    
    # Args:
    #     file_names (list[str]): List of file names (stems or full paths, but only stem is used for extraction).
    
    # Returns:
    #     list[str]: Sorted list of file names.

    def extract_key(name):
        # Use only the stem if it's a path
        if '/' in name or '\\' in name:
            name = name.split('/')[-1].split('\\')[-1].split('.')[0]
        
        match = re.search(r'v(\d+)_c(\d+)', name)
        v_num = int(match.group(1)) if match else 0
        c_num = int(match.group(2)) if match else 0
        return (v_num, c_num, name) 

    return sorted(file_names, key=extract_key)
