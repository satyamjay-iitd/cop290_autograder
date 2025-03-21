from datetime import datetime
import sys
from pathlib import Path
import pexpect
from rich.console import Console as RConsole
from rich.table import Table as RTable
import re
import zipfile
import shutil
import time


from runtime_utils import *
from compile_utils import *


prompt_regex = r"\[.*] ?\(.*\) ?> ?$"

# [0.00] (actual_status) > [0.00] (ok) >
status_line_regex = r"\(([^)]+)\)"


def get_status(status_line: str) -> bool:
    match = re.search(r"\(([^)]+)\)", status_line)
    if match:
        return "ok" in match.group(1)
    else:
        raise Exception("Unexpected status line")


console = RConsole()


"""Parse the .exp file"""


def parse_expected_file(file_nam: Path) -> list[ExpectedOutput]:
    with open(file_nam, "r", encoding="utf-8") as file_name:
        content = file_name.read()

    expected = []
    chunks = content.split("*******************\n")
    chunks = chunks[:-1]
    for chunk in chunks:
        lines = chunk.split("\n")
        lines = list(filter(lambda line: len(line) != 0, lines))

        # First line is status and time
        first_line = lines.pop(0)
        status, time = first_line.split()
        time = int(time)

        if len(lines) == 0:
            expected.append(ExpectedOutput(status == "ok", time, None))
        else:
            expected.append(ExpectedOutput(status == "ok", time, parse_table(lines)))

    return expected


"""
Waits for the prompt to appear, and return all the output
before, and after the prompt
"""
def read_till_prompt(child, timeout) -> tuple[str, str]:
    child.expect(prompt_regex, timeout=timeout)
    return child.before, child.after


"""
Runs the commands given in the command file.
"""
def run_test(bin_path: Path, cmd_file, exp_out_file):
    # Start the program
    log = open("/tmp/cop290_autograderlog.txt", "w")

    try:
        child = pexpect.spawn(
            str(bin_path), args=["999", "18278"], echo=False, encoding="utf-8"
        )
    except:
        return TestResult(is_pass=False, reason="Couldn't spawn the program")
    child.logfile_read = log

    # Expect the spreadsheet that is printed at the start of the program
    try:
        read_till_prompt(child, 2)
    except:
        return TestResult(is_pass=False, reason="Couldn't read the initial prompt")

    # Read the command file
    f = open(cmd_file, "r")
    commands = f.readlines()
    exp_tables = parse_expected_file(exp_out_file)
    assert len(commands) == len(
        exp_tables
    ), f"Error in test case len(commands)={len(commands)}, len(exp_tables)={len(exp_tables)}"

    # Feed the commands one by one to the program
    start = datetime.now()
    for i, (cmd, exp) in enumerate(zip(commands, exp_tables)):
        if (i + 1) % 1000 == 0:
            end = datetime.now()
            print(f"Ran {i} commands in {(end-start).total_seconds()} secs")
            start = datetime.now()

        # Feed command
        child.sendline(cmd)
        time.sleep(0.1)

        # Wait for the prompt to appear and read all the output before it.
        try:
            output, status_line = read_till_prompt(child, timeout=exp.time + 0.2)
            # Status line is in the following format:-
            # [0.00] (ok) > [0.00] (ok) >
            status_line = status_line.lower()
            status_is_ok = get_status(status_line)
        except pexpect.exceptions.TIMEOUT:
            diff = Diff(time_diff=(cmd.strip(), exp.time))
            child.sendline("q")
            print_diff(console, diff, cmd, exp.table, None)
            return TestResult(is_pass=False, reason="Time limit exceeded")
        except Exception as e:
            return TestResult(is_pass=False, reason=f"Couldn't send command {cmd.strip()} to the program")

        # Split the output by line.
        output_lines = output.split("\r\n")

        # Remove empty lines
        output_lines: list[str] = list(filter(lambda x: x != "", output_lines))

        # parse into Table
        student_table = parse_table(output_lines)
        # diff with expected table
        diff = compute_diff(exp, student_table, status_is_ok)
        if diff is not None:
            child.sendline("q")
            print_diff(console, diff, cmd, exp.table, student_table)
            return TestResult(is_pass=False, reason="Output Incorrect")

    # Quit the program
    child.sendline("q")
    return TestResult(is_pass=True, reason="")



if __name__ == "__main__":
    try:
        # /blah/blah/lab1_entry1_entry2_entry_3
        mode = sys.argv[1]
        submission = Path(sys.argv[2])
        test_dir = Path(sys.argv[3])
        marks_mapping = Path(sys.argv[4])
    except:
        print("Usage: python main.py [mode] [submission_dir] [test_dir] [marks_mapping]")
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
        eval_batch(run_test, submission, test_dir, marks_mapping, "~/lab1_marks.csv")
    elif mode == "single":
        entry_nos = submission.name.split("_")[1:]
        eval_single(run_test, submission, test_dir, entry_nos, marks_mapping)
