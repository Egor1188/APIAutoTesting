import requests

from lib.base_case import BaseCase


class UserAuth(BaseCase):
    def is_the_response_correct(self):
        assert 'auth_sid' in self.logged_user.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in self.logged_user.headers, "There is no CSRF token header in the response"
        assert "user_id" in self.logged_user.json(), "There is no user id in the response"

    def is_user_authorized(self):

        response2 = self.get_authorised_user_id()
        assert "user_id" in response2.json(), "There is no user id in the response"
        user_id_from_check = response2.json()["user_id"]
        assert user_id_from_check == self.user_id, 'User ids are different'

    def cant_authorize_without_cookie_or_csrf(self, condition):
        if condition == 'no_cookie':
            response2 = requests.get(self.url_check_auth, proxies=self.proxy, headers=self.headers)
        else:
            response2 = requests.get(self.url_check_auth, proxies=self.proxy, cookies=self.cookie)

        assert "user_id" in response2.json(), "There is no user id in the response"

        user_id_from_check = response2.json()["user_id"]
        assert user_id_from_check == 0, f'User is authorized with condition {condition}'
