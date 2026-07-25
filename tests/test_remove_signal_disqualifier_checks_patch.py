from __future__ import annotations

import importlib
import sys
from pathlib import Path
from types import SimpleNamespace

ROOT = Path(__file__).resolve().parents[1]
if str(ROOT) not in sys.path:
    sys.path.insert(0, str(ROOT))

PATCH_MODULE = (
    "sales_engagement_intelligence.patches.v0_0_1."
    "remove_signal_disqualifier_checks"
)


class FakeDB:
    def __init__(self, *, table_exists: bool, has_column: bool):
        self._table_exists = table_exists
        self._has_column = has_column
        self.ddl_calls: list[str] = []

    def exists(self, doctype: str, name: str):
        assert doctype == "DocType"
        assert name == "SEI Signal Disqualifier Check"
        return True

    def table_exists(self, doctype: str) -> bool:
        assert doctype == "SEI Signal"
        return self._table_exists

    def has_column(self, doctype: str, fieldname: str) -> bool:
        assert doctype == "SEI Signal"
        assert fieldname == "is_strength_capped"
        return self._has_column

    def sql_ddl(self, statement: str) -> None:
        self.ddl_calls.append(statement)


class FakeFrappe(SimpleNamespace):
    def __init__(self, *, table_exists: bool, has_column: bool, legacy_exists: bool = True):
        super().__init__()
        self.db = FakeDB(table_exists=table_exists, has_column=has_column)
        self.legacy_exists = legacy_exists
        self.deleted: list[tuple] = []

        def exists(doctype: str, name: str):
            assert doctype == "DocType"
            assert name == "SEI Signal Disqualifier Check"
            return self.legacy_exists

        self.db.exists = exists

    def delete_doc(self, *args, **kwargs):
        self.deleted.append((args, kwargs))


def load_patch(fake_frappe: FakeFrappe):
    sys.modules.pop(PATCH_MODULE, None)
    sys.modules["frappe"] = fake_frappe
    return importlib.import_module(PATCH_MODULE)


def test_patch_executes_legacy_cleanup_and_schema_drop():
    fake = FakeFrappe(table_exists=True, has_column=True)
    patch = load_patch(fake)

    patch.execute()

    assert fake.deleted == [
        (
            ("DocType", "SEI Signal Disqualifier Check"),
            {"ignore_permissions": True, "force": True},
        )
    ]
    assert fake.db.ddl_calls == [
        "ALTER TABLE `tabSEI Signal` DROP COLUMN `is_strength_capped`"
    ]


def test_patch_is_safe_when_legacy_artifacts_are_already_gone():
    fake = FakeFrappe(table_exists=True, has_column=False, legacy_exists=False)
    patch = load_patch(fake)

    patch.execute()

    assert fake.deleted == []
    assert fake.db.ddl_calls == []


def test_patch_does_not_attempt_column_check_when_signal_table_is_missing():
    fake = FakeFrappe(table_exists=False, has_column=True, legacy_exists=False)
    patch = load_patch(fake)

    patch.execute()

    assert fake.deleted == []
    assert fake.db.ddl_calls == []
