1. poetic intro
2. philosophical trends toward humility perspectivalism
3. purposes
3.1 teach as someone who is learning
3.2 conceptual economy elegance natural philosophy - example of reading relativity
3.2.1 no historical
3.2.2 no problem solving
3.3 heavy visualization like 3 blue 1 brown
3.4 use the math we need, learn it as we go
3.5 have some fun
4. the conceptual map
4.1 symmetry
4.2 unitarity
4.3 locality
4.4 variational
4.5 Quantum


for symmetry draft

“then one other question. if you take poincare seriously, and you take -fields- seriously, and you take unitary evoution seriously, then you just have to get U(1). Why not at that point just name a new group Poincare+U(1). Why not just say U(1) -is- a spacetime symmetry.”
One the above. I think a problem iwht the current chapter and a thing the critic was complaining about is that I was sort of saying "look H3 is a symmetry group, and it has unitarity, so there you go, nature has unitarity." that's inverted. It needs to be "H3 is a symmetry group. Nature is unitary (this is imported as an a priori). Unitary has to preserve the [x,k] commutator (phase), so nature forces a relationship on x/k (coupling their 'parallelogram sides').

Yes. **That is the right direction of explanation.** Unitarity of closed-system evolution is an independent physical premise. Finding a unitary representation of $H_3$ does not establish that premise.

We have already found the relationship

```math
[X,K]=iI,
```

where $iI$ generates overall phase. Under unitary evolution, the corresponding evolved operators are $X(t)=U^\dagger XU$ and $K(t)=U^\dagger KU$. Consequently,

```math
[X(t),K(t)]
=U^\dagger[X,K]U
=iI.
```

Their relationship survives evolution. This is the standard [Heisenberg description of evolution](https://www.damtp.cam.ac.uk/user/tong/qft/qfthtml/S2.html#S2.SS6).

**Your “coupling their parallelogram sides” captures a real constraint.** For example, suppose evolution simply rescales the two operators:

```math
X(t)=aX,\qquad K(t)=bK.
```

Then preserving their commutator requires

```math
ab=1.
```

Here, shortening one side requires lengthening the other.

For general evolution, the lasting claim is **preservation of the canonical relationship**. The literal parallelogram picture applies when the transformation of $X,K$ is linear. “Coupled” means their changes must satisfy that shared constraint, not that both must always change.

That gives the group structure a definite role: once we require unitary evolution, its existing relationship between $x$ and $k$ constrains how they can evolve together.