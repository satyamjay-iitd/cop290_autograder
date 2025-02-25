import argparse

class Range:
    def __init__(self, range_start, range_end):
        self.range_start = range_start  # (row, col)
        self.range_end = range_end      # (row, col)
        self.current = range_start      # Start iteration from range_start

    def __iter__(self):
        return self

    def __next__(self):
        if self.current is None:
            raise StopIteration

        row, col = self.current  # Get current position
        current_position = (row, col)  # Store current position for return

        # Calculate next position
        next_col = col + 1
        next_row = row

        if next_col > self.range_end[1]:  # Move to next row
            next_col = self.range_start[1]
            next_row += 1

        # Update current state
        if next_row > self.range_end[0]:
            self.current = None  # End of iteration
        else:
            self.current = (next_row, next_col)

        return current_position

    def __len__(self):
        return ((self.range_end[0] - self.range_start[0] + 1) *
                (self.range_end[1] - self.range_start[1] + 1))

def col_idx_to_name(idx: int) -> str:
    if idx < 0:
        raise ValueError("Index must be non-negative")

    if idx // 26 != 0:
        parent = col_idx_to_name(idx // 26 - 1)
    else:
        parent = ""

    return parent + chr(ord('A') + (idx % 26))


def generate_pattern(r: Range):
    cells = list(r)
    cmd_file = open("tests/large_dep_chain.cmds", "w")
    exp_file = open("tests/large_dep_chain.exp", "w")
    print("disable_output", file=cmd_file)
    print("ok 0\n*******************", file=exp_file)
    for i in range(1, len(cells)):
        lhs_x, lhs_y = cells[i]
        rhs_x, rhs_y = cells[i-1]
        lhs_col = col_idx_to_name(lhs_y)
        rhs_col = col_idx_to_name(rhs_y)
        print(f"{lhs_col}{lhs_x+1}={rhs_col}{rhs_x+1}+1", file=cmd_file)
        print("ok 0\n*******************", file=exp_file)
    print("A1=1", file=cmd_file)
    print("ok 0\n*******************", file=exp_file)
    


# Change this to generate larger/smaller test cases
if __name__=="__main__":
    parser = argparse.ArgumentParser(description="Process range end values.")
    parser.add_argument("rows", type=int, help="Number of rows")
    parser.add_argument("cols", type=int, help="Number of columns")
    
    args = parser.parse_args()
    r = Range((0, 0), (args.rows-1, args.cols-1))
    generate_pattern(r)
