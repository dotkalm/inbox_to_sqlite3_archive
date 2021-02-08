import os
import time
import imaplib
import email
from email.parser import HeaderParser
import traceback 
from dotenv import load_dotenv
from datetime import datetime
from models import insert_row, create_db, field_map, c, conn
import models
import time
import json
import email.utils as eut
from actions.get_recipients import get_recipients
load_dotenv()
password = os.getenv("GMAIL_PASSWORD")

def get_email_ids(mail, label='INBOX', criteria='ALL', max_mails_to_look=3000):
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

def get_gmail(email_address, table_name):
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(email_address, password)
    create_db(table_name)
    return mail

def gmail_archive_and_expunge(email_address, table_name):
    gmail = get_gmail(email_address, table_name)
    mail_ids = get_email_ids(gmail)
    header_keys = {}
    def get_email_msg(email_id):
        all_object = {}
        email_id = str(int(email_id))
        type, data = gmail.uid('fetch', str(email_id), '(RFC822)')
        if bool(data[0]):
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
            original_file_names = []
            original_file_ext = []
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
                    f_name, f_ext = os.path.splitext(file_name)
                    filename_unique = str(int(time_value)) + '_' + email_id + f_ext
                    file_path = os.path.join(os.getcwd(), 'email_attachments_from_backup/' + filename_unique)
                    file_names.append(filename_unique)
                    original_file_names.append(file_name)
                    original_file_ext.append(f_ext)
                    if not os.path.isfile(file_path):
                        fp = open(file_path, 'wb')
                        if part.get_payload(decode=True):
                            fp.write(part.get_payload(decode=True))
                            fp.close()
            all_object['file_names'] = ", ".join(file_names)
            all_object['original_file_names'] = ", ".join(original_file_names)
            all_object['original_file_ext'] = ", ".join(original_file_ext)
            all_object['uid'] = email_id
        return all_object
    for mail_id in mail_ids:
        msg = get_email_msg(mail_id)
        gmail.store(mail_id, '+FLAGS', '\\Deleted')
        new_msg = {}
        for key in msg.keys():
            db_key = field_map[key][0]
            new_msg[db_key] = msg[key]
        insert_row(new_msg, table_name)
    success = gmail.expunge()
    print(success)
    gmail.close()
    gmail.logout()
    conn.commit()
    c.close()
    return mail_ids
