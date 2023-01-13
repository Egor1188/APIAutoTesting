import pytest
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from testdata.userdata import UserData
from endpoints.endpoints import ApiPostLinks, ApiGetLinks

from lib.assertions import Assertions


class TestUserAuth(BaseCase):
    exclude_params = {
        'no_cookie',
        'no_token'
    }

    def setup(self):
        data = UserData.TEST_USER1
        response1 = MyRequests.post(ApiPostLinks.USER_LOGIN, data=data)

        self.auth_sid = self.get_cookie(response1, "auth_sid")
        self.token = self.get_header(response1, "x-csrf-token")
        self.user_id_from_auth = self.get_json_value(response1, "user_id")

    def test_user_auth(self):
        response2 = MyRequests.get(
            ApiGetLinks.GET_AUTHORIZED_USER_ID,
            headers={"x-csrf-token": self.token},
            cookies={'auth_sid': self.auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            self.user_id_from_auth,
            "User ids are not equal"
        )

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth(self, condition):
        if condition == 'no_cookie':
            response2 = MyRequests.get(ApiGetLinks.GET_AUTHORIZED_USER_ID,
                                       headers={"x-csrf-token": self.token}
                                       )
        else:
            response2 = MyRequests.get(ApiGetLinks.GET_AUTHORIZED_USER_ID,
                                       cookies={'auth_sid': self.auth_sid}
                                       )

        Assertions.assert_json_value_by_name(
            response2,
            "user_id",
            0,
            f"User is authorized with condition {condition}"
        )
