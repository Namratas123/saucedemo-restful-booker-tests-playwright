import uuid

import pytest

BASE_URL = "https://restful-booker.herokuapp.com"


def build_booking(**overrides) -> dict:
    """A booking with a unique first name, so tests never collide on the shared server."""
    booking = {
        "firstname": f"Qa{uuid.uuid4().hex[:10]}",
        "lastname": "Tester",
        "totalprice": 150,
        "depositpaid": True,
        "bookingdates": {"checkin": "2026-12-01", "checkout": "2026-12-05"},
        "additionalneeds": "Breakfast",
    }
    booking.update(overrides)
    return booking


@pytest.fixture(scope="session")
def api(playwright):
    context = playwright.request.new_context(
        base_url=BASE_URL,
        extra_http_headers={"Accept": "application/json"},
    )
    yield context
    context.dispose()


@pytest.fixture(scope="session")
def token(api) -> str:
    """A valid auth token for the admin test account."""
    response = api.post("/auth", data={"username": "admin", "password": "password123"})
    assert response.status == 200
    value = response.json().get("token")
    assert value
    return value


@pytest.fixture
def auth_headers(token) -> dict:
    return {"Cookie": f"token={token}"}


@pytest.fixture
def booking(api, auth_headers):
    """A booking created for this test only; deleted again in teardown."""
    payload = build_booking()
    response = api.post("/booking", data=payload)
    assert response.status == 200
    booking_id = response.json()["bookingid"]
    yield {"id": booking_id, "payload": payload}
    # The test may already have deleted it, so the status is not asserted.
    api.delete(f"/booking/{booking_id}", headers=auth_headers)
