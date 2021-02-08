import os
from actions.gmail_backup import gmail_archive_and_expunge
from dotenv import load_dotenv
load_dotenv()

email = os.getenv("GMAIL_ADDRESS")

all_ids = () 
def recursive_retrieve():
    limit = 1000
    ids = gmail_archive_and_expunge(email, 'inbox', limit)
    all_ids = all_ids + ids
    print(len(all_ids), 'expunged ids length')
    if(len(ids[1]) == limit):
        recursive_retrieve()
    else: 
        print('done????')
        print(len(all_ids), 'expunged ids length')
