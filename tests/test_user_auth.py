import pytest
import requests

from lib.base_case import BaseCase
from tests.user_auth_tests import UserAuth
from testdata.userdata import UserData
from endpoints.endpoints import ApiPostLinks, ApiGetLinks
from testdata.proxy import Proxy


class TestUserAuth(BaseCase):
    exclude_params = {
        'no_cookie',
        'no_token'
    }

    def setup(self):
        data = UserData.TEST_USER1
        response1 = requests.post(ApiPostLinks.USER_LOGIN, proxies=Proxy.PROXY, data=data)
        assert 'auth_sid' in response1.cookies, "There is no auth cookie in the response"
        assert "x-csrf-token" in response1.headers, "There is no CSRF token header in the response"
        assert 'user_id' in response1.json(), "There is no user id in the response"
        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth = response1.json()["user_id"]

    def test_user_auth(self):
        response2 = requests.get(
            ApiGetLinks.GET_AUTHORIZED_USER_ID,
            proxies=Proxy.PROXY,
            headers={"x-csrf-token": self.token},
            cookies={'auth_sid': self.auth_sid}
        )

        assert 'user_id' in response2.json(), "There is no user id in the second response"
        user_id_from_check = response2.json()["user_id"]
        assert self.user_id_from_auth == user_id_from_check, "User ids are not equal"

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth(self, condition):
        if condition == 'no_cookie':
            response2 = requests.get(ApiGetLinks.GET_AUTHORIZED_USER_ID,
                                     proxies=Proxy.PROXY,
                                     headers={"x-csrf-token": self.token}
            )
        else:
            response2 = requests.get(ApiGetLinks.GET_AUTHORIZED_USER_ID,
                                     proxies=Proxy.PROXY,
                                     cookies={'auth_sid': self.auth_sid}
            )

        assert "user_id" in response2.json(), "There is no user id in the second response"

        user_id_from_check = response2.json()["user_id"]
        assert user_id_from_check == 0, f'User is authorized with condition {condition}'


