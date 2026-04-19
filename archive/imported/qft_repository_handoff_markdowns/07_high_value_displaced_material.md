# High-value displaced and alternate source material

*Repository support note.* This file preserves selected high-value material from the source manuscript that is displaced, left out, alternate, or struck through, and that is **not already adequately preserved** in the current markdown set. It is intentionally selective. It does **not** attempt to preserve every leftover or every alternate paragraph. The criterion here is practical value for future revision of the QFT chapter or its most direct dependencies.

Where original DOCX equations did not extract cleanly in plain text, I have marked that with bracketed notes such as `[display equation in source]`.

---

## 1. Alternate “what does QFT actually calculate?” bridge

**Why this is worth preserving:**  
The current QFT draft already has a “what the theory calculates” section, but this struck source block has a particularly clean bridge from fixed-particle quantum mechanics to asymptotic scattering language, and it states the “inserted potential versus interacting fields” contrast in a compact way that may be useful later.

> Once we have our model of operator-valued fields, what do we calculate with it? In one sense, we use it to calculate the behavior of any physical system. It is, after all, the deepest framework we currently have for nongravitational physics. But real-world calculations are often extremely difficult, and in many low-energy settings we use nonrelativistic or fixed-particle approximations when those are sufficient. Still, such calculations are built from more elemental ones. That is what we are after here: what is the most elemental thing QFT calculates?
>
> In fixed-particle quantum mechanics, the basic building-block calculation is
>
> `[display equation in source]`
>
> This says that if I prepare an initial state and let it evolve in time, I can calculate the amplitude for a final state. For example, if I specify a particle moving in a prescribed potential, I can ask for the amplitude that it later be found in some other state. There is already a subtlety here, however. The potential is assumed to be given. Quantum mechanics tells us how states behave in that interaction environment, but not, at that level, where the interaction itself comes from.
>
> QFT goes one level deeper. Its fundamental input is not a prescribed potential, but interacting fields. For this reason, the cleanest first calculation is not the evolution of a particle inside a permanently given background, but the transition from completely free particles before an interaction to completely free particles after it. We therefore define asymptotic “in” states infinitely far in the past and asymptotic “out” states infinitely far in the future. The operator connecting them is the scattering matrix,
>
> `[display equation in source]`
>
> This is the amplitude for one incoming particle configuration to become another outgoing configuration after all allowed interactions have taken place.
>
> This is also the situation engineered in a particle accelerator. We prepare a beam with a narrow momentum distribution, allow it to collide with another beam or a target, and record the outgoing particles in a detector. The incoming beam defines the initial state, the detected particles define the final state, and the theory gives us amplitudes from which observable rates and cross sections can be computed.
>
> At first glance this can seem like a downgrade. In ordinary quantum mechanics, we seemed to have a richer picture: an evolving wavefunction in a tidy setting like a box or well. In QFT, by contrast, the middle of the process can seem to disappear into a black box, leaving us only with asymptotic states and conserved quantities. But that richer description in quantum mechanics came with an important limitation: the interaction structure was put in by hand. QFT gives up the tidy box in exchange for something more fundamental — a description in terms of interacting fields from which effective forces and potentials can emerge.
>
> If this formalism is really to deserve the name “fundamental,” it should recover the ordinary forces we already know. We will therefore use QFT, in the appropriate low-energy limit, to recover the Coulomb interaction: the familiar inverse-square electric force as the static remnant of electromagnetic field interaction.

---

## 2. Alternate momentum-basis and diagonalization explanation

**Why this is worth preserving:**  
The current draft now contains the momentum-basis block, but this struck source version is more patient at one key place: it explains what a mode *is* in plain language and ties diagonalization directly to the future particle interpretation. This may help later if the chapter needs a slower version of that bridge.

> Before we can quantize the field, we need to rewrite the free lattice in the variables in which its energy actually separates into independent pieces. In the site basis, that is not true. Each displacement is tied to its neighbors by the coupling springs, so the Hamiltonian is not a sum of independent local oscillator energies. A disturbance placed at one site immediately talks to the others. The local variables are useful for seeing causality and propagation, but they do not diagonalize the free dynamics.
>
> So the next step is not merely to find a basis that is mathematically tidier. It is to find the variables in which the Hamiltonian becomes a sum of independent quadratic terms. That is what diagonalizing the Hamiltonian means here. We are looking for coordinates in which the free field breaks apart into non-interacting oscillators. This matters because independent oscillator energies are the quantities that will later become independently countable excitations. That is the first real hint of what will eventually deserve to be called a particle.
>
> For a translationally invariant lattice, the required variables are the normal modes, which are just the discrete Fourier modes. Instead of specifying the displacement of each individual site, we describe the lattice as a superposition of collective patterns spread across all sites. On a finite lattice, only a discrete set of wavelengths fits, so the allowed wavevectors are discrete. We therefore write the field as
>
> `[display equation in source]`
>
> and similarly for the conjugate momenta,
>
> `[display equation in source]`
>
> It is worth being very plain about what one such mode is. A mode is not one site vibrating by itself. It is a whole-lattice pattern. In a single mode, every site oscillates in time at the same angular frequency, but with fixed relative phases and amplitudes set by the spatial pattern. The dynamical variable is the amplitude of that entire pattern. That amplitude is what oscillates like a simple harmonic oscillator.
>
> You can see this in the simplest examples. The zero mode is the uniform mode: every site rises and falls together. The next mode is a long-wavelength ripple across the lattice: neighboring sites are slightly out of step, but the pattern as a whole simply breathes in time. Higher-$k$ modes alternate more rapidly from site to site, producing shorter wavelengths and therefore larger restoring forces from the coupling springs. Each allowed spatial pattern has one time-dependent amplitude, and that amplitude behaves as one oscillator. This is exactly what one sees in any normal-mode decomposition of a coupled mechanical system. The only difference here is that the system has many sites, and in the continuum limit infinitely many.
>
> Now comes the key fact. When these Fourier expansions are inserted into the free Hamiltonian, all cross-couplings between different $k$-values disappear. The Hamiltonian becomes
>
> `[display equation in source]`
>
> So the Fourier transform does not merely re-label the same messy system. It identifies the variables in which the free energy is already split into independent pieces. Each $k$-mode evolves on its own, as though it were its own oscillator, with its own natural frequency $\omega_k$.
>
> In the continuum limit, that frequency becomes
>
> `[display equation in source]`
>
> This is the relativistic dispersion relation we have been preparing for. The same mass parameter that appeared earlier as the frequency of the uniform on-site oscillation now appears as the rest term in the mode frequency, while the inter-site coupling contributes the $k^2$ part. The field, viewed locally, is one extended coupled medium. The same field, viewed in momentum modes, is an infinite collection of decoupled oscillators labeled by $k$.
>
> That is the decisive simplification. In position space, the field looks like an enormous coupled machine. In momentum space, its free dynamics have already been resolved into its natural independent motions. This does not yet give us particles. Nothing quantum has happened. But it gives us the classical structures that quantization will act on. Once each mode is quantized, the energy in that mode will no longer vary continuously. It will come in discrete units. Those countable units of excitation, one mode at a time, are what will become the particle interpretation of the field.

---

## 3. Source version of “The Spaces of QFT” — framing paragraphs

**Why this is worth preserving:**  
The current markdown set preserves the *idea* of “spaces of QFT,” and the current QFT draft contains a chapter section by that name, but the source document has a stronger philosophical opening for the whole spaces-framework than the chapter currently carries. It may be useful later, either as a preface to the section or as a source of sentence-level salvage.

> Nature unfolds in spaces. We are biased to favor spacetime because it is the space we directly perceive, but nature is not required to privilege our habits of perception. In physics, how influence transmits locally, how a complete instantaneous state is specified, how symmetries constrain possibility, and, in a quantum theory, how identity is preserved in a probabilistic world are organized in the interplay of multiple spaces. We will begin by reviewing the spaces of classical and early quantum mechanics, then turn to the changes made by QFT. This language of spaces is not a mathematical detour. It is a way of making QFT’s “ontology” precise, the kinds of things the theory says exist, in terms of which phenomena are explained.
>
> Classical mechanics incorporates spacetime, phase space, and symmetry structure. Quantum mechanics needs this classical structure in translated form, but it also needs a new space, state space, because a quantum state is not a point in phase space. Quantum field theory keeps the quantum state space, restores local objects to spacetime in the form of fields, enlarges the state space to allow variable particle number, and requires the resulting arrangement to satisfy both relativistic symmetry and unitary evolution.

---

## 4. Source version of “The Spaces of QFT” — Hamiltonian mechanics subsection

**Why this is worth preserving:**  
The current repository materials summarize the role of phase space, but this source block gives a more explicit bridge from Hamiltonian phase space to the later need for Hilbert space and QFT’s multi-space ecology. It is especially useful because it states the role of symplectic structure, Poisson brackets, and symmetry generators in one conceptual line.

> A classical theory must distinguish a state at an instant from a history through time. A history is the full trajectory. A state is the information on one time slice from which that trajectory can be generated. In Hamiltonian mechanics that state is organized in phase space. For finitely many degrees of freedom one writes
>
> `[display equations in source]`
>
> and for a classical field one writes, on a time slice,
>
> `[display equation in source]`
>
> The variables $q^i$, or in the field case $\phi(\mathbf{x})$, specify the configuration. The variables $p_i$, or $\pi(\mathbf{x})$, specify the conjugate momentum. We stress “on a time slice” because spacetime contains entire histories, while dynamics asks a different question: what present state is enough to determine the future.
>
> One could try to organize the state using position and velocity. For simple systems that often works. But momentum is not just velocity renamed. It is defined from the Lagrangian by
>
> `[display equation in source]`
>
> In the simplest cases momentum is proportional to velocity. In general it is not. The distinction matters in generalized coordinates, in relativistic systems, in gauge theories, and in field theory. More importantly, momentum lets us rewrite the theory in a form that carries much more structure than a bare position-velocity description. The state is no longer just “where things are” and “how fast they are changing.” It is organized into conjugate pairs.
>
> This pairing is the first sign that phase space is not an arbitrary list of variables. Once the rate data are written in this momentum form, position and momentum fit together in a built-in geometric structure.
>
> That built-in structure is the symplectic form,
>
> `[display equation in source]`
>
> Here $\omega$ represents the infinitesimal oriented area in each position-momentum plane. So the symplectic form is the phase-space area structure. It tells us that the basic geometry of phase space is not a geometry of lengths and angles, but of conjugate pairings and conserved oriented areas.
>
> This matters because that area structure turns functions into flows. A function on phase space, such as the Hamiltonian, tells us how its value changes under small moves away from a point. The symplectic structure converts that information into a vector field, that is, into a rule for how the state moves.
>
> The Poisson bracket is the algebraic expression of that rule. For two functions $F$ and $G$ on phase space,
>
> `[display equation in source]`
>
> This bracket tells us how the flow generated by one function acts on another. Classical observables are then ordinary functions on phase space.
>
> When the generating function is the Hamiltonian $H$, the resulting flow is physical time evolution. Hamilton’s equations are
>
> `[display equations in source]`
>
> So the symplectic form, the Poisson bracket, and Hamilton’s equations are three parts of one structure. The symplectic form gives phase space its position-momentum area geometry. The Poisson bracket is the corresponding algebraic rule. Hamilton’s equations are the particular flow generated by the Hamiltonian.
>
> Because the flow is generated in this way, it preserves the symplectic structure itself. In the simplest picture, a region of phase space may be stretched and sheared as the system evolves, but its basic position-momentum area is preserved. Phase space therefore does more than store enough information to start the system evolving. It organizes the classical state in a form that makes time evolution a vector flow, gives a natural bracket algebra on observables, and packages symmetry generators into the same language.
>
> Symmetry groups that constrain dynamics like the Poincaré group reside in their own space, whose geometric structure constrains the theory. In Hamiltonian mechanics each continuous symmetry has a generator, a function on phase space.
>
> `[display equation in source]`
>
> The group geometry is reflected in the Poisson algebra, and the Poisson algebra acts on the phase-space observables.
>
> The minimal classical picture is therefore this. Spacetime carries locality and causal order. Phase space carries complete instantaneous state data and symplectic structure. Symmetry structure supplies invariants and generators.

---

## 5. Source version of “The Spaces of QFT” — quantum mechanics subsection

**Why this is worth preserving:**  
The current dependency summary covers this at a higher level, but this source block contains a stronger internal bridge from phase space to Hilbert space, especially the idea that Hilbert space takes over part of phase space’s structural job in translated form. That may matter if the “spaces” section is later expanded.

> Quantum mechanics keeps the classical need for spacetime, canonical structure, and symmetry, but it adds something genuinely new. The classical state was a point in phase space. The quantum state is not. It is a vector, or more precisely a ray, in a complex Hilbert space.
>
> This new space is required to carry the structure demanded by superposition, interference, and probabilistic prediction. A point in phase space singles out one actual configuration and momentum, but a quantum state assigns amplitudes to many alternatives at once for the same state. We must, therefore, have a space that can preserve the structure of such states as time evolves.
>
> The observables are now self-adjoint, or real-eigenvalued, operators on $\mathcal{H}$. In ordinary one-particle quantum mechanics one may represent the state as a wavefunction
>
> `[display equation in source]`
>
> Now, we could look at this and think that we’ve represented the state in spacetime, but we have not, for this is a representation over space only, and we could just as easily have represented the state in the basis of any other observable. Time evolution acts on the state as a whole in Hilbert space, and nothing in this representation ties that evolution to position in a way that builds in relativistic locality. Without that, there is no Minkowski metric, no light cones, and no causal structure of the sort that defines the spacetime in which our emitters and detectors live. But what if we could somehow arrange the time evolution of the state so that emission and detection events do respect the proper causal structure. That is what we will do in QFT.
>
> While Hilbert space does not carry the needed structure of spacetime, it does take over structural elements of phase space’s job. Hilbert space looks very different from phase space. We know it encodes superposition rather than definite observable values, but it also is represented in the eigenbasis of only one chosen observable at a time. How can a space that is represented in a basis of “either position or momentum” replace a space whose coordinates were “position and momentum”? The reason it can do so is that, unlike particles, the wave object encodes both position and wavelength information. Once we associate wavelength with momentum, the wave-like state encodes position and momentum.
>
> We have seen that Hilbert space contributes to the structure needed for quantum evolution. A complex inner product gives a norm, so states can be normalized and total probability can remain one. It also gives angles, so different states can interfere. If $\langle \cdot,\cdot \rangle$ is the complex inner product, then its real and imaginary parts define
>
> `[display equations in source]`
>
> Here $g$ is symmetric and metric-like. The second quantity, $\omega$, is antisymmetric. We can see this with a simple example. Writing $z=x+iy$:
>
> `[display expression in source]`
>
> That antisymmetric part is exactly what one needs for a symplectic form. Hilbert space preserves the part of classical mechanics concerned with reversible flow and conjugate pairings in translated form.
>
> Quantum mechanics preserves that structure in operator form, replacing the Poisson bracket with the commutator,
>
> `[display equation in source]`
>
> which for canonical position and momentum becomes
>
> `[display equation in source]`
>
> Symmetry works in quantum mechanics much as it did in Hamiltonian mechanics, except that Poisson brackets are replaced by commutators. If the symmetry group is the Poincaré group, one may represent it on Hilbert space, but this still does not put the observables themselves into local spacetime form.

---

## 6. Source version of “The Spaces of QFT” — quantum field theory subsection

**Why this is worth preserving:**  
The current QFT draft has its own “Spaces of QFT” section, but this source material contains sharper wording on why only fields can mediate influence relativistically and why local observables, not just Poincaré representation on state space, are needed. That is directly relevant to one of the project’s deepest recurring motivations.

> Quantum field theory adjusts the roles of spacetime and Hilbert space so that quantum observables carry local spacetime structure, and so that interactions can create and destroy particles.
>
> In quantum mechanics there are two objects that work together to calculate measurements, the state and the operators. If we want to bring spacetime into quantum mechanics, it is natural to ask whether one or the other should be situated in spacetime. Since operators are observables, they are the natural choice. The state, by contrast, is better understood as a global object, whose job is to encode the amplitudes and correlations from which measurement outcomes are computed. If we want the operators to depend on spacetime, we must further specify what sort of local spacetime structure they inhabit: discrete points, as in a particle configuration, or a field, as in electromagnetism and gravity. In fact, only fields can mediate influence relativistically. If influence could act directly across a spacelike gap, then because spacelike separated events have no observer-independent time order, one observer’s cause could be another observer’s effect, opening the door to causal paradox. Influence cannot simply jump the gap. But once it does not jump the gap, whatever later makes a difference elsewhere must be instantiated in the intervening region while it is on its way. The moment one says that information propagates, one has already admitted local degrees of freedom that carry it from place to place. In the continuum, that distributed local state is by definition a field.
>
> We can now state this in notation. The basic local objects are operator-valued fields:
>
> `[display equations in source]`
>
> More carefully, because exact point values are singular, one should work with smeared operators,
>
> `[display expression in source]`
>
> and similarly for the other fields.
>
> Once the basic observables are placed in spacetime, relativistic causality can be stated directly:
>
> `[display commutator condition in source]`
>
> This is how relativistic causality is expressed in commutator algebra. It says that the order of two spacelike separated operations has no physical effect. A representation of the Poincaré group on state space alone was not enough, because this new condition presupposes local observables attached to spacetime regions.
>
> A state in Hilbert space is still an amplitude assignment over possible alternatives, but now those alternatives are entire field configurations written in the eigenbasis of field operators. If $|\phi(\mathbf{x}),t\rangle$ denotes a field-configuration eigenstate at fixed time $t$, then
>
> `[display equation in source]`
>
> and the state may be represented as a wave functional,
>
> `[display equation in source]`
>
> thus shifting the notion of locality to the field itself rather than trying to locate it in the position representation of the state.
>
> We can see how this provides the needed spacetime constraint by looking at an example. Consider two localized interventions, one in region $A$ near “Alice” and one in region $B$ near “Bob,” with $A$ and $B$ spacelike separated. Alice changes something in her lab. Bob asks whether his detector statistics change immediately.
>
> In ordinary one-particle quantum mechanics, Alice’s intervention is represented by modifying the Hamiltonian near $A$, but the state is global and the theory has no condition forbidding that change from having an immediate mathematical effect on amplitudes elsewhere.
>
> In QFT, it does. Alice’s intervention is represented by a local operator and Bob’s by a local operator. If the regions are spacelike separated, the theory requires
>
> `[display commutator condition in source]`
>
> That means their order has no physical effect. Since different observers may disagree on which spacelike-separated event happened first, this is exactly what relativistic causality requires.
>
> Poincaré transformations of spacetime are represented by unitary operators on the Hilbert or Fock space, and local fields transform accordingly. For a scalar field,
>
> `[display transformation law in source]`
>
> This is the bridge connecting state space to spacetime. The relation holds because the field operator and the unitary Poincaré transformations are inherited from the same classical relativistic structure. The classical field placed observables directly in spacetime. Quantization keeps them there, but promotes them to operator-valued objects acting on a quantum state space.
>
> The state space must also be enlarged. Since the field may have no excitations, one excitation, two excitations, and so on, the state space must contain all of those sectors. This is Fock space, the direct sum of particle-number sectors.
>
> The vacuum sector $\mathcal{H}_0$ contains the zero-particle state. The sector $\mathcal{H}_n$ contains the $n$-particle sector.

---

## 7. Source version of “Unitarity”

**Why this is worth preserving:**  
The current draft contains a unitarity section, but this source version is more expansive and more explicitly tied to the geometry of Hilbert space and the translated symplectic structure inherited from classical mechanics. It may be useful later if the chapter needs a fuller unitarity section or if some of this belongs earlier in the QM chapter.

> Before introducing the full machinery of quantum mechanics, it is worth isolating one requirement that already tells us a great deal about what the theory must look like. If the basic object of the theory is not a point in phase space but a superposition of amplitudes, then its evolution cannot be arbitrary. It must preserve the structure that makes those amplitudes physically meaningful. That requirement is unitarity.
>
> Let the state of a system be represented by a vector in a complex vector space equipped with an inner product. This inner product is not an ornamental extra. It is the structure from which the measurable content of the theory is built. Norms come from it. Overlaps come from it. Transition amplitudes come from it. Once probabilities are extracted from squared overlaps, the inner product becomes the quantity whose preservation matters.
>
> An allowed time evolution must therefore preserve that inner product. If the state evolves by a linear map $U$, then the condition is
>
> `[display equation in source]`
>
> for all states. A map with this property is called unitary. In operator form, this is
>
> `[display equation in source]`
>
> That compact equation says a great deal. It says the evolution may rotate the state in its abstract space, it may mix components, it may alter phases, but it may not stretch, shrink, or scramble the geometry that gives the state physical meaning.
>
> This geometry is richer than ordinary Euclidean geometry because the inner product is complex. If we temporarily view the complex vector space as a real one with extra structure, then the inner product splits into two parts,
>
> `[display equation in source]`
>
> where
>
> `[display equation in source]`
>
> The real part plays the role of a metric-like structure. It measures lengths and angles. The imaginary part is antisymmetric and area-like. It is the Hilbert-space remnant of the symplectic structure that classical mechanics preserves in phase space. In classical mechanics, lawful evolution preserves symplectic area. In quantum mechanics, lawful evolution preserves something stronger. It preserves the entire complex inner product, and therefore preserves both the metric-like and symplectic-like parts at once. Symplecticity has not disappeared. It has been absorbed into unitarity.
>
> This is one reason quantum theory needs Hilbert space rather than ordinary configuration space. A wave-like state carries internal structure. Its components do not merely list mutually exclusive possibilities. They coexist with relative magnitudes and relative phases, and those relative phases affect future outcomes through interference. The state is therefore not just a distribution over alternatives. It is a single object whose parts can reinforce or cancel one another. A theory of such objects needs a geometry that can keep track of both size and phase relations. The complex inner product does exactly that.
>
> Consider a state written as a superposition,
>
> `[display equation in source]`
>
> The coefficients are amplitudes, not probabilities. Their squared magnitudes may eventually be read probabilistically in a suitable basis, but the state itself contains more than those magnitudes. It also contains the phase relations among the components. Those phases are not decorative. They are what make interference possible. Under unitary evolution,
>
> `[display equation in source]`
>
> the amplitudes change, but they change in a way that preserves the full pattern of relations among components. A superposition may spread, twist, and recombine, but it does not come apart. The geometry that makes interference meaningful is carried forward intact.
>
> From this one condition follow many of the most familiar features of quantum mechanics.
>
> First, unitarity preserves norm. Since
>
> `[display equation in source]`
>
> a normalized state remains normalized. This is why total probability is conserved in a closed quantum system. But probability conservation is only the most visible consequence, not the deepest one.
>
> Second, unitarity preserves transition amplitudes and therefore transition probabilities. If two states have a given overlap now, they retain that overlap after both are evolved. The mutual relations among states are not distorted.
>
> Third, unitarity preserves angles and orthogonality. If two states are orthogonal, meaning perfectly distinguishable in principle, then unitary evolution keeps them orthogonal. Quantum evolution may make a state harder for us to describe in one chosen basis, but it does not collapse the difference between distinct states.
>
> Fourth, unitarity makes closed-system evolution reversible. Since $U^\dagger U = 1$, the inverse of $U$ exists and is $U^\dagger$. One can run the evolution backward. This does not mean that every practical process in the world is reversible. Measurement, environment, and coarse-graining bring new issues. But at the level of closed-system dynamics, the evolution does not lose information.
>
> These consequences are often taught separately. Probability conservation is presented in one place, reversibility in another, orthogonality in another. But they are all facets of the same geometric fact. A unitary evolution preserves the full inner-product structure of Hilbert space.
>
> This gives quantum mechanics a kind of continuity very different from classical continuity. In classical mechanics, a system remains itself by tracing a path through phase space. In quantum mechanics, a state need not follow any single classical path. Yet something deeper is preserved: the relational structure that makes the state a coherent physical object at all. This is why unitarity is not just probability conservation. It is the condition that allows identity to survive in a world described by superposition.
>
> Unitarity, then, is the principle that pulls identity out of the ashes of uncertainty. A quantum state may be indefinite with respect to many classical questions, but it is not without structure, and that structure is not allowed to decay arbitrarily. Whatever else quantum mechanics turns out to mean, its lawful evolution is rigid in this precise sense.

---

## 8. Small but important note about source value

The material preserved here is not necessarily destined to be reinserted verbatim into the manuscript. Its value is mixed:

- some of it contains stronger philosophical framing than the current draft,
- some of it contains slower explanatory rungs than the current draft,
- some of it preserves source-language that may matter later for dependency sections,
- and some of it contains structural emphasis that helps keep the project aligned with its own deepest motivations.

That is why these passages are being preserved separately rather than silently folded into the chapter draft.
