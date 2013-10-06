from django import forms
from django.utils.translation import ugettext as _

from parsley.decorators import parsleyfy
from models import Wasted


@parsleyfy
class UserWastedForm(forms.Form):
    tweet = forms.CharField(label=_('Tweet'), help_text='', required=True, min_length=20, max_length=140, widget=forms.Textarea(attrs={'class':'xxlarge'}))

    def __init__(self, **kwargs):
        self.request = kwargs.pop('request', None)
        self.object = kwargs.pop('object', None)
        super(UserWastedForm, self).__init__(**kwargs)

    def save(self):
        if self.object:
            tweet = self.cleaned_data.get('tweet')
            tags = self.object.extract_hashtags(text=tweet)
            # set the main text object and not the tweet.data
            self.object.tweet = tweet
            self.object.save()
            # handle tags
            self.object.tags.all().delete()
            self.object.tags.add(*tags)

        return self.object
        