from pymongo.mongo_client import MongoClient
from pymongo.server_api import ServerApi
from dotenv import load_dotenv
import os

load_dotenv()

uri = os.getenv("NEW_MONGODB_CONNECTION_STRING")


# Create a new client and connect to the server
client = MongoClient(uri, server_api=ServerApi("1"))

# Send a ping to confirm a successful connection
if __name__ == "__main__":
    try:
        db = client["Hazelnut"]
        collection = db["Hazelnut_chats"]
        collection.insert_one({"session_id": 0, "chat_history_list": ["HI bro"]})
        print("You successfully connected to MongoDB!")
    except Exception as e:
        print(e)
