from pymongo import MongoClient
client = MongoClient('mongodb://localhost',27017)  # default port
db = client['brandsbrother']


def getNextSequenceCompanyId(collection, name):
    return collection.find_and_modify(query={'_id': name}, update={'$inc': {'seq': 1}}, new=True).get('seq');


def getAllDocuments(collection):
    coll =db[collection]
    cursor = coll.find({"isActivated":"true"}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    allDocuments=[]
    for doc in cursor:
        allDocuments.append(doc)
    return (allDocuments)