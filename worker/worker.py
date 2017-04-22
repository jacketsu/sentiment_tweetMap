import threading
import os
import time
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as features
import boto3
import json
from kafka import KafkaConsumer, KafkaProducer

natural_language_understanding = NaturalLanguageUnderstandingV1(
		version='2017-02-27',
		username='82e07fd0-a7ec-41b6-978c-b33ebb5d2826',
		password='4KvREkMTNRbu')

sns = boto3.client('sns', region_name='us-east-1')
arn = 'arn:aws:sns:us-east-1:164250278793:sns'

def worker():
        consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                 group_id='my-group',
                                 auto_offset_reset='largest')
        consumer.subscribe(['tweets'])
        while True:
                for message in consumer:
                        msg = message.value.decode()
                        msg = json.loads(msg)
                        text = msg["text"]
                        try:
                                res = natural_language_understanding.analyze(text=text, features=[features.Sentiment()])
                                emotion = (json.dumps(res['sentiment']['document']['label'], indent=2))
                                print(emotion)

                        except Exception as e:
                                print("ERROR: " + str(e))
                                emotion = "neutral"
                                print(emotion)
                                msg["sentiment"] = emotion
                                sns_msg = json.dumps({"default":json.dumps(msg)})
                                sns.publish(TargetArn=arn, MessageStructure='json', Message=sns_msg)
                                print(msg)




for i in range(3):
	thread = threading.Thread(target=worker, name="worker")
	thread.start()

