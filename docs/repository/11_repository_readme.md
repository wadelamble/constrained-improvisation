# Repository README for QFT handoff

This repository is a handoff substrate for continued work on the QFT chapter of a larger physics manuscript. It is not a polished publication package. It is a structured working archive meant to let a later human or agent continue development without losing the project’s logic, priorities, buried reasoning, or partial prose.

The repository currently contains four broad kinds of material:

1. **Structural documents** — outlines and architecture
2. **Chapter prose** — the current QFT draft
3. **Project memory and critique** — what the conversations established, what remains weak, what to preserve
4. **Support notes** — slower worked notes on compressed technical chains the draft currently handles briefly

The guiding idea is that no single file is sufficient on its own. The chapter draft shows what currently exists in prose. The outlines show what the chapter is trying to be. The memory file preserves the project’s deeper commitments and rejected framings. The support notes preserve explanatory rungs that may later be folded into the chapter.

## File map

### Structural files
- `01_mother_outline.md` — broad original mother outline; more infrastructural and repository-wide
- `05_mother_outline_updated.md` — later alternative outline written after the fuller QFT draft existed; sharper for the QFT chapter itself

### Main chapter prose
- `02_qft_section_draft.md` — current full QFT chapter draft on disk

### Project memory and critique
- `03_true_chat_summary.md` — deep project-memory document preserving settled, provisional, open, and rejected lines of thought
- `04_feedback_on_qft_draft.md` — editorial critique of the current QFT draft

### Dependency and salvage support
- `06_qft_dependency_summaries.md` — what the QFT chapter imports from earlier manuscript sections
- `07_high_value_displaced_material.md` — selected high-value source material not fully preserved elsewhere

### Worked technical notes
- `08_modes_fock_worked_note.md` — local field → modes → quantized oscillators → Fock space → particle emergence
- `09_correlators_propagators_scattering_note.md` — local fields → correlators → propagators → in/out states → S-matrix → LSZ → beam-lab interpretation
- `10_gauge_qed_coulomb_worked_note.md` — global symmetry → local symmetry → covariant derivative → gauge field → QED → Coulomb recovery → classical EM regime

## What this repository is for

This repository is meant to support:
- continued drafting of the QFT chapter
- structural comparison of alternate outlines
- later prose strengthening without losing the project’s own architecture
- selective mining of support notes into cleaner manuscript prose
- future chapter cleanup, especially deduplication and weight redistribution

It is **not** meant, yet, to be:
- a clean publication draft
- a full markdown conversion of the entire manuscript
- a full technical field-theory reference
- a general physics knowledge base detached from this manuscript’s goals

## Immediate practical use

A later human or agent should normally begin with:
1. `05_mother_outline_updated.md`
2. `02_qft_section_draft.md`
3. `04_feedback_on_qft_draft.md`
4. `03_true_chat_summary.md`

Then use the support notes as needed.

## Current major caution

The current QFT draft exists in full, but contains a duplicated middle block. That is a structural cleanup issue, not a content absence. See the dedicated deduplication map for handling guidance.

## Current major missing non-meta content

Only one clearly important non-meta support gap remains:
- a slower worked note on fermionic fields

Everything else is now optional strengthening or cleanup rather than core absence.
