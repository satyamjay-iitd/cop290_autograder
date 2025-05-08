import subprocess
import shutil
import json
import tempfile
import os
import sys


def run_autograder(student_file, template_dir):
    # 1. Make a temporary directory
    with tempfile.TemporaryDirectory() as tempdir:
        # 2. Copy template project into tempdir
        shutil.copytree(template_dir, tempdir, dirs_exist_ok=True)

        # 3. Replace src/lib.rs with student's file
        src_lib = os.path.join(tempdir, "src", "lib.rs")
        shutil.copy(student_file, src_lib)

        # 4. Run cargo test with JSON output
        env = os.environ.copy()
        env["RUSTFLAGS"] = "-Awarnings"
        try:
            result = subprocess.run(
                ["cargo", "+nightly", "test", "hidden_tests", "--", "-Z", "unstable-options", "--format", "json"],
                cwd=tempdir,
                capture_output=True,
                text=True,
                timeout=2,
                env=env
            )
        except subprocess.TimeoutExpired:
            return 0, ["Test took more than 2 seconds"]


        # 6. Parse the JSON output
        failed = []
        passed = 0
        for line in result.stdout.splitlines():
            try:
                obj = json.loads(line)
            except json.JSONDecodeError:
                continue
            if obj.get("type") == "test":
                if obj.get("event") == "ok":
                    passed += 1
                if obj.get("event") == "failed":
                    failed.append(obj)

        # If failed is empty and no test cases passed => There was a compile error.
        if len(failed) == 0 and passed==0:
            return 0, [result.stderr]
        return passed, failed

if __name__ == "__main__":
    if len(sys.argv) != 3:
        print("Usage: python3 autograder.py <student_q1.rs> <total_tests>")

    student_file = sys.argv[1]
    template_dir = sys.argv[2]

    passed, failed = run_autograder(student_file, template_dir)
    print("Test cases passed:- ", passed)
    print("Failure reason:- ", failed)


