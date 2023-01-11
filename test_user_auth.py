import pytest
from tests.user_auth_tests import UserAuth


class TestUserAuth:
    exclude_params = {
        'no_cookie',
        'no_token'
    }

    def test_user_auth(self):
        user = UserAuth()
        user.is_the_response_correct()
        user.is_user_authorized()

    @pytest.mark.parametrize('condition', exclude_params)
    def test_negative_auth(self, condition):
        test = UserAuth()
        test.is_the_response_correct()

        test.cant_authorize_without_cookie_or_csrf(condition=condition)
