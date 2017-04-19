import json
from watson_developer_cloud import NaturalLanguageUnderstandingV1
import watson_developer_cloud.natural_language_understanding.features.v1 as \
    features


natural_language_understanding = NaturalLanguageUnderstandingV1(
    version='2017-02-27',
    username='82e07fd0-a7ec-41b6-978c-b33ebb5d2826',
    password='4KvREkMTNRbu')

response = natural_language_understanding.analyze(
    text='Bruce Banner is the Hulk and Bruce Wayne is BATMAN! '
         'Superman fears not Banner, but Wayne.',
    # features=[features.Entities(), features.Keywords()])
    features=[features.Sentiment()])

print(json.dumps(response['sentiment']['document']['label'], indent=2))
print(response)