import os
import re
import requests
from datetime import datetime, timezone

TOKEN = os.environ["MOODLE_TOKEN"]
README_PATH = os.environ.get("README_PATH", "README.md")
PLUGINS = [p.strip() for p in os.environ["MOODLE_PLUGINS"].split(",") if p.strip()]

resp = requests.post(
    "https://moodle.org/webservice/rest/server.php",
    data={
        "wstoken": TOKEN,
        "wsfunction": "local_plugins_get_maintained_plugins",
        "moodlewsrestformat": "json",
    },
    headers={
        "User-Agent": "kelsoncm-readme-moodle-stats/1.0",
        "Accept": "application/json",
    },
    timeout=30,
)

if resp.status_code != 200:
    raise SystemExit(f"HTTP {resp.status_code}: {resp.text[:1000]}")

data = resp.json()

if isinstance(data, dict) and data.get("exception"):
    raise SystemExit(f"{data.get('errorcode')}: {data.get('message')}")

if not isinstance(data, list):
    raise SystemExit(f"Unexpected API response: {data}")

plugins_by_frankenstyle = {p.get("frankenstyle"): p for p in data}

def human_age_from_timestamp(ts: int) -> str:
    dt = datetime.fromtimestamp(ts, tz=timezone.utc)
    now = datetime.now(timezone.utc)
    days = max((now - dt).days, 0)

    years = days // 365
    months = days // 30

    if years >= 1:
        return f"{years} year{'s' if years != 1 else ''}"
    if months >= 1:
        return f"{months} month{'s' if months != 1 else ''}"
    return f"{max(days, 1)} day{'s' if days != 1 else ''}"

rows = []
missing = []

for frankenstyle in PLUGINS:
    plugin = plugins_by_frankenstyle.get(frankenstyle)
    if not plugin:
        missing.append(frankenstyle)
        continue

    versions = plugin.get("currentversions", [])
    if versions:
        latest_version = max(versions, key=lambda v: v.get("timecreated", 0))
        oldest_supported_version = min(versions, key=lambda v: v.get("timecreated", 0))

        latest_ts = latest_version.get("timecreated")
        oldest_ts = oldest_supported_version.get("timecreated")

        latest_release = human_age_from_timestamp(latest_ts) if latest_ts else "n/a"
        oldest_supported_release = human_age_from_timestamp(oldest_ts) if oldest_ts else "n/a"
        supported_moodle = latest_version.get("supportedmoodle", "n/a")
    else:
        latest_release = "n/a"
        oldest_supported_release = "n/a"
        supported_moodle = "n/a"

    rows.append({
        "plugin": frankenstyle,
        "oldest_supported_release": oldest_supported_release,
        "latest_release": latest_release,
        "supported_moodle": supported_moodle,
        "sites": plugin.get("aggsites", 0),
        "downloads": plugin.get("aggdownloads", 0),
        "fans": plugin.get("aggfavs", 0),
    })

if missing:
    raise SystemExit(f"Plugins not found in maintained list: {', '.join(missing)}")

table_lines = [
    "| Plugin | Oldest supported release | Latest release | Supported Moodle versions | Sites | Downloads | Fans |",
    "|---|---:|---:|---|---:|---:|---:|",
]

for row in rows:
    table_lines.append(
        f"| {row['plugin']} | {row['oldest_supported_release']} | {row['latest_release']} | {row['supported_moodle']} | {row['sites']} | {row['downloads']} | {row['fans']} |"
    )

block = "<!-- moodle-plugin-stats:start -->\n" + "\n".join(table_lines) + "\n<!-- moodle-plugin-stats:end -->"

with open(README_PATH, "r", encoding="utf-8") as f:
    readme = f.read()

pattern = r"<!-- moodle-plugin-stats:start -->(.*?)<!-- moodle-plugin-stats:end -->"
if not re.search(pattern, readme, flags=re.S):
    raise SystemExit("Stats block markers not found in README")

updated = re.sub(pattern, block, readme, flags=re.S)

with open(README_PATH, "w", encoding="utf-8") as f:
    f.write(updated)