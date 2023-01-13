from json.decoder import JSONDecodeError
import requests
proxy = {
    'https': '89.38.96.219:3128'
}
payload = {
    "name": "User"
}
# response = requests.get('https://playground.learnqa.ru/api/hello',params=payload, proxies=proxy)
# print(response.text)
# try:
#     parsed_response = response.json()
#     print(parsed_response['answer'])
# except JSONDecodeError:
#     print("Response is not JSON format")


# response_get = requests.get("https://playground.learnqa.ru/api/check_type", params=payload, proxies=proxy)
# response_post = requests.post("https://playground.learnqa.ru/api/check_type", data=payload, proxies=proxy)
# print(response_get.text)
# print(response_post.text)
# response_get_500 = requests.get("https://playground.learnqa.ru/api/get_500", proxies=proxy)
# print(response_get_500.status_code)
# response_get_301 = requests.get("https://playground.learnqa.ru/api/get_301", allow_redirects=True, proxies=proxy)
# first_response = response_get_301.history[0]
# print(first_response.url)
# second_response = response_get_301
# print(second_response.url)
# print(response_get_301.status_code)

# headers = {"some_headers": "123"}
# response_headers = requests.get("https://playground.learnqa.ru/api/show_all_headers", headers=headers, proxies=proxy)
# print(response_headers.text)
# print(response_headers.headers)

# payload = {
#     "login": "secret_login",
#     "password": "secret_pass"
# }
# response_auth_cookie1 = requests.post("https://playground.learnqa.ru/api/get_auth_cookie", data=payload, proxies=proxy)
# print(response_auth_cookie1.text)
# print(response_auth_cookie1.status_code)
# print(response_auth_cookie1.cookies)
# print(dict(response_auth_cookie1.cookies))
# cookie_value = response_auth_cookie1.cookies.get('auth_cookie')
# cookies = {}
# if cookie_value is not None:
#     cookies.update({'auth_cookie': cookie_value})
# response_auth_cookie2 = requests.post("https://playground.learnqa.ru/api/check_auth_cookie", proxies=proxy, cookies=cookies)
# print(response_auth_cookie2.text)
# print(response_auth_cookie2.status_code)



