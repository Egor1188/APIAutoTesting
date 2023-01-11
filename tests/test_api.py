import pytest
import requests

proxy = {
    'https': '89.38.96.219:3128'
}


@pytest.mark.skip()
class TestApi:
    names = [
        "Rafael",
        "Michelangelo",
        "Donatello",
        "Leonardo",
        ""
    ]

    @pytest.mark.parametrize('name', names)
    def test_hello_call(self, name):
        url = 'https://playground.learnqa.ru/api/hello'
        data = {"name": name}

        response = requests.get(url, params=data, proxies=proxy)

        assert response.status_code == 200, "Wrong response code"

        response_dict = response.json()

        assert "answer" in response_dict, "There is no key 'answer' in the response"

        expected_response_text = f'Hello, {name}'
        actual_response_text = response_dict['answer']
        assert actual_response_text == expected_response_text, "Actual response text is incorrect"
