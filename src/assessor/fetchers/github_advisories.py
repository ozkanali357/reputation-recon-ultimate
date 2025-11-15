from typing import List, Dict
import httpx

class GitHubAdvisoriesFetcher:
    BASE_URL = "https://api.github.com/advisories"

    def fetch_advisories(self) -> List[Dict]:
        response = httpx.get(self.BASE_URL)
        response.raise_for_status()
        return response.json()

    def parse_advisory(self, advisory: Dict) -> Dict:
        return {
            "id": advisory.get("id"),
            "summary": advisory.get("summary"),
            "description": advisory.get("description"),
            "severity": advisory.get("severity"),
            "published_at": advisory.get("published_at"),
            "updated_at": advisory.get("updated_at"),
            "references": advisory.get("references"),
        }

    def get_advisories(self) -> List[Dict]:
        advisories = self.fetch_advisories()
        return [self.parse_advisory(advisory) for advisory in advisories]