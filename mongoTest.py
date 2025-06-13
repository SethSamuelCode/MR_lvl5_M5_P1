from pymongo import MongoClient

client = MongoClient("mongodb://fluffy:pass@localhost:27017/m5Test")
db = client['m5Test']

print(db.list_collection_names())