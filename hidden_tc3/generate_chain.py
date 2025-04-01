import sys

NUM_COL = 18278

def column_to_letter(col):
    """Convert a column number (1-based) to a spreadsheet-style column letter."""
    letters = ""
    while col > 0:
        col -= 1
        letters = chr(ord('A') + (col % 26)) + letters
        col //= 26
    return letters



def main(chain_size, range_width, file_path, add_reassign):

    with open(file_path, "w") as file:
        file.write("999 18278\n")
        file.write("disable_output\n")
        file.write(f"A1={1000000}\n")

        for start_col in range(1, chain_size*range_width, range_width+1):
            start_col_l = column_to_letter(start_col)
            start_cell = (1, start_col_l)
            end_col_l = column_to_letter(start_col+range_width)
            end_cell = (999, end_col_l)

            to_assign = (1, column_to_letter(start_col+range_width+1))
            file.write(f"{to_assign[1]}{to_assign[0]}=MAX({start_cell[1]}{start_cell[0]}:{end_cell[1]}{end_cell[0]})\n")

        if add_reassign:
            file.write("A1=2000000\n")
        file.write(f"scroll_to {to_assign[1]}{to_assign[0]}\n")
        file.write("enable_output\n")
        file.write("q\n")


if __name__ == "__main__":
    # small
    main(50, 100, "chain/small.cmds", True)
    # large
    main(180, 101, "chain/large.cmds", True)
