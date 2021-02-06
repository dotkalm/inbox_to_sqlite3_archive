import os
import time
import imaplib
import email
import traceback 
from dotenv import load_dotenv
from datetime import datetime
import time
import email.utils as eut
from actions.get_recipients import get_recipients

load_dotenv()

password = os.getenv("GMAIL_PASSWORD")

def get_email_ids(mail, label='INBOX', criteria='ALL', max_mails_to_look=30):
    mail.select(label)
    type, data = mail.uid('search', None, "ALL") 
    mail_ids = data[0]
    id_list = mail_ids.split()
    id_list = id_list[: min(len(id_list), max_mails_to_look)]
    return id_list

def roles_with_subject(raw_email):
    email_message = email.message_from_string(raw_email)
    recipients = get_recipients(email_message)
    return recipients

def get_gmail(email_address):
    SMTP_SERVER = "imap.gmail.com"
    SMTP_PORT = 993
    mail = imaplib.IMAP4_SSL(SMTP_SERVER)
    mail.login(email_address, password)
    return mail

def gmail_archive_and_expunge(email_address):
    gmail = get_gmail(email_address)
    mail_ids = get_email_ids(gmail)

    def get_email_msg(email_id):
        email_id = str(int(email_id))
        type, data = gmail.uid('fetch', str(email_id), '(RFC822)')
        raw_email = data[0][1]
        raw_email_string = raw_email.decode('ISO-8859-1')
        email_message = email.message_from_string(raw_email_string)
        roles_and_subject = roles_with_subject(raw_email_string)
        print(roles_and_subject, 'roles_and_subject', 47)
        date = email_message['Date']
        parsed = eut.parsedate(date)
        time_list = list(parsed)
        time_tuple = tuple(time_list)
        time_value = time.mktime(time_tuple) * 1000
        print(int(time_value))
        file_string = '' 
        for tupl in parsed: 
            file_string = file_string + '_' + str(tupl)

        for part in email_message.walk():
            if part.get_content_maintype() == 'multipart':
                continue
            if part.get('Content-Disposition') is None:
                continue
            message_body = part.get_payload(i=None, decode=False)
            ##if bool(message_body):
            fileName = part.get_filename()
            if bool(fileName):
                filePath = os.path.join(os.getcwd(), 'email_attachments_from_backup/' + str(time_value) + '_' + file_string + '_' + fileName)
                if not os.path.isfile(filePath) :
                    fp = open(filePath, 'wb')
                    fp.write(part.get_payload(decode=True))
                    fp.close()

    for mail_id in mail_ids:
        msg = get_email_msg(mail_id)

