from __future__ import annotations

import importlib
import sys
from pathlib import Path

import pytest

ROOT = Path(__file__).resolve().parents[1]
APP_ROOT = ROOT
sys.path.insert(0, str(APP_ROOT))
runner = importlib.import_module(
    "sales_engagement_intelligence.sales_engagement_and_intelligence.services.signal_qualification_script"
)

pytestmark = pytest.mark.skipif(not runner._find_node(), reason="Node unavailable")


def test_default_script_preserves_three_way_threshold():
    strong = [{"strength": "Strong"}]
    one_moderate = [{"strength": "Moderate"}]
    two_moderate = [{"strength": "Moderate"}, {"strength": "Moderate"}]
    assert (
        runner.evaluate_signal_qualification_script(runner.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT, strong)
        == "Qualified"
    )
    assert (
        runner.evaluate_signal_qualification_script(runner.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT, one_moderate)
        == "Needs Review"
    )
    assert (
        runner.evaluate_signal_qualification_script(runner.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT, two_moderate)
        == "Qualified"
    )
    assert (
        runner.evaluate_signal_qualification_script(runner.DEFAULT_SIGNAL_QUALIFICATION_SCRIPT, [])
        == "Unqualified"
    )


def test_runner_exposes_every_qualification_status_enum_item():
    items = {
        "Qualified": "Qualified",
        "NeedsReview": "Needs Review",
        "ManuallyApproved": "Manually Approved",
        "Rejected": "Rejected",
        "DoNotContact": "Do Not Contact",
        "Unqualified": "Unqualified",
    }
    for item, expected in items.items():
        assert (
            runner.evaluate_signal_qualification_script(f"return QualificationStatus.{item};", []) == expected
        )


def test_runner_rejects_non_enum_results():
    with pytest.raises(runner.SignalQualificationScriptError, match="QualificationStatus"):
        runner.evaluate_signal_qualification_script('return "Qualified";', [])


def test_find_node_falls_back_to_nvm(monkeypatch, tmp_path):
    fake_home = tmp_path
    node = fake_home / ".nvm" / "versions" / "node" / "v24.12.0" / "bin" / "node"
    node.parent.mkdir(parents=True)
    node.write_text("")
    monkeypatch.setattr(runner.shutil, "which", lambda _name: None)
    monkeypatch.setattr(runner.Path, "home", lambda: fake_home)
    assert runner._find_node() == str(node)
