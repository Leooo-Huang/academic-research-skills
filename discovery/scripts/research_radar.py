#!/usr/bin/env python3
"""
Research Radar — Academic paper discovery engine for discovery skill.

Modes:
  search   (default) Multi-source search: Semantic Scholar + arXiv + HuggingFace + GitHub
  verify   Verify arXiv paper IDs by fetching their abstract pages
  expand   Citation expansion via Semantic Scholar references/citations API

Usage:
  python research_radar.py --mode search --query "robot motion retargeting" --output-json
  python research_radar.py --mode search --days 30 --source all
  python research_radar.py --mode verify --arxiv-ids "2510.02252,2402.16796" --output-json
  python research_radar.py --mode expand --s2-ids "abc123,def456" --output-json
  python research_radar.py --quick                    # arXiv only, 3 days, markdown

Output:
  --output-json    JSON to stdout (progress to stderr). For programmatic consumption.
  (default)        Markdown report appended to community/weekly_signals.md

Dependencies:
  pip install requests arxiv huggingface-hub
"""

import argparse
import io
import json
import os
import re
import sys
import time
from datetime import datetime, timedelta, timezone
from pathlib import Path
from urllib.parse import quote_plus

# Windows terminal encoding fix
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding="utf-8", errors="replace")
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding="utf-8", errors="replace")

# ── Dependency check ───────────────────────────────────────
# If core dependency (requests) is missing, output clean JSON error and exit
# so the discovery skill can catch it and fall back to WebFetch gracefully.
try:
    import requests as _requests_check  # noqa: F401
except ImportError:
    _err = {
        "status": "error",
        "errors": ["Missing dependency: requests. Run: pip install requests arxiv huggingface-hub"],
        "papers": [],
        "metadata": {},
    }
    if "--output-json" in sys.argv:
        json.dump(_err, sys.stdout, ensure_ascii=False)
        sys.stdout.write("\n")
    else:
        print("ERROR: 'requests' package not installed.", file=sys.stderr)
        print("  Run: pip install requests arxiv huggingface-hub", file=sys.stderr)
    sys.exit(1)

# ── Paths ──────────────────────────────────────────────────
SCRIPT_DIR = Path(__file__).resolve().parent
SKILL_ROOT = SCRIPT_DIR.parent
DEFAULT_CONFIG = {
    "keywords": [
        "robot motion retargeting",
        "humanoid whole-body control",
        "human to robot imitation learning",
        "embodied AI foundation model",
        "robot teleoperation",
    ],
    "arxiv_categories": ["cs.RO", "cs.AI", "cs.LG", "cs.CV"],
    "github_topics": ["robot learning", "embodied AI", "humanoid robot"],
}

# ── S2 API helpers ─────────────────────────────────────────

S2_BASE = "https://api.semanticscholar.org/graph/v1"
S2_FIELDS = "title,abstract,authors,year,citationCount,venue,publicationDate,externalIds"


def _log(msg: str):
    """Progress messages to stderr (never pollutes JSON stdout)."""
    print(msg, file=sys.stderr)


def _s2_headers() -> dict:
    headers = {"Accept": "application/json"}
    key = os.environ.get("S2_API_KEY")
    if key:
        headers["x-api-key"] = key
    return headers


def _s2_request(url: str, params: dict | None = None, max_retries: int = 3) -> dict | None:
    """S2 API request with exponential backoff on 429."""
    import requests

    headers = _s2_headers()
    for attempt in range(max_retries):
        try:
            resp = requests.get(url, params=params, headers=headers, timeout=20)
            if resp.status_code == 200:
                return resp.json()
            if resp.status_code == 429:
                wait = min(10 * (2 ** attempt), 120)
                _log(f"  S2 rate limited (429), waiting {wait}s (attempt {attempt+1}/{max_retries})...")
                time.sleep(wait)
                continue
            _log(f"  S2 HTTP {resp.status_code}: {resp.text[:200]}")
            return None
        except requests.Timeout:
            _log(f"  S2 timeout (attempt {attempt+1}/{max_retries})")
            time.sleep(5)
        except Exception as e:
            _log(f"  S2 error: {e}")
            return None
    _log("  S2 all retries exhausted")
    return None


def _parse_s2_paper(paper: dict) -> dict:
    """Extract structured data from an S2 API paper result."""
    ext = paper.get("externalIds") or {}
    authors_raw = paper.get("authors") or []
    return {
        "s2_id": paper.get("paperId", ""),
        "arxiv_id": ext.get("ArXiv"),
        "doi": ext.get("DOI"),
        "title": (paper.get("title") or "").replace("\n", " "),
        "authors": [a.get("name", "") for a in authors_raw],
        "year": paper.get("year"),
        "date": paper.get("publicationDate") or "",
        "abstract": (paper.get("abstract") or ""),
        "citation_count": paper.get("citationCount") or 0,
        "venue": paper.get("venue") or "",
        "url": f"https://arxiv.org/abs/{ext['ArXiv']}" if ext.get("ArXiv") else f"https://www.semanticscholar.org/paper/{paper.get('paperId', '')}",
        "source": "semantic_scholar",
        "verified": False,
    }


# ── MODE: search ───────────────────────────────────────────

def search_semantic_scholar(keywords: list[str], days: int = 30) -> list[dict]:
    """Query S2 API for each keyword with rate-controlled requests."""
    _log(f"  Scanning Semantic Scholar ({len(keywords)} queries, last {days} days)...")
    cutoff_year = datetime.now().year
    all_papers = []
    seen_ids = set()

    for i, kw in enumerate(keywords):
        _log(f"    Q{i+1}/{len(keywords)}: {kw}")
        if i > 0:
            time.sleep(1.5)  # rate control between queries

        data = _s2_request(
            f"{S2_BASE}/paper/search",
            params={
                "query": kw,
                "year": f"{cutoff_year - 2}-{cutoff_year}",
                "fields": S2_FIELDS,
                "limit": 100,
            },
        )
        if not data:
            continue

        for paper in data.get("data") or []:
            pid = paper.get("paperId", "")
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)

            parsed = _parse_s2_paper(paper)

            # Date filter
            if parsed["date"]:
                try:
                    pub_dt = datetime.strptime(parsed["date"], "%Y-%m-%d")
                    if pub_dt < datetime.now() - timedelta(days=days):
                        continue
                except (ValueError, TypeError):
                    pass

            all_papers.append(parsed)

    # Also run publicationDate:desc for recency
    _log(f"    Recency sweep: {keywords[0] if keywords else ''}...")
    time.sleep(1.5)
    data = _s2_request(
        f"{S2_BASE}/paper/search",
        params={
            "query": keywords[0] if keywords else "",
            "fields": S2_FIELDS,
            "sort": "publicationDate:desc",
            "limit": 50,
        },
    )
    if data:
        for paper in data.get("data") or []:
            pid = paper.get("paperId", "")
            if not pid or pid in seen_ids:
                continue
            seen_ids.add(pid)
            all_papers.append(_parse_s2_paper(paper))

    all_papers.sort(key=lambda x: x.get("citation_count", 0), reverse=True)
    _log(f"  Semantic Scholar: {len(all_papers)} papers found")
    return all_papers


def search_arxiv(keywords: list[str], days: int = 7) -> list[dict]:
    """Query arXiv API for recent papers."""
    try:
        import arxiv
    except ImportError:
        _log("  [skip] arxiv package not installed (pip install arxiv)")
        return []

    _log(f"  Scanning arXiv (last {days} days)...")
    cutoff = datetime.now(timezone.utc) - timedelta(days=days)
    all_results = []
    seen_ids = set()

    client = arxiv.Client()
    for kw in keywords:
        try:
            search = arxiv.Search(query=kw, max_results=30, sort_by=arxiv.SortCriterion.SubmittedDate)
            for result in client.results(search):
                if result.published.replace(tzinfo=timezone.utc) < cutoff:
                    continue
                paper_id = result.entry_id.split("/")[-1]
                if paper_id in seen_ids:
                    continue
                seen_ids.add(paper_id)
                # Extract clean arXiv ID (remove version suffix like v1, v2)
                clean_id = re.sub(r"v\d+$", "", paper_id)
                all_results.append({
                    "s2_id": "",
                    "arxiv_id": clean_id,
                    "doi": None,
                    "title": result.title.replace("\n", " "),
                    "authors": [a.name for a in result.authors],
                    "year": result.published.year,
                    "date": result.published.strftime("%Y-%m-%d"),
                    "abstract": result.summary.replace("\n", " "),
                    "citation_count": 0,
                    "venue": "",
                    "url": result.entry_id,
                    "categories": list(result.categories),
                    "source": "arxiv",
                    "verified": True,  # arXiv API returns verified data
                })
        except Exception as e:
            _log(f"    arXiv query error ({kw}): {e}")

    all_results.sort(key=lambda x: x["date"], reverse=True)
    _log(f"  arXiv: {len(all_results)} papers found")
    return all_results


def search_huggingface() -> list[dict]:
    """Scan HuggingFace trending papers."""
    results = []
    try:
        import requests
        _log("  Scanning HuggingFace Trending Papers...")
        resp = requests.get("https://huggingface.co/api/daily_papers", timeout=15)
        if resp.status_code == 200:
            for p in resp.json():
                title = p.get("title", "") or (p.get("paper") or {}).get("title", "")
                if any(kw in title.lower() for kw in ["robot", "embodied", "manipulation", "grasp", "vla", "humanoid", "retarget"]):
                    paper_obj = p.get("paper") or {}
                    results.append({
                        "s2_id": "",
                        "arxiv_id": paper_obj.get("id", ""),
                        "doi": None,
                        "title": title.replace("\n", " "),
                        "authors": [],
                        "year": None,
                        "date": p.get("publishedAt", "")[:10],
                        "abstract": "",
                        "citation_count": 0,
                        "venue": "",
                        "url": f"https://huggingface.co/papers/{paper_obj.get('id', '')}",
                        "upvotes": paper_obj.get("upvotes", 0),
                        "source": "huggingface",
                        "verified": False,
                    })
            _log(f"  HuggingFace: {len(results)} robot-related papers")
    except Exception as e:
        _log(f"  HuggingFace error: {e}")
    return results


def search_github(topics: list[str], days: int = 30) -> list[dict]:
    """Query GitHub trending repos."""
    try:
        import requests
    except ImportError:
        return []

    _log(f"  Scanning GitHub Trending (last {days} days)...")
    cutoff = (datetime.now() - timedelta(days=days)).strftime("%Y-%m-%d")
    results = []
    seen = set()

    for topic in topics:
        try:
            resp = requests.get(
                "https://api.github.com/search/repositories",
                params={"q": f"{topic} created:>{cutoff}", "sort": "stars", "order": "desc", "per_page": 10},
                headers={"Accept": "application/vnd.github.v3+json"},
                timeout=15,
            )
            if resp.status_code == 200:
                for repo in resp.json().get("items", []):
                    name = repo["full_name"]
                    if name not in seen:
                        seen.add(name)
                        results.append({
                            "title": name,
                            "description": (repo.get("description") or "")[:200],
                            "stars": repo["stargazers_count"],
                            "url": repo["html_url"],
                            "date": repo["created_at"][:10],
                            "language": repo.get("language", ""),
                            "source": "github",
                        })
            elif resp.status_code == 403:
                _log("  GitHub rate limit, skipping remaining")
                break
        except Exception as e:
            _log(f"  GitHub error ({topic}): {e}")

    results.sort(key=lambda x: x.get("stars", 0), reverse=True)
    _log(f"  GitHub: {len(results)} repos found")
    return results[:20]


def run_search(keywords: list[str], github_topics: list[str], days: int, source: str) -> dict:
    """Run search mode. Returns structured result dict."""
    arxiv_papers = []
    ss_papers = []
    hf_results = []
    gh_repos = []

    if source in ("all", "semantic"):
        ss_papers = search_semantic_scholar(keywords, days=days)
    if source in ("all", "arxiv"):
        arxiv_papers = search_arxiv(keywords, days=min(days, 30))
    if source in ("all", "huggingface"):
        hf_results = search_huggingface()
    if source in ("all", "github"):
        gh_repos = search_github(github_topics, days=days)

    # Merge papers, deduplicate by arxiv_id
    all_papers = []
    seen_arxiv = set()
    seen_s2 = set()

    # S2 first (more metadata)
    for p in ss_papers:
        aid = p.get("arxiv_id")
        sid = p.get("s2_id")
        if aid and aid in seen_arxiv:
            continue
        if sid and sid in seen_s2:
            continue
        if aid:
            seen_arxiv.add(aid)
        if sid:
            seen_s2.add(sid)
        all_papers.append(p)

    # Then arXiv (catches newer papers)
    for p in arxiv_papers:
        aid = p.get("arxiv_id")
        if aid and aid in seen_arxiv:
            continue
        if aid:
            seen_arxiv.add(aid)
        all_papers.append(p)

    # Then HF
    for p in hf_results:
        aid = p.get("arxiv_id")
        if aid and aid in seen_arxiv:
            continue
        if aid:
            seen_arxiv.add(aid)
        all_papers.append(p)

    return {
        "status": "success",
        "mode": "search",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "errors": [],
        "papers": all_papers,
        "github_repos": gh_repos,
        "metadata": {
            "keywords": keywords,
            "days": days,
            "source": source,
            "counts": {
                "semantic_scholar": len(ss_papers),
                "arxiv": len(arxiv_papers),
                "huggingface": len(hf_results),
                "github": len(gh_repos),
                "total_deduplicated": len(all_papers),
            },
        },
    }


# ── MODE: verify ──────────────────────────────────────────

def verify_arxiv_ids(arxiv_ids: list[str]) -> dict:
    """Verify arXiv papers by fetching their abstract pages."""
    import requests

    _log(f"  Verifying {len(arxiv_ids)} arXiv papers...")
    results = []
    errors = []

    for i, aid in enumerate(arxiv_ids):
        aid = aid.strip()
        if not aid:
            continue
        if i > 0:
            time.sleep(0.5)  # polite rate limiting for arXiv

        url = f"https://arxiv.org/abs/{aid}"
        _log(f"    [{i+1}/{len(arxiv_ids)}] {aid}...")

        try:
            resp = requests.get(url, timeout=15, headers={"User-Agent": "research-radar/1.0"})
            if resp.status_code != 200:
                results.append({"arxiv_id": aid, "verified": False, "reason": f"HTTP {resp.status_code}"})
                continue

            html = resp.text

            # Check for error pages
            if "arXiv Error" in html or "404" in html[:500]:
                results.append({"arxiv_id": aid, "verified": False, "reason": "arXiv error page"})
                continue

            # Extract title
            title_match = re.search(r'<meta name="citation_title" content="([^"]+)"', html)
            title = title_match.group(1) if title_match else ""

            # Extract authors
            author_matches = re.findall(r'<meta name="citation_author" content="([^"]+)"', html)
            authors = author_matches if author_matches else []

            # Extract date
            date_match = re.search(r'<meta name="citation_date" content="([^"]+)"', html)
            date = date_match.group(1) if date_match else ""

            # Extract abstract
            abs_match = re.search(r'<blockquote class="abstract[^"]*">\s*<span class="descriptor">Abstract:</span>\s*(.*?)</blockquote>', html, re.DOTALL)
            abstract = abs_match.group(1).strip().replace("\n", " ") if abs_match else ""

            # Extract categories
            cat_match = re.search(r'<span class="primary-subject">([^<]+)</span>', html)
            categories = cat_match.group(1) if cat_match else ""

            # Extract DOI if present
            doi_match = re.search(r'<meta name="citation_doi" content="([^"]+)"', html)
            doi = doi_match.group(1) if doi_match else None

            if not title or not abstract:
                results.append({"arxiv_id": aid, "verified": False, "reason": "Missing title or abstract"})
                continue

            results.append({
                "arxiv_id": aid,
                "verified": True,
                "title": title,
                "authors": authors,
                "date": date,
                "abstract": abstract,
                "categories": categories,
                "doi": doi,
                "url": url,
                "source": "arxiv",
            })

        except requests.Timeout:
            results.append({"arxiv_id": aid, "verified": False, "reason": "timeout"})
            errors.append(f"Timeout: {aid}")
        except Exception as e:
            results.append({"arxiv_id": aid, "verified": False, "reason": str(e)})
            errors.append(f"Error: {aid}: {e}")

    verified_count = sum(1 for r in results if r.get("verified"))
    _log(f"  Verification complete: {verified_count}/{len(results)} verified")

    return {
        "status": "success" if not errors else "partial",
        "mode": "verify",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "errors": errors,
        "papers": results,
        "metadata": {
            "total": len(results),
            "verified": verified_count,
            "failed": len(results) - verified_count,
        },
    }


# ── MODE: expand ──────────────────────────────────────────

def expand_citations(s2_ids: list[str], direction: str = "both") -> dict:
    """Expand corpus via S2 citation graph."""
    _log(f"  Expanding citations for {len(s2_ids)} papers (direction={direction})...")
    all_new = []
    errors = []
    seen = set(s2_ids)

    for i, sid in enumerate(s2_ids):
        sid = sid.strip()
        if not sid:
            continue

        endpoints = []
        if direction in ("both", "references"):
            endpoints.append(("references", f"{S2_BASE}/paper/{sid}/references"))
        if direction in ("both", "citations"):
            endpoints.append(("citations", f"{S2_BASE}/paper/{sid}/citations"))

        for rel_type, url in endpoints:
            if i > 0 or rel_type == "citations":
                time.sleep(1.5)

            _log(f"    [{i+1}/{len(s2_ids)}] {rel_type} of {sid[:12]}...")
            data = _s2_request(url, params={"fields": S2_FIELDS, "limit": 50})
            if not data:
                errors.append(f"Failed to fetch {rel_type} for {sid}")
                continue

            items = data.get("data") or []
            for item in items:
                cited = item.get("citedPaper") or item.get("citingPaper") or {}
                pid = cited.get("paperId", "")
                if not pid or pid in seen:
                    continue
                seen.add(pid)
                parsed = _parse_s2_paper(cited)
                parsed["expansion_source"] = sid
                parsed["expansion_type"] = rel_type
                all_new.append(parsed)

    _log(f"  Expansion complete: {len(all_new)} new candidates")
    return {
        "status": "success" if not errors else "partial",
        "mode": "expand",
        "timestamp": datetime.now(timezone.utc).isoformat(),
        "errors": errors,
        "papers": all_new,
        "metadata": {
            "seed_papers": len(s2_ids),
            "direction": direction,
            "new_candidates": len(all_new),
        },
    }


# ── Markdown report (legacy, kept for standalone use) ─────

def generate_markdown_report(search_result: dict) -> str:
    """Generate Markdown report from search results."""
    now = datetime.now().strftime("%Y-%m-%d %H:%M")
    papers = search_result.get("papers", [])
    repos = search_result.get("github_repos", [])
    counts = search_result.get("metadata", {}).get("counts", {})

    lines = [f"\n---\n", f"## Scan: {now}\n"]

    # Papers by source
    for src_name, src_key in [("Semantic Scholar", "semantic_scholar"), ("arXiv", "arxiv"), ("HuggingFace", "huggingface")]:
        src_papers = [p for p in papers if p.get("source") == src_key]
        if not src_papers:
            continue
        lines.append(f"### {src_name} ({len(src_papers)} papers)\n")
        for p in src_papers[:15]:
            cites = p.get("citation_count", 0)
            venue = p.get("venue", "")
            cite_str = f" [{cites} cites]" if cites else ""
            venue_str = f" | {venue}" if venue else ""
            auths = ", ".join(p.get("authors", [])[:3])
            if len(p.get("authors", [])) > 3:
                auths += "..."
            lines.append(f"- **{p['title']}**{cite_str}{venue_str}")
            lines.append(f"  {auths} | {p.get('date', '')}")
            lines.append(f"  {p.get('url', '')}\n")

    # GitHub
    if repos:
        lines.append(f"### GitHub ({len(repos)} repos)\n")
        for r in repos[:10]:
            lines.append(f"- **{r['title']}** [stars: {r.get('stars', 0)}]")
            if r.get("description"):
                lines.append(f"  {r['description']}")
            lines.append(f"  {r['url']}\n")

    # Stats
    lines.append("### Stats\n")
    lines.append("| Source | Count |")
    lines.append("|--------|-------|")
    for k, v in counts.items():
        lines.append(f"| {k} | {v} |")
    lines.append("")

    return "\n".join(lines)


# ── Main ──────────────────────────────────────────────────

def main():
    parser = argparse.ArgumentParser(description="Research Radar — Academic paper discovery engine")
    parser.add_argument("--mode", choices=["search", "verify", "expand"], default="search")
    parser.add_argument("--days", type=int, default=30, help="Lookback window in days (default: 30)")
    parser.add_argument("--quick", action="store_true", help="Quick mode: arXiv only, 3 days")
    parser.add_argument("--source", choices=["arxiv", "semantic", "huggingface", "github", "all"], default="all")
    parser.add_argument("--query", type=str, help="Ad-hoc search query (overrides config keywords)")
    parser.add_argument("--output-json", action="store_true", help="Output JSON to stdout")
    parser.add_argument("--output-file", type=str, help="Markdown output file path")
    # Verify mode args
    parser.add_argument("--arxiv-ids", type=str, help="Comma-separated arXiv IDs for verify mode")
    # Expand mode args
    parser.add_argument("--s2-ids", type=str, help="Comma-separated S2 paper IDs for expand mode")
    parser.add_argument("--direction", choices=["both", "references", "citations"], default="both")

    args = parser.parse_args()

    if args.quick:
        args.days = 3
        args.source = "arxiv"

    # Determine keywords
    keywords = DEFAULT_CONFIG["keywords"]
    if args.query:
        keywords = [args.query]

    github_topics = DEFAULT_CONFIG["github_topics"]

    # Route to mode
    if args.mode == "search":
        _log(f"Research Radar — search mode (days={args.days}, source={args.source})")
        result = run_search(keywords, github_topics, args.days, args.source)

    elif args.mode == "verify":
        if not args.arxiv_ids:
            _log("Error: --arxiv-ids required for verify mode")
            sys.exit(1)
        ids = [x.strip() for x in args.arxiv_ids.split(",") if x.strip()]
        result = verify_arxiv_ids(ids)

    elif args.mode == "expand":
        if not args.s2_ids:
            _log("Error: --s2-ids required for expand mode")
            sys.exit(1)
        ids = [x.strip() for x in args.s2_ids.split(",") if x.strip()]
        result = expand_citations(ids, args.direction)

    else:
        _log(f"Unknown mode: {args.mode}")
        sys.exit(1)

    # Output
    if args.output_json:
        json.dump(result, sys.stdout, ensure_ascii=False, indent=2, default=str)
        sys.stdout.write("\n")
    else:
        # Markdown report (search mode only)
        if args.mode == "search":
            report = generate_markdown_report(result)
            output_path = Path(args.output_file) if args.output_file else Path.cwd() / "community" / "weekly_signals.md"
            output_path.parent.mkdir(parents=True, exist_ok=True)
            header_needed = not output_path.exists()
            with open(output_path, "a", encoding="utf-8") as f:
                if header_needed:
                    f.write("# Research Radar\n\n> Auto-generated trend signals.\n")
                f.write(report)
            _log(f"Report appended to {output_path}")
        else:
            # Non-search modes always output JSON
            json.dump(result, sys.stdout, ensure_ascii=False, indent=2, default=str)
            sys.stdout.write("\n")

    total = len(result.get("papers", []))
    _log(f"Done. {total} papers processed.")


if __name__ == "__main__":
    main()
