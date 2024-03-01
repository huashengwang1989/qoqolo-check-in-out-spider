import csv
import os.path

from utils.month_table import DailyCheckInOut, csv_columns

def create_csv_from_dicts(source: list[DailyCheckInOut], folder_path: str, filename: str):
    csv_filename = os.path.join(folder_path, f"{filename}.csv")

    # Write data to CSV file
    with open(csv_filename, 'w', newline='') as csvfile:
        writer = csv.DictWriter(csvfile, fieldnames=csv_columns)
        writer.writeheader()
        for row in source:
            writer.writerow(row)
