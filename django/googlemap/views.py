from django.shortcuts import render
from django.http import HttpResponse

import time
import json
import urllib2
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
from .elasticsearch_wrapper import ElasticsearchWrapper
from .tweet_callback import TweetCallback
from kafka import KafkaConsumer, KafkaProducer

es = ElasticsearchWrapper("../setup.cfg")
callback = TweetCallback(es, 5)

def index(request):
    return render(request, 'googlemap/index.html')

def first_fetch(request):
    print ('first_fetch')
    response = es.fetch_latest(200)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')


def update_tweets(request):
    print ('update_tweets')
    response = es.fetch_latest(10)
    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')

def stop_tweets(request):
    print ('stop_tweets')
#    tweet_streamer.stop_stream()# stop the stream
    return HttpResponse()

def search(request):
    print ('search request')
    keyword = request.POST['keyword']
    response = es.search(keyword)

    response = response['hits']['hits']
    response = json.dumps(response)

    return HttpResponse(response, content_type='application/json')

def geosearch(request):
    print ('geosearch request')
    location = request.POST.get('location')
    distance = request.POST.get('distance')
    print ('location: %s, radius: %s' % (location, distance))

    response = es.geosearch(location, distance, 2000)# search at most 2000 tweets
    print ('geosearch response: %s' % response)
    response = json.loads(response)
    response = response['hits']['hits']
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')

@csrf_exempt
def sns_parse(request):
    print("get a notification")
    if request.method=="GET":
        print("get")
        pass
    else:
        headers = json.loads(request.body.decode('utf-8'))
        print("get sns post request")
        if 'Type' in headers.keys():
            if headers['Type']=="SubscriptionConfirmation":
                print("received confirmation request")
                subscribeUrl = headers['SubscribeURL']
                responseData = urllib2.urlopen(subscribeUrl).read()
#                responseData = urllib.request.urlopen(subscribeUrl).read()
                print("subscribed to sns")
            elif headers['Type']=="Notification":

                message = headers['Message']
                message = json.loads(message)

                print("get a notification")

                callback.notify(message)
                print(message['sentiment'])
