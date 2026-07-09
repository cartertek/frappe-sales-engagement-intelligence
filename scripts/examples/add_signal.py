import os

from _client import call

call(
    "sales_engagement_intelligence.sales_engagement_and_intelligence.api.add_signal",
    prospect=os.environ["SEI_PROSPECT"],
    payload={
        "signal_type": "Technical Distress",
        "signal_strength": "Moderate",
        "evidence_basis": "Observed",
        "confidence": 80,
        "source_url": "https://example.com/evidence",
        "evidence_notes": "Observed evidence from source page.",
        "counts_toward_qualification": 1,
    },
)
