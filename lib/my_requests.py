import requests
from endpoints import endpoints
from lib.logger import Logger
from testdata.proxy import Proxy


class MyRequests:
    @staticmethod
    def post(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "POST")

    @staticmethod
    def get(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "GET")

    @staticmethod
    def put(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "PUT")

    @staticmethod
    def delete(url: str, data: dict = None, headers: dict = None, cookies: dict = None):
        return MyRequests._send(url, data, headers, cookies, "DELETE")

    @staticmethod
    def _send(url: str, data: dict, headers: dict, cookies: dict, method: str):
        proxy = Proxy.PROXY
        url = f"{endpoints.BASE_URL}{url}"

        if headers is None:
            headers = {}
        if cookies is None:
            cookies = {}

        Logger.add_request(url, data, headers, cookies, method)

        if method == 'GET':
            response = requests.get(url, proxies=proxy, params=data, headers=headers, cookies=cookies)
        elif method == "POST":
            response = requests.post(url, proxies=proxy, data=data, headers=headers, cookies=cookies)
        elif method == "PUT":
            response = requests.put(url, proxies=proxy, data=data, headers=headers, cookies=cookies)
        elif method == 'DELETE':
            response = requests.delete(url, proxies=proxy, params=data, headers=headers, cookies=cookies)
        else:
            raise Exception(f"Bad HTTP method '{method}' was received")

        Logger.add_response(response)

        return response
