from datetime import datetime
import json
import os

class Snapshot:
    def __init__(self, snapshot_id, created_at=None):
        self.snapshot_id = snapshot_id
        self.created_at = created_at or datetime.utcnow().isoformat()
        self.content = {}
        self.facts = {}
        self.claims = {}

    def add_content(self, url, sha256, retrieved_at):
        self.content[url] = {
            'sha256': sha256,
            'retrieved_at': retrieved_at
        }

    def add_fact(self, claim_id, text, score_contrib, confidence):
        self.facts[claim_id] = {
            'text': text,
            'score_contrib': score_contrib,
            'confidence': confidence
        }

    def add_claim(self, claim_id, product_id, category, text, score_contrib, confidence):
        self.claims[claim_id] = {
            'product_id': product_id,
            'category': category,
            'text': text,
            'score_contrib': score_contrib,
            'confidence': confidence
        }

    def save(self, directory):
        if not os.path.exists(directory):
            os.makedirs(directory)
        snapshot_file = os.path.join(directory, f"{self.snapshot_id}.json")
        with open(snapshot_file, 'w') as f:
            json.dump({
                'snapshot_id': self.snapshot_id,
                'created_at': self.created_at,
                'content': self.content,
                'facts': self.facts,
                'claims': self.claims
            }, f, indent=4)

    @classmethod
    def load(cls, snapshot_file):
        with open(snapshot_file, 'r') as f:
            data = json.load(f)
            snapshot = cls(data['snapshot_id'], data['created_at'])
            snapshot.content = data['content']
            snapshot.facts = data['facts']
            snapshot.claims = data['claims']
            return snapshot