from endpoints.endpoints import ApiDeleteLinks, ApiGetLinks
from lib.assertions import Assertions
from lib.base_case import BaseCase
from lib.my_requests import MyRequests
from testdata.userdata import UserData


class TestUserDelete(BaseCase):
    def setup(self):
        self.first_user_registration_data = self.prepare_registration_data()
        self.first_user_login_data = self.register_new_user(self.first_user_registration_data)

    def test_deleting_just_created_authorized_user(self):
        """Test checks deleting of authorized user"""
        # LOGIN
        auth_data = self.log_in_user(self.first_user_login_data)

        # DELETE
        response = MyRequests.delete(
            f"{ApiDeleteLinks.DELETE_USER_BY_ID}{self.first_user_login_data['user_id']}",
            headers={"x-csrf-token": auth_data["token"]},
            cookies={"auth_sid": auth_data['auth_sid']}
        )
        Assertions.check_status_code(response, 200)

        # GET
        response2 = MyRequests.get(
            f"{ApiGetLinks.GET_USER_INFO_BY_ID}{self.first_user_login_data['user_id']}",
            headers={"x-csrf-token": auth_data["token"]},
            cookies={"auth_sid": auth_data['auth_sid']}
        )
        Assertions.is_there_error_in_response_text(response2, "User not found")
        print(response2.text)

    def test_delete_user_by_another_authorized_user(self):
        """Test checks user deleting by another authorized user"""
        # SECOND USER REGISTRATION
        registration_data = self.prepare_registration_data()
        second_user_login_data = self.register_new_user(registration_data)

        # SECOND USER LOGIN
        second_user_auth_data = self.log_in_user(second_user_login_data)

        # DELETE FIRST USER
        response = MyRequests.delete(
            f"{ApiDeleteLinks.DELETE_USER_BY_ID}{self.first_user_login_data['user_id']}",
            headers={"x-csrf-token": second_user_auth_data["token"]},
            cookies={"auth_sid": second_user_auth_data['auth_sid']}
        )
        Assertions.check_status_code(response, 200)

        # LOGIN FIRST USER
        first_user_auth_data = self.log_in_user(self.first_user_login_data)

        # GET FIRST USER
        response2 = MyRequests.get(
            f"{ApiGetLinks.GET_USER_INFO_BY_ID}{self.first_user_login_data['user_id']}",
            headers={"x-csrf-token": first_user_auth_data["token"]},
            cookies={"auth_sid": first_user_auth_data['auth_sid']}
        )
        Assertions.check_json_has_keys(response2, UserData.USER_KEYS)
