class Evidence:
    def __init__(self, claim_id, url, source_type, excerpt, retrieved_at, parser_id):
        self.claim_id = claim_id
        self.url = url
        self.source_type = source_type
        self.excerpt = excerpt
        self.retrieved_at = retrieved_at
        self.parser_id = parser_id

    def __repr__(self):
        return f"<Evidence claim_id={self.claim_id}, url={self.url}, source_type={self.source_type}>"

    def to_dict(self):
        return {
            "claim_id": self.claim_id,
            "url": self.url,
            "source_type": self.source_type,
            "excerpt": self.excerpt,
            "retrieved_at": self.retrieved_at,
            "parser_id": self.parser_id,
        }