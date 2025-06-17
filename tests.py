'''
Create a new tests.py file in the root of your project. When executed directly, it should:

    Run get_files_info("calculator", ".") and print the result to the console.
    Run get_files_info("calculator", "pkg") and print the result to the console.
    Run get_files_info("calculator", "/bin") and print the result to the console (this should return an error string)
    Run get_files_info("calculator", "../") and print the result to the console (this should return an error string)


# from subdirectory.filename import function_name

def testGetFiles():
    result = get_files_info("calculator", ".")
    print(result)

    result = get_files_info("calculator", "pkg")
    print(result)

    result = get_files_info("calculator", "/bin")
    print(result)

    result = get_files_info("calculator", "../")
    print(result)

    Update your tests.py file. Remove all the calls to get_files_info, and instead test get_file_content("calculator", "lorem.txt"). Ensure that it truncates properly.
Remove the lorem ipsum test, and instead test the following cases:

    get_file_content("calculator", "main.py")
    get_file_content("calculator", "pkg/calculator.py")
    get_file_content("calculator", "/bin/cat") (this should return an error string)


# from calculator.pkg import calculator
from functions.get_files_info import write_file

def testWriteFile():
    res = write_file("calculator", "lorem.txt", "wait, this isn't lorem ipsum")
    print(res)

    res = write_file("calculator", "pkg/morelorem.txt", "lorem ipsum dolor sit amet")
    print(res)

    res = write_file("calculator", "/tmp/temp.txt", "this should not be allowed")
    print(res)

'''

from functions.run_python import run_python_file

def testRunPythonFile():

    res = run_python_file("calculator", "main.py")
    print(res)

    res = run_python_file("calculator", "tests.py")
    print(res)

    res = run_python_file("calculator", "../main.py") 
    print(res)

    res = run_python_file("calculator", "nonexistent.py") 
    print(res)


if __name__ == "__main__":
    # call your function here
    testRunPythonFile()


