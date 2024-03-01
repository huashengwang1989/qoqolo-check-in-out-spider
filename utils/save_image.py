import requests
import os.path

from utils.bcolors import bcolors as c
from utils.daily_image_src import InOutImg

# yr_mon: yyyy-mm, will be sub-folder in the folder_path
def download_and_save_images(img_srcs: list[InOutImg], folder_path: str, yr_mon: str, headers, cookies):
    mon_folder_path = os.path.join(folder_path, yr_mon)
    if not os.path.exists(mon_folder_path):
        os.makedirs(mon_folder_path)

    for src_info in img_srcs:
        filename = f"{src_info['rename_as']}.jpg"
        try:
            url = src_info['src']
            response = requests.get(url, headers=headers, cookies=cookies)
            if response.status_code == 200:
                # Save the image with the desired name
                filepath = os.path.join(mon_folder_path, filename)
                
                with open(filepath, "wb") as file:
                    file.write(response.content)
                
                print(f">>> {c.OKGREEN} Downloaded image \"{filename}\".{c.ENDC}")
            else:
                print(f">>> {c.FAIL} Failed to download image \"{filename}\". Status code: {response.status_code}.{c.ENDC}")
        except Exception as e:
            print(f">>> {c.FAIL} Error downloading image \"{filename}\": {str(e)}.{c.ENDC}")