from core.db.mongo import connection


db = connection.get_database()

result = db.idk.find()

print("Inserted id: ", result.inserted_id)
