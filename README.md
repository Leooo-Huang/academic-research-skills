# Academic Research Skills for Claude Code

[![Version](https://img.shields.io/badge/version-v3.0-blue)](https://github.com/Leooo-Huang/academic-research-skills)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)
[![Skills](https://img.shields.io/badge/skills-5-green)]()
[![Agents](https://img.shields.io/badge/agents-50+-orange)]()

[中文文档](README.zh-CN.md)

> **50-100 verified papers. Zero hallucinated citations. Publication-ready manuscript. One conversation.**

Academic papers cite LLM-generated references that don't exist. This project fixes that. A 50+ agent skill suite for Claude Code that automates the full academic research pipeline — from real-time paper discovery with verified citations to publication-ready manuscripts with simulated peer review.

---

## The Problem

LLMs hallucinate citations. You ask Claude to find papers, it invents plausible-sounding references that don't exist. You build your literature review on fabricated sources. Your paper gets desk-rejected.

## The Solution

```
You: "Find papers on robot motion retargeting"

Claude: [Phase A] Scanning X/Twitter, GitHub, HuggingFace for community signals...
       [Phase B] Querying Semantic Scholar API... 34 candidates found
       [Phase C] Verifying each paper on arXiv... 28 confirmed real
       [Phase D] Expanding via citation graph... 12 new papers added
       [Phase E] Scoring & ranking...

       Discovery complete: 40 verified papers, 0 hallucinated.
       Ready for deep analysis.
```

Every single citation is verified by fetching its actual arXiv page. If a paper can't be confirmed, it's discarded — never guessed.

---

## Install

```bash
git clone https://github.com/Leooo-Huang/academic-research-skills.git ~/.claude/skills/academic-research-skills
```

Optional (faster paper discovery):
```bash
pip install requests arxiv huggingface-hub
```

That's it. Open Claude Code and start talking.

---

## What You Can Do

| Say this | What happens |
|----------|-------------|
| `"Find papers on [topic]"` | Discovers 50-100 verified papers from S2 + arXiv + community signals |
| `"I want to write a paper on [topic]"` | Runs the full 11-stage pipeline: discover → research → write → review → revise → publish |
| `"Research the impact of AI on [field]"` | 13-agent deep research with gap analysis and synthesis |
| `"Review this paper"` | 5-person simulated peer review (Editor-in-Chief + 3 reviewers + Devil's Advocate) |
| `"Guide my research on [topic]"` | Socratic dialogue with SCR protocol to sharpen your thinking |

---

## Full Pipeline

```
DISCOVER ──→ RESEARCH ──→ WRITE ──→ VERIFY ──→ REVIEW ──→ REVISE ──→ PUBLISH
50-100       13-agent     12-agent  100% ref   5-person   Address    LaTeX
papers       team         pipeline  check      review     feedback   → PDF
```

11 stages. Every reference verified. Two rounds of peer review. Zero tolerance for fabricated citations.

---

## 5 Skills, 50+ Agents

### 1. Discovery v2.1

**The anti-hallucination engine.** Python-first API access with proper rate limiting.

| Phase | Purpose | Method |
|-------|---------|--------|
| Community Intelligence | What's trending, what hurts | last30days / WebSearch |
| Systematic Search | 200-500 candidates | Python → Semantic Scholar + arXiv + HF + GitHub |
| Verification | Is this paper real? | Python → fetch each arXiv page |
| Citation Expansion | What did they cite? Who cited them? | Python → S2 citation graph |

**Scoring**: Papers ranked by PIS (Paper Importance Score) — citation velocity, venue prestige, community buzz, recency. Weights adapt by paper age: new papers judged on relevance, mature papers judged on impact.

### 2. Deep Research v2.4

13 agents including Research Question formulation (FINER scoring), Socratic mentoring (with SCR reflection protocol), systematic literature search, source verification, cross-source synthesis, risk of bias assessment, meta-analysis, and editorial review.

7 modes: full / quick / systematic-review / socratic / fact-check / lit-review / paper-review

### 3. Academic Paper v2.4

12 agents covering intake, literature strategy, structure architecture, argument building, draft writing, citation compliance (APA/IEEE/Chicago/MLA/Vancouver), bilingual abstracts, visualization, revision coaching, and formatting (LaTeX/DOCX/PDF via tectonic).

### 4. Academic Paper Reviewer v1.4

Simulates a 5-person review panel: Editor-in-Chief + 3 domain-specific reviewers + Devil's Advocate. 0-100 quality rubrics with behavioral indicators. Decision mapping: >=80 Accept, 65-79 Minor Revision, 50-64 Major Revision, <50 Reject.

### 5. Academic Pipeline v2.8

Orchestrates everything into an 11-stage workflow with mandatory integrity verification (Stage 2.5 + 4.5), two-stage peer review, Socratic revision coaching, and post-pipeline collaboration quality evaluation.

---

## Why Python?

Discovery v2.1 uses a Python script (`research_radar.py`) for all API calls instead of Claude's built-in WebFetch. Why?

| | WebFetch | Python script |
|--|---------|--------------|
| Rate limiting | No control, 429 errors cached 15 min | Exponential backoff (10s → 30s → 120s) |
| Request spacing | Cannot add delays | 1.5s between calls |
| Batch processing | One at a time | Batch verify 80 papers in one command |
| Error recovery | Stuck on cached errors | Retry with backoff, graceful fallback |

**No Python? No problem.** The skill falls back to WebFetch automatically. Same results, just slower and may hit rate limits.

---

## Real Output

See complete pipeline artifacts from a real run: **[examples/showcase/](examples/showcase/)**

| Artifact | What it shows |
|----------|-------------|
| [Final Paper (EN)](examples/showcase/full_paper_apa7.pdf) | APA 7.0 LaTeX output |
| [Integrity Report](examples/showcase/integrity_report_stage2.5.pdf) | Caught 15 fabricated refs + 3 statistical errors |
| [Peer Review](examples/showcase/stage3_review_report.pdf) | Full 5-person review with 0-100 scoring |
| [Post-Publication Audit](examples/showcase/post_publication_audit_2026-03-09.pdf) | Found 21/68 issues missed by 3 rounds of checks |

---

## Configuration

**Recommended model**: Claude Opus 4.6 (Max plan). Full pipeline can exceed 200K tokens.

**For uninterrupted runs**: `claude --dangerously-skip-permissions`

**Optional API keys**:
| Key | Purpose | Cost |
|-----|---------|------|
| `S2_API_KEY` | Higher Semantic Scholar rate limit | Free |
| `OPENAI_API_KEY` | last30days skill (Reddit/X/YouTube intelligence) | Paid |

---

## Project Structure

```
academic-research-skills/
├── discovery/           ← Paper discovery engine (v2.1)
│   ├── scripts/         ← research_radar.py (Python API client)
│   └── agents/
├── deep-research/       ← 13-agent research team (v2.4)
├── academic-paper/      ← 12-agent writing pipeline (v2.4)
├── academic-paper-reviewer/ ← 5-person peer review (v1.4)
├── academic-pipeline/   ← 11-stage orchestrator (v2.8)
├── shared/              ← Cross-skill data contracts
└── examples/showcase/   ← Real pipeline outputs
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

---

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — Free to share and adapt for non-commercial use with attribution.

Based on [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.
