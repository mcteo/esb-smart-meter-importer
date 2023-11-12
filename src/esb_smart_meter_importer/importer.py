import json
from datetime import datetime
from typing import Dict, Tuple

from bs4 import BeautifulSoup
from requests import Session


def get_app_settings(sess: Session) -> Tuple[str, str]:
    """
    Fetches some of the dynamic settings to needed to login.
    """
    req = sess.get("https://myaccount.esbnetworks.ie")
    req.raise_for_status()

    soup = BeautifulSoup(req.content, "html.parser")
    script_tag = soup.script.text

    start = script_tag.find("{", script_tag.find("SETTINGS"))
    end = script_tag.find(";", start)

    settings = json.loads(script_tag[start:end])

    return settings["csrf"], settings["transId"]


def login(sess: Session, username: str, password: str, csrf_token: str, transaction_id: str) -> None:
    """
    The endpoint for fetching the usage data we want uses cookie authentication. Therefore we
    simulate going through the different login steps in order fill the given Session with cookies.
    """
    initial_login_req = sess.post(
        "https://login.esbnetworks.ie/esbntwkscustportalprdb2c01.onmicrosoft.com/B2C_1A_signup_signin/SelfAsserted",
        data={
            "request_type": "RESPONSE",
            "signInName": username,
            "password": password,
        },
        params={
            "tx": transaction_id,
            "p": "B2C_1A_signup_signin",
        },
        headers={
            "X-CSRF-TOKEN": csrf_token,
        },
    )
    initial_login_req.raise_for_status()

    form_tokens_req = sess.get(
        "https://login.esbnetworks.ie/esbntwkscustportalprdb2c01.onmicrosoft.com"
        "/B2C_1A_signup_signin/api/CombinedSigninAndSignup/confirmed",
        params={
            "rememberMe": False,
            "csrf_token": csrf_token,
            "tx": transaction_id,
            "p": "B2C_1A_signup_signin",
        },
    )
    form_tokens_req.raise_for_status()

    soup = BeautifulSoup(form_tokens_req.content, "html.parser")
    form = soup.find("form", {"id": "auto"})

    confirm_login_req = sess.post(
        form["action"],
        allow_redirects=False,
        data={
            "state": form.find("input", {"name": "state"})["value"],
            "client_info": form.find("input", {"name": "client_info"})["value"],
            "code": form.find("input", {"name": "code"})["value"],
        },
    )
    confirm_login_req.raise_for_status()


def parse_date(date_str: str) -> datetime:
    return datetime.fromisoformat(date_str)


def fetch_data(sess: Session, mprn: str, start_date: str) -> Tuple[Dict[datetime, float], Dict[datetime, float]]:
    req = sess.get(
        "https://myaccount.esbnetworks.ie/datahub/GetHdfContent",
        params={
            "mprn": mprn,
            "startDate": start_date,
            "unit": "kWh",
        },
    )
    req.raise_for_status()

    data = req.json()

    imports = {parse_date(unit["x"]): unit["y"] for unit in data["imports"]}
    exports = {parse_date(unit["x"]): unit["y"] for unit in data["exports"]}

    return imports, exports


def smart_meter_usage(
    username: str, password: str, mprn: str, start_date: str
) -> Tuple[Dict[datetime, float], Dict[datetime, float]]:
    sess = Session()

    csrf_token, transaction_id = get_app_settings(sess)

    login(sess, username, password, csrf_token, transaction_id)

    return fetch_data(sess, mprn, start_date)
