# Academic Research Skills for Claude Code

[![Version](https://img.shields.io/badge/version-v3.0-blue)](https://github.com/Leooo-Huang/academic-research-skills)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

[中文文档](README.zh-CN.md)

A 50+ agent skill suite for [Claude Code](https://docs.anthropic.com/en/docs/claude-code) that automates the full academic research pipeline — from paper discovery with citation verification to publication-ready manuscripts with simulated peer review.

**Core guarantee**: every citation is verified against its actual arXiv page. Unconfirmed papers are discarded. Zero hallucinated references.

---

## Overview

LLMs hallucinate citations. This project solves that by building a multi-phase verification pipeline on top of Claude Code's skill system.

The suite covers five stages of academic research:

| Skill | Version | Agents | Scope |
|-------|---------|--------|-------|
| **Discovery** | v2.1 | 4-phase | Paper discovery via Semantic Scholar + arXiv APIs, community signal aggregation, citation graph expansion, importance scoring |
| **Deep Research** | v2.4 | 13 | Research question formulation (FINER), systematic literature search, cross-source synthesis, bias assessment, meta-analysis |
| **Academic Paper** | v2.4 | 12 | Structure architecture, argument building, draft writing, citation compliance (APA/IEEE/Chicago/MLA/Vancouver), LaTeX/PDF output |
| **Paper Reviewer** | v1.4 | 5 | Simulated peer review panel — Editor-in-Chief + 3 domain reviewers + Devil's Advocate, 0-100 rubric scoring |
| **Pipeline** | v2.8 | orchestrator | 11-stage workflow with mandatory integrity verification, two-round peer review, Socratic revision coaching |

The full pipeline produces 50-100 verified papers per topic, catches fabricated references at two verification checkpoints (Stage 2.5 and 4.5), and outputs publication-ready manuscripts.

---

## Installation

```bash
git clone https://github.com/Leooo-Huang/academic-research-skills.git ~/.claude/skills/academic-research-skills
```

Optional — install Python dependencies for faster API access with rate limiting:

```bash
pip install requests arxiv huggingface-hub
```

Without Python, the skill falls back to Claude's built-in WebFetch. Same results, slower throughput.

---

## Usage

The skills activate through natural language in Claude Code:

- **Paper discovery**: `"Find papers on [topic]"` — runs the 4-phase discovery pipeline
- **Full pipeline**: `"I want to write a paper on [topic]"` — executes all 11 stages from discovery to PDF
- **Deep research**: `"Research the impact of AI on [field]"` — 13-agent analysis with gap identification
- **Peer review**: `"Review this paper"` — 5-person simulated review with scoring
- **Research guidance**: `"Guide my research on [topic]"` — Socratic dialogue with SCR reflection protocol

### Discovery Pipeline

```
Phase A: Community Intelligence    →  trending signals from X, GitHub, HuggingFace
Phase B: Systematic Search         →  200-500 candidates via S2 + arXiv + HF + GitHub APIs
Phase C: Verification              →  each candidate verified against its arXiv page
Phase D: Citation Graph Expansion  →  forward/backward citation traversal via S2 API
Phase E: Scoring                   →  PIS (Paper Importance Score) ranking
```

**PIS scoring** combines citation velocity, venue prestige, community buzz, and recency decay. Weights adapt by paper age — newer papers scored on relevance, mature papers on impact.

### Full Pipeline

```
DISCOVER → RESEARCH → WRITE → VERIFY → REVIEW → REVISE → PUBLISH
```

11 stages with two mandatory integrity checkpoints. Every reference verified. Two rounds of peer review.

---

## Output Examples

Complete artifacts from a real pipeline run are available in [examples/showcase/](examples/showcase/):

| Artifact | Description |
|----------|-------------|
| [Final Paper](examples/showcase/full_paper_apa7.pdf) | APA 7.0, LaTeX typeset |
| [Integrity Report](examples/showcase/integrity_report_stage2.5.pdf) | Caught 15 fabricated references + 3 statistical errors |
| [Peer Review](examples/showcase/stage3_review_report.pdf) | 5-person review panel, 0-100 scoring |
| [Post-Publication Audit](examples/showcase/post_publication_audit_2026-03-09.pdf) | Stress test found 21/68 issues after 3 rounds of automated checks |

---

## Configuration

**Model**: Claude Opus 4.6 recommended (Max plan). Full pipeline may exceed 200K tokens.

**Unattended mode**: `claude --dangerously-skip-permissions`

**Optional API keys**:

| Key | Purpose | Cost |
|-----|---------|------|
| `S2_API_KEY` | Higher Semantic Scholar rate limits | Free |
| `OPENAI_API_KEY` | Community intelligence via last30days skill | Paid |

---

## Project Structure

```
academic-research-skills/
├── discovery/               Paper discovery engine (v2.1)
│   ├── scripts/             research_radar.py — Python API client
│   └── agents/
├── deep-research/           13-agent research team (v2.4)
├── academic-paper/          12-agent writing pipeline (v2.4)
├── academic-paper-reviewer/ 5-person peer review (v1.4)
├── academic-pipeline/       11-stage orchestrator (v2.8)
├── shared/                  Cross-skill data contracts
└── examples/showcase/       Real pipeline artifacts
```

---

## Contributing

See [CONTRIBUTING.md](CONTRIBUTING.md).

## License

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/) — Free to share and adapt for non-commercial use with attribution.

Based on [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.
