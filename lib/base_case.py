import json.decoder
from datetime import datetime

import requests
from requests import Response

from endpoints.endpoints import ApiPostLinks, ApiGetLinks
from lib.assertions import Assertions
from lib.my_requests import MyRequests

from testdata.proxy import Proxy
from testdata.userdata import UserData


class BaseCase:

    def get_cookie(self, response: Response, cookie_name):
        assert cookie_name in response.cookies, f'Cannot find cookie with name {cookie_name} in the last response'
        return response.cookies[cookie_name]

    def get_header(self, response: Response, header_name):
        assert header_name in response.headers, f'Cannot find header with name {header_name}in the last response'
        return response.headers[header_name]

    def get_json_value(self, response: Response, name):
        try:
            response_as_dict = response.json()
        except json.decoder.JSONDecodeError:
            assert False, f'Response is not in JSON Format. Response text is {response.text}'

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        return response_as_dict[name]

    def prepare_registration_data(self, email=None):
        if email is None:
            base_part = "test"
            domain = "@example.com"
            random_part = datetime.now().strftime("%m%d%Y%H%M%S")
            email = f"{base_part}{random_part}{domain}"
        data = UserData.USER_WITH_EXISTING_EMAIL.copy()
        data["email"] = email
        return data

    def log_in_user(self, login_data: dict):
        login_data = {
            "email": login_data["email"],
            "password": login_data["password"]
        }
        response = MyRequests.post(ApiPostLinks.USER_LOGIN, data=login_data)
        print(response.text)
        auth_sid = self.get_cookie(response, "auth_sid")
        token = self.get_header(response, "x-csrf-token")
        Assertions.check_status_code(response, 200)
        Assertions.check_json_has_key(response, "user_id")
        return {
            "auth_sid": auth_sid,
            "token": token
        }

    def register_new_user(self, registration_data: dict):
        response = MyRequests.post(ApiPostLinks.CREATE_USER, data=registration_data)

        Assertions.check_status_code(response, 200)
        Assertions.check_json_has_key(response, "id")

        email = registration_data["email"]
        password = registration_data["password"]
        user_id = self.get_json_value(response, "id")
        return {
            "user_id": user_id,
            "email": email,
            "password": password
        }



#

