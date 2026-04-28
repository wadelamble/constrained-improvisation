# Hamiltonian Mechanics

## Why Another Mechanics?

Lagrangian Mechanics already gives us a remarkably deep way to do physics. We write down an invariant quantity, extremize it, and recover the physical path. The particle, we may say, has "learned" what the right trajectory is by solving an optimization problem. While this global perspective perhaps feels less orthodox in physics than the local differential-equation perspective, only it suggests an answer to the question of why dynamical laws exist. Here we will discuss Hamiltonian Mechanics, the modern local formulation of mechanics, for two reasons. First, it brings to light physical structure, with an accompanying geometric and algebraic structure, that is essential to understanding the evolution of statistical states. Second, and relatedly, it expresses kinematic structure in the language of generator algebra, which is indispensable when formulating quantum mechanics.

## Information Evolution in Physical Systems

One might justifiably think that the content of our physical laws is limited to predicting future histories from initial conditions. Yet in conservative systems, where energy is never given off to a heat bath but is instead continuously traded between potential and kinetic form, our laws make the additional implication that the information encoded in the arrangement of the probability density over possible instantaneous states is never lost. This is a categorically different kind of claim. It is not about one particle's specific initial conditions and its future, but about the information-theoretic behavior of a statistical ensemble of initial conditions drawn from a distribution. How can laws that seem wholly oriented toward initial states and future trajectories contain implications about ensembles, whose members, by definition, follow independent trajectories? The answer we will arrive at lies in the structural relationship between paired position and momentum, which defines a measure of information content, and in the way a conservative system preserves that measure.

### Example -- Set Permutation
We can get a feel for this kind of structure in the example of permuting a set. Take a deck of three cards labeled `A`, `B`, and `C`. The exact possible states are the six deck orders

```text
ABC, ACB, BAC, BCA, CAB, CBA.
```

Now choose one specific permutation of these states, for example: move the top card to the bottom. Then

```text
ABC -> BCA
BCA -> CAB
CAB -> ABC
ACB -> CBA
CBA -> BAC
BAC -> ACB
```

And assign a probability distribution on these six exact states. For example,

```text
P(ABC) = 1/2
P(BAC) = 1/3
P(CBA) = 1/6
```

with all other states assigned probability `0`. After applying the permutation to all arrangements consistent with the distribution, the distribution becomes

```text
P(BCA) = 1/2
P(ACB) = 1/3
P(BAC) = 1/6
```

with all other states still assigned probability `0`. The same probability weights are still present. They have only been reassigned to different exact states.

Let's make a few observations about this example:
1. An initial arrangement is unique.
2. Under a given permutation rule, a new arrangement is dictated by the previous arrangement.
3. We can run the permutation in reverse and recover the original arrangement.
4. Two arrangements under the same number of permutations remain distinct.

These properties, which we will show exist in physical situations, are what we mean by "determinism" and "reversibility" and, following from these, by "distinguishability" of the ensemble under time evolution.

We can map the elements of our card deck to Hamiltonian mechanics, in which "phase space" is position/momentum space for one body, or the product of such for multiple bodies.

1. An arrangement -> an \(instantaneous\) state
2. All possible arrangements -> phase space
3. The count of distinct arrangements in a collection -> phase space area

The last of these elements is what we call a "measure" on the space. A measure has a role analogous to a metric, though it does something different. A metric measures separation. A measure assigns size to regions or collections. In the present case, what matters is that when such a quantity is preserved under transformation, it encodes some regularity or structure in the space. Conservative systems bestow an "incompressibility" on phase space. In our card deck, the discrete analogue is already built in by the fact that the law is a permutation, so collections of arrangements are rearranged without losing or gaining members.

### Example -- Mass on a Spring

We see this same structure in physical systems. Consider a mass on a spring. To speak experimentally about a probability distribution over initial conditions, we need an ensemble, that is, many runs of the same system, prepared by the same procedure, with initial position and momentum drawn from some distribution around an average starting state. At the initial time, measurements across the ensemble reveal that distribution. We then let each member of the ensemble evolve under the same conservative law, and at some later time we again measure position and momentum across the ensemble. Those later measurements reveal a new distribution.

At the full position/velocity space level, we observe, again, that the distribution is not flattened or sharpened by the dynamics. Rather, each exact initial state in the ensemble is carried to one exact later state, so the later distribution is the earlier one transported by the law of motion. In a dissipative system, nearby runs can truly be driven together, so distinctions among initial conditions are washed out. The extreme example of such a dissipative system is one in which all initial conditions end at rest. But in a conservative system, such distributions are not washed out. They are transported onto new ensembles.

As promised, this is the direct analogue of the permutation example. There, the state space was a finite set, the natural measure was counting measure, and the law was a permutation. Here, the state space is continuous, the natural measure is phase-space measure, and the law is a Hamiltonian flow generated by conservative forces. A permutation rearranges exact states without merging them. A Hamiltonian flow does the same for a continuum of exact states, with phase-space measure playing the role that counting measure played before. In conservative physical systems, this behavior is known as Liouville's theorem.

### Information as an Incompressible Fluid

In the set permutation and physical ensembles example, we looked at spaces of possible arrangements. We might imagine that these spaces behave like incompressible fluids, and indeed we can see this same structure in real fluid flows. Imagine marking out a connected patch of an ideal incompressible fluid and then simply tracking that same patch as the fluid moves. The patch may be stretched into a long filament, bent, folded, or sheared almost beyond recognition. But it does not tear, it does not split, and it does not lose its area. It remains the same material patch, carried along by the flow.

In our card example, exact states were permuted. In the ensemble example, exact initial conditions were carried by a Hamiltonian flow. Here, a material patch is carried by the velocity field of the fluid. In all three cases, the same structural fact is present that the dynamics moves possibilities around without changing their identity as defined by the information they encode.

One can see the beginning of that geometry in the mathematics of ordinary incompressible flow. In two dimensions, if the velocity field is

```math
\frac{dx}{dt} = u(x,y),\qquad \frac{dy}{dt} = v(x,y),
```

then incompressibility means

```math
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0.
```

This condition says that a small material patch does not locally compress or expand. In two dimensions it has a powerful consequence. There exists a scalar function \(\psi(x,y)\) such that

```math
u = \frac{\partial \psi}{\partial y},
\qquad
v = -\frac{\partial \psi}{\partial x}.
```

\<animation\>

So incompressibility forces the motion into a crossed form. Change in one direction is generated by variation in the other. This is not yet Hamiltonian Mechanics, because we have not yet said what the relevant variables are. But it is the pattern Hamiltonian Mechanics will formalize. The geometry of incompressible flow already hints that the state of a system may come with paired directions, and that the law of motion may preserve not lengths, but oriented area.

### Information Embodied in States
We have talked about systems that preserve the structure of distributions. Let us now express this briefly in the language of information theory.

How much information does a penny showing heads contain? A good way to think about this is as a question about surprise. If a coin were weighted so that heads always appeared, seeing heads would contain no information at all. If it showed heads 90% of the time, seeing heads would confirm what I already expected, and would therefore contain only a small amount of information. But if it came up tails, it would force a revision of my expectations. That is the sense in which it would be informative. Let us call this quantity "surprisal." We want surprisal to go up as probability goes down.

We also want information to add as independent systems are combined. If I show you two independent coins that are heads, the probabilities multiply. For a 50/50 coin, the probability of seeing two heads is 0.25. But the information should add. In an 8-bit computer, it is natural to say that it holds 8 bits of information rather than to characterize it by the \(2^8\) possible bit strings it can realize. These two requirements are met by defining the information content of an outcome using a base-2 logarithm:

```math
I(H) = -\log_2 P(H),
```

When the probability of heads is 50%, this is exactly 1 bit. If the probability increases, it goes down. If it decreases, it goes up. Moreover, the information from 2 heads adds:

```math
I(HH) = -\log_2\big(P(H)P(H)\big) = -\log_2 P(H) - \log_2 P(H) = 2I(H).
```

This quantity describes the information associated with one realized outcome. When we turn from one outcome to an ensemble, the natural scalar quantity is the average surprisal over the whole distribution. That is what Shannon entropy is.

There is nothing essentially different between our coin example and an ensemble of initial conditions in a physical system. Rather than a discrete number of possibilities, there is a continuous set, so we must deal in probability densities rather than probabilities. With this change, the expression for the ensemble entropy becomes:


```math
H[\rho] = -\int \rho(x)\log_2 \rho(x)\,d\mu,
```

where \(d\mu\) is the natural measure on the space of states. In this precise sense, an ensemble is information-bearing, and the amount of information it carries is exactly quantifiable.

Liouville's theorem implies that this fine-grained entropy is preserved in ideal conservative evolution. That alone is not yet the full strength of the theorem. Different probability densities can have the same entropy while encoding different distinctions among possible states. The informational identity of an ensemble therefore lies not merely in the scalar \(H[\rho]\), but in the full fine-grained arrangement of its density \(\rho(x)\) over the state space. The key point we want to emphasize here is that the structure Hamiltonian Mechanics illuminates pertains to the embodiment and preservation of information in physical systems.

### The Importance of the Information Perspective
Liouville's theorem and the information-theoretic implications of conservative systems are at the heart of statistical mechanics, in which the exact microscopic initial conditions of the constituent bodies are never knowable precisely, both because one cannot know the exact state of any one particle in a continuous phase space and because the number of combinations of microscopic states is unfathomably large, even if one were to divide phase space into a finite number of parcels. The laws of thermodynamics, expressing how temperature, volume, pressure, and number of particles relate, would be impossible without understanding this preservation of information. But even more deeply, when we move to quantum mechanics and individual bodies give way to distributions over possible measurements, physics must be expressed as the evolution of distributions, for distributions are all there is.

## From the Lagrangian to Canonical Momentum

## Phase Space and the Hidden Geometry of State

## The Symplectic Structure

## Kinematics and Dynamics in Phase Space

## Generator Pairing

## Poisson Brackets as Algebraic Bookkeeping

## The Legendre Transformation Proper and the Hamiltonian

## The Hamiltonian as Time Generator

## Hamilton's Equations

## Why This Matters for QM and QFT
