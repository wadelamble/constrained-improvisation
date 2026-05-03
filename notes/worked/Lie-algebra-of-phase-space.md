# Lie Algebra of Phase Space


## some notes
notes: function are generators, p <-> x, but p special \(\{f,H\}=0=\{H,f\}
\) b/c commutes with H, 


## bot generated
Phase space does not come equipped with a canonical distance. One can impose a metric on it by hand, but Hamiltonian mechanics does not single one out. What phase space comes with intrinsically is a symplectic area form:

```math
\omega = dq^i \wedge dp_i.
```

This means that the relevant invariant is not length but oriented area. In Euclidean or Minkowski geometry, the invariant object is a metric, and the corresponding allowed transformations are those that preserve that metric. In phase space, the invariant object is the symplectic form, and the corresponding allowed transformations are those that preserve it. These are the canonical transformations.

A canonical transformation is therefore not merely a convenient change of variables. It is a change of phase-space coordinates that leaves intact the area structure in which Hamiltonian dynamics is written. Some canonical transformations also preserve ordinary Euclidean distance, but that is an extra fact about them, not part of what makes them canonical.

In the simplest one-degree-of-freedom case, consider

```math
(Q,P) = (2q,p/2).
```

This preserves the symplectic form, since

```math
dQ \wedge dP
=
2\,dq \wedge \frac{1}{2}\,dp
=
dq \wedge dp.
```

But it does not preserve ordinary Euclidean distance. A unit step in the $q$ direction is doubled, while a unit step in the $p$ direction is halved. Lengths change, but symplectic area does not.

Likewise, a shear such as

```math
(Q,P) = (q+kp,p)
```

is also canonical, since

```math
dQ \wedge dP
=
(dq+k\,dp)\wedge dp
=
dq \wedge dp,
```

yet it does not preserve Euclidean length or angle. The point is that symplectic geometry does not demand rigid metric shape. It demands preservation of the area structure.

Hamiltonian time evolution sits inside this larger class. For each fixed time $t$, the evolution map from the initial state to the state at time $t$ is a canonical transformation. The Hamiltonian picks out one particular one-parameter family inside the larger space of allowable canonical transformations.
