# COP290 Lab1 Autograder

# New Instructions

## Prerequisite
1. Ubuntu (Might work on Windows-WSL and MacOs too, haven't tested)
2. Python3.12 (Might work on 3.10, 3.11 as well, haven't tested though)

## First time setup
1. `git clone https://github.com/satyamjay-iitd/cop290_autograder`
2. `cd lab1_autograder`
3. Create python virtualenv:- `python3.12 -m venv venv`
4. Activate environment:- `source venv/bin/activate`
5. Install dependencies:- `pip install -r requirements.txt`

## Running Autograder
1. For Easy Test Cases, Run `python main.py binary <path_to_your_sheet_binary> hidden_tc/ marks_mapping.csv`
2. For example, `python main.py binary /home/satyam/dev/CProjects/sheet hidden_tc/ marks_mapping.csv`
3. For Hard Test Cases, Run `python main2.py binary <path_to_your_sheet_binary> hidden_tc2/ marks_mapping.csv`
4. You can ignore `hidden_tc3`. This is not being used.
5. Testcase to Marks mapping is given in `marks_mapping.csv`, where the first column is the test case; second is marks allotted if the test passes; third column is maximum time allowed for your program to run, if your program doesn't finish in this time, the test case will considered to be failing. You can ignore the fourth column.

# Old Instructions (Abu Dhabi Student should ignore)

## Play demo
1. Install [asciinema](https://docs.asciinema.org/getting-started/)
2. Run `asciinema play autograder.cast`

## Prerequisite
1. Ubuntu (Might work on Windows-WSL and MacOs too, haven't tested)
2. Python3.12 (Might work on 3.10, 3.11 as well, haven't tested though)
3. gcc-11 to compile your project
4. Project zip that you submitted on the moodle

## First time setup
1. `git clone https://github.com/satyamjay-iitd/cop290_autograder`
2. `cd lab1_autograder`
3. Create python virtualenv:- `python3.12 -m venv venv`
4. Activate environment:- `source venv/bin/activate`
5. Install dependencies:- `pip install -r requirements.txt`

## Two types of testers:-

### `main.py`
`main.py`: uses pexpect and is ideal for small testcases. Test cases tested using this
tester is located here:- `hidden_tc/`

### Run all tests in a directory
`python main.py single {path_to_zip_file} hidden_tc/ marks_mapping.csv`

### Run single test
`python main.py single {path_to_zip_file} hidden_tc/*/*.cmds marks_mapping.csv`


### `main2.py`
`main2.py`: parses just the final output and checks total runtime and memory. It is used for test
cases with lot of commands (> 1000).
Test cases tested using this tester is located here:- `hidden_tc2/`

### Run all tests in a directory
`python main2.py single {path_to_zip_file} hidden_tc2/ marks_mapping.csv`

### Run single test
`python main2.py single {path_to_zip_file} hidden_tc2/*/*.cmds marks_mapping.csv`
