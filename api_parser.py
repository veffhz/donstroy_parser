import datetime
import math

import requests
import xlsxwriter

from request import data_request

BASE_URL = 'https://donstroy.moscow/api/v1/flatssearch/choose_params_api_flats/'


def get_page(page_no=1):
    data_request['page'] = page_no
    response = requests.post(BASE_URL, json=data_request)
    return response.json()


def main():
    data = get_page()

    total_flats = data['total_flats']

    flats = [flat for flat in data['flats'] if not flat['isUtp']]

    pages_count = math.ceil(total_flats / (len(flats)))

    now = datetime.datetime.today().strftime("%Y-%m-%d_%H-%M-%S")

    workbook = xlsxwriter.Workbook('report.xlsx')
    worksheet = workbook.add_worksheet(now)

    row = 0
    column = 0

    for page in range(1, pages_count + 1):

        if page > 1:
            data = get_page(page)
            flats = [flat for flat in data['flats'] if not flat['isUtp']]

        for flat in flats:

            rooms = f'{flat["rooms"]}-комнатная квартира {flat["number"]}'
            project = f'{flat["project"]}'
            details = f'{flat["quarter"]}, Корпус {flat["building"]}, секция {flat["section"]}, этаж {flat["floor"]}'

            template = rooms + '\n' + project + '\n' + details

            print(template)
            print()

            worksheet.write(row, column, rooms)
            worksheet.write(row, column + 1, project)
            worksheet.write(row, column + 2, details)

            row += 1

    workbook.close()


if __name__ == "__main__":
    main()
