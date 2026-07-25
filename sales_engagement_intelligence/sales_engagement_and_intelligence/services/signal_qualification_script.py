from __future__ import annotations

import json
import shutil
import subprocess
from typing import Any

DEFAULT_SIGNAL_QUALIFICATION_SCRIPT = (
    'return signals.some(it => it.strength == "Strong") '
    '|| signals.filter(it => it.strength == "Moderate").length > 1;'
)

NODE_RUNNER = r'''
const vm = require('vm');
let input = '';
process.stdin.setEncoding('utf8');
process.stdin.on('data', chunk => { input += chunk; });
process.stdin.on('end', () => {
  try {
    const payload = JSON.parse(input);
    const sandbox = Object.create(null);
    sandbox.signals = Object.freeze(payload.signals.map(it => Object.freeze(it)));
    const context = vm.createContext(sandbox, {
      codeGeneration: { strings: false, wasm: false },
    });
    const source = `Boolean((function () {\n${payload.script}\n})())`;
    const result = new vm.Script(source).runInContext(context, { timeout: 50 });
    process.stdout.write(JSON.stringify({ ok: true, result: Boolean(result) }));
  } catch (error) {
    process.stdout.write(JSON.stringify({ ok: false, error: String(error && error.message || error) }));
  }
});
'''


class SignalQualificationScriptError(RuntimeError):
    pass


def evaluate_signal_qualification_script(script: str, signals: list[dict[str, Any]]) -> bool:
    """Evaluate a playbook JavaScript function body in a constrained Node VM subprocess."""
    if not str(script or "").strip():
        return False

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
    return bool(result.get("result"))


def _json_default(value: Any) -> str:
    isoformat = getattr(value, "isoformat", None)
    if callable(isoformat):
        return isoformat()
    return str(value)
