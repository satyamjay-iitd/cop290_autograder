# COP290 Lab1 Autograder

## Prerequisite
1. Python3.12 (Might work on 3.10, 3.11 as well, haven't tested though)
2. Project directory:-
  a. Name should be of the form `lab1_entry1_entry2_entry3`
  b. Should contain a Makefile
  c. Running `make` inside the project directory should build a binary named `spreadsheet` in `{project_dir}/target/release`

## First time setup
1. `git clone TODO`
2. `cd lab1_autograder`
3. Create python virtualenv:- `python3.12 -m venv venv`
4. Activate environment:- `source venv/bin/activate`
5. Install dependencies:- `pip install -r requirements.txt`

## Run all tests in a directory
1. `python main.py {path_to_proj_dir} {path_to_test_dir}`

## Run single test
1. `python main.py {path_to_proj_dir} {path_to_test_dir}/x.cmds`

### Play demo
1. Install [asciinema](https://docs.asciinema.org/getting-started/)
2. Run `asciinema play demo.cast`


## Notes on test cases
Every test X has 2 components:- `x.cmds` and `x.exp`. `x.cmds` is the input to
your program. And `x.exp` is the expected output.

### .exp file format
The file follows a structured layout with three distinct sections: metadata, spreadsheet data, and a separator.

#### File Structure

An example file might look like this:

```
ok 0
    ZZZ
999 -5
*****************
```

#### 1. First Line: Metadata
The first line consists of two parts:

```
[status] [exp_time]
```

- **`status`**: A string indicating status of the command. Common values might include:
  - `ok`: Indicates a successful operation.
  - `error`: Indicates a failure or issue.
- **`exp_time`**: A numeric value, expected time that should be taken to run the commands .

**Example:**
```
ok 0
```
- Here, `ok` signifies success, and `0` indicate that running this command should take 0 seconds.

#### 2. Middle Section: Spreadsheet Data
This section contains tabular data that appears similar to a spreadsheet. This section could also be empty
if output has been disabled.
```
    ZZZ
999 -5
```
- **`ZZZ`**: This is column header.
- **`999 -5`**: Represents a row of data with values separated by spaces.

#### 3. Last Line: Separator
The final line consists of a sequence of asterisks (`*`):

```
*****************
```
- This serves as a **seperation marker** between outputs of diferent commands .


## Adding test cases
If you want to share your own interesting test cases with your classmates, feel free
to add them in `students_tests` directory, and raise a PR. Please follow the format above. 


## Bug in autograder
If you find any bug in the autograder, you can either fix it and raise a PR, or
create an issue on [github](https://github.com/satyamjay-iitd/cop290_autograder/issues), I
will try to fix it ASAP.


# Submission instructions
1. Zip your project directoy
`zip -r lab1_entry1_entry2.zip lab1_entry1_entry2 -x "lab1_entry1_entry2/target/*"`
Note that this is the same directory that you passed to the test script.
2. Submit on moodle.


TA TODOs:-

Testcases:-
  1. ~~stddev~~
  1. ~~avg~~
  2. div/0
  3. scroll
  4. cyclic dependency
  5. range
