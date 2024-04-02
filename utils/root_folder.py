import os.path
from utils.bcolors import bcolors as c

# Get the default Pictures directory
sys_home_folder = os.path.expanduser('~')
sys_pic_path = os.path.join(sys_home_folder, "Pictures")
default_folder_path = os.path.join(sys_pic_path, 'Check in-out Photos')

def get_root_folder_dir(dir_from_config: str):

    output_root_folder_dir = dir_from_config if dir_from_config else default_folder_path

    # If user specifies system Pictures as the path, just add the default sub-folder and don't do a "Picture 2" in user's folder
    output_root_folder_dir = default_folder_path if os.path.normpath(output_root_folder_dir) == os.path.normpath(sys_pic_path) else output_root_folder_dir

    # init and open output folder
    original_output_root_folder_dir = output_root_folder_dir
    output_folder_name_cnt = 0
    while os.path.exists(output_root_folder_dir):
        output_folder_name_cnt = output_folder_name_cnt + 1
        output_root_folder_dir = original_output_root_folder_dir + ' ' + str(output_folder_name_cnt + 1)

    if not os.path.exists(output_root_folder_dir):
        # Create the directory
        os.makedirs(output_root_folder_dir)
        print(f"> {c.OKGREEN}Directory created successfully for \"{output_root_folder_dir}\".{c.ENDC}")
        if output_folder_name_cnt > 0:
            print(f"> {c.FAIL}Note that directory {c.BOLD}\"{output_root_folder_dir}\"{c.ENDC}{c.FAIL} is different from your configuration as \"{original_output_root_folder_dir}\" already exists.{c.ENDC}")
        return output_root_folder_dir
    else:
        # This should not happen after the while above
        print(f"> {c.WARNING}Directory cannot be created as it already exists: \"{output_root_folder_dir}\".{c.ENDC}")
        return ""

