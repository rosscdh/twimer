# -*- coding: UTF-8 -*-
"""
"""
import unittest
from django.utils.encoding import smart_unicode
from django.db.models.query import QuerySet

from models import Wasted
from wastingtimer.utils import TWEET_TYPES
from factories import WastedFactory
from wastingtimer.factories import UserFactory


test_user = UserFactory.create()


class WastedModelUnitTest(unittest.TestCase):
    def setUp(self):
        self.subject = WastedFactory.create(user=test_user)
        expected_text = '@wastingtimer 20min 20mins 2:20 #my_category #another_category #1_and_ #and_numbers_1 #a_1 #Krümmer Krümmer'
        self.expected_text = smart_unicode(expected_text)
        self.expected_model_representation = smart_unicode('%s - %s' % (expected_text, self.subject.created_at,))

    def test_model_representation_unicode(self):
        self.assertEqual(unicode(self.subject), self.expected_model_representation)
        self.assertEqual(smart_unicode(self.subject), self.expected_model_representation)

    def test_tweet_text(self):
        self.assertEqual(unicode(self.subject.text), self.expected_text)
        self.assertEqual(smart_unicode(self.subject.text), self.expected_text)

    def test_hashtags(self):
        #note the uppercase hashtags are converted to lower
        expected = [u'my_category', u'another_category', u'1_and_', u'and_numbers_1', u'a_1', u'kr\xfcmmer']
        self.assertEqual(self.subject.hashtags, expected)

    def test_is_private(self):
        # test public messages
        self.subject.tweet_type = TWEET_TYPES.mention
        self.assertEqual(self.subject.is_private, False)

        self.subject.tweet_type = TWEET_TYPES.unknown
        self.assertEqual(self.subject.is_private, False)

        self.subject.tweet_type = TWEET_TYPES.dm
        self.assertEqual(self.subject.is_private, True)

    def test_object_tags_are_correct(self):
        expected = [u'my_category', u'another_category', u'1_and_', u'and_numbers_1', u'a_1', u'kr\xfcmmer']
        result = self.subject.tags.all()
        self.assertTrue(type(result) is QuerySet)
        self.assertTrue(type(list(result)) is list)

        self.assertEqual(result[0].name, 'My category')
        self.assertEqual(result[0].slug, 'my-category')

        last = len(result)
        self.assertEqual(result[last-3].name, u'Kr\xfcmmer')
        # @TODO.. modify django-taggit to handle unicode
        self.assertEqual(result[last-3].slug, u'krummer')

    def test_extract_time(self):
        expected = 140 # minutes
        self.assertEqual(self.subject.extract_time(), expected)


class MentionsServiceUnitTest(unittest.TestCase):
    pass


class DirectMessagesService(unittest.TestCase):
    pass