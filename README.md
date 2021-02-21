# inbox_to_sqlite3_archive
back up then expunge your inbox to a highly portable sqlite3 database. script includes models for data types and relationships.


for info about creating virtual env <br/>
https://docs.python.org/3/tutorial/venv.html

I named my environment .inbox do whatever you want
source .inbox/bin/activate

# only 1 dependency!!!!
```pip install requirements.txt```
tantamount to:
```pip install python-dotenv```

	create an APP PASSWORD for your gmail account and enable imap access in gmail settings also toggle auto-expunge off
vi .env
```
    GMAIL_PASSWORD=""
    GMAIL_ADDRESS=""
```
```:wq```

then simply run ```python3 main.py```

your attachments will be renamed the unix timestamp based on the date from email header along with trailing index of attachments array. these can be found in email_attachments_from_backup folder that is created when main.py runs. each email will be saved as a row in the sqlite3 db that is generated when main.py is run. 

note: these will emails will be removed from your inbox but you will need to search for an empty string then "select all emails in this search" and delete forever. 

# YOU DID IT 
