import sqlite3
conn = sqlite3.connect('hello3.sqlite3')

field_map = { 'From': 'from_person', 'To': 'to_person', 'Reply-To': 'reply_to', 'Sender': 'sender', 'Subject': 'subject', 'Message-ID': 'message_id', 'time': 'time', 'body': 'body', 'files': 'files', 'uid': 'uid', 'In-Reply-To': 'in_reply_to', 'References': 'email_references', 'Bcc': 'b_c_c', 'Cc': 'c_c' }

c = conn.cursor()
def create_db():
    #c.execute
    print('''CREATE TABLE inbox (id INTEGER PRIMARY KEY, time INTEGER NOT NULL, to_person TEXT, c_c TEXT, b_c_c TEXT, body TEXT, email_references TEXT UNIQUE, message_id TEXT, in_reply_to TEXT, reply_to TEXT, files TEXT, from_person TEXT, sender TEXT, subject TEXT, uid TEXT)''')


def insert_row(row, table_name):
    sqlite_insert_with_param = '''INSERT INTO inbox (time, to_person, c_c, b_c_c, body, email_references, message_id, in_reply_to, reply_to, files, from_person, sender, subject, uid) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data_tuple = tuple(row.values())
    insert_string_head = 'INSERT INTO' + table_name + '(' 
    insert_string_tail = 'VALUES('
    for i in  range(len(row.keys())):
        key = row.keys()[i]
        val = data_tuple[i]
        if i == len(row.keys()) -1:
            insert_string_head = insert_string_head + key + ', '
            insert_string_tail = insert_string_tail + '?, '
        else:
            insert_string_head = insert_string_head + key + ')'
            insert_string_tail = insert_string_tail + '?)'
    insert_string = "'''" + insert_string_head + insert_string_tail + "'''" 
    print(insert_string, 27)
    ##c.execute(sqlite_insert_with_param, data_tuple)
