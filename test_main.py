# test_main.py
import pytest
from main import app


@pytest.fixture
def client():
    """
    Pytest fixture that creates a Flask test client from the 'app' in main.py.
    """
    with app.test_client() as client:
        yield client


def test_root_endpoint(client):
    """
    Test the GET '/' endpoint to ensure it returns
    the greeting and a 200 status code.
    """
    resp = client.get("/")
    assert resp.status_code == 200
    assert b"Hello from my Password Validator!" in resp.data


# Not that this test only makes sense for the starter code,
# in practice we would not test for a 501 status code!

def test_check_password_no_uppercase(client):
    """
    Test lack of uppercase letters
    """
    resp = client.post("/v1/checkPassword", json={"password": "abc123$@!$#"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("reason") == "Needs at least 2 uppercase letters"
    assert data.get("valid") is False

def test_check_password_no_digits(client):
    """
    Test lack of digits letters
    """
    resp = client.post("/v1/checkPassword", json={"password": "abcABC$@!$#"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("reason") == "Needs at least 2 digits"
    assert data.get("valid") is False

def test_check_password_no_special_char(client):
    """
    Test lack of special characters
    """
    resp = client.post("/v1/checkPassword", json={"password": "abcABC123456"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("reason") == "Needs at least 1 special character"
    assert data.get("valid") is False

def test_check_password_valid(client):
    """
    Test a valid password
    """
    resp = client.post("/v1/checkPassword", json={"password": "abcABC123$@!"})
    assert resp.status_code == 200
    data = resp.get_json()
    assert data.get("valid") is True

def test_check_password_short(client):
    """
    Test a short password
    """
    resp = client.post("/v1/checkPassword", json={"password": "abc123"})
    assert resp.status_code == 400
    data = resp.get_json()
    assert data.get("reason") == "Length must be >= 8"
    assert data.get("valid") is False