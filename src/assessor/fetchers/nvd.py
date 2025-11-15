from typing import List, Dict
import httpx

class NVDFetcher:
    BASE_URL = "https://services.nvd.nist.gov/rest/json/v2/cve/"

    def __init__(self):
        self.client = httpx.Client()

    def fetch_cve_data(self, cve_id: str) -> Dict:
        response = self.client.get(f"{self.BASE_URL}{cve_id}")
        response.raise_for_status()
        return response.json()

    def fetch_recent_cves(self, start_index: int = 0, results_per_page: int = 20) -> List[Dict]:
        params = {
            "startIndex": start_index,
            "resultsPerPage": results_per_page
        }
        response = self.client.get(f"{self.BASE_URL}recent", params=params)
        response.raise_for_status()
        return response.json().get("result", {}).get("CVE_Items", [])

    def close(self):
        self.client.close()