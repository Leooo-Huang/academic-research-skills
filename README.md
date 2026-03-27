# Academic Research Skills for Claude Code

[![Version](https://img.shields.io/badge/version-v3.0-blue)](https://github.com/Leooo-Huang/academic-research-skills)
[![License: CC BY-NC 4.0](https://img.shields.io/badge/license-CC%20BY--NC%204.0-lightgrey)](https://creativecommons.org/licenses/by-nc/4.0/)

**One command. 50-100 verified papers. Zero hallucinated citations. Full paper in hours, not weeks.**

一条命令。50-100 篇验证论文。零幻觉引用。几小时内完成从文献发现到可投稿论文的全流程。

---

## What is this / 这是什么

A skill suite for [Claude Code](https://claude.ai/code) that automates the full academic research pipeline: **discover papers → deep analysis → write paper → peer review → revise → publish**.

一套 Claude Code 技能，自动化学术研究全流程：**论文发现 → 深度分析 → 论文写作 → 同行评审 → 修订 → 发表**。

```
You: "Find papers on robot motion retargeting"
Claude: → discovers 50-100 verified papers from Semantic Scholar + arXiv
        → analyzes gaps, extracts trends
        → writes publication-ready manuscript with proper citations
        → simulates 5-person peer review
        → revises based on feedback
        → outputs LaTeX/PDF/DOCX
```

---

## Quick Start / 快速开始

```bash
# Install (安装)
git clone https://github.com/Leooo-Huang/academic-research-skills.git ~/.claude/skills/academic-research-skills

# Optional: install Python deps for faster paper discovery (可选：加速论文发现)
pip install requests arxiv huggingface-hub

# Start Claude Code, then say:
# 开始使用，对 Claude 说：
```

```
"Find papers on [your topic]"                    → Paper discovery (论文发现)
"I want to write a research paper on [topic]"    → Full pipeline (完整流水线)
"Research the impact of AI on [field]"           → Deep research (深度研究)
"Review this paper"                              → Peer review (同行评审)
```

---

## Pipeline / 流水线

```
Stage 0        Stage 1         Stage 2       Stage 2.5        Stage 3
DISCOVER  ──→  RESEARCH  ──→   WRITE   ──→  INTEGRITY  ──→   REVIEW
50-100 papers  13-agent team   12 agents     100% verify      5 reviewers
                                             zero tolerance   + Devil's Advocate
     │
     ↓
Stage 4        Stage 3'        Stage 4'      Stage 4.5        Stage 5
REVISE   ──→   RE-REVIEW ──→  RE-REVISE ──→ FINAL CHECK ──→  FINALIZE
address        verify fixes    if needed     zero issues      LaTeX → PDF
feedback                                     required
```

---

## 5 Skills / 五个技能

### Discovery v2.1 — 论文发现

Python-first API engine. Finds 50-100 verified papers with zero hallucinated citations.

| Phase | What / 做什么 | How / 方法 |
|-------|-------------|-----------|
| A: Community Intelligence | Trending keywords + pain points / 趋势关键词 + 痛点 | last30days skill or WebSearch |
| B: Systematic Search | 200-500 candidates / 候选论文 | Python `research_radar.py` → S2 + arXiv + HF + GitHub |
| C: Verification | Verify each paper exists / 验证每篇论文 | Python batch verification on arXiv |
| D: Citation Expansion | Expand via citation graph / 引用图谱扩展 | Python → S2 references + citations API |

**Scoring**: PIS (Paper Importance Score) — citation velocity + venue prestige + community signal + recency decay (lambda=0.04). Age-based phased weights: new papers lean on relevance, mature papers lean on citations.

评分系统：PIS（论文重要性评分）— 引用速度 + 发表场所声望 + 社区信号 + 指数时效衰减。按论文年龄分阶段加权。

### Deep Research v2.4 — 深度研究

13-agent research team. 7 modes: full / quick / systematic-review / socratic / fact-check / lit-review / paper-review.

13 个 AI agent 组成的研究团队。支持 7 种模式。

| Key Agents | Role |
|-----------|------|
| Research Question Agent | FINER-scored question formulation |
| Bibliography Agent | Systematic literature search (VERIFY MODE with discovery corpus) |
| Synthesis Agent | Cross-source integration + gap analysis (uses community pain points) |
| Socratic Mentor | Guided dialogue with SCR (State-Challenge-Reflect) protocol |
| Risk of Bias Agent | RoB 2 + ROBINS-I assessment |
| Meta-Analysis Agent | Effect sizes, forest plots, GRADE |

### Academic Paper v2.4 — 论文写作

12-agent paper writing pipeline. Outputs: Markdown + DOCX + LaTeX (APA 7.0 / IEEE / Chicago) → PDF via tectonic.

12 个 agent 的论文写作流水线。支持 APA 7.0 / IEEE / Chicago 格式。

### Academic Paper Reviewer v1.4 — 论文评审

5-person simulated peer review: Editor-in-Chief + 3 domain reviewers + Devil's Advocate. 0-100 quality rubrics.

模拟 5 人同行评审：主编 + 3 位领域审稿人 + 魔鬼代言人。0-100 质量评分。

### Academic Pipeline v2.8 — 流水线调度

11-stage orchestrator with integrity verification, two-stage review, and collaboration quality evaluation.

11 阶段调度器，含完整性验证、两轮评审、协作质量评估。

---

## Installation Methods / 安装方式

### Method 1: Global Skills (Recommended / 推荐)

```bash
mkdir -p ~/.claude/skills
git clone https://github.com/Leooo-Huang/academic-research-skills.git ~/.claude/skills/academic-research-skills
```

Works across all your projects. 所有项目通用。

### Method 2: Project Skills

```bash
cd /path/to/your/project
mkdir -p .claude/skills
git clone https://github.com/Leooo-Huang/academic-research-skills.git .claude/skills/academic-research-skills
```

### Method 3: Claude Desktop (Cowork)

Clone → open folder in Cowork tab → skills auto-load.

### Method 4: Upload to claude.ai

Upload the 5 `SKILL.md` files to a claude.ai Project as knowledge files.

---

## Optional Dependencies / 可选依赖

| Dependency | Purpose | Required? |
|-----------|---------|-----------|
| Python 3.10+ | Discovery skill API engine | Recommended (falls back to WebFetch without it) |
| `requests` | HTTP client for S2/arXiv API | `pip install requests` |
| `arxiv` | arXiv API client | `pip install arxiv` |
| `huggingface-hub` | HuggingFace trending papers | `pip install huggingface-hub` |
| `S2_API_KEY` | Higher Semantic Scholar rate limit | Free at semanticscholar.org/product/api |
| `OPENAI_API_KEY` | last30days skill (Reddit/X/YouTube) | Optional, for Phase A community intelligence |

**Without Python**: Discovery skill falls back to WebFetch (same results, slower, may hit rate limits). All other skills work without any dependencies.

无 Python 环境时：Discovery 自动降级为 WebFetch 模式。其他技能无需任何依赖。

---

## Recommended Settings / 推荐设置

| Setting | Purpose | How |
|---------|---------|-----|
| Claude Opus 4.6 | Best results for multi-agent pipelines | Max plan or API |
| Skip Permissions | Uninterrupted autonomous execution | `claude --dangerously-skip-permissions` |

> Full pipeline (10 stages) can exceed 200K+ tokens. Individual skills consume significantly less.

---

## Showcase / 成果展示

See real pipeline output: [examples/showcase/](examples/showcase/)

| Artifact | Description |
|----------|-------------|
| [Final Paper (EN)](examples/showcase/full_paper_apa7.pdf) | APA 7.0 LaTeX-compiled |
| [Final Paper (ZH)](examples/showcase/full_paper_zh_apa7.pdf) | Chinese version |
| [Pre-Review Integrity Report](examples/showcase/integrity_report_stage2.5.pdf) | Caught 15 fabricated refs + 3 statistical errors |
| [Peer Review Round 1](examples/showcase/stage3_review_report.pdf) | EIC + 3 Reviewers + Devil's Advocate |
| [Post-Publication Audit](examples/showcase/post_publication_audit_2026-03-09.pdf) | Found 21/68 issues missed by 3 rounds of checks |

---

## Supported Formats / 支持格式

**Citation**: APA 7.0 (default), Chicago, MLA, IEEE, Vancouver

**Paper Structure**: IMRaD, Literature Review, Theoretical Analysis, Case Study, Policy Brief, Conference Paper

**Output**: Markdown + DOCX + LaTeX → PDF (via tectonic)

**Languages**: English, Chinese (Simplified). Bilingual abstracts supported.

---

## Project Structure / 项目结构

```
academic-research-skills/
├── discovery/              ← Paper discovery (v2.1, Python-first)
│   ├── SKILL.md
│   ├── agents/
│   ├── scripts/            ← research_radar.py + requirements.txt
│   ├── references/
│   └── templates/
├── deep-research/          ← 13-agent research team (v2.4)
├── academic-paper/         ← 12-agent paper writing (v2.4)
├── academic-paper-reviewer/← 7-agent peer review (v1.4)
├── academic-pipeline/      ← 11-stage orchestrator (v2.8)
├── shared/                 ← Cross-skill data contracts
├── examples/showcase/      ← Real pipeline output samples
├── CONTRIBUTING.md
└── README.md
```

---

## Contributing / 贡献

See [CONTRIBUTING.md](CONTRIBUTING.md) for guidelines.

---

## License / 许可

[CC BY-NC 4.0](https://creativecommons.org/licenses/by-nc/4.0/)

Free to share and adapt for non-commercial use with attribution.

Based on [academic-research-skills](https://github.com/Imbad0202/academic-research-skills) by Cheng-I Wu.
