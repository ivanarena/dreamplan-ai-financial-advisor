def test_calculate_target_prices_success(api, payload):
    """Test successful API call to calculate target prices"""
    response = api.calculate_target_prices(payload)

    assert response is not None
    assert "companyOutput" in response
    assert "emergencySavingsOutput" in response
    assert "houseAndMortgageOutput" in response
    assert "liquidSavingsOutput" in response
    assert "pensionOutput" in response
    assert "overallResultOutput" in response
    assert "messages" in response
    # assert "statements" in response
