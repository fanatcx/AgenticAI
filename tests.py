# denote the directory with "."
# this file is being run from the root dir of our project. You only need a relative name
# fyi current dir is a dot
from functions.get_file_content import get_file_content
from functions.write_file import write_file
from functions.run_python import run_python_file


def test():
    test1 = run_python_file("calculator", "main.py")
    test2 = run_python_file("calculator", "main.py", ["3 + 5"])
    test3 = run_python_file("calculator", "tests.py")
    test4 = run_python_file("calculator", "../main.py")
    test5 = run_python_file("calculator", "nonexistent.py")

    print(test1, test2, test3, test4, test5)

if __name__ == "__main__":
    test()
