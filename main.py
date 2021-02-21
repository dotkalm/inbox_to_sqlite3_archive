import os
from actions.gmail_backup import gmail_archive_and_expunge
from dotenv import load_dotenv
load_dotenv()
from models import c, count_rows 

email = os.getenv("GMAIL_ADDRESS")

all_ids = () 
def recursive_retrieve():
    limit = 10
    ids = gmail_archive_and_expunge(email, 'inbox', limit)
    if(len(ids[1]) == limit):
        recursive_retrieve()
    else: 
        total = count_rows()
        c.close()
        print('dun, your local db has', total[0], 'archived emails')

recursive_retrieve()
