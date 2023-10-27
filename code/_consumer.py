from confluent_kafka import Consumer

conf = {'bootstrap.servers': '192.168.0.226',
        'group.id': '1',
        'session.timeout.ms': 6000,
        # 'on_commit': my_commit_callback,
        'auto.offset.reset': 'earliest'}

while True:
    consumer = Consumer(conf)
    print(consumer)