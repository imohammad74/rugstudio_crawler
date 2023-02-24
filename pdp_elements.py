import os
import re

import requests
from bs4 import BeautifulSoup

from common import Common
from table import Table


class PDPElements:

    @staticmethod
    def page_is_exist(soup):
        if soup.find(class_='OneColumn _404'):
            return False
        else:
            return True

    @staticmethod
    def title(soup):
        """get title of pdp"""
        title = soup.find(class_='ProductDetailsProductName no-m-t').text
        return title

    @staticmethod
    def description(soup):
        desc = soup.find(class_='desc col-sm-7').text
        return desc

    @staticmethod
    def feature_section_type_1(content):
        a = str(content).split('<br/>')
        features_label = [i.split(':')[0].replace(' ', '_') for i in a if i.split(':')[0][0] != '<']
        features = []
        for i in a:
            fe = i.split('href')
            fe_part = len(fe)
            if fe_part == 1:
                if ':' in fe[0]:
                    fe = fe[0].split(':')
                    feature = fe[1]
                    if '<sup>' and '</sup>' and '<sub>' and '</sub>' in feature:
                        feature = Common.convert_sup_sub_to_str(feature)
                else:
                    continue
                features.append(feature.strip())
            elif fe_part == 2:
                m = BeautifulSoup(str(i), 'html.parser')
                feature = m.find('a').text
                if feature != 'Rug pad':
                    features.append(feature.strip())
            else:
                continue
        z = {}
        for i in range(0, len(features)):
            z['%s' % features_label[i]] = features[i]
        return z

    @staticmethod
    def feature_section_type_2(soup):
        section = soup.find(class_='bullets col-sm-5')
        a = str(section).split('<br/>')
        del a[0]
        del a[-1]
        features_label = [i.split(':')[0].replace(' ', '_') for i in a if not re.search('<a', i.split(':')[0])]
        if '\n' or '' in features_label:
            features_label.remove('\n')
            features_label.remove('')
        features = []
        for i in a:
            fe = i.split('href')
            fe_part = len(fe)
            if fe_part == 1:
                if ':' in fe[0]:
                    fe = fe[0].split(':')
                    feature = fe[1]
                    if '<sup>' and '</sup>' and '<sub>' and '</sub>' in feature:
                        feature = Common.convert_sup_sub_to_str(feature)
                else:
                    continue
                features.append(feature.strip())
            elif fe_part == 2:
                m = BeautifulSoup(str(i), 'html.parser')
                feature = m.find('a').text
                if feature != 'Rug pad':
                    features.append(feature.strip())
            else:
                continue
        z = {}
        for i in range(0, len(features)):
            z['%s' % features_label[i]] = features[i]
        return z

    def features(self, soup):
        content = soup.find(class_='bullets col-sm-5').find('span')
        if content is not None:
            features = self.feature_section_type_1(content)
            return features
        else:
            features = self.feature_section_type_2(soup)
            return features

    @staticmethod
    def images_product(url: str, soup: str, download_image: bool):
        images = soup.find_all('a', {'class': 'thumbnail'})
        main_url = 'https://www.rugstudio.com'
        image_links = [f'{main_url}{image.get("href")}' for image in images if '.aspx' not in image]
        cnt = 0
        sku = Table.body(url, soup)[0]['Item #'].split('x')[0]
        path = f'{sku}'
        if download_image:
            for image in image_links:
                cnt += 1
                r = requests.get(image, allow_redirects=True, timeout=15)
                is_exist = os.path.exists(path)
                image_size = requests.head(image)
                image_format = image_size.headers.get('content-type').split('/')[-1]
                if not is_exist:
                    os.makedirs(path)
                if '.aspx' not in image:
                    file = open(f'{path}/{sku}-{cnt}.{image_format}', 'wb').write(r.content)
        else:
            return image_links

    def design_id(self, soup, pattern_id: str):
        title = self.title(soup)
        collection_name = self.features(soup)['Collection']
        if pattern_id == '1':
            Common.design_id_pattern_i(title)
        elif pattern_id == '2':
            Common.design_id_pattern_ii(title=title, brand=title.split(' ')[0], collection_name=collection_name)
        else:
            return 'Not found'


# todo:design id
