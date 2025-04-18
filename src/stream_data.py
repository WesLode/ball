import time
from confluent_kafka import Consumer
from confluent_kafka import Producer

from report.box_score import score_table


config = {
    # User-specific properties that you must set
    'bootstrap.servers': 'localhost:33206',
    # 'default.topic.config': {'api.version.request': True},
    # 'client.id': socket.gethostname(),
    # 'group.id': 'test',
    # 'security.protocol': 'SSL',
    # 'ssl.providers':'legacy',
    # 'ssl.endpoint.identification.algorithm' : 


    # Fixed properties
    'acks': 'all'
}

producer = Producer(config)


x, x_status =score_table()
topic = 'LiveScore'

def acked(err, msg):
    if err is not None:
        print("Failed to deliver message: %s: %s" % (str(msg), str(err)))
    else:
        print("Message produced: %s" % (str(msg)))

# while 

try:
    while min(x_status) != 4:
        x, x_status =score_table()

        producer.produce(topic, key="Peanut", value=x, callback=acked)

        producer.poll(1)
        time.sleep(5)
    print('The Game has ended')


except KeyboardInterrupt:
    print("Polling stopped.")
