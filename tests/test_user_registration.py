import requests
from lib.base_case import BaseCase
from lib.assertions import Assertions
from testdata.userdata import UserData
from endpoints.endpoints import ApiPostLinks
from testdata.proxy import Proxy


class TestUserRegistration(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = requests.post(ApiPostLinks.CREATE_USER, data=data, proxies=Proxy.PROXY)
        Assertions.check_status_code(response, 200)
        Assertions.check_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        data = UserData.USER_WITH_EXISTING_EMAIL
        response = requests.post(ApiPostLinks.CREATE_USER, data=data, proxies=Proxy.PROXY)

        print(response.status_code)
        print(response.content)

        Assertions.check_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{data['email']}' already exists", \
            f"Unexpected response content {response.content}"