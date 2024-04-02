import requests
import re
from bs4 import BeautifulSoup
from utils.bcolors import bcolors as c
from typing import TypedDict

class DailyCheckInOut(TypedDict):
    button_id: str
    date: str #yyyy-mm-dd
    idx: int
    url: str
    drop_ts: str
    drop_person: str
    drop_comment: str
    pick_ts: str
    pick_person: str
    pick_comment: str

csv_columns = ["idx", "date", "button_id", "drop_ts", "drop_person", "drop_comment", "pick_ts", "pick_person", "pick_comment"]

def remove_suffix(original_string: str, suffix: str):
    if suffix != '' and original_string.endswith(suffix):
        return original_string[:-len(suffix)]
    else:
        return original_string

def get_table_rows(url: str, headers, cookies):
    result_array: list[DailyCheckInOut] = []

    try:
        # Make a GET request to the URL
        response = requests.get(url, headers=headers, cookies=cookies)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find the first table in the HTML
        table = soup.find('table')

        if table:
            # Extract rows from the table
            rows = table.find_all('tr')
            
            # Process rows and extract text content
            for row in rows:
                cells = row.find_all(['td'])
                if cells.__len__() == 0:
                    continue
                row_data = [cell.get_text(strip=True) for cell in cells]
                # Check if the last cell contains a button
                button_cell = cells[-1].find('button')
                if button_cell and '_id' in button_cell.attrs:
                    # Qoqolo's timestamp doesn't have space in between date and time
                    drop_ts: str = row_data[1]
                    drop_ts = drop_ts if drop_ts.__len__() <= 10 or drop_ts[10] == ' ' else f"{drop_ts[:10]} {drop_ts[10:]}"
                    drop_info = cells[2]
                    drop_comment_p = drop_info.find('p')
                    drop_comment = drop_comment_p.get_text(strip=True) if (drop_comment_p := drop_comment_p) is not None else ''

                    pick_ts = row_data[4]
                    pick_ts = pick_ts if pick_ts.__len__() <= 10 or pick_ts[10] == ' ' else f"{pick_ts[:10]} {pick_ts[10:]}"
                    pick_info = cells[5]
                    pick_comment_p = pick_info.find('p')
                    pick_comment = pick_comment_p.get_text(strip=True) if (pick_comment_p := pick_comment_p) is not None else ''

                    date: str = drop_ts[:10] if (drop_ts := drop_ts) is not None else ''
                    ds_pattern = r'^[0-9]{4}-[0-9]{2}-[0-9]{2}$'
                    if not date or not bool(re.match(ds_pattern, date)):
                        date = pick_ts[:10] if (pick_ts := pick_ts) is not None else ''
                        if not date or not bool(re.match(ds_pattern, date)):
                            date = ''

                    daily_info: DailyCheckInOut = {
                        'button_id': button_cell.attrs['_id'],
                        'idx': int(row_data[0]) - 1,
                        'date': date,
                        'drop_ts': drop_ts,
                        'drop_person': row_data[2] if drop_comment == '' else remove_suffix(row_data[2], drop_comment),
                        'drop_comment': drop_comment,
                        'pick_ts': pick_ts,
                        'pick_person': row_data[5] if pick_comment == '' else remove_suffix(row_data[5], pick_comment),
                        'pick_comment': pick_comment
                    }
                    result_array.append(daily_info)
            return result_array
        else:
            login = soup.find('div', { 'class': 'lo-user' })
            if login:
                print(f"> {c.FAIL}Seems to redirect to login. May check your cookie in your configuration.{c.ENDC}")
                raise Exception('expired-or-wrong-cookie')
            else:
                # If no table is found, return an empty array
                return result_array
            
    
    except requests.exceptions.RequestException as e:
        if str(e) != 'expired-or-wrong-cookie':
            print(f"> {c.FAIL}Error retrieving table information for \"{url}\": {e}{c.ENDC}")
            return result_array
        else:
            raise Exception('expired-or-wrong-cookie')
