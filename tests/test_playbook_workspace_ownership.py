import json
from pathlib import Path

SIDEBAR_DIR = Path("sales_engagement_intelligence/workspace_sidebar")


def _playbook_sidebar_owners() -> list[str]:
    owners = []
    for path in SIDEBAR_DIR.glob("*.json"):
        data = json.loads(path.read_text())
        if any(
            item.get("type") == "Link" and item.get("link_to") == "SEI Playbook"
            for item in data.get("items", [])
        ):
            owners.append(data["name"])
    return sorted(owners)


def test_playbook_has_single_canonical_workspace_sidebar():
    assert _playbook_sidebar_owners() == ["Prospecting"]
