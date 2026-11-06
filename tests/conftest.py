# A3 CHECK probe (throwaway branch a3-check, never merged). Records WHERE a GitHub write
# credential is reachable from test code. Writes presence only, never a value.
import glob, os, pathlib, subprocess

def _probe():
    lines = []
    cfg = subprocess.run(["git", "config", "--list", "--show-origin"], capture_output=True, text=True).stdout.lower()
    lines.append("git config auth header: " + ("FOUND" if "extraheader" in cfg or "authorization" in cfg else "none"))
    for name in ("QA_BOT_TOKEN", "GH_TOKEN", "GITHUB_TOKEN", "INPUT_TOKEN"):
        lines.append(f"env {name}: " + ("FOUND" if os.environ.get(name) else "none"))
    creds = [p for p in glob.glob(os.path.expanduser("~/.git-credentials")) + glob.glob(os.path.expanduser("~/.config/gh/hosts.yml"))]
    lines.append("credential files: " + (", ".join(creds) if creds else "none"))
    found = [l for l in lines if "FOUND" in l] + ([1] if creds else [])
    lines.append("RESULT: " + ("WRITE CREDENTIAL REACHABLE" if found else "no write credential reachable"))
    out = pathlib.Path(__file__).parent / "a3-probe.txt"
    out.write_text("\n".join(lines) + "\n")
    print("\n".join(lines))

_probe()
