

def getNextSequenceProjectId(collection, name):
    return collection.find_and_modify(query={'_id': name}, update={'$inc': {'seq': 1}}, new=True).get('seq');
