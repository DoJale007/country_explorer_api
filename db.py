from pymongo import MongoClient
import os
from dotenv import load_dotenv

load_dotenv()

# Connect to Mongo Atlas Cluster
mongo_client = MongoClient(os.getenv("MONGO_URI"))

# Assess database
country_explorer_db = mongo_client["country_explorer_db"]

# Select a collection
favorites_collection = country_explorer_db["favorites"]
