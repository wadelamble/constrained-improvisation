# Technical check of the quantum-state action

This supports the claim in footnote 5 of the candidate introduction. It is not manuscript prose.

For a time-independent self-adjoint Hamiltonian, define

```math
D=i\hbar\partial_t-\hat H,
\qquad
\mathcal A[\Psi]=\int_{t_1}^{t_2}dt\,\langle\Psi|D|\Psi\rangle.
```

Variations of the bra and ket, vanishing at the time endpoints, give the Schrödinger equation and its adjoint. This is a variational principle for quantum-state histories. It is not the classical field action varied over individual field configurations. An initial vector and specified dynamics determine the final vector; fixing both compatible endpoints in a variational calculation does not make them independent initial data.

Assume a unitary representation of the proper orthochronous Poincaré group (or its cover), with this same Hamiltonian as time-translation generator. Write its action on time-zero data as $U(g)$. On equal-time histories the induced dynamical action is

```math
W_g(t)=e^{-i\hat Ht/\hbar}U(g)e^{i\hat Ht/\hbar}.
```

Direct differentiation gives

```math
i\hbar\dot W_g=[\hat H,W_g],
\qquad D W_g=W_gD.
```

Therefore, for admissible trial histories, not only solutions,

```math
\mathcal A[W_g\Psi]
=\int dt\,\langle\Psi|W_g^\dagger D W_g|\Psi\rangle
=\int dt\,\langle\Psi|D|\Psi\rangle
=\mathcal A[\Psi].
```

Boosts need not commute with the Hamiltonian. Their equal-time realization is time dependent, and this dependence supplies the required term in the identity above. Applying a time-independent boost to the state while keeping the same Hamiltonian and time slicing is not the calculation above.

The same algebra works formally for any initial-data unitary. It therefore does not prove that an arbitrary Hamiltonian is relativistic or derive its form. The substantive assumption is a physical Poincaré representation with the correct generators and spacetime action on observables. The usual qualifications about operator domains and well-defined evolution apply. This establishes stationarity and action invariance, not minimization. A specified state-vector phase convention gives a unique vector history; the physical history is a history of rays.

## Primary references

- [Kobe, *Lagrangian Densities and Principle of Least Action in Nonrelativistic Quantum Mechanics*, §3](https://arxiv.org/pdf/0712.1608) gives a wave-function action and derives the Schrödinger equation by variation.
- [Torres del Castillo and Herrera Flores, *Symmetries of the Hamiltonian operator and constants of motion*, §2](https://arxiv.org/pdf/1510.04876) gives the condition for time-dependent unitary transformations to preserve the Schrödinger dynamics. The action identity above is a direct calculation using that condition, not a quoted theorem from the paper.
- [Dirac, *Forms of Relativistic Dynamics*](https://journals.aps.org/rmp/abstract/10.1103/RevModPhys.21.392) treats realizations of relativistic dynamics and the role of dynamical generators.
