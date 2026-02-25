from core.db.documents import ArticleDocument
from core.db.mongo import connection

db = connection.get_database()
collection = db[ArticleDocument.Settings.name]

print("db name:", db.name)
print("Collection name:", collection.name)

ids = [str(doc.get("_id")) for doc in collection.find({}, {"_id": 1}) if doc.get("_id")]

print(ids)
