from pymongo import (
    MongoClient,
    errors
)

mongo_client = None
mongodb = None
mongo_feed_collection = 'feed'
mongo_processed_collection = 'processed'


def initialize():
    global mongo_client, mongodb

    # Connection to MongoDB
    try:
        mongo_client = MongoClient('mongodb://localhost:27017/')
        mongodb = mongo_client.skroutz_cart
    except errors.ConnectionFailure, e:
        print "Could not connect to MongoDB: %s" % e

