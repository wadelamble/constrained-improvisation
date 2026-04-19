# Correlators, Propagators, and Scattering — worked note

*Repository support note.* This file is not polished manuscript prose. It is a slower, more explicit technical note meant to preserve intermediate explanatory rungs that the current QFT chapter draft handles more compactly. Its topic is the calculational hierarchy

local field operators  
→ time-ordered correlators  
→ propagators as two-point functions and Green’s functions  
→ higher-point functions  
→ asymptotic in/out states  
→ scattering operator and amplitudes  
→ LSZ at a conceptual level  
→ beam-lab interpretation

This note is meant to help later revision avoid the feeling that the chapter “jumps” from local fields to scattering language too quickly.

---

## 1. What problem this note is solving

Once the field has been quantized and Fock space has been introduced, a natural reader question is:

> Fine, but what do we actually calculate with this machinery?

If that question is not answered carefully, QFT can start to feel like it has two disconnected halves:
- an ontological half about fields and particles,
- and a calculational half about scattering amplitudes and diagrams.

The goal of this note is to make clear that these are not disconnected. Scattering amplitudes grow out of local field correlators. The field language is not abandoned when one starts talking about experiments. The particle-scattering language is extracted from the local field theory in a controlled way.

---

## 2. Start from local field operators

In the operator formulation, the basic local object is a field operator such as

$$
\hat\phi(x),
$$

where \(x\) is a spacetime point. For more complicated theories one might have:
- a scalar field \(\hat\phi(x)\),
- a spinor field \(\hat\psi(x)\),
- a gauge field \(\hat A_\mu(x)\),
- and so on.

The first thing to notice is that these are **local operators**. They are attached to spacetime points or, more carefully, to small regions when one works rigorously with smearing.

This means the most primitive things the theory naturally gives us are not already scattering probabilities. What the theory naturally gives us are expressions involving local field insertions.

That is why the calculational story must begin with correlators rather than with a fully formed beam-lab picture.

---

## 3. Correlation functions

## 3.1 What a correlator is

A correlation function is an expectation value of a product of field operators in some state, most often the vacuum. The simplest example is

$$
\langle 0|\hat\phi(x)\hat\phi(y)|0\rangle.
$$

This asks, roughly, how the field at point \(x\) and the field at point \(y\) are related in the vacuum state.

But for relativistic QFT, the most important version is the **time-ordered** correlation function:

$$
\langle 0|T\{\hat\phi(x)\hat\phi(y)\}|0\rangle.
$$

The time-ordering symbol \(T\) means:
- whichever operator corresponds to the later time is placed to the left,
- whichever corresponds to the earlier time is placed to the right.

So if \(x^0 > y^0\), then

$$
T\{\hat\phi(x)\hat\phi(y)\} = \hat\phi(x)\hat\phi(y),
$$

while if \(y^0 > x^0\), then

$$
T\{\hat\phi(x)\hat\phi(y)\} = \hat\phi(y)\hat\phi(x).
$$

This is not merely a convention pasted on top of the theory. It is the object that naturally appears when one expands the time-evolution operator in perturbation theory. So if later we want amplitudes for local interactions distributed through spacetime, time-ordered products are exactly what the formalism gives us.

## 3.2 Why correlators come first

This is a point worth emphasizing because it is easy to miss.

QFT does **not** start by calculating:
- particle trajectories,
- detector clicks directly,
- or classical histories.

It starts by calculating vacuum or state expectation values of products of local field operators.

That is what the theory naturally knows how to do, because its basic objects are local fields.

The rest of the hierarchy — propagators, amplitudes, cross sections — grows from that.

---

## 4. The two-point function and the propagator

## 4.1 The Feynman propagator

For a free scalar field, the central two-point function is the Feynman propagator:

$$
\Delta_F(x-y)
=
\langle 0|T\{\hat\phi(x)\hat\phi(y)\}|0\rangle.
$$

It is worth taking seriously that this object has *two* identities at once:

1. it is a time-ordered vacuum correlator of field operators,
2. it is a Green’s function for the free field equation.

That dual role is one of the most conceptually important compression points in QFT.

## 4.2 Why it is called a propagator

People often say the propagator is “the amplitude for a particle to go from \(y\) to \(x\).” That phrase is serviceable as shorthand, but it should be handled carefully.

The deeper statement is:
- the propagator is fundamentally a two-point function of the **field**,
- it becomes associated with particle propagation because particles are excitations of that field,
- and because the propagator’s singularity structure knows about the field’s one-particle states.

So the propagator is not primitive particle language. It is field language that contains the particle interpretation.

## 4.3 Propagator as Green’s function

For the free scalar field, the equation of motion is

$$
(\Box + m^2)\phi(x)=0.
$$

The corresponding Green’s function satisfies

$$
(\Box + m^2)\Delta_F(x-y)
=
-\,i\,\delta^{(4)}(x-y)
$$

up to convention-dependent factors.

This is the same Green’s-function logic familiar from classical differential equations:
- the differential operator acts on a kernel,
- the result is a delta function,
- so the kernel is the inverse of the operator in the appropriate sense.

This means the propagator is not only a quantum expectation value. It is also the inverse kernel of the free field operator.

That is why it sits so naturally between the classical and quantum descriptions.

## 4.4 Propagator in momentum space

The momentum-space propagator is

$$
\Delta_F(p) = \frac{i}{p^2 - m^2 + i\epsilon}.
$$

This formula should be unpacked, not merely memorized.

- The denominator vanishes at \(p^2 = m^2\), which is the mass-shell condition for a free relativistic particle.
- The \(i\epsilon\) prescription tells us how to navigate the poles and produce the correct time-ordered object.
- The whole expression is the momentum-space inverse of the Klein–Gordon operator.

So one should read the propagator as carrying three kinds of information at once:
- differential-equation information,
- vacuum correlation information,
- particle-spectrum information.

---

## 5. Higher-point functions

## 5.1 Why the two-point function is not enough

In a truly free theory, the two-point function already captures a lot of the dynamics. But interactions require more.

If the theory has local interaction terms, then products of more than two fields naturally appear. That means one must consider higher-point time-ordered correlators such as

$$
\langle 0|T\{\hat\phi(x_1)\hat\phi(x_2)\hat\phi(x_3)\hat\phi(x_4)\}|0\rangle.
$$

These are not optional elaborations. They are the natural field-theoretic objects needed to describe interacting processes.

## 5.2 Why interactions generate higher-point functions

Suppose the interaction density contains something like \(\phi^4\). Then when one expands the time-evolution operator or generating functional perturbatively, products of fields at multiple points appear. Evaluating those expressions leads naturally to higher-point correlators.

So the hierarchy is:
- free field → two-point structure becomes central,
- interacting field → higher-point functions become essential.

## 5.3 What higher-point functions are for

Very roughly:
- a two-point function tracks single-field insertion structure,
- a four-point function is the first place one naturally sees two-to-two scattering,
- higher-point functions organize more complicated processes.

The exact process-to-correlator mapping depends on the theory and the external states, but the principle is stable:
the interacting theory’s physical content is encoded in its higher-point correlation functions.

---

## 6. Why experiments still talk about particles

At this stage, a reader might reasonably object:

> Experiments do not usually report “we measured a four-point correlator.”  
> They report incoming particles, outgoing particles, cross sections, decay rates, and detector events.

That is true. But it does not mean the correlator language was a detour. It means the laboratory language is an asymptotic repackaging of the local field theory.

This is one of the deepest conceptual transitions in QFT.

---

## 7. Asymptotic in/out states

## 7.1 Why asymptotic states appear

Before a scattering event, if particles are very far apart and not yet strongly overlapping, the system is well approximated by a free multi-particle state. After the interaction, once the outgoing products are again very far apart, the system is again approximated by a free multi-particle state.

Those are the **in** and **out** states.

They are asymptotic because they live in the far past and far future, where the interaction effectively switches off and the free-particle language becomes a good approximation.

## 7.2 Why free-particle language is legitimate there

This works because the free theory has already been quantized:
- its modes are known,
- its ladder operators are known,
- its Fock space is known.

So asymptotic particles are not being smuggled in from outside the field theory. They are the free excitations the field theory itself already supplies.

## 7.3 The middle is still field theory

This point is crucial.

The process is not:
- “particles are fundamental, and QFT is just a fancy way of describing their collision.”

The process is:
- free-particle language is valid in the asymptotic regions,
- but the interaction region in the middle is most faithfully described by local interacting fields.

That is why the beam-lab language and the field language are not rivals. They govern different parts of the same physical process.

---

## 8. The scattering operator

Let \(|i\rangle\) be an asymptotic incoming state and \(|f\rangle\) an asymptotic outgoing state. Then the central object is

$$
\langle f|S|i\rangle,
$$

where \(S\) is the scattering operator.

This is the amplitude that the in-state evolves into the out-state.

## 8.1 Free and interacting Hamiltonian split

One usually writes

$$
\hat H = \hat H_0 + \hat H_{\mathrm{int}}.
$$

Here:
- \(\hat H_0\) is the free Hamiltonian, whose Fock space and particles are under control,
- \(\hat H_{\mathrm{int}}\) introduces couplings among fields and mixes the free sectors.

This split is important because it tells us what is being used as the asymptotic particle basis and what is being treated as the interaction.

## 8.2 Interaction-picture formula

In the interaction picture, the formal scattering operator is

$$
S
=
T\exp\left[
-\frac{i}{\hbar}
\int d^4x\,
\mathcal H_{\mathrm{int}}(x)
\right].
$$

This deserves a slow reading.

- The interaction is local in spacetime.
- The interaction density is integrated over all spacetime.
- Time ordering is built in.
- Expanding the exponential gives a perturbation series.

So this one formula already expresses a major QFT idea:
local interactions are not attached to a single classical collision point chosen by hand; they are summed over all possible spacetime positions consistent with the theory.

---

## 9. How correlators and \(S\)-matrix language fit together

This is the heart of the hierarchy.

The field theory naturally gives local correlation functions.  
The laboratory naturally speaks in terms of in/out particles.  
The scattering operator connects the asymptotic particle states.  
The bridge between them comes from the analytic structure of the correlators.

This means the \(S\)-matrix is not a separate theory laid on top of QFT. It is a derived asymptotic packaging of the same local field theory.

---

## 10. LSZ at the conceptual level

LSZ is one of the places where many expositions become too abrupt. The full formula is important in serious field theory, but for repository purposes the main thing to preserve is the *logic*.

## 10.1 What LSZ is trying to do

A time-ordered correlator contains:
- the genuinely interacting core of the process,
- plus the free propagation of the external particles into and out of the interaction region.

If you want the actual scattering amplitude for real asymptotic particles, you need to peel those two things apart.

That is what LSZ does.

## 10.2 Pole structure

A one-particle state shows up in momentum space as a pole in the correlator at the mass shell. That is why the propagator was so important earlier. The correlators know about the asymptotic particle content because they develop the right singular behavior when external momenta approach the mass shell.

## 10.3 “Amputation”

In Feynman-diagram language, one says that the external propagators are “amputated.”

That ugly phrase means:
- remove the free propagation factors attached to the external legs,
- because those are not the dynamical heart of the interaction itself,
- then put the external states on shell to represent real incoming and outgoing particles.

So the conceptual ladder is:

1. calculate the time-ordered correlator,
2. identify the poles corresponding to asymptotic particle states,
3. strip away the external propagator factors,
4. impose on-shell external momenta,
5. what remains is the scattering amplitude.

That is LSZ in conceptual form.

## 10.4 Why this matters philosophically

LSZ is one of the clearest formal places where the chapter’s ontological story is vindicated:
- fields are primary,
- particles are asymptotic excitations,
- scattering amplitudes are extracted from field correlators,
- the particle language is therefore contained inside the field theory, not externally imposed.

---

## 11. Beam-lab interpretation

This is the point where the formal hierarchy becomes experimentally intuitive.

A typical beam experiment looks like this:

- prepare an incoming beam with known momentum profile,
- let it collide with another beam or target,
- observe outgoing particles in detectors,
- infer cross sections, decay rates, or event distributions.

The field-theoretic description says:

- the incoming beam is an asymptotic in-state in Fock space,
- the interaction region is a local field interaction,
- the outgoing detected particles form an asymptotic out-state,
- and the probabilities come from \(S\)-matrix elements extracted from correlators.

So the experimenter’s particle language is not wrong. It is just not the deepest language. It is the asymptotic language appropriate to preparation and detection.

## 11.1 Why this matters for the chapter’s central claims

This beam-lab interpretation is one of the places where the chapter’s whole project comes together:

- particles remain real enough to be prepared and detected,
- fields remain fundamental enough to describe the interaction region,
- scattering amplitudes are not ad hoc quantities but are derived from the field correlators,
- and the theory is therefore both ontologically deep and experimentally legible.

---

## 12. Propagators, diagrams, and a common misconception

A common beginner mistake is to think that once diagrams appear, the theory has really become “about particles moving and exchanging other particles.”

That is too naive.

A diagram is a visual encoding of terms in a perturbative expansion.  
An internal line is a propagator.  
A propagator is a two-point function / Green’s function.  
That two-point function belongs to the **field**.

So the diagram language is useful precisely because the field-theoretic correlators admit a compact visual grammar. It is not evidence that the field ontology can now be thrown away.

This is one of the reasons the chapter was right to delay diagrams until after:
- local fields,
- free-field quantization,
- correlators,
- and asymptotic states

were already conceptually on the table.

---

## 13. Compact summary of the hierarchy

Here is the hierarchy in the shortest usable form.

### Level 1 — local ontology
The theory’s basic objects are local field operators \(\hat\phi(x)\), \(\hat\psi(x)\), \(\hat A_\mu(x)\), etc.

### Level 2 — primitive calculational objects
One computes time-ordered correlation functions of those fields.

### Level 3 — two-point kernel
The two-point function is the propagator, which is both a field correlator and a Green’s function.

### Level 4 — interacting content
Higher-point functions encode interacting processes.

### Level 5 — asymptotic particle packaging
Far in the past and future, the states are free in/out particle states in Fock space.

### Level 6 — scattering amplitudes
The \(S\)-matrix gives transition amplitudes between those asymptotic states.

### Level 7 — LSZ bridge
Scattering amplitudes are extracted from correlators by isolating the one-particle poles and removing the external propagation factors.

### Level 8 — experiment
From amplitudes one gets probabilities, cross sections, decay rates, and event statistics.

---

## 14. Common confusions this note is meant to prevent

### Confusion 1: “Correlators are just formal machinery and real physics begins only with scattering amplitudes”
No. Correlators are the local field-theoretic objects out of which scattering amplitudes are extracted.

### Confusion 2: “Propagator means a particle literally travels from one point to another”
Too crude. The propagator is fundamentally a field two-point function / Green’s function.

### Confusion 3: “In/out particle states mean fields are no longer important”
No. In/out particles are asymptotic excitations of the fields.

### Confusion 4: “LSZ is a separate extra theorem with no conceptual connection to the chapter’s ontology”
No. LSZ is one of the formal places where the field ontology yields the particle-scattering language.

### Confusion 5: “Beam experiments are particle-first, so the theory must really be particle-first”
No. The beam-lab description is asymptotic packaging of a local field interaction.

---

## 15. Likely future uses of this note

A later reviser could mine this note for:
- a slower version of the correlator section,
- a stronger explanation of propagators as both Green’s functions and correlators,
- a more patient bridge from correlators to in/out particle states,
- a clearer LSZ explanation,
- a stronger beam-lab interpretation passage,
- and a cleaner defense of why diagram language should not displace field ontology.

---

## 16. Final compact statement

QFT does not begin by calculating particle motions.  
It begins by calculating local field correlators.  
The two-point correlator becomes the propagator, which is also the Green’s function of the field equation.  
Higher-point correlators encode interactions.  
Asymptotic free-particle states in Fock space package the far-past and far-future behavior.  
The \(S\)-matrix gives amplitudes between those states.  
LSZ extracts those amplitudes from the correlators.  
The beam laboratory then reads those amplitudes as measurable event probabilities.

That is the hierarchy this note is meant to preserve.
