class UserData:
    TEST_USER1 = {
        'email': 'vinkotov@example.com',
        'password': '1234'
    }
    USER_WITH_EXISTING_EMAIL = {
        'password': '123',
        'username': 'testname',
        'firstName': 'testfirstname',
        'lastName': 'testLastname',
        'email': 'vinkotov@example.com'
    }
    USER_KEYS = ["username", "email", "firstName", "lastName"]


class InvalidUserData:
    INVALID_EMAILS = [
        "test12345example.com",
        "test12345@examplecom",
        "test12345examplecom",

    ]
