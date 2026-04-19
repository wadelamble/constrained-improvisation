# Authority and precedence map

This file defines which repository files should be treated as authoritative for which kinds of decisions. The aim is to prevent later work from flattening different file roles into one another.

## Core rule

No single file is authoritative for everything.

Use:
- outlines for **structure**
- chapter draft for **current prose**
- project memory for **deep intent and rejected routes**
- feedback for **current weaknesses**
- worked notes for **missing explanatory rungs**

## Primary authority by task

### For chapter architecture
Primary:
- `05_mother_outline_updated.md`

Supporting:
- `01_mother_outline.md`
- `03_true_chat_summary.md`

Use `05` when deciding the current best shape of the QFT chapter.
Use `01` when repository-wide scaffolding or broader mother-outline logic matters.
Use `03` to check whether a structural simplification would violate project memory.

### For current manuscript prose
Primary:
- `02_qft_section_draft.md`

Supporting:
- `04_feedback_on_qft_draft.md`
- `07_high_value_displaced_material.md`

Use `02` as the current prose base.
Use `04` before revising it.
Use `07` only when looking for salvageable source-language or alternate explanatory blocks.

### For project intent, settled conclusions, and rejected framings
Primary:
- `03_true_chat_summary.md`

Supporting:
- `04_feedback_on_qft_draft.md`

If there is a conflict between smooth prose in `02` and a repeated project-level commitment recorded in `03`, pause and reconcile rather than silently privileging fluent prose.

### For compressed technical chains
Primary:
- `08_modes_fock_worked_note.md`
- `09_correlators_propagators_scattering_note.md`
- `10_gauge_qed_coulomb_worked_note.md`

These are not chapter prose. They are support notes meant to strengthen or clarify compressed sections of `02`.

### For non-QFT manuscript dependencies
Primary:
- `06_qft_dependency_summaries.md`

Use this when revising QFT passages that rely on earlier manuscript sections, especially to avoid rederiving earlier material unnecessarily or introducing terms without context.

## Conflict-resolution rules

### Rule 1
If `02_qft_section_draft.md` and `05_mother_outline_updated.md` disagree, prefer `05` for structure and `02` for currently realized prose.

### Rule 2
If `02_qft_section_draft.md` sounds smooth but `03_true_chat_summary.md` says the project repeatedly rejected that framing, prefer `03` unless there is a deliberate documented reason to reverse course.

### Rule 3
If a section in `02` feels compressed and a worked note exists on the same topic, the worked note should be treated as the better explanatory reservoir, not as competing prose.

### Rule 4
Do not mine `07_high_value_displaced_material.md` indiscriminately. It contains high-value salvage, not automatically canonical material.

## Current high-confidence canonical claims

These are currently safe to treat as stable:
- QFT is the capstone that completes the manuscript’s earlier arc.
- The chapter should use both the operator-in-spacetime route and the classical-field / quantization route.
- Fields are primary; particles are derived excitations.
- The spring-lattice / KG construction is central rather than ornamental.
- The momentum-basis / mode decomposition is essential.
- Fock space is structurally necessary, not optional.
- The chapter must explain what QFT actually calculates.
- Path integrals are important but are not the chapter’s primary ontology.
- Gauge fields explain force through local symmetry.
- QED should recover Coulomb / classical electromagnetism as a payoff.

## Current live but not fully settled matters

Still adjustable:
- exact depth of LSZ treatment
- exact weight of the path-integral section
- how much explicit derivation to give in the QED-to-Coulomb payoff
- how much fermion detail belongs in this chapter rather than later
- exact later technical boundary (renormalization, gauge fixing, etc.)

## Practical guidance for later revision

When revising:
1. decide whether the change is structural, prose-level, or explanatory
2. consult the file authoritative for that type of change
3. check `03_true_chat_summary.md` before making any change that alters the chapter’s conceptual identity
4. do not treat support notes as finished prose, but do treat them as high-authority explanatory reservoirs
