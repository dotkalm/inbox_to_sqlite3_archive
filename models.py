import sqlite3
conn = sqlite3.connect('inbox2.sqlite3')

field_map = { 'From': ['from_person', 'TEXT'], 'To': ['to_person', 'TEXT'], 'Reply-To': ['reply_to', 'TEXT'], 'Sender': ['sender', 'TEXT'], 'Subject': ['subject', 'TEXT'], 'Message-ID': ['message_id', 'TEXT UNIQUE'], 'time': ['time', 'INTEGER NOT NULL'], 'body': ['body', 'TEXT'], 'file_names': ['file_names', 'TEXT'], 'original_file_names': ['original_file_names', 'TEXT'], 'original_file_ext': ['original_file_ext', 'TEXT'], 'uid': ['uid', 'TEXT'], 'In-Reply-To': ['in_reply_to', 'TEXT'], 'References': ['email_references', 'TEXT'], 'Bcc': ['b_c_c', 'TEXT'], 'Cc': ['c_c', 'TEXT'] }

c = conn.cursor()
def create_db(table_name):
    insert_string_head = 'CREATE TABLE IF NOT EXISTS ' + table_name + ' (id INTEGER PRIMARY KEY, '
    field_map_values = tuple(field_map.values())
    for i in  range(len(field_map_values)):
        key = field_map_values[i][0] + ' ' 
        data_type = field_map_values[i][1]
        type_string = data_type
            
        if i == len(field_map_values) -1:
            insert_string_head = insert_string_head + key + type_string 
        else:
            insert_string_head = insert_string_head + key + type_string + ', '
    insert_string = insert_string_head + ")"
    c.execute(insert_string)


def insert_row(row, table_name):
    data_tuple = tuple(row.values())
    insert_string_head = 'INSERT INTO ' + table_name + '('
    insert_string_tail = ' VALUES('
    key_tuple = tuple(row.keys())
    if len(key_tuple) > 0:
        for i in  range(len(key_tuple)):
            key = key_tuple[i]
            val = data_tuple[i]
            if i != len(row.keys()) -1:
                insert_string_head = insert_string_head + key + ', '
                insert_string_tail = insert_string_tail + '?, '
            else:
                insert_string_head = insert_string_head + key + ')'
                insert_string_tail = insert_string_tail + '?)'
        insert_string = insert_string_head + insert_string_tail 
        tup = tuple(row.values())
        print(insert_string, tup)
        return c.execute(insert_string, tup)
    else:
        return ''
