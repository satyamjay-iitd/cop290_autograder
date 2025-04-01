"""
    This utilities are used to prepare the submission for evaluation.
"""
import shutil
from pathlib import Path
import os
import subprocess
import pandas as pd
import re


def extract_entry_no(zip_file: Path) -> list[str]:
    name = zip_file.stem
    entry_no_regex = r"20\d{2}\w{2,3}\d{4,5}"
    entry_nos = name.split("_")
    entry_nos = list(filter(lambda x: bool(re.fullmatch(entry_no_regex, x)), entry_nos))
    return entry_nos


def find_makefile(base_dir: Path) -> Path | None:
    for makefile in base_dir.rglob('Makefile'):
        return makefile.parent
    for makefile in base_dir.rglob('makefile'):
        return makefile.parent
    for makefile in base_dir.rglob('Makefile.txt'):
        return makefile.parent
    return None


def parse_marks_mapping(file: Path):
    df = pd.read_csv(file, header=None, names=['tc_name', 'marks', 'good_time', 'max_mem'])

    marks_mapping = df.set_index('tc_name').to_dict()
    return marks_mapping


def get_test_case_pairs(test_dir: Path):
    if test_dir.is_file():
        exp_file = test_dir.with_suffix(".exp")  # Change suffix to .exp
        return [(test_dir, exp_file)]

    test_cases = []

    # Find all .cmds files and map them to their corresponding .exp files
    for cmds_file in test_dir.rglob("*.cmds"):
        exp_file = cmds_file.with_suffix(".exp")  # Replace .cmds with .exp
        if exp_file.exists():
            test_cases.append((cmds_file, exp_file))

    test_cases.sort()
    return test_cases


"""
1. Builds the binary by running Make in the given
submission directory
2. Copies the binary to a temp directory
3. Returns the path to the binary.
"""
def build_binary(submission_dir: Path, entry_nos: list[str]) -> Path:
    output_dir = Path("/tmp/cop290/lab1_build/")

    output_dir.mkdir(parents=True, exist_ok=True)

    out_binary_name = "spreadsheet" + "_".join(entry_nos)

    try:
        subprocess.run(
            ["make"],
            cwd=submission_dir,
            check=True,
            stdout=subprocess.PIPE,
            stderr=subprocess.PIPE,
        )

        binary_path = submission_dir / "target" / "release" / "spreadsheet"
        if not os.path.exists(binary_path):
            raise FileNotFoundError(
                f"Expected binary '{out_binary_name}' not found in {submission_dir}/target/release"
            )

        shutil.copy2(binary_path, output_dir / out_binary_name)
    except subprocess.CalledProcessError as e:
        print(f"Make failed: {e.stderr.decode()}")
    except FileNotFoundError as e:
        print(f"Error: {e}")

    print(submission_dir)
    return output_dir / out_binary_name

