import os
import json
import requests
from amadeus import Client, ResponseError, Location
from dotenv import load_dotenv

load_dotenv()


class AmadeusFlightService:
    def __init__(self):
        self.api_key, self.api_secret = self.get_amadeus_credentials()

        try:
            self.amadeus = Client(client_id=self.api_key, client_secret=self.api_secret)
        except Exception as e:
            raise Exception(f"Failed to create Amadeus client: {str(e)}")

    def get_amadeus_credentials(self) -> tuple[str, str]:
        api_key = os.getenv("AMADEUS_API_KEY")
        api_secret = os.getenv("AMADEUS_API_SECRET")
        if not api_key or not api_secret:
            raise ValueError("Amadeus API credentials not configured")
        return (api_key, api_secret)

    def get_amadeus_access_token(self) -> str:
        """
        Retrieves an Amadeus access token using client credentials from environment variables.

        Returns:
            The access token string if the request is successful.
        """
        client_id, client_secret = self.get_amadeus_credentials()

        url = "https://test.api.amadeus.com/v1/security/oauth2/token"

        data = {
            "grant_type": "client_credentials",
            "client_id": client_id,
            "client_secret": client_secret,
        }

        try:
            response = requests.post(url, data=data)
            response.raise_for_status()
            response_json = response.json()
            return response_json.get("access_token")

        except requests.exceptions.RequestException as e:
            raise e

    def search_flights(self, request_body: dict) -> dict:
        """
        Search for flight offers using Amadeus POST endpoint.
        """
        try:
            print("=" * 80)
            print("FLIGHT SEARCH REQUEST:")
            print(json.dumps(request_body, indent=2))
            print("=" * 80)

            # Amadeus requires: { "data": { ... } }
            payload = {"data": request_body}

            response = self.amadeus.shopping.flight_offers_search.post(payload)

            print("FLIGHT SEARCH RESPONSE STATUS: SUCCESS")
            print(f"Number of offers found: {len(response.data)}")
            print("=" * 80)

            return response.data

        except ResponseError as api_error:
            print("=" * 80)
            print("AMADEUS API ERROR:")

            if hasattr(api_error, 'response'):
                print(f"Status Code: {api_error.response.status_code}")
                print(f"Response Body: {api_error.response.body}")

            print("=" * 80)

            status_code = api_error.response.status_code if hasattr(api_error, 'response') else 400
            raise Exception(f"[{status_code}]")

    def confirm_price(self, request_body: dict):
        """
        Confirm flight pricing using Amadeus pricing endpoint.
        """
        try:
            response = self.amadeus.shopping.flight_offers.pricing.post(request_body)
            return response.data

        except ResponseError as error:
            print(f"Price confirmation error: {error}")
            if hasattr(error, 'response'):
                print(f"Response body: {error.response.body}")
            raise error

    def create_flight_order(self, request_body: dict):
        """
        Creates a flight order using a pre-selected and price-confirmed flight offer.

        IMPORTANT: The flight offer must be recent (from a fresh search/pricing call).
        Amadeus flight offers expire quickly and cannot be booked after they become stale.
        """
        try:
            flight_offer = request_body.get("flight_offer")
            travelers = request_body.get("travelers")

            if not flight_offer:
                raise ValueError("flight_offer is required in request body")
            if not travelers:
                raise ValueError("travelers information is required")

            # The Amadeus SDK expects flight_offer and travelers as separate arguments
            booked_flight = self.amadeus.booking.flight_orders.post(
                flight_offer, travelers
            ).data

            return booked_flight

        except ResponseError as error:
            # Log the error for debugging
            print(f"Amadeus API Error: {error}")
            if hasattr(error, "response"):
                print(f"Response body: {error.response.body}")
            raise error

    def search_flights_get(self, request_body: dict) -> dict:
        """
        Search for flights using GET method (simpler parameters).
        """
        try:
            response = self.amadeus.shopping.flight_offers_search.get(
                **request_body
            ).data
            return response
        except ResponseError as error:
            print(f"Flight search GET error: {error}")
            if hasattr(error, 'response'):
                print(f"Response body: {error.response.body}")
            raise error

    def view_seat_map_get(self, flightorderId: str) -> dict:
        """
        View seat map for a flight order.
        """
        try:
            response = self.amadeus.shopping.seatmaps.get(
                flightOrderId=flightorderId
            ).data
            return response
        except ResponseError as error:
            raise error

    def view_seat_map_post(self, flight_offer: dict) -> dict:
        """
        View seat map for a flight offer.
        """
        try:
            body = {"data": [flight_offer]}
            response = self.amadeus.shopping.seatmaps.post(body).data
            return response
        except ResponseError as error:
            raise error

    def get_flight_order(self, flight_orderId: str) -> dict:
        """
        Retrieves flight order details using the Amadeus Flight Orders API.

        Args:
            flight_order_id (str): The ID of the flight order to retrieve.

        Returns:
            dict: The flight order details.
        """
        try:
            response = self.amadeus.booking.flight_order(flight_orderId).get()
            return response.data
        except ResponseError as error:
            raise error

    def cancel_flight_order(self, flight_orderId: str) -> dict:
        """
        Cancels flight order details using the Amadeus Flight Orders API.

        Args:
            flight_order_id (str): The ID of the flight order to retrieve.

        Returns:
            dict: The flight order details.
        """
        try:
            response = self.amadeus.booking.flight_order(flight_orderId).delete()
            return response
        except ResponseError as error:
            raise error

    def airport_city_search(self, request_body: dict) -> dict:
        """
        Search for airports and cities.
        """
        try:
            keyword = request_body.get("keyword")
            sub_type = request_body.get("sub_type", "ANY")
            if sub_type.upper() == "AIRPORT":
                sub_type = Location.AIRPORT
            elif sub_type.upper() == "CITY":
                sub_type = Location.CITY
            else:
                sub_type = Location.ANY

            response = self.amadeus.reference_data.locations.get(
                keyword=keyword, subType=sub_type
            )
            return response.data
        except ResponseError as error:
            raise error

    def get_flight_orders(self, flight_order_ids: list[str]):
        """
        Retrieve multiple flight orders based on their ids.
        """
        try:
            flight_orders = []
            for order_id in flight_order_ids:
                response = self.amadeus.booking.flight_order(order_id).get()
                flight_orders.append(response.data)
            return flight_orders
        except ResponseError as error:
            raise error


amadeus_flight_service = AmadeusFlightService()