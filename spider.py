import json
import os.path

from utils.bcolors import bcolors as c
from utils.root_folder import get_root_folder_dir
from utils.month_year import generate_month_year_range
from utils.url import is_valid_url, add_query_params, get_hostname_from_url
from utils.month_table import get_table_rows
from utils.daily_image_src import get_img_srcs
from utils.save_image import download_and_save_images
from utils.csv import create_csv_from_dicts

from typing import List, TypedDict

# default headers

headers = {
    'User-Agent': 'Mozilla/5.0 (Windows NT 6.1; WOW64) AppleWebKit/537.36 (KHTML, like Gecko) Chrome/66.0.3359.181 Safari/537.36',
}

# --- Read Configs and Get the Root Folder ---

# Get the default Pictures directory
sys_home_folder = os.path.expanduser('~')
sys_pic_path = os.path.join(sys_home_folder, "Pictures")
default_folder_path = os.path.join(sys_pic_path, 'Check in-out Photos')

print("")
print(f"{c.HEADER}{c.BOLD}=== Starting script... ==={c.ENDC}{c.ENDC}")
print("")

# Duplicate from config_sample.json and name it config_personal.json. Fill in your contents.
# get configs from config_personal.json

with open('config_personal.json') as json_config:
    configs = json.load(json_config)

cookies = configs['cookies']
recent_inout_link = configs["recentCheckInOutLink"]
st_yr_mon = configs['startYearMonth'] if configs['startYearMonth'] else ''
end_yr_mon = configs['endYearMonth'] if configs['endYearMonth'] else ''

output_root_folder_dir = get_root_folder_dir(configs['outputRootFolderDirectory'])

# --- Generate month-year range. Qoqolo is using month-year in URL param ---
month_years = generate_month_year_range(st_yr_mon, end_yr_mon, 12)

if month_years.__len__() == 0:
    print(f"> {c.FAIL}No valid year-month range. Please check your config file for startYearMonth and endYearMonth. They need be in \"yyyy-mm\" format.{c.ENDC}")

# --- Check URL for in_out_link, destruct and construct new URLs based on year-month range ---

class MonthUrlInfo(TypedDict):
    mon_yr: str
    yr_mon: str
    url: str

if is_valid_url(recent_inout_link):
    hotname = get_hostname_from_url(recent_inout_link)
    month_urls: list[MonthUrlInfo] = []
    print(f"> {c.OKBLUE}Will retrieve info for the following {month_years.__len__()} pages:{c.ENDC}")
    for mon_yr in month_years:
        selected_date_params: dict[str, str] = {"func": "recent", "selectDate": mon_yr}
        new_url_month = add_query_params(recent_inout_link, selected_date_params)
        month, year = mon_yr.split('-')
        yr_mon = f'{year}-{month}'
        month_urls.append({
            'yr_mon': yr_mon,
            'mon_yr': mon_yr,
            'url': new_url_month
        })
        print(f"{c.UNDERLINE}>>> {new_url_month}{c.ENDC}")

    for month_info in month_urls:
        rows_of_month = get_table_rows(month_info['url'], headers, cookies)
        yr_mon = month_info['yr_mon']

        print("")
        print(f"> {c.OKBLUE}Will retrieve info for {month_info['yr_mon']}:{c.ENDC}")

        # --- Get Image Links from individual View Check-in Page ---
        # ...&func=view_checkin&type=students&output=ajax&rid=<button_id>&selectDate=<yyyy_mm_dd>

        for row_info in rows_of_month:
            print(f">>> {row_info['date']}: rid - {row_info['button_id']}")

            indv_date_params: dict[str, str] = {
                "func": "view_checkin",
                "type": "students",
                "output": "ajax",
                "rid": row_info['button_id'],
                "selectDate": row_info['date'],
            }
            url_of_day = add_query_params(recent_inout_link, indv_date_params)

            img_srcs = get_img_srcs(url_of_day, row_info['date'], hotname, headers, cookies)
            download_and_save_images(img_srcs, output_root_folder_dir, yr_mon, headers, cookies)
        
        create_csv_from_dicts(rows_of_month, os.path.join(output_root_folder_dir, yr_mon), yr_mon)
            
        print("")
        print(f">>> {c.OKBLUE}CSV for {yr_mon} is generated.{c.ENDC}")
        print("")

else:
    print(f"> {c.FAIL}Invalid URL: \"{recent_inout_link}\".{c.ENDC}")

# --- END ---

print("")
print(f"{c.HEADER}{c.BOLD}=== Srcipt execution completed. ==={c.ENDC}{c.ENDC}")
print(f"check {c.BOLD}\"{c.UNDERLINE}{output_root_folder_dir}{c.ENDC}\"{c.ENDC} folder for exported photos.")
print("")
