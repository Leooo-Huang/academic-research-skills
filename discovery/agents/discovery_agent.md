# Discovery Agent v2.1

## Role

Four-phase paper discovery agent with Python-first API access. Phase A: community intelligence via optional last30days skill or WebSearch fallback. Phase B: `scripts/research_radar.py --mode search` via Bash (primary) or WebFetch (fallback). Phase C: `scripts/research_radar.py --mode verify` via Bash (primary) or WebFetch (fallback). Phase D: `scripts/research_radar.py --mode expand` via Bash (primary) or WebFetch (fallback). Assemble and output Schema-2-compliant Bibliography with COMMUNITY_SIGNALS. Python handles all API calls with proper rate limiting and exponential backoff; WebFetch is only used when Python is unavailable.

---

## Phase A: Community Intelligence

### Purpose

Surface trending keywords, recently-discussed papers, and practitioner pain points from community platforms. These signals inform Phase B query construction and are passed to downstream synthesis_agent for gap analysis.

### Path A-Primary: last30days skill (preferred — Reddit + X + YouTube coverage)

If the user has the `last30days` skill installed and `OPENAI_API_KEY` configured:

1. Suggest the user run: `/last30days [primary_topic] robot research`
2. From the last30days output, extract COMMUNITY_SIGNALS:
   - **trending_keywords**: technical terms with high engagement (upvotes, likes, views)
   - **hot_paper_ids**: arXiv IDs mentioned in posts or comments with significant engagement
   - **pain_points**: practitioner complaints and open problems from Reddit/X discussions
   - **signal_sources**: list which platforms returned results (`reddit`, `twitter`, `youtube`)
3. Pass extracted COMMUNITY_SIGNALS to Phase B

**Note**: last30days requires `OPENAI_API_KEY` (paid) + `python3` + `node`. It is an optional integration — discovery skill works without it.

### Path A-Fallback: WebSearch (no API key required)

When last30days is unavailable, run these WebSearch queries:

```
A3 (GitHub trending repos):
  site:github.com "[primary_topic]" robot OR manipulation 2025 stars

A4 (HuggingFace Papers):
  site:huggingface.co/papers "[primary_topic]" 2025

A5 (arXiv new submissions — recent, possibly not S2-indexed yet):
  site:arxiv.org "[primary_topic]" [current_month_year]
```

**Why not Twitter/Reddit via WebSearch**: `site:twitter.com` and `site:reddit.com` queries consistently return no usable results through WebSearch. Coverage of these platforms requires the last30days skill (Path A-Primary).

### Community Signal Extraction

From each result (whether from last30days or WebSearch fallback), extract:
- **trending_keywords**: recurring technical terms appearing in multiple results (not the user's own query terms — look for emerging terminology)
- **hot_paper_ids**: arXiv IDs mentioned in posts, comments, or links with significant engagement indicators (retweets, upvotes, stars, downloads)
- **pain_points**: problems or limitations repeatedly mentioned by practitioners ("X doesn't work for...", "the main challenge is...", "nobody has solved...")
- **signal_sources**: which platforms were searched successfully

### COMMUNITY_SIGNALS Output

```json
{
  "trending_keywords": ["keyword_1", "keyword_2", "keyword_3"],
  "hot_paper_ids": ["2412.NNNNN", "2501.NNNNN"],
  "pain_points": ["pain point description 1", "pain point description 2"],
  "signal_sources": ["github", "huggingface", "arxiv"],
  "collection_date": "YYYY-MM-DDTHH:MM:SSZ"
}
```

**If Phase A yields no signals**: Proceed to Phase B without community signals. Note in coverage_assessment: "No community signals retrieved. Phase B used user-provided topic keywords only."

---

## Phase B: Systematic Search

### B0: Python Environment Check

Before Phase B API calls, check Python + dependencies availability:

```
Bash: uv run --with requests python ~/.claude/skills/academic-research-skills/discovery/scripts/research_radar.py --help 2>/dev/null && echo "RADAR_OK"
```

- If output contains "RADAR_OK" → `PYTHON_AVAILABLE = true`
- If fails → try without uv: `python3 ~/.claude/skills/academic-research-skills/discovery/scripts/research_radar.py --help 2>/dev/null`
- If both fail → `PYTHON_AVAILABLE = false` → use WebFetch fallback path

Store the working command prefix as `RADAR_CMD`:
- If uv works: `RADAR_CMD = "uv run --with requests --with arxiv --with huggingface-hub python ~/.claude/skills/academic-research-skills/discovery/scripts/research_radar.py"`
- If python3 works directly: `RADAR_CMD = "python3 ~/.claude/skills/academic-research-skills/discovery/scripts/research_radar.py"`

### B1: Semantic Scholar + arXiv + HuggingFace + GitHub (Multi-source search)

#### Primary Path (PYTHON_AVAILABLE = true)

Run the research radar script via Bash:

```
Bash: {RADAR_CMD} \
  --mode search \
  --query "{user_topic}" \
  --days 30 \
  --source all \
  --output-json
```

Parse the JSON stdout. The script returns:
```json
{
  "status": "success",
  "papers": [
    {
      "s2_id": "full S2 paper ID",
      "arxiv_id": "YYMM.NNNNN or null",
      "doi": "10.xxxx or null",
      "title": "Paper title",
      "authors": ["Author 1", "Author 2"],
      "year": 2025,
      "date": "2025-03-15",
      "abstract": "Full abstract text",
      "citation_count": 42,
      "venue": "ICRA 2025",
      "url": "https://arxiv.org/abs/...",
      "source": "semantic_scholar|arxiv|huggingface",
      "verified": false
    }
  ],
  "metadata": { "counts": { "semantic_scholar": N, "arxiv": N, ... } }
}
```

**Advantages over WebFetch**:
- Rate limiting handled internally (exponential backoff: 10s → 30s → 120s on 429)
- Requests spaced 1.5s apart (no cache collisions)
- Abstract included in results (enables B4 pre-filtering without extra calls)
- Full paperId preserved (not truncated — needed for Phase D)
- Also runs publicationDate:desc query automatically for recency coverage

#### Fallback Path (PYTHON_AVAILABLE = false)

Use WebFetch to call S2 API directly (v2.0 behavior):

```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/search?query={ENCODED_QUERY}&fields=title,abstract,authors,year,citationCount,venue,externalIds&limit=100
```

Run 3-5 queries with different keyword combinations. Note: WebFetch has 15-minute cache and no rate control — may trigger 429 with no recovery.

#### API Rate Limiting (applies to both paths)

- Free tier: 100 requests per 5 minutes
- With `S2_API_KEY` env var: rate limit increases significantly
- Python path: handles 429 automatically with exponential backoff
- WebFetch path: if 429, wait 60s and retry once; if still 429, proceed with results collected

### B2: arXiv WebSearch (Supplementary — catches recent papers)

Run 2-3 WebSearch queries on arXiv to catch papers submitted in the last 1-3 months that may not yet be indexed in Semantic Scholar:

```
B2-Q1 (arXiv, recent):
  site:arxiv.org "[primary_keyword]" "[secondary_keyword]" [current_year]

B2-Q2 (arXiv + venue):
  site:arxiv.org "[primary_keyword]" "[venue_name]" [year]

B2-Q3 (Papers With Code):
  site:paperswithcode.com "[primary_keyword]" "[task_name]"
```

From each result, extract arXiv IDs (format: `YYMM.NNNNN` from URLs matching `arxiv.org/abs/XXXX.XXXXX`).

### B3: Deduplication

Merge all candidates from B1 and B2:
1. Primary dedup key: arXiv ID (`externalIds.ArXiv` from S2, or extracted from URL)
2. Secondary dedup key: S2 paperId (for papers without arXiv IDs)
3. When same paper appears in both S2 and arXiv WebSearch: keep S2 entry (has more metadata)

**Stop condition**: If total candidates < 20 after all B1 and B2 queries, inform the user and ask to broaden scope or date range before proceeding to Phase C.

### B4: Abstract Pre-filtering (reduces Phase C verification load by ~70%)

S2 API already returns `abstract` in Phase B results. Use it to filter BEFORE Phase C WebFetch:

**Step 1 — Domain relevance check**:
Discard papers whose abstract does not contain ANY of the user's primary keywords or close synonyms. This removes off-topic results from broad queries (Q3, Q5).

**Step 2 — Quality signal check** (basic "water paper" filter):
Flag papers as `quality_suspect` if their abstract:
- Contains no quantitative results (no numbers, percentages, metrics, or comparison terms like "outperforms", "achieves", "improves by")
- Is shorter than 50 words (indicates incomplete or placeholder entry)
Papers flagged `quality_suspect` are deprioritized for Phase C verification (processed last, and only if candidate budget allows).

**Step 3 — Candidate budget for Phase C**:
After pre-filtering, send at most **80 candidates** to Phase C (ordered by: non-suspect first, then by S2 citationCount descending within each group). This caps Phase C WebFetch calls at ~80 instead of 200-300.

**Outcome**: Candidate pool 200-300 → pre-filtered pool 60-80 → Phase C verification.

---

## Phase C: Verification

#### Primary Path (PYTHON_AVAILABLE = true)

Collect all candidate arXiv IDs from Phase B, then batch-verify:

```
Bash: {RADAR_CMD} \
  --mode verify \
  --arxiv-ids "2510.02252,2402.16796,2505.03738,..." \
  --output-json
```

The script fetches each arXiv abstract page with 0.5s polite delay, parses HTML for metadata (title, authors, abstract, date, categories, DOI), and returns JSON with `verified: true/false` per paper.

#### Fallback Path (PYTHON_AVAILABLE = false)

For each candidate arXiv ID, perform WebFetch:

```
URL: https://arxiv.org/abs/{arxiv_id}
Example: https://arxiv.org/abs/2303.04137
```

### Verification Success Criteria

The fetched page MUST contain all of the following to be considered verified:
1. A `<title>` element containing the paper title (not "arXiv Error" or "not found")
2. Author names in the page body
3. An abstract section
4. A submission date

### On Success — Extract These Fields

| Field | Where to Find It | Notes |
|-------|-----------------|-------|
| `title` | `<title>` tag or `h1.title` | Strip "[YYYY.NNNNN] " prefix if present |
| `authors` | Author list section | Format as "Last, F., Last, F., ..." |
| `year` | Submission date | Use year of first submission |
| `doi` | DOI field if present | Optional; only if paper is published |
| `arxiv_id` | URL | Format: YYMM.NNNNN |
| `categories` | Subject classes | e.g., "cs.RO, cs.LG" |
| `abstract` | Abstract section | Used for relevance scoring + annotation |
| `venue` | Journal-ref field if present | e.g., "ICRA 2025", "NeurIPS 2024" |

### On Failure — DISCARD

Discard the candidate without substitution if ANY of these occur:
- HTTP 4xx or 5xx response
- Page title contains "arXiv Error", "not found", "404"
- Page does not contain an abstract section
- arXiv ID does not match the expected paper (redirect to a different paper)

**Rule**: Never synthesize missing fields from the search snippet. If the page cannot be fetched, the paper does not enter the output.

### DOI Verification (Optional)

If the fetched arXiv page contains a DOI (journal-ref field):
```
WebFetch: https://doi.org/{doi}
```
- If resolves (HTTP 200): update `verified: true`, add journal name to citation
- If fails: keep arXiv URL as primary reference, do not discard

### Relevance Scoring (1-10)

Score each verified paper against the user's research topic using the abstract:

| Score | Meaning |
|-------|---------|
| 9-10 | Directly addresses the exact research question; highly relevant |
| 7-8 | Addresses the core topic with slight variation in method or scope |
| 5-6 | Related technique or adjacent problem; supporting context |
| 3-4 | Loosely related; peripheral background |
| 1-2 | Tangentially relevant; unlikely to be cited |

**Threshold**: Papers scoring ≤ 3 are excluded from the output.

---

## Phase D: Citation Expansion

For the top 10 papers by relevance_score from Phase C, expand the corpus via Semantic Scholar's citation graph.

#### Primary Path (PYTHON_AVAILABLE = true)

Collect S2 paper IDs of top papers, then batch-expand:

```
Bash: {RADAR_CMD} \
  --mode expand \
  --s2-ids "paperId1,paperId2,paperId3,..." \
  --direction both \
  --output-json
```

The script fetches references + citations for each paper with 1.5s delay between calls, handles 429 with exponential backoff, and returns new candidate papers as JSON.

#### Fallback Path (PYTHON_AVAILABLE = false)

### D1: Fetch References (Papers Cited By This Paper)

```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/{S2_PAPER_ID}/references?fields=title,abstract,authors,year,externalIds&limit=50
```

### D2: Fetch Citations (Papers That Cite This Paper)

```
WebFetch: https://api.semanticscholar.org/graph/v1/paper/{S2_PAPER_ID}/citations?fields=title,abstract,authors,year,externalIds&limit=50
```

### D0: Temporal Triage (run before D1/D2)

Before expanding a paper via citation graph, check its age:

| Paper age (months since publication) | D1 References | D2 Citations | Rationale |
|--------------------------------------|--------------|--------------|-----------|
| < 3 months | ✅ Run | ❌ Skip | Too new to have accumulated citations; D2 would return near-empty |
| 3–12 months | ✅ Run | ✅ Run (limit=25) | Early citations exist; references reveal foundational work |
| > 12 months | ✅ Run | ✅ Run (limit=50) | Full citation graph available |

**For papers < 3 months old**: rely on Phase A `hot_paper_ids` and Phase B2 arXiv WebSearch as the primary recency signal. Note in Discovery Summary: "N papers too recent for citation expansion; coverage via Phase A + Phase B2."

### D3: Process Expansion Candidates

1. Extract arXiv IDs from `externalIds.ArXiv` in the references/citations response
2. Exclude papers already in the corpus (already verified)
3. Pre-score by abstract relevance
4. Run Phase C verification on new candidates with relevance pre-score ≥ medium
5. Add verified papers to corpus

**Expansion budget**: Maximum 10 S2 API calls in Phase D (5 reference + 5 citation lookups for top 5 papers). Do not expand indefinitely.

---

## Phase E: Output Assembly

### Evidence Tier Assignment

| Tier | Type |
|------|------|
| 1 | Systematic review or meta-analysis |
| 2 | RCT or high-quality experimental study |
| 3 | Cohort or comparative study |
| 4 | Case study or ablation study |
| 5 | Preprint with strong experimental results |
| 6 | Workshop paper or short paper |
| 7 | Position paper or technical report |

For AI/robotics papers: most arXiv preprints = Tier 5; published conference papers (ICRA, NeurIPS, CVPR, CoRL) = Tier 3-4; journal papers = Tier 2-3.

### Quality Tier Assignment

| Quality Tier | Condition |
|-------------|-----------|
| tier_1 | Published in top-quartile venue (NeurIPS, ICML, ICLR, CVPR, ICRA, CoRL, RSS, RA-L, T-RO, IJRR, Science Robotics) |
| tier_2 | Published in other peer-reviewed venue |
| tier_3 | arXiv preprint with ≥ 3 months since submission and no venue |
| tier_4 | arXiv preprint < 3 months old; workshop papers |

### Annotation Writing

Write 2-3 sentences for each paper:
1. **Sentence 1**: What the paper proposes/does (method or contribution)
2. **Sentence 2**: Key result or finding (be specific: include numbers if available in abstract)
3. **Sentence 3**: Why it is relevant to the user's research topic

**Anti-patterns** (never do these):
- "This paper studies X." → too vague
- Copying the abstract verbatim
- Claiming results not stated in the abstract

### Citation Format

APA 7.0 for journal/conference papers:
```
Authors. (Year). Title. Venue, Volume(Issue), Pages. https://doi.org/XXX
```

arXiv preprint format:
```
Authors. (Year). Title. arXiv preprint arXiv:YYMM.NNNNN. https://arxiv.org/abs/YYMM.NNNNN
```

### Composite Scoring (PIS — Paper Importance Score)

Replace raw `citationCount` ranking with a multi-dimensional composite score. **Weights change based on paper age** — because different signals are trustworthy at different stages of a paper's life.

---

#### Sub-score 1: Citation Velocity (time-adjusted impact)

```
months_alive = (current_year - pub_year) × 12 + (current_month - 6)  # approximate
citation_velocity = citationCount / max(months_alive, 1)
```

Normalize across the full corpus: find `max_velocity` in the corpus, then:
```
citation_velocity_score = (citation_velocity / max_velocity) × 10    # scale to 0–10
```

**Note**: Citation velocity is ONLY meaningful for papers > 3 months old. For papers < 3 months, set `citation_velocity_score = 5` (neutral) to avoid penalizing or inflating based on insufficient data.

---

#### Sub-score 2: Venue Score (domain-aware prestige)

Robotics-focused domain-aware weighting (not just generic tier):

```
CoRL, RSS                                                              → 10  (robotics-specific top venues)
ICRA, IROS, RA-L, T-RO, IJRR, Science Robotics                       → 9   (robotics flagship)
NeurIPS, ICML, ICLR, CVPR, ICCV                                       → 8   (top ML/CV — high prestige, lower domain specificity)
Other peer-reviewed venue                                              → 6
arXiv preprint ≥ 6 months (no venue)                                   → 3
arXiv preprint < 6 months (no venue), workshop                         → 2
```

**Why domain-aware**: A CoRL paper on motion retargeting is reviewed by robotics experts; a NeurIPS paper on the same topic might be reviewed by general ML reviewers. Both are excellent venues, but CoRL acceptance carries stronger domain-specific validation.

---

#### Sub-score 3: Community Score (from Phase A COMMUNITY_SIGNALS)

```
arxiv_id in hot_paper_ids                                → 10
title or abstract contains ≥ 2 trending_keywords        → 6
title or abstract contains 1 trending_keyword           → 3
no match                                                → 0
```

---

#### Sub-score 4: Recency Score (exponential decay, not step function)

```
recency_score = max(1, exp(-0.04 × months_since_publication) × 10)
```

**Decay curve for AI/Robotics** (λ = 0.04):
| Paper age | recency_score | Interpretation |
|-----------|--------------|----------------|
| 1 month   | 9.6          | Brand new      |
| 3 months  | 8.9          | Very recent    |
| 6 months  | 7.9          | Recent         |
| 12 months | 6.2          | Current        |
| 24 months | 3.8          | Aging but valid |
| 36 months | 2.4          | Old but cited  |
| 60 months | 1.0          | Floor (never zero) |

**Why exponential**: Step functions create cliff edges (12→24 months drops from 2 to 1). Exponential decay is smooth — a 13-month-old paper scores nearly the same as a 12-month-old paper. The floor of 1.0 ensures classic papers (Dex-Net, Policy Distillation) never fully vanish.

**Why λ = 0.04**: Calibrated for robotics. At λ=0.04, a paper retains 55% of its recency score at 12 months. NLP would use λ=0.10+ (faster decay); pure theory would use λ=0.01 (slower).

---

#### Sub-score 5: Quality Penalty (from Phase B4 pre-filtering)

```
quality_suspect flag from B4                             → multiply final_score by 0.7
no flag                                                  → no penalty (×1.0)
```

---

#### Age-based Phased Weights

**Core insight**: A new paper has no citation track record, so weighting citation_velocity heavily is nonsensical. A mature paper's community buzz has faded, so community_score is stale. The weights must adapt.

```
Paper age < 6 months (NEW — trust relevance + venue, citations insufficient):
  final_score = 0.65 × relevance_score
              + 0.05 × citation_velocity_score    # almost ignored — data too sparse
              + 0.12 × venue_score
              + 0.08 × community_score
              + 0.10 × recency_score

Paper age 6–18 months (EMERGING — balanced, all signals have data):
  final_score = 0.55 × relevance_score
              + 0.15 × citation_velocity_score    # now meaningful
              + 0.12 × venue_score
              + 0.10 × community_score
              + 0.08 × recency_score

Paper age > 18 months (MATURE — velocity + venue dominate; recency fades):
  final_score = 0.50 × relevance_score
              + 0.20 × citation_velocity_score    # strongest importance signal
              + 0.15 × venue_score
              + 0.10 × community_score
              + 0.05 × recency_score
```

All sub-scores are on a 0–10 scale. `final_score` ranges 0–10.

**Design rationale**:
- **Relevance always leads** (0.50–0.65): an off-topic paper can never compensate with high citations
- **New papers lean on relevance + venue** (0.65 + 0.12): a new CoRL paper scores well even with 0 citations
- **Mature papers lean on velocity + venue** (0.20 + 0.15): proven track record matters more for older papers
- **Community score stays moderate** (0.08–0.10): enough to surface hot papers, not enough for hype to dominate
- **Recency is a bonus** (0.05–0.10): prevents classic papers from vanishing, prevents new-but-weak papers from dominating

### Ranking and Capping

1. Sort verified papers by `final_score` descending
2. Cap at 100 sources maximum
3. Assign sequential IDs: [S01], [S02], ..., [S100]
4. Include `final_score`, `importance_score`, and `relevance_score` in the source entry for transparency

---

## Failure Paths

| Failure | Trigger | Recovery |
|---------|---------|---------|
| < 20 candidates after Phase B | Topic too narrow or recent | Inform user; suggest broader keywords or extended date range |
| < 10 verified papers after Phase C | Many candidates unresolvable | Inform user with discard count; ask whether to proceed or retry with broader search |
| S2 API rate limited | HTTP 429 | Wait 60s; retry once; if still 429, proceed with results collected |
| All candidates from same lab/group | Query too specific | Add diversity query in B2: site:arxiv.org "[broader topic]" -"[specific lab keyword]" |
| No Papers With Code results | Task framing doesn't match PwC taxonomy | Skip B2-Q3; proceed with B1 and B2-Q1/Q2 |
| Phase A yields no community signals | Community search returns unrelated results | Note in coverage_assessment; proceed without community signals |
| Phase D expansion yields no new papers | Corpus is already comprehensive | Note "Citation graph did not expand corpus" in Discovery Summary |

---

## Output Validation Checklist

Before outputting, verify:

- [ ] COMMUNITY_SIGNALS block is present (or absence is documented)
- [ ] Every source has `verified: true` (confirmed by successful WebFetch)
- [ ] Every source has all required Schema-2 fields: id, title, authors, year, citation, type, evidence_tier, quality_tier, relevance, relevance_score, annotation
- [ ] No source has `relevance_score ≤ 3`
- [ ] Phase E scoring used age-based phased weights (not fixed weights)
- [ ] `quality_suspect` papers received 0.7× penalty in final_score
- [ ] Annotations are 2-3 sentences (not copied abstracts)
- [ ] Material Passport is present and complete (version: discovery_v2)
- [ ] Search strategy block lists actual queries used across all phases
- [ ] Coverage assessment is honest about gaps
- [ ] Discovery Summary phase counts are accurate (A/B/C/D counts)
- [ ] discovery_phases counts match actual numbers
