#!/usr/bin/env python3
"""Gera o card de estatísticas do perfil GitHub (github-metrics.svg).

Substitui o lowlighter/metrics por um gerador próprio, sem dependências
externas (apenas a biblioteca padrão do Python).

Uso:
    METRICS_TOKEN=... python metrics/generate_card.py --user kelsoncm --output github-metrics.svg

Tokens (variáveis de ambiente, na ordem de preferência):
    METRICS_TOKEN  PAT clássico (read:user, read:org, repo) — vê contribuições
                   privadas, organizações privadas e repositórios privados.
    GITHUB_TOKEN   token do Actions — fallback quando o METRICS_TOKEN está
                   ausente ou inválido; vê só dados públicos.
"""

from __future__ import annotations

import argparse
import base64
import json
import os
import sys
import urllib.error
import urllib.request
from collections import Counter
from dataclasses import dataclass, field
from datetime import UTC, datetime
from html import escape
from typing import Any

API_URL = "https://api.github.com/graphql"
WIDTH = 480
PAD = 16
LANG_LIMIT = 8
LICENSE_LIMIT = 6
LICENSE_COLORS = [
    "#2f81f7",
    "#3fb950",
    "#d29922",
    "#db61a2",
    "#a371f7",
    "#f85149",
    "#6e7781",
]


class GitHubError(RuntimeError):
    """Erro retornado pela API do GitHub."""


class BadCredentials(GitHubError):
    """Token inválido, expirado ou revogado (HTTP 401)."""


@dataclass
class Stats:
    login: str
    name: str
    created_at: datetime
    avatar_data_uri: str | None
    followers: int
    contributed_to: int
    organizations: int
    commits: int
    reviews: int
    prs_opened: int
    issues_opened: int
    issues_closed: int
    yearly: list[tuple[int, int]] = field(default_factory=list)
    languages: list[tuple[str, str, int]] = field(default_factory=list)
    licenses: list[tuple[str, int]] = field(default_factory=list)


class GitHubClient:
    def __init__(self, token: str) -> None:
        self.token = token

    def query(
        self, query: str, variables: dict[str, Any] | None = None
    ) -> dict[str, Any]:
        body = json.dumps({"query": query, "variables": variables or {}}).encode()
        req = urllib.request.Request(
            API_URL,
            data=body,
            headers={
                "Authorization": f"bearer {self.token}",
                "Content-Type": "application/json",
                "User-Agent": "profile-metrics-card",
            },
        )
        try:
            with urllib.request.urlopen(req, timeout=60) as resp:
                payload: dict[str, Any] = json.load(resp)
        except urllib.error.HTTPError as exc:
            if exc.code == 401:
                raise BadCredentials(
                    "Bad credentials (HTTP 401): token inválido, expirado ou revogado"
                ) from exc
            raise GitHubError(
                f"HTTP {exc.code} da API GraphQL: {exc.read().decode(errors='replace')[:300]}"
            ) from exc
        except urllib.error.URLError as exc:
            raise GitHubError(
                f"Falha de rede ao acessar a API do GitHub: {exc.reason}"
            ) from exc
        if payload.get("errors"):
            msgs = "; ".join(e.get("message", "?") for e in payload["errors"])
            raise GitHubError(f"Erro GraphQL: {msgs}")
        return payload["data"]


USER_QUERY = """
query($login: String!) {
  user(login: $login) {
    login name createdAt avatarUrl(size: 96)
    followers { totalCount }
    repositoriesContributedTo(
      includeUserRepositories: false,
      contributionTypes: [COMMIT, ISSUE, PULL_REQUEST, REPOSITORY, PULL_REQUEST_REVIEW]
    ) { totalCount }
    organizations { totalCount }
    pullRequests { totalCount }
    issues { totalCount }
    closedIssues: issues(states: CLOSED) { totalCount }
  }
}
"""

REPOS_QUERY = """
query($login: String!, $after: String) {
  user(login: $login) {
    # inclui repositórios das organizações (onde estão os plugins Moodle/PHP e as licenças GPL)
    repositories(first: 100, after: $after, ownerAffiliations: [OWNER, ORGANIZATION_MEMBER], isFork: false) {
      pageInfo { hasNextPage endCursor }
      nodes {
        licenseInfo { spdxId name }
        languages(first: 20, orderBy: {field: SIZE, direction: DESC}) {
          edges { size node { name color } }
        }
      }
    }
  }
}
"""


def yearly_query(years: list[int]) -> str:
    parts = []
    for y in years:
        parts.append(
            f'y{y}: contributionsCollection(from: "{y}-01-01T00:00:00Z", to: "{y}-12-31T23:59:59Z") '
            "{ totalCommitContributions totalPullRequestReviewContributions "
            "contributionCalendar { totalContributions } }"
        )
    return "query($login: String!) { user(login: $login) { " + " ".join(parts) + " } }"


def fetch_avatar(url: str) -> str | None:
    """Baixa o avatar e devolve como data URI (o camo do GitHub bloqueia imagens externas em SVG)."""
    try:
        with urllib.request.urlopen(
            urllib.request.Request(url, headers={"User-Agent": "profile-metrics-card"}),
            timeout=30,
        ) as resp:
            ctype = resp.headers.get_content_type() or "image/png"
            return f"data:{ctype};base64,{base64.b64encode(resp.read()).decode()}"
    except (urllib.error.URLError, TimeoutError) as exc:
        print(
            f"aviso: não foi possível baixar o avatar ({exc}); seguindo sem ele",
            file=sys.stderr,
        )
        return None


def collect(client: GitHubClient, login: str) -> Stats:
    u = client.query(USER_QUERY, {"login": login})["user"]
    if u is None:
        raise GitHubError(f"Usuário '{login}' não encontrado")
    created = datetime.fromisoformat(u["createdAt"])
    now = datetime.now(UTC)

    years = list(range(created.year, now.year + 1))
    yd = client.query(yearly_query(years), {"login": login})["user"]
    yearly: list[tuple[int, int]] = []
    commits = reviews = 0
    for y in years:
        c = yd[f"y{y}"]
        commits += c["totalCommitContributions"]
        reviews += c["totalPullRequestReviewContributions"]
        yearly.append((y, c["contributionCalendar"]["totalContributions"]))

    lang_size: Counter[str] = Counter()
    lang_color: dict[str, str] = {}
    lic: Counter[str] = Counter()
    after: str | None = None
    while True:
        repos = client.query(REPOS_QUERY, {"login": login, "after": after})["user"][
            "repositories"
        ]
        for r in repos["nodes"]:
            li = r["licenseInfo"]
            if li is None:
                lic["No license"] += 1
            else:
                spdx = li["spdxId"]
                # NOASSERTION = arquivo de licença que o GitHub não reconhece
                lic["Custom" if not spdx or spdx == "NOASSERTION" else spdx] += 1
            for e in r["languages"]["edges"]:
                name = e["node"]["name"]
                lang_size[name] += e["size"]
                lang_color[name] = e["node"]["color"] or "#8b949e"
        if not repos["pageInfo"]["hasNextPage"]:
            break
        after = repos["pageInfo"]["endCursor"]

    total = sum(lang_size.values()) or 1
    languages = [
        (n, lang_color[n], s) for n, s in lang_size.most_common() if s / total >= 0.02
    ][:LANG_LIMIT]

    return Stats(
        login=u["login"],
        name=u["name"] or u["login"],
        created_at=created,
        avatar_data_uri=fetch_avatar(u["avatarUrl"]),
        followers=u["followers"]["totalCount"],
        contributed_to=u["repositoriesContributedTo"]["totalCount"],
        organizations=u["organizations"]["totalCount"],
        commits=commits,
        reviews=reviews,
        prs_opened=u["pullRequests"]["totalCount"],
        issues_opened=u["issues"]["totalCount"],
        issues_closed=u["closedIssues"]["totalCount"],
        yearly=yearly,
        languages=languages,
        licenses=lic.most_common(),
    )


# ---------------------------------------------------------------- SVG


def fmt(n: int) -> str:
    return f"{n:,}".replace(",", " ")


def plural(n: int, one: str, many: str) -> str:
    return f"{fmt(n)} {one if n == 1 else many}"


def years_ago(created: datetime) -> int:
    now = datetime.now(UTC)
    return (
        now.year - created.year - ((now.month, now.day) < (created.month, created.day))
    )


def section_title(y: int, text: str) -> str:
    return f'<text x="{PAD}" y="{y}" class="title">{escape(text)}</text>'


def stat_line(x: int, y: int, text: str) -> str:
    return f'<circle cx="{x + 4}" cy="{y - 4}" r="3" class="dot"/><text x="{x + 14}" y="{y}" class="txt">{escape(text)}</text>'


def stacked_bar(y: int, items: list[tuple[str, str, int]]) -> tuple[list[str], int]:
    """Barra empilhada + legenda em 2 colunas. Retorna (elementos, nova coordenada y)."""
    out: list[str] = []
    total = sum(v for _, _, v in items) or 1
    bar_w = WIDTH - 2 * PAD
    out.append(
        f'<clipPath id="clip{y}"><rect x="{PAD}" y="{y}" width="{bar_w}" height="8" rx="4"/></clipPath>'
    )
    out.append(f'<g clip-path="url(#clip{y})">')
    x = float(PAD)
    for _, color, v in items:
        w = bar_w * v / total
        out.append(
            f'<rect x="{x:.2f}" y="{y}" width="{w + 0.5:.2f}" height="8" fill="{color}"/>'
        )
        x += w
    out.append("</g>")
    y += 26
    col_w = (WIDTH - 2 * PAD) // 2
    for i, (label, color, v) in enumerate(items):
        cx = PAD + (i % 2) * col_w
        cy = y + (i // 2) * 20
        pct = 100 * v / total
        out.append(f'<circle cx="{cx + 5}" cy="{cy - 4}" r="5" fill="{color}"/>')
        out.append(
            f'<text x="{cx + 16}" y="{cy}" class="txt">{escape(label)} <tspan class="muted">{pct:.1f}%</tspan></text>'
        )
    y += ((len(items) + 1) // 2) * 20
    return out, y


def render(s: Stats) -> str:
    el: list[str] = []
    y = PAD

    # ---- Profile
    if s.avatar_data_uri:
        el.append(
            f'<clipPath id="av"><circle cx="{PAD + 20}" cy="{y + 20}" r="20"/></clipPath>'
        )
        el.append(
            f'<image href="{s.avatar_data_uri}" x="{PAD}" y="{y}" width="40" height="40" clip-path="url(#av)"/>'
        )
    el.append(f'<text x="{PAD + 52}" y="{y + 27}" class="name">{escape(s.name)}</text>')
    y += 66
    col2 = WIDTH // 2 + 4
    ago = years_ago(s.created_at)
    el.append(stat_line(PAD, y, f"Joined GitHub {plural(ago, 'year', 'years')} ago"))
    el.append(
        stat_line(
            col2,
            y,
            f"Contributed to {plural(s.contributed_to, 'repository', 'repositories')}",
        )
    )
    y += 22
    el.append(stat_line(PAD, y, f"Followed by {plural(s.followers, 'user', 'users')}"))
    el.append(
        stat_line(
            col2,
            y,
            f"Member of {plural(s.organizations, 'organization', 'organizations')}",
        )
    )
    y += 30

    # ---- Contribuições por ano
    el.append(section_title(y, "Contributions by year"))
    el.append(
        f'<text x="{WIDTH - PAD}" y="{y}" class="txt" text-anchor="end">{escape(plural(s.commits, "commit", "commits"))}</text>'
    )
    y += 12
    chart_h = 70
    n = len(s.yearly)
    maxv = max((v for _, v in s.yearly), default=0) or 1
    slot = (WIDTH - 2 * PAD) / max(n, 1)
    bw = min(slot * 0.7, 28)
    base = y + 14 + chart_h
    for i, (year, v) in enumerate(s.yearly):
        # escala raiz quadrada: um ano muito ativo não achata os demais
        h = max(chart_h * (v / maxv) ** 0.5, 1.5 if v else 0)
        cx = PAD + slot * i + slot / 2
        el.append(
            f'<rect x="{cx - bw / 2:.2f}" y="{base - h:.2f}" width="{bw:.2f}" height="{h:.2f}" rx="2" class="bar"><title>{year}: {fmt(v)}</title></rect>'
        )
        el.append(
            f'<text x="{cx:.2f}" y="{base - h - 3:.2f}" class="val">{fmt(v) if v else ""}</text>'
        )
        el.append(
            f'<text x="{cx:.2f}" y="{base + 12:.2f}" class="yr">{str(year)[2:] if n > 10 else year}</text>'
        )
    y = base + 34

    # ---- Activity
    el.append(section_title(y, "Activity"))
    y += 22
    acts = [
        plural(s.reviews, "pull request reviewed", "pull requests reviewed"),
        plural(s.prs_opened, "pull request opened", "pull requests opened"),
        plural(s.issues_opened, "issue opened", "issues opened"),
        plural(s.issues_closed, "issue resolved", "issues resolved"),
    ]
    for i, t in enumerate(acts):
        el.append(stat_line(PAD if i % 2 == 0 else col2, y, t))
        if i % 2 == 1:
            y += 22
    y += 30 if len(acts) % 2 else 8

    # ---- Most used
    if s.languages:
        el.append(section_title(y, "Most used languages"))
        parts, y = stacked_bar(y + 12, s.languages)
        el.extend(parts)
        y += 14
    if s.licenses:
        top = s.licenses[:LICENSE_LIMIT]
        rest = sum(c for _, c in s.licenses[LICENSE_LIMIT:])
        if rest:
            top.append(("Other", rest))
        items = [
            (name, LICENSE_COLORS[i % len(LICENSE_COLORS)], c)
            for i, (name, c) in enumerate(top)
        ]
        el.append(section_title(y, "Most used licenses"))
        parts, y = stacked_bar(y + 12, items)
        el.extend(parts)

    updated = datetime.now(UTC).strftime("%Y-%m-%d")
    y += 6
    el.append(f'<text x="{WIDTH - PAD}" y="{y}" class="foot">Updated {updated}</text>')
    height = y + PAD - 4

    style = """
  <style>
    .name { font: 600 20px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; fill: #0969da; }
    .title { font: 600 15px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; fill: #0969da; }
    .txt { font: 400 13px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; fill: #57606a; }
    .muted { fill: #8c959f; }
    .val { font: 400 9px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; fill: #57606a; text-anchor: middle; }
    .yr { font: 400 10px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; fill: #57606a; text-anchor: middle; }
    .foot { font: 400 10px -apple-system, BlinkMacSystemFont, 'Segoe UI', Helvetica, Arial, sans-serif; fill: #8c959f; text-anchor: end; }
    .dot { fill: #8c959f; }
    .bar { fill: #40c463; }
    @media (prefers-color-scheme: dark) {
      .name, .title { fill: #58a6ff; }
      .txt, .val, .yr { fill: #8b949e; }
      .muted, .foot { fill: #6e7681; }
      .dot { fill: #6e7681; }
      .bar { fill: #26a641; }
    }
  </style>"""
    body = "\n  ".join(el)
    return (
        f'<svg xmlns="http://www.w3.org/2000/svg" width="{WIDTH}" height="{height}" viewBox="0 0 {WIDTH} {height}" '
        f'role="img" aria-label="GitHub metrics of {escape(s.login)}">{style}\n  {body}\n</svg>\n'
    )


def tokens() -> list[tuple[str, str]]:
    out = [
        (name, os.environ[name].strip())
        for name in ("METRICS_TOKEN", "GITHUB_TOKEN")
        if os.environ.get(name, "").strip()
    ]
    if not out:
        raise SystemExit("erro: defina METRICS_TOKEN ou GITHUB_TOKEN")
    return out


def main() -> int:
    ap = argparse.ArgumentParser(
        description=__doc__, formatter_class=argparse.RawDescriptionHelpFormatter
    )
    ap.add_argument("--user", required=True, help="login do GitHub")
    ap.add_argument(
        "--output", default="github-metrics.svg", help="arquivo SVG de saída"
    )
    args = ap.parse_args()

    candidates = tokens()
    for i, (name, tok) in enumerate(candidates):
        try:
            stats = collect(GitHubClient(tok), args.user)
            break
        except BadCredentials as exc:
            if i + 1 < len(candidates):
                print(
                    f"::warning::{name}: {exc}. Usando {candidates[i + 1][0]} (só dados públicos). Renove o {name}."
                )
                continue
            print(f"::error::{name}: {exc}", file=sys.stderr)
            return 1
        except GitHubError as exc:
            print(f"::error::{exc}", file=sys.stderr)
            return 1

    with open(args.output, "w", encoding="utf-8", newline="\n") as f:
        f.write(render(stats))
    print(
        f"{args.output} gerado: {stats.commits} commits, {len(stats.yearly)} anos, {len(stats.languages)} linguagens, {len(stats.licenses)} licenças"
    )
    return 0


if __name__ == "__main__":
    sys.exit(main())
