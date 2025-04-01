# This script is to test testcases with large number of commands
# It assumes that only final command will produce the output and
# compares only that.

from pathlib import Path
import psutil
import subprocess
import time
import sys
from datetime import datetime
from compile_utils import *
from runtime_utils import *


def parse_exp_file(exp_file: Path):
    with open(exp_file) as f:
        rows = f.readlines()
        timeout = int(rows[0])
        rows = rows[1:]
        num_cols = -1
        table = []
        for row in rows:
            # First cell is row_idx, ignore that
            cells = list(map(lambda x: int(x), row.split()[1:]))
            if num_cols == -1:
                num_cols = len(cells)
            else:
                assert len(cells), num_cols

            table.append(cells)

        return timeout, table, num_cols


def parse_out_file(out_file: Path, num_rows: int):
    with open(out_file) as f:
        rows = f.readlines()
        rows = rows[-(num_rows + 1) : -1]
        num_cols = -1
        num_rows = len(rows)
        table = []
        for row in rows:
            # First cell is row_idx, ignore that
            try:
                cells = list(map(lambda x: int(x), row.split()[1:]))
            except Exception as e:
                print(rows)
                print(len(rows))
                raise e
            if num_cols == -1:
                num_cols = len(cells)
            else:
                assert len(cells), num_cols

            table.append(cells)

        return table


def compare_table(table1, table2) -> bool:
    if len(table1) != len(table2):
        return False
    for row1, row2 in zip(table1, table2):
        if row1 != row2:
            return False
    return True


MAX_MEM_M = 2048
"""
Runs the commands given in the command file.
"""
def run_test(bin_path: Path, cmd_file, exp_out_file, marks_mapping) -> TestResult:
    exp_timeout, exp_table, num_cols = parse_exp_file(exp_out_file)
    out_file = Path("/tmp/out.txt")
    outerr_file = Path("/tmp/outerr.txt")
    max_mem_usage_gb = 0

    if out_file.exists():
        out_file.unlink()
    with open(out_file, "w") as f:
        start_time = time.time()
        try:
            # Read the file and skip the first line
            with open(cmd_file) as f1:
                lines = f1.readlines()
                num_rows, num_cols = list(map(lambda x: int(x), lines[0].split()))
                commands = "\n".join(lines[1:])

            temp_in_file = open("/tmp/in.cmds", "w")
            for line in commands:
                temp_in_file.write(f"{line}")
            temp_in_file.close()
            temp_in_file = open("/tmp/in.cmds", "r")

            """
                systemd-run --scope --user -p MemoryMax=1G -- /target/release/spreadsheet 999 18278
            """
            process = subprocess.Popen(
                ["systemd-run", "--scope", "--user", "-p", f"MemoryMax={MAX_MEM_M}M", "--", str(bin_path), str(num_rows), str(num_cols)],
                stdin=temp_in_file,
                stdout=f,
                stderr=open(outerr_file, "w"),
            )

            ps_process = psutil.Process(process.pid)
            while process.poll() is None:
                mem_info = ps_process.memory_info()
                max_mem_usage_mb = max(max_mem_usage_gb, mem_info.vms / 2**20)
                if max_mem_usage_mb >= MAX_MEM_M:
                    return TestResult(is_pass=False, reason="Mem limit exceed", time_taken_s=(time.time() - start_time)*1000, max_mem_gb=max_mem_usage_gb, marks=0)
                if (time.time() - start_time) > exp_timeout:
                    return TestResult(is_pass=False, reason="Timeout", time_taken_s=(time.time() - start_time)*1000, max_mem_gb=max_mem_usage_gb, marks=0)
                time.sleep(0.001)
            
            process.wait()
            process.kill()
        except FileNotFoundError:
            return TestResult(is_pass=False, reason="Compilation error", marks=0)
        f.flush()

    out_table = parse_out_file(out_file, len(exp_table))
    if not compare_table(exp_table, out_table):
        return TestResult(is_pass=False, reason="Wrong output", marks=0)
    marks = marks_mapping['marks'][cmd_file]
    return TestResult(is_pass=True, time_taken_s=(time.time() - start_time)*1000, max_mem_gb=max_mem_usage_gb, marks=marks)


# if __name__ == "__main__":
#     try:
#         # /blah/blah/lab1_entry1_entry2_entry_3
#         submission_dir = Path(sys.argv[1])
#         test_dir = Path(sys.argv[2])

#         entry_nos = submission_dir.name.split("_")[1:]
#         assert submission_dir.is_dir(), "Must be a directory"
#         assert submission_dir.exists(), "Directory must exist"
#     except:
#         print("Usage: python main.py [submission_dir] [test_dir]")
#         exit(1)

#     bin_path = build_binary(submission_dir, entry_nos)
#     test_cases = get_test_case_pairs(test_dir)

#     verdict = []
#     for cmd, expected in test_cases:
#         console.print(f"Running {cmd}")
#         result = run_test(bin_path, cmd, expected)
#         verdict.append((cmd, result))

#     table = RTable()

#     table.add_column("Test Case", justify="right", style="cyan", no_wrap=True)
#     table.add_column("Verdict", justify="right", style="cyan", no_wrap=True)
#     for test, result in verdict:
#         if result.p:
#             table.add_row(str(test), "PASS", style="green")
#         elif result.f_timeout:
#             table.add_row(str(test), "FALSE: TIMEOUT", style="red")
#         elif result.f_wrong_out:
#             table.add_row(str(test), "FALSE: WRONG OUT", style="red")
#         else:
#             assert False
#     console.print(table)


if __name__ == "__main__":
    try:
        # /blah/blah/lab1_entry1_entry2_entry_3
        mode = sys.argv[1]
        submission = Path(sys.argv[2])
        test_dir = Path(sys.argv[3])
        marks_mapping = Path(sys.argv[4])
        try:
            apply_patch = bool(sys.argv[5])
        except:
            apply_patch = False
    except:
        print(
            "Usage: python main.py [mode] [submission_dir] [test_dir] [marks_mapping]"
        )
        exit(1)

    assert mode == "batch" or mode == "single"
    if mode == "batch":
        assert submission.is_dir(), "Must be a directory"
        assert submission.exists(), "Directory must exist"
    else:
        assert submission.is_file(), "Must be a zip file"
        assert submission.exists(), "Zip file must exist"

    # tc_name -> marks
    marks_mapping = parse_marks_mapping(marks_mapping)
    if mode == "batch":
        eval_batch(run_test, submission, test_dir, marks_mapping, Path("~/lab1_marks3.csv"), True, patch=apply_patch)
    elif mode == "single":
        entry_nos = submission.name.split("_")[1:]
        eval_single(run_test, submission, test_dir, entry_nos, marks_mapping,  patch=apply_patch)
