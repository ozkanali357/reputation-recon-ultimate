def test_scoring_engine():
    from assessor.scoring.engine import calculate_risk_score

    # Test case 1: Basic risk score calculation
    inputs = {
        'exposure': 30,
        'controls': 20,
        'vendor_posture': 15,
        'compliance': 15,
        'incidents': 10,
        'data_handling': 10,
        'confidence': 0.9
    }
    expected_score = (inputs['exposure'] * 0.3 +
                      inputs['controls'] * 0.2 +
                      inputs['vendor_posture'] * 0.15 +
                      inputs['compliance'] * 0.15 +
                      inputs['incidents'] * 0.1 +
                      inputs['data_handling'] * 0.1) * inputs['confidence']
    
    score = calculate_risk_score(**inputs)
    assert score == expected_score, f"Expected {expected_score}, got {score}"

    # Test case 2: Edge case with zero confidence
    inputs['confidence'] = 0
    expected_score = 0
    score = calculate_risk_score(**inputs)
    assert score == expected_score, f"Expected {expected_score}, got {score}"

    # Test case 3: All inputs at maximum
    inputs = {
        'exposure': 100,
        'controls': 100,
        'vendor_posture': 100,
        'compliance': 100,
        'incidents': 100,
        'data_handling': 100,
        'confidence': 1
    }
    expected_score = (inputs['exposure'] * 0.3 +
                      inputs['controls'] * 0.2 +
                      inputs['vendor_posture'] * 0.15 +
                      inputs['compliance'] * 0.15 +
                      inputs['incidents'] * 0.1 +
                      inputs['data_handling'] * 0.1) * inputs['confidence']
    
    score = calculate_risk_score(**inputs)
    assert score == expected_score, f"Expected {expected_score}, got {score}"

    # Test case 4: Negative inputs (should handle gracefully)
    inputs = {
        'exposure': -10,
        'controls': -20,
        'vendor_posture': -15,
        'compliance': -15,
        'incidents': -10,
        'data_handling': -10,
        'confidence': 1
    }
    expected_score = 0  # Assuming negative inputs should not contribute to score
    score = calculate_risk_score(**inputs)
    assert score == expected_score, f"Expected {expected_score}, got {score}"