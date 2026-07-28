from pathlib import Path


def test_embedded_signal_list_unwraps_api_contract_data():
    source = Path(
        "sales_engagement_intelligence/sales_engagement_and_intelligence/doctype/sei_prospect/sei_prospect.js"
    ).read_text()
    assert "const data = unwrap_api_data(response) || {};" in source
    assert "const signals = data.signals || [];" in source
    assert "response.message?.signals" not in source
