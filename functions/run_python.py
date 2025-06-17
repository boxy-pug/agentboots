import os
import subprocess


def run_python_file(working_directory, file_path):

    abs_working_dir = os.path.abspath(working_directory)
    abs_file_path = os.path.abspath(os.path.join(abs_working_dir, file_path))

    # print(f"abs work dir: {abs_working_dir}\nabs file path: {abs_file_path}")

    if not abs_file_path.startswith(abs_working_dir):
        return f'Error: Cannot execute "{file_path}" as it is outside the permitted working directory'

    if not os.path.exists(abs_file_path):
        return f'Error: File "{file_path}" not found.'

    if not abs_file_path.endswith(".py"):
        return f'Error: "{abs_file_path}" is not a Python file.'

    try:

        res = subprocess.run(["python3", abs_file_path], timeout=30, text=True, cwd=abs_working_dir)

        res_string = ""

        res_string += f"STDOUT: {res.stdout}\n"
        res_string += f"STDERR: {res.stderr}\n"

        if res.returncode != 0:
            res_string += f"Process exited with code {res.returncode}\n"

        if len(res_string) == 0:
            return "No output produced."

        return res_string

    except Exception as e:
        return f"Error: executing Python file: {e}"


