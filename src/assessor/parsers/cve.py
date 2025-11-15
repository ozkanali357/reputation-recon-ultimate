from typing import List, Dict
import requests

class CVEParser:
    def __init__(self, cve_data: Dict):
        self.cve_data = cve_data

    def parse(self) -> List[Dict]:
        parsed_data = []
        for item in self.cve_data.get('CVE_Items', []):
            cve_id = item['cve']['CVE_data_meta']['ID']
            description = item['cve']['description']['description_data'][0]['value']
            severity = self.get_severity(item)
            parsed_data.append({
                'cve_id': cve_id,
                'description': description,
                'severity': severity,
                'references': self.get_references(item)
            })
        return parsed_data

    def get_severity(self, item: Dict) -> str:
        if 'impact' in item:
            if 'baseMetricV3' in item['impact']:
                return item['impact']['baseMetricV3']['severity']
        return 'UNKNOWN'

    def get_references(self, item: Dict) -> List[str]:
        references = []
        if 'references' in item['cve']:
            for ref in item['cve']['references']['reference_data']:
                references.append(ref['url'])
        return references

def fetch_cve_data(url: str) -> Dict:
    response = requests.get(url)
    response.raise_for_status()
    return response.json()