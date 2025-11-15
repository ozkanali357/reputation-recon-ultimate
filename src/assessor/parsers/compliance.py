from typing import Dict, Any
import requests

class ComplianceParser:
    def __init__(self):
        self.compliance_data = {}

    def fetch_compliance_data(self, url: str) -> None:
        response = requests.get(url)
        if response.status_code == 200:
            self.compliance_data = response.json()
        else:
            raise Exception(f"Failed to fetch data from {url}")

    def parse_compliance(self) -> Dict[str, Any]:
        parsed_data = {}
        # Example parsing logic; this should be tailored to the actual data structure
        for item in self.compliance_data.get('compliance', []):
            parsed_data[item['id']] = {
                'name': item['name'],
                'status': item['status'],
                'details': item.get('details', ''),
            }
        return parsed_data

    def get_compliance_summary(self) -> Dict[str, Any]:
        summary = {
            'total_compliance': len(self.compliance_data.get('compliance', [])),
            'compliant': sum(1 for item in self.compliance_data.get('compliance', []) if item['status'] == 'compliant'),
            'non_compliant': sum(1 for item in self.compliance_data.get('compliance', []) if item['status'] != 'compliant'),
        }
        return summary