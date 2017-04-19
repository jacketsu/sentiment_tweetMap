import threading, logging, time

from kafka import KafkaConsumer, KafkaProducer
import json

class Producer():
    # daemon = True
    def __init__(self):
        self.producer = KafkaProducer(bootstrap_servers='localhost:9092')
    def collect(self, tweet):
        # print(tweet)
        print("good")
        # print(tweet)
        # msg =  yaml.safe_load(tweet)
        self.producer.send('tweets', json.dumps(tweet).encode('utf-8'))
        # print(tweet)
        # print("good")
        # producer = KafkaProducer(bootstrap_servers='localhost:9092')

        # while True:
        #     producer.send('tweets', b"test")
        #     producer.send('tweets', b"\xc2Hola, mundo!")
        #     time.sleep(1)


class Consumer():

    def __init__(self):
        self.consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                      auto_offset_reset='earliest')
    def dispense(self):
        self.consumer.subscribe(['tweets'])
        return self.consumer
    #     for msg in msgs:
    #     print(json.loads(msg).decode('utf-8'))
        # return (json.loads(msg).decode('utf-8'))
        # print(consumer.poll().decode('utf-8'))
        # return self.consumer.poll().decode('utf-8')
    # daemon = True

    # def run(self):
    #     consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
    #                              auto_offset_reset='earliest')
    #     consumer.subscribe(['tweets'])

    #     for message in consumer:
    #         print (message)


# def main():
#     threads = [
#         Producer(),
#         Consumer()
#     ]

#     for t in threads:
#         t.start()

#     time.sleep(10)

# if __name__ == "__main__":
#     logging.basicConfig(
#         format='%(asctime)s.%(msecs)s:%(name)s:%(thread)d:%(levelname)s:%(process)d:%(message)s',
#         level=logging.INFO
#         )
#     main()
# Contact GitHub API Training Shop Blog About
