from utils.bcolors import bcolors as c

def generate_month_year_range(start_ym: str, end_ym: str, max: int):
    cur_ym = start_ym
    year, month = map(int, cur_ym.split('-'))
    month_year_array: list[str] = []

    cur_cnt = 0

    while cur_ym <= end_ym and cur_cnt < max:
        year, month = map(int, cur_ym.split('-'))
        cur_my = f"{month:02d}-{year:04d}"
        month_year_array.append(cur_my)

        # Increment the month
        month += 1
        if month > 12:
            month = 1
            year += 1
        
        cur_ym = f"{year:04d}-{month:02d}"
        cur_cnt += 1

    if cur_cnt == max and cur_ym <= end_ym:
        print(f"> {c.WARNING}We only support maximum {str(max)}  months for the range. Please check your config file for startYearMonth and endYearMonth, and reduce the range covered.{c.ENDC}")

    return month_year_array
