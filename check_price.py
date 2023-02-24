import logging
from datetime import datetime

import requests
from bs4 import BeautifulSoup
from xlsxwriter.workbook import Workbook

from common import Common
from db import DBManagement as db
from mail import Mail
from pdp_elements import PDPElements
from table import Table
from woker import Worker

now = datetime.now()


class CheckPrice:

    @staticmethod
    def check_prices():
        db.custom_query(db_file=db.db_file(), query="""UPDATE check_prices SET
                                            is_warning = (CASE WHEN (new_price-last_price)/100>5 THEN 1 ELSE NULL END)
                        """)
        print('check price is Done')

    @staticmethod
    def detect_large_change():
        logging.warning('step3')
        datas = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[5], all_columns=True,
                               condition="is_warning='1'")
        return datas

    def export_excel(self):
        workbook = Workbook('output1.xlsx')
        worksheet = workbook.add_worksheet()
        header = ['item_id', 'last_update', 'last_price', 'new_price', 'url', 'brand_name']
        cell_format = workbook.add_format({'bold': True})
        for i, title in enumerate(header):
            worksheet.write(0, i, title, cell_format)
        for i, row in enumerate(self.detect_large_change()):
            for j, value in enumerate(row):
                worksheet.write(i + 1, j, value)
        workbook.close()
        print('execl file is created')
        Mail(attachment=True)

    @staticmethod
    def main(params):
        url = params['url']
        brand_name = params['brand_name']
        current_time = int(now.strftime("%y%m%d"))
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        if PDPElements.page_is_exist(soup):
            variants = Table().body(url, soup)
        else:
            return logging.warning('Table not found')
        for variant in variants:
            item_id = variants[variants.index(variant)]['Item #']
            new_price = variant['Sale Price']
            try:
                all_columns = [
                    {'column': 'last_update', 'value': current_time},
                    {'column': 'item_id', 'value': item_id},
                    {'column': 'new_price', 'value': new_price},
                    {'column': 'url', 'value': url},
                    {'column': 'brand_name', 'value': brand_name}
                ]
                db.update_rows(db_file=db.db_file(), table_name=db.db_table()[5], condition=f'item_id="{item_id}"',
                               columns=all_columns)
            except:
                db.update_rows(db_file=db.db_file(), table_name=db.db_table()[5], condition=f'item_id="{item_id}"',
                               columns=all_columns)

    def __init__(self):
        max_worker = Common.max_worker()
        # for first
        # db.copy_column(db_file=db.db_file(), table_name=db.db_table()[5],
        #               columns=['new_price', 'last_price'])
        urls = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[0], all_columns=False,
                              columns=['brand', 'url_address'])
        urls_ = []
        for item in urls:
            product = {
                'brand_name': item[0],
                'url': item[1]
            }
            urls_.append(product)
        Worker(self.main, data=urls_, max_worker=max_worker)
