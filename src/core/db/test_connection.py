from core.db.mongo import connection

db = connection.get_database()

result = db.idk.insert_one({"ping": "pong"})

print("Inserted id: ", result.inserted_id)
