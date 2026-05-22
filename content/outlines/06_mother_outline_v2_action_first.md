# 06_mother_outline_v2_action_first.md

*Repository note.* This file is a v2 structural proposal based on the May 2026 LM/action/curvature conversation. It does not overwrite `01_mother_outline.md` or `05_mother_outline_updated.md`. Its purpose is to preserve a revised dependency order: spacetime supplies the basic invariant, action turns invariant histories into dynamics and energy-momentum, Hamiltonian mechanics reorganizes those action-born quantities, and QFT inherits a cleaner account of force as sourced geometry rather than as inserted potential.

This file should be read alongside:

- `01_mother_outline.md` - first-pass mother outline.
- `05_mother_outline_updated.md` - updated outline after the QFT draft existed.
- `content/drafts/lm-draft.md` - current Path Mechanics / LM draft.
- `content/drafts/hamiltonian-mechanics-section-draft.md` - Hamiltonian mechanics draft.
- `notes/worked/geometry-as-coupled-flow.md` - exploratory note on matter, geometry, and sources.

---

## Status labels used in this file

- **[CANONICAL]** - current best structural judgment.
- **[PROVISIONAL]** - likely right, but still open in emphasis, placement, or boundary.
- **[SPLIT]** - concept belongs in more than one place, with different levels of completion.
- **[MOVE]** - material should move from an older location to the new location.
- **[GUARDRAIL]** - important constraint against a tempting but unsafe framing.

---

# Part I. Main v2 Change

## 1. Core structural revision [CANONICAL]

The current outlines put relativity before action and let relativity carry too much early energy-momentum structure. They also let Hamiltonian mechanics become the place where momentum is first deeply explained.

The v2 revision is:

1. Spacetime supplies the basic invariant: proper time / interval.
2. Action assigns invariant scalars to whole candidate histories.
3. Endpoint variation of action produces energy-momentum.
4. Noether reasoning explains why those quantities are conserved under spacetime symmetries.
5. Relativistic kinematics, including mass shell and \(E=mc^2\), is then derived from action plus spacetime symmetry, rather than introduced as a primitive relativity topic.
6. Curvature and force enter after this as the question: what geometry defines the geodesics, and what sources that geometry?
7. Hamiltonian mechanics becomes a later local reformulation of action-born quantities, not the first definition of momentum.

The basic spacetime invariant remains prior to action. Proper time does not need energy or momentum. But the physical quantities that scale, respond to, or emerge from action belong with the action story.

## 2. Why this revision matters [CANONICAL]

This order fixes a dependency problem. The manuscript wants to say that action is the invariant scalar assigned to histories. If that is the case, then energy and momentum should first appear as boundary responses and conserved quantities of that action, not as pre-loaded names in relativity or Hamiltonian mechanics.

The revised order makes the conceptual chain cleaner:

- spacetime gives invariant history-measures,
- action makes those measures physical,
- endpoint variation yields conjugate quantities,
- symmetry makes them conserved,
- Hamiltonian mechanics reorganizes them into phase-space evolution,
- quantum mechanics later lifts the generator structure into operators.

---

# Part II. Whole-Book Spine v2

## 3. Introduction and framing [CANONICAL]

Function: establish the manuscript's method, audience, and nonstandard order.

Core message:

- The book is organized by conceptual dependency, not by standard course sequence.
- It aims to make advanced theory intelligible by showing why each structure is needed.
- It will sometimes delay familiar names until the structure that earns them is in place.

## 4. Symmetry [CANONICAL with revision]

Function: introduce transformations, invariants, generators, representations, and the idea that physical law must survive changes of description.

Core subsections:

1. Discrete symmetries and invariants.
2. Continuous symmetries and infinitesimal generators.
3. Commutators as the algebra of infinitesimal transformations.
4. Representations as ways symmetry acts on objects.
5. Spacetime symmetry as the bridge to physical geometry.

Revision from earlier outlines:

Momentum as "generator of translations" may be introduced conceptually here, but not as the full physical definition of momentum. The full definition should wait until action endpoint variation. Symmetry can say what kind of thing momentum will be; action says how the system produces it.

Guardrail:

Do not let this chapter derive or settle relativistic energy-momentum. It should prepare the generator language and representation logic, not cash out all physical quantities.

## 5. Spacetime [CANONICAL]

Function: establish the invariant arena before dynamics.

Core subsections:

1. Relativity from symmetry and invariant speed.
2. Minkowski interval.
3. Light cones and causal order.
4. Proper time as worldline length.
5. Lorentz transformations as changes of spacetime description.
6. Worldlines and histories.

What belongs here:

- The basic invariant \(d\tau\) or spacetime interval.
- The fact that different observers slice the same spacetime differently.
- The idea that a physical scalar assigned to a history must be invariant.

What should move out:

- Full derivations of 4-momentum.
- Mass shell as a primary structure.
- \(E=mc^2\) as a standalone relativity payoff.

Those belong after action, where energy-momentum can emerge as boundary response and conserved generator.

## 6. Action / Path Mechanics [CANONICAL]

Function: introduce action as the invariant scalar assigned to histories and make constrained optimization the structural heart of dynamics.

### 6.1 Constrained optimization and the circle

Start from a clean variational example:

- Among closed curves with fixed perimeter, the circle encloses maximal area.
- The important structure is not "nature tries"; it is candidate space plus scalar functional plus extremal solution.

This gives the reader the action-principle shape before physics.

### 6.2 Histories as candidates

Move from curves to physical histories:

- A particle history is a worldline.
- A field history is a field assignment over spacetime.
- The action assigns a scalar to each candidate history.
- A physical action must be invariant, because physics cannot depend on observer description.

### 6.3 Free relativistic action

Spacetime supplies proper time as the basic invariant along a worldline.

For a free massive particle, the action is built from worldline length:

\(S=-m\int d\tau\)

This should be explained as:

- proper time is the available spacetime invariant,
- mass is the physical scale coupling the particle to that invariant,
- the free particle follows the geodesic / straightest available history.

Guardrail:

Do not claim bare spacetime geometry alone derives mass. In this section, mass is the physical scale in the action. Later, representation theory and quantum theory can deepen the meaning of mass.

### 6.4 Endpoint variation and energy-momentum [MOVE]

This is the new home for the first serious definition of energy and momentum.

Core idea:

- Momentum is the coefficient of endpoint spatial displacement in the on-shell variation of action.
- Energy is the coefficient of endpoint time displacement, up to sign convention.
- In relativistic form, four-momentum is the covector paired with spacetime endpoint displacement.

Conceptual split:

- Endpoint variation defines the quantity.
- Translation symmetry makes it conserved.

This directly resolves the apparent separation between "momentum as Noether charge" and "momentum as endpoint variation." They are the same structure from two sides.

### 6.5 Relativistic kinematics from action [MOVE]

After endpoint variation, derive or explain:

- four-momentum,
- energy-momentum relation,
- mass shell,
- rest energy,
- \(E=mc^2\),
- low-speed limits.

This material used to live too early in relativity or too late in Hamiltonian mechanics. In v2 it belongs here because it depends on action-born momentum, while still using spacetime symmetry.

### 6.6 Dynamics and curvature

Once free motion is geodesic, force becomes the next question:

- Given a geometry, matter follows geodesics or connection-defined straightness.
- What looks like force can be understood as motion through nontrivial geometry.
- In GR, the geometry is metric spacetime geometry.
- In gauge theory, the geometry is connection/fiber geometry, and a Kaluza-Klein picture can illustrate charged-particle motion as geodesic upstairs in a suitable bundle metric.

Guardrail:

Do not claim the full action is a single drawable shape. For fixed geometry, the geodesic picture is strong. For dynamical geometry, the full object is a coupled matter-geometry history.

### 6.7 The source question

After "force is geometry," ask:

What causes the curvature?

The answer is physical stuff:

- mass-energy / stress-energy sources metric curvature,
- charge/current sources gauge curvature.

This should be framed as the physical bridge, not as a proof from pure action logic. We observe forces, interpret force geometrically, and observe forces being produced by matter/charge; therefore a theory of the force must include source equations for the relevant geometry.

## 7. Gravitation [CANONICAL]

Function: develop the metric version of the source-geometry story.

Core subsections:

1. Metric as the geometry of free fall.
2. Free matter follows metric geodesics when only gravity acts.
3. Matter does not merely move on the metric in full GR; stress-energy sources the metric.
4. Einstein's field equation as the compact source-geometry relation.
5. Gravitational waves as waves in the geodesic-defining structure.
6. Bianchi identities as built-in geometric consistency, not as an extra law.

Preferred thesis:

Matter creates the kind of geometry in which it moves.

Guardrails:

- Do not overuse the rubber-sheet picture.
- Do not say the metric term is simply "least curvature."
- Do not claim Einstein's equation is derived from geodesics alone.
- Do distinguish fixed-background geodesic motion from full dynamical geometry.

## 8. Hamiltonian Mechanics [CANONICAL after action]

Function: reformulate action mechanics as local evolution on the space of instantaneous states.

This chapter should no longer be the first deep explanation of momentum. Momentum has already appeared as an action boundary response and conserved quantity.

Core subsections:

1. Why another mechanics?
2. From histories to instantaneous states.
3. Phase space as position-momentum space.
4. Boundary one-form and the origin of conjugate variables, now as a review/reactivation rather than first definition.
5. Symplectic two-form as the intrinsic phase-space structure.
6. Liouville / ensemble preservation.
7. Hamiltonian flows.
8. Poisson algebra.
9. Bridge to quantum commutators.

Revision from existing HM draft:

The current Hamiltonian material that defines momentum through boundary variation should be trimmed or reframed. It should say: action already showed why momentum pairs with endpoint displacement; Hamiltonian mechanics now builds the instantaneous state space around that pairing.

Preferred top-level HM outline:

- Evolution of ensembles.
- Phase-space geometry.
- Hamiltonian flows.
- Poisson algebra.

## 9. Quantum Mechanics [CANONICAL]

Function: introduce quantum state space, amplitudes, observables, operators, and probability structure.

In v2, QM inherits:

- symmetry and generator language,
- action-born energy-momentum,
- Hamiltonian evolution as generator flow,
- Poisson brackets as classical predecessor to commutators.

Core subsections:

1. Experimental pressures.
2. State space and amplitudes.
3. Observables and operators.
4. Born rule.
5. Unitary evolution.
6. Commutators and uncertainty.
7. Entanglement and Bell.

Guardrail:

Do not let QM carry the first explanation of momentum or energy. It should inherit those ideas and transform their representation.

## 10. Gauge Theory [SPLIT but structurally necessary before QFT]

Gauge theory has two roles in v2.

Early role in the action/curvature cluster:

- show force as connection geometry,
- explain curvature as phase/parallel-transport mismatch around loops,
- introduce the idea that charge/current sources gauge curvature.

Later role after QM:

- local phase symmetry becomes physically meaningful once quantum state phase is in view,
- ordinary derivatives fail under local phase changes,
- the connection \(A\) restores local comparison,
- the curvature \(F=dA\) is the physical field strength,
- the simplest gauge-field action is built from \(F^2\),
- matter-gauge coupling prepares QED.

Core subsections:

1. Global versus local phase.
2. Gauge transformation as local convention change.
3. Connection as comparison rule.
4. Curvature as loop failure.
5. Faraday tensor as gauge-invariant connection curvature.
6. Field term \(F^2\).
7. Matter plus interaction plus gauge terms.
8. Source equation: charge/current sources gauge curvature.
9. Handoff to QFT/QED.

Guardrail:

Do not say gauge curvature is spacetime curvature. It is curvature of the internal comparison rule over spacetime. But it maps to an ordinary field over spacetime: in electromagnetism, the components of \(F\) are the electric and magnetic fields.

## 11. Quantum Field Theory [CANONICAL]

Function: complete the synthesis of quantum theory, relativity, local fields, and mediated interactions.

The QFT chapter should inherit from v2:

- spacetime locality and light-cone structure,
- action as invariant history scalar,
- energy-momentum as action-born conserved quantities,
- Hamiltonian mechanics as local state evolution and generator algebra,
- gauge theory as local symmetry plus connection curvature,
- the problem of potentials being inserted rather than physically sourced.

The current detailed QFT architecture from `05_mother_outline_updated.md` remains mostly intact:

1. Why early QM is not enough.
2. The spaces of QFT.
3. Classical field to be quantized.
4. Why Klein-Gordon belongs and Schrodinger does not.
5. Momentum basis and normal modes.
6. Quantizing modes.
7. Fock space.
8. Correlators, propagators, and scattering.
9. Path integral as secondary formulation.
10. Fermions.
11. Gauge fields.
12. QED and recovery of classical electromagnetism.

The main dependency change is that QFT should no longer need to teach energy-momentum, action, or gauge motivation from scratch.

---

# Part III. Revised Dependency Map

## 12. What each section earns

### 12.1 Symmetry earns

- transformations,
- invariants,
- generators,
- commutators,
- representations,
- law surviving description change.

### 12.2 Spacetime earns

- interval,
- proper time,
- light cone,
- worldline,
- Lorentz transformations,
- the demand that physical history-scalars be invariant.

### 12.3 Action earns

- candidate histories,
- scalar functional,
- constrained optimization,
- free geodesic motion,
- endpoint variation,
- energy-momentum,
- Noether conservation,
- relativistic kinematics.

### 12.4 Curvature / force earns

- force as geometry,
- given geometry -> matter follows geodesics/straightness,
- observed sources -> geometry must be sourced,
- full theory -> matter and geometry solved together.

### 12.5 Hamiltonian mechanics earns

- instantaneous state space,
- phase-space measure,
- local evolution flow,
- Hamiltonian as time-evolution generator,
- Poisson bracket algebra,
- bridge to quantum commutators.

### 12.6 Quantum mechanics earns

- Hilbert space,
- amplitudes,
- operators,
- Born rule,
- unitary evolution,
- intrinsic probabilistic state structure.

### 12.7 Gauge theory earns

- local phase comparison,
- connection,
- gauge curvature,
- gauge-invariant field strength,
- matter-current sourcing,
- conceptual bridge to QED.

### 12.8 QFT earns

- local quantum fields,
- variable particle number,
- particles as excitations,
- interactions as field couplings,
- QED as the explanation of what earlier theories inserted as potentials.

---

# Part IV. Specific Relocation Instructions

## 13. Relativity material to move into Action

Move or reframe:

- 4-momentum,
- mass shell,
- \(E=mc^2\),
- energy-momentum relation,
- momentum as boundary response,
- relativistic momentum derivation.

Keep in Spacetime:

- interval,
- Lorentz transformations,
- proper time,
- light-cone causality,
- geometry of observer disagreement.

## 14. Hamiltonian material to reframe

The Hamiltonian section may still discuss boundary terms, but it should not present them as if the reader is first discovering momentum.

New framing:

Action already exposed the boundary pairing. Hamiltonian mechanics asks what local state space and flow structure are implied by that pairing.

This turns the Legendre transform from a magic algebraic maneuver into a consequence of a prior action structure.

## 15. Gauge material to split carefully

Gauge theory is conceptually connected to curvature and force before QFT, but full QED belongs later.

The pre-QFT gauge section may discuss:

- local phase,
- connection,
- curvature \(F\),
- source-current relation,
- classical field action,
- why potentials are no longer primitive.

The QFT chapter then quantizes the matter and gauge fields and explains photons, interactions, and recovered electromagnetism.

## 16. Action claims to protect

Use:

- action is an invariant scalar assigned to histories,
- free matter follows geodesics in given geometry,
- force can be read as geometry/curvature,
- matter creates the kind of geometry in which it moves,
- the full theory solves matter and geometry together.

Avoid:

- action is literally a simple shape,
- all full dynamics is just a shortest path in one fixed space,
- the field term and matter term minimize independently,
- gauge curvature is spacetime curvature,
- GR metric action is simply "least curvature."

---

# Part V. Revised Whole-Book Table of Contents Candidate

## 17. Top-level manuscript order [PROVISIONAL but preferred]

1. Introduction
2. Symmetry
3. Spacetime
4. Path Mechanics / Action
5. Gravitation
6. Hamiltonian Mechanics
7. Quantum Mechanics
8. Gauge Theory
9. Quantum Field Theory
10. Later continuations / appendices

## 18. Alternative placement note for Gauge Theory [PROVISIONAL]

If the Gauge Theory section feels too dependent on quantum phase, keep it after Quantum Mechanics, as listed above.

If the geometric-force story needs it earlier, include only a short gauge preview in the Action/Curvature cluster and reserve the full section for after QM.

Current v2 preference:

- preview gauge geometry in Path Mechanics / Curvature,
- place full Gauge Theory after QM and before QFT.

This preserves the conceptual force of "GR and gauge are two geometrizations of force" without asking the reader to metabolize local quantum phase before the QM chapter exists.

---

# Part VI. Final v2 Judgment

## 19. Structural conclusion [CANONICAL]

The manuscript should no longer treat relativistic energy-momentum as something fully established inside the spacetime chapter or first deeply explained in Hamiltonian mechanics.

The cleaner structure is:

Spacetime gives proper time.

Action makes invariant histories physical.

Endpoint variation gives energy-momentum.

Symmetry makes those quantities conserved.

Curvature explains force.

Sources explain curvature.

Hamiltonian mechanics reorganizes the action-born quantities into phase-space flow.

Quantum mechanics turns generator structure into operator structure.

Gauge theory physicalizes local comparison.

QFT quantizes the local fields and recovers particles and forces.

This v2 keeps the project's original ambition but gives the pre-QFT half a cleaner dependency spine.
