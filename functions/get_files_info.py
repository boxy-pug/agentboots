import os


def get_files_info(working_directory, directory=None):

    try:
        if directory == None:
            directory = "."

        absolute_working_dir = os.path.abspath(working_directory)

        # If the directory argument is not a directory, again, return an error string:
        if not os.path.isdir(absolute_working_dir):
            return f'Error: "{directory}" is not a directory'

        absolute_list_dir = os.path.join(absolute_working_dir, directory)

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
            res += f'- {entry}: file_size={file_size} bytes, is_dir={is_dir}\n'

        return res

    except Exception as e:
        return f"Error: {e}"

    '''
    - README.md: file_size=1032 bytes, is_dir=False
    - src: file_size=128 bytes, is_dir=True
    - package.json: file_size=1234 bytes, is_dir=False
    '''
