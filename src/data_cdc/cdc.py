import json

from bson import json_util
from core.config import settings
from core.db.mongo import MongoDatabaseConnector
from core.mq import publish_to_rabbitmq

def stream_process():
    try:
        client = MongoDatabaseConnector()
        db = client.get_database()


        print("Connected to MongoDB")

        # watch changes in a specific collection
        changes = db.watch([{"$match": {"operationType": {"$in": ["insert"]}}}])
        for change in changes:
            data_type = change["ns"]["coll"]
            entry_id = str(change["fullDocument"]["_id"])

            change["fullDocument"].pop("_id")
            change["fullDocument"]["type"] = data_type
            change["fullDocument"]["entry_id"] = entry_id

            if data_type not in ["articles", "posts", "repositories"]:
                            print(f"Unsupported data type: '{data_type}'")
                            continue

        # use json_utils to serialize the fullDocument
        data = json.dumps(change["fullDocument"], default=json_util.default)
        print(f"Change detected and serialized for a data sample of type {data_type}.")

        # send data to RabbitMQ
        publish_to_rabbitmq(queue_name=settings.RABBITMQ_QUEUE_NAME, data=data)
        print(f"Data of type '{data_type}' published to RabbitMQ.")
    except Exception as e:
            print(f"An error occurred: {e}")

if __name__ == "__main__":
    stream_process()
