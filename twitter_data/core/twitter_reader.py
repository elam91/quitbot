from selenium.common import TimeoutException
from selenium.webdriver.common.by import By
from selenium.webdriver.support.wait import WebDriverWait

from twitter_data.core.base import BaseLinkedinBot
from selenium.webdriver.support import expected_conditions as EC

from twitter_data.models import Tweet


class TwitterReaderBot(BaseLinkedinBot):
    def __init__(self, start_page=0):
        super().__init__()
        self.old_names = []
        self.current_page = start_page

    def go_to_twitter(self):
        self.browser = self.create_browser(headless=False)
        self.user = "quit"
        self.browser.get('https://twitter.com')
        self.random_wait(3, 5)
        self.load_cookie()
        self.browser.refresh()
        self.random_wait(2, 4)

    def go_to_user(self, username):
        self.browser.get(f'https://twitter.com/{username}')
        self.wait_for_xpath('//span[text()="Posts"]')

    def check_is_pinned(self, tweet):
        try:
            pinned = tweet.find_element(By.XPATH, './/span[text()="Pinned"]')
            self.log('Pinned tweet, skip')
            return True
        except Exception as error:
            self.log('Not pinned tweet')
            return False

    def check_is_rt(self, tweet):
        try:
            pinned = tweet.find_element(By.XPATH, './/span[contains(.," reposted")]')
            self.log('retweet, skip')
            return True
        except Exception as error:
            self.log('Not retweet')
            return False
    def check_is_qt(self, tweet):
        try:
            user_avatars = tweet.find_elements(By.XPATH, './/div[@data-testid="Tweet-User-Avatar"]')
            if len(user_avatars) > 1:
                self.log('Quote tweet, skip')
                return True
            else:
                self.log('Not quote tweet')
                return False
        except Exception as error:
            return False

    def get_by_xpath(self,xpath, multi=False):
        if multi:
            return self.browser.find_elements(By.XPATH, xpath)
        else:
            return self.browser.find_element(By.XPATH,xpath)

    def wait_for_xpath(self, xpath):
        element_present = EC.presence_of_element_located((By.XPATH, xpath))
        element = WebDriverWait(self.browser, 5).until(element_present)

    def go_to_last_tweet(self):
        xpath_article= '//article[@data-testid="tweet"]'
        selected_tweet = None
        self.wait_for_xpath(xpath_article)
        tweets = self.get_by_xpath(xpath_article, multi=True)
        print(len(tweets))
        for tweet in tweets[:5]:
            if (not self.check_is_rt(tweet)) and (not self.check_is_pinned(tweet)) and (not self.check_is_qt(tweet)):
                selected_tweet = tweet
                break
        if selected_tweet:
            selected_tweet_text = selected_tweet.find_element(By.XPATH,".//div[@data-testid='tweetText']")
            self.log("Selected a tweet")
            selected_tweet_text.click()
            self.random_wait()
            return True
        else:
            return False


    def get_or_save_tweet(self, user):
        url = self.browser.current_url.split('/')
        for url_part in url:
            if url_part.isnumeric() and len(url_part) > 5:
                self.log(f"tweet_id: {url_part} length of id:{len(url_part)}")

                tweet, created = Tweet.objects.get_or_create(tweet_id=url_part, user=user)
                return tweet

    def reply_quit(self, user):
        textbox_xpath = '//div[@role="textbox"]'
        try:
            self.wait_for_xpath(textbox_xpath)
        except TimeoutException:
            return False

        try:
            input = self.get_by_xpath(textbox_xpath)
        except TimeoutException:
            return False
        reply_text = "תתפטר"
        if not user.gender == 'M':
            reply_text = reply_text + 'י'
        input.send_keys(reply_text)
        try:
            button = self.get_by_xpath('//div[contains(@data-testid,"tweetButton")]')
            self.click_button_humanly(button)
        except TimeoutException:
            return False
        self.random_wait()
        return True