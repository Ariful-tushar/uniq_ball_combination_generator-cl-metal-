from number_parser import parse_ordinal
import requests
from lxml import html
import csv
import os
import sys
import random
from collections import Counter


def ordinal(n):
    """PARSE INTEGER TO ORDINAL. EX: 1 >> 1st"""
    return "%d%s" % (n, "tsnrhtdd"[(n//10 % 10 != 1)*(n % 10 < 4)*n % 10::4])


def save_csv(file_name, data_list, isFirst=False):
    """SAVE DATA INTO CSV FILE"""
    if isFirst:
        if os.path.isfile(f'{file_name}'):
            os.remove(file_name)

    with open(f'{file_name}', "a", newline='', encoding='utf-8-sig') as fp:
        wr = csv.writer(fp, dialect='excel')
        wr.writerow(data_list)


def xpath_to_text(webpage, xpath):
    """CONVER XPATH TO TEXT"""

    try:
        return webpage.xpath(xpath)[0].strip()
    except:
        return ""


def get_webpage(url, headers="", cookies=""):
    """SEND REQUESTS AND GET PAGE"""

    response = requests.get(url, headers=headers, cookies=cookies)
    status_code = response.status_code
    webpage = html.fromstring(response.content)

    return webpage, status_code


def get_random_number(isPowerball=False):
    """GENERATE A RANDOM BALL NUMBER"""

    if isPowerball:
        return f"{random.randint(1, 26)}"
    else:
        return f"{random.randint(1, 69)}"


def get_random_set():
    """GENERATE A RANDOM SET FOR USER"""

    random_ball_list = []
    while len(random_ball_list) != 5:
        random_ball = get_random_number()
        if random_ball not in random_ball_list:
            random_ball_list.append(random_ball)
        else:
            continue

    random_ball_list.append(get_random_number(isPowerball=True))
    random_ball_list_string = "|".join(random_ball_list)

    return random_ball_list_string


def generate_uniq_random_ballset(all_ball_set_strings, generate_set_numbers):
    """GENERATE UNIQ BALL NUMBER SETS"""

    new_sets = []
    for i in range(generate_set_numbers):
        while True:

            random_ball_string = get_random_set()
            if random_ball_string not in all_ball_set_strings:
                all_ball_set_strings.append(random_ball_string)
                new_sets.append(random_ball_string)
                break
            else:
                continue

    return [s.split("|") for s in new_sets]


def count_sets_for_duplicate(all_ball_set_strings, file_name):
    """COUNT DUPLICATE SETS AND WRITE TO CSV FILE"""

    count_sets = dict(Counter(all_ball_set_strings))
    for each_set in count_sets.items():
        data_list = each_set[0].split("|")
        data_list.append(each_set[1])
        # data_list = [each_set[0].split("|"), each_set[1]]
        save_csv(file_name, data_list)


def scraper(file_name, main_url, start_year, end_year, generate_set_numbers):
    """SCRAPER FUNCTION TO SCRPE DATA"""

    all_ball_set_strings = []
    for year in range(start_year, end_year+1):
        print(f">>>> SCRAPING YEAR {year}")
        year_url = f"{main_url}{year}"
        webpage, status_code = get_webpage(year_url)
        ball_set_list_elems = webpage.xpath(
            "//table[@class = 'prizes archive ']/tbody/tr")

        for each_ball_set_elem in ball_set_list_elems:
            ball_numbers = each_ball_set_elem.xpath(
                ".//ul[1]/li[not(contains(@class , 'power-play'))]/text()")
            ball_numbers = [s.strip() for s in ball_numbers]
            ball_set_string = "|".join(ball_numbers)
            all_ball_set_strings.append(ball_set_string)

    count_sets_for_duplicate(all_ball_set_strings, file_name)
    newly_generated_sets = generate_uniq_random_ballset(
        all_ball_set_strings, generate_set_numbers)

    for idx, each_new_set in enumerate(newly_generated_sets):
        print(f"{ordinal(idx+1)} set is: {','.join(each_new_set)}")


def main():
    """MAIN FUNCTION"""

    try:
        new_sets_to_generate = int(
            input("Please enter how many sets you wnat to create: "))
    except:
        print("Wrong Input!")
        sys.exit()
    main_url = "https://www.lottery.net/powerball/numbers/"
    file_name = "uniq_ball_data.csv"
    start_year = 2020
    end_year = 2022
    print("-------------------------------------------------")
    print(f"            Scraping Started                    ")
    print("-------------------------------------------------")
    save_csv(file_name, ['ball_1', 'ball_2', 'ball_3',
             'ball_4', 'ball_5', 'power_ball', 'Count'], isFirst=True)
    scraper(file_name, main_url, start_year, end_year, new_sets_to_generate)


if __name__ == "__main__":
    main()
