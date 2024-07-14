import pytest
from requests import Session

from esb_smart_meter_importer import importer
from esb_smart_meter_importer.exceptions import LoginError


def test_get_app_settings(mock_valid_requests):
    sess = Session()

    csrf, transaction_id = importer.get_app_settings(sess)

    assert csrf == "FAKE_CSRF_TOKEN"
    assert transaction_id == "StateProperties=XXX"


def test_login(mock_valid_requests):
    sess = Session()

    importer.login(sess, "username", "password", "csrf", "tx")


def test_fetch_data(mock_valid_requests):
    sess = Session()

    imports, exports = importer.fetch_data(sess, "100xxx", "2023-01-01")

    assert len(imports.items()) == 3
    assert len(exports.items()) == 0


def test_smart_meter_usage(mock_valid_requests):
    imports, exports = importer.smart_meter_usage("username", "password", "100xxx", "2023-01-01")

    assert len(imports.items()) == 3
    assert len(exports.items()) == 0


def test_invalid_login(mock_login_failed_requests):
    sess = Session()

    with pytest.raises(LoginError):
        importer.login(sess, "username", "password", "csrf", "tx")
