import email.utils as eut
import re
import email
ADDR_PATTERN = re.compile('<(.*?)>')

def get_recipients(msg):
    """Given a parsed message, extract and return recipient list"""
    recipients = {}
    msg_fields = ['From', 'To', 'Cc', 'Bcc', 'Reply-To', 'Sender', 'Subject', 'uid']

    for f in msg_fields:
        if f is msg_fields[-1]:
            recipients[f] = msg[f] 
            continue
        if f is msg_fields[-2]:
            recipients[f] = msg[f] 
            continue
        if msg[f] is None:
            continue
        person = email.utils.parseaddr(msg[f])
        recipients[f] = person 

    return recipients 
