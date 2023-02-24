from bs4 import BeautifulSoup
from common import Common


class Table:

    @staticmethod
    def header(table):
        thead = table.find('thead')
        tr = thead.find_all('th')
        head = []
        for title in tr:
            t = BeautifulSoup(str(title), 'html.parser')
            header = t.find('th').text
            if header != '' and header != 'You Save':
                head.append(header)
        return head

    def body(self, url, soup):
        if soup.find('body', class_='OneColumn _404'):
            print('Not table found!')
            with open('not-product.txt', '+a') as f:
                f.write(f'\n{url}')
            f.close()
            return [{'item': '', 'size': '', 'ships_within': '', 'msrp': '', 'sale_price': ''}]
        elif soup.find('table', attrs={'class': 'ProductGroup'}) is None:
            print('Not table found!')
            with open('not-table.txt', '+a') as f:
                f.write(f'\n{url}')
            f.close()
            return [{'item': '', 'size': '', 'ships_within': '', 'msrp': '', 'sale_price': ''}]
        else:
            table = soup.find('table', attrs={'class': 'ProductGroup'})
            header = self.header(soup)
            if len(header) < 4:
                print('3333 : \nBad table')
                with open('bad-table.txt', '+a') as f:
                    f.write(f'\n{url}')
                f.close()
                return [{'item': '', 'size': '', 'ships_within': '', 'msrp': '', 'sale_price': ''}]
            else:
                rows = table.find_all('tr')
                tbl = []
                for row in rows:
                    columns = row.find_all('td')
                    product = {}
                    for col in columns:
                        if col != '':
                            n = BeautifulSoup(str(col), 'html.parser')
                            m = n.find('td').text
                            # item
                            if col.get('class') == ['tdProductGroupDisplayItemNumber'] or [
                                    'tdProductGroupDisplayAltItemNumber'] == col.get('class'):
                                item = m
                                product['%s' % header[0]] = item
                            # size
                            elif col.get('class') == ['tdProductGroupDisplayDescription'] or col.get('class') == [
                                    'tdProductGroupDisplayAltDescription']:
                                size = m
                                if '&nbsp' in size:
                                    size = size.replace('&nbsp', '')
                                if ' with free pad' in size:
                                    size = size.replace(' with free pad', '')
                                product['%s' % header[1]] = size
                            # within_ships
                            elif col.get('class') == ['tdProductGroupDisplayAvailability'] or col.get('class') == [
                                    'tdProductGroupDisplayAltAvailability']:
                                ships_within = m
                                if ships_within != 'InStock':
                                    product['%s' % header[2]] = ships_within
                            # msrp
                            elif col.get('class') == ['tdProductGroupDisplayMSRP'] or col.get('class') == [
                                    'tdProductGroupDisplayAltMSRP']:
                                msrp = m
                                if '$' in msrp:
                                    msrp = Common.clean_price(msrp)
                                if ',' in msrp:
                                    msrp = Common.clean_price(msrp)
                                msrp = float(msrp)
                                product['%s' % header[3]] = msrp
                            # sale price
                            try:
                                if n.find(class_='sale-red'):
                                    sale_price = n.find(class_='sale-red').text
                                    sale_price = Common.clean_price(sale_price)
                                    product['%s' % header[4]] = sale_price
                                if n.find(class_='ProductGroupItemPrice'):
                                    sale_price = n.find(class_='ProductGroupItemPrice').text
                                    sale_price = Common.clean_price(sale_price)
                                    product['%s' % header[4]] = sale_price
                                if n.find(class_='ProductGroupAlternatingItemPrice'):
                                    sale_price = n.find(class_='ProductGroupAlternatingItemPrice').text
                                    sale_price = Common.clean_price(sale_price)
                                    product['%s' % header[4]] = sale_price
                            except TypeError:
                                print(TypeError)
                    if product != {} and len(product) != 1:
                        tbl.append(product)
            return tbl
