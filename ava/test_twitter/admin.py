from django.contrib import admin

from ava.test_twitter.models import *

admin.site.register(TwitterTest)
admin.site.register(TwitterAccount)
admin.site.register(TweetTemplate)
admin.site.register(TweetLink)