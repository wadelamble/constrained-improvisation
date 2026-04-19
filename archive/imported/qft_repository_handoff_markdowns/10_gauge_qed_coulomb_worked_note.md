# Gauge Structure, QED, and Coulomb Recovery — worked note

*Repository support note.* This file is not polished manuscript prose. It is a slower, more explicit technical note meant to preserve explanatory rungs that the current QFT chapter draft handles more compactly. Its topic is the chain

global phase symmetry  
→ local phase symmetry  
→ failure of the ordinary derivative  
→ covariant derivative  
→ gauge field as connection  
→ interaction term in QED  
→ photon-mediated interaction  
→ low-momentum / static limit  
→ Coulomb behavior  
→ classical electromagnetism as a coherent-field regime

This note is meant to help later revision avoid two common failures:
1. jumping from “local symmetry” to “therefore introduce \(A_\mu\)” too abruptly,
2. gesturing at Coulomb recovery without enough explicit structure to feel explanatory.

---

## 1. What problem this note is solving

Ordinary quantum mechanics often introduces electromagnetic interaction by placing a Coulomb potential into the Hamiltonian. That is useful and often perfectly appropriate as an effective description. But it leaves a deeper question unanswered:

> Why should charged matter interact in that way at all?

QFT, and more specifically QED, answers that question differently. It does not begin from a ready-made potential. It begins from matter fields, local symmetry, and the need to write derivatives that transform correctly under that symmetry. Once that is done, a new field appears, and its quantized excitations become the mediator particles. In an appropriate limit, the familiar Coulomb interaction re-emerges.

So this note is really about one explanatory reversal:

> What ordinary quantum mechanics treats as an inserted potential, QED treats as an effective low-energy remnant of local gauge-field interaction.

---

## 2. Start with a matter field and global phase symmetry

Take a complex matter field \(\psi(x)\). For the purposes of this note, \(\psi\) could be thought of abstractly first, and later as the Dirac field of the electron.

A free matter-field Lagrangian has the general form

$$
\mathcal L_{\text{free}} = \bar\psi(i\gamma^\mu \partial_\mu - m)\psi
$$

for a Dirac field, or an analogous expression for a complex scalar field.

A key feature of such a theory is that it is invariant under a **global** phase transformation:

$$
\psi(x) \to e^{i\alpha}\psi(x),
$$

where \(\alpha\) is a constant, the same everywhere in spacetime.

Why is this important? Because a global phase change does not alter observable physics. The entire field is rotated in complex phase by the same amount everywhere, and the free theory does not care.

This is a \(U(1)\) symmetry.

### 2.1 Why the symmetry is called “global”

It is called global because the same transformation is applied at every point. The phase does not vary from one spacetime point to another.

That distinction will matter enormously in a moment.

### 2.2 Why a complex phase should matter at all

A common beginner reaction is: why should a phase symmetry force so much structure? The reason is that quantum fields are not ordinary real-valued mechanical displacements. They carry complex amplitude structure, and changes in phase are deeply built into how charged matter is represented.

A global phase symmetry already signals that the matter field has an internal direction in a complex plane that is physically redundant at the global level. The next question is what happens if that redundancy is demanded **locally** rather than globally.

---

## 3. Promote the symmetry from global to local

Now suppose we demand invariance under a phase transformation that may vary from point to point:

$$
\psi(x) \to e^{i\alpha(x)}\psi(x).
$$

This is a **local** \(U(1)\) symmetry.

At first this sounds like a modest change. Instead of rotating the field by the same phase everywhere, we rotate it by different phases at different spacetime points.

But mathematically and physically this is a profound demand. It is no longer just a uniform re-labeling of the field’s complex phase. It is a local rephasing, and the derivatives of the field will feel that variation.

That is where the ordinary derivative fails.

---

## 4. Why the ordinary derivative fails

Start from the transformed field:

$$
\psi'(x) = e^{i\alpha(x)}\psi(x).
$$

Now act on it with the ordinary derivative:

$$
\partial_\mu \psi'(x)
=
\partial_\mu\bigl(e^{i\alpha(x)}\psi(x)\bigr).
$$

Using the product rule,

$$
\partial_\mu \psi'(x)
=
e^{i\alpha(x)}\partial_\mu\psi(x)
+
\bigl(\partial_\mu e^{i\alpha(x)}\bigr)\psi(x).
$$

Since

$$
\partial_\mu e^{i\alpha(x)}
=
i(\partial_\mu \alpha)e^{i\alpha(x)},
$$

we get

$$
\partial_\mu \psi'(x)
=
e^{i\alpha(x)}
\left[
\partial_\mu\psi(x)
+
i(\partial_\mu\alpha)\psi(x)
\right].
$$

That extra term is the whole issue.

If the derivative transformed “covariantly,” meaning in the same simple way as the field itself, we would want

$$
\partial_\mu \psi'(x)
\stackrel{?}{=}
e^{i\alpha(x)}\partial_\mu \psi(x).
$$

But that is **not** what happens. The derivative picks up the extra term

$$
i(\partial_\mu\alpha)\psi(x).
$$

So the ordinary derivative is not compatible with local phase symmetry.

### 4.1 Why this matters physically

This is not a minor algebraic irritation. Derivatives enter the kinetic term of the theory, and therefore the equations of motion. If the derivative term fails to transform properly, then the whole Lagrangian fails to be invariant under the local symmetry.

In other words:

- the matter field itself transforms fine,
- but the structure that tells us how the field changes from point to point does not.

This is the moment where the theory forces us to add new structure.

---

## 5. Introduce the covariant derivative

To repair the failure of the ordinary derivative, define a new derivative:

$$
D_\mu = \partial_\mu + ieA_\mu.
$$

Here \(A_\mu(x)\) is a new field, and \(e\) is the coupling constant (later interpreted as electric charge).

Now demand that under the local phase transformation,

$$
\psi(x)\to e^{i\alpha(x)}\psi(x),
$$

the new derivative transform covariantly:

$$
D_\mu \psi(x) \to e^{i\alpha(x)} D_\mu \psi(x).
$$

This requirement determines how \(A_\mu\) must transform.

---

## 6. Derive the gauge-field transformation law

Let

$$
\psi'(x)=e^{i\alpha(x)}\psi(x),
$$

and suppose

$$
A_\mu'(x)
=
A_\mu(x) + \delta A_\mu(x).
$$

Then

$$
D_\mu' \psi'
=
(\partial_\mu + ieA_\mu') e^{i\alpha}\psi.
$$

Expanding,

$$
D_\mu' \psi'
=
\partial_\mu(e^{i\alpha}\psi)
+
ieA_\mu' e^{i\alpha}\psi.
$$

Using the derivative result from above,

$$
D_\mu' \psi'
=
e^{i\alpha}
\left[
\partial_\mu\psi + i(\partial_\mu\alpha)\psi + ieA_\mu'\psi
\right].
$$

For this to equal

$$
e^{i\alpha}D_\mu\psi
=
e^{i\alpha}(\partial_\mu + ieA_\mu)\psi,
$$

the bracketed terms must match:

$$
\partial_\mu\psi + i(\partial_\mu\alpha)\psi + ieA_\mu'\psi
=
\partial_\mu\psi + ieA_\mu\psi.
$$

So

$$
i(\partial_\mu\alpha)\psi + ieA_\mu'\psi = ieA_\mu\psi.
$$

Dividing by \(i\psi\),

$$
\partial_\mu\alpha + eA_\mu' = eA_\mu.
$$

Thus

$$
A_\mu' = A_\mu - \frac{1}{e}\partial_\mu\alpha.
$$

Depending on convention, some signs shift because one may instead define \(D_\mu = \partial_\mu - ieA_\mu\). What matters is the structure:
the gauge field transforms by a derivative of the local phase.

That derivative shift is exactly what cancels the unwanted derivative term from the matter field.

### 6.1 What just happened conceptually

This is the key conceptual move:

- local symmetry broke the ordinary derivative,
- introducing a new field repaired that failure,
- and the transformation law of the new field was not guessed arbitrarily — it was forced by the demand that the derivative transform correctly.

That is why the gauge field is not an optional decorative add-on. It is the new structure required to make local symmetry possible.

---

## 7. Why \(A_\mu\) is naturally interpreted as a connection

The transformation behavior of \(A_\mu\) shows that it is not behaving like an ordinary matter field. It is behaving like a compensating structure that tells us how to compare local phases from point to point.

That is exactly what a connection does.

You can think of the issue this way:
- at each point, the field may be rephased independently,
- so there is no absolute global phase reference,
- therefore comparing “the phase here” to “the phase over there” requires extra geometric information,
- the gauge field supplies that information.

So \(A_\mu\) is best understood not just as “another field,” but as the connection that makes local phase comparison meaningful.

This is why the gauge-field story fits so well with the manuscript’s earlier curvature / connection material. It is the same kind of geometric move:
a local redundancy or local comparison problem requires a connection.

---

## 8. The matter Lagrangian with the covariant derivative

Replace the ordinary derivative in the free matter Lagrangian with the covariant derivative.

For a Dirac field,

$$
\mathcal L_{\text{matter}}
=
\bar\psi(i\gamma^\mu D_\mu - m)\psi.
$$

Insert

$$
D_\mu = \partial_\mu + ieA_\mu.
$$

Then

$$
\mathcal L_{\text{matter}}
=
\bar\psi(i\gamma^\mu \partial_\mu - m)\psi
-
e\,\bar\psi\gamma^\mu A_\mu \psi
$$

up to the sign convention induced by the choice of \(D_\mu\).

This is the crucial result:
the interaction term appears automatically when the ordinary derivative is replaced by the covariant derivative.

So the interaction is not being separately “added in” as an arbitrary force law. It is already implicit in the demand for local symmetry.

That is one of the deepest explanatory advantages of the gauge principle.

---

## 9. The gauge field must also have its own dynamics

So far \(A_\mu\) has been introduced as the compensating field required for local symmetry. But it cannot merely be a passive algebraic placeholder. It must also have its own dynamics.

The appropriate gauge-invariant field strength is

$$
F_{\mu\nu} = \partial_\mu A_\nu - \partial_\nu A_\mu.
$$

This quantity is gauge invariant for the Abelian \(U(1)\) case because the derivative shift terms cancel.

The free gauge-field Lagrangian is

$$
\mathcal L_{\text{gauge}}
=
-\frac{1}{4}F_{\mu\nu}F^{\mu\nu}.
$$

So the full QED Lagrangian is

$$
\mathcal L_{\text{QED}}
=
\bar\psi(i\gamma^\mu D_\mu - m)\psi
-
\frac{1}{4}F_{\mu\nu}F^{\mu\nu}.
$$

This contains:
- the free matter dynamics,
- the matter-gauge interaction,
- and the free gauge-field dynamics.

That is a complete local field theory.

---

## 10. Quantizing the gauge field

At the conceptual level, quantizing the gauge field parallels the scalar-field story:
- decompose the free field into modes,
- quantize those modes,
- interpret the resulting quanta as particles.

For the electromagnetic field, those quanta are photons.

There is an important complication: not every component of \(A_\mu\) represents an independent physical degree of freedom. Gauge symmetry introduces redundancy. So gauge fixing and related machinery are needed for a full technical treatment.

But for the purposes of this repository note, the main conceptual chain is enough:
- the connection field required by local symmetry becomes a dynamical field,
- that field is quantized,
- and its quanta are the mediator particles.

So the photon is not an extra tiny object inserted to carry force between already-primitive electrons. The electromagnetic field comes first, and the photon is its quantized excitation.

---

## 11. Matter–gauge interaction in QED

The interaction term

$$
\mathcal L_{\text{int}}
=
- e\,\bar\psi\gamma^\mu A_\mu\psi
$$

is the heart of QED.

What does it say?

It says that:
- the electron field \(\psi\),
- the positron sector contained in that same field,
- and the electromagnetic field \(A_\mu\)

are locally coupled.

This one term already permits:
- emission of a photon by a charged particle,
- absorption of a photon by a charged particle,
- scattering of charged particles by exchanging photons,
- and, at sufficient energy, pair processes.

So the same local-coupling structure explains both radiation and static force behavior.

That is another major conceptual gain over the old potential-based picture.

---

## 12. From local interaction to photon-mediated scattering

Consider electron–electron scattering. In perturbation theory, the leading-order contribution comes from one exchanged photon.

Diagrammatically this is the familiar tree-level one-photon-exchange graph.

But the important point is not the picture — it is the amplitude structure.

Each interaction vertex contributes a factor of the coupling \(e\) and the appropriate spinor/gamma-matrix structure. The internal photon line contributes the photon propagator. The amplitude is therefore organized around the propagator of the gauge field.

This is how “electromagnetic force” appears in QED:
not as a primitive potential, but as the amplitude structure generated by local matter–gauge coupling.

---

## 13. Why the Coulomb law should emerge in the static / low-momentum limit

The chapter’s explanatory promise is not merely to say “photon exchange causes force.” It is to show why the ordinary Coulomb behavior comes back in the appropriate limit.

The key point is that in the nonrelativistic, low-momentum-transfer, nearly static regime, the exchanged-photon amplitude simplifies.

Very schematically, the photon propagator gives a momentum-space factor behaving like

$$
\frac{1}{q^2},
$$

or, in the static regime where energy transfer is negligible,

$$
\frac{1}{\mathbf q^2},
$$

where \(\mathbf q\) is the spatial momentum transfer.

This is the key object.

So the question becomes:
what spatial potential corresponds to a momentum-space interaction kernel proportional to \(1/\mathbf q^2\)?

The answer is: a \(1/r\) potential.

---

## 14. Why \(1/\mathbf q^2\) turns into \(1/r\)

The relationship comes from Fourier transform.

Very schematically, a potential in position space is related to its momentum-space kernel by an integral of the form

$$
V(\mathbf r)
\propto
\int \frac{d^3q}{(2\pi)^3}
\frac{e^{i\mathbf q\cdot \mathbf r}}{\mathbf q^2}.
$$

The result is proportional to

$$
\frac{1}{r}.
$$

This is a standard Fourier-transform fact in three dimensions:
the inverse transform of \(1/\mathbf q^2\) is proportional to \(1/r\).

So the chain is:

- local gauge coupling gives photon exchange,
- photon exchange gives momentum-space propagator structure,
- static limit reduces this to \(1/\mathbf q^2\),
- Fourier transformation gives \(1/r\),
- and the corresponding force is the familiar inverse-square Coulomb force.

This is the central explanatory reversal:
the Coulomb potential is recovered as a limit of the gauge-field amplitude structure.

It is not where the theory begins.

---

## 15. Why this matters conceptually

This is not a minor technical re-description of the same old idea.

Ordinary quantum mechanics often says:
- here is a Coulomb potential,
- now solve for the electron in that potential.

QED says:
- here is a local matter field,
- here is a local gauge field required by local symmetry,
- here is their interaction term,
- here is the resulting exchange amplitude,
- and in the appropriate limit, the old Coulomb potential emerges.

That is a deeper explanation.

The potential has been demoted from primitive input to effective description.

---

## 16. Classical electromagnetism as a coherent-field regime

The explanatory chain should not stop at Coulomb recovery.

The manuscript’s broader ambition is to unify:
- classical electromagnetic fields,
- and photons,
as two regimes of one underlying object.

The key idea is that a classical field configuration corresponds, in quantum language, to a state with:
- large occupation number,
- stable phase relations,
- and sufficiently suppressed relative quantum fluctuations.

A coherent state is the standard example of such a quantum state.

So the classical electromagnetic field is not a different ontological kind from the photon. It is a regime of the same quantized electromagnetic field in which the wave-like field description becomes macroscopically stable and directly useful.

This means:
- sparse, discrete excitations are naturally described as photons,
- large coherent excitations are naturally described as classical electromagnetic waves or fields.

That is exactly the kind of unification the chapter wants:
particles and classical fields are not rival realities; they are different regimes of the same field.

---

## 17. Compact chain from symmetry to Coulomb

It may help to state the whole chain in one straight line.

### Step 1
A free matter field has a global phase symmetry.

### Step 2
Demanding the symmetry locally makes the ordinary derivative fail.

### Step 3
To repair that failure, introduce a covariant derivative and a new field \(A_\mu\).

### Step 4
That field transforms so as to cancel the derivative-of-phase term.

### Step 5
The new field is naturally interpreted as a connection.

### Step 6
Replacing \(\partial_\mu\) by \(D_\mu\) automatically produces a local interaction term.

### Step 7
The gauge field has its own dynamics and is quantized; its quanta are photons.

### Step 8
Matter–matter interaction can then be described by photon exchange.

### Step 9
In the static / low-momentum-transfer limit, the momentum-space kernel behaves like \(1/\mathbf q^2\).

### Step 10
The Fourier transform of that gives \(1/r\).

### Conclusion
The Coulomb interaction is recovered as the low-energy, long-distance remnant of local gauge-field interaction.

---

## 18. Common confusions this note is meant to prevent

### Confusion 1: “The gauge field is just added in by hand”
No. The local-symmetry requirement forces the compensating structure once one insists the derivative transform properly.

### Confusion 2: “Covariant derivative is just notation”
No. It is the repaired derivative that makes local symmetry possible.

### Confusion 3: “The interaction term is separately chosen after the symmetry story”
No. It appears automatically when the covariant derivative is inserted into the matter Lagrangian.

### Confusion 4: “Photon exchange is just a pictorial story unrelated to the mathematics”
No. It is the perturbative manifestation of the local matter–gauge coupling and the photon propagator.

### Confusion 5: “Coulomb force is the fundamental thing, and QED merely rephrases it”
Backward. Coulomb behavior is the effective low-energy limit of the more fundamental field-theoretic interaction.

### Confusion 6: “Classical electromagnetic fields and photons are different ontological kinds”
No. They are different regimes of the same quantized gauge field.

---

## 19. Likely future uses of this note

A later reviser could mine this note for:
- a slower derivation of why the ordinary derivative fails,
- a more patient introduction of the covariant derivative,
- a stronger explanation of the gauge field as connection,
- a cleaner argument that the interaction term is symmetry-forced,
- a more explicit QED-to-Coulomb payoff passage,
- and a stronger unification of classical electromagnetic fields with photon language.

---

## 20. Final compact statement

QED begins not from a Coulomb potential, but from a matter field with local phase symmetry.  
Local symmetry breaks the ordinary derivative.  
Repairing that derivative requires a gauge field.  
That gauge field is a connection with its own dynamics.  
Its local coupling to matter produces the interaction term of QED.  
Quantizing the gauge field yields photons.  
In the low-momentum, static limit, the exchange amplitude reduces to a \(1/\mathbf q^2\) kernel.  
The Fourier transform of that kernel produces \(1/r\).  
So Coulomb behavior is not primitive. It is a limit of local gauge-field interaction.  
Classical electromagnetism and photons are two regimes of the same quantized field.
