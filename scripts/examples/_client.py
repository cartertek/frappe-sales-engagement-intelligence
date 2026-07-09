from __future__ import annotations

import json
import os
import urllib.parse
import urllib.request

BASE_URL = os.environ.get("FRAPPE_URL", "http://localhost:8000")
API_KEY = os.environ["FRAPPE_API_KEY"]
API_SECRET = os.environ["FRAPPE_API_SECRET"]


def call(method: str, **params):
    url = f"{BASE_URL.rstrip('/')}/api/method/{method}"
    data = urllib.parse.urlencode(
        {k: json.dumps(v) if isinstance(v, (dict, list)) else v for k, v in params.items()}
    ).encode()
    req = urllib.request.Request(
        url,
        data=data,
        headers={"Authorization": f"token {API_KEY}:{API_SECRET}"},
        method="POST",
    )
    with urllib.request.urlopen(req) as response:
        payload = json.loads(response.read().decode())
    message = payload.get("message", payload)
    print(json.dumps(message, indent=2, default=str))
    return message
