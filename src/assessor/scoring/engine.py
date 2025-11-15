from typing import Union

def _clamp_non_negative(x: Union[int, float]) -> float:
    try:
        return float(x) if x is not None and float(x) > 0 else 0.0
    except (TypeError, ValueError):
        return 0.0

def calculate_risk_score(
    exposure: float,
    controls: float,
    vendor_posture: float,
    compliance: float,
    incidents: float,
    data_handling: float,
    confidence: float
) -> float:
    """
    Weighted sum with non-negative clamping and confidence scalar.
    """
    weights = {
        'exposure': 0.30,
        'controls': 0.20,
        'vendor_posture': 0.15,
        'compliance': 0.15,
        'incidents': 0.10,
        'data_handling': 0.10
    }

    exposure = _clamp_non_negative(exposure)
    controls = _clamp_non_negative(controls)
    vendor_posture = _clamp_non_negative(vendor_posture)
    compliance = _clamp_non_negative(compliance)
    incidents = _clamp_non_negative(incidents)
    data_handling = _clamp_non_negative(data_handling)
    confidence = float(confidence or 0.0)

    base = (
        exposure * weights['exposure'] +
        controls * weights['controls'] +
        vendor_posture * weights['vendor_posture'] +
        compliance * weights['compliance'] +
        incidents * weights['incidents'] +
        data_handling * weights['data_handling']
    )
    return base * confidence

def generate_score_report(score, confidence):
    return {
        'score': score,
        'confidence': confidence,
        'status': 'Pass' if score >= 70 else 'Fail'
    }

def main():
    # Example inputs
    exposure = 25
    controls = 15
    vendor_posture = 10
    compliance = 12
    incidents = 8
    data_handling = 6

    risk_score = calculate_risk_score(exposure, controls, vendor_posture, compliance, incidents, data_handling)
    confidence = 0.85  # Example confidence level

    report = generate_score_report(risk_score, confidence)
    print(report)

if __name__ == "__main__":
    main()