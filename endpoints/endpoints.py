class BaseUrl:
    BASE_URL = "https://playground.learnqa.ru/api"


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

