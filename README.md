# qoqolo-check-in-out-spider

This is a small python spider to extract the check-in check-out photos from Qoqolo system for your account.

## Kick-start

Make sure that you have latest Python 3 installed. Version used for development is 3.10.9.

You may install following modules too:

```bash
pip3 install beautifulsoup4
pip3 install requests
```

Then `cd` to the project folder. Duplicate `config_sample.json` and rename it to `config_personal.json`.

In your browser, open Qoqolo, login, and navigate to "Recent Sign-in/out" from side menu. Stay at the default page of sign-in/out, and note down the URL.

Open your browser inspector and note down the cookies. Then Update the contents of `config_personal.json` (see details below).

Finally, run the python script:

```bash
python3 spider.py
```

> Depending on your environment, you may need use `python` and `pip` commands, or `python3` and `pip3` as above.

### Update the Configs

```json
{
    "cookies": {
        "SALTSESS": "abcdefghijklmnopqrstuvwxyz",
        "__utma": "1234567.987654321.1234567890.1234567890.1234567890.1",
        "__utmc": "1234567",
        "__utmz": "1234567.1234567890.1.1.utmcsr=google|utmccn=(organic)|utmcmd=organic|utmctr=(not%20provided)"
    },
    "recentCheckInOutLink": "https://pcfsparkletots.qoqolo.com/cos/o.x?c=/abcd_efg/check_in&func=recent",
    "startYearMonth": "2024-01",
    "endYearMonth": "2024-12",
    "outputRootFolderDirectory": "/Users/<my-name>/Pictures/2024 Check-in-out Photos"
}
```

**Cookies**: Note down all the cookies based on what you have from your browser's inspector.

**recentCheckInOutLink**: The URL when you navigate to "Recent Sign-in/out". You should have similar format as the sample one.

> This script is done based on Singapore's PCF Spartletots Pre-school customised version, as in the URL `pcfsparkletots.qoqolo.com`. It would work with other schools though it depends on whether there is any customisation that may break the codes.

**startYearMonth**, **endYearMonth**: In yyyy-mm format. Note that to avoid polling too many things for one time, it will limit to maximum 12 months' range per time.

**outputRootFolderDirectory**: The folder path to place your photos. It is recommended to create an empty folder for them. The path format in above sample is based on Mac.

> It should work with Windows paths too; though I don't have a Windows machine to test it out.

### Expected Output

You should expect daily check-in/out image files saved to the folder that you have supplied as `outputRootFolderDirectory`, like:

```
+ 2024 Check-in-out Photos
  + 2024-01
    - 2024-01-02-in.jpg
    - 2024-01-02-out.jpg
    - 2024-01-03-in.jpg
    - 2024-01-03-out.jpg
    ...
    - 2024-01.csv
  + 2024-02
    - 2024-02-01-in.jpg
    - 2024-02-01-out.jpg
    - 2024-02-02-in.jpg
    - 2024-02-02-out.jpg
    ...
    - 2024-02.csv
  ...
```

## Disclaimer

This script is for personal use, and has no affliation with Qoqolo nor PCF Spartletots Pre-school.

This script is equivilant to how you will do to manually open each month and each day's pop-up to save the images one by one. It will not create additional traffic to Qoqolo's server. It will not, and it cannot access to other people's account for other kids' images, as it is purely based on the information retrievable from your account only.

Please refrain from using this script to perform other jobs, other than retreiving daily check-in-out images for your kids.
