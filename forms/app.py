#!/usr/bin/env python3
"""Form endpoint for grovano.com.

Accepts the SMS opt-in submission from /messaging/signup and appends a consent
record to an append-only JSONL file. Deliberately dependency-free: the whole
point of this service is that it cannot break, because a form that will not
accept a submission fails A2P 10DLC carrier review no matter how correct the
consent language on the page is. That is what got campaign CM584c06 rejected.

The stored record is the proof of express written consent. It keeps the exact
disclosure text that was on the page at submission time, alongside the IP,
user agent and timestamp, so a record can answer "what did this person actually
agree to, and when" years later without relying on the site's git history.

Routes:
  POST /messaging/signup/submit   record a submission
  GET  /healthz                   liveness for the container healthcheck
"""

import json
import os
import re
import sys
import threading
import time
from collections import deque
from http.server import BaseHTTPRequestHandler, ThreadingHTTPServer
from urllib.parse import parse_qs

PORT = int(os.environ.get("PORT", "8080"))
DATA_DIR = os.environ.get("DATA_DIR", "/data")
LEADS = os.path.join(DATA_DIR, "leads.jsonl")

MAX_BODY = 64 * 1024          # a lead is ~2 KB; anything larger is not a lead
# Deliberately loose. Carrier reviewers submit the form several times from one
# address, and several of them can share a corporate NAT. Blocking a reviewer
# is the exact failure this service exists to prevent, so the limit only has to
# stop a bot hammering the endpoint, not police normal use.
RATE_LIMIT = 15               # submissions per IP...
RATE_WINDOW = 600             # ...per 10 minutes

THANK_YOU = "/messaging/signup/thank-you/"
SIGNUP = "/messaging/signup/"

# Fields copied verbatim into the consent record. Anything not listed is
# ignored, so a bot padding the body cannot bloat the store.
KEEP = (
    "name", "email", "phone", "property",
    "consent_language_version", "consent_page_url",
    "consent_transactional_text", "consent_marketing_text",
    "submitted_at",
)

EMAIL_RE = re.compile(r"^[^\s@]+@[^\s@]+\.[^\s@]{2,}$")

_lock = threading.Lock()
_hits = {}                    # ip -> deque[timestamp]


def digits(value):
    return re.sub(r"\D", "", value or "")


def valid(fields):
    """Return an error string, or None if the submission is acceptable."""
    if fields.get("company"):
        # Honeypot. Hidden from humans, irresistible to bots. Treated as a
        # silent success so the bot does not learn to leave it blank.
        return "honeypot"
    if len(fields.get("name", "").strip()) < 2:
        return "Please enter your full name."
    if not EMAIL_RE.match(fields.get("email", "").strip()):
        return "Please enter a valid email address."
    phone = digits(fields.get("phone")).lstrip("1")
    if len(phone) != 10:
        return "Please enter a 10-digit US mobile number."
    return None


def rate_limited(ip):
    now = time.time()
    with _lock:
        seen = _hits.setdefault(ip, deque())
        while seen and now - seen[0] > RATE_WINDOW:
            seen.popleft()
        if len(seen) >= RATE_LIMIT:
            return True
        seen.append(now)
        # Keep the table from growing without bound on a long-lived process.
        if len(_hits) > 4096:
            for stale in [k for k, v in _hits.items() if not v or now - v[-1] > RATE_WINDOW]:
                del _hits[stale]
    return False


def record(fields, ip, agent):
    row = {
        "received_at": time.strftime("%Y-%m-%dT%H:%M:%SZ", time.gmtime()),
        "ip": ip,
        "user_agent": agent,
        # Consent is stored as an explicit boolean per channel. The two are
        # never collapsed into one flag: Twilio error 30913 is precisely the
        # rule that marketing and transactional consent must stay separate.
        "sms_consent_transactional": fields.get("sms_consent_transactional") == "yes",
        "sms_consent_marketing": fields.get("sms_consent_marketing") == "yes",
    }
    for key in KEEP:
        if key in fields:
            row[key] = fields[key][:4000]

    line = json.dumps(row, ensure_ascii=False) + "\n"
    with _lock:
        with open(LEADS, "a", encoding="utf-8") as fh:
            fh.write(line)
            fh.flush()
            os.fsync(fh.fileno())
    return row


class Handler(BaseHTTPRequestHandler):
    server_version = "grovano-forms"
    sys_version = ""

    def log_message(self, fmt, *args):
        sys.stderr.write("%s %s\n" % (self.client_ip(), fmt % args))

    def client_ip(self):
        # Caddy is the only thing that can reach this container, so the
        # left-most XFF entry is the real client.
        fwd = self.headers.get("X-Forwarded-For", "")
        return fwd.split(",")[0].strip() if fwd else self.client_address[0]

    def wants_json(self):
        return "application/json" in (self.headers.get("Accept") or "")

    def send(self, code, body=b"", ctype="text/plain; charset=utf-8", extra=None):
        self.send_response(code)
        self.send_header("Content-Type", ctype)
        self.send_header("Content-Length", str(len(body)))
        self.send_header("Cache-Control", "no-store")
        self.send_header("X-Content-Type-Options", "nosniff")
        for key, value in (extra or {}).items():
            self.send_header(key, value)
        self.end_headers()
        if body:
            self.wfile.write(body)

    def ok(self):
        if self.wants_json():
            self.send(200, b'{"ok":true}', "application/json")
        else:
            self.send(303, b"", "text/plain; charset=utf-8", {"Location": THANK_YOU})

    def fail(self, code, message):
        if self.wants_json():
            body = json.dumps({"ok": False, "error": message}).encode()
            self.send(code, body, "application/json")
        else:
            page = (
                "<!doctype html><meta charset=utf-8>"
                "<title>We could not accept that submission</title>"
                "<style>body{font:16px/1.6 system-ui,sans-serif;max-width:38rem;"
                "margin:12vh auto;padding:0 1.5rem;color:#14181f}"
                "a{color:#1b4d89}</style>"
                "<h1>We could not accept that submission</h1>"
                "<p>%s</p><p><a href=\"%s\">Go back to the form</a></p>"
                % (message, SIGNUP)
            ).encode()
            self.send(code, page, "text/html; charset=utf-8")

    def do_GET(self):
        if self.path == "/healthz":
            self.send(200, b"ok")
        else:
            self.fail(405, "This address only accepts form submissions.")

    def do_POST(self):
        if self.path.rstrip("/") != "/messaging/signup/submit":
            self.fail(404, "Not found.")
            return

        try:
            length = int(self.headers.get("Content-Length") or 0)
        except ValueError:
            self.fail(400, "Malformed request.")
            return
        if length <= 0 or length > MAX_BODY:
            self.fail(400, "Malformed request.")
            return

        if rate_limited(self.client_ip()):
            self.fail(429, "Too many submissions from this connection. "
                           "Please wait a few minutes and try again.")
            return

        raw = self.rfile.read(length).decode("utf-8", "replace")
        fields = {k: v[0] for k, v in parse_qs(raw, keep_blank_values=True).items()}

        problem = valid(fields)
        if problem == "honeypot":
            self.ok()
            return
        if problem:
            self.fail(400, problem)
            return

        try:
            row = record(fields, self.client_ip(), self.headers.get("User-Agent", ""))
        except OSError as exc:
            # Never claim success we did not achieve: a lost consent record is
            # worse than a visible error, both legally and for the user.
            self.log_message("STORE FAILED: %s", exc)
            self.fail(500, "We could not save your request. Please email "
                           "support@grovano.com and we will take it directly.")
            return

        self.log_message("lead stored: tx=%s mk=%s",
                         row["sms_consent_transactional"],
                         row["sms_consent_marketing"])
        self.ok()


def main():
    os.makedirs(DATA_DIR, exist_ok=True)
    # Consent records are PII. Keep them off the world-readable default.
    if not os.path.exists(LEADS):
        with open(LEADS, "a", encoding="utf-8"):
            pass
        os.chmod(LEADS, 0o600)

    server = ThreadingHTTPServer(("0.0.0.0", PORT), Handler)
    server.daemon_threads = True
    sys.stderr.write("grovano-forms listening on :%d, storing to %s\n" % (PORT, LEADS))
    server.serve_forever()


if __name__ == "__main__":
    main()
