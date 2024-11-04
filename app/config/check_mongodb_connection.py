import os #it gets the env varibales and other stuff
from pymongo import MongoClient #mongodb client import
#load environmental variables
from dotenv import load_dotenv
from colorama import Fore, Back
load_dotenv() #fetches the env variables

#create variables for values from .env
MONGO_URI = os.getenv("MONGO_URI")
#create a mongodb client instance
client = MongoClient(MONGO_URI)

print(Fore.YELLOW+"Trying to connect to MongoDB...")
def check_mongodb_connection():
    try:
        
        client.admin.command({"ping":1})
        print(Fore.GREEN+"You have connected to MongoDB Successfully...")
    except Exception as e:
        print( Fore.RED + f"The following error occurred while connecting to the database: {str(e)}")