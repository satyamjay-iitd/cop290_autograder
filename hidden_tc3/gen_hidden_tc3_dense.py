import sys
import string

NUM_COL = 18278

def column_to_letter(col):
    """Convert a column number (1-based) to a spreadsheet-style column letter."""
    letters = ""
    while col > 0:
        col -= 1
        letters = chr(ord('A') + (col % 26)) + letters
        col //= 26
    return letters

def main():
    if len(sys.argv) != 6:
        print("Usage: python script.py <r> <c> <operation> <file_path> <add_reassign>")
        sys.exit(1)
    
    rx = int(sys.argv[1])
    ry = int(sys.argv[2])
    operation = sys.argv[3].upper()
    file_path = sys.argv[4]
    add_reassign = bool(int(sys.argv[5]))

    with open(file_path, "w") as file:
        file.write("disable_output\n")
        # for col in range(1,NUM_COL+1):
        #     col_letter = column_to_letter(col)
        #     file.write(f"{col_letter}1={col}\n")

        file.write(f"A1=10000\n")
        file.write(f"B1=100000\n")

        num_edges = 0
        last_cell = ""

        for row in range(rx, 1000):
            for col in range(ry, NUM_COL+1):
                num_edges += col*(row-1)
                # if num_edges>max_num_edges:
                #     break
                col_letter = column_to_letter(col)
                last_cell = f"{col_letter}{row}"
                file.write(f"{col_letter}{row}={operation}(A1:{col_letter}{row-1})\n")
            # if num_edges>max_num_edges:
            #     break

        if add_reassign:
            file.write(f"A1=1000000\n")
        file.write(f"scroll_to {last_cell}\n")
        file.write("enable_output\n")

if __name__ == "__main__":
    main()
