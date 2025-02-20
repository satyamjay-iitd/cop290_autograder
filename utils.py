import dataclasses
from typing import Literal
import re
from rich.console import Console as RConsole
from rich.text import Text as RText
from rich.table import Table as RTable
from rich.panel import Panel as RPanel
from rich.style import Style as RStyle
from rich.columns import Columns as RColumns


type ColNames = list[str]
type RowIdx = int
type Err = Literal["Err"]
type Rows = list[tuple[RowIdx, list[int | Err]]]

@dataclasses.dataclass
class Diff:
    existence_diff: tuple[bool, bool] | None = None
    header_diff: tuple[ColNames, ColNames] | None = None
    num_row_diff: tuple[int, int] | None = None
    # RowIdx, ExpectedValue, ObservedValue
    row_id_diff: tuple[int, int, int] | None = None
    # CellIdx, ExpectedValue, ObservedValue
    cell_value_diff: tuple[tuple[int, int], int | Err, int | Err] | None = None
    time_diff: tuple[str, int] | None = None


@dataclasses.dataclass
class Table:
    col_names: ColNames
    rows: Rows

    """Returns whether the table is valid, if it is invalid, return reason."""
    def validate(self) -> tuple[bool, str]:
        if len(self.col_names) > 10:
            return False, "Num columns > 10"
        if len(self.rows) > 10:
            return False, "Num rows > 10"

        for col in self.col_names:
            if not re.match("[A-Z]{1,3}", col):
                return False, f"Invalid Col name {col}"

        for row in self.rows:
            if row[0] > 999:
                return False, f"Only 999 rows are allowed found {row[0]}"
            if len(row[1]) != self.num_cols():
                return False, f"All rows must have {self.num_cols()} number of cells found {len(row[1])}"

        return True, ""
            

    def num_cols(self) -> int:
        return len(self.col_names)
        
    def num_rows(self) -> int:
        return len(self.rows)


@dataclasses.dataclass
class ExpectedOutput:
    status_is_ok: bool
    time: int
    table: Table | None


"""Calculates diff with the other tables"""
def diff_table(exp: Table|None, other: Table|None) -> Diff | None:
    if other is None and exp is None:
        return None
    if exp is None and other is not None:
        return Diff(existence_diff=(False, True))
    if other is None and exp is not None:
        return Diff(existence_diff=(True, False))

    assert(exp is not None)
    assert(other is not None)

    if exp.col_names != other.col_names:
        return Diff(header_diff=(exp.col_names, other.col_names))
    if exp.num_rows() != other.num_rows():
        return Diff(num_row_diff=(exp.num_rows(), other.num_rows()))

    for (row_idx, (my_row, other_row)) in enumerate(zip(exp.rows, other.rows)):
        if my_row[0] != other_row[0]:
            return Diff(row_id_diff=(row_idx, my_row[0], other_row[0]))
        for (cell_idx, (my_cell, other_cell)) in enumerate(zip(my_row[1], other_row[1])):
            if my_cell != other_cell:
                return Diff(cell_value_diff=((row_idx, cell_idx), my_cell, other_cell))

    return None

def get_rich_table(sheet: Table, highlight_cell: tuple[tuple[int, int], str]=((-1, -1), "")) -> RTable:
    table = RTable()

    table.add_column("row_id", justify="right", style="cyan", no_wrap=True)
    for col in sheet.col_names:
        table.add_column(col, justify="right", no_wrap=True)

    for row_idx, row in enumerate(sheet.rows):
        cells = []
        for col_idx, cell in enumerate(row[1]):
            if highlight_cell[0] == (row_idx, col_idx):
                style = RStyle(bgcolor=highlight_cell[1])
                colored_text = RText(str(cell), style=style)
                cells.append(colored_text)
            else:
                cells.append(str(cell))
        table.add_row(str(row[0]), *cells)

    return table

"""Shows diff in a rich console"""
def print_diff(console: RConsole, diff: Diff, cmd: str, exp_sheet: Table|None, student_sheet: Table|None):
    console.print(f"For command {cmd}:-", style="red")
    if diff.existence_diff is not None:
        if diff.existence_diff == (True, False):
            text = RText("Expected following table found None:-")
            console.print(text)
            rich_table = get_rich_table(exp_sheet)
            console.print(rich_table)
        elif diff.existence_diff == (False, True):
            text = RText("Expected None found the following table:-")
            rich_table = get_rich_table(student_sheet)
            console.print(text)
            console.print(rich_table)
    elif diff.header_diff is not None:
        print(exp_sheet)
        print(student_sheet)
        text = RText("Expected header != given header")
        table = RTable()
        table.add_row("Expected", *exp_sheet.col_names)
        table.add_row("Found", *student_sheet.col_names)
        console.print(text)
        console.print(table)
    elif diff.num_row_diff is not None:
        text = RText()
        text.append("Number of ")
        text.append("expected", style="green")
        text.append(f" rows {exp_sheet.num_rows()}, ")
        text.append("found", style="red")
        text.append(f" num rows {student_sheet.num_rows()}")
        console.print(text)

    elif diff.row_id_diff is not None:
        text = RText()
        text.append("Id of ")
        text.append("{}th row", style="cyan")
        text.append(f" is supposed to be {diff.row_id_diff[0]},", style="green")
        text.append(f" found num rows {diff.row_id_diff[1]}", style="red")

    elif diff.cell_value_diff is not None:
        table1, table2 = get_rich_table(exp_sheet, (diff.cell_value_diff[0], "green")), get_rich_table(student_sheet, (diff.cell_value_diff[0], "red"))
        panel = RPanel.fit(
            RColumns([table1, table2]),
            title="Table diff",
            border_style="red",
            title_align="left",
            padding=(1, 2),
        )
        console.print(panel)
    elif diff.time_diff is not None:
        text = RText()
        text.append("Command ")
        text.append(diff.time_diff[0], style="yellow")
        text.append(", expected to run in ")
        text.append(str(diff.time_diff[1]), style="green")
        text.append("secs.")
        console.print(text)
        

"""
Parses list of string to Table.
"""
def parse_table(lines: list[str]) -> Table | None:
    if len(lines) == 0:
        return None
    # Parse header line
    header_line = lines[0].split()
    rows: list[tuple[int, list[int | Literal["Err"]]]] = []

    # Parse row
    for row in lines[1:]:
        if len(row) == 0:
            continue
        row = row.strip()
        cells = row.split()
        # First cell is row number
        assert cells[0].isnumeric(), "Row index must be integer"
        row_num = int(cells[0])

        # Parse cell to integer or Err
        parsed_cells: list[int|Literal["Err"]] = []
        for cell in cells[1:]:
            cell = cell.strip()
            try:
                parsed_cells.append(int(cell))
            except ValueError:
                parsed_cells.append("Err")
        rows.append((row_num, parsed_cells))

    return Table(header_line, rows)


