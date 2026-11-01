"""Sign in each staging QA user once and save the tokens for this CI run.

Reads QA_USERS ({"<role>": {"email", "password"}}) and optional QA_OWNER ({"email", "password"})
from the environment, signs in through STAGING_API_URL/api/auth/login (Fello-based apps), and
writes {"<role>": {"email", "token"}} to $RUNNER_TEMP/qa-tokens.json. Sets QA_TOKENS to that path
for the following steps. Tests use tokens only: no passwords, and one sign-in per role per run
(the apps allow 10 sign-ins a minute). Never prints a password or a token.
"""
import json
import os
import sys
import time
import urllib.error
import urllib.request

users = json.loads(os.environ.get("QA_USERS") or "{}")
if os.environ.get("QA_OWNER"):
    users["owner"] = json.loads(os.environ["QA_OWNER"])
if not users:
    print("No QA_USERS secret: signed-in tests will be skipped.")
    sys.exit(0)

base = os.environ["STAGING_API_URL"].rstrip("/")
tokens, failed = {}, []
for role, user in sorted(users.items()):
    body = json.dumps({"email": user["email"], "password": user["password"]}).encode()
    req = urllib.request.Request(f"{base}/api/auth/login", data=body, method="POST",
                                 headers={"Content-Type": "application/json"})
    # The apps allow 10 sign-ins a minute, counted for everyone behind the proxy, so runs
    # that start together can hit 429: wait for the next minute and try again.
    for attempt in range(3):
        try:
            with urllib.request.urlopen(req, timeout=30) as r:
                token = json.load(r)["access_token"]
            break
        except urllib.error.HTTPError as e:
            if e.code == 429 and attempt < 2:
                time.sleep(61)
                continue
            token, err = None, e.code
            break
        except (urllib.error.URLError, KeyError, ValueError) as e:
            token, err = None, type(e).__name__
            break
    if token is None:
        failed.append(f"{role} ({err})")
        continue
    print(f"::add-mask::{token}")
    tokens[role] = {"email": user["email"], "token": token}

path = os.path.join(os.environ.get("RUNNER_TEMP", "/tmp"), "qa-tokens.json")
with open(os.open(path, os.O_WRONLY | os.O_CREAT | os.O_TRUNC, 0o600), "w") as f:
    json.dump(tokens, f)
with open(os.environ["GITHUB_ENV"], "a") as f:
    f.write(f"QA_TOKENS={path}\n")
print(f"Signed in: {', '.join(sorted(tokens)) or 'none'}")
if failed:
    print(f"::warning::Could not sign in: {', '.join(failed)}")
