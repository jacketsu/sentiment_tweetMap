from multiprocessing import Pool
import os
import time
# from alchemyapi import AlchemyAPI
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
		features
import boto3
import json
from kafka import KafkaConsumer, KafkaProducer

natural_language_understanding = NaturalLanguageUnderstandingV1(
		version='2017-02-27',
		username='82e07fd0-a7ec-41b6-978c-b33ebb5d2826',
		password='4KvREkMTNRbu')

# sns = boto3.client('sns')
# arn = 'arn:aws:sns:us-east-1:164250278793:sns'
# consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
# 												 auto_offset_reset='earliest')
# # consumer = KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('utf-8')))
# consumer.subscribe(['tweets'])
# print('hello')
# for message in consumer:
# 	print((message.value.decode('utf-8')))
# sentiment = ["positive","negative","neutral"]

def worker():
		# print("hello")
		# print(consumer)
		producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(0,10))
		consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
												 auto_offset_reset='largest')
		consumer.subscribe(['tweets'])
		while True:
				# consumer.subscribe(['tweets'])
				for message in consumer:
					msg = message.value.decode()
					msg = json.loads(msg)
					# print(msg)
					text = msg["text"]
					print(text)
					# print(msg['text'])
				# print(consumer)
				# 	# if len(msg) <= 0:
				# 	# 	break
				# 	print(msg.value)
					# text = json.dumps(msg['text'])
					# print(text)

					try:
						res = natural_language_understanding.analyze(text=text, features=[features.Sentiment()])
						emotion = (json.dumps(res['sentiment']['document']['label'], indent=2))
						time.sleep(10)
						print(emotion)

					# # # 	res = alchemyapi.sentiment('text', text)
					# # # 	emotion = res.get('docSentiment').get('type')
					except Exception as e:
						print("ERROR: " + str(e))
						emotion = "neutral"
						print(emotion)
					msg["sentiment"] = emotion
					print(msg)
					producer.send('sns', json.dumps(msg).encode('utf-8'))
					# 	print("snsMessage: " + msg.value)
					# sns_msg = json.dumps(msg)
					# sns.publish(TargetArn = arn, Message=json.dumps({'default':sns_msg}))

				# if len(messages)>0:
				#     for message in messages:
				#         # Get the custom author message attribute if it was set
				#         if message.message_attributes is not None:
				#             id = message.message_attributes.get('Id').get('StringValue')
				#             tweet = message.message_attributes.get('Tweet').get('StringValue')
				#             lat = message.message_attributes.get('Latitude').get('StringValue')
				#             lng = message.message_attributes.get('Longitude').get('StringValue')
				#             # senti = sentiment[random.randint(0,2)]
				#             try:
				#                 response = alchemiapi.sentiment('text',tweet)
				#                 senti = response.get('docSentiment').get('type')
				#             except Exception as e:
				#                 print("ERROR: "+str(e))
				#                 senti = "neutral"
				#             # Using SNS
				#             sns_message = {"id":id, "tweet":tweet, "lat":lat, "lng": lng, "sentiment":senti}
				#             print("SNS messsage: "+str(sns_message))
				#             sns.publish(TargetArn=arn, Message=json.dumps({'default':json.dumps(sns_message)}))
				#         # Print out the body and author (if set)
				#         # print('Id: {0}; Tweet: {1}; Latitude: {2}; Longitude: {3}; sentiment: {4}'.format(id,tweet,lat,lng,senti))
				#         # Let the queue know that the message is processed
				#         message.delete()
				# else:
				#     time.sleep(1)
print("begin")
pool = Pool(1)
for i in range(2):
	pool.apply_async(worker)
	print("begin")
pool.close()
pool.join()
print('all done')

while True:
	pass