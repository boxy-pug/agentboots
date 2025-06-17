import os

MAX_CHARS = 10000


def get_files_info(working_directory, directory=None):

    try:
        if directory == None:
            directory = "."

        absolute_working_dir = os.path.abspath(working_directory)

        # If the directory argument is not a directory, again, return an error string:
        if not os.path.isdir(absolute_working_dir):
            return f'Error: "{directory}" is not a directory'

        absolute_list_dir = os.path.abspath(os.path.join(absolute_working_dir, directory))

        # If the directory argument is outside the working_directory, return a string with an error:
        if not absolute_list_dir.startswith(absolute_working_dir):
            return f'Error: Cannot list "{absolute_working_dir}" as it is outside the permitted working directory'

        if not os.path.isdir(absolute_list_dir):
            return f'Error: "{directory}" is not a directory'

        res = ""

        for entry in os.listdir(absolute_list_dir):
            abs_dir_entry = os.path.join(absolute_list_dir, entry)
            is_dir = os.path.isdir(abs_dir_entry)
            file_size = os.path.getsize(abs_dir_entry)
            res += f"- {entry}: file_size={file_size} bytes, is_dir={is_dir}\n"

        return res

    except Exception as e:
        return f"Error: {e}"


def get_file_content(working_directory, file_path):
    try:
        absolute_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(absolute_working_dir, file_path))

        if not absolute_file_path.startswith(absolute_working_dir):
            return f'Error: Cannot read "{absolute_file_path}" as it is outside the permitted working directory'

        if not os.path.isfile(absolute_file_path):
            return f'Error: File not found or is not a regular file: "{file_path}"'

        with open(absolute_file_path, "r") as f:
            file_content_string = f.read(MAX_CHARS)

            if len(file_content_string) == MAX_CHARS:
                file_content_string += (
                    f'[...File "{absolute_file_path}" truncated at 10000 characters]'
                )

        return file_content_string

    except Exception as e:
        return f"Error: {e}"


def write_file(working_directory, file_path, content):

    try:
        absolute_working_dir = os.path.abspath(working_directory)
        absolute_file_path = os.path.abspath(os.path.join(absolute_working_dir, file_path))

        if not absolute_file_path.startswith(absolute_working_dir):
            return f'Error: Cannot write to "{file_path}" as it is outside the permitted working directory'

        with open(absolute_file_path, "w") as f:
            f.write(content)

        return f'Successfully wrote to "{absolute_file_path}" ({len(content)} characters written)'

    except Exception as e:
        return f"Error: {e}"
