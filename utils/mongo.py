from pymongo import MongoClient


def articles_collection(mongo_url):
    client = MongoClient(mongo_url)
    db = client.get_default_database()
    db.articles.create_index('url', unique=True)
    return db.articles
