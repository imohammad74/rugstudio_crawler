import requests
from bs4 import BeautifulSoup
from common import Common
from db import DBManagement as db
from pdp_elements import PDPElements
from table import Table


class PDP:

    @staticmethod
    def main(params: dict):
        url = params['url']
        brand = Common.find_brand(url, params['brands_list'])
        design_ids = params['design_ids']
        r = requests.get(url)
        soup = BeautifulSoup(r.content, 'html.parser')
        if PDPElements.page_is_exist(soup):
            features = list(PDPElements().features(soup).keys())
            variants = Table().body(url, soup)
            for variant in variants:
                title = PDPElements.title(soup)
                description = PDPElements.description(soup)
                design_id = PDPElements().design_id(soup, design_ids)
                item_id = variants[variants.index(variant)]['Item #']
                size = variant['Size']
                ships_within = variant['Ships Within']
                msrp = variant['MSRP']
                sale_price = variant['Sale Price']
                # image_urls = PDPElements.images_product(url, soup, download_image=False)
                all_columns = [
                    {'column': 'title', 'value': title},
                    {'column': 'description', 'value': description},
                    {'column': 'url', 'value': url},
                    {'column': 'brand', 'value': brand},
                    {'column': 'size', 'value': size},
                    {'column': 'ships_within', 'value': ships_within},
                    {'column': 'msrp', 'value': msrp},
                    {'column': 'design_id', 'value': design_id},
                    {'column': 'sale_price', 'value': sale_price}
                ]
                try:
                    db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[2],
                                   columns=[{'column': 'item_id', 'value': item_id}])
                except:
                    db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[2],
                                   columns=[{'column': 'item_id', 'value': ''}])
                for feature in features:
                    feature_value = PDPElements().features(soup)[f'{feature}']
                    try:
                        db.update_rows(db_file=db.db_file(), table_name=db.db_table()[2],
                                       condition=f'item_id="{item_id}"',
                                       columns=[{'column': f'{feature}', 'value': feature_value}])
                    except:
                        db.update_rows(db_file=db.db_file(), table_name=db.db_table()[2],
                                       condition=f'item_id="{item_id}"',
                                       columns=[{'column': f'{feature}', 'value': ''}])
                try:
                    db.update_rows(db_file=db.db_file(), table_name=db.db_table()[2], condition=f'item_id="{item_id}"',
                                   columns=all_columns)
                except:
                    db.update_rows(db_file=db.db_file(), table_name=db.db_table()[2], condition=f'item_id="{item_id}"',
                                   columns=all_columns)
            print(f'"{title}" finish!')
        else:
            try:
                db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                               columns=[{'column': 'url', 'value': url}])
            except:
                db.insert_rows(db_file=db.db_file(), table_name=db.db_table()[3],
                               columns=[{'column': 'url', 'value': ''}])
            print('No data!')

    def __init__(self, params: dict):
        self.main(params)
