# -*- coding: UTF-8 -*-
import factory
from wastingtimer.utils import TWEET_TYPES
from models import Wasted

import datetime


class WastedFactory(factory.Factory):
    FACTORY_FOR = Wasted

    twitter_id = 12345
    tweet_type = TWEET_TYPES.mention
    created_at = datetime.datetime.utcnow()
    tweet_data = {
          "lang": "en", 
          "favorited": False, 
          "entities": {
            "user_mentions": [
              {
                "indices": [
                  0, 
                  8
                ], 
                "screen_name": "wastingtimer", 
                "id": 12345, 
                "name": "Wasting Timer Manager", 
                "id_str": "12345"
              }
            ], 
            "hashtags": [{'text': u'my_category'}, {'text': u'another_category'}, {'text': u'1_and_'}, {'text': u'and_numbers_1'}, {'text': u'a_1'}, {'text': u'Krümmer'}], 
            "urls": []
          }, 
          "contributors": None, 
          "truncated": False, 
          "text": "@wastingtimer 20min 20mins 2:20 #my_category #another_category #1_and_ #and_numbers_1 #a_1 #Krümmer Krümmer", 
          "created_at": "2013-03-14T16:50:55", 
          "retweeted": False, 
          "in_reply_to_status_id_str": None, 
          "coordinates": None, 
          "source_url": "", 
          "source": "", 
          "in_reply_to_status_id": None, 
          "in_reply_to_screen_name": None, 
          "id_str": "312244460371197953", 
          "in_reply_to_user_id_str": "14083026", 
          "retweet_count": 0, 
          "geo": None, 
          "id": 312244460371197953, 
          "favorite_count": 0, 
          "in_reply_to_user_id": 14083026
        }