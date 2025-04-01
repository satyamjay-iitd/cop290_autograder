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



def main(num_cmds, add_reassign, fn, file_path):
    # if len(sys.argv) != 5:
    #     print("Usage: python script.py <num_cmds> <add_reassign> <fn> <file_path>")
    #     sys.exit(1)
    
    # num_cmds = int(sys.argv[1])
    # assert num_cmds < 1000
    # add_reassign = bool(int(sys.argv[2]))
    # fn = sys.argv[3]
    # file_path = sys.argv[4]

    with open(file_path, "w") as file:
        file.write("999 18278\n")
        file.write("disable_output\n")
        if add_reassign:
            file.write(f"B1={2000000}\n")
        for i in range(num_cmds):
            file.write(f"A{i+1}={fn}(B1:ALA999)\n")
        if add_reassign:
            file.write("B1=1000000\n")
        file.write("enable_output\n")
        file.write("q")
            


if __name__ == "__main__":
    # range1
    main(300, 0, "MAX", "range1/small_max.cmds")
    main(300, 0, "MIN", "range1/small_min.cmds")
    main(300, 0, "SUM", "range1/small_sum.cmds")
    main(300, 0, "AVG", "range1/small_avg.cmds")
    main(300, 0, "STDDEV", "range1/small_stdev.cmds")
    # range2
    main(999, 0, "MAX", "range2/large.cmds")
    # range3
    main(300, 1, "MAX", "range3/small_max.cmds")
    main(300, 1, "MIN", "range3/small_min.cmds")
    main(300, 1, "SUM", "range3/small_sum.cmds")
    main(300, 1, "AVG", "range3/small_avg.cmds")
    main(300, 1, "STDDEV", "range3/small_stdev.cmds")
    # range3
    main(999, 1, "MAX", "range4/large.cmds")
