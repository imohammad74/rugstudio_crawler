import requests
from bs4 import BeautifulSoup
from mail import Mail
from check_price import CheckPrice
from common import Common
from db import DBManagement as db
from get_all_brands_url import GetAllBrandsURL
from get_brands_url import GetBrandsURL
from pdp import PDP
from woker import Worker


class Main:
    print('Welcome to Rugstudio Crawler')

    @staticmethod
    def find_last_crawled_url():
        last_url = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[4], all_columns=False,
                                  columns=['seq'], condition="name='rugstudio_url'")
        last_url = int(last_url[0][0])
        return last_url

    @staticmethod
    def get_urls(all_brand):
        url = "https://rugs.rugstudio.com/newnav/"
        re = requests.get(url)
        soup = BeautifulSoup(re.content, "html.parser")
        params = {
            'url': url,
            're': re,
            'soup': soup
        }
        if all_brand is True:
            GetAllBrandsURL(params=params)
        else:
            GetBrandsURL()

    def get_pdp(self, resume: bool):
        max_worker = Common.max_worker()
        if resume:
            last_url_id = self.find_last_crawled_url()
            urls = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[0], all_columns=False,
                                  columns=['url_address'])
            total_url = len(urls)
            for i in range(last_url_id, total_url):
                PDP(urls[i][0])
                db.update_rows(db_file=db.db_file(), table_name=db.db_table()[4],
                               columns=[{'column': 'seq', 'value': i}],
                               condition="name='rugstudio_url'")
        else:
            urls = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[0], all_columns=False,
                                  columns=['url_address'])
            urls_ = [url[0] for url in urls]
            Worker(fn=PDP, data=urls_, max_worker=max_worker)
            # for url in urls:
            #   PDP(url[0])

    def __init__(self):
        while True:
            print('''
            [1]: Get All URLs
            [2]: Get Some Brand URLs
            [3]: Get PDPs
            [4]: Resume Get PDPs
            [5]: Check Price
            ''')
            select_option = input("Enter a option: ")
            if select_option == '1':
                self.get_urls(all_brand=True)
            elif select_option == '2':
                self.get_urls(all_brand=False)
            elif select_option == '3':
                Mail(attachment=False)
                self.get_pdp(resume=False)
            elif select_option == '4':
                Mail(attachment=False)
                self.get_pdp(resume=True)
            elif select_option == '5':
                Mail(attachment=True)
                CheckPrice()
            else:
                continue


Main()
