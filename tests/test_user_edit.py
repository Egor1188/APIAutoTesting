import requests

from endpoints.endpoints import ApiPostLinks, ApiPutLinks, ApiGetLinks
from lib.base_case import BaseCase
from lib.assertions import Assertions
from testdata.proxy import Proxy


class TestUserEdit(BaseCase):
    def test_edit_just_created_user(self):
        # REGISTRATION
        registration_data = self.prepare_registration_data()
        response1 = requests.post(ApiPostLinks.CREATE_USER, proxies=Proxy.PROXY, data=registration_data)

        Assertions.check_status_code(response1, 200)
        Assertions.check_json_has_key(response1, "id")

        email = registration_data["email"]
        first_name = registration_data["firstName"]
        password = registration_data["password"]
        user_id = self.get_json_value(response1, "id")

        # LOGIN
        login_data = {
            "email": email,
            "password": password
        }
        response2 = requests.post(ApiPostLinks.USER_LOGIN, proxies=Proxy.PROXY, data=login_data)
        print(response2.text)
        auth_sid = self.get_cookie(response2, "auth_sid")
        token = self.get_header(response2, "x-csrf-token")
        Assertions.check_status_code(response2, 200)
        Assertions.check_json_has_key(response2, "user_id")

        # EDIT
        new_name = "Changed Name"

        response3 = requests.put(f"{ApiPutLinks.UPDATE_USER}{user_id}",
                                 proxies=Proxy.PROXY,
                                 headers={"x-csrf-token": token},
                                 cookies={"auth_sid": auth_sid},
                                 data={"firstName": new_name})

        Assertions.check_status_code(response3, 200)

        # GET
        response4 = requests.get(
            f"{ApiGetLinks.GET_USER_INFO_BY_ID}{user_id}",
            proxies=Proxy.PROXY,
            headers={"x-csrf-token": token},
            cookies={"auth_sid": auth_sid}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong username after editing"
        )
