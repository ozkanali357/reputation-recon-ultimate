from fastapi import APIRouter, HTTPException
from typing import List, Any, Dict
from assessor.models.claim import Claim
from assessor.scoring.engine import calculate_risk_score

router = APIRouter()

def get_cached_comparison(product_name: str) -> Dict[str, Any]:
    # TODO(step 4): return cached comparison from SQLite/JSON
    return {}

@router.get("/compare/{product_name}")
async def compare_products(product_name: str):
    comparison_data = get_cached_comparison(product_name)
    if not comparison_data:
        raise HTTPException(status_code=404, detail="Product not found or insufficient evidence.")

    claims = []
    for claim in comparison_data.get('claims', []):
        score = calculate_risk_score(
            exposure=claim.get('exposure', 0),
            controls=claim.get('controls', 0),
            vendor_posture=claim.get('vendor_posture', 0),
            compliance=claim.get('compliance', 0),
            incidents=claim.get('incidents', 0),
            data_handling=claim.get('data_handling', 0),
            confidence=claim.get('confidence', 0),
        )
        claims.append(Claim(
            id=claim['id'],
            product_id=claim['product_id'],
            category=claim['category'],
            text=claim['text'],
            score_contrib=score,
            confidence=claim['confidence']
        ))
    return claims