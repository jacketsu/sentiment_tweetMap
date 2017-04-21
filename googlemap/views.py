from django.shortcuts import render
from django.http import HttpResponse

from . import tweet_streamer

import time
import json
import urllib
from django.views.decorators.csrf import csrf_exempt
from django.conf import settings
# import pdb; pdb.set_trace()
from .elasticsearch_wrapper import ElasticsearchWrapper
from .tweet_callback import TweetCallback
from .tweet_stream_thread import TweetStreamThread
from kafka import KafkaConsumer, KafkaProducer
from .tweet_observer import TweetObserver

observer = TweetObserver()
es = ElasticsearchWrapper()

stream_thread = TweetStreamThread(TweetCallback(es, 5))
stream_thread.start_thread()

# consumer = KafkaConsumer(bootstrap_servers='localhost:9092',
#                          auto_offset_reset='earliest')
# consumer = KafkaConsumer(value_deserializer=lambda m: json.loads(m.decode('ascii')))
# consumer.subscribe(['tweets'])

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
    # consumer.subscribe(['tweets'])
    # print(response)
    # print(consumer.poll(20))
    # consumer.subscribe(['tweets'])
    # # res = consumer.poll(20)
    # for msg in consumer:
    #     # consumer.commit()
    #     print(msg.value)
    # for msg in consumer:
    #     # amsg = json.loads(msg)
    #     print(msg)
    #     response = msg['hits']['hits']
    #     response 
    # # # for i in range(20):
    # # # if consumer.dispense() is None:
    # # #     continue
    # msgs = consumer.dispense()
    # for msg in msgs:
    #     amsg = json.loads(msg.value).decode('utf-8')
    #     print(amsg)
    # print("hi")
    # # print(res.value())
    # print("guys")
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
    response = response['hits']['hits']
    response = json.dumps(response)
    return HttpResponse(response, content_type='application/json')

@csrf_exempt
def sns_parse(request):
    print("get a notification")
    if request.method=="GET":
        print("get")
        pass
        # context = {"title":"Home"}
        # return render(request, "index.html", context)
    else:
        headers = json.loads(request.body.decode('utf-8'))
        print("get sns post request")
        if 'Type' in headers.keys():
            if headers['Type']=="SubscriptionConfirmation":
                print("received confirmation request")
                subscribeUrl = headers['SubscribeURL']
                responseData = urllib.request.urlopen(subscribeUrl).read()
                print("subscribed to sns")
            elif headers['Type']=="Notification":
                # print ("received a new message: "+str(headers['Message']))
                message = json.loads(headers['Message']).get('default')
                message = json.loads(message)
                # message = json.loads(json.loads(headers['Message']).get('default'))
                print("get a notification")
                # message = json.loads(headers['Message'])['default']
                # print(message)
                # msg = json.loads(message)
                # observer.flush_tweet(message)
                print(message['sentiment'])
                # print ("Message :"+str(message))
                # observer.flush_tweet(message)
    # return render(request, 'googlemap/index.html')
    # return render(request, 'googlemap/index.html', {'post_params': str(request.POST)})

        #         id = message.get('id')
        #         tweet = message.get('tweet')
        #         lat = message.get("lat")
        #         lng = message.get("lng")
        #         sentiment = message.get("sentiment")
        #         index_name = getattr(settings, "INDEX_NAME", None)
        #         host = getattr(settings, "HOST_NAME", None)
        #         add_object_to_index(index_name, id, tweet, lat, lng, sentiment, host)
        #         new_tweet = NewTweets(id=id, tweet=tweet, lat=lat, lng=lng, sentiment=sentiment)
        #         new_tweet.save()
        # return render(request, "data.html", {"post_params": str(request.POST)})
