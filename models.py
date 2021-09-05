from flask import Flask
from os import path
from pymongo import MongoClient
from config import MONGO_CLIENT_TEST, MONGO_CLIENT_LIVE, TEST_DB

app = Flask(__name__)

client = MongoClient(MONGO_CLIENT_TEST, retrywrites=False)

db = client.get_database(TEST_DB)

########################################## SCHEMA VARIABLES ##################################################
PROFILE_ID = "profile_id"
ID = "id"
ENROLLED_SECONDS = "enrolled_seconds"
ENROLLMENT_COUNT = "enrollment_count"
EMBEDDINGS = "embeddings"
PROFILE_ID_LIST = "profile_id_list"

####################### MODELS FOR FULL IMPLEMENTATION ######################################
profile_doc = {
    PROFILE_ID: "",
    ENROLLED_SECONDS: 0,
    ENROLLMENT_COUNT: 0,
    EMBEDDINGS: b"",
}


if __name__ == "__main__":
    for coll in db.list_collection_names():
        db.drop_collection(coll)
    db.create_collection("Profile")
    db.create_collection("Log")
