from typing import Any, Dict
import httpx

class ComplianceFetcher:
    def __init__(self, base_url: str):
        self.base_url = base_url

    def fetch_compliance_data(self, product_name: str) -> Dict[str, Any]:
        response = httpx.get(f"{self.base_url}/compliance/{product_name}")
        response.raise_for_status()
        return response.json()

    def parse_compliance_data(self, data: Dict[str, Any]) -> Dict[str, Any]:
        # Implement parsing logic here
        parsed_data = {
            "product": data.get("product"),
            "compliance_standards": data.get("standards"),
            "certifications": data.get("certifications"),
        }
        return parsed_data

    def get_compliance_info(self, product_name: str) -> Dict[str, Any]:
        data = self.fetch_compliance_data(product_name)
        return self.parse_compliance_data(data)