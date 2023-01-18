import pytest

from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from testdata.userdata import UserData, InvalidUserData
from endpoints.endpoints import ApiPostLinks


@pytest.mark.skip()
class TestUserRegistration(BaseCase):
    absent_fields = [field for field in UserData.USER_WITH_EXISTING_EMAIL.keys()]

    def test_create_user_successfully(self):
        """Test checks registration of new user with valid email"""
        data = self.prepare_registration_data()

        response = MyRequests.post(ApiPostLinks.CREATE_USER, data=data)
        Assertions.check_status_code(response, 200)
        Assertions.check_json_has_key(response, "id")

    @pytest.mark.parametrize("invalid_email", InvalidUserData.INVALID_EMAILS)
    def test_create_user_with_invalid_email(self, invalid_email):
        """Test checks email validation"""

        data = self.prepare_registration_data(invalid_email)

        response = MyRequests.post(ApiPostLinks.CREATE_USER, data=data)
        Assertions.check_status_code(response, 400)
        Assertions.is_there_error_in_response_text(response, "Invalid email format")

    @pytest.mark.parametrize("absent_field", absent_fields)
    def test_create_user_with_absent_field(self, absent_field):
        """Test checks possibility of user registration
        without one of required fields in registration data"""

        data = self.prepare_registration_data()
        data[absent_field] = None
        response = MyRequests.post(ApiPostLinks.CREATE_USER, data=data)
        Assertions.check_status_code(response, 400)
        error = f"The following required params are missed: {absent_field}"
        Assertions.is_there_error_in_response_text(response, error)

    def test_create_user_with_existing_email(self):
        """Test checks possibility of user registration
        with already registered email"""
        data = UserData.USER_WITH_EXISTING_EMAIL
        response = MyRequests.post(ApiPostLinks.CREATE_USER, data=data)

        print(response.status_code)
        print(response.content)

        Assertions.check_status_code(response, 400)
        assert response.content.decode("utf-8") == f"Users with email '{data['email']}' already exists", \
            f"Unexpected response content {response.content}"
