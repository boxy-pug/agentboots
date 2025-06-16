'''
Create a new tests.py file in the root of your project. When executed directly, it should:

    Run get_files_info("calculator", ".") and print the result to the console.
    Run get_files_info("calculator", "pkg") and print the result to the console.
    Run get_files_info("calculator", "/bin") and print the result to the console (this should return an error string)
    Run get_files_info("calculator", "../") and print the result to the console (this should return an error string)

'''

# from subdirectory.filename import function_name
from functions.get_files_info import get_files_info

def testGetFiles():
    result = get_files_info("calculator", ".")
    print(result)

    result = get_files_info("calculator", "pkg")
    print(result)

    result = get_files_info("calculator", "/bin")
    print(result)

    result = get_files_info("calculator", "../")
    print(result)

if __name__ == "__main__":
    # call your function here
    testGetFiles()
