import time

from selenium.webdriver import Firefox
from selenium.webdriver.common.by import By
from selenium.webdriver.support.ui import WebDriverWait
from selenium.webdriver.support import expected_conditions as EC
from selenium.common.exceptions import WebDriverException, SessionNotCreatedException


class Client():
    def __init__(self, username: str, password: str) -> None:
        self.username = username
        self.password = password
        self.twitter_base_url = "https://twitter.com"
        self.login_twitter = "/login"
        self.next_button_xpath = "//div[.//span[text()='Next'] and @role='button']"
        self.input_username = "input[name='text']"
        self.input_password = "input[name='password']"
        self.default_sleep = 3
        pass

    def authenticate(self):
        try:
            driver = Firefox()
        except (WebDriverException or SessionNotCreatedException):
            # Alert with error
            quit()

        wait = WebDriverWait(driver, 30)
        driver.get(f"{self.twitter_base_url}{self.login_twitter}")
        
        wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, self.input_username)
            )
        )

        username_field = driver.find_element(
            By.CSS_SELECTOR, self.input_username
        )

        time.sleep(self.default_sleep)

        username_field.send_keys(self.username)

        next_button = driver.find_element(By.XPATH, self.next_button_xpath)
        next_button.click()

        wait.until(
            EC.visibility_of_all_elements_located(
                (By.CSS_SELECTOR, self.input_password)
            )
        )

        password_field = driver.find_element(
            By.CSS_SELECTOR, self.input_password
        )

        time.sleep(self.default_sleep)

        password_field.send_keys(self.password)