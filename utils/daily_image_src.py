import requests
from bs4 import BeautifulSoup
from typing import TypedDict

class InOutImg(TypedDict):
    inout: str # "in" "out"
    src: str
    date: str # yyyy-mm-dd
    rename_as: str

def get_img_srcs(url: str, date: str, hostname: str, headers, cookies):
    img_srcs: list[InOutImg] = []

    if url == "" or date == "":
        return img_srcs

    try:
        # Make a GET request to the URL
        response = requests.get(url, headers=headers, cookies=cookies)
        response.raise_for_status()  # Raise an error for bad responses

        # Parse the HTML content
        soup = BeautifulSoup(response.content, 'html.parser')

        # Find all fieldsets
        fieldsets = soup.find_all('fieldset')

        for fieldset in fieldsets:
            # Find all divs with class "form-group"
            form_groups = fieldset.find_all('div', class_='form-group')

            # Get Legend to determine "in" or "out"
            legend = fieldset.find('legend')
            inout_text = legend.get_text(strip=True) if (legend := legend) is not None else ''

            inout = ''
            if inout_text == "Sign in":
                inout = "in"
            if inout_text == "Sign out":
                inout = "out"

            if (inout == ''):
                continue

            # Extract img src from form groups with label "Photo"
            for form_group in form_groups:
                label = form_group.find('label')
                img = form_group.find('img')

                if label and label.get_text(strip=True) == "Photo" and img:
                    src_raw = img['src']
                    src = src_raw if hostname in src_raw else f"https://{hostname}/{src_raw}"
                    if src and (hostname in src_raw or hostname != ''):
                        img_info: InOutImg = {
                            "date": date,
                            "inout": inout,
                            "src": src,
                            "rename_as": f"{date}-{inout}"
                        }
                        img_srcs.append(img_info)
        return img_srcs
    
    except requests.exceptions.RequestException as e:
        print(f"Error: {e}")
        return img_srcs
