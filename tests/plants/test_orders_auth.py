import urllib.error
import urllib.request


def test_orders_without_token_returns_401(plants_url):
    request = urllib.request.Request(f"{plants_url}/api/orders")
    try:
        with urllib.request.urlopen(request) as response:
            status = response.status
    except urllib.error.HTTPError as err:
        status = err.code
    assert status == 401
