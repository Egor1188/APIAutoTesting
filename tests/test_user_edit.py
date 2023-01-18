import pytest

from endpoints.endpoints import ApiPutLinks, ApiGetLinks
from lib.base_case import BaseCase
from lib.assertions import Assertions
from lib.my_requests import MyRequests
from testdata.userdata import UserData, InvalidUserData


@pytest.mark.skip
class TestUserEdit(BaseCase):

    def setup(self):
        # FIRST USER REGISTRATION
        registration_data = self.prepare_registration_data()
        self.first_user_login_data = self.register_new_user(registration_data)

    @pytest.mark.skip
    def test_edit_just_created_user(self):
        """Test checks possibility of just created user editing """
        # LOGIN
        auth_data = self.log_in_user(self.first_user_login_data)

        # EDIT
        new_name = "Changed Name"

        response3 = MyRequests.put(f"{ApiPutLinks.UPDATE_USER}{self.first_user_login_data['user_id']}",
                                   headers={"x-csrf-token": auth_data["token"]},
                                   cookies={"auth_sid": auth_data['auth_sid']},
                                   data={"firstName": new_name})

        Assertions.check_status_code(response3, 200)

        # GET
        response4 = MyRequests.get(
            f"{ApiGetLinks.GET_USER_INFO_BY_ID}{self.first_user_login_data['user_id']}",
            headers={"x-csrf-token": auth_data["token"]},
            cookies={"auth_sid": auth_data['auth_sid']}
        )

        Assertions.assert_json_value_by_name(
            response4,
            "firstName",
            new_name,
            "Wrong username after editing"
        )

    @pytest.mark.skip()
    def test_edit_user_data_by_another_authorized_user(self):
        """Test checks if it is possible to edit user data with another user's auth data"""

        # SECOND USER REGISTRATION
        registration_data = self.prepare_registration_data()
        second_user_login_data = self.register_new_user(registration_data)

        # SECOND USER LOGIN
        second_user_auth_data = self.log_in_user(second_user_login_data)

        # EDIT FIRST USER'S DATA WITH SECOND USER'S AUTH DATA
        new_name = "Changed Name"

        response3 = MyRequests.put(f"{ApiPutLinks.UPDATE_USER}{second_user_login_data['user_id']}",
                                   headers={"x-csrf-token": second_user_auth_data['token']},
                                   cookies={"auth_sid": second_user_auth_data['auth_sid']},
                                   data={"firstName": new_name})
        print(response3.text)
        Assertions.check_status_code(response3, 200)

        # FIRST USER LOGIN
        first_user_auth_data = self.log_in_user(self.first_user_login_data)

        # GET FIRST USER
        response5 = MyRequests.get(
            f"{ApiGetLinks.GET_USER_INFO_BY_ID}{self.first_user_login_data['user_id']}",
            headers={"x-csrf-token": first_user_auth_data['token']},
            cookies={"auth_sid": first_user_auth_data['auth_sid']}
        )
        print(response5.json())
        Assertions.assert_json_value_by_name(
            response5,
            "firstName",
            UserData.USER_WITH_EXISTING_EMAIL["firstName"],
            "Wrong username after editing"
        )
        # GET SECOND USER
        response6 = MyRequests.get(
            f"{ApiGetLinks.GET_USER_INFO_BY_ID}{second_user_login_data['user_id']}",
            headers={"x-csrf-token": second_user_auth_data['token']},
            cookies={"auth_sid": second_user_auth_data['auth_sid']}
        )
        print(response6.json())
        Assertions.assert_json_value_by_name(
            response6,
            "firstName",
            UserData.USER_WITH_EXISTING_EMAIL["firstName"],
            "Wrong username after editing"
        )

    # @pytest.mark.skip()
    def test_edit_user_data_by_same_unauthorized_user(self):
        """Test checks if it is possible to edit self user's data when user is unauthorized"""
        # EDIT
        new_name = "Changed Name"

        response1 = MyRequests.put(f"{ApiPutLinks.UPDATE_USER}{self.first_user_login_data['user_id']}",
                                   data={"firstName": new_name})

        Assertions.check_status_code(response1, 400)

        # LOGIN
        auth_data = self.log_in_user(self.first_user_login_data)

        # GET
        response2 = MyRequests.get(
            f"{ApiGetLinks.GET_USER_INFO_BY_ID}{self.first_user_login_data['user_id']}",
            headers={"x-csrf-token": auth_data['token']},
            cookies={"auth_sid": auth_data['auth_sid']}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "firstName",
            UserData.USER_WITH_EXISTING_EMAIL["firstName"],
            "Wrong username after editing"
        )

    # @pytest.mark.skip()
    @pytest.mark.parametrize("new_email", InvalidUserData.INVALID_EMAILS)
    def test_change_authorized_user_email_to_invalid_email(self, new_email):
        """Test checks if the self email can be changed to invalid by authorized user"""
        # LOGIN
        auth_data = self.log_in_user(self.first_user_login_data)
        # EDIT
        response1 = MyRequests.put(f"{ApiPutLinks.UPDATE_USER}{self.first_user_login_data['user_id']}",
                                   data={"email": new_email})
        Assertions.check_status_code(response1, 400)

        # GET
        response2 = MyRequests.get(
            f"{ApiGetLinks.GET_USER_INFO_BY_ID}{self.first_user_login_data['user_id']}",
            headers={"x-csrf-token": auth_data['token']},
            cookies={"auth_sid": auth_data['auth_sid']}
        )

        Assertions.assert_json_value_by_name(
            response2,
            "email",
            self.first_user_login_data["email"],
            "Email has been changed when it didn't have to"
        )
