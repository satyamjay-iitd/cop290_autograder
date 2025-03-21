import sys
import string

def column_to_letter(col):
    """Convert a column number (1-based) to a spreadsheet-style column letter."""
    letters = ""
    while col > 0:
        col -= 1
        letters = chr(ord('A') + (col % 26)) + letters
        col //= 26
    return letters

def main():
    if len(sys.argv) != 8:
        print("Usage: python script.py <col_start> <col_end> <row_start> <row_end> <operation> <file_path> <add_reassign>")
        sys.exit(1)
    
    col_start, col_end, row_start, row_end = map(int, sys.argv[1:5])
    operation = sys.argv[5].upper()
    file_path = sys.argv[6]
    add_reassign = bool(int(sys.argv[7]))
    
    start_cell = f"{column_to_letter(col_start)}{row_start}"
    last_cell = f"{column_to_letter(col_end)}{row_end}"
    
    with open(file_path, "w") as file:
        file.write("disable_output\n")
        for col in range(col_start, col_end + 1):
            col_letter = column_to_letter(col)
            for row in range(row_start, row_end + 1):
                file.write(f"{col_letter}{row}={(row * col)%10}\n")
        
        file.write(f"A1={operation}({start_cell}:{last_cell})\n")
        if add_reassign:
            file.write(f"{start_cell}=-1\n")
        file.write("enable_output\n")

if __name__ == "__main__":
    main()