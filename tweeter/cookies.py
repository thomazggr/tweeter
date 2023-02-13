import pickle

from selenium import webdriver as swd


class Cookies():
    """
    """
    
    def __init__(self, cookies_dir) -> None:
        self.cookies_dir = cookies_dir
        pass

    def __get_cookies_filepath(self, username):
        return f"{self.cookies_dir}{username}-tweeter-pylib.pkl"

    def save(self, cookies, username):
        try:
            cookies_path = self.__get_cookies_filepath(username)

            with open(cookies_path, "wb") as f:
                pickle.dump(cookies, f)
        except:
            #TODO: set excepetions
            print("COOKIES SAVING ERROR!")
            quit()
    
    def load(self, username, driver: swd):
        try:
            cookies_path = self.__get_cookies_filepath(username)
            
            with open(cookies_path, "rb") as f:
                cookies_loader = pickle.load(f)

            for cookie in cookies_loader:
                driver.add_cookie(cookie)
        except:
            #TODO: set excepetions
            print("COOKIES LOADING ERROR!")
            quit()
        
        return driver