from flask import Flask, jsonify
from flask import request
from pymongo import MongoClient
import  companylib
import vclib
import json
import requests
import pprint
import time
import string
import random
client = MongoClient('mongodb://localhost',27017)  # default port
db = client['victorcalls']
coll=db['Company']
# client = MongoClient('localhost', 27017) explicitely

headers = {
            "Content-Type": "application/json",
            "Auth": "vcToken"
        }
serverUrl = '192.168.1.10'
serverPort = '5005'
print('running victorcalls.py')

app = Flask(__name__)
app.config['JSON_SORT_KEYS'] = False

@app.route('/api/companies/', methods=['GET'])
def getCompanies():
    collection = 'Company'
    return jsonify(vclib.getAllDocuments(collection))

@app.route('/api/', methods=['GET'])
def getapi():
    return 'success'

@app.route('/api/projects/', methods=['GET'])
def getProjects():
    collection = 'Project'
    return jsonify(vclib.getAllDocuments(collection))

@app.route('/api/add/company/', methods=['POST'])
def insertIntoCompany():
    content=request.json
    response=vclib.addCompany(content)
    return 'success'

@app.route('/api/update/company/<int:id>', methods=['PUT'])
def updateComapny(id):
    content = request.json
    response = vclib.updateCompany(content,id)
    return 'success'

@app.route('/api/addProject/<int:cid>', methods=['PUT'])
def addProjectToComapny(cid):
    content = request.json
    resDocument=vclib.addPorject(content)
    response = vclib.addProjectToCompany(resDocument,cid)
    return 'success'

@app.route('/api/addDocument/<int:cid>/<int:pid>', methods=['PUT'])
def addDocProjectToComapny(cid,pid):
    content = request.json
    resDoc = vclib.addDocument(content)
    res= vclib.addDocumentToProject(resDoc,pid)
    response = vclib.addDocProjectToCompany(resDoc,cid,pid)
    return 'success'


if __name__ == '__main__':
    app.run(host=serverUrl,port=serverPort)
