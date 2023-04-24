import re

from db import DBManagement as db


class Common:

    @staticmethod
    def last_url(total_product):
        """this function helps to get end of urls.
        for ex: https://rugs.rugstudio.com/newnav/96 ; 96 is returned by this function.
        """
        show_product_in_plp = 48
        end_url_list = [int(i) for i in range(0, int(total_product), show_product_in_plp)]
        return end_url_list

    @staticmethod
    def number_of_product(soup):
        """this function helps to find last pages of plp."""
        total_product_string = soup.find_all(id='lblProductCountTop')
        number_of_product = int(total_product_string[0].find_all('b')[1].text)
        return number_of_product

    @staticmethod
    def get_url(plp_url):
        url = plp_url.split('url=')
        url = url[1].split('&')
        url = url[0].replace('%3a', ':')
        url = url.replace('%2f', '/')
        return url

    @staticmethod
    def convert_sup_sub_to_str(size):
        r = size.replace('<sup>', '')
        r = r.replace('<sub>', '')
        r = r.replace('</sup>', '')
        size = r.replace('</sub>', '').strip()
        return size

    @staticmethod
    def clean_price(price):
        if '$' in price:
            price = price.replace('$', '')
        if ',' in price:
            price = price.replace(',', '')
        return price

    @staticmethod
    def brand_from_url(url):
        title = url.replace('https://www.rugstudio.com/', '')
        brand = title.split('-')[0]
        return brand

    @staticmethod
    def design_id_pattern_i(title):
        """
        Rugs have some patterns from designID. In Rugstudio, there are two patterns. In this pattern, designID has the
        digital number in its pattern.
        """
        title_separate = title.split(" ")
        for character in title_separate:
            if re.findall('[0-9]', character):
                design_id = character
                return design_id

    @staticmethod
    def design_id_pattern_ii(title: str, brand: str, collection_name: str):
        """
        Rugs have some patterns from designID. In Rugstudio, there are two patterns. In this pattern, designID is a
        word. The location of this word is different in the brands title.
        """
        title_ = title.lower().split(' ')
        print(f'title: {title_}')
        brand_ = brand.lower().split(' ')
        print(f'brand_: {brand_}')
        collection_name_ = collection_name.lower().split(' ')
        print(f'collection_name_: {collection_name_}')
        title_collection = brand_ + collection_name_
        print(f'title_collection: {title_collection}')
        design_id = []
        for part in title_:
            if part in title_collection:
                continue
            else:
                design_id.append(part)
        if len(design_id) == 1:
            design_id = design_id[:-3][0]
            return design_id
        else:
            design_id = f'{design_id[:-3][0]} {design_id[:-3][1]}'
            return design_id

    @staticmethod
    def max_worker():
        """
        Fetch max worker from database
        """
        max_worker = db.fetch_datas(db_file=db.db_file(), table_name=db.db_table()[4], all_columns=False,
                                    columns=['seq'], condition="name='max_worker'")
        max_worker = int(max_worker[0][0])
        return max_worker

    @staticmethod
    def find_brand(url: str, brands: list) -> str:
        for brand in brands:
            if brand in url:
                return brand
