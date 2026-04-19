# Modes, Fock Space, and Particle Emergence — worked note

*Repository support note.* This file is not polished manuscript prose. It is a slower, more explicit technical note meant to preserve intermediate explanatory rungs that the current QFT draft handles more compactly. Its focus is the chain

local field  
→ Fourier / normal modes  
→ diagonalized free Hamiltonian  
→ quantized oscillators  
→ ladder operators  
→ vacuum  
→ Fock space  
→ particle interpretation

This note is meant to be mined later by a human or agent revising the chapter.

---

## 1. What problem this note is solving

A free relativistic scalar field can be written locally in position space as a field value at every point. That is the right way to see locality, causality, and the equation of motion. But it is *not* yet the best way to see why the field should have quantized excitations that deserve to be called particles.

The main reason is that in position space the free field looks like one enormous coupled system. Neighboring points are tied together by the spatial derivative term. The local description is honest about propagation, but it hides the independent dynamical pieces.

So this note is really about one major conceptual move:

> The field is first understood locally in spacetime, but it becomes easiest to quantize when rewritten in the basis singled out by translation symmetry.

That is the whole chain in one sentence.

---

## 2. Start from the local classical field

Take a real scalar field \(\phi(\mathbf x,t)\) with Lagrangian density

$$
\mathcal L
=
\frac{1}{2}\partial_\mu \phi\,\partial^\mu \phi
-
\frac{1}{2}m^2\phi^2.
$$

In non-covariant form, with the \((+,-,-,-)\) sign convention, this is

$$
\mathcal L
=
\frac{1}{2}(\partial_t\phi)^2
-
\frac{1}{2}(\nabla \phi)^2
-
\frac{1}{2}m^2\phi^2.
$$

The Euler–Lagrange equation is the Klein–Gordon equation

$$
(\Box + m^2)\phi = 0,
$$

or

$$
\partial_t^2 \phi - \nabla^2 \phi + m^2\phi = 0
$$

in natural units.

At this stage the field is a local object in spacetime. The value of the field at one point is coupled to nearby points through the gradient term. That is good — locality should be visible. But the field is not yet written in the basis where the free dynamics are simplest.

---

## 3. Why Fourier modes are the right next step

### 3.1 Not “because Fourier transforms are useful”

That is true but too weak. The deeper reason is symmetry.

If the free theory is spatially translation-invariant, then its natural basis is the basis in which translations act simply. Plane waves do that. A plane wave is an eigenfunction of the translation operator. Translating it multiplies it by a phase.

So when the field is expanded in plane waves, that is not an arbitrary mathematical trick. It is the basis adapted to the symmetry of the free theory.

### 3.2 What a mode really is

This is a place where many presentations go too fast.

A mode is not “the field at one momentum value” in some shallow bookkeeping sense. A mode is a whole-field spatial pattern — spread across all space — whose time-dependent amplitude evolves independently of the other such patterns in the free theory.

If you have ever diagonalized a coupled spring system, the analogy is direct:
- the original coordinates are local displacements,
- the normal-mode coordinates are collective patterns,
- and each pattern has one amplitude that oscillates independently.

The field case is the infinite-dimensional version of that same idea.

---

## 4. Fourier decomposition of the field

Put the field in a finite box of volume \(V\) first, so the momentum labels are discrete. Then

$$
\phi(\mathbf x,t)
=
\frac{1}{\sqrt V}
\sum_{\mathbf k}
Q_{\mathbf k}(t)e^{i\mathbf k\cdot \mathbf x}.
$$

Because the field is real,

$$
Q_{-\mathbf k}(t)=Q_{\mathbf k}^*(t).
$$

In infinite volume, the sum becomes an integral:

$$
\phi(\mathbf x,t)
=
\int \frac{d^3k}{(2\pi)^3}\,
Q_{\mathbf k}(t)e^{i\mathbf k\cdot \mathbf x}.
$$

The local field has now been rewritten in terms of mode amplitudes \(Q_{\mathbf k}(t)\). The key question is: what equations do these mode amplitudes satisfy?

Insert the Fourier expansion into the Klein–Gordon equation:

$$
\partial_t^2 \phi - \nabla^2 \phi + m^2\phi = 0.
$$

The spatial Laplacian acting on a plane wave gives

$$
\nabla^2 e^{i\mathbf k\cdot \mathbf x}
=
-\,\mathbf k^2 e^{i\mathbf k\cdot \mathbf x}.
$$

So each mode satisfies

$$
\ddot Q_{\mathbf k}(t) + \omega_{\mathbf k}^2 Q_{\mathbf k}(t) = 0,
$$

with

$$
\omega_{\mathbf k}^2 = \mathbf k^2 + m^2.
$$

This is the decisive simplification:
each mode amplitude obeys the equation of a simple harmonic oscillator.

---

## 5. Why this means the Hamiltonian is diagonal in momentum space

The Lagrangian density gives the canonical momentum field

$$
\pi(\mathbf x,t) = \frac{\partial \mathcal L}{\partial(\partial_t\phi)} = \partial_t \phi(\mathbf x,t).
$$

The Hamiltonian density is

$$
\mathcal H
=
\pi\,\partial_t\phi - \mathcal L
=
\frac{1}{2}\pi^2 + \frac{1}{2}(\nabla \phi)^2 + \frac{1}{2}m^2\phi^2.
$$

So the Hamiltonian is

$$
H
=
\int d^3x\,
\left[
\frac{1}{2}\pi^2
+
\frac{1}{2}(\nabla \phi)^2
+
\frac{1}{2}m^2\phi^2
\right].
$$

Now rewrite \(\phi\) and \(\pi\) in Fourier modes. Orthogonality of the plane waves eliminates cross terms between different \(\mathbf k\)-values. The Hamiltonian becomes a sum over independent mode Hamiltonians:

$$
H
=
\sum_{\mathbf k}
\left[
\frac{1}{2}P_{\mathbf k}P_{-\mathbf k}
+
\frac{1}{2}\omega_{\mathbf k}^2
Q_{\mathbf k}Q_{-\mathbf k}
\right],
$$

or the corresponding integral form in the continuum.

This is what “diagonalizing the free Hamiltonian” means here. It means:
- in position space the field degrees of freedom are coupled,
- in momentum space the free theory separates into independent oscillators.

Nothing quantum has happened yet. But the structure that quantization will act on is finally visible.

---

## 6. Why the simple harmonic oscillator matters so much

The simple harmonic oscillator is not just a toy example in pre-QFT quantum mechanics. It is the prototype for every free bosonic field mode.

For one oscillator of frequency \(\omega\),

$$
H = \frac{P^2}{2} + \frac{1}{2}\omega^2 Q^2
$$

(using units where the mass-like coefficient has been absorbed for simplicity).

Quantization promotes \(Q\) and \(P\) to operators with

$$
[\hat Q,\hat P]=i\hbar.
$$

Then define ladder operators

$$
\hat a
=
\sqrt{\frac{\omega}{2\hbar}}\,\hat Q
+
\frac{i}{\sqrt{2\hbar\omega}}\,\hat P,
$$

$$
\hat a^\dagger
=
\sqrt{\frac{\omega}{2\hbar}}\,\hat Q
-
\frac{i}{\sqrt{2\hbar\omega}}\,\hat P.
$$

These satisfy

$$
[\hat a,\hat a^\dagger]=1.
$$

The Hamiltonian becomes

$$
\hat H
=
\hbar\omega
\left(
\hat a^\dagger \hat a + \frac{1}{2}
\right).
$$

The meaning of this form is extremely important:
- \(\hat a^\dagger \hat a\) counts excitations,
- the energies are discrete,
- the ground state is not zero-energy but carries zero-point energy.

The field mode will inherit exactly this structure.

---

## 7. Quantizing each field mode

For each momentum mode \(\mathbf k\), promote \(Q_{\mathbf k}\) and \(P_{\mathbf k}\) to operators:

$$
[\hat Q_{\mathbf k}, \hat P_{\mathbf k'}]
=
i\hbar\,\delta_{\mathbf k\mathbf k'}
$$

in box normalization, or a delta function in continuum normalization.

Define ladder operators for each mode:

$$
\hat a_{\mathbf k}
=
\sqrt{\frac{\omega_{\mathbf k}}{2\hbar}}\,
\hat Q_{\mathbf k}
+
\frac{i}{\sqrt{2\hbar\omega_{\mathbf k}}}\,
\hat P_{\mathbf k},
$$

$$
\hat a_{\mathbf k}^\dagger
=
\sqrt{\frac{\omega_{\mathbf k}}{2\hbar}}\,
\hat Q_{-\mathbf k}
-
\frac{i}{\sqrt{2\hbar\omega_{\mathbf k}}}\,
\hat P_{-\mathbf k}.
$$

Then

$$
[\hat a_{\mathbf k}, \hat a_{\mathbf k'}^\dagger]
=
\delta_{\mathbf k\mathbf k'}.
$$

The Hamiltonian becomes

$$
\hat H
=
\sum_{\mathbf k}
\hbar\omega_{\mathbf k}
\left(
\hat a_{\mathbf k}^\dagger \hat a_{\mathbf k}
+
\frac{1}{2}
\right).
$$

This is the key payoff of the whole diagonalization story:

> a free quantum field is an infinite collection of quantized harmonic oscillators, one for each momentum mode.

That sentence should be read carefully. It does **not** mean the field is “really many separate things” in a naive sense. It means the free Hamiltonian separates in a basis of independent collective modes, and each of those modes quantizes like an oscillator.

---

## 8. The vacuum

The vacuum state \(|0\rangle\) is defined by

$$
\hat a_{\mathbf k}|0\rangle = 0
\qquad
\text{for every } \mathbf k.
$$

This is one of the most important conceptual corrections QFT makes to ordinary language.

“Vacuum” does **not** mean:
- no field,
- or the absence of all structure.

It means:
- the lowest-energy state of the field,
- with every mode in its ground state.

This is why the vacuum still carries formal zero-point energy:

$$
E_{\text{vac}}
=
\frac{1}{2}
\sum_{\mathbf k}
\hbar\omega_{\mathbf k}.
$$

For later technical purposes, this quantity raises well-known issues. But the main conceptual point here is earlier than that:
the vacuum is not emptiness between particles; it is the ground state of the field.

That alone is a major ontological shift.

---

## 9. One-particle and many-particle states

Once the vacuum is defined, one builds excitations on top of it.

A one-particle state of momentum \(\mathbf k\) is

$$
|\mathbf k\rangle = \hat a_{\mathbf k}^\dagger |0\rangle.
$$

A two-particle state is

$$
|\mathbf k_1,\mathbf k_2\rangle
=
\hat a_{\mathbf k_1}^\dagger
\hat a_{\mathbf k_2}^\dagger
|0\rangle.
$$

More generally,

$$
|\mathbf k_1,\mathbf k_2,\dots,\mathbf k_n\rangle
=
\hat a_{\mathbf k_1}^\dagger
\hat a_{\mathbf k_2}^\dagger
\cdots
\hat a_{\mathbf k_n}^\dagger
|0\rangle.
$$

For a bosonic scalar field, the creation operators commute, so the order does not matter. A single mode can be occupied arbitrarily many times.

This is where the particle concept becomes precise.

A particle is not inserted at the beginning as a primitive object. It is recovered as a quantized excitation of a field mode.

This is the deep ontological reversal:
- old picture: start with particles, then attach waves;
- QFT picture: start with fields, then recover particles as excitations.

---

## 10. Fock space

The Hilbert space of a single fixed-particle-number system is not enough for a field. A field can be in:
- the vacuum sector,
- a one-particle sector,
- a two-particle sector,
- and so on.

So the full state space is the direct sum of all particle-number sectors:

$$
\mathcal F
=
\mathcal H_0
\oplus
\mathcal H_1
\oplus
\mathcal H_2
\oplus
\cdots
$$

This is Fock space.

A convenient basis is the occupation-number basis:

$$
|n_{\mathbf k_1},n_{\mathbf k_2},n_{\mathbf k_3},\dots\rangle,
$$

where each \(n_{\mathbf k}\) is a nonnegative integer.

This is more than a notational convenience. It solves one of the structural limitations of early quantum mechanics.

In many ordinary QM setups, the number of particles is part of the problem statement. In QFT, the number of particles is part of the state.

That is a profound difference:
- fixed-particle quantum mechanics has a Hilbert space too small for emission, absorption, and creation processes to be native;
- QFT’s Fock space contains all those sectors from the beginning.

---

## 11. Rebuilding the local field from the mode operators

One might worry that once everything is expressed in momentum modes and ladder operators, locality has been lost. It has not. The local field operator is reconstructed from those modes:

$$
\hat\phi(\mathbf x,t)
=
\int \frac{d^3k}{(2\pi)^3}
\frac{1}{\sqrt{2\omega_{\mathbf k}}}
\left(
\hat a_{\mathbf k} e^{i\mathbf k\cdot\mathbf x - i\omega_{\mathbf k}t}
+
\hat a_{\mathbf k}^\dagger e^{-i\mathbf k\cdot\mathbf x + i\omega_{\mathbf k}t}
\right),
$$

again up to normalization convention.

This expression is worth unpacking slowly.

- The plane-wave factors come from translation symmetry.
- The ladder operators come from oscillator quantization.
- The whole object is still local in spacetime in the sense that \(\hat\phi(\mathbf x,t)\) is an operator attached to the spacetime point \((\mathbf x,t)\).

So the momentum-space and local-spacetime descriptions are not rivals. The local field is built from momentum modes, and the momentum modes are simply the basis in which the free Hamiltonian diagonalizes.

This is one of the chapter’s main philosophical balances:
- locality is most vivid in spacetime,
- independence of the free dynamics is most vivid in momentum space,
- quantum states live in Fock space,
- and the field operator bridges them.

---

## 12. Why this chain explains particle emergence

It is worth now stating the entire chain in compact form.

### Step 1
A classical relativistic field is a local object distributed over spacetime.

### Step 2
Because the free theory is translation-invariant, the field is naturally expanded in plane-wave modes.

### Step 3
In that basis the free Hamiltonian diagonalizes into independent oscillators.

### Step 4
Each oscillator is quantized using the same ladder-operator logic as the ordinary quantum harmonic oscillator.

### Step 5
The vacuum is the state with no excitations in any mode.

### Step 6
Applying creation operators builds one-particle and many-particle states.

### Step 7
The direct sum of all particle-number sectors is Fock space.

### Step 8
The field operator, rebuilt from these mode operators, is the local object that can create or destroy excitations.

### Conclusion
Particles are the quantized excitations of fields.

This is the cleanest technical route to the chapter’s main ontological claim.

---

## 13. Why this also explains variable particle number

The free Hamiltonian is diagonal in number operators, so in the free theory the occupation number of each mode is conserved.

But once interaction terms are added, the Hamiltonian contains products of several creation and annihilation operators. Schematically, an interaction term might look like combinations of

$$
\hat a^\dagger \hat a^\dagger \hat a,
\qquad
\hat a^\dagger \hat a^\dagger \hat a \hat a,
\qquad
\text{etc.}
$$

depending on the theory.

Such terms mix sectors with different occupation numbers. So particle creation and annihilation are no longer anomalies relative to the formalism. They are exactly what the formalism is built to allow.

This is why Fock space is not an optional elaboration. It is required if the theory is to describe real interacting microscopic physics.

---

## 14. Common confusions this note is meant to prevent

### Confusion 1: “The field becomes many separate particles”
Not really. The field remains primary. The mode decomposition is a basis change for the free theory.

### Confusion 2: “Momentum space replaces position space”
No. Momentum space diagonalizes the free dynamics. Position space keeps locality visible.

### Confusion 3: “A particle is just whatever has definite momentum”
Too crude. Exact momentum eigenstates are one clean free basis, but localized wave packets are superpositions of those modes. The deeper statement is that particles are excitation structures in the quantized field.

### Confusion 4: “The vacuum means nothing exists”
No. It means the field is in its lowest-energy state.

### Confusion 5: “QFT adds particles on top of fields”
Backward. QFT starts with fields and recovers particles from their quantized excitations.

---

## 15. Likely future uses of this note

A later agent or human reviser could mine this note for:

- a slower version of the momentum-basis section,
- a stronger explanation of diagonalization,
- a more patient transition from oscillator to field quantization,
- a fuller explanation of the vacuum,
- a stronger articulation of why Fock space is structurally necessary,
- and a more precise bridge between local fields and particle states.

---

## 16. Final compact statement

The field is first encountered as a local relativistic object in spacetime.  
The free theory is then rewritten in the basis selected by translation symmetry.  
In that basis the free Hamiltonian becomes a sum of independent oscillators.  
Quantizing those oscillators yields ladder operators, a vacuum, and Fock space.  
Particles emerge as the countable excitations of the field modes.  
The field remains primary. The particle is what the field looks like when one counts its quantized excitations.
