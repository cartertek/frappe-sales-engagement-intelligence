from __future__ import annotations

import ast
import json
import re
from pathlib import Path

ROOT = Path(__file__).resolve().parents[1]
APP = ROOT / "sales_engagement_intelligence"
MODULE = APP / "sales_engagement_and_intelligence"
DOCTYPE_ROOT = MODULE / "doctype"
PATCHES_FILE = APP / "patches.txt"

REMOVED_DOCTYPES = {
    "SEI Thesis",
    "SEI Thesis Research Arena",
    "SEI Research Arena Thesis",
}
ACTIVE_REFERENCE_ROOTS = (
    MODULE / "doctype",
    MODULE / "workspace",
    APP / "workspace_sidebar",
    APP / "hooks.py",
    APP / "fixtures",
)


def _doctype_documents() -> list[tuple[Path, dict]]:
    docs: list[tuple[Path, dict]] = []
    for path in sorted(DOCTYPE_ROOT.glob("*/*.json")):
        data = json.loads(path.read_text())
        if data.get("doctype") == "DocType":
            docs.append((path, data))
    return docs


def _controller_class_name(doctype_name: str) -> str:
    return re.sub(r"[^A-Za-z0-9]", "", doctype_name)


def _module_path(dotted: str) -> Path:
    parts = dotted.split(".")
    if parts[0] != "sales_engagement_intelligence":
        raise AssertionError(f"Not an app-local module: {dotted}")
    return ROOT.joinpath(*parts).with_suffix(".py")


def _defined_names(path: Path) -> set[str]:
    tree = ast.parse(path.read_text(), filename=str(path))
    return {
        node.name
        for node in tree.body
        if isinstance(node, (ast.ClassDef, ast.FunctionDef, ast.AsyncFunctionDef))
    }


def test_every_doctype_has_importable_controller_shape():
    failures: list[str] = []
    for json_path, doc in _doctype_documents():
        controller = json_path.with_suffix(".py")
        if not controller.exists():
            failures.append(f"{doc['name']}: missing {controller.relative_to(ROOT)}")
            continue
        try:
            names = _defined_names(controller)
        except SyntaxError as exc:
            failures.append(f"{doc['name']}: controller syntax error: {exc}")
            continue
        expected = _controller_class_name(doc["name"])
        if expected not in names:
            failures.append(
                f"{doc['name']}: controller must define class {expected} in "
                f"{controller.relative_to(ROOT)}"
            )
    assert not failures, "\n" + "\n".join(failures)


def test_every_registered_patch_module_exists_and_defines_execute():
    failures: list[str] = []
    for raw_line in PATCHES_FILE.read_text().splitlines():
        line = raw_line.strip()
        if not line or line.startswith("[") or line.startswith("#"):
            continue
        module_path = _module_path(line)
        if not module_path.exists():
            failures.append(f"{line}: missing {module_path.relative_to(ROOT)}")
            continue
        try:
            names = _defined_names(module_path)
        except SyntaxError as exc:
            failures.append(f"{line}: syntax error: {exc}")
            continue
        if "execute" not in names:
            failures.append(f"{line}: patch module does not define execute()")
    assert not failures, "\n" + "\n".join(failures)


def test_local_link_and_table_options_reference_existing_doctypes():
    local_doctypes = {doc["name"] for _, doc in _doctype_documents()}
    failures: list[str] = []
    for path, doc in _doctype_documents():
        for field in doc.get("fields", []):
            fieldtype = field.get("fieldtype")
            option = field.get("options")
            if not option or fieldtype not in {"Link", "Table", "Table MultiSelect"}:
                continue
            # All child-table options are app-owned. SEI-prefixed Link targets are app-owned.
            is_local = fieldtype in {"Table", "Table MultiSelect"} or option.startswith("SEI ")
            if is_local and option not in local_doctypes:
                failures.append(
                    f"{doc['name']}.{field.get('fieldname')}: {fieldtype} references missing DocType {option}"
                )
    assert not failures, "\n" + "\n".join(failures)


def test_internal_hook_targets_resolve_to_python_symbols():
    hooks = (APP / "hooks.py").read_text()
    targets = sorted(
        set(
            re.findall(
                r'["\'](sales_engagement_intelligence(?:\.[A-Za-z_][A-Za-z0-9_]*)+)["\']',
                hooks,
            )
        )
    )
    failures: list[str] = []
    for target in targets:
        if target.endswith((".js", ".css")):
            continue
        parts = target.split(".")
        resolved = False
        for split_at in range(len(parts), 0, -1):
            module_parts = parts[:split_at]
            remainder = parts[split_at:]
            module_file = ROOT.joinpath(*module_parts).with_suffix(".py")
            package_file = ROOT.joinpath(*module_parts, "__init__.py")
            module_path = module_file if module_file.exists() else package_file
            if not module_path.exists():
                continue
            resolved = True
            if not remainder:
                break  # A package/module reference is valid and has no callable suffix.
            if len(remainder) != 1:
                failures.append(f"{target}: nested attribute path cannot be statically resolved")
                break
            symbol = remainder[0]
            if symbol not in _defined_names(module_path):
                failures.append(f"{target}: missing symbol {symbol} in {module_path.relative_to(ROOT)}")
            break
        if not resolved:
            failures.append(f"{target}: no app-local Python module or package resolves")
    assert not failures, "\n" + "\n".join(failures)


def test_workspace_and_sidebar_doctype_links_exist():
    local_doctypes = {doc["name"] for _, doc in _doctype_documents()}
    failures: list[str] = []
    paths = list((MODULE / "workspace").rglob("*.json")) + list(
        (APP / "workspace_sidebar").rglob("*.json")
    )
    for path in sorted(paths):
        data = json.loads(path.read_text())
        for item in data.get("links", []) + data.get("items", []):
            if item.get("link_type") != "DocType":
                continue
            target = item.get("link_to")
            if target and target.startswith("SEI ") and target not in local_doctypes:
                failures.append(f"{path.relative_to(ROOT)} references missing DocType {target}")
    assert not failures, "\n" + "\n".join(failures)


def test_removed_doctypes_are_absent_from_active_runtime_surfaces():
    failures: list[str] = []
    for root in ACTIVE_REFERENCE_ROOTS:
        paths = [root] if root.is_file() else list(root.rglob("*")) if root.exists() else []
        for path in paths:
            if not path.is_file() or path.suffix not in {".py", ".json", ".js"}:
                continue
            text = path.read_text(errors="ignore")
            for removed in REMOVED_DOCTYPES:
                if removed in text:
                    failures.append(f"{path.relative_to(ROOT)} still references removed DocType {removed}")
    assert not failures, "\n" + "\n".join(failures)


def test_patches_after_thesis_replacement_do_not_reference_removed_doctypes():
    patch_lines = [
        line.strip()
        for line in PATCHES_FILE.read_text().splitlines()
        if line.strip() and not line.startswith("[") and not line.startswith("#")
    ]
    marker = "sales_engagement_intelligence.patches.v0_0_1.replace_theses_with_playbooks"
    assert marker in patch_lines, "replacement patch is not registered"
    failures: list[str] = []
    for dotted in patch_lines[patch_lines.index(marker) + 1 :]:
        path = _module_path(dotted)
        text = path.read_text()
        for removed in REMOVED_DOCTYPES:
            if removed in text:
                failures.append(f"{dotted} references removed DocType {removed}")
    assert not failures, "\n" + "\n".join(failures)


def test_removed_doctypes_are_not_loaded_through_document_api_in_patches():
    forbidden_calls = {"get_doc", "new_doc", "get_cached_doc"}
    failures: list[str] = []
    patch_lines = [
        line.strip()
        for line in PATCHES_FILE.read_text().splitlines()
        if line.strip() and not line.startswith("[") and not line.startswith("#")
    ]
    marker = "sales_engagement_intelligence.patches.v0_0_1.replace_theses_with_playbooks"
    assert marker in patch_lines, "replacement patch is not registered"
    for dotted in patch_lines[patch_lines.index(marker) :]:
        path = _module_path(dotted)
        tree = ast.parse(path.read_text(), filename=str(path))
        for node in ast.walk(tree):
            if not isinstance(node, ast.Call) or not isinstance(node.func, ast.Attribute):
                continue
            if node.func.attr not in forbidden_calls or not node.args:
                continue
            first = node.args[0]
            if isinstance(first, ast.Constant) and first.value in REMOVED_DOCTYPES:
                failures.append(
                    f"{dotted}:{node.lineno} loads removed DocType {first.value} "
                    f"through frappe.{node.func.attr}()"
                )
    assert not failures, "\n" + "\n".join(failures)


def test_after_migrate_cleans_removed_workspace_targets_before_workspace_saves():
    setup_path = APP / "setup" / "__init__.py"
    tree = ast.parse(setup_path.read_text(), filename=str(setup_path))
    after_migrate = next(
        node for node in tree.body if isinstance(node, ast.FunctionDef) and node.name == "after_migrate"
    )
    calls = [
        node.func.id
        for node in after_migrate.body
        if isinstance(node, ast.Expr)
        and isinstance(node.value, ast.Call)
        and isinstance(node.value.func, ast.Name)
        for node in [node.value]
    ]
    cleanup = "remove_stale_workspace_doctype_links"
    assert cleanup in calls
    assert calls.index(cleanup) < calls.index("ensure_milestone_5_workspace_items")

    source = setup_path.read_text()
    for removed in REMOVED_DOCTYPES:
        assert removed in source, f"workspace cleanup does not enumerate removed target {removed}"
