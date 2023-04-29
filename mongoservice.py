import pymongo
import ssl

mongodb_url = "mongodb+srv://varshav0119:{password}@dev.i0hulwp.mongodb.net/?retryWrites=true&w=majority"
client = pymongo.MongoClient(mongodb_url.format(password = "postcanvasdb"), tlsAllowInvalidCertificates = True)

db = "pdfs"
collection = "links"

def insert(document):
    return client[db][collection].insert_one(document)

def update(link, document):
    client[db][collection].update_one({"link": link}, { "$set": document })

def exists(link):
    record = client[db][collection].find_one({"link": link})
    if record:
        return True
    else:
        return False
