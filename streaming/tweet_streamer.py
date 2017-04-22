#!/usr/bin/env python
from __future__ import print_function
import time
import tweepy
import json

from getpass import getpass
from datetime import datetime
from six.moves import configparser
from kafka import KafkaConsumer, KafkaProducer

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
#                print ("sending tweets to kafka")
                producer.send('tweets', json.dumps(tweet).encode('utf-8'))
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


def start_stream():
    consumer_key, consumer_secret, access_token, access_token_secret = read_config('../setup.cfg')

    auth = tweepy.auth.OAuthHandler(consumer_key, consumer_secret)
    auth.set_access_token(access_token, access_token_secret)

    global stream
    stream = tweepy.Stream(auth, TweetStreamListener(), timeout=None)
    stream.filter(locations=[-180, -90, 180, 90], languages=['en'])

def stop_stream():
    print ('stopping stream...')
 #   observer.save_tweets()
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

start_stream()
