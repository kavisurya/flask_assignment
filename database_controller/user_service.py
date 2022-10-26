import pymongo
import os
from dotenv import load_dotenv
import pymongo

load_dotenv()
myclient = pymongo.MongoClient(os.getenv("MONGO_URI"))
mydb = myclient[os.getenv("MONGO_DB_NAME")]
mycol = mydb[os.getenv("MONGO_COLLECTION_NAME")]

# User insertion
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
    

# get the user details by email
def get_by_user(email):
    result = mycol.find_one({'email' : email})
    return result

# update the user details by email
def update(fname, lname, email, mobile, yog, gender):

    user_profile_update = {
        "fname" : fname, 
        "lname" : lname,
        "mobile" : mobile, 
        "yog" : yog, 
        "gender" : gender}

    myquery = { "email": email }
    newvalues = { "$set": user_profile_update }

    result = mycol.update_one(myquery, newvalues)

    if(result):
        return True
    else:
        return False

# delete the user account by email
def delete(email):
    myquery = { "email": email }
    result = mycol.delete_one(myquery) 

    if(result):
        return True
    else:
        return False

