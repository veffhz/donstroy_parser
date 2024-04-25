import re

import requests

from bs4 import BeautifulSoup


def generate_new_url():
    base_url = ("https://donstroy.moscow/full-search/?price%5B%5D=9.8&price%5B%5D=725.2&area%5B%5D=21&area%5B%5D=420"
                "&floor_number%5B%5D=1&floor_number%5B%5D=52&rooms%5B%5D=2&projects%5B%5D=28&quarters%5B%5D=a1d5edf9"
                "-6238-11eb-8162-0050569d5829&quarters%5B%5D=7e9a1662-fb88-11eb-817d-0050569d5829&quarters%5B%5D"
                "=8b3ab8ee-fb88-11eb-817d-0050569d5829&quarters%5B%5D=7dfba2a5-30c4-11ec-8188-0050569d5829"
                "&floor_first_last=false&discount=false&furnish=false&apartments=false&sort=price-asc&view_type=flats"
                "&page=1&view=card")

    return "{}".format(base_url)


def download_raw_page_content():
    url = generate_new_url()
    request = requests.get(url)
    return request.text


def extract_data_by_class(raw_content, elem, class_name, is_all=False):
    """extract html tags by element and class name"""
    parser = "html.parser"
    soup = BeautifulSoup(str(raw_content), parser)
    if is_all:
        return soup.find_all(elem, class_=class_name)
    else:
        return soup.find(elem, class_=class_name)


def parse_count(article_block):
    count = extract_data_by_class(article_block, "div", "d-choose-params__count").text
    return count


def parse_block(article_block):
    title_raw = extract_data_by_class(article_block, "div", "d-flat-card__title").text

    title = title_raw.replace("комн.", "")
    title = title.replace("\n", "")

    title = re.sub(' +', ' ', title).lstrip()

    position_raw = extract_data_by_class(article_block, "div", "d-flat-card__position").text

    position = re.sub(' +', ' ', position_raw)

    return title, position


def collect_items(page_content):
    items = []
    div_blocks = extract_data_by_class(page_content, "div", "d-flat-card__top", is_all=True)
    for div_block in div_blocks:
        parsed_data = parse_block(div_block)
        items.append(parsed_data)
    return items


def print_result(data):
    for item in data:
        title, position = item
        template = f"{title} {position}"
        print('------------------------------------------')
        print(template)


def main():
    pages_content = download_raw_page_content()
    data = collect_items(pages_content)
    print_result(data)


if __name__ == "__main__":
    main()
