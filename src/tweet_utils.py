#!/usr/bin/python
# -*- coding: utf-8 -*-
'''
Original code contributor: mentzera
Article link: https://aws.amazon.com/blogs/big-data/building-a-near-real-time-discovery-platform-with-aws/

'''
import re
from textblob import TextBlob


class Sentiments:
    POSITIVE = 'Positive'
    NEGATIVE = 'Negative'
    NEUTRAL = 'Neutral'
    CONFUSED = 'Confused'


id_field = 'id_str'
emoticons = {Sentiments.POSITIVE: '😀|😁|😂|😃|😄|😅|😆|😇|😈|😉|😊|😋|😌|😍|😎|😏|😗|😘|😙|😚|😛|😜|😝|😸|😹|😺|😻|😼|😽',
             Sentiments.NEGATIVE: '😒|😓|😔|😖|😞|😟|😠|😡|😢|😣|😤|😥|😦|😧|😨|😩|😪|😫|😬|😭|😾|😿|😰|😱|🙀',
             Sentiments.NEUTRAL: '😐|😑|😳|😮|😯|😶|😴|😵|😲',
             Sentiments.CONFUSED: '😕'
             }

tweet_mapping = {
    'mappings': {
        'properties':
            {'timestamp_ms': {
                'type': 'date'
            },
                'text': {
                    'type': 'string'
                },
                'coordinates': {
                    'properties': {
                        'coordinates': {
                            'type': 'geo_point'
                        },
                        'type': {
                            'type': 'string',
                            'index': 'not_analyzed'
                        }
                    }
                },
                'user': {
                    'properties': {
                        'id': {
                            'type': 'long'
                        },
                        'name': {
                            'type': 'string'
                        }
                    }
                },
                'sentiments': {
                    'type': 'string',
                    'index' : 'not_analyzed'
                }
            }
    }
}


# https://www.elastic.co/blog/strings-are-dead-long-live-strings
tweet_mapping_v5 = {
    'properties':
        {'timestamp_ms': {
            'type': 'date'
        },
            'text': {
                'type': 'text'
            },
            'coordinates': {
                'properties': {
                    'coordinates': {
                        'type': 'geo_point'
                    },
                    'type': {
                        'type': 'keyword'
                    }
                }
            },
            'user': {
                'properties': {
                    'id': {
                        'type': 'long'
                    },
                    'name': {
                        'type': 'text'
                    }
                }
            },
            'sentiments': {
                'type': 'keyword'
            },
            'place': {
                'type': 'text'
            }
        }
}


def _sentiment_analysis(tweet):
    tweet['emoticons'] = []
    tweet['sentiments'] = []
    _sentiment_analysis_by_emoticons(tweet)
    if len(tweet['sentiments']) == 0:
        _sentiment_analysis_by_text(tweet)


def _sentiment_analysis_by_emoticons(tweet):
    for sentiment, emoticons_icons in emoticons.items():
        matched_emoticons = re.findall(emoticons_icons, tweet['text'])
        if len(matched_emoticons) > 0:
            tweet['emoticons'].extend(matched_emoticons)
            tweet['sentiments'].append(sentiment)

    if Sentiments.POSITIVE in tweet['sentiments'] and Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.CONFUSED
    elif Sentiments.POSITIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.POSITIVE
    elif Sentiments.NEGATIVE in tweet['sentiments']:
        tweet['sentiments'] = Sentiments.NEGATIVE

def _sentiment_analysis_by_text(tweet):
    blob = TextBlob(tweet['text'])
    sentiment_polarity = blob.sentiment.polarity
    if sentiment_polarity < 0:
        sentiment = Sentiments.NEGATIVE
    elif sentiment_polarity <= 0.2:
        sentiment = Sentiments.NEUTRAL
    else:
        sentiment = Sentiments.POSITIVE
    tweet['sentiments'] = sentiment


def get_tweet(doc):
    tweet = {}
    print(doc)
    tweet[id_field] = doc['data'][id_field]
    # tweet['hashtags'] = map(lambda x: x['text'],doc['entities']['hashtags'])
    tweet['hashtags'] = [x['tag'] for x in doc['data']['entities']['hashtags']]
    tweet['coordinates'] = doc['includes']['places'][0]['geo']['bbox']
    tweet['created_at'] = doc['data']['created_at']
    tweet['text'] = doc['data']['text']
    tweet['user'] = {'id': doc['includes']['users'][0]['id'], 'name': doc['includes']['users'][0]['name']}
    tweet['mentions'] = re.findall(r'@\w*', doc['data']['text'])
    tweet['place'] = doc['includes']['places'][0]['full_name']
    # _sentiment_analysis(tweet)
    return tweet


def get_tweet_mapping(es_version_number_str):
    major_number = int(es_version_number_str.split('.')[0])
    if major_number >= 5:
        return tweet_mapping_v5
    return tweet_mapping_v5


