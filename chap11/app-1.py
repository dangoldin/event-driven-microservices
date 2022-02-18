import json
from kafka import KafkaConsumer, KafkaProducer

bootstrap_servers = ['127.0.0.1:61824','127.0.0.1:61829','127.0.0.1:61830']

producer = KafkaProducer(
    bootstrap_servers=bootstrap_servers,
    value_serializer=lambda v: json.dumps(v).encode('utf-8')
    )

consumer = KafkaConsumer('in', bootstrap_servers=bootstrap_servers)
for msg in consumer:
    x = json.loads(msg.value)
    print('Read', x)

    producer.send('out', {
        'id': x['id'],
        'first_name': x['first_name'],
        'last_name': x['last_name'],
        'value': x['value'] * 2
    })

    producer.flush()
