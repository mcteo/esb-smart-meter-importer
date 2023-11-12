import json
import re

import pytest
from requests import Session
import requests_mock

from esb_smart_meter_importer import importer


@pytest.fixture(autouse=True)
def mock_requests():
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


def test_get_app_settings():
    sess = Session()

    csrf, transaction_id = importer.get_app_settings(sess)

    assert csrf == "FAKE_CSRF_TOKEN"
    assert transaction_id == "StateProperties=XXX"


def test_login():
    sess = Session()

    importer.login(sess, "username", "password", "csrf", "tx")


def test_fetch_data():
    sess = Session()

    imports, exports = importer.fetch_data(sess, "100xxx", "2023-01-01")

    assert len(imports.items()) == 3
    assert len(exports.items()) == 0


def test_smart_meter_usage():
    imports, exports = importer.smart_meter_usage("username", "password", "100xxx", "2023-01-01")

    assert len(imports.items()) == 3
    assert len(exports.items()) == 0
