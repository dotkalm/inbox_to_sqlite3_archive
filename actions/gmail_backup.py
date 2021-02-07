import os
import time
import imaplib
import email
from email.parser import HeaderParser
import traceback 
from dotenv import load_dotenv
from datetime import datetime
from models import insert_row, create_db
import models
import time
import json
import email.utils as eut
from actions.get_recipients import get_recipients
load_dotenv()
password = os.getenv("GMAIL_PASSWORD")

def get_email_ids(mail, label='INBOX', criteria='ALL', max_mails_to_look=300):
    mail.select(label)
    type, data = mail.uid('search', None, "ALL") 
    mail_ids = data[0]
    id_list = mail_ids.split()
    id_list = id_list[: min(len(id_list), max_mails_to_look)]
    return id_list

def roles_with_subject(raw_email, return_object):
    email_message = email.message_from_string(raw_email)
    recipients = get_recipients(email_message, return_object)
    return recipients

def get_gmail(email_address):
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(email_address, password)
    create_db()
    return mail

def gmail_archive_and_expunge(email_address):
    gmail = get_gmail(email_address)
    mail_ids = get_email_ids(gmail)

    def get_email_msg(email_id):
        all_object = {}
        email_id = str(int(email_id))
        type, data = gmail.uid('fetch', str(email_id), '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('ISO-8859-1')
        email_message = email.message_from_string(raw_email_string)
        parser = HeaderParser()
        h = parser.parsestr(raw_email_string)
        all_object = roles_with_subject(raw_email_string, all_object)
        date = email_message['Date']
        parsed = eut.parsedate(date)
        time_list = list(parsed)
        time_tuple = tuple(time_list)
        time_value = time.mktime(time_tuple) * 1000
        all_object['time'] = int(time_value)
        file_string = email_id + '_' + str(int(time_value))
        file_names = []
        for part in email_message.walk():
            content_disposition = str(part.get("Content-Disposition"))
            content_type = part.get_content_type()
            if content_disposition == 'multipart':
                continue
            if content_disposition is None:
                continue
            message_body = part.get_payload(i=None, decode=True)
            if content_type == 'text/plain' and "attachment" not in content_disposition:
                if bool(message_body):
                    all_object['body'] = str(message_body)
            file_name = part.get_filename()
            if bool(file_name):
                filename_unique = file_string + '_' + file_name
                file_path = os.path.join(os.getcwd(), 'email_attachments_from_backup/' + filename_unique )
                file_names.append(filename_unique)
                if not os.path.isfile(file_path) :
                    fp = open(file_path, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()
        all_object['files'] = ", ".join(file_names)
        all_object['uid'] = email_id
        return all_object

    for mail_id in mail_ids:
        msg = get_email_msg(mail_id)
        print(msg)
        insert_row(msg)
