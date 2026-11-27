
import os

# End Goal: function to accept a directory path; return a string representing the contents of that directory
def get_files_info(working_directory: str, directory: str = ".") -> str:
    # The `directory` parameter (where the agent wants to scan) will be treated as a relative path
    # within the `working_directory` (that is set by us)
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    try:
        if directory == ".":
            dir_name = "current directory"
        else:
            dir_name = directory
        list_file_results: str = (f'''Results for {dir_name} directory:''')

        if valid_target_dir is False:
            invalid_target_result = list_file_results + (f'\n    Error: Cannot list "{directory}" as it is outside the permitted working directory')
            print(invalid_target_result)
        
        if os.path.isdir(directory):           
            dir_content = os.listdir(target_dir)
            for thing in dir_content:
                thing_results = list_file_results + (f'\n    - {thing}: file_size={os.path.getsize(thing)} bytes, is_dir={os.path.isdir(thing)}')
                print(thing_results)
        else:
            invalid_dir_result = list_file_results + (f'\n    Error: "{directory}" is not a directory')
            print(invalid_dir_result)
    
    except:
        return Exception('Error: Unknown standard library error')
    
    