# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
import mongo_db
from process import process, find_optimum
from carts import cart_1


def store(mongo_db):

    for url in cart_1:
        page = urllib2.urlopen(url)
        soup = BeautifulSoup(page, 'html.parser')
        prices = soup.find(id='prices')
        o = 0

        item_id = soup.find('div', class_='sku-card').a['data-sku-id']
        item_name = soup.find('div', class_='sku-card').h2.a.contents
        for li in prices.find_all('li'):

            entry = {"item_id": item_id,
                     "item_name": unicode(item_name[0]),
                     "shop_id": 0,
                     "shop_name": "NA",
                     "price": 0.0,
                     "extra_metaforika": 0.0,
                     "extra_antikatavoli": 0.0}

            if 'disabled' in li['class']:
                pass
            else:
                try:
                    entry["shop_id"] =  li.get('data-shopid')
                    entry["shop_name"] = li.a.img['alt']
                    div = li.find('div', class_='price')
                    try:
                        if 'product-link' in div.a['class']:
                            entry["price"] = float(div.a.contents[0].split()[0].replace(',', '.'))
                    except TypeError:
                        pass

                    extra_costs = div.find_all('span', class_='extra-cost')
                    for extra_cost in extra_costs:
                        try:
                            extra_price = float(extra_cost.contents[1].contents[0].split()[1].replace(',', '.'))
                            if u"αντικαταβολή" in extra_cost.contents[2]:
                                entry["extra_antikatavoli"] = extra_price
                            elif u"ελάχ. μεταφορικά" in extra_cost.contents[2]:
                                entry["extra_metaforika"] = extra_price
                        except IndexError:
                            pass
                    o += 1
                except AttributeError:
                    pass

                if entry["price"] != 0:
                    # print entry
                    # print"-----"*10
                    mongo_db.mongodb[mongo_db.mongo_feed_collection].insert(entry)
        # print o


if __name__ == '__main__':
    mongo_db.initialize()
    # store(mongo_db)
    # process(mongo_db)
    find_optimum(mongo_db)
