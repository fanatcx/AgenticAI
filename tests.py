# denote the directory with "."
# this file is being run from the root dir of our project. You only need a relative name
# fyi current dir is a dot
from functions.get_file_content import get_file_content


def test():
    output = get_file_content("calculator", "main.py")
    print(output)

    output = get_file_content("calculator", "pkg/calculator.py")
    print(output)

    output = get_file_content("calculator", "/bin/cat")
    print(output)

    output = get_file_content("calculator", "pkg/does_not_exist.py")
    print(output)


if __name__ == "__main__":
    test()
