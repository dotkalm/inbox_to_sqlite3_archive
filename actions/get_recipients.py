import email.utils as eut
import re
import email
ADDR_PATTERN = re.compile('<(.*?)>')

def get_recipients(msg, recipients):
    """Given a parsed message, extract and return recipient list"""
    msg_fields = ['From', 'To', 'Cc', 'Bcc', 'Reply-To', 'Sender', 'Subject', 'In-Reply-To', 'Message-ID','References']
    for f in msg_fields:
        if msg[f] is None:
            continue
        if f == 'Subject' or f == 'Message-ID' or f == 'References':
            recipients[f] = msg[f] 
            continue
        if f == 'Cc':
            copies = msg[f]
            recipients["Cc"] = copies
        else:
            recipients[f] = msg[f] 

    return recipients 
