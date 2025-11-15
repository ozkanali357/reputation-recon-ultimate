from typing import List, Dict
import httpx

class CISAKEVFetcher:
    BASE_URL = "https://www.cisa.gov/known-exploited-vulnerabilities-catalog-api"

    def fetch_data(self) -> List[Dict]:
        response = httpx.get(self.BASE_URL)
        response.raise_for_status()  # Raise an error for bad responses
        return response.json().get("data", [])

    def parse_data(self, data: List[Dict]) -> List[Dict]:
        parsed_data = []
        for item in data:
            parsed_data.append({
                "id": item.get("id"),
                "name": item.get("attributes", {}).get("name"),
                "description": item.get("attributes", {}).get("description"),
                "published_date": item.get("attributes", {}).get("published"),
                "last_modified": item.get("attributes", {}).get("modified"),
                "cve": item.get("attributes", {}).get("cve"),
            })
        return parsed_data

    def get_kev_data(self) -> List[Dict]:
        raw_data = self.fetch_data()
        return self.parse_data(raw_data)