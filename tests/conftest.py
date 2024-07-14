import json
import re

import pytest
import requests_mock


@pytest.fixture()
def mock_valid_requests():
    with requests_mock.Mocker() as mock:
        with open("tests/mocks/homepage.html") as fin:
            mock.get("https://myaccount.esbnetworks.ie", text=fin.read())

        with open("tests/mocks/initial_login_response.json") as fin:
            mock.post(re.compile(".+/SelfAsserted"), json=json.loads(fin.read()))

        with open("tests/mocks/form_tokens.html") as fin:
            mock.get(re.compile(".+/confirmed"), text=fin.read())

        with open("tests/mocks/usage_page.html") as fin:
            mock.post("https://myaccount.esbnetworks.ie/signin-oidc", text=fin.read())

        with open("tests/mocks/data.json") as fin:
            mock.get("https://myaccount.esbnetworks.ie/datahub/GetHdfContent", json=json.loads(fin.read()))

        yield


@pytest.fixture()
def mock_login_failed_requests():
    with requests_mock.Mocker() as mock:
        with open("tests/mocks/invalid_login_response.json") as fin:
            mock.post(re.compile(".+/SelfAsserted"), json=json.loads(fin.read()))

        yield
