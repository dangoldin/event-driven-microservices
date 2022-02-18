import json
from kafka import KafkaConsumer
import multiprocessing
from collections import defaultdict
import time
import sqlite3

bootstrap_servers = ['127.0.0.1:61824','127.0.0.1:61829','127.0.0.1:61830']

class Consumer(multiprocessing.Process):
    daemon = True
    topic = None
    conn = None

    def __init__(self, topic, conn):
        multiprocessing.Process.__init__(self)
        self.stop_event = multiprocessing.Event()
        self.topic = topic
        self.conn = conn

    def stop(self):
        self.stop_event.set()

    def run(self):
        c = KafkaConsumer(bootstrap_servers=bootstrap_servers)
        c.subscribe(self.topic)

        while not self.stop_event.is_set():
            for msg in c:
                x = json.loads(msg.value)
                animal = x['animal']

                if self.topic == 'in':
                    conn.execute('''INSERT INTO animals (NAME, VALUE0, VALUE1) VALUES (?,?,?) ON CONFLICT(NAME) DO UPDATE SET VALUE0 = VALUE0 + excluded.VALUE0, VALUE1 = VALUE1 + excluded.VALUE1''', (animal, x['value'], 0))
                else:
                    conn.execute('''INSERT INTO animals (NAME, VALUE0, VALUE1) VALUES (?,?,?) ON CONFLICT(NAME) DO UPDATE SET VALUE0 = VALUE0 + excluded.VALUE0, VALUE1 = VALUE1 + excluded.VALUE1''', (animal, 0, x['value']))
                conn.commit()

                curr = conn.execute('''SELECT * FROM animals WHERE name = ?''', (animal,))
                row = curr.fetchone()

                if row[1] > 0 and row[2] > 0:
                    print('{} has values {} and {}'.format(animal, row[1], row[2]))

        c.close()

if __name__ == '__main__':
    multiprocessing.set_start_method('fork')

    conn = sqlite3.connect('app-2.db')

    conn.execute('''CREATE TABLE IF NOT EXISTS animals (
        NAME TEXT PRIMARY KEY NOT NULL,
        VALUE0 INTEGER NOT NULL,
        VALUE1 INTEGER NOT NULL
        )''')

    consumer = Consumer('in', conn)
    consumer2 = Consumer('in2', conn)

    consumer.start()
    consumer2.start()

    consumer.join()
    consumer2.join()

    time.sleep(300)

    consumer.stop()
    consumer2.stop()
