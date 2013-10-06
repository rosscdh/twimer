# -*- coding: UTF-8 -*-
from django.contrib.auth import get_user_model
from django_rq import job

from models import Wasted
from wastingtimer.utils import TWEET_TYPES

from social_auth.db.django_models import UserSocialAuth

User = get_user_model()
import pdb

@job
def process_twitter_tweet(**kwargs):
    tweet = kwargs.get('tweet', None)
    type_of_tweet = kwargs.get('type_of_tweet', TWEET_TYPES.unknown)

    try:
    	# public Mention
    	twitter_user = tweet.user
    except:
    	# Private DM
    	twitter_user = tweet.sender

    user,is_new = ensure_user_present(twitter_user=twitter_user, tweet=tweet)
    ensure_tweet_present(user=user, tweet=tweet, type_of_tweet=type_of_tweet)


def ensure_user_present(**kwargs):

	twitter_user = kwargs.get('twitter_user', None)

	tweet = kwargs.get('tweet', None)
	if twitter_user is not None:
		user, is_new = User.objects.get_or_create(username=twitter_user.screen_name)

		if user.email == '':
			User.objects.filter(pk=user.pk).update(email='%s@twitter.com' % tweet.user.id)
			profile = user.get_profile()
			profile.twitter_image = twitter_user.profile_image_url
			profile.twitter_data = twitter_user.__getstate__()
			profile.save()

		# Add the twitter auth model
		ensure_twitter_socialauth_present(user=user, tweet=tweet)

		# Follow the twitter user
		if is_new:
			follow_twitter_user(twitter_user=twitter_user)

		return user, is_new
	return False, False


def follow_twitter_user(**kwargs):
	from wastingtimer.wasted.services import FollowerSyncService # import here to avoid crcular dependency
	twitter_user = kwargs.get('twitter_user', None)
	if twitter_user is not None:
		follower_service = FollowerSyncService(follower=twitter_user)
		follower_service.process()

def ensure_twitter_socialauth_present(**kwargs):
	user = kwargs.get('user', None)
	tweet = kwargs.get('tweet', None)
	# get twitter id
	try:
		uid = tweet.user.id
	except:
		uid = None
	if user is not None and uid is not None:
		auth, is_new = UserSocialAuth.objects.get_or_create(user=user, provider='twitter', uid=uid)
		return auth, is_new
	return False, False


def ensure_tweet_present(**kwargs):
	user = kwargs.get('user', None)
	tweet = kwargs.get('tweet', None)
	type_of_tweet = kwargs.get('type_of_tweet', TWEET_TYPES.unknown)

	if tweet is not None:
		tweet = tweet.__getstate__() # makea json object from the tweepy object

		# remove unjsonable
		try:
			tweet.pop('user')
		except KeyError:
			pass
		try:
			tweet.pop('sender')
		except KeyError:
			pass
		try:
			tweet.pop('author')
		except KeyError:
			pass
		try:
			tweet.pop('place')
		except KeyError:
			pass
		try:
			tweet.pop('recipient')
		except KeyError:
			pass
			
		created_at = tweet.get('created_at')

		if tweet is not None:
			try:
				wasted = Wasted.objects.get(twitter_id=tweet.get('id'))
				is_new = False
			except Wasted.DoesNotExist:
				wasted, is_new = Wasted.objects.get_or_create(user=user, twitter_id=tweet.get('id'), tweet_type=type_of_tweet, created_at=created_at)
				wasted.tweet_data = tweet
				wasted.save()

			return wasted, is_new
	return False, False
