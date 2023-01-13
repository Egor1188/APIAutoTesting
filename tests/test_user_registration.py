from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from testdata.userdata import UserData
from endpoints.endpoints import ApiPostLinks


class TestUserRegistration(BaseCase):

    def test_create_user_successfully(self):
        data = self.prepare_registration_data()

        response = MyRequests.post(ApiPostLinks.CREATE_USER, data=data)
        Assertions.check_status_code(response, 200)
        Assertions.check_json_has_key(response, "id")

    def test_create_user_with_existing_email(self):
        data = UserData.USER_WITH_EXISTING_EMAIL
        response = MyRequests.post(ApiPostLinks.CREATE_USER, data=data)

        print(response.status_code)
        print(response.content)

        Assertions.check_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{data['email']}' already exists", \
            f"Unexpected response content {response.content}"
