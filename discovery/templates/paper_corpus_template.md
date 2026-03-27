# Paper Corpus Template — Schema 2 Compliant (Discovery v2.0)

<!--
  This template is used by discovery_agent to assemble the output Bibliography artifact.
  It conforms exactly to shared/handoff_schemas.md Schema 2, with optional
  community_signals and discovery_phases fields added by discovery v2.0.
  Fill every required field. Do not omit fields — missing required fields trigger HANDOFF_INCOMPLETE.
-->

## Discovery Output: [TOPIC]

**Material Passport**:
- Origin Skill: discovery
- Origin Mode: [standard | recent | comprehensive | venue | pipeline]
- Origin Date: [YYYY-MM-DDTHH:MM:SSZ]
- Verification Status: VERIFIED
- Version Label: discovery_v2

---

**Community Signals** *(Phase A output — omit block if Phase A yielded no signals)*:
- Trending Keywords: [keyword_1, keyword_2, keyword_3]
- Hot Papers Surfaced: [N] (arXiv IDs: [list])
- Pain Points Identified: [N] ([brief description of each])
- Sources Searched: [X/Twitter | Reddit | GitHub | HuggingFace | arXiv]
- Collection Date: [YYYY-MM-DDTHH:MM:SSZ]

---

**Search Strategy**:
- Databases: Semantic Scholar API (WebFetch), arXiv (WebSearch + WebFetch), Papers With Code (WebSearch)
- Community Sources: [list of Phase A platforms searched, or "N/A — Phase A skipped"]
- Keywords: [list every search term used across Phases A–D]
- Inclusion: [date range], arXiv preprints and published papers, relevance_score ≥ 4
- Exclusion: Papers failing WebFetch verification; relevance_score ≤ 3
- Date Range: [YYYY-MM-DD] to [YYYY-MM-DD]
- Verification Method: WebFetch on https://arxiv.org/abs/{arxiv_id} for each candidate; DOI resolution for published papers

**Coverage Assessment**: [2-4 sentences honestly describing what was found and what gaps remain. E.g.: "Strong coverage of arXiv preprints and Semantic Scholar-indexed papers. Limited coverage of IEEE Xplore papers behind paywall. Community signals identified 3 trending keywords that steered search toward emerging subfields. Citation expansion added 12 papers not found in initial search."]

**Minimum Sources**: [N] (required: 10 minimum)

---

### Sources

<!-- Repeat this block for each verified paper. Assign sequential IDs: [S01], [S02], ... -->
<!-- Sort by relevance_score descending, then by citationCount descending within same score -->

**[S01]** [Last, F., Last, F., & Last, F.]. ([YYYY]). [Paper Title]. *[Journal/Venue/arXiv preprint arXiv:YYMM.NNNNN]*. [https://arxiv.org/abs/YYMM.NNNNN | https://doi.org/DOI]
- Type: [journal_article | conference | preprint]
- Evidence Tier: [1-7]
- Quality: [tier_1 | tier_2 | tier_3 | tier_4]
- Relevance: [core | supporting | peripheral]
- Score: [1-10]
- Citations: [N] (Semantic Scholar) | S2 ID: [paperId]
- Verified: true (WebFetch: arxiv.org/abs/YYMM.NNNNN — HTTP 200, title/abstract/authors confirmed)
- Annotation: [Sentence 1: what the paper proposes.] [Sentence 2: key quantitative result or finding.] [Sentence 3: specific relevance to the user's research topic.]

**[S02]** ...

**[S03]** ...

<!-- Continue for all verified papers, up to 100 maximum -->

---

**Discovery Summary**:
- Phase A (community): [N] trending keywords, [N] hot paper IDs surfaced from community signals
- Phase B (search): [N] candidates from Semantic Scholar API, [N] from arXiv WebSearch, [N] total after deduplication
- Phase C (verified): [N] passed WebFetch verification, [N] discarded (WebFetch failed), [N] excluded (relevance_score ≤ 3)
- Phase D (expansion): [N] new candidates from citation graph, [N] additional verified, [N] additional excluded
- Final corpus size: [N]
- Ready for handoff: [YES | NO — reason if NO]

---

<!--
  HANDOFF INSTRUCTIONS (remove this block before final output):

  To continue to deep-research (analysis only):
    Say: "Analyze these papers" or "Do a systematic review of these papers"
    deep-research will detect Has Bibliography → skip bibliography_agent search → run synthesis
    COMMUNITY_SIGNALS.pain_points will be passed to synthesis_agent for gap analysis

  To continue to academic-pipeline (full pipeline):
    Say: "Write a paper on [topic] using these papers"
    academic-pipeline Stage 1 will receive PAPER_CORPUS with bibliography_agent in VERIFY MODE
    synthesis_agent will use community_signals.pain_points for gap analysis framing

  To use standalone (no further processing):
    Output is complete. User can save and use the corpus independently.
-->
