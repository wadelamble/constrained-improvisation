# To-be-used-material

## Unitarity

Before introducing the full machinery of quantum mechanics, it is worth isolating one requirement that already tells us a great deal about what the theory must look like. If the basic object of the theory is not a point in phase space but a superposition of amplitudes, then its evolution cannot be arbitrary. It must preserve the structure that makes those amplitudes physically meaningful. That requirement is unitarity.

Let the state of a system be represented by a vector $`\mid \psi\rangle`$in a complex vector space equipped with an inner product $`\langle\phi \mid \psi\rangle`$. This inner product is not an ornamental extra. It is the structure from which the measurable content of the theory is built. Norms come from it. Overlaps come from it. Transition amplitudes come from it. Once probabilities are extracted from squared overlaps, the inner product becomes the quantity whose preservation matters.

An allowed time evolution must therefore preserve that inner product. If the state evolves by a linear map $`U`$, then the condition is

``` math
\langle U\phi \mid U\psi\rangle = \langle\phi \mid \psi\rangle
```

for all states $`\mid \phi\rangle`$and $`\mid \psi\rangle`$. A map with this property is called unitary. In operator form, this is

``` math
U^{\dagger}U = I.
```

That compact equation says a great deal. It says the evolution may rotate the state in its abstract space, it may mix components, it may alter phases, but it may not stretch, shrink, or scramble the geometry that gives the state physical meaning.

This geometry is richer than ordinary Euclidean geometry because the inner product is complex. If we temporarily view the complex vector space as a real one with extra structure, then the inner product splits into two parts,

``` math
\langle\phi \mid \psi\rangle = g(\phi,\psi) + i\text{â€‰}\omega(\phi,\psi),
```

where

``` math
g(\phi,\psi) = Re\text{â€‰}\langle\phi \mid \psi\rangle,\omega(\phi,\psi) = Im\text{â€‰}\langle\phi \mid \psi\rangle.
```

The real part $`g`$plays the role of a metric-like structure. It measures lengths and angles. The imaginary part $`\omega`$is antisymmetric and area-like. It is the Hilbert-space remnant of the symplectic structure that classical mechanics preserves in phase space. In classical mechanics, lawful evolution preserves symplectic area. In quantum mechanics, lawful evolution preserves something stronger. It preserves the entire complex inner product, and therefore preserves both the metric-like and symplectic-like parts at once. Symplecticity has not disappeared. It has been absorbed into unitarity.

This is one reason quantum theory needs Hilbert space rather than ordinary configuration space. A wave-like state carries internal structure. Its components do not merely list mutually exclusive possibilities. They coexist with relative magnitudes and relative phases, and those relative phases affect future outcomes through interference. The state is therefore not just a distribution over alternatives. It is a single object whose parts can reinforce or cancel one another. A theory of such objects needs a geometry that can keep track of both size and phase relations. The complex inner product does exactly that.

Consider a state written as a superposition,

``` math
\mid \psi\rangle = \sum_{n}^{}c_{n} \mid n\rangle.
```

The coefficients $`c_{n}`$are amplitudes, not probabilities. Their squared magnitudes may eventually be read probabilistically in a suitable basis, but the state itself contains more than those magnitudes. It also contains the phase relations among the $`c_{n}`$. Those phases are not decorative. They are what make interference possible. Under unitary evolution,

``` math
\mid \psi(t)\rangle = U(t) \mid \psi(0)\rangle,
```

the amplitudes change, but they change in a way that preserves the full pattern of relations among components. A superposition may spread, twist, and recombine, but it does not come apart. The geometry that makes interference meaningful is carried forward intact.

From this one condition follow many of the most familiar features of quantum mechanics.

First, unitarity preserves norm. Since

``` math
\langle\psi(t) \mid \psi(t)\rangle = \langle\psi(0) \mid \psi(0)\rangle,
```

a normalized state remains normalized. This is why total probability is conserved in a closed quantum system. But probability conservation is only the most visible consequence, not the deepest one.

Second, unitarity preserves transition amplitudes and therefore transition probabilities. If two states have a given overlap now, they retain that overlap after both are evolved. The mutual relations among states are not distorted.

Third, unitarity preserves angles and orthogonality. If two states are orthogonal, meaning perfectly distinguishable in principle, then unitary evolution keeps them orthogonal. Quantum evolution may make a state harder for us to describe in everyday terms, but it does not erase the distinctions the theory itself makes. Distinguishability is preserved.

Fourth, unitarity makes closed-system evolution reversible. Since $`U^{\dagger}U = I`$, the inverse of $`U`$exists and is $`U^{\dagger}`$. One can run the evolution backward. This does not mean that every practical process in the world is reversible. Measurements, coarse-graining, and open-system effects complicate the story. But the underlying law for an isolated system does not discard information. It transforms without tearing.

These consequences are often taught separately. Probability conservation is presented in one place, reversibility in another, orthogonality in another. But they are all facets of the same geometric fact. A unitary evolution preserves the full inner-product structure of state space.

This gives quantum mechanics a kind of continuity very different from classical continuity. In classical mechanics, a system remains itself by tracing a path through phase space. In quantum mechanics, a state need not follow a sharp trajectory at all. It may be spread across many possibilities. It may evolve into a superposition whose components correspond to outcomes that classical language would regard as incompatible. Yet the state is not thereby destroyed into a formless cloud. What persists is not a point, but a structure. What survives is not certainty, but identity of form.

That is why unitarity deserves to be understood before the usual interpretive puzzles arrive. It tells us that quantum uncertainty is not chaos. Superposition does not mean that anything goes. The amplitudes evolve under a severe constraint. Their total geometric organization must be preserved. Norm is preserved. Distinguishability is preserved. Reversibility is preserved. The metric-like and symplectic-like aspects of the theory are preserved together.

Unitarity, then, is the principle that pulls identity out of the ashes of uncertainty. A quantum state may be indefinite with respect to many classical questions, but it is not without structure, and that structure is not allowed to decay under lawful evolution. The state may rotate through possibility, but it must remain itself.
