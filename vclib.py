from pymongo import MongoClient
client = MongoClient('mongodb://localhost',27017)  # default port
db = client['victorcalls']


def getNextSequenceCompanyId(collection, name):
    return collection.find_and_modify(query={'_id': name}, update={'$inc': {'seq': 1}}, new=True).get('seq');


def getAllDocuments(collection):
    coll =db[collection]
    cursor = coll.find({"isActivated":"true"}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    allDocuments=[]
    for doc in cursor:
        allDocuments.append(doc)
    return (allDocuments)

def addCompany(document):
    coll = db['Company']
    #db.users.insert({'CompanyId': getNextSequenceCompanyId(db.CompanyCounter, "CompanyId"), 'name': "Sara a"})
    i=coll.find().count()
    document["companyId"] = i+1
    doc_id = coll.insert_one(document).inserted_id
    return doc_id

def updateCompany(document,id):
    coll = db['Company']
    res = coll.update({"companyId":id},document)
    return  res

def addProjectToCompany(document,id):
    coll = db['Company']
    cmp=coll.find_one({"companyId":id})
    cmp['projects'].append(document)
    res = coll.update({"companyId":id},cmp)
    return  res

def addDocProjectToCompany(document,cid,pid):
    coll = db['Company']
    cmp=coll.find_one({"companyId":cid})
    #if cmp['projects']['projectId']==
    ind=0
    for x in cmp['projects']:
        if x['projectId']==pid:
            index=ind
            cmp['projects'][index]['documents'].append(document)
            break
        ind = ind+1
    #cmp['projects'][index]['documents'].append(document)
    res = coll.update({"companyId":cid},cmp)
    return  res

def addPorject(document):
    coll=db['Project']
    i = coll.find().count()
    document["projectId"] = i + 1
    doc_id = coll.insert_one(document).inserted_id
    return document

def addDocument(document):
    coll=db['Document']
    i = coll.find().count()
    document["documentId"] = i + 1
    doc_id = coll.insert_one(document).inserted_id
    return document

def addDocumentToProject(document,pid):
    print('add doc to projecr',pid)
    coll=db['Project']
    doc = coll.find_one({"projectId": pid})
    doc['documents'].append(document)
    res = coll.update({"projectId": pid}, doc)
    return res