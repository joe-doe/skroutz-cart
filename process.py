def process(mongo_db):
    items_id = mongo_db.mongodb[mongo_db.mongo_feed_collection]\
        .distinct('item_id')
    shops_id = mongo_db.mongodb[mongo_db.mongo_feed_collection]\
        .distinct('shop_id')
    # print items_id
    # print shops_id

    for shop_id in shops_id:
        shop = mongo_db.mongodb[mongo_db.mongo_feed_collection].\
            find_one({"shop_id": shop_id})

        shop_name = shop["shop_name"]
        item_metaforika = shop["extra_metaforika"]
        item_anikatavoli = shop["extra_antikatavoli"]

        shop_cart = {
            "shop_name": shop_name,
            "shop_id": shop_id,
            "item_metaforika":item_metaforika,
            "item_antikatavoli": item_anikatavoli,
            "items": [],
            "items_length": 0,
            "items_price": 0
        }

        for item_id in items_id:
            item_info = mongo_db.mongodb[mongo_db.mongo_feed_collection]. \
                find_one({"shop_id": shop_id, "item_id": item_id})

            item = {}
            if item_info:
                item["item_name"] = unicode(item_info["item_name"])
                item["item_price"] = item_info["price"]
                shop_cart["items_price"] += item_info["price"]
                shop_cart["items"].append(item)

        shop_cart["items_length"] = len(shop_cart["items"])
        mongo_db.mongodb[mongo_db.mongo_processed_collection].insert(shop_cart)
        print shop_cart


def find_optimum(mongo_db):
    result = list(mongo_db.mongodb[mongo_db.mongo_processed_collection].
                  find({}, {"shop_name": 1,
                            "items_length": 1,
                            "items_price": 1,
                            "item_metaforika": 1,
                            "item_antikatavoli": 1,
                            "_id": 0})
                  .sort([("items_length", -1),
                         ("items_price", 1)]))

    # result.sort(key=lambda shop_data: shop_data["items_price"])
    for i in result:
        # print "price:{}, items:{}".format(i["items_price"], i["items_length"])
        print i
