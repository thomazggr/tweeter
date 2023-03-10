import re
import os
import time

from selenium import webdriver
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException

from tweeter.cookies import Cookies

class Client():
    def __init__(self, 
        username: str, 
        password: str, 
        two_fa_code: str = None,
        load_cookies: bool = False,
        cookies_dir: str = None) -> None:
        self.curr_dir = f"{os.getcwd()}"
        self.username = username
        self.password = password
        self.two_fa_code = two_fa_code
        self.load_cookies = load_cookies
        self.cookies_dir = cookies_dir if cookies_dir[-1] == "/" else f"{cookies_dir}/"
        self.twitter_base_url = "https://twitter.com"
        self.default_status_url = f"{self.twitter_base_url}/{username}/status/"
        self.match_user = re.compile(r"com/([a-zA-Z0-9]{1,200})/status")
        self.login_twitter = "/login"
        self.next_button_xpath = "//div[.//span[text()='Next'] and @role='button']"
        self.input_username_two_fa = "input[name='text']"
        self.input_password = "input[name='password']"
        self.login_button = "//span[contains(text(), 'Log in')]"
        self.two_fa_next_button = "//span[contains(text(), 'Next')]"
        self.default_sleep = 3
        pass

    def authenticate(self) -> None:
        try:
            self.driver = webdriver.Firefox()
            cookies = Cookies(cookies_dir = self.cookies_dir)
        except (WebDriverException or SessionNotCreatedException) as e:
            # Alert with error
            print("DRIVER ERROR!")
            quit()

        if self.load_cookies and self.cookies_dir:
            self.driver = cookies.load(self.username, self.driver)

        wait = WebDriverWait(self.driver, 30)
        self.driver.get(f"{self.twitter_base_url}{self.login_twitter}")
        
        # Username field
        wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, self.input_username_two_fa)
            )
        )
        username_field = self.driver.find_element(
            By.CSS_SELECTOR, self.input_username_two_fa
        )
        time.sleep(self.default_sleep)
        username_field.click()
        username_field.click()
        username_field.send_keys(self.username)

        # Next page to password
        next_button = self.driver.find_element(By.XPATH, self.next_button_xpath)
        next_button.click()

        # Password field
        wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, self.input_password)
            )
        )
        password_field = self.driver.find_element(
            By.CSS_SELECTOR, self.input_password
        )
        password_field.send_keys(self.password)

        # Login button
        wait.until(
            EC.visibility_of_all_elements_located(
                (By.XPATH, self.login_button)
            )
        )
        login_button = self.driver.find_element(
            By.XPATH, self.login_button
        )
        login_button.click()

        # 2FA if needed
        if self.two_fa_code:
            wait.until(
                EC.visibility_of_all_elements_located(
                    (By.CSS_SELECTOR, self.input_username_two_fa)
                )
            )
            two_fa_field = self.driver.find_element(
                By.CSS_SELECTOR, self.input_username_two_fa
            )
            two_fa_field.click()
            two_fa_field.send_keys(self.two_fa_code)

            # Next button two FA
            wait.until(
                EC.visibility_of_all_elements_located(
                    (By.XPATH, self.two_fa_next_button)
                )
            )
            two_fa_next_button = self.driver.find_element(
                By.XPATH, self.two_fa_next_button
            )
            two_fa_next_button.click()
        else:
            #TODO: No 2FA code, 2FA code expired, ask for 2FA later, separate 2FA auth
            pass
        
        cookies.save(self.driver.get_cookies(), self.username)


    def delete_tweet(self, tweet_id: int):
        self.driver.get(f"{self.default_status_url}{tweet_id}")

        time.sleep(self.default_sleep)

        current_url = self.driver.current_url

        tweet_owner = self.match_user.match(current_url).group(1)

        if self.username == tweet_owner:
            pass

        #TODO: Test tweet owner so it can be `Deleted` or `Unretweeted`
        # if self.username == tweet_owner:

