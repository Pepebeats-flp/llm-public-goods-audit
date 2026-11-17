"""Client for the OpenCode Go inference API (OpenAI-compatible chat completions).

The API key is read at call time from the OPENCODE_API_KEY environment variable or from
OpenCode's own auth file. It is never written to logs or data files.

Etiquette required by the provider's documentation: own user agent, stable session id in
the `x-opencode-session` header. Requests are sequential and paced.
"""
import json
import os
import re
import time
import urllib.error
import urllib.request

BASE_URL = "https://opencode.ai/inference/go/openai/v1"
USER_AGENT = "llm-public-goods-study/0.1 (research script; sequential, low volume)"
_AUTH_FILE = os.path.expanduser("~/.local/share/opencode/auth.json")


def _key():
    key = os.environ.get("OPENCODE_API_KEY")
    if key:
        return key
    with open(_AUTH_FILE) as f:
        return json.load(f)["opencode-go"]["key"]


class Client:
    def __init__(self, session_id, min_interval=1.5, timeout=180):
        self.session_id = session_id
        self.min_interval = min_interval
        self.timeout = timeout
        self._last = 0.0

    def chat(self, model, prompt, temperature=None, reasoning_effort=None, max_tokens=None, extra=None):
        """One user message, one completion. Returns a dict; never raises on HTTP errors."""
        body = {"model": model, "messages": [{"role": "user", "content": prompt}]}
        if temperature is not None:
            body["temperature"] = temperature
        if reasoning_effort is not None:
            body["reasoning_effort"] = reasoning_effort
        if max_tokens is not None:
            body["max_tokens"] = max_tokens
        if extra:
            body.update(extra)
        wait = self.min_interval - (time.monotonic() - self._last)
        if wait > 0:
            time.sleep(wait)
        req = urllib.request.Request(
            BASE_URL + "/chat/completions",
            data=json.dumps(body).encode(),
            headers={
                "Authorization": "Bearer " + _key(),
                "Content-Type": "application/json",
                "User-Agent": USER_AGENT,
                "x-opencode-session": self.session_id,
            },
        )
        t0 = time.monotonic()  # monotonic: the wall clock can step backwards (seen under WSL)
        out = {"model": model, "request": {k: v for k, v in body.items() if k != "messages"}}
        try:
            with urllib.request.urlopen(req, timeout=self.timeout) as resp:
                data = json.load(resp)
            msg = (data.get("choices") or [{}])[0].get("message", {}) or {}
            out.update(
                ok=True,
                text=msg.get("content") or "",
                reasoning_text=msg.get("reasoning_content") or msg.get("reasoning") or "",
                finish_reason=(data.get("choices") or [{}])[0].get("finish_reason"),
                usage=data.get("usage"),
                served_model=data.get("model"),
                provider_meta=data.get("opencode"),
            )
        except urllib.error.HTTPError as e:
            out.update(ok=False, http_status=e.code, error=e.read().decode("utf-8", "replace")[:600])
        except Exception as e:  # timeouts, connection errors
            out.update(ok=False, http_status=None, error=f"{type(e).__name__}: {e}"[:600])
        self._last = time.monotonic()
        out["latency_s"] = round(self._last - t0, 3)
        return out


_OBJ = re.compile(r"\{[^{}]*\}")


def parse_json_field(text, field):
    """Return the value of `field` from the last JSON object in `text`, or None.

    No repair is attempted: if there is no parseable object with that field, the output
    is invalid and is recorded as such.
    """
    for candidate in reversed(_OBJ.findall(text or "")):
        try:
            obj = json.loads(candidate)
        except json.JSONDecodeError:
            continue
        if isinstance(obj, dict) and field in obj:
            return obj[field]
    return None


def parse_amount(text, endowment):
    """Integer amount in [0, endowment], or None if the output is invalid."""
    v = parse_json_field(text, "amount")
    if isinstance(v, bool) or v is None:
        return None
    if isinstance(v, float) and v.is_integer():
        v = int(v)
    if isinstance(v, int) and 0 <= v <= endowment:
        return v
    return None
