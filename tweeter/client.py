import requests


class Client():
    def __init__(self) -> None:
        self.session = requests.session()
        self._cookie_repository
        pass

    def _request_cookies(self):
        response = requests.get(
            "TWITTER_AUTH_URL",
            headers = None,
            proxies = None
        )
        
        return response.cookies

    def _set_cookies(self, cookies):
        self.session.cookies = cookies
        pass
