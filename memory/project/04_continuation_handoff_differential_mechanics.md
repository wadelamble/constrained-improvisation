# Continuation Handoff: Differential Mechanics and Manuscript Workflow

This is repository memory, not manuscript prose. It records the state of
the long-running chat that was continued in a new thread because the old
thread had become sluggish. Treat future work as continuous with that
conversation, not as a restart.

## Active Working Context

- Repo: `C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a`
- Current key draft: `content/drafts/Differential-Mechanics.md`
- Visual companion draft: `content/drafts/Differential-Mechanics-With-Diagrams.md`
- Visual assets: `content/drafts/animations`
- Asset generator: `scripts/generate_differential_mechanics_assets.py`
- Animation environment: `scripts/anim-python.ps1`

## Collaboration Standard

- The project is a manuscript building toward QFT through classical
  mechanics, symmetry, Hamiltonian mechanics, and conceptual bridges.
- The work is not standard textbook recitation. It is structure-discovery:
  finding the natural order of explanation and enforcing it.
- The prose target is dry, economical, structurally honest, and
  anti-perfunctory.
- The user wants judgment more than completionism. Say plainly when
  something works, when it is delicate, and when it is fake or generic.
- Prefer direct file work when the task is clear. Use `apply_patch` for
  manual edits. Keep commentary updates short before substantial work.
- Do not over-praise, over-explain, soften weak material, or ask
  unnecessary questions.

## Current Differential Mechanics Draft

`content/drafts/Differential-Mechanics.md` is the current combined
Hamiltonian / differential mechanics section. It has a four-part arc:

1. why Hamiltonian mechanics
2. information evolution, Liouville, and ensembles
3. Hamilton's equations and Hamiltonian construction
4. Poisson algebra, Lie-algebra perspective, and bridge to QM

Important repairs already made:

- The opening now frames Hamiltonian mechanics as the local,
  differential, kinematical formulation of mechanics before pivoting to
  information preservation.
- The draft no longer makes one oversized claim about Hamiltonian
  mechanics. It separates local differential mechanics, information
  preservation, and algebraic repackaging.
- The one-form to two-form bridge was repaired as a change of question:
  from one displaced state to patches of nearby states, not a mystical
  promotion in rank.
- A callback was added so the cross-coupled Hamiltonian equations are
  described as the dynamical face of the same pairing that appears
  geometrically as `dq^i \wedge dp_i`.
- The transition into Lie algebra was softened so it feels like a lift
  in altitude rather than a new essay.

Current judgment:

- The draft reads like a real manuscript section, not a bundle of notes.
- Remaining risks are mainly force and proportion, not architecture.
- The formerly deepest pressure points were the opening wager about
  information preservation, the one-form to two-form bridge, and the
  altitude shift into Lie algebra. All three have been repaired enough
  for the section to cohere.

## Lie Algebra / Poisson Context

The relevant hierarchy is:

```text
function -> vector field -> flow -> canonical transformations
```

- A flow is a one-parameter family of canonical transformations.
- Choosing a parameter value picks out one canonical transformation.
- A function is not the finite transformation. It encodes a Hamiltonian
  vector field.
- "Generate" is used in two nearby senses: a function generates a vector
  field, and a vector field generates a flow.
- The key bridge is `[X_f, X_g] = X_{ {f,g} }`, up to sign convention.
- This is why functions on phase space can participate in a Lie-style
  algebra through the Poisson bracket.

The quantum bridge should preserve the settled idea:

- The algebra is a bridge into QM.
- Replacing Poisson brackets with commutators transports a large part of
  Hamiltonian structure forward before the new quantum geometry is fully
  understood.
- The preferred formulation is: "the geometry changes, but the algebra
  transports."

## Visual / Animation State

The immediate previous work was a first visual-production pass for
`Differential-Mechanics`.

Created:

- `content/drafts/Differential-Mechanics-With-Diagrams.md`
- `content/drafts/animations`
- `scripts/generate_differential_mechanics_assets.py`

Current judgment of the visual layer:

- Technically productive.
- Conceptually respectable as prototypes.
- Artistically and rhetorically under-responsive.
- It often illustrates topics generically rather than answering the
  specific prose turn at the point of insertion.
- Do not assume more visuals are better. Prioritize manuscript effect.

The strongest current assets are roughly:

- `differential-one-form-to-two-form.png`
- `differential-function-to-flow.mp4`
- `differential-symplectic-patch-preservation.mp4`

Many other visuals may be placeholders and should be cut, replaced, or
reconceived.

Important correction from the new chat:

- When the user asks about "text" in visuals, they mean literal labels
  and equations inside diagrams/animations colliding with other text or
  visual elements.
- Do not interpret that as merely connecting animations to manuscript
  prose.
- Evaluation must be based on rendered output, not source-code intent.
- For PNGs, inspect the final rendered image.
- For MP4s, extract representative frames/contact sheets and inspect
  them.
- Text collision checks should include text-vs-text overlap, text near
  figure edges, text over plotted elements, labels too close to arrows,
  and moving elements entering label regions during animation.
- Most visuals should probably carry less in-frame prose. The manuscript
  already carries the explanation; the visual should carry geometry.

## Related Files Worth Knowing

- `notes/worked/the-hamiltonian-2.md`
- `notes/worked/lie-algebra-of-phase-space-human-v1.md`
- Older feeder notes exist, but these are the main Hamiltonian-side
  continuity files.

## Broader Project Context

The repo also contains QFT drafts and worked notes. The broader project
memory is in `memory/project/03_true_chat_summary.md`.

Stable QFT-side commitments include:

- QFT is the capstone where symmetry, relativity, locality, and quantum
  amplitudes come due.
- The deepest motivation is local relativistic mediation of influence,
  not the slogan "QM plus relativity."
- The operator-in-spacetime route and the spring-lattice-to-Klein-Gordon
  route are both central.
- Particle means excitation of a field mode above the vacuum, not a
  primitive object.
- Fock space, correlators/propagators/amplitudes, gauge-mediated force,
  and QED recovering classical electromagnetism are structurally
  important.

Do not flatten future work into a standard textbook order merely because
that order is familiar.
