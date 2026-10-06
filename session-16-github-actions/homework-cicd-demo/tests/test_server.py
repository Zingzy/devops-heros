import json
import threading
from http.server import ThreadingHTTPServer
from urllib.error import HTTPError
from urllib.request import urlopen

import pytest

from app.server import CalculatorHandler


@pytest.fixture(scope="module")
def base_url():
    server = ThreadingHTTPServer(("127.0.0.1", 0), CalculatorHandler)
    threading.Thread(target=server.serve_forever, daemon=True).start()
    yield f"http://127.0.0.1:{server.server_port}"
    server.shutdown()


def get(url):
    try:
        with urlopen(url) as resp:
            return resp.status, json.load(resp)
    except HTTPError as e:
        return e.code, json.load(e)


def test_healthz(base_url):
    status, body = get(f"{base_url}/healthz")
    assert status == 200
    assert body["status"] == "ok"


@pytest.mark.parametrize(
    "op, expected",
    [("add", 15), ("subtract", 5), ("multiply", 50), ("divide", 2)],
)
def test_calc(base_url, op, expected):
    status, body = get(f"{base_url}/calc/{op}?a=10&b=5")
    assert status == 200
    assert body["result"] == expected


def test_divide_by_zero_is_400(base_url):
    status, body = get(f"{base_url}/calc/divide?a=10&b=0")
    assert status == 400
    assert body["error"] == "Cannot divide by zero"


def test_bad_number_is_400(base_url):
    status, _ = get(f"{base_url}/calc/add?a=ten&b=5")
    assert status == 400


def test_unknown_route_is_404(base_url):
    status, _ = get(f"{base_url}/calc/power?a=2&b=3")
    assert status == 404
