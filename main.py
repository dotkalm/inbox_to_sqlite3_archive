import os
from actions.gmail_backup import gmail_archive_and_expunge
from dotenv import load_dotenv
load_dotenv()
from models import c

email = os.getenv("GMAIL_ADDRESS")

all_ids = () 
def recursive_retrieve():
    limit = 100
    ids = gmail_archive_and_expunge(email, 'inbox', limit)
    if(len(ids[1]) == limit):
        print(ids[1], 13)
        recursive_retrieve()
    else: 
        c.close()
        print('done????')
        print(len(all_ids), 'ids length')
recursive_retrieve()


