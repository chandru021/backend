from pymongo import MongoClient

client = MongoClient("mongodb+srv://20z342:cBwPEGWx2iMWCUyE@cluster0.xdefz6l.mongodb.net/")
dbName = "complaints"
collectionName = "user_locations"
collection = client[dbName][collectionName]

# Read all documents in the collection
documents = collection.find()

# Update each document to add the imageUrl attribute with an initial value of ""
for document in documents:
    collection.update_one(
        {"_id": document["_id"]},
        {"$set": {"imageUrl": ""}}
    )

print("Added 'imageUrl' attribute with initial value to all documents in the collection.")