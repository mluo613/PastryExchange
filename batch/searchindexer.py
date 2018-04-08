from kafka import KafkaConsumer
from elasticsearch import Elasticsearch
import json
import time

time.sleep(20)

while True:
    consumer = KafkaConsumer('new-listings-topic', group_id='listing-indexer', bootstrap_servers=['kafka:9092'])
    es = Elasticsearch(['es'])
    for message in consumer:
        new_listing = json.loads((message.value).decode('utf-8'))
        es.index(index='listing_index', doc_type='listing', id=json.loads(new_listing)['id'], body=new_listing)
        es.indices.refresh(index="listing_index")
