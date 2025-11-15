class Claim:
    def __init__(self, id, product_id, category, text, score_contrib, confidence):
        self.id = id
        self.product_id = product_id
        self.category = category
        self.text = text
        self.score_contrib = score_contrib
        self.confidence = confidence

    def __repr__(self):
        return f"Claim(id={self.id}, product_id={self.product_id}, category={self.category}, text={self.text}, score_contrib={self.score_contrib}, confidence={self.confidence})"