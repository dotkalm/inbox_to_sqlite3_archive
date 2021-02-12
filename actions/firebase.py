import os
import json
import firebase_admin
from google.cloud import storage
from firebase_admin import credentials
from firebase_admin import auth
from firebase_admin import firestore
from firebase_admin import storage as firebase_storage 
from dotenv import load_dotenv

load_dotenv()
credPath = os.getenv("GOOGLE_APPLICATION_CREDENTIALS")
bucket_url = os.getenv("BUCKET_URL")
cred = credentials.Certificate(credPath)
firebase_admin.initialize_app(cred)
db = firestore.client()
client = storage.Client()
bucket = client.get_bucket(bucket_url)

def set_doc(collection_name, dictionary, uid):
    print(collection_name, dictionary, uid)
    db.collection(collection_name).document(uid).set(dictionary)

def verify_token(id_token):
    return auth.verify_id_token(id_token)

def upload_blob(source_file_name, destination_blob_name):
    print(source_file_name, destination_blob_name, "28")
    blob = bucket.blob(destination_blob_name)
    blob.upload_from_filename(source_file_name)
    return destination_blob_name

