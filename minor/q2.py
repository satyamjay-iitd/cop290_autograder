#!/usr/bin/env python3
import sys
import subprocess
import os
import csv
import difflib

def compile_source(source_file):
    """Compiles the submitted C source file into an executable named 'submission2'."""
    compile_cmd = ["gcc", source_file, "-o", "submission2"]
    try:
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # print("Compilation successful.")
        return True
    except subprocess.CalledProcessError as e:
        # print("Compilation failed!")
        # print(e.stderr)
        # sys.exit(1)
        return False

def diff_outputs(expected, actual):
    """Return a unified diff between expected and actual outputs."""
    expected_lines = expected.strip().splitlines()
    actual_lines = actual.strip().splitlines()
    diff = difflib.unified_diff(expected_lines, actual_lines, fromfile='expected', tofile='actual', lineterm='')
    return "\n".join(diff)

def run_test(test_arg, expected_output):
    """
    Runs the executable 'submission' with the given test argument (as a command-line argument).
    It compares the trimmed stdout with the expected output.
    Returns (passed: bool, actual_output: str).
    """
    try:
        result = subprocess.run(["./submission2", test_arg],
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=5)
    except subprocess.TimeoutExpired:
        # print(f"Test with argument '{test_arg}' timed out.")
        return False, "Test timed out."
    
    actual = result.stdout.strip()
    expected = expected_output.strip()
    return (actual == expected), actual

def run_tests():
    """
    Runs 10 test cases for Question 2 with the following mapping:

        Input    Expected Output
        "A"      "0"
        "Z"      "25"
        "AA"     "26"
        "AZ"     "51"
        "ZZ"     "701"
        "AAA"    "702"
        "0"      "A"
        "100"    "CV"
        "701"    "ZZ"
        "728"    "AAB"
    
    Each test carries 0.5 marks.
    Returns the total score (max = 5.0).
    """
    tests = [
        {"input": "B",   "expected": "1"},
        {"input": "Z",   "expected": "25"},
        {"input": "AB",  "expected": "27"},
        {"input": "AZ",  "expected": "51"},
        {"input": "ZZ",  "expected": "701"},
        {"input": "AAA", "expected": "702"},
        {"input": "0",   "expected": "A"},
        {"input": "24", "expected": "Y"},
        {"input": "6", "expected": "G"},
        {"input": "728", "expected": "ABA"},
    ]
    
    score = 0.0
    marks_each = 0.5
    remarks = ""
    
    for i, test in enumerate(tests, start=1):
        passed, actual_output = run_test(test["input"], test["expected"])
        if passed:
            # print(f"Test case {i} with argument '{test['input']}' passed.")
            score += marks_each
        else:
            remarks+=f"Test case {i} with argument '{test['input']}' failed.\n\
                        Expected:{repr(test['expected'])}\nGot:     {repr(actual_output)}\n\n"
                        # Diff:\n{diff_outputs(test['expected'], actual_output)}\n\n"
    return score,remarks

# def write_csv(submission_id, score, remarks, csv_filename="resultsq2.csv"):
#     """
#     Appends a record with submission_id and score into a CSV file.
#     Creates a header row if the file does not already exist.
#     """
#     file_exists = os.path.exists(csv_filename)
#     try:
#         with open(csv_filename, "a", newline="") as csvfile:
#             writer = csv.writer(csvfile)
#             if not file_exists:
#                 writer.writerow(["submission", "marks","remarks"])
#             writer.writerow([submission_id, score,remarks])
#         # print(f"Results appended to {csv_filename}.")
#     except Exception as e:
#         print(f"Error writing to CSV file: {e} for submission_id: {submission_id}")


def write_csv(submission_id, score, remarks, csv_filename="resultsq2.csv"):
    """
    Appends a record with submission_id and score into a CSV file.
    If the file does not exist, a header row is added.
    Also writes the grade to a text file 'gradeq1.txt' (overwriting each time).
    """
    file_exists = os.path.exists(csv_filename)
    try:
        with open(csv_filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["submission", "marks", "remarks"])
            writer.writerow([submission_id, score, remarks])
        
        # Write the score to a text file (overwrite each time)
        with open("gradeq2.txt", "w") as grade_file:
            grade_file.write(str(score))

    except Exception as e:
        print(f"Error writing to file: {e} for submission_id: {submission_id}")


def remove_executable():
    """Removes the generated 'submission' executable if it exists."""
    if os.path.exists("submission2"):
        os.remove("submission2")

def main():
    if len(sys.argv) < 2:
        print("Usage: python autograder.py <source_file.c> [submission_id]")
        sys.exit(1)
    
    source_file = sys.argv[1]

    submission_id = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(source_file)
    

    compiled=compile_source(source_file)
    
    if compiled:
        total_score,remarks = run_tests()
        remove_executable()
        # print(f"Final Score: {total_score:.2f} / 5.00")
    else:
        total_score,remarks = 0.0,"Failed to Compile"

    # write_csv(submission_id, total_score,remarks)
    print(total_score)

if __name__ == "__main__":
    main()
