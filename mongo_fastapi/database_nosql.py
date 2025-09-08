import os
from pymongo import MongoClient
from dotenv import load_dotenv

load_dotenv()

# MongoDB connection
MONGO_URI = os.getenv("MONGO_URI")
MONGO_DB = os.getenv("MONGO_DB")

mongo_client = MongoClient(MONGO_URI, tls=True)
mongo_db = mongo_client[MONGO_DB]
profiles_collection = mongo_db["profiles"]
