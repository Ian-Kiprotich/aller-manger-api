import os
#import MongoClient Object
from pymongo import MongoClient
#load environmental variables
from dotenv import load_dotenv
load_dotenv()

#create variables for values from .env
MONGO_URI = os.getenv("MONGO_URI")
#create a mongodb client instance
client = MongoClient(MONGO_URI)

#create/ bring in database
aller_db = client["aller_manger_db"]

#create collections to be used

#user accounts collections
accounts = aller_db["accounts"]

#create a collection for the restaurant tables
tables = aller_db["tables"]
