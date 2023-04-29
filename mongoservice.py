from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi

# connecting to (mongodb.com) database
mongodb_url = "mongodb+srv://varshav0119:{password}@dev.i0hulwp.mongodb.net/?retryWrites=true&w=majority"
client = MongoClient(mongodb_url.format(password="postcanvasdb"),
                     server_api=ServerApi('1'),
                     tlsAllowInvalidCertificates=True)

db = "pdfs"
collection = "links"

def insert(document):
  return client[db][collection].insert_one(document)

def update(link, document):
  client[db][collection].update_one({"link": link}, {"$set": document})

def exists(link):
  record = client[db][collection].find_one({"link": link})
  if record:
    return True
  else:
    return False
