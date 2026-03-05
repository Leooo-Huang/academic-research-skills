# Academic Research Skills Changelog

Cross-skill fixes and update history. Synced from [hei-skills-package](https://github.com/Imbad0202/hei-skills-package).

---

## 2025-03-05

### v2.2 / v1.3 Cross-Agent Quality Alignment Update (4 skills)

**Files changed**: 19 files across 4 skills (+550 lines)

**deep-research v2.2**:
- Added cross-agent quality alignment definitions (peer-reviewed, currency rule, CRITICAL severity, source tier, minimum source count, verification threshold)
- Synthesis anti-patterns, Socratic quantified thresholds & auto-end conditions
- Reference existence verification (DOI + WebSearch)
- Enhanced ethics reference integrity check (50% + Retraction Watch)
- Mode transition matrix

**academic-paper v2.2**:
- 4-level argument strength scoring with quantified thresholds
- Plagiarism & retraction screening protocol
- F11 Desk-Reject Recovery + F12 Conference-to-Journal Conversion failure paths
- Plan → Full mode conversion protocol

**academic-paper-reviewer v1.3**:
- DA vs R3 role boundaries with explicit responsibility tables
- CRITICAL finding criteria with concrete examples
- Consensus classification (CONSENSUS-4/3/SPLIT/DA-CRITICAL)
- Confidence Score weighting rules
- Asian & Regional Journals reference (TSSCI + Asia-Pacific + OA options)

**academic-pipeline v2.2**:
- Checkpoint confirmation semantics (6 user commands with precise actions)
- Mode switching rules (safe/dangerous/prohibited matrix)
- Skill failure fallback matrix (per-stage degradation strategies)
- State ownership protocol (single source of truth with write access control)
- Material version control (versioned artifacts with audit trail)

---

## 2026-03-01

### Simplify Academic Research Skills SKILL.md (4 files)

**Motivation**: 4 academic research skills totaled 2,254 lines with significant cross-skill duplication and redundant inline content already available as template files.

**Files changed**:
- `academic-paper-reviewer/SKILL.md` (570→470, -100 lines)
- `academic-pipeline/SKILL.md` (675→535, -140 lines)
- `deep-research/SKILL.md` (469→435, -34 lines)
- `academic-paper/SKILL.md` (540→443, -97 lines)

**Changes**:
- A: Reviewer — removed inline templates, replaced with `templates/` file references (kept Devil's Advocate special format notes)
- B: Pipeline — removed ASCII state machine, replaced with concise 9-stage list + reference
- C: Pipeline — simplified Two-Stage Review Protocol to inputs/outputs/branching only
- D: 3 skills — "Full Academic Pipeline" section replaced with one-line reference to `academic-pipeline/SKILL.md`
- E: 4 skills — trimmed routing tables, removed HEI routes already defined in root CLAUDE.md
- F+G: Removed duplicate Mode Selection sections from deep-research and academic-paper
- H: academic-paper Handoff Protocol simplified to overview + upstream reference
- I: academic-paper Phase 0 Config replaced with reference to `agents/intake_agent.md`
- J: 4 skills — Output Language sections reduced to 1 line each
- K: Fixed revision loop cap contradiction (pipeline overrides academic-paper's max 2 rule)

**Result**: 2,254→1,883 lines (-371 lines, -16.5%), all 371 quality tests passed

**Lesson**: Inlining full template content in SKILL.md is unnecessary redundancy — a one-line reference suffices when template files exist at the correct path
