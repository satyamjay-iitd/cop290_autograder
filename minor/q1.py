#!/usr/bin/env python3
import sys
import subprocess
import os
import csv

# -------------------------------
def compile_source(source_file):
    """
    Compiles the submitted C source file into an executable named 'submission1'.
    """
    compile_cmd = ["gcc", source_file, "-o", "submission1"]
    try:
        subprocess.run(compile_cmd, check=True, stdout=subprocess.PIPE, stderr=subprocess.PIPE, text=True)
        # print("Compilation successful.")
        return True
    except subprocess.CalledProcessError as e:
        # print("Compilation failed!")
        # print(e.stderr)
        # sys.exit(1)
        return False

# -------------------------------
def run_test(test_input, expected_outputs):
    """
    Runs 'submission' with test_input supplied on stdin.
    Compares the stdout (after stripping extra spaces/newlines) with expected_outputs.
    Returns (passed:bool, actual_output:str)
    """
    try:
        result = subprocess.run(["./submission1"],
                                input=test_input,
                                stdout=subprocess.PIPE,
                                stderr=subprocess.PIPE,
                                text=True,
                                timeout=5)
    except subprocess.TimeoutExpired:
        # print("Test timed out.")
        return False, "Test timed out."
    
    actual = result.stdout.strip()
    expecteds = [expected_output.strip() for expected_output in expected_outputs]
    return (actual in expecteds), actual

# -------------------------------
def run_tests():
    """
    Runs four test cases for Question 1:
        Input: "4+5"    Expected output: "9"
        Input: "2*5"    Expected output: "10"
        Input: "3-2"    Expected output: "-1"
        Input: "100/20"   Expected output: "5"
    Each test case carries 0.5 marks.
    Returns total score (max = 2.0) and remarks
    """
    tests = [
        {"input": "4\n+\n5\n",  "expected": ["9"],},
        {"input": "2\n*\n5\n",  "expected": ["10"]},
        {"input": "2\n-\n3\n",  "expected": ["-1"]},
        {"input": "100\n/\n20\n", "expected": ["5"]} #either is accepted
    ]
    
    score = 0.0
    marks_each = 0.5
    remarks=""
    
    for i, test in enumerate(tests, start=1):
        passed, output = run_test(test["input"], test["expected"])
        if passed:
            # print(f"Test case {i} passed.")
            score += marks_each
        else:
            remarks+=f"Test case {i} failed.\nInput:    {repr(test['input'])}\
                        \nExpected: {repr(test['expected'])}\nGot:      {repr(output)}\n\n"
    return score,remarks

# -------------------------------
# def write_csv(submission_id, score, remarks,csv_filename="resultsq1.csv"):
#     """
#     Appends a record with submission_id and score into a CSV file.
#     If the file does not exist, a header row is added.
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

def write_csv(submission_id, score, remarks, csv_filename="resultsq1.csv"):
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
        with open("gradeq1.txt", "w") as grade_file:
            grade_file.write(str(score))

    except Exception as e:
        print(f"Error writing to file: {e} for submission_id: {submission_id}")


# -------------------------------
def remove_executable():
    """
    Removes the generated 'submission' executable.
    """
    if os.path.exists("submission1"):
        os.remove("submission1")

# -------------------------------
def main():
    if len(sys.argv) < 2:
        print("Usage: python autograder.py <submission.c> [submission_id]")
        sys.exit(1)
    
    source_file = sys.argv[1]
    submission_id = sys.argv[2] if len(sys.argv) > 2 else os.path.basename(source_file)
    

    compiled=compile_source(source_file)
    
    if compiled:
        total_score,remarks = run_tests()
        remove_executable()
        # print(f"Final Score: {total_score:.2f} / 2.00")
    else:
        total_score,remarks=0.0,"Failed to Compile"
    print(f"Total Score: {total_score:.2f}, {remarks}")
    # write_csv(submission_id, total_score,remarks)

if __name__ == "__main__":
    main()
