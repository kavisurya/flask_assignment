import pymongo
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
myclient = pymongo.MongoClient(os.getenv("MONGO_URI"))
mydb = myclient[os.getenv("MONGO_DB_NAME")]
mycol = mydb[os.getenv("MONGO_COLLECTION_NAME")]

def insert(fname, lname, email, mobile, password, yog, gender):    

    user_insert = {
        "fname" : fname, 
        "lname" : lname,
        "email" : email, 
        "mobile" : mobile, 
        "password" : password, 
        "yog" : yog, 
        "gender" : gender}
        

    result = mycol.insert_one(user_insert)
    if(result):
        return True
    else:
        return False
    
    
def get_all():
    pass


def get_by_user(email):
    result = mycol.find_one({'email' : email})
    return result


def update():
    pass


def delete():
    pass


