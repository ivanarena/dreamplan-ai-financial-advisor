import requests
import dotenv
from calculation.templates import CalculateRequest, CalculateResponse
import os

dotenv.load_dotenv()


class CalculationApiClient:
    def __init__(
        self, base_url: str = os.getenv("CALCULATION_API_URL", "http://localhost:5000")
    ):
        self.base_url = base_url

    def calculate_target_prices(self, payload: CalculateRequest) -> CalculateResponse:
        url = f"{self.base_url}/api/CalculateTargetPrices"
        headers = {
            "Content-Type": "application/json",
        }

        try:
            response = requests.post(url, json=payload, headers=headers)

            if response.status_code == 200:
                return response.json()  # If the response is JSON
            else:
                print(f"Error: {response.status_code}")
                print(response.text)
                return None

        except requests.exceptions.RequestException as e:
            print(f"Request failed: {e}")
            return None


client = CalculationApiClient()
