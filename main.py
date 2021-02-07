import os
from actions.gmail_backup import gmail_archive_and_expunge
from dotenv import load_dotenv
load_dotenv()

email = os.getenv("GMAIL_ADDRESS")

gmail_archive_and_expunge(email, 'inbox')

