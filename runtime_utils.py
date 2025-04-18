"""
This utilities are used for running the submission.
"""

import dataclasses
import os
from typing import Literal, Optional
import re
import subprocess
from rich.console import Console as RConsole
from rich.text import Text as RText
from rich.table import Table as RTable
from rich.panel import Panel as RPanel
from rich.style import Style as RStyle
from rich.columns import Columns as RColumns
from pathlib import Path
import shutil
import pandas as pd
from dataclasses import dataclass
from typing import Callable
import zipfile
from compile_utils import (
    find_makefile,
    extract_entry_no,
    build_binary,
    get_test_case_pairs,
)

console = RConsole()
# import pdb
# pdb.set_trace()


type ColNames = list[str]
type RowIdx = int
type Err = Literal["Err"]
type Rows = list[tuple[RowIdx, list[int | Err]]]

PATCH_DIR = "/home/baadalvm/lab1_patches"


@dataclasses.dataclass
class Diff:
    status_diff: tuple[bool, bool] | None = None
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
                return (
                    False,
                    f"All rows must have {self.num_cols()} number of cells found {len(row[1])}",
                )

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


def compute_diff(
    exp: ExpectedOutput, student_table: Table | None, student_status: bool
) -> Diff | None:
    if student_status != exp.status_is_ok:
        return Diff(status_diff=(exp.status_is_ok, student_status))

    if student_table is None and exp.table is None:
        return None
    if exp.table is None and student_table is not None:
        return Diff(existence_diff=(False, True))
    if student_table is None and exp.table is not None:
        return Diff(existence_diff=(True, False))

    exp_table = exp.table
    assert exp_table is not None
    assert student_table is not None

    if exp_table.col_names != student_table.col_names:
        return Diff(header_diff=(exp_table.col_names, student_table.col_names))
    if exp_table.num_rows() != student_table.num_rows():
        return Diff(num_row_diff=(exp_table.num_rows(), student_table.num_rows()))

    for row_idx, (my_row, other_row) in enumerate(
        zip(exp_table.rows, student_table.rows)
    ):
        if my_row[0] != other_row[0]:
            return Diff(row_id_diff=(row_idx, my_row[0], other_row[0]))
        for cell_idx, (my_cell, other_cell) in enumerate(zip(my_row[1], other_row[1])):
            if my_cell != other_cell:
                return Diff(cell_value_diff=((row_idx, cell_idx), my_cell, other_cell))

    return None


def get_rich_table(
    sheet: Table, highlight_cell: tuple[tuple[int, int], str] = ((-1, -1), "")
) -> RTable:
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


def print_diff(
    console: RConsole,
    diff: Diff,
    cmd: str,
    exp_sheet: Table | None,
    student_sheet: Table | None,
):
    console.print(f"For command {cmd}:-", style="red")
    if diff.status_diff is not None:
        if diff.status_diff == (True, False):
            console.print("Expected status 'ok' found 'err'")
        elif diff.status_diff == (False, True):
            console.print("Expected status 'err' found 'ok'")
        return

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
        text.append(f"{diff.row_id_diff[0]}th row", style="cyan")
        text.append(f" is supposed to be {diff.row_id_diff[1]},", style="green")
        text.append(f" found num rows {diff.row_id_diff[2]}", style="red")
        console.print(text)

    elif diff.cell_value_diff is not None:
        table1, table2 = (
            get_rich_table(exp_sheet, (diff.cell_value_diff[0], "green")),
            get_rich_table(student_sheet, (diff.cell_value_diff[0], "red")),
        )
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
        assert cells[0].isnumeric(), f"Row index must be integer  {lines}"
        row_num = int(cells[0])

        # Parse cell to integer or Err
        parsed_cells: list[int | Literal["Err"]] = []
        for cell in cells[1:]:
            cell = cell.strip()
            try:
                parsed_cells.append(int(cell))
            except ValueError:
                parsed_cells.append("Err")
        rows.append((row_num, parsed_cells))

    return Table(header_line, rows)


def extract_zip(file: Path) -> Path | None:
    if file.suffix != ".zip":
        return None
    extract_to = Path("/tmp/cop290_lab1/")
    # Remove the extract_to directory if it exists
    if extract_to.exists():
        shutil.rmtree(extract_to)

    # Create a fresh extract_to directory
    extract_to.mkdir(parents=True, exist_ok=True)
    with zipfile.ZipFile(file, "r") as zip_ref:
        zip_ref.extractall(extract_to)
        print(f"Extracted {file} to {extract_to}")

    return extract_to

def extract_patch_file_path(entry_num: str) -> Optional[Path]:
    try:
        for filename in os.listdir(PATCH_DIR):
            if entry_num.lower() in filename.lower():
                return Path(PATCH_DIR) / filename
        return None
    except FileNotFoundError:
        return None


@dataclass
class TestResult:
    is_pass: bool
    marks: float
    time_taken_s: int = -1
    max_mem_gb: int = -1
    reason: str = ""


def eval_single(
    test_lambda: Callable[[Path, Path, Path, dict[str, int]], TestResult],
    submission_zip: Path,
    test_dir: Path,
    entry_nos: list[str],
    marks_mapping: dict[str, int],
    patch: bool = False,
    add_mem_info: bool = False,
):
    extraction = extract_zip(submission_zip)
    if extraction is None:
        return "Couldn't extract zip file"
    else:
        extracted_dir = extraction

    make_file_dir = find_makefile(extracted_dir)
    if make_file_dir is None:
        return "Makefile not found"

    if patch:
        # find the patch file
        patch_path = None
        for entry_no in entry_nos:
            patch_file = extract_patch_file_path(entry_no) 
            if patch_file:
                if patch_path:
                    assert patch_file == patch_file, f"Two different patch file found {patch_file} {patch_path}"
                else:
                    patch_path = patch_file
        if patch_path:
            print(patch_path)
            print("Applying patch")
            subprocess.run(["git", "apply", str(patch_path)], cwd=str(make_file_dir))

    try:
        bin_path = build_binary(make_file_dir, entry_nos)
    except FileNotFoundError:
        return "Couldn't compile binary"

    test_cases = get_test_case_pairs(test_dir)

    verdict = []
    marks = {}
    for cmd, expected in test_cases:
        console.print(f"Running {cmd}")
        result = test_lambda(bin_path, cmd, expected, marks_mapping)
        # Kill spreadsheet process for sanity
        subprocess.run(["pkill", "-f", "spreadsheet"])

        verdict.append((cmd, result.is_pass, result.reason, result.marks, result.max_mem_gb, result.time_taken_s))
        if not result.is_pass:
            marks[str(cmd)] = result.reason
        else:
            marks[str(cmd)] = result.marks
        if add_mem_info and result.max_mem_gb != -1:
            marks[f"{str(cmd)}_mem"] = result.max_mem_gb
            marks[f"{str(cmd)}_time"] = result.time_taken_s

    table = RTable()

    table.add_column("Test Case", justify="right", style="cyan", no_wrap=True)
    table.add_column("Verdict", justify="right", style="cyan", no_wrap=True)
    table.add_column("Marks", justify="right", style="cyan", no_wrap=True)
    table.add_column("Memory(MB)", justify="right", style="cyan", no_wrap=True)
    table.add_column("Time(ms)", justify="right", style="cyan", no_wrap=True)
    for test, is_pass, reason, mark, mem, time in verdict:
        if is_pass:
            table.add_row(str(test), "PASS", str(mark), str(mem), str(time), style="green")
        else:
            table.add_row(str(test), f"FAIL: {reason}", str(mark), str(mem), str(time), style="red")
    console.print(table)
    print(marks)
    return marks


def eval_batch(
    test_lambda: Callable[[Path, Path, Path, dict[str, int]], TestResult],
    submission_dir: Path,
    test_dir: Path,
    marks_mapping: dict[str, int],
    marks_csv: Path,
    add_mem_info: bool = False,
    patch: bool = False
):
    def is_number(s: str) -> bool:
        try:
            float(s)
            return True
        except ValueError:
            return False

    total_data = []
    # Add the failed submissions to this directory for manual inspection
    failed_dir = Path("/tmp/cop290_lab1_failed/")

    if failed_dir.exists():
        shutil.rmtree(failed_dir)
        failed_dir.mkdir(parents=True, exist_ok=True)

    i = 0
    for submission_zip in submission_dir.iterdir():
        i += 1
        # if i > 10:
        #     continue

        print(f"Evaluating: {submission_zip}")
        try:
            entry_nos = extract_entry_no(submission_zip)
            if not entry_nos:
                data = {}
                data["group_idx"] = submission_zip.stem
                data["entry_no"] = None
                data["error"] = f"Couldn't extract entry numbers from {submission_zip}"
                data["total"] = 0
                failed_dir.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(submission_zip, failed_dir / submission_zip.name)
                continue

            group_idx = "_".join(entry_nos)
            result = eval_single(
                test_lambda,
                submission_zip,
                test_dir,
                entry_nos,
                marks_mapping,
                patch,
                add_mem_info,
            )
            if isinstance(result, str):
                data = {}
                data["group_idx"] = submission_zip.stem
                for e in entry_nos:
                    data = {}
                    data["group_idx"] = group_idx
                    data["entry_no"] = e
                    data["error"] = result
                    data["total"] = 0
                    total_data.append(data)
                failed_dir.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(submission_zip, failed_dir / submission_zip.name)
            else:
                for e in entry_nos:
                    data = {}
                    data["group_idx"] = group_idx
                    data["entry_no"] = e
                    data["error"] = None
                    data |= result
                    total = 0
                    for k, v in result.items():
                        if k.endswith(".cmds") and is_number(v):
                            total += v
                    data["total"] = total
                    total_data.append(data)

        except Exception as e:
            for en in entry_nos:
                data = {}
                data["group_idx"] = group_idx
                data["entry_no"] = en
                data["error"] = str(e)
                data["total"] = 0
                failed_dir.mkdir(parents=True, exist_ok=True)
                shutil.copyfile(submission_zip, failed_dir / submission_zip.name)
                total_data.append(data)

    df = pd.DataFrame(total_data)
    df.to_csv(str(marks_csv), index=False)
