from flask import Flask, jsonify
from flask import request
from pymongo import MongoClient
import json
import requests
import pprint
import time
import string
import random
client = MongoClient('mongodb://localhost',27017)  # default port
# client = MongoClient('localhost', 27017) explicitely

headers = {
            "Content-Type": "application/json",
            "Auth": "vcToken"
        }
def getNextSequence(collection, name):
    return collection.find_and_modify(query={'_id': name}, update={'$inc': {'seq': 1}}, new=True).get('seq');

def getNextSequenceNew(collection, name):
    return collection.find_and_modify(query={'_id': name}, update={'$inc': {'seq': 1}}, new=True).get('seq');

serverUrl = '192.168.1.10'
serverPort = '5005'

db = client['brandsbrother']
RawLeads = db['RawLeads']
Auto = db['Auto']
CompanyV = db['CompanyV']
coll1 = db['CurrentLeads']
coll2 = db['FollowUpLeads']
Companies = db['Companies']
Projects = db['Project']
User = db['User']

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

#urlResponse1 = requests.get(url1)
#time.sleep(5)
# print(urlResponse)
#jData1 = json.loads(urlResponse1.content)
#time.sleep(3)

#db = client['brands']
#coll = db['new']
from datetime import datetime

#
# doc = {
#     "title": "An article Mongodb",
#     "author": "Gaurav B",
#     "publication_date": datetime.utcnow(),
#     # more fields
# }

#coll.insert(doc)
#doc_id = coll.insert_one(doc).inserted_id

random = ''.join([random.choice(string.ascii_letters + string.digits) for n in range(32)])
print(random)


@app.route('/get', methods=['GET'])
def fetchContactUsData1():
   return 'Aarif'

@app.route('/api/rawLeads/', methods=['GET'])
def getAllRawLeads():
    #allRawLeads = []
    totalLeads =[]
    allRawLeads = RawLeads.find({}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    count=0
    for doc in allRawLeads:
        totalLeads.append(doc)
        #pprint.pprint(doc)
        #break
        count=count+1
    print(len(totalLeads))
    return jsonify(totalLeads) # with jsonify will throw error

@app.route('/api/projects/', methods=['GET'])
def getProjects():
    #allRawLeads = []
    totalProjects =[]
    cursor = Projects.find({}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    count=0
    for doc in cursor:
        totalProjects.append(doc)
        #pprint.pprint(doc)
        #break
        count=count+1
    print(len(totalProjects))
    return jsonify(totalProjects) # with jsonify will throw error

@app.route('/api/users/', methods=['GET'])
def getallusers():
    #allRawLeads = []
    totalUsers =[]
    cursor = User.find({}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    count=0
    for doc in cursor:
        doc['password']='na'
        doc['confirmPassword'] = 'na'
        totalUsers.append(doc)
    print(len(totalUsers))
    return jsonify(totalUsers) # with jsonify will throw error

@app.route('/api/user/cmpId/<int:cmpId>', methods=['GET'])
def getUsersOfCompany(cmpId):
    #allRawLeads = []
    totalUsers =[]
    cursor = User.find({"companyId": cmpId}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    count=0
    for doc in cursor:
        totalUsers.append(doc)
    print(len(totalUsers))
    return jsonify(totalUsers) # with jsonify will throw error

@app.route('/api/user/projectId/<int:id>', methods=['GET'])
def getUsersByProjectId(id):
    #allRawLeads = []
    totalUsers =[]
    cursor = User.find({"projectId": id}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    count=0
    for doc in cursor:
        totalUsers.append(doc)
    print(len(totalUsers))
    return jsonify(totalUsers)

@app.route('/api/user/namewp/<string:name>', methods=['GET'])
def getUsersByUserNmae(name):
    cursor = User.find_one({"userName": name}, {'_id': False})
    cursor['password']='na'
    cursor['confirmPassword'] = 'na'
    print(cursor['password'])
    #cursor['confirmPassword']
    return jsonify(cursor)

@app.route('/api/user/roleId/<string:id>', methods=['GET'])
def getUsersWithRoleId(id):
    #allRawLeads = []
    totalUsers =[]
    cursor = User.find({"role.roleID": id}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    count=0
    for doc in cursor:
        totalUsers.append(doc)
    print(len(totalUsers))
    return jsonify(totalUsers) # with jsonify will throw error


@app.route('/api/projects/<int:id>', methods=['GET'])
def getByProjectId(id):
    #allRawLeads = []
    cursor = Projects.find_one({"projectId": id}, {'_id': False})
    return jsonify(cursor) # with jsonify will throw error

@app.route('/api/projects/company/<int:id>', methods=['GET'])
def getprojectsByCmpId(id):
    #allRawLeads = []
    cursor = Projects.find({"companyId": id}, {'_id': False})
    projects=[]
    for doc in cursor:
        projects.append(doc)
    print(len(projects))
    return jsonify(projects) # with jsonify will throw error

@app.route('/api/companies/', methods=['GET'])
def getCompanies():
    #allRawLeads = []
    totalCompanies =[]
    cursor = Companies.find({}, {'_id': False})  # one data from top i.e bydefalt oldest Data
    count=0
    for doc in cursor:
        totalCompanies.append(doc)
        #pprint.pprint(doc)
        #break
        count=count+1
    print(len(totalCompanies))
    return jsonify(totalCompanies) # with jsonify will throw error

@app.route('/api/addCompany', methods=['POST'])
def addCompany():
	content = request.json
	print (content) # correct
	#doc_id = collection.insert_one(myData).inserted_id    # correct
	doc_id2 = Companies.insert_one(content).inserted_id  #correct
	return 'one document inserted'

@app.route('/api/user/', methods=['POST'])
def apiWithHeaders():
    if request.headers['Content-Type'] == 'application/json' and request.headers['Auth'] == 'password':
        #print(request.headers['Auth'])
        return "JSON Message: " + json.dumps(request.json)

@app.route('/api/user/header', methods=['GET'])
def apiWithHeadersuser():
    if request.headers['Content-Type'] == 'application/json' and request.headers['Auth'] == 'password':
        #print(request.headers['Auth'])
        return "JSON Message: " + request.headers['Auth']

@app.route('/api/login/<string:username>/<string:password>', methods=['GET'])
def login(username,password):
    if username=='kaushik' and password=='kaushik@123':
        return 'Hello '+username

@app.route('/api/head/', methods=['GET'])
def apiAuth():
    if request.headers['Content-Type'] == 'application/json' and request.headers['Auth'] == 'password':
        #print(request.headers['Auth'])
        return "JSON Message: "


@app.route('/api/cmpH/', methods=['GET'])
def getAllCompanies12():
    if request.headers['Content-Type'] == 'application/json' and request.headers['Auth'] == 'password':
        totalCompanies = []
        cursor = Companies.find({}, {'_id': False})  # one data from top i.e bydefalt oldest Data
        count = 0
        for doc in cursor:
            totalCompanies.append(doc)
            count = count + 1

        print(len(totalCompanies))
        return jsonify(totalCompanies)
        # with jsonify will throw error

@app.route('/api/leads/<int:sleadId>', methods=['GET'])
def getLeadsById(sleadId):
    print(sleadId)
    cursor = RawLeads.find_one({"leadId":sleadId},{'_id':False})
    #doc = cursor
    #print(doc)
    print(cursor)
    return jsonify(cursor)

@app.route('/api/cmpleads/<int:companyId>', methods=['GET'])
def getLeadsByCmpId(companyId):
    print(companyId)
    leads =[]
    cursor = RawLeads.find({"companyId":companyId},{'_id':False})
    for doc in cursor:
        leads.append(doc)
    #doc = cursor
    #print(doc)
    print(len(leads))
    return jsonify(leads)

@app.route('/api/rawleads/<int:startlimit>/<int:endlimit>')
def getrawleadsbypaging(startlimit,endlimit):
    startlimit = startlimit-1
    cursor = RawLeads.find({},{'_id':False}).skip(startlimit).limit(endlimit)
    leads=[]
    for document in cursor:
        leads.append(document)
    print(len(leads))
    return jsonify(leads)

@app.route('/api/addCounter', methods=['GET'])
def addCounter():
    #content = request.json
    #print(content)
    db.Auto.insert({'_uid': getNextSequence(db.counters, "userid"), 'name': "Kaushik"})
    return 'one counter inserted'

@app.route('/api/addCompnay1', methods=['GET'])
def addcmp():
    db.CompanyV.insert({'companyId': getNextSequenceNew(db.cmpCounter, "companyId"), 'name': "Brandsbrother"})
    return 'one counter inserted'


if __name__ == '__main__':
    app.run(host=serverUrl,port=serverPort)

#content = request.json
#print(content)
#db.CompanyV.insert({'companyId': getNextSequenceNew(db.cmpCounter, "companyId"), 'name': "Kaushik"})