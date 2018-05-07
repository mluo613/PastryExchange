from kafka import KafkaConsumer
import json
import time


time.sleep(30)

while True:

    consumer = KafkaConsumer('item-detail-topic', group_id='item-detail', bootstrap_servers=['kafka:9092'])

    for message in consumer:
        #print(json.loads((message.value).decode('utf-8')))
        recommend_listing = json.loads((message.value).decode('utf-8'))
        entry = str(recommend_listing['username']) + '\t' + str(recommend_listing['item-id']) + '\n'
        f = open("access_log.txt", "a+")
        f.write(entry)
