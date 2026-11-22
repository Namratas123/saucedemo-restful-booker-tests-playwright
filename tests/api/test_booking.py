from tests.api.conftest import build_booking

NON_EXISTENT_ID = 999_999_999


class TestCreateBooking:
    def test_creates_a_booking_and_echoes_what_was_sent(self, api, auth_headers):
        payload = build_booking()

        response = api.post("/booking", data=payload)

        assert response.status == 200
        body = response.json()
        assert body["bookingid"] > 0
        assert body["booking"] == payload
        api.delete(f"/booking/{body['bookingid']}", headers=auth_headers)

    def test_accepts_a_zero_price_and_unicode_names(self, api, auth_headers):
        payload = build_booking(firstname="Zoë", lastname="Müller-Åkesson", totalprice=0)

        response = api.post("/booking", data=payload)

        assert response.status == 200
        body = response.json()
        assert body["booking"]["firstname"] == "Zoë"
        assert body["booking"]["totalprice"] == 0
        api.delete(f"/booking/{body['bookingid']}", headers=auth_headers)

    def test_rejects_a_booking_with_required_fields_missing(self, api):
        response = api.post("/booking", data={"firstname": "OnlyFirstName"})

        # Restful-Booker answers invalid bodies with a 500 rather than a 400.
        assert not response.ok
        assert response.status in (400, 500)


class TestReadBooking:
    def test_returns_the_booking_that_was_created(self, api, booking):
        response = api.get(f"/booking/{booking['id']}")

        assert response.status == 200
        assert response.json() == booking["payload"]

    def test_lists_the_new_booking_id_in_the_full_list(self, api, booking):
        response = api.get("/booking")

        assert response.status == 200
        assert booking["id"] in [item["bookingid"] for item in response.json()]

    def test_filters_the_list_by_first_name(self, api, booking):
        response = api.get("/booking", params={"firstname": booking["payload"]["firstname"]})

        assert response.status == 200
        assert response.json() == [{"bookingid": booking["id"]}]

    def test_returns_404_for_an_id_that_does_not_exist(self, api):
        response = api.get(f"/booking/{NON_EXISTENT_ID}")

        assert response.status == 404


class TestUpdateBooking:
    def test_full_update_with_a_token_replaces_every_field(self, api, booking, auth_headers):
        updated = build_booking(
            firstname=f"{booking['payload']['firstname']}X",
            lastname="Updated",
            totalprice=321,
            depositpaid=False,
            bookingdates={"checkin": "2027-01-10", "checkout": "2027-01-12"},
            additionalneeds="Late checkout",
        )

        response = api.put(f"/booking/{booking['id']}", headers=auth_headers, data=updated)

        assert response.status == 200
        assert response.json() == updated
        assert api.get(f"/booking/{booking['id']}").json() == updated

    def test_full_update_also_works_with_basic_auth_instead_of_a_token(self, api, booking):
        updated = {**booking["payload"], "lastname": "BasicAuth"}

        response = api.put(
            f"/booking/{booking['id']}",
            headers={"Authorization": "Basic YWRtaW46cGFzc3dvcmQxMjM="},
            data=updated,
        )

        assert response.status == 200
        assert response.json()["lastname"] == "BasicAuth"

    def test_partial_update_changes_only_the_fields_that_were_sent(self, api, booking, auth_headers):
        response = api.patch(
            f"/booking/{booking['id']}",
            headers=auth_headers,
            data={"firstname": "PatchedName", "totalprice": 999},
        )

        assert response.status == 200
        body = response.json()
        assert body["firstname"] == "PatchedName"
        assert body["totalprice"] == 999
        assert body["lastname"] == booking["payload"]["lastname"]
        assert body["bookingdates"] == booking["payload"]["bookingdates"]

    def test_update_without_a_token_is_forbidden_and_changes_nothing(self, api, booking):
        response = api.put(
            f"/booking/{booking['id']}",
            data={**booking["payload"], "lastname": "ShouldNotSave"},
        )

        assert response.status == 403
        assert api.get(f"/booking/{booking['id']}").json()["lastname"] == booking["payload"]["lastname"]

    def test_update_with_an_invalid_token_is_forbidden(self, api, booking):
        response = api.put(
            f"/booking/{booking['id']}",
            headers={"Cookie": "token=not-a-real-token"},
            data=booking["payload"],
        )

        assert response.status == 403

    def test_update_of_an_id_that_does_not_exist_is_refused(self, api, auth_headers):
        response = api.put(f"/booking/{NON_EXISTENT_ID}", headers=auth_headers, data=build_booking())

        # Restful-Booker answers 405 here; a stricter API would use 404.
        assert response.status in (404, 405)


class TestDeleteBooking:
    def test_delete_with_a_token_removes_the_booking(self, api, booking, auth_headers):
        response = api.delete(f"/booking/{booking['id']}", headers=auth_headers)

        # Restful-Booker answers a successful delete with 201 Created.
        assert response.status == 201
        assert api.get(f"/booking/{booking['id']}").status == 404

    def test_delete_without_a_token_is_forbidden_and_the_booking_stays(self, api, booking):
        response = api.delete(f"/booking/{booking['id']}")

        assert response.status == 403
        assert api.get(f"/booking/{booking['id']}").status == 200

    def test_deleting_the_same_booking_twice_fails_the_second_time(self, api, booking, auth_headers):
        api.delete(f"/booking/{booking['id']}", headers=auth_headers)

        second = api.delete(f"/booking/{booking['id']}", headers=auth_headers)

        assert second.status in (404, 405)

    def test_delete_of_an_id_that_does_not_exist_is_refused(self, api, auth_headers):
        response = api.delete(f"/booking/{NON_EXISTENT_ID}", headers=auth_headers)

        assert response.status in (404, 405)
