import os
from actions.gmail_backup import gmail_archive_and_expunge
from dotenv import load_dotenv
load_dotenv()
from models import c
from actions.firebase import upload_blob

email = os.getenv("GMAIL_ADDRESS")

all_ids = () 
def recursive_retrieve():
    limit = 10
    ids = gmail_archive_and_expunge(email, 'inbox', limit)
    if(len(ids[1]) == limit):
        print(ids[1], 13)
        recursive_retrieve()
    else: 
        c.close()
        print('done????')
        print(len(all_ids), 'ids length')

def upload_sqlite_blob(file_name):
    file_path = os.path.join(os.getcwd(), file_name)
    print(file_path)
    uploaded_file = upload_blob(file_path, 'db/' + file_name)
    print(uploaded_file)
    
