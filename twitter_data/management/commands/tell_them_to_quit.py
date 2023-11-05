import tweepy

from twitter_data.core.base import BaseLinkedinBot
from twitter_data.core.twitter_reader import TwitterReaderBot
from twitter_data.models import TwitterUser
from django.contrib.auth import get_user_model
from django.core.management import BaseCommand, CommandError
from django.conf import settings





class Command(BaseCommand):
    help = 'Start the stream of the bot telling everyone to quit'

    def handle(self, *args, **options):
        bot = TwitterReaderBot()
        self.stdout.write("getting users")
        bot.log("Starting")
        users = TwitterUser.objects.order_by('user_profile').all()

        bot.go_to_twitter()
        for index,user in enumerate(users):
            bot.log(f"Going to user no{index+1} {user.user_profile}")
            bot.go_to_user(user.user_profile)
            bot.random_wait()
            tweet_page = bot.go_to_last_tweet()
            if tweet_page:
                tweet = bot.get_or_save_tweet(user=user)
                if not tweet or tweet.replied:
                    if not tweet:
                        bot.log("No tweet found")
                    elif tweet.replied:
                        bot.log("Latest tweet already replied to")
                    continue
                else:
                    bot.log(f"Found a new tweet, replying")
                    res = bot.reply_quit(user)
                    if res:
                        tweet.replied = True
                        tweet.save()
                    bot.log("Done replying")
                    bot.random_wait()
        bot.log('All users done')
        self.stdout.write("task finished")




