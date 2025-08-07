# denote the directory with "."
# this file is being run from the root dir of our project. You only need a relative name
# fyi current dir is a dot
from functions.get_file_content import get_file_content
from functions.write_file import write_file


def test():
    file_1 = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    file_2 = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum color sit amet")
    file_3 = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(file_1)
    print(file_2)
    print(file_3)




if __name__ == "__main__":
    test()
