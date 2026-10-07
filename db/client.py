import os

from dotenv import load_dotenv
from pymongo import MongoClient

load_dotenv()

mongo_uri = os.getenv("MONGODB_URI")
if not mongo_uri:
    raise RuntimeError("Configura MONGODB_URI en el entorno o en .env")

db_client = MongoClient(mongo_uri)[os.getenv("MONGODB_DB", "test")]
