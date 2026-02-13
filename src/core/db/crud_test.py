import pymongo

from core.config import settings

class TestIDK:
    _instance = None

    def __new__(cls, *args, **kwargs):
        if cls._instance is None:
            cls._instance = super().__new__(cls)
            cls._instance._client = None
            cls._instance._initialized = False
        return cls._instance

    def __init__(self):
        if self._initialized:
            return
        try:
            self._client = MongoClient(settings.MONGO_DATABASE_HOST)
            self._initialized = True

        except ConnectionFailure as exc:
            raise ConnectionFailure("Failed to connect to MongoDB")

    def get_database(self):
        assert self._client is not None, "Database connection not initialized"
        return self._client[settings.MONGO_DATABASE_NAME]

    def close(self):
        if self._client is not None:
            self._client.close()
            print("MongoDB connection closed")




class Student:
    def __init__(self, sid, username, email, department):
        self.sid = sid
        self.username = username
        self.email = email
        self.department = department

class CRUDTest:
    def __init__(self, client: pymongo.MongoClient | None = None, database=None, collection=None):
        if client is None:
            raise ValueError("Client cannot be None")
        else:
            self.client = client
            self.database = database
            self.collection = collection

            self.database = self.client[database]
            self.collection = self.database[collection]

    def insert(self, student):
        try:
            # creating a dictionary with what we want to insert
            data = {
                "_id": student.sid,
                "username": student.username,
                "email": student.email,
                "department": student.department,
            }

            # Inserting the student data into the students collection and obtain the
            # inserted_id
            sid = self.collection.insert_one(data).inserted_id

            print(f"Data inserted with ID: {sid}")
            return sid
        except Exception as e:
            print(f"Error: {e}")
            return None

    # fetch data
    def fetch(self, sid: str):
        # Querying the students collection
        data = self.collection.find_one({"_id": sid})
        return data

    def update(self, sid, student):
        data = {
            'username': student.username,
            'email': student.email,
            'department': student.department,
        }

        # update
        self.collection.update_one({'_id': sid}, {'$set': data})

    def delete(self, sid):
        self.collection.delete_one({'_id': sid})

    # error handling and cleanup
    def cleanup(self):
        self.client.close()
        print("connection Closed")

crud = CRUDTest(client=pymongo.MongoClient("mongodb://admin:password@localhost:27017/"), database="test", collection="students")
# student = Student("2", "ali_rahmani", "ali@example.com", "Computer Eng")
# sid = crud.insert(student)

# 123
student=Student("2", "ali_rahmani", "ali@gmail.com", "nothing")
crud.update(sid="2", student=student)

data = crud.fetch("2")
print(data)
