import json
import sqlite3
from kafka import KafkaConsumer

bootstrap_servers = ['127.0.0.1:61824','127.0.0.1:61829','127.0.0.1:61830']

conn = sqlite3.connect('app-0.db')

conn.execute('''CREATE TABLE IF NOT EXISTS animals (
    NAME TEXT PRIMARY KEY NOT NULL,
    VALUE_SUM INTEGER NOT NULL)''')

consumer = KafkaConsumer('in', bootstrap_servers=bootstrap_servers)
for msg in consumer:
    x = json.loads(msg.value)
    print('Read', x)

    conn.execute('''INSERT INTO animals (NAME, VALUE_SUM) VALUES (?,?) ON CONFLICT(NAME) DO UPDATE SET VALUE_SUM = VALUE_SUM + excluded.VALUE_SUM''', (x['animal'], x['value']))
    conn.commit()
