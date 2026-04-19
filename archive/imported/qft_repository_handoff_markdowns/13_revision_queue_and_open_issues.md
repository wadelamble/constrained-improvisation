# Revision queue and open issues

This file records the current post-handoff revision queue for the QFT chapter and its repository materials. It is deliberately limited to substantive issues, not workflow chatter.

## Tier 1 — highest-priority issues

### 1. Deduplicate the middle of `02_qft_section_draft.md`
The draft currently contains a duplicated middle block, including repeated coverage of:
- working in the momentum basis
- quantizing the modes
- spaces of QFT
- what the theory calculates

This is the most urgent structural cleanup issue because it affects every later read of the chapter.

### 2. Decide which middle-block version survives
The reconstructed middle block appears generally stronger, but this should be judged explicitly rather than assumed. A controlled comparison should determine:
- which version is canonical
- whether any material from the weaker version should be salvaged
- how transitions must be repaired after deduplication

### 3. Reassess weight distribution after deduplication
The earlier half of the chapter is more developed and patient than the later half. After deduplication, reassess:
- whether the scalar-field construction is too dominant
- whether the later half is too summary-like
- where added breathing room is most needed

## Tier 2 — strong next candidates

### 4. Create a worked fermions note
This is the clearest remaining non-meta support gap. The chapter has a fermions section, but it is more compressed than the other major chains now covered by dedicated notes.

The note should likely cover:
- why spinors are different kinds of objects from scalars
- why the Dirac field is first-order and spinorial
- why anticommutators replace commutators
- how antiparticles arise in the mode expansion
- why Pauli exclusion follows algebraically

### 5. Strengthen the deepest motivation hierarchy in the “why QFT?” section
The draft currently lists several motivations well, but could make the hierarchy sharper:
- deepest: need for local carriers of influence compatible with relativity
- then fixed particle number and inserted potentials as related deficiencies

### 6. Decide whether the unitarity section needs more room
The section is good and project-specific, but may still be short relative to its conceptual importance.

## Tier 3 — likely later refinement

### 7. Evaluate whether the path-integral section needs more explicitness
The current balance is good in principle, but it remains possible that the section needs:
- slightly more generation-functional detail
- or slightly more relation-to-correlator emphasis

### 8. Consider expanding the QED payoff slightly
Possible modest strengthening targets:
- one slower sentence on the \(1/\mathbf q^2 \to 1/r\) Fourier relation
- one slower sentence on classical EM as coherent-field regime
- or an appendix-level derivational sketch rather than more in-chapter prose

### 9. Tighten the opening after the middle is stabilized
Do this only after deduplication and weight redistribution. The opening should be judged against the now-full chapter rather than revised preemptively.

## Tier 4 — deferred unless the chapter grows

These are not currently missing, just deferred:
- technical LSZ derivation
- renormalization / regularization details
- gauge fixing / ghosts / BRST
- non-Abelian technical depth
- Standard Model expansion

## Current repository-level judgment

The handoff is already strong enough to continue serious work. The queue above is about moving from “strong substrate” toward “stable working draft,” not about rescuing a missing chapter.
