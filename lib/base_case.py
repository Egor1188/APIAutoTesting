import requests
from endpoints.endpoints import ApiPostLinks, ApiGetLinks


class BaseCase:
    def __init__(self):
        self.data = {
            'email': 'vinkotov@example.com',
            'password': '1234'
        }
        self.proxy = {
            'https': '89.38.96.219:3128'
        }
        self.url_check_auth = "https://playground.learnqa.ru/api/user/auth"
        self.logged_user = self.log_user_into_the_system()

        self.auth_sid = self.logged_user.cookies.get("auth_sid")
        self.token = self.logged_user.headers.get("x-csrf-token")
        self.user_id = self.logged_user.json()["user_id"]

        self.headers = {
            "x-csrf-token": self.token
        }
        self.cookie = {
            'auth_sid': self.auth_sid
        }

    def log_user_into_the_system(self):
        return requests.post(url=ApiPostLinks.USER_LOGIN, proxies=self.proxy, data=self.data)

    def get_authorised_user_id(self):
        return requests.get(url=ApiGetLinks.GET_AUTHORIZED_USER_ID,
                            proxies=self.proxy, headers=self.headers, cookies=self.cookie)
