import sys

def normalize_indentation(file_path, use_tabs=False, tab_size=4):
    """
    Normalizes the indentation in a Python file by converting mixed tabs and spaces to consistent use.
    If `use_tabs` is True, it will convert spaces to tabs (each tab being equivalent to `tab_size` spaces).
    Otherwise, it will convert tabs to spaces (each tab being replaced by `tab_size` spaces).

    :param file_path: Path to the Python file.
    :param use_tabs: If True, converts spaces to tabs. Otherwise, converts tabs to spaces.
    :param tab_size: Number of spaces equivalent to one tab.
    """
    try:
        with open(file_path, 'r') as file:
            lines = file.readlines()
        
        with open(file_path, 'w') as file:
            for line in lines:
                stripped_line = line.lstrip()
                
                # Skip empty lines and lines without leading whitespace
                if stripped_line == "" or line == stripped_line:
                    file.write(line)
                    continue

                indentation = line[:len(line) - len(stripped_line)]

                # Count number of tabs and spaces
                tab_count = indentation.count('\t')
                space_count = len(indentation) - tab_count

                # Calculate total equivalent space count (considering 1 tab = tab_size spaces)
                total_space_equivalent = tab_count * tab_size + space_count

                # Convert to the desired indentation
                if use_tabs:
                    new_indentation = '\t' * (total_space_equivalent // tab_size)
                else:
                    new_indentation = ' ' * total_space_equivalent

                # Write the normalized line
                file.write(new_indentation + stripped_line)
        
        print(f"Successfully normalized indentation in {file_path}.")
    
    except Exception as e:
        print(f"An error occurred: {e}")

if __name__ == "__main__":
    if len(sys.argv) != 2:
        print("Usage: python normalize_indentation.py <file_path>")
    else:
        normalize_indentation(sys.argv[1])

