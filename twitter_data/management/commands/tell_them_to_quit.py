import tweepy

from twitter_data.core.base import BaseLinkedinBot
from twitter_data.core.twitter_reader import TwitterReaderBot
from twitter_data.models import TwitterUser
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError
from django.conf import settings

# quit bot bearer token
bearer = 'AAAAAAAAAAAAAAAAAAAAAJIhqwEAAAAAOwvmC4uwUG0sECnbQ4jSLqG48v0%3DesPeXP0CsNtCgbzpnKYeJPiZnGy8fqnM9enwxRH2LZ88n2wUMW'

# api token
api_token = 'u8Vf4fLJimdUIbOZivUw1ctgh'

# api secret
api_secret = 'lrhh2f3H8DnKKgAfDLgXL1vBCMGoeniRoCdAWMsVu6y2n3RUwn'
# user token
user_token = '1719194526441455616-zsFzuEl4BthbkcDEdR3RUKZRQtEtRp'

# user secret
user_secret = 'Jduu3MKLIIIbuVvze2kfZCzlfZTVI6bWMlmwrIzbItQ6H'




class Command(BaseCommand):
    help = 'Start the stream of the bot telling everyone to quit'

    def handle(self, *args, **options):
        bot = TwitterReaderBot()
        self.stdout.write("getting users")
        users = TwitterUser.objects.all()

        bot.go_to_twitter()
        for user in users:
            try:
                bot.go_to_user(user.user_profile)
                tweet_page = bot.go_to_last_tweet()
                if tweet_page:
                    tweet = bot.get_or_save_tweet(user=user)
                    if not tweet or tweet.replied:
                        continue
                    else:
                        res = bot.reply_quit(user)
                        if res:
                            tweet.replied = True
                            tweet.save()
            except Exception as error:
                bot.log(error)
                continue




