
import os

# End Goal: function to accept a directory path; return a string representing the contents of that directory
def get_files_info(working_directory: str, directory: str = ".") -> str:
    # The `directory` parameter (where the agent wants to scan) will be treated as a relative path
    # within the `working_directory` (that is set by us)
    abs_working_dir = os.path.abspath(working_directory)
    target_dir = os.path.normpath(os.path.join(abs_working_dir, directory))
    valid_target_dir = os.path.commonpath([abs_working_dir, target_dir]) == abs_working_dir
    try:
        
        if valid_target_dir is False:
            return IndexError(f'Error: Cannot list "{directory}" as it is outside the permitted working directory')
        
        if os.path.isdir(directory):
            for item in target_dir:
                dir_content = os.listdir(target_dir)
                dir_metadata = ()
                for thing in dir_content:
                    dir_metadata[thing] = [("file_size", os.path.getsize(thing)), ("is_dir",os.path.isdir(thing))]
                    return (dir_metadata)
            return (f'Success: "{directory}" is within the working directory')

        else:
            return ValueError(f'Error: "{directory}" is not a directory')
    
    except:
        return Exception('Error: Unknown standard library error')