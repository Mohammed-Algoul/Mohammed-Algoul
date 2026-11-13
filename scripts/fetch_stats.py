"""Fetch public GitHub activity for the profile card and write data/stats.json.

Runs in GitHub Actions with the built-in GITHUB_TOKEN (or an optional
STATS_TOKEN secret). Only public data is requested. The file is rewritten
only when the numbers actually change, so the repository is not spammed with
daily commits.
"""
from __future__ import annotations

import json
import os
import sys
import urllib.request
from datetime import datetime, timezone
from pathlib import Path

LOGIN = os.environ.get("GH_LOGIN", "Mohammed-Algoul")
OUT = Path(__file__).resolve().parent.parent / "data" / "stats.json"

QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    contributionsCollection {
      contributionCalendar {
        totalContributions
        weeks { firstDay contributionDays { contributionCount weekday } }
      }
    }
    repositories(first: 100, after: $after, ownerAffiliations: OWNER, privacy: PUBLIC, isFork: false) {
      pageInfo { hasNextPage endCursor }
      nodes { name primaryLanguage { name } }
    }
  }
}"""


def gql(variables: dict) -> dict:
    token = os.environ["GITHUB_TOKEN"]
    req = urllib.request.Request(
        "https://api.github.com/graphql",
        data=json.dumps({"query": QUERY, "variables": variables}).encode(),
        headers={"Authorization": f"bearer {token}", "Content-Type": "application/json",
                 "User-Agent": "profile-stats-card"},
    )
    with urllib.request.urlopen(req, timeout=30) as resp:
        payload = json.load(resp)
    if payload.get("errors"):
        sys.exit(f"GraphQL error: {payload['errors']}")
    return payload["data"]["user"]


def main() -> None:
    after, repos, user = None, [], None
    while True:
        user = gql({"login": LOGIN, "after": after})
        page = user["repositories"]
        repos += page["nodes"]
        if not page["pageInfo"]["hasNextPage"]:
            break
        after = page["pageInfo"]["endCursor"]

    # the profile repository itself is not a project
    repos = [r for r in repos if r["name"].lower() != LOGIN.lower()]
    # share of public projects by primary language (bytes are dominated by notebook outputs)
    langs: dict[str, int] = {}
    for r in repos:
        if r["primaryLanguage"]:
            name = r["primaryLanguage"]["name"]
            langs[name] = langs.get(name, 0) + 1

    cal = user["contributionsCollection"]["contributionCalendar"]
    weeks, starts, days = [], [], []
    for w in cal["weeks"]:
        row = [None] * 7
        for d in w["contributionDays"]:
            row[d["weekday"]] = d["contributionCount"]
            days.append(d["contributionCount"])
        weeks.append(row)
        starts.append(w["firstDay"])

    longest = run = 0
    for c in days:
        run = run + 1 if c > 0 else 0
        longest = max(longest, run)

    data = {
        "login": LOGIN,
        "public_repos": len(repos),
        "contributions": cal["totalContributions"],
        "active_days": sum(1 for c in days if c > 0),
        "longest_streak": longest,
        "languages": sorted(langs.items(), key=lambda kv: (-kv[1], kv[0])),
        "weeks": weeks,
        "week_starts": starts,
    }

    if OUT.exists():
        old = json.loads(OUT.read_text())
        old.pop("generated_at", None)
        if json.loads(json.dumps(data)) == old:
            print("No change in public activity; keeping existing file.")
            return
    data["generated_at"] = datetime.now(timezone.utc).isoformat(timespec="seconds")
    OUT.parent.mkdir(exist_ok=True)
    OUT.write_text(json.dumps(data, indent=1) + "\n")
    print(f"Updated: {data['public_repos']} repos, {data['contributions']} contributions.")


if __name__ == "__main__":
    main()
