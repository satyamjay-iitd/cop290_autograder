import os
import autograder
import pandas as pd
import tqdm

submissions_dir = "major_submissions"
# TODO: Currently all test in a question has equal weightage.
template_dirs = {
    "q1": ("major_templates/q1_template", 1, 1),
    "q2": ("major_templates/q2_template", 2, 3),
    "q3": ("major_templates/q3_template", 2, 2),
    "q4": ("major_templates/q4_template", 2, 2),
    "q5": ("major_templates/q5_template", 2, 2),
    "q6": ("major_templates/q6_template", 2, 3),
    "q7": ("major_templates/q7_template", 3, 6),
    "q8": ("major_templates/q8_template", 6, 37),
}

results = {}

for student_id in tqdm.tqdm(os.listdir(submissions_dir)):
    student_path = os.path.join(submissions_dir, student_id)
    if not os.path.isdir(student_path):
        continue

    results[student_id] = {}

    for question, (template_dir, marks, num_tests) in template_dirs.items():
        student_file = os.path.join(student_path, f"{question}.rs")
        # student_file = os.path.join("major_sol/", f"{question}.rs")

        if not os.path.exists(student_file):
            continue

        passed, failed_tests = autograder.run_autograder(student_file, template_dir)
        results[student_id][f"{question}_marks"] = (passed * marks) / num_tests
        results[student_id][f"{question}_failed_tests"] = failed_tests
    # break

df = pd.DataFrame(results)
df = df.transpose()  # swap rows and columns
df = df.reset_index().rename(columns={"index": "entry_no"})
df = df.fillna(0)

# print(df)
df["total"] = (
    df["q1_marks"]
    + df["q2_marks"]
    + df["q3_marks"]
    + df["q4_marks"]
    + df["q5_marks"]
    + df["q6_marks"]
    + df["q7_marks"]
    + df["q8_marks"]
)
df["feedback"] = f"""
----------------------------\n
Q1:
    {df["q1_failed_tests"]}
----------------------------\n
Q2:
    {df["q2_failed_tests"]}
----------------------------\n
Q3:
    {df["q3_failed_tests"]}
----------------------------\n
Q4:
    {df["q4_failed_tests"]}
----------------------------\n
Q5:
    {df["q5_failed_tests"]}
----------------------------\n
Q6:
    {df["q6_failed_tests"]}
----------------------------\n
Q7:
    {df["q7_failed_tests"]}
----------------------------\n
Q8:
    {df["q8_failed_tests"]}
----------------------------\n
# """
df = df.drop(
    columns=[
        "q1_failed_tests",
        "q2_failed_tests",
        "q3_failed_tests",
        "q4_failed_tests",
        "q5_failed_tests",
        "q6_failed_tests",
        "q7_failed_tests",
        "q8_failed_tests",
        "feedback"
    ]
)
df.to_excel("major_marks.xlsx")
df.to_csv("major_marks.csv")
