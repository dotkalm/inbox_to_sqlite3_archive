import sqlite3
conn = sqlite3.connect('hello3.sqlite3')
c = conn.cursor()
def create_db():
    c.execute('''CREATE TABLE inbox (id INTEGER PRIMARY KEY, time INTEGER NOT NULL, toto TEXT, Cc TEXT, Bcc TEXT, Body TEXT, References TEXT UNIQUE, MessageID TEXT, InReplyTo TEXT, ReplyTo TEXT, files TEXT, From TEXT, Sender TEXT, Subject TEXT, uid TEXT)''')


def insert_row(row):
    sqlite_insert_with_param = '''INSERT INTO inbox (time, To, Cc, Bcc, Body, References, MessageID, InReplyTo, ReplyTo, files, From, Sender, Subject, uid) VALUES(?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?, ?)'''
    data_tuple = tuple(row.values())
    c.execute(sqlite_insert_with_param, data_tuple)
    print(data_tuple)
