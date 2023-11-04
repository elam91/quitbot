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

    def check_is_pinned(self, tweet):
        try:
            pinned = tweet.find_element(By.XPATH, './/span[text()="Pinned"]')
            return True
        except Exception as error:
            print(error)
            return False

    def check_is_rt(self, tweet):
        try:
            pinned = tweet.find_element(By.XPATH, './/span[contains(.," reposted")]')
            return True
        except Exception as error:
            print(error)
            return False
    def check_is_qt(self, tweet):
        try:
            user_avatars = tweet.find_elements(By.XPATH, './/div[@data-testid="Tweet-User-Avatar"]')
            if len(user_avatars) > 1:
                return True
            else:
                return False
        except Exception as error:
            print(error)
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
        for tweet in tweets:
            if (not self.check_is_rt(tweet)) and (not self.check_is_pinned(tweet)) and (not self.check_is_qt(tweet)):
                selected_tweet = tweet
                break
        if selected_tweet:
            selected_tweet.click()
            return True
        else:
            return False


    def get_or_save_tweet(self, user):
        url = self.browser.current_url.split('/')
        for url_part in url:
            if url_part.isnumeric() and len(url_part) > 5:
                print(url_part,len(url_part))

                tweet = Tweet.get_or_save_tweet(tweet_id=url_part[:20], text='NOT SAVING TEXT RN', user=user)
                return tweet

    def reply_quit(self, user):
        textbox_xpath = '//div[@role="textbox"]'
        self.wait_for_xpath(textbox_xpath)
        input = self.get_by_xpath(textbox_xpath)
        reply_text = "תתפטר"
        if not user.gender == 'M':
            reply_text = reply_text + 'י'
        input.send_keys(reply_text)
        button = self.get_by_xpath('//div[contains(@data-testid,"tweetButton")]')
        self.click_button_humanly(button)
        self.random_wait()
        return True