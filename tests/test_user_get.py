import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from endpoints.endpoints import ApiGetLinks, ApiPostLinks
from lib.my_requests import MyRequests
from testdata.userdata import UserData


@pytest.mark.skip()
class TestUserGet(BaseCase):
    def test_get_user_details_not_auth(self):
        """Test checks possibility of receiving user data with id by another user"""
        user_id = 2
        response = MyRequests.get(f"{ApiGetLinks.GET_USER_INFO_BY_ID}{user_id}")
        Assertions.check_json_has_key(response, "username")
        Assertions.check_json_has_no_key(response, "email")
        Assertions.check_json_has_no_key(response, "firstName")
        Assertions.check_json_has_no_key(response, "lastName")

    def test_get_user_details_auth_as_same_user(self):
        """Test checks possibility of receiving user data by id by same authorized user"""
        data = UserData.TEST_USER1

        response1 = MyRequests.post(ApiPostLinks.USER_LOGIN, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id")

        response2 = MyRequests.get(f"{ApiGetLinks.GET_USER_INFO_BY_ID}{user_id_from_auth}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )

        Assertions.check_json_has_keys(response2, UserData.USER_KEYS)

    def test_get_user_details_auth_as_another_user(self):
        """Test checks possibility of receiving user data by id
        by another authorized user"""
        data = UserData.TEST_USER1

        response1 = MyRequests.post(ApiPostLinks.USER_LOGIN, data=data)
        auth_sid = self.get_cookie(response1, "auth_sid")
        token = self.get_header(response1, "x-csrf-token")
        user_id_from_auth = self.get_json_value(response1, "user_id") - 1

        response2 = MyRequests.get(f"{ApiGetLinks.GET_USER_INFO_BY_ID}{user_id_from_auth}",
                                   headers={'x-csrf-token': token},
                                   cookies={'auth_sid': auth_sid}
                                   )
        names = ["email", "firstName", "lastName"]
        Assertions.check_json_has_key(response2, "username")
        Assertions.check_json_has_no_keys(response2, names)
