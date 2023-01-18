from enviroment import ENV_OBJECT
# "https://playground.learnqa.ru/api"
BASE_URL = ENV_OBJECT.get_base_url()


class ApiGetLinks:
    GET_AUTHORIZED_USER_ID = '/user/auth'
    # id is required
    GET_USER_INFO_BY_ID = "/user/"


class ApiPostLinks:
    USER_LOGIN = '/user/login'
    CREATE_USER = '/user/'


class ApiPutLinks:
    # id is required
    UPDATE_USER = "/user/"


class ApiDeleteLinks:
    # id is required
    DELETE_USER_BY_ID = "/user/"
