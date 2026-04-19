# 01_mother_outline.md

## Purpose of this file

This file is the canonical structural map of the manuscript and the first-pass architectural handoff for the repository. It is not the manuscript itself, and it is not a chat log. Its job is to preserve the book's structure at a level detailed enough that a future agent can expand, rearrange, compress, or rewrite material without losing the book's governing logic.

The manuscript is not being built as a standard textbook. It is being built as a conceptual argument whose deepest organizing commitments are:

- symmetry is structurally prior,
- relativity is best understood through geometry and invariance rather than slogans,
- quantum mechanics is best introduced as a theory of state space, observables, and probability structure rather than as a bag of paradoxes,
- gauge structure and local curvature are the bridge from geometry to force,
- quantum field theory is the culmination of that story rather than an isolated technical add-on.

This file therefore does four things at once:

1. preserves the whole-book spine,
2. identifies the dependencies that the QFT chapter inherits from earlier chapters,
3. gives the most detailed architecture to the QFT chapter,
4. records strong alternate branches, unresolved placement questions, and displaced but valuable material.

This file should be the first place a future human or repository agent checks before changing structure.

---

## How to use this file

Use this file when the question is structural:

- What does the book think it is doing?
- What order are the ideas supposed to appear in?
- What must the QFT chapter accomplish?
- Which earlier sections are prerequisites and which are merely background?
- Which structural choices are canonical and which are still provisional?
- Which left-out sections are actually likely to return later?

Do **not** use this file as if it were the manuscript prose. Use `02_qft_section_full.md` for that. Do **not** use this file as the historical memory of how the project evolved. Use `03_true_chat_summary.md` for that.

---

## Status conventions

The outline below uses a deliberately explicit status vocabulary.

- **[CANONICAL]**: current best structural choice.
- **[PROVISIONAL]**: wanted, likely, but still unstable in order, emphasis, or level.
- **[ALTERNATE]**: serious rival organization still worth preserving.
- **[DEFERRED]**: important material likely to move elsewhere or later.
- **[DISPLACED]**: material that exists in the current source document but is not in its likely final location.
- **[REJECTED]**: route that should not quietly re-enter without explicit decision.

Status here refers to structure, not truth. A section may be conceptually important and still be structurally provisional.

---

## Source basis for this outline

This outline is based primarily on the uploaded manuscript document and secondarily on the established project direction from the ongoing work around the QFT chapter. Within the source document, the following strata matter most:

1. the whole-book drafted chapters before QFT,
2. the QFT notes bank,
3. the current in-draft QFT section,
4. the left-out / struck / unused QFT material,
5. the displaced but high-value QFT sections such as **The Spaces of QFT** and **Unitarity**.

This file therefore distinguishes between what is already present in prose and what is only present as outline or note material.

---

# Part I. Governing architecture of the manuscript

## 1. Governing thesis of the book [CANONICAL]

The book is trying to tell a coherent story of modern physics in which mathematical structure is not introduced as a technical overlay on top of physical intuition, but as the thing from which the physical picture becomes intelligible. The central through-lines are:

- **symmetry** as the source of structural law,
- **geometry** as the language in which invariance becomes visible,
- **probability and state space** as the proper setting for quantum theory,
- **locality and causality** as constraints that eventually force field-theoretic ontology,
- **force and interaction** as consequences of local symmetry and curvature,
- **QFT** as the point where relativistic locality, quantum structure, and variable particle number finally live in one framework.

The manuscript is therefore not organized historically and not organized as a standard undergraduate course. It is organized by what the author takes to be the deepest explanatory dependencies.

### 1.1 What this means in practice

- The book does not begin with Newtonian mechanics as the ultimate ground floor.
- It does not present relativity as a list of weird experimental facts.
- It does not present quantum mechanics as a sequence of mysteries followed by recipes.
- It does not present electromagnetism as a separate classical kingdom and only later explain that QED exists.
- It does not present QFT as merely a way to draw Feynman diagrams.

Instead, it attempts to move from structural prerequisites to richer theories by asking: what new mathematical space or local constraint becomes necessary once the previous framework has done all it can do?

### 1.2 Core methodological principle [CANONICAL]

The book prefers **conceptual inevitability** over historical chronology.

This means each chapter should answer two questions:

1. What does the previous framework already do well?
2. What exact structural demand does it fail to satisfy, forcing the next framework?

That principle is especially important for the QFT chapter. QFT must not appear as "and here is the next technical toolkit." It must appear as the theory forced on us by the simultaneous demands of relativistic locality, quantum state structure, and particle creation/annihilation.

---

## 2. Whole-book spine [CANONICAL]

### 2.1 Front matter / introduction

**Function:** establish audience, method, ambition, and nonstandard ordering.

What this part must do:

- tell the reader the book aims at conceptual rather than drill-based mastery,
- make clear that mathematics will appear as explanation rather than mere formalism,
- justify why the sequence departs from conventional pedagogy,
- establish that the manuscript is trying to offer a story of modern physics rather than a survey of disconnected topics.

### 2.2 Symmetry

**Function:** establish transformations, generators, representations, commutators, conserved quantities, and the idea that physical law can be read from invariance.

This chapter is the true beginning of the book's logic. It should establish:

- finite versus infinitesimal transformations,
- discrete versus continuous symmetry,
- generators,
- momentum as generator of translations,
- angular momentum and noncommutation,
- the passage from group structure to geometry and stage.

**Dependency relevance to QFT:** enormous. QFT will inherit generators, commutators, translation symmetry, momentum, representation language, and the idea that fields transform under spacetime and internal symmetries.

### 2.3 Relativity

**Function:** establish Minkowski structure, light cones, Lorentz transformations, proper time, 4-momentum, relativistic dispersion, and waves as representations of symmetry.

This chapter should do more than teach kinematics. It should establish the geometric notion of causality and the sign structure that later reappears in wave equations and hyperbolic propagation.

**Dependency relevance to QFT:** decisive. The QFT chapter needs:

- spacetime locality,
- light-cone causality,
- relativistic energy-momentum relation,
- the mass shell,
- wave representations consistent with Poincaré symmetry.

### 2.4 Quantum mechanics

**Function:** establish Hilbert space, state, observable, representation, Born rule, unitarity, Schrödinger evolution, and the experimental pressure that forces the formalism.

This chapter is the origin of the state/operator framework that QFT later reassigns across spacetime and Fock space.

**Dependency relevance to QFT:** decisive. The QFT chapter inherits:

- operator language,
- state versus observable distinction,
- unitary evolution,
- basis / representation logic,
- probability amplitude structure,
- nonclassical state composition,
- entanglement and the distinction between nonlocal state description and local signal constraints.

### 2.5 Change, curvature, gauge, and force

**Function:** establish extremization, geodesics, gravity as curvature, local symmetry, gauge fields, and force as geometric or connection-based structure.

This chapter is the conceptual runway for gauge field theory and local mediation.

**Dependency relevance to QFT:** substantial. It gives the QFT chapter:

- action-based reasoning,
- local symmetry logic,
- gauge field motivation,
- connection/curvature language,
- a geometric understanding of why force should come from local structure rather than action at a distance.

### 2.6 Quantum field theory

**Function:** unify quantum state structure with relativistic locality and variable particle number by placing observables in spacetime and quantizing fields.

This chapter is not merely another chapter. It is the culmination of the book's governing arc.

### 2.7 Beyond / aftermath / recovery

**Function:** recover classical interaction laws, possibly discuss standard model structure, and clarify how classical descriptions emerge from QFT limits.

Depending on the final manuscript plan, some of this may live inside the QFT chapter or immediately after it.

---

## 3. The book's logic as a dependency chain [CANONICAL]

The manuscript's internal dependency chain can be written compactly like this:

1. **Symmetry** tells us what kinds of invariance and generators are available.
2. **Relativity** tells us the spacetime geometry and causal structure those laws must respect.
3. **Quantum mechanics** tells us how states, observables, and amplitudes must be organized when classical state description fails.
4. **Gauge and curvature** tell us how local symmetry becomes interaction and mediation.
5. **QFT** tells us how all of that can coexist in one framework when particle number is not fixed and locality must be built into the observables themselves.

This chain should not be broken by local rewrites. If a future agent changes chapter order or local emphasis, it should preserve this deeper dependency.

---

# Part II. Detailed chapter architecture before QFT

## 4. Introduction [CANONICAL]

### 4.1 Mission

The introduction should establish the following claims clearly and early:

- physics is a story of structure rather than an inventory of facts,
- the reader is being asked to engage conceptually, not merely computationally,
- the manuscript will pursue a modern, symmetry-first route,
- the final aim is not to avoid mathematics but to make it legible.

### 4.2 Material that belongs here

- reader note,
- statement of level and purpose,
- brief defense of nonstandard order,
- preview of the story.

### 4.3 Material that does not belong here

- long digressions on interpretation,
- too much historical narration,
- technical detail that really belongs in symmetry or QM,
- overly ornate metaphysical throat-clearing.

### 4.4 Cross-links to likely prose in `02_qft_section_full.md`

The QFT chapter introduction should echo the same promise structure established here, but more narrowly. See future `02_qft_section_full.md` §§1–3.

---

## 5. Symmetry [CANONICAL]

### 5.1 Chapter role

This chapter should make the reader comfortable with the idea that transformations are not decorative operations on pre-existing laws. They are among the deepest clues to what the laws can be.

### 5.2 Core subsections

#### 5.2.1 Discrete symmetries

Role: easy on-ramp to transformation thinking.

#### 5.2.2 Continuous symmetries and generators

Role: establish infinitesimal transformation as the real entry point to modern physics.

#### 5.2.3 Momentum as generator of translations

Role: crucial prerequisite for QFT. This makes translation symmetry directly responsible for momentum language, Fourier basis language, and later mode decomposition.

#### 5.2.4 Commutation structure

Role: prepare the reader for noncommuting generators and later operator algebra.

#### 5.2.5 From symmetry to geometry / stage

Role: establish that symmetry structure constrains the space on which physics is written.

### 5.3 Notes for future agents

The symmetry chapter is not optional background for QFT. It is structurally upstream of:

- Poincaré transformations,
- momentum basis,
- translation eigenmodes,
- commutator structure,
- conserved quantities,
- group representation talk for particles and fields.

If QFT prose later re-explains these at length, it should do so only as reactivation, not from scratch.

---

## 6. Relativity [CANONICAL]

### 6.1 Chapter role

This chapter should give the reader a geometric conception of relativistic law, not just a toolbox for time dilation problems.

### 6.2 Core subsections

#### 6.2.1 Relativity from symmetry

Role: continuity with prior chapter.

#### 6.2.2 Geometry of relativity

Role: Minkowski interval, invariance, proper time, light cones.

#### 6.2.3 Relativistic mechanics

Role: 4-velocity, 4-momentum, mass shell.

#### 6.2.4 Spacetime fields and dispersion relation

Role: major prerequisite for QFT. Introduces field/wave language in relativistic setting.

#### 6.2.5 Wave packet representation and symmetry in Hilbert space

Role: important bridge from relativity into QM and later into QFT.

### 6.3 High-priority inherited concepts for QFT

The QFT chapter will need to inherit, not redundantly rederive, the following:

- null cone and causal order,
- hyperbolic spacetime sign structure,
- massive versus massless dispersion,
- momentum-space reasoning,
- plane-wave / wave packet representation,
- Poincaré covariance.

### 6.4 Structural guardrail

QFT's later comparison of Klein–Gordon and Schrödinger should explicitly lean on relativity chapter results rather than pretending the comparison arises out of nowhere.

Cross-link target: future `02_qft_section_full.md` §§5–7.

---

## 7. Quantum mechanics [CANONICAL]

### 7.1 Chapter role

Quantum mechanics introduces the new kind of state space demanded by interference, basis dependence, and probabilistic prediction.

### 7.2 Core subsections

#### 7.2.1 Seminal experiments

Role: motivate need for the formalism.

#### 7.2.2 Dirac notation and theory of QM

Role: state, measurement, representation, Born rule, probability conservation, time evolution.

#### 7.2.3 Implications of state being a wavefunction

Role: sets up later tension between wavefunction and field.

#### 7.2.4 Entanglement and Bell

Role: clarifies difference between global state structure and local causality.

### 7.3 High-priority inherited concepts for QFT

- state versus operator distinction,
- unitary time evolution,
- basis changes,
- superposition,
- measurement probabilities,
- global state structure,
- the fact that nonlocal state description is not the same as signal nonlocality.

### 7.4 Structural guardrail

The QFT chapter should not portray ordinary QM as "wrong." It should portray it as structurally incomplete for relativistic local interaction and variable particle number.

Cross-link targets: future `02_qft_section_full.md` §§2, 4, 8, 12.

---

## 8. Change, curvature, gauge, and force [CANONICAL]

### 8.1 Chapter role

This section should make local geometry and local symmetry look like natural precursors to force laws. It should also provide the action-based habits of thought that make the path integral later feel like an extension rather than a new religion.

### 8.2 Core subsections

#### 8.2.1 Symmetry, parallel transport, and extremization

Role: bridge from geometry to dynamics.

#### 8.2.2 Gravity and general relativity

Role: shows what it means for geometry itself to carry force.

#### 8.2.3 Gauge forces

Role: absolutely central for QFT. The notions of local symmetry, gauge field, continuity equation, and force from gauge structure must already be visible here.

### 8.3 High-priority inherited concepts for QFT

- extremization / action,
- local symmetry,
- gauge field as necessary connection-like structure,
- force mediation not as action at a distance but as local field structure.

### 8.4 Structural guardrail

The QFT chapter should use this prior conceptual runway so that gauge fields do not enter as arbitrary new machinery.

Cross-link targets: future `02_qft_section_full.md` §§11, 14, 15.

---

# Part III. The QFT chapter: canonical architecture

## 9. Chapter-level mission of QFT [CANONICAL]

The QFT chapter must do more than define a formalism. It must complete the manuscript's story.

It should answer the following questions:

1. Why is ordinary quantum mechanics not enough once relativistic locality and variable particle number matter?
2. Why are fields, not only particles or wavefunctions, the right local objects?
3. What changes when observables are attached to spacetime points?
4. How does a classical field become a quantum field?
5. How do particle states reappear from that structure rather than being assumed from the start?
6. What does the theory calculate?
7. How do interactions and gauge fields enter?
8. How does a familiar classical force law emerge from the field-theoretic picture?

### 9.1 Things the chapter must not do

- It must not leap straight to Feynman diagrams without ontology.
- It must not gesture at path integrals ceremonially and move on.
- It must not treat the field as just the wavefunction renamed.
- It must not overstate causal failure in ordinary QM in sloppy ways.
- It must not leave the reader without some clear sense of what particles are in QFT.

---

## 10. Internal architecture of the QFT chapter [CANONICAL with provisional subsections]

### 10.1 Chapter introduction [CANONICAL]

**Role:** frame QFT as the culmination of the book's logic.

**Must do:**

- remind the reader that symmetry, relativity, QM, and gauge ideas are now converging,
- state that QFT will diagnose the limits of early QM, then build the field-theoretic answer,
- promise both ontological clarity and calculational clarity.

**Must not do:**

- over-explain background already covered,
- begin with overly technical machinery,
- begin with renormalization or standard-model survey.

**Likely prose target:** `02_qft_section_full.md` §1.

---

### 10.2 Why early quantum mechanics is not enough [CANONICAL]

This section is conceptually central. It must be rewritten into one stable, non-duplicative argument.

#### 10.2.1 Main subclaims

- nonrelativistic Schrödinger evolution is not built for relativistic local propagation,
- fixed-particle-number state spaces are too small,
- ordinary QM lacks native local mediating degrees of freedom for interaction,
- potentials enter as inserted structures rather than explained local fields.

#### 10.2.2 Best emphasis ordering [CANONICAL]

1. relativistic mismatch,
2. locality / mediation problem,
3. particle-number problem,
4. potentials as symptomatic rather than separate.

#### 10.2.3 Strong alternate ordering [ALTERNATE]

1. local mediation problem first,
2. relativistic equation mismatch second,
3. variable particle number third.

This alternate route may be stronger if the author wants to foreground ontology over PDE type.

#### 10.2.4 Structural note

The current manuscript already has this material, but it is duplicated and partly unstable. Consolidation required.

**Likely prose target:** `02_qft_section_full.md` §2.

---

### 10.3 Two routes into QFT [CANONICAL]

This is a major conceptual insight in the current draft and should probably remain explicit.

#### Route A: put observables in spacetime

This is the more ontological route. It starts from QM's operator framework and asks where spacetime locality should live. The answer is: in the observables themselves, not merely in a global state description.

#### Route B: quantize a classical relativistic field

This is the more procedural route. It starts with a classical field already built to satisfy relativistic propagation requirements, then quantizes its degrees of freedom.

#### Why both routes should appear [CANONICAL]

Because together they answer both:

- what the ontology is,
- how the practical free theory is built.

#### Risk to avoid

The chapter must not let these feel like two unrelated introductions. They must converge.

**Likely prose targets:** `02_qft_section_full.md` §§3–5.

---

### 10.4 Operators in spacetime [CANONICAL]

This is one of the strongest pieces already in the source material.

#### Must establish

- Schrödinger versus Heisenberg pictures,
- moving time dependence to operators,
- local operator-valued fields,
- field operator and conjugate momentum,
- equal-time canonical commutators,
- microcausality at spacelike separation,
- optional field-functional representation of states.

#### Structural importance

This section gives the deepest ontological answer available in the current project: QFT is what happens when the observables of quantum theory become local spacetime objects.

#### Placement note [CANONICAL]

This should come **before** the spring-lattice quantization route, so that quantization of the field feels like construction of the answer rather than arbitrary technical detour.

#### Risk to avoid

Do not let the functional Schrödinger picture become the main track. It should support, not dominate.

**Likely prose target:** `02_qft_section_full.md` §4.

---

### 10.5 Classical field model to be quantized [CANONICAL]

This section should begin the constructive route.

#### Main choice [CANONICAL]

Use the spring-lattice / bead-lattice model with nearest-neighbor coupling and on-site restoring term.

#### Why this choice remains strong

- it makes locality visible,
- it makes propagation visible,
- it gives a concrete source of the mass scale / rest-frequency term,
- it yields a clean route to Klein–Gordon,
- it naturally sets up normal modes and later quantization.

#### Must establish

- degrees of freedom at sites,
- Lagrangian,
- equation of motion,
- dispersion relation,
- meaning of the on-site term,
- continuum limit,
- emergence of KG structure.

#### Structural note

The spring model is more than a pedagogical toy. In this manuscript it is the conceptual engine that ties locality, mass scale, and field propagation together.

**Likely prose target:** `02_qft_section_full.md` §5.

---

### 10.6 Why Klein–Gordon and not Schrödinger [CANONICAL]

This section is motivational and conceptual, not merely classificatory.

#### Must establish

- parabolic vs hyperbolic PDE structure,
- imaginary versus real mode frequencies,
- diffusion-like spreading versus causal wave propagation,
- relation between mixed sign structure and Minkowski interval,
- why hyperbolic structure respects finite-speed propagation.

#### Dependency note

This section should explicitly rely on the relativity chapter's discussion of the interval and light cone.

#### Risk to avoid

Do not overclaim that Schrödinger equation directly violates relativity in every practical sense. The claim should be about structural mismatch and locality properties, not cheap sensationalism.

**Likely prose target:** `02_qft_section_full.md` §6.

---

### 10.7 Working in the momentum basis / normal modes [CANONICAL]

This is the bridge from field-medium picture to particle language.

#### Must establish

- diagonalization as linear algebra,
- translation symmetry of the lattice,
- Fourier basis as eigenbasis of translation,
- decomposition into independent modes,
- diagonal Hamiltonian as sum of independent oscillator energies.

#### Why this is structurally central

It is the point where the field ceases to look like an unwieldy many-coupled system and becomes a countable set of independent oscillators, each ready for quantization.

#### Risk to avoid

Do not equate the momentum basis too quickly with “the particle is fundamentally momentum-basis.” The project has repeatedly resisted over-simplified particle language. Keep basis talk careful.

**Likely prose target:** `02_qft_section_full.md` §7.

---

### 10.8 Canonical quantization of the modes [CANONICAL but not yet fully drafted]

This section is not yet fully present in the current manuscript, but it must appear in the canonical architecture.

#### Must establish

- simple harmonic oscillator review at exactly the needed level,
- promotion of mode amplitudes and conjugate momenta to operators,
- ladder operators,
- vacuum state,
- one-particle excitations,
- multiparticle excitations,
- Fock space,
- field operator expansion in creation/annihilation operators.

#### Why this section is non-negotiable

Without it, the chapter stops just before the actual emergence of particle sectors.

#### Structural note

This is the place where the manuscript can answer, in its own vocabulary, what a particle is in QFT.

**Likely prose target:** `02_qft_section_full.md` §8.

---

### 10.9 The spaces of QFT [DISPLACED but likely returning]

This section already exists in strong form in the source document, but not in the current in-draft location. It should probably be integrated into the canonical chapter.

#### Main function

Clarify that QFT requires several spaces at once:

- spacetime,
- field configuration space,
- Hilbert/Fock space,
- momentum space,
- symmetry-group action spaces.

#### Why it matters

This is the manuscript's best way to prevent category errors such as:

- identifying Hilbert space with spacetime,
- identifying the wavefunction with the field,
- identifying a local operator with a state vector.

#### Possible placements

**Placement A [CANONICAL candidate]:** after quantization of the modes, once the reader has both local fields and Fock sectors in hand.

**Placement B [ALTERNATE]:** earlier, right after “Operators in spacetime,” as a conceptual map before constructive work.

#### Current judgment

Placement A seems stronger. Earlier placement risks abstraction before the field story has enough content. Later placement lets it function as synthesis.

**Likely prose target:** `02_qft_section_full.md` §9.

---

### 10.10 What the theory calculates [CANONICAL but only partly drafted]

This section must answer the persistent project question: what does QFT actually compute?

#### Must establish

- correlators,
- Green's functions,
- propagators,
- in/out states,
- amplitudes,
- the beam-lab interpretation of those objects,
- an LSZ-level bridge if included.

#### Structural importance

This section prevents the chapter from becoming only ontology. It is where the theory becomes operational.

#### Risk to avoid

Do not drown the section in formal scattering machinery before the reader knows why it is there.

**Likely prose target:** `02_qft_section_full.md` §10.

---

### 10.11 Path integral formulation [PROVISIONAL but strongly likely]

The project has repeatedly insisted that the path integral should appear, but not as the chapter's primary ontology.

#### Must establish

- field histories weighted by action,
- connection to least action,
- relation to operator framework,
- role in perturbation theory and diagrams,
- relation to correlators rather than mystical storytelling.

#### Structural note

The path integral should come **after** the operator and canonical free-field picture, not before.

#### Reason

The chapter's deeper claim is that QFT's ontology is best explained in terms of local operators/fields and state spaces, while the path integral is a complementary and powerful formulation.

#### Risk to avoid

Ceremonial mention. If included, it must do real work.

**Likely prose target:** `02_qft_section_full.md` §11.

---

### 10.12 Unitarity [DISPLACED but likely returning]

A strong section already exists in source form, though currently outside the active QFT draft.

#### Main function

Not merely probability conservation. Also:

- preservation of overlap,
- preservation of orthogonality and distinguishability,
- reversible closed-system evolution,
- identity-preservation in a superposed state space.

#### Placement options

**Placement A [CANONICAL candidate]:** inside QFT, after “what the theory calculates,” as a way of clarifying what amplitude evolution is constrained to preserve.

**Placement B [ALTERNATE]:** earlier in the QM chapter.

#### Current judgment

A condensed version should likely live in QM, but the more elaborate version still belongs in or near QFT because scattering, amplitudes, and field-theoretic evolution make the stakes clearer there.

**Likely prose target:** `02_qft_section_full.md` §12.

---

### 10.13 More fields: fermions and gauge fields [CANONICAL but partly outline-level]

The scalar/Klein–Gordon development is not enough. The chapter needs at least one strong extension to matter fields and gauge fields.

#### Must establish

- why scalar fields are not the whole story of matter,
- Dirac field as matter field,
- anticommutation and fermionic Fock space,
- gauge field as local interaction field,
- why local symmetry requires gauge structure.

#### Structural importance

This is where the chapter stops being a free scalar-field story and becomes genuine QFT.

**Likely prose targets:** `02_qft_section_full.md` §§13–14.

---

### 10.14 QED and recovery of classical electromagnetism [CANONICAL end-target]

This is one of the project's clearest long-term aims.

#### Must establish

- matter-gauge coupling,
- photon exchange picture at the right level,
- static / low-energy / long-distance limit leading toward Coulomb behavior,
- classical electromagnetic field as emergent or coherent limit rather than primitive starting point.

#### Why this end-target matters

It gives the chapter a concrete payoff. The reader should not feel the theory exists only to describe collider diagrams. The chapter should recover a familiar force law from the framework the book has built.

**Likely prose target:** `02_qft_section_full.md` §15.

---

### 10.15 Closing synthesis [CANONICAL]

The chapter should end by answering:

- what was added to ordinary QM,
- what stayed the same,
- why fields were necessary,
- how particles re-emerged from fields,
- why gauge structure matters,
- what classical theory is recovered in the appropriate limit.

**Likely prose target:** `02_qft_section_full.md` §16.

---

# Part IV. Alternate, displaced, and unresolved branches inside QFT

## 11. Displaced but high-value material [CANONICAL to preserve]

### 11.1 "The Spaces of QFT" [DISPLACED]

This is not scrap. It is likely future core architecture. Preserve it.

### 11.2 "Unitarity" [DISPLACED]

Likewise not scrap. Preserve it.

### 11.3 Why these are displaced rather than rejected

They are conceptually mature and align with the manuscript's deepest priorities. Their current misfit is positional, not intellectual.

---

## 12. Outline branches to preserve [ALTERNATE but important]

### 12.1 Branch centered on "Why QFT" before any ontology

This branch begins with the failings of early QM and only later introduces fields. It remains strong because it foregrounds necessity.

### 12.2 Branch centered on "Operators in spacetime" first

This branch begins by relocating observables into local spacetime, then builds the classical and canonical machinery afterward. It is ontologically elegant and likely the better opening.

### 12.3 Branch centered on "Spaces of QFT" very early

This branch could work for a more abstract reader, but current judgment is that it risks becoming too schematic before the physics is felt.

Status: **[ALTERNATE / probably not preferred]**.

### 12.4 Branch centered on path integral early

Status: **[REJECTED]** for this manuscript's present commitments.

Reason: it conflicts with the desire to make operator-in-spacetime ontology primary.

---

## 13. Structural questions still open [PROVISIONAL]

### 13.1 Where exactly should "Spaces of QFT" go?

Current preference: after free-field quantization, before or alongside "what the theory calculates."

### 13.2 How much LSZ should appear?

Current preference: conceptual bridge level, not full technical derivation.

### 13.3 How much path integral detail is right?

Current preference: enough to make it a real second formulation, not enough to displace the operator narrative.

### 13.4 Should unitarity be a stand-alone QFT subsection or distributed across QM and QFT?

Current preference: brief premise in QM, developed consequence in QFT.

### 13.5 How far should the chapter go toward standard model material?

Current preference: enough to motivate Dirac fields, gauge fields, and QED, but not enough to collapse into a standard model survey.

---

# Part V. Canonical chapter-by-chapter outline with explicit status and cross-links

## 14. Full manuscript outline at first-pass detail

### 14.1 Introduction [CANONICAL]

- reader note
- why this book exists
- how to read it
- nonstandard order
- conceptual promises

### 14.2 Geometry and Physics [CANONICAL but possibly integrated]

- early framing bridge from math to physical law

### 14.3 Symmetry [CANONICAL]

- discrete symmetries
- generators of continuous transformations
- momentum as generator of translations
- commutation
- symmetry to geometry
- symmetry to stage

### 14.4 Relativity [CANONICAL]

- relativity from symmetry
- path of reasoning to relativity
- geometry of relativity
  - invariance
  - proper time
  - physical invariance
  - light cones
  - twin paradox
- relativistic mechanics
  - relativistic force and dynamics
  - spacetime fields
  - dispersion relation
  - complex-valued waves
  - spin and internal symmetries in relativity
- wave packet representation of symmetry
  - Heisenberg symmetry
  - symmetry representation in Hilbert space
  - uncertainty and operator relations from Heisenberg commutator
  - boosts and uncertainty
  - wave representation summary

### 14.5 Quantum Mechanics [CANONICAL]

- seminal experiments
  - photoelectric effect
  - double slit
  - Stern–Gerlach
- Dirac notation
- theory of QM
  - state
  - measurements and representations
  - Planck's constant and wave representation
  - Born rule
  - collapse
  - examples
  - probability conservation and real measurements
  - implications of state being a wavefunction
  - time evolution and Schrödinger equation
- experiments explained
  - photoelectric effect
  - double slit
  - Stern–Gerlach revisited
  - entanglement and Bell revisited

### 14.6 Change and Curvature [CANONICAL]

- symmetry, parallel transport, and extremization
  - geodesics
  - straight line in flat space
  - minimizing length on sphere
  - from geometry to physics
- gravity and general relativity
  - equivalence principle
  - Einstein field equation
  - implications
    - time dilation
    - gravitational lensing
    - black holes
    - gravitational waves
- gauge forces
  - local symmetry
  - finance as gauge theory
  - gauge theories in physics
    - global symmetry and continuity equation in fields
    - gauge fields from local symmetry
    - dynamics and force

### 14.7 Quantum Field Theory [CANONICAL]

See Part III above for full architecture.

### 14.8 Later chapters or appendices [PROVISIONAL]

- explicit classical recovery material
- possibly standard model consolidation
- possibly interpretive or summary chapters

---

# Part VI. Repo guidance for future drafting passes

## 15. Priority order for writing and revision [CANONICAL]

The repository should probably treat the drafting tasks in this order:

1. stabilize QFT chapter structure,
2. complete free-field quantization and Fock-space sections,
3. integrate displaced material on spaces and unitarity,
4. build calculation section,
5. add path integral as secondary formulation,
6. extend to Dirac and gauge fields,
7. write QED and classical EM recovery,
8. then revisit earlier chapters only where QFT dependency gaps remain.

### 15.1 Why this order

Because the QFT chapter already has the strongest active draft pressure and the clearest downstream utility for repository structuring.

---

## 16. Material classes for the repo [CANONICAL]

The repo should distinguish four classes of source material:

### 16.1 Canonical prose

Already drafted, likely to survive, basis for revision.

### 16.2 Canonical structure but unwritten prose

Needed sections whose architecture is clear but prose is missing.

### 16.3 Displaced high-value material

Strong sections currently outside ideal location.

### 16.4 Historical / exploratory material

Notes, alternate outlines, abandoned passages, objections, reminders.

The repo must not flatten all of these into one undifferentiated corpus.

---

## 17. Things a future repo agent must preserve [CANONICAL]

- symmetry-first architecture,
- relativity and QM as genuine prerequisites to QFT,
- operator-in-spacetime route as a central conceptual move,
- spring-lattice model as main pedagogical and conceptual model for free scalar field,
- the distinction between ontology and calculational formalism,
- the reluctance to make path integrals the primary ontology,
- the goal of recovering classical electromagnetism from QFT,
- careful handling of particle language,
- explicit concern for local causality.

---

## 18. Things a future repo agent should treat cautiously [CANONICAL]

- any claim that ordinary QM straightforwardly violates relativity,
- any phrasing equating the field with the wavefunction,
- any compression that erases the difference between state space and spacetime,
- any rewrite that removes the momentum/translation/generator continuity from earlier chapters,
- any treatment of QFT that reduces it to perturbation theory only,
- any premature standard-model sprawl.

---

# Part VII. Section status ledger

## 19. What already exists in substantial prose [CANONICAL inventory]

### Pre-QFT

- introduction and framing,
- symmetry chapter,
- relativity chapter,
- quantum mechanics chapter,
- change/curvature/gauge chapter.

### QFT

- chapter framing,
- limits of early QM,
- operators in spacetime,
- classical spring-lattice field model,
- KG vs Schrödinger comparison,
- momentum-basis / normal-mode decomposition.

### Displaced QFT

- spaces of QFT,
- unitarity.

---

## 20. What exists mainly as outline or notes [CANONICAL inventory]

- full free-field quantization and Fock-space treatment,
- full calculation section with correlators/propagators/amplitudes,
- path integral as a real chapter subsection,
- Dirac field development,
- gauge-field development inside QFT,
- QED and classical EM recovery.

---

## 21. What is structurally settled vs unsettled

### 21.1 Settled enough to treat as canonical

- whole-book arc ending in QFT,
- QFT as culmination of symmetry + relativity + QM + gauge ideas,
- importance of operator-in-spacetime route,
- importance of spring-lattice model,
- importance of momentum-basis route,
- importance of eventual classical EM recovery.

### 21.2 Still unsettled enough to keep visible

- final placement of spaces/unity sections,
- exact level of scattering formalism,
- exact path integral depth,
- exact balance between ontology and calculation,
- extent of standard model / gauge extension inside chapter.

---

# Part VIII. First-pass closing judgment

## 22. First-pass structural conclusion

The manuscript already has a strong governing architecture. The most important fact for repository purposes is that the QFT chapter is not an isolated blob of advanced material. It is the natural endpoint of everything the manuscript has built earlier.

The active QFT draft is strongest where it:

- diagnoses the insufficiency of early QM,
- puts observables into spacetime,
- constructs a classical relativistic field model,
- explains why hyperbolic field equations matter,
- diagonalizes into normal modes.

The active draft is weakest where it still has to complete:

- free-field quantization,
- particle/Fock interpretation,
- spaces synthesis,
- calculations and amplitudes,
- path integral integration,
- fermions and gauge fields,
- QED and classical recovery.

The repository should therefore treat this outline as the canonical structural backbone and use later files to supply prose and historical memory.

---

## 23. Next-step cross-link map to likely QFT prose draft

If the next file is `02_qft_section_full.md`, its likely major sections should map back here roughly as follows:

- `02` §1  <- QFT introduction (this file §10.1)
- `02` §2  <- limits of early QM (this file §10.2)
- `02` §§3–4 <- two routes / operators in spacetime (this file §§10.3–10.4)
- `02` §§5–7 <- classical model, KG comparison, momentum basis (this file §§10.5–10.7)
- `02` §8 <- quantization and Fock space (this file §10.8)
- `02` §9 <- spaces of QFT (this file §10.9)
- `02` §§10–12 <- calculations, path integrals, unitarity (this file §§10.10–10.12)
- `02` §§13–15 <- fermions, gauge fields, QED recovery (this file §§10.13–10.14)
- `02` §16 <- closing synthesis (this file §10.15)

