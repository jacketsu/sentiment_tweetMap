#!/usr/bin/env python

import time
import tweepy
import json

from getpass import getpass
from datetime import datetime
from six.moves import configparser
from .tweet_observer import TweetObserver
from kafka import KafkaConsumer, KafkaProducer
import threading

observer = TweetObserver()
TIMEZONE_OFFSET = datetime.utcnow() - datetime.now()
producer = KafkaProducer(bootstrap_servers='localhost:9092', api_version=(0,10))

class TweetStreamListener(tweepy.StreamListener):

    def on_status(self, status):
        try:
            coords = status.coordinates["coordinates"]
            if coords is not None:
                local_created_time = status.created_at - TIMEZONE_OFFSET;
                tweet = {
                    'name': status.author.screen_name,
                    'time': local_created_time.strftime("%Y/%m/%d %H:%M:%S"),
                    'location': {'lat': coords[1], 'lon': coords[0]},
                    'text': status.text,
                    'profile_image_url': status.author.profile_image_url,
                    'sentiment': ''
                }
                # observer.flush_tweet(tweet)
                # print(tweet)
                print("hello")
                producer.send('tweets', json.dumps(tweet).encode('utf-8'))
                # print(tweet)

                return True

        except:
            # Catch any unicode errors while printing to console
            # and just ignore them to avoid breaking application.
            pass

    def on_error(self, status_code):
        print ('An error has occured! Status code = %s' % status_code)
        return True  # keep stream alive

    def on_timeout(self):
        print ('Snoozing Zzzzzz')


def register_callback(callback):
    observer.register_callback(callback)

def start_stream():
    consumer_key, consumer_secret, access_token, access_token_secret = read_config('setup.cfg')

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    global stream
    stream = tweepy.Stream(auth, TweetStreamListener(), timeout=None)
    stream.filter(locations=[-180, -90, 180, 90], languages=['en'])

def stop_stream():
    print ('stopping stream...')
    observer.save_tweets()
    global stream
    stream.disconnect()

def read_config(config_file):
    config = configparser.ConfigParser()
    config.read(config_file)

    consumer_key = config.get('TweetStreaming', 'consumer_key')
    consumer_secret = config.get('TweetStreaming', 'consumer_secret')
    access_token = config.get('TweetStreaming', 'access_token')
    access_token_secret = config.get('TweetStreaming', 'access_token_secret')

    return (consumer_key, consumer_secret, access_token, access_token_secret)

def listen_sns():
    print("listenning")
    consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
                                                 auto_offset_reset='largest')
    consumer.subscribe(['sns'])
    print("listenning")
    while True:
        for message in consumer:
            print(message)
            message = json.loads(message.value.decode())
            observer.flush_tweet(message)


