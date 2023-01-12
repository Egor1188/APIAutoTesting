import json

from requests import Response


class Assertions:
    @staticmethod
    def assert_json_value_by_name(response: Response, name, expected_value, error_message):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"
        assert response_as_dict[name] == expected_value, error_message

    @staticmethod
    def check_json_has_key(response: Response, name):
        try:
            response_as_dict = response.json()
        except json.JSONDecodeError:
            assert False, f"Response is not in JSON Format. Response text is {response.text}"

        assert name in response_as_dict, f"Response JSON doesn't have key {name}"

    @staticmethod
    def check_status_code(response: Response, expected_status_code):
        assert response.status_code == expected_status_code, f"Unexpected status code! " \
                                                             f"Expected: {expected_status_code}. " \
                                                             f"Actual: {response.status_code}"