# -*- coding: utf-8 -*-
from bs4 import BeautifulSoup
import urllib2
from carts import cart_1


class Model(object):
    db = None

    def __init__(self, config, db):
        super(Model, self).__init__()
        self.config = config
        self.db = db

    def store(self, items_url_list):
        for url in items_url_list:
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
                        self.db.mongodb[self.config.get("feed_collection")]\
                            .insert(entry)
            # print o
        return self.process()

    def process(self):
        items_id = self.db.mongodb[self.config.get("feed_collection")]\
            .distinct('item_id')
        shops_id = self.db.mongodb[self.config.get("feed_collection")]\
            .distinct('shop_id')
        # print items_id
        # print shops_id

        for shop_id in shops_id:
            shop = self.db.mongodb[self.config.get("feed_collection")].\
                find_one({"shop_id": shop_id})

            shop_name = shop["shop_name"]
            item_metaforika = shop["extra_metaforika"]
            item_anikatavoli = shop["extra_antikatavoli"]

            shop_cart = {
                "shop_name": shop_name,
                "shop_id": shop_id,
                "metaforika":item_metaforika,
                "antikatavoli": item_anikatavoli,
                "items": [],
                "items_length": 0,
                "items_price": 0
            }

            for item_id in items_id:
                item_info = self.db.mongodb[self.config.get("feed_collection")]. \
                    find_one({"shop_id": shop_id, "item_id": item_id})

                item = {}
                if item_info:
                    item["item_name"] = unicode(item_info["item_name"])
                    item["item_price"] = item_info["price"]
                    shop_cart["items_price"] += item_info["price"]
                    shop_cart["items"].append(item)

            shop_cart["items_length"] = len(shop_cart["items"])
            self.db.mongodb[self.config.get("processed_collection")].insert(shop_cart)
            return shop_cart

    def find_best(self):
        result = list(self.db.mongodb[self.config.get("processed_collection")]
                      .find({}, {"shop_name": 1,
                                "items_length": 1,
                                "items_price": 1,
                                "metaforika": 1,
                                "antikatavoli": 1,
                                "_id": 0})
                      .sort([("items_length", -1),
                             ("items_price", 1)]))

        # result.sort(key=lambda shop_data: shop_data["items_price"])
        for i in result:
            # print "price:{}, items:{}".format(i["items_price"], i["items_length"])
            print i
        return result
