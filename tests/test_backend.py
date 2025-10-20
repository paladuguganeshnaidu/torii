import os
import pytest
import requests

BASE = os.environ.get('TORII_BASE', 'http://127.0.0.1:5000')

def reachable():
    try:
        requests.get(BASE, timeout=1)
        return True
    except Exception:
        return False

@pytest.mark.skipif(not reachable(), reason="Flask not running on default port")
def test_api_scan_url_smoke():
    files = { }
    data = { 'urls': 'https://example.com' }
    r = requests.post(f"{BASE}/api/scan_url", data=data, files=files, timeout=5)
    assert r.status_code == 200
    assert 'example.com' in r.text

@pytest.mark.skipif(not reachable(), reason="Flask not running on default port")
def test_api_sms_smoke():
    data = { 'text': 'You are a winner! click link to win prize' }
    r = requests.post(f"{BASE}/api/test_sms", data=data, timeout=5)
    assert r.status_code == 200
