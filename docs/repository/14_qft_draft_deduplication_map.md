# Deduplication map for `02_qft_section_draft.md`

This file identifies the known duplicated block inside the current QFT draft and gives a conservative plan for cleanup. It is a metadata file, not manuscript prose.

## Purpose

The current QFT draft on disk is conceptually complete but contains duplicated middle material. This file exists to prevent ad hoc cleanup and to preserve deliberate comparison logic.

## Duplicate region

The duplicate region begins at the heading:

`## Reconstructed second major block`

After that point, the draft contains second versions of material already treated earlier.

## Repeated sections

The repeated sequence currently includes:
- `## Working in the momentum basis`
- `## Quantizing the modes`
- `## Fock space`
- `## The spaces of QFT`
- `## What the theory calculates`

The later sections following these — path integral onward — are not duplicated in the same way.

## Provisional judgment about which versions to keep

### Likely keep as canonical
The later, reconstructed versions likely deserve to survive because they are:
- more integrated with the later chapter blocks
- more explicit about the field → mode → Fock-space → particle chain
- more aligned with the later repository support notes

### Likely remove or heavily mine
The earlier versions of the duplicated sections are likely candidates for removal after comparison, but only after checking whether they contain:
- slower introductory transitions
- cleaner wording in a few local passages
- better pacing in one or two explanations

## Cleanup procedure

1. Compare the earlier and reconstructed versions section by section.
2. Choose the reconstructed section as provisional base.
3. Salvage any superior local explanatory sentences from the earlier version if needed.
4. Delete the weaker duplicated version.
5. Repair transitions so the chapter reads continuously from:
   - KG vs Schrödinger
   - to momentum basis
   - to quantized modes
   - to Fock space
   - to spaces of QFT
   - to what the theory calculates
6. Re-read for pacing only after structural cleanup is complete.

## Why this matters

If the duplication is not resolved first:
- later critiques become fuzzy,
- sentence-level revision becomes wasteful,
- and agents may accidentally blend two competing middle structures rather than improving one.

## Important caution

Do not treat the presence of duplication as evidence that the middle content itself is weak or dispensable. The issue is not conceptual absence. The issue is duplicated realization. The chapter’s middle is one of its most important load-bearing regions and should be cleaned carefully rather than compressed aggressively.
