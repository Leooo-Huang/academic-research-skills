# Contributing to Academic Research Skills

Thank you for your interest in contributing. This project is a collection of Claude Code skills for academic research. Contributions that improve coverage, accuracy, and usability are welcome.

---

## What We Accept

| Type | Examples | Notes |
|------|---------|-------|
| Bug fixes | Incorrect schema field, broken workflow logic | Preferred — small and focused |
| Skill improvements | Better search queries, improved agent instructions | Must not reduce existing functionality |
| New references | Better evidence tier definitions, new venue lists | Keep references/ files lean |
| New templates | Output templates for edge cases | Must conform to shared handoff schemas |
| New skills | Entirely new capability | Discuss in an Issue first |
| Documentation | README improvements, SKILL.md clarifications | Welcome |

## What We Do NOT Accept

- Changes that break backwards compatibility with existing handoff schemas
- Skills that require paid external APIs (all tools must work with free-tier access)
- Agent instructions that produce unverified or fabricated academic content
- Changes that add mandatory manual steps to otherwise automated pipelines

---

## Before You Start

1. **Open an Issue first** for new skills or significant changes — describe the problem you're solving and your proposed approach. This prevents duplicate work and misaligned PRs.
2. **Small PRs are preferred** — one concern per PR. A PR that fixes one schema field will merge faster than one that rewrites three SKILL.md files.
3. **Test your changes** — run your modified skill end-to-end and include the output in your PR description or as an example file.

---

## Setting Up

```bash
# Clone to your skills directory
git clone https://github.com/Imbad0202/academic-research-skills.git ~/.claude/skills/academic-research-skills

# Create a branch for your work
cd academic-research-skills
git checkout -b feat/your-feature-name
```

No build step required. Skill files are plain Markdown with YAML frontmatter.

---

## File Structure

```
academic-research-skills/
├── SKILL.md                          ← (no top-level skill)
├── README.md
├── CONTRIBUTING.md
├── CHANGELOG.md
├── shared/
│   └── handoff_schemas.md            ← Cross-skill data contracts — coordinate before changing
├── discovery/
│   ├── SKILL.md                      ← Skill entrypoint — must have valid YAML frontmatter
│   ├── agents/
│   │   └── discovery_agent.md
│   ├── references/
│   │   └── arxiv_categories.md
│   └── templates/
│       └── paper_corpus_template.md
├── deep-research/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── templates/
├── academic-paper/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── templates/
├── academic-paper-reviewer/
│   ├── SKILL.md
│   ├── agents/
│   ├── references/
│   └── templates/
└── academic-pipeline/
    ├── SKILL.md
    ├── agents/
    ├── references/
    └── templates/
```

---

## SKILL.md Requirements

Every SKILL.md must have valid YAML frontmatter:

```yaml
---
name: skill-name
description: "One-sentence description used for skill detection. Must include trigger keywords."
metadata:
  version: "X.Y"
  last_updated: "YYYY-MM-DD"
  depends_on: "other-skill (optional), ..."   # omit if none
allowed-tools: WebSearch, WebFetch            # comma-separated list of tools this skill uses
---
```

**Rules**:
- `version` and `last_updated` must be under `metadata:` — claude.ai upload will reject files with frontmatter at root level for these fields
- `description` must include trigger keywords so Claude can detect when to activate this skill
- `allowed-tools` must list only tools that the skill actually uses

---

## Handoff Schema Changes

`shared/handoff_schemas.md` defines the data contracts between all skills. Changes here affect every skill.

**Before modifying handoff_schemas.md**:
1. Open an Issue describing the proposed change
2. List every skill that produces or consumes the affected schema
3. Update all affected skills in the same PR
4. Add a validation rule if the new field has constraints

**Adding optional fields** (preferred — backwards compatible):
```markdown
| `new_field` | type | Description — populated by X skill; consumed by Y agent |
```

**Adding required fields** (breaking change — needs major version bump):
- Requires updating all producers to output the field
- Requires updating all consumers to validate the field
- Bump major version in all affected SKILL.md files

---

## Agent Instruction Guidelines

Agent files (`agents/*.md`) contain Claude instructions. Follow these rules:

1. **No fabrication**: Agents must never synthesize metadata from search snippets — only from fetched pages
2. **Explicit failure paths**: Every agent must document what to do when a step fails
3. **Output validation checklist**: Include a checklist at the end of each agent file that Claude can use to self-verify output
4. **Discard over guess**: When data is unavailable, discard the item — never fill in missing fields with approximations

---

## PR Checklist

Before submitting, verify:

- [ ] YAML frontmatter is valid (check with a YAML linter)
- [ ] Version bumped in the modified SKILL.md (patch for fixes, minor for new features)
- [ ] `last_updated` set to today's date (YYYY-MM-DD)
- [ ] Changelog entry added to the modified SKILL.md and to `CHANGELOG.md`
- [ ] All cross-references (Related Skills tables, depends_on fields) are updated
- [ ] If handoff schema changed: all affected skills updated in the same PR
- [ ] No mandatory API keys introduced (all tools must have a free path)
- [ ] PR description includes a brief test run output or example

---

## Versioning

We use semantic versioning at the skill level:

| Change | Version bump |
|--------|-------------|
| Bug fix, typo, clarification | Patch (X.Y → X.Y+1... wait, we use X.Y not X.Y.Z) |
| New feature, new mode, new agent | Minor (X.Y → X.(Y+1)) |
| Breaking change (removed field, incompatible schema) | Major (X.Y → (X+1).0) |

The README badge version reflects the highest version across all skills. Update the badge when any skill reaches a new milestone.

---

## Style Guide

- **Headings**: Use `##` for top-level sections, `###` for subsections
- **Tables**: Always include a header row; align columns for readability
- **Code blocks**: Use fenced code blocks with language hints (````markdown`, ````json`, ````bash`)
- **Examples**: Use realistic but clearly illustrative values (not "foo", "bar", "test")
- **Language**: English only in skill files. User-facing output may follow the user's language.
- **Length**: Prefer concise over comprehensive. Remove redundant explanations.

---

## Questions?

Open an Issue or start a Discussion. We welcome questions before implementation — it's better to align early than to submit a PR that needs significant rework.
