#!/usr/bin/env python3
import sys
import subprocess
import os
import csv
import difflib

def compile_source(source_file):

    compile_cmd = ["gcc", source_file, "-o", "submission"]
    try:
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # print("Compilation successful.")
        return True
    except subprocess.CalledProcessError as e:
        # print("Compilation failed!")
        # print(e.stderr)
        # sys.exit(1)
        return False

def normalize_output(output):

    return output.strip().lower()

def diff_outputs(expected, actual):

    expected_lines = expected.strip().splitlines()
    actual_lines = actual.strip().splitlines()
    diff = difflib.unified_diff(expected_lines, actual_lines, fromfile='expected', tofile='actual', lineterm='')
    return "\n".join(diff)

def run_test(test_input, expected_output,timeout=5):

    if type(test_input) != str:
        test_input=test_input()
    try:
        result = subprocess.run(["./submission"],
                                input=test_input,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=timeout)
    except subprocess.TimeoutExpired:
        # print("Test timed out.")
        return False, "Test timed out."
    
    actual_output = result.stdout
    if normalize_output(actual_output) == normalize_output(expected_output):
        return True, actual_output
    else:
        return False, actual_output
    
def evaluate_tests(test_set):
    score = 0.0
    remarks = ""
    # marks_each = (10.0 / len(test_set)) /2   # Each set contributes half (max total=10; each set max=5)
    marks_each = 0.5
    
    for idx, test in enumerate(test_set, start=1):
        passed, output = run_test(test["input"], test["expected"], test["timeout"])
        if passed:
            score += marks_each
        else:
            remarks += f"Test {idx} failed. Expected '{test['expected']}', got '{output}'.\n"
    
    return score, remarks

def run_tests():

    # tests = [
    #     {"input": "4\n3\n0 1\n1 2\n2 3\n", "expected": "no","timeout": 5},
    #     {"input": "6\n3\n0 1\n2 3\n4 5\n", "expected": "no","timeout": 5},
    #     {"input": "6\n4\n0 1\n1 2\n2 0\n3 4\n", "expected": "yes","timeout": 5},
    #     {"input": "5\n5\n0 1\n1 2\n2 3\n3 4\n4 1\n", "expected": "yes","timeout": 5},
    #     {"input": "10\n9\n0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n", "expected": "no","timeout": 5},
    #     {"input": "10\n10\n0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 0\n", "expected": "yes","timeout": 5},
    #     {"input": lambda file="tc1.txt": open(file, 'r').read(), "expected": "no", "timeout": 20},
    #     {"input": lambda file="tc2.txt": open(file, 'r').read(), "expected": "yes", "timeout": 20}
    # ]

    yes_tests = [
        {"input": "6\n4\n0 1\n1 2\n2 0\n3 4\n", "expected": "yes","timeout": 5},
        {"input": "5\n5\n0 1\n1 2\n2 3\n3 4\n4 1\n", "expected": "yes","timeout": 5},
        {"input": "10\n10\n0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n9 0\n", "expected": "yes","timeout": 5},
        {"input": "7\n7\n0 1\n1 2\n2 0\n3 4\n4 5\n5 6\n6 0\n", "expected": "yes","timeout": 5},
        {"input": "7\n7\n0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 4\n", "expected": "yes","timeout": 5},
        {"input": "7\n7\n0 1\n1 2\n2 3\n3 4\n4 2\n5 6\n6 0\n", "expected": "yes","timeout": 5},
        {"input": "8\n8\n0 1\n1 2\n2 3\n3 4\n4 1\n5 6\n6 7\n7 0\n", "expected": "yes","timeout": 5},
        {"input": lambda file="tc2.txt": open(file, 'r').read(), "expected": "yes", "timeout": 20}

    ]

    no_tests = [
        {"input": "4\n3\n0 1\n1 2\n2 3\n", "expected": "no","timeout": 5},
        {"input": "6\n3\n0 1\n2 3\n4 5\n", "expected": "no","timeout": 5},
        {"input": "10\n9\n0 1\n1 2\n2 3\n3 4\n4 5\n5 6\n6 7\n7 8\n8 9\n", "expected": "no","timeout": 5},
        {"input": "6\n4\n0 1\n2 3\n3 4\n4 5\n", "expected": "no","timeout": 5},
        {"input": "7\n5\n0 1\n1 2\n2 3\n3 4\n4 5\n", "expected": "no","timeout": 5},
        {"input": "8\n6\n0 1\n1 2\n7 8\n3 4\n4 5\n5 6\n", "expected": "no","timeout": 5},
        {"input": "8\n6\n0 1\n1 2\n2 3\n3 4\n7 8\n5 6\n", "expected": "no","timeout": 5},
        {"input": lambda file="tc1.txt": open(file, 'r').read(), "expected": "no", "timeout": 20}
    ]
    
    # total_score = 0.0
    # marks_each = 0.5
    # remarks=""
    
    # for idx, test in enumerate(tests, start=1):
    #     passed, output = run_test(test["input"], test["expected"])
    #     if passed:
    #         # print(f"Test case {idx} passed.")
    #         total_score += marks_each
    #     else:
    #         remarks+=f"Test case {idx} failed.\nInput:    {repr(test['input'])}\n\
    #         Expected: {repr(test['expected'])}\nGot:      {repr(output.strip())}"
    #         # print("  Diff:")
    #         # print(diff_outputs(test["expected"], output))
    
    # return total_score,remarks

    yes_score, yes_remarks = evaluate_tests(yes_tests)
    no_score, no_remarks = evaluate_tests(no_tests)

    final_score = min(yes_score, no_score)

    remarks = ""
    if yes_score != no_score:
        remarks += f"Score imbalance detected: YES-tests={yes_score}, NO-tests={no_score}. Taking minimum.\n"
    
    remarks += "\nYES-test remarks:\n" + yes_remarks + "\nNO-test remarks:\n" + no_remarks

    # Cleanup executable after evaluation
    if os.path.exists("submission"):
        os.remove("submission")

    return final_score, remarks.strip()


# def write_csv(submission_id, score, csv_filename="resultsq3.csv"):
#     """
#     Appends the submission identifier and score to a CSV file.
#     If the file does not exist, it creates one with a header row.
#     """
#     file_exists = os.path.exists(csv_filename)
#     try:
#         with open(csv_filename, "a", newline="") as csvfile:
#             writer = csv.writer(csvfile)
#             if not file_exists:
#                 writer.writerow(["submission", "marks"])
#             writer.writerow([submission_id, score])
#         # print(f"Results appended to {csv_filename}.")
#     except Exception as e:
#         print(f"Error writing to CSV file: {e} for submission_id: {submission_id}")

def write_csv(submission_id, score, csv_filename="resultsq3.csv"):
    """
    Appends the submission identifier and score to a CSV file.
    If the file does not exist, it creates one with a header row.
    Also writes the grade to a text file 'gradeq3.txt' (overwriting each time).
    """
    file_exists = os.path.exists(csv_filename)
    try:
        with open(csv_filename, "a", newline="") as csvfile:
            writer = csv.writer(csvfile)
            if not file_exists:
                writer.writerow(["submission", "marks"])
            writer.writerow([submission_id, score])
        
        # Write the score to a text file (overwrite each time)
        with open("gradeq3.txt", "w") as grade_file:
            grade_file.write(str(score))

    except Exception as e:
        print(f"Error writing to file: {e} for submission_id: {submission_id}")


def remove_executable():
    """
    Removes the generated 'submission' executable if it exists.
    """
    if os.path.exists("submission"):
        os.remove("submission")

def main():
    if len(sys.argv) < 2:
        print("Usage: python autograder.py <source_file.c> [submission_id]")
        sys.exit(1)
    
    source_file = sys.argv[1]
    submission_id = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(source_file)
    

    compiled=compile_source(source_file)
    
    if compiled:
        score,remarks = run_tests()
        remove_executable()
        # print(f"\nFinal Score: {score:.2f} / 4.0")
    else:    
        score,remarks=0.0,"Failed to Compile"
        
    # write_csv(submission_id, score)
    print(score)
    print(remarks)

if __name__ == "__main__":
    main()
