---
name: discovery
description: "Real-time academic paper discovery for Claude Code. Four-phase pipeline: (A) Community Intelligence — optional last30days skill integration (Reddit/X/YouTube) or WebSearch fallback (GitHub/HuggingFace/arXiv); (B) Systematic Search — Python script (research_radar.py) as primary API engine for Semantic Scholar + arXiv + HuggingFace + GitHub, with WebFetch as fallback; (C) Verification — Python script verifies arXiv pages, WebFetch as fallback; (D) Citation Expansion — Python script expands via S2 citation graph. Outputs Schema-2-compliant Bibliography with COMMUNITY_SIGNALS. Python-first design: proper rate limiting, exponential backoff, no WebFetch cache issues. Triggers on: find papers, discover papers, search arxiv, recent papers on, literature search, find literature, find me papers."
metadata:
  version: "2.1"
  last_updated: "2026-03-27"
  depends_on: "academic-pipeline (optional), deep-research (optional)"
  requires:
    bins: [python3]
    files: ["scripts/*"]
allowed-tools: Bash, WebSearch, WebFetch
---

# Discovery v2.1 — Real-time Academic Paper Discovery

Four-phase pipeline that grounds all citations in live, fetched data — eliminating bibliography_agent's reliance on training-memory citations. Achieves 50-100 verified papers by combining community intelligence signals (Phase A), Python-driven API search (Phase B), automated verification (Phase C), and citation graph expansion (Phase D).

**Design Principles**:
1. **No training-memory citations** — every paper was verified by fetching its actual web page
2. **Discard over guess** — if a paper fails verification, it is dropped; metadata is never synthesized from search snippets
3. **Schema-2 compliance** — output conforms exactly to `shared/handoff_schemas.md` Schema 2 so downstream agents need zero reformatting
4. **Community-informed search** — Phase A community signals steer Phase B queries toward currently-active research fronts
5. **Python-first API access** — `scripts/research_radar.py` handles all Semantic Scholar/arXiv API calls via Bash, with proper rate limiting and exponential backoff; WebFetch is a fallback when Python is unavailable
6. **Volume through APIs** — Semantic Scholar API returns 100+ candidates per query; citation expansion multiplies coverage further

---

## Quick Start

**Find recent papers on a topic:**
```
Find papers on vision-language models for robotic grasping
```

**With date filter:**
```
Find papers on diffusion policy for robot manipulation published after 2024-06-01
```

**With venue filter:**
```
Find ICRA 2025 papers on sim-to-real transfer for legged robots
```

**Handoff to pipeline (full workflow):**
```
I want to write a research paper on [topic]
```
→ academic-pipeline launches Stage 0 (DISCOVERY), then passes verified corpus to Stage 1

---

## Trigger Conditions

### Trigger Keywords

**English**: find papers, discover papers, search arxiv, recent papers on, literature search, find literature, find me papers, search literature, search for papers, literature discovery

### Non-Trigger Scenarios

| Scenario | Skill to Use |
|----------|-------------|
| Need deep analysis of already-found papers | `deep-research` |
| Need to write a paper | `academic-paper` |
| Need full research-to-publication pipeline | `academic-pipeline` |
| Need to verify specific citations | `deep-research` (fact-check mode) |

### Quick Mode Selection Guide

| Your Situation | Use This |
|----------------|----------|
| Starting a new research topic from scratch | `discovery` → then `academic-pipeline` |
| Already have some papers, need more | `discovery` with specific query |
| Used inside `academic-pipeline` | Triggered automatically as Stage 0 |

---

## Agent Team (1 Agent)

| # | Agent | Role | Phases |
|---|-------|------|--------|
| 1 | `discovery_agent` | Four-phase community intelligence + S2 API search + arXiv verification + citation expansion; Schema-2 output assembly | A + B + C + D |

---

## Orchestration Workflow

```
User: "Find papers on [topic]"
     |
=== Phase A: COMMUNITY INTELLIGENCE (WebSearch) ===
     |
     |-> [discovery_agent] — Community signal extraction
     |   - Path A-Primary (if last30days skill available): /last30days [topic]
     |     → covers Reddit, X/Twitter, YouTube (requires OPENAI_API_KEY)
     |   - Path A-Fallback (WebSearch only): GitHub, HuggingFace, arXiv
     |     → Twitter/Reddit not accessible via WebSearch site: operator
     |   - Extract: trending_keywords, hot_paper_ids, pain_points
     |
     |   ** Output: COMMUNITY_SIGNALS artifact **
     |   {trending_keywords: [...], hot_paper_ids: [...], pain_points: [...], signal_sources: [...]}
     |
=== Phase B: SYSTEMATIC SEARCH (Python script primary, WebFetch fallback) ===
     |
     |-> [discovery_agent] — Check Python availability
     |   Bash: python3 --version 2>/dev/null
     |   → If available: PYTHON_AVAILABLE = true (use Python primary path)
     |   → If not: PYTHON_AVAILABLE = false (use WebFetch fallback)
     |
     |-> [discovery_agent] — Semantic Scholar + arXiv + HuggingFace + GitHub
     |
     |   PRIMARY (Python available):
     |     Bash: {RADAR_CMD} \
     |       --mode search --query "[topic]" --days 30 --output-json
     |     → Parses JSON stdout: 200-400 candidates with s2_id, arxiv_id, abstract, citations
     |     → Rate limiting handled internally (exponential backoff on 429)
     |
     |   FALLBACK (no Python):
     |     WebFetch: S2 API search (existing v2.0 flow)
     |     WebSearch: arXiv site search
     |
     |-> B4: Abstract pre-filtering (in-agent logic, unchanged)
     |   → 200-400 candidates → 60-80 after pre-filtering
     |
     ** Phase B complete: candidate pool assembled **
     |
=== Phase C: VERIFICATION (Python script primary, WebFetch fallback) ===
     |
     |-> [discovery_agent] — Verify all candidate arXiv IDs
     |
     |   PRIMARY (Python available):
     |     Bash: {RADAR_CMD} \
     |       --mode verify --arxiv-ids "id1,id2,..." --output-json
     |     → Batch verification with 0.5s polite delay between requests
     |     → Returns verified: true/false for each paper with full metadata
     |
     |   FALLBACK (no Python):
     |     WebFetch: https://arxiv.org/abs/{arxiv_id} for each candidate
     |
     |   Assign relevance_score (1-10) and filter: discard score ≤ 3
     |   → Verified corpus: 30-80 papers
     |
     ** Phase C complete: verified corpus assembled **
     |
=== Phase D: CITATION EXPANSION (Python script primary, WebFetch fallback) ===
     |
     |-> [discovery_agent] — For top 10 papers by relevance_score:
     |
     |   PRIMARY (Python available):
     |     Bash: {RADAR_CMD} \
     |       --mode expand --s2-ids "id1,id2,..." --output-json
     |     → Fetches references + citations with rate limiting
     |     → Returns new candidate papers
     |
     |   FALLBACK (no Python):
     |     WebFetch: S2 references/citations endpoints
     |
     |   → Run Phase C verification on new candidates
     |   → Add verified papers to corpus
     |
     ** Phase D complete: citation-expanded corpus assembled **
     |
=== Phase E: ASSEMBLE (Schema 2 Output) ===
     |
     +-> [discovery_agent] — Build Bibliography artifact
         - Assign sequential IDs: [S01], [S02], ...
         - Rank by relevance_score (10 = highest); secondary: citationCount desc
         - Cap at 100 sources maximum
         - Assign evidence_tier and quality_tier per source_quality_hierarchy
         - Write annotation (2-3 sentences: key contribution + relevance to query)
         - Embed COMMUNITY_SIGNALS block
         - Assemble search_strategy block
         - Write coverage_assessment
         - Output Schema-2-compliant Bibliography with discovery_phases counts
```

### Checkpoint Rules

1. **Phase A minimum**: Report if no community signals found (proceed anyway — Phase B is independent)
2. **Phase B minimum**: Must collect at least 20 candidates from Semantic Scholar before entering Phase C. If fewer: try broader keywords, use fallback queries
3. **Phase C discard rule**: Papers that fail WebFetch verification are ALWAYS discarded — never synthesized from search snippet metadata
4. **Minimum output**: Final Bibliography must contain at least 10 verified sources. If fewer: report to user with explanation and ask to broaden scope or date range
5. **Maximum output**: Cap at 100 sources per run to maintain quality. If >100 candidates pass verification and scoring, select top 100 by relevance_score
6. **Date rule**: Default date filter = papers submitted or published within past 24 months. User can override with explicit date range
7. **Rate limiting**: If Semantic Scholar API returns 429 (rate limited), pause 60 seconds and retry. S2_API_KEY (optional) raises limit from 100 to 1000 req/5min

---

## Semantic Scholar API Usage

### Primary Search Endpoint

```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={ENCODED_QUERY}&fields=title,abstract,authors,year,citationCount,venue,externalIds&limit=100
```

Returns JSON array of papers. Parse `externalIds.ArXiv` for arXiv ID, `paperId` for S2 ID.

**Example query construction**:
```
Query 1 (primary topic): "vision language model robotic grasping"
Query 2 (method variant): "diffusion policy robot manipulation"
Query 3 (community-informed): "{{top trending keyword from Phase A}}"
Query 4 (recent/broad): "robot learning 2025"
```

### Citation/Reference Endpoints

```
References: https://api.semanticscholar.org/graph/v1/paper/{S2_PAPER_ID}/references?fields=title,abstract,authors,year,externalIds&limit=50
Citations:   https://api.semanticscholar.org/graph/v1/paper/{S2_PAPER_ID}/citations?fields=title,abstract,authors,year,externalIds&limit=50
```

### API Key (Optional)

**No API key required for basic use.** Free tier allows 100 requests per 5 minutes.

For extended use (1000 req/5min), set the header:
```
x-api-key: {S2_API_KEY}
```

Users can obtain a free S2_API_KEY at https://www.semanticscholar.org/product/api — fill in a 1-sentence description of use.

When running via Claude Code, the key can be passed as an environment variable. If `S2_API_KEY` is set in the environment, include it as a header in all S2 API calls.

---

## Community Intelligence (Phase A)

Phase A uses WebSearch to extract trending signals from community platforms. These signals are used to:
1. Identify emerging research fronts not yet captured in structured databases
2. Surface hot paper IDs that have significant community attention
3. Extract pain points that indicate active research problems

### Search Patterns

**Path A-Primary — last30days skill** (preferred; covers Reddit + X/Twitter + YouTube):

If `last30days` skill is installed and `OPENAI_API_KEY` is configured:
```
/last30days [primary_topic] robot research
```
Extract `trending_keywords`, `hot_paper_ids`, `pain_points` from the output.

**Path A-Fallback — WebSearch only** (no API key required):

`site:twitter.com` and `site:reddit.com` are not reliably accessible via WebSearch.
Use these three platforms that do work:
```
GitHub (trending repos):
  site:github.com "[topic]" stars robotics 2025

HuggingFace Papers (recent uploads):
  site:huggingface.co/papers "[topic]" 2025

arXiv new submissions (not yet indexed):
  site:arxiv.org "[topic]" 2025 OR 2026
```

### COMMUNITY_SIGNALS Artifact

```json
{
  "trending_keywords": ["[keyword 1]", "[keyword 2]", ...],
  "hot_paper_ids": ["arxiv:YYMM.NNNNN", "arxiv:YYMM.NNNNN", ...],
  "pain_points": ["[pain point 1]", "[pain point 2]", ...],
  "signal_sources": ["twitter", "reddit", "github", "huggingface", "arxiv"],
  "collection_date": "YYYY-MM-DDTHH:MM:SSZ"
}
```

---

## Operational Modes

| Mode | Trigger | Date Filter | Phase A | Target Papers | Use Case |
|------|---------|-------------|---------|---------------|----------|
| `standard` (default) | "find papers on X" | Past 24 months | Yes | 50-100 | General literature discovery |
| `recent` | "recent papers on X", "latest X" | Past 6 months | Yes (priority) | 30-60 | Cutting-edge survey |
| `comprehensive` | "comprehensive search on X", "find all papers on X" | Past 5 years | Yes | 80-100 | Systematic review prep |
| `venue` | "find X papers at [venue]" | Specified venue year | No | 30-60 | Conference-specific survey |
| `pipeline` | Called by `academic-pipeline` Stage 0 | Past 24 months | Yes | 50-100 | Pipeline integration mode |

---

## Output Format

Output conforms exactly to **Schema 2: Bibliography** from `shared/handoff_schemas.md`, with optional `community_signals` and `discovery_phases` fields.

```markdown
## Discovery Output: [topic]

**Material Passport**:
- Origin Skill: discovery
- Origin Mode: [mode]
- Origin Date: [ISO 8601]
- Verification Status: VERIFIED
- Version Label: discovery_v2

---

**Community Signals**:
- Trending Keywords: [comma-separated list]
- Hot Papers Surfaced: [N] (arXiv IDs)
- Pain Points Identified: [N]
- Sources: [X/Twitter, Reddit, GitHub, HuggingFace, arXiv]

---

**Search Strategy**:
- Databases: Semantic Scholar API (WebFetch), arXiv (WebSearch + WebFetch), Papers With Code (WebSearch)
- Community Sources: [list of Phase A platforms searched]
- Keywords: [list of search terms used across all phases]
- Inclusion: [date range], arXiv preprints and published papers, relevance_score ≥ 4
- Exclusion: unresolvable arXiv IDs, papers scoring relevance_score ≤ 3
- Date Range: [start] to [end]
- Verification Method: WebFetch on arxiv.org/abs/{id} for each candidate; DOI resolution for published papers

**Coverage Assessment**: [2-4 sentences honestly describing what was found and what gaps remain]

**Minimum Sources**: [N] verified

---

### Sources

**[S01]** [Authors]. ([Year]). [Title]. *[Journal/Venue/arXiv preprint arXiv:YYMM.NNNNN]*. [URL]
- Type: [journal_article | conference | preprint] | Evidence Tier: [1-7] | Quality: [tier_1 to tier_4] | Relevance: [core | supporting | peripheral] | Score: [1-10]
- Citations: [N] (Semantic Scholar) | S2 ID: [paperId]
- Verified: true (WebFetch: arxiv.org/abs/[id] — HTTP 200, metadata confirmed)
- Annotation: [Sentence 1: what the paper proposes.] [Sentence 2: key quantitative result.] [Sentence 3: specific relevance to the user's research topic.]

**[S02]** ...

---

**Discovery Summary**:
- Phase A (community): [N] trending keywords, [N] hot paper IDs surfaced
- Phase B (search): [N] candidates from S2 API, [N] from arXiv WebSearch, [N] total after dedup
- Phase C (verified): [N] passed WebFetch verification, [N] discarded
- Phase D (expansion): [N] new candidates from citation graph, [N] additional verified
- Final corpus size: [N]
- Ready for handoff: YES

To proceed: say "analyze these papers" or "write a paper on [topic]" and academic-pipeline will continue from Stage 1 using this corpus.
```

---

## Integration

```
                   discovery
                       |
       ┌───────────────┼───────────────┐
       ↓               ↓               ↓
 academic-pipeline  deep-research  standalone
 (Stage 0 → Stage 1) (skip Phase 2)  (output only)

Upstream: none (entry point)
Downstream: deep-research (skip bibliography_agent search),
            academic-paper (skip literature search),
            academic-pipeline (Stage 0 → Stage 1 handoff)
```

### Handoff to academic-pipeline

When called from `academic-pipeline` Stage 0:
1. discovery outputs Schema-2-compliant Bibliography with COMMUNITY_SIGNALS
2. `state_tracker_agent` records `Has_PAPER_CORPUS = true`
3. Stage 1 (`deep-research`) receives PAPER_CORPUS; `bibliography_agent` enters VERIFY MODE
4. `synthesis_agent` uses `community_signals.pain_points` to inform gap analysis

### Handoff to deep-research (standalone)

User says "analyze these papers" after discovery:
- Pass Bibliography artifact directly to `deep-research`
- `deep-research`'s `intake_agent` detects `Has Bibliography → skip literature search`
- COMMUNITY_SIGNALS.pain_points passed to synthesis_agent for gap analysis framing
- Pipeline continues from synthesis phase

### Standalone use

User only wants to find papers (no analysis or writing):
- Output the Bibliography artifact and stop
- User can save it for later use

---

## Agent File References

| Agent | Definition File |
|-------|----------------|
| discovery_agent | `agents/discovery_agent.md` |

---

## Reference Files

| Reference | Purpose |
|-----------|---------|
| `references/arxiv_categories.md` | arXiv category codes for AI, robotics, ML, and related fields |
| `shared/handoff_schemas.md` | Schema 2 (Bibliography) — output must conform exactly |
| `deep-research/references/source_quality_hierarchy.md` | Evidence tier and quality tier definitions |

---

## Templates

| Template | Purpose |
|----------|---------|
| `templates/paper_corpus_template.md` | Schema-2-compliant output template for discovery_agent |

---

## Quality Standards

1. **Zero unverified citations** — every source in the output has `verified: true` from a successful WebFetch
2. **Discard over guess** — if WebFetch fails, the paper is dropped; metadata is never synthesized from search snippets
3. **Honest coverage assessment** — explicitly state what the search did NOT cover (e.g., "IEEE Xplore papers behind paywall not accessible via WebFetch")
4. **Relevance scoring** — every source has a relevance_score 1-10; sources scoring ≤ 3 are excluded
5. **Annotation quality** — annotations are 2-3 sentences: (1) what the paper proposes, (2) key result, (3) relevance to the specific query
6. **Schema compliance** — output validated against Schema 2 before handoff; missing required fields trigger re-generation
7. **Citation count included** — include S2 citationCount for each paper when available; helps downstream agents assess influence

---

## Output Language

Follows the user's language. Paper titles, authors, and citations retained in original language (typically English).

---

## Related Skills

| Skill | Relationship |
|-------|-------------|
| `academic-pipeline` | Calls discovery as Stage 0; receives PAPER_CORPUS for Stage 1 |
| `deep-research` | Receives PAPER_CORPUS; bibliography_agent enters VERIFY MODE; synthesis_agent uses COMMUNITY_SIGNALS |
| `academic-paper` | Can receive Bibliography via intake_agent for literature skip |
| `academic-paper-reviewer` | Can receive PAPER_CORPUS for rapid paper-grounded review |

---

## Version Info

| Item | Content |
|------|---------|
| Skill Version | 2.0 |
| Last Updated | 2026-03-26 |
| Author | Fork contribution to Imbad0202/academic-research-skills |
| Motivation | Scale verified paper discovery from 15-30 (v1.0 WebSearch only) to 50-100 via Semantic Scholar API + citation expansion |
| Schema Compliance | Output conforms to shared/handoff_schemas.md Schema 2 with optional community_signals and discovery_phases fields |

---

## Changelog

| Version | Date | Changes |
|---------|------|---------|
| 2.0 | 2026-03-26 | Four-phase pipeline: Phase A (community intelligence via WebSearch on X/Twitter/Reddit/GitHub/HuggingFace), Phase B (Semantic Scholar API via WebFetch — 200-500 candidates), Phase C (arXiv WebFetch verification), Phase D (citation graph expansion via S2 references/citations API). Target: 50-100 verified papers. COMMUNITY_SIGNALS artifact added for downstream synthesis gap analysis. S2_API_KEY optional (free, increases rate limit). |
| 1.0 | 2026-03-26 | Initial release. Two-phase WebSearch + WebFetch pipeline for hallucination-free paper discovery. Schema-2-compliant output. Integrates with academic-pipeline as Stage 0 and with deep-research via PAPER_CORPUS handoff. Supports 5 modes: standard, recent, comprehensive, venue, pipeline. |
