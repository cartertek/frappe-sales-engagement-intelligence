from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

QUALIFICATION_STATUSES = (
    "Qualified",
    "Needs Review",
    "Manually Approved",
    "Rejected",
    "Do Not Contact",
    "Unqualified",
)

DEFAULT_SIGNAL_QUALIFICATION_SCRIPT = """if (signals.some(it => it.strength == \"Strong\")) {
    return QualificationStatus.Qualified;
}
if (signals.filter(it => it.strength == \"Moderate\").length > 1) {
    return QualificationStatus.Qualified;
}
if (signals.some(it => it.strength == \"Moderate\")) {
    return QualificationStatus.NeedsReview;
}
return QualificationStatus.Unqualified;"""

NODE_RUNNER = r"""
const vm = require('vm');
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const payload = JSON.parse(input);
    const QualificationStatus = Object.freeze({
      Qualified: 'Qualified',
      NeedsReview: 'Needs Review',
      ManuallyApproved: 'Manually Approved',
      Rejected: 'Rejected',
      DoNotContact: 'Do Not Contact',
      Unqualified: 'Unqualified',
    });
    const allowedStatuses = new Set(Object.values(QualificationStatus));
    const sandbox = Object.create(null);
    sandbox.signals = Object.freeze(payload.signals.map(it => Object.freeze(it)));
    sandbox.QualificationStatus = QualificationStatus;
    const context = vm.createContext(sandbox, {
      codeGeneration: { strings: false, wasm: false },
    });
    const source = `(function () {\n${payload.script}\n})()`;
    const result = new vm.Script(source).runInContext(context, { timeout: 50 });
    if (!allowedStatuses.has(result)) {
      throw new Error('Qualification script must return a QualificationStatus value.');
    }
    process.stdout.write(JSON.stringify({ ok: true, result }));
  } catch (error) {
    process.stdout.write(JSON.stringify({ ok: false, error: String(error && error.message || error) }));
  }
});
"""


class SignalQualificationScriptError(RuntimeError):
    pass


def evaluate_signal_qualification_script(script: str, signals: list[dict[str, Any]]) -> str:
    """Evaluate a playbook JavaScript function body and return a qualification status."""
    if not str(script or "").strip():
        raise SignalQualificationScriptError("Signals Qualification Script is blank.")

    node = shutil.which("node") or shutil.which("nodejs")
    if not node:
        raise SignalQualificationScriptError("Node.js is required to evaluate Signals Qualification Scripts.")

    payload = json.dumps(
        {"script": script, "signals": signals},
        ensure_ascii=False,
        default=_json_default,
    )
    try:
        completed = subprocess.run(
            [node, "--max-old-space-size=32", "-e", NODE_RUNNER],
            input=payload,
            text=True,
            capture_output=True,
            timeout=0.5,
            check=False,
            env={"PATH": ""},
        )
    except subprocess.TimeoutExpired as exc:
        raise SignalQualificationScriptError("Script exceeded the execution time limit.") from exc

    if completed.returncode != 0:
        detail = (completed.stderr or completed.stdout or "Node.js execution failed.").strip()
        raise SignalQualificationScriptError(detail[:500])

    try:
        result = json.loads(completed.stdout)
    except json.JSONDecodeError as exc:
        raise SignalQualificationScriptError("Script runner returned an invalid response.") from exc
    if not result.get("ok"):
        raise SignalQualificationScriptError(str(result.get("error") or "Script execution failed."))
    status = result.get("result")
    if status not in QUALIFICATION_STATUSES:
        raise SignalQualificationScriptError("Script runner returned an invalid qualification status.")
    return status


def _json_default(value: Any) -> str:
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        return isoformat()
    return str(value)
