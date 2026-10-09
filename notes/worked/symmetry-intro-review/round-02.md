# Symmetry
Strike a pool ball with a cue, and the balls move in an expected way. Move the table over a few feet, and the balls move in recognizably the same way. Wait a few minutes, and the balls move in the same way. Turn the pool table a few degrees, and the balls still move the same way. Put the pool table on a train at constant velocity, and, again, the balls move in the same way. These are the manifest "symmetries" of the world we live in -- position and time translation, rotation, and velocity "boosts."

![The same pool-ball collision under position and time translations, rotation, and a velocity boost](../../../content/drafts/animations/symmetry-pool-table-poster.png)

[Open MP4: symmetry-pool-table.mp4](../../../content/drafts/animations/symmetry-pool-table.mp4)

*Symmetry transforms don't change how pool balls behave*

Our pool game illustrates what we mean by symmetries of physical behavior, but why should we start our story here? We will argue that symmetry constrains both the laws that govern physical evolution and the classification of the objects that undergo that evolution.

Perhaps the notion that the pool balls behave "in the same way" could be quantified, and such a quantification might figure into the equations that describe a system's evolution. In fact, we will see that whenever a symmetry is present there are quantifiable *invariants* that express what is left the same by the symmetry. Setting aside symmetry for a moment, there is a principle of classical mechanics that associates a quantity, called **action**, with each candidate history of a physical system. The physically valid history makes this quantity stationary -- often a minimum, but not necessarily.[^1] We might imagine this quantity would itself be an invariant of our symmetry, and in the relativistic theories we will study, it is.[^2] In ideal cases, it is minus the time measured by a clock following the object's candidate path times the object's mass times the speed of light squared.[^3] However, the classical description is not fundamental. Quantum mechanics generally predicts probabilities for possible outcomes rather than a single certain outcome. What we observe as the predictable behavior of pool balls is the regime in which those probabilities are concentrated very narrowly around the classical predictions.[^4] Quantum mechanics replaces the evolution of an "object following a path" with a new object that is something like a wave. For an isolated system with specified dynamics and a given initial pure state, this wave function does have a single physically valid "history," which can itself be obtained from a stationary-action principle. In a relativistic quantum theory, this principle can also be expressed through an action invariant under spacetime symmetry.[^5]

Symmetry not only constrains physical behavior but also the form that the "things" behaving can take. We suggested above that in quantum mechanics, the state that evolves is a "wave function." Several aspects of the way this function transforms under different symmetry actions will classify the "thing" in question, or, in the parlance of modern physics, the kind of **particle**, such as an electron or photon. (We will have to wait until later to delve into the curiosity of how a function can be associated with particles.) These transformation properties serve to specify the **mass**, **spin**, **charge** and other related quantities that together provide a particle's classification. Mass appears in the characteristic relationship between a free particle's spatial and temporal frequencies. Relativistic spacetime symmetry, including boosts, dictates the form of this relationship, while the mass value is determined empirically. Spin characterizes how the wave function's internal components transform under rotations.[^6] Charge labels how a particle's state transforms under an internal symmetry that is not manifest in our pool table example.[^7]

The term "symmetry" in this context may not at first glance seem like the same concept as, say, a triangle's symmetry, but it is precisely the same concept, as we will see. Let's then start with the humble triangle and build up the vocabulary about symmetry we need to tell the rest of our story.

[^1]: "Stationary" means that, in the case of a single object following some path, the action does not change to first order under small variations of the path with its spacetime endpoints held fixed. A minimum or maximum satisfies this condition, but a stationary history can also be neither. The stationary-action principle supplies equations of motion, not by itself a guarantee that every pair of endpoints admits exactly one solution.

[^2]: The usual Newtonian free-particle action changes under a Galilean velocity boost by a term that depends only on the endpoints. This leaves its stationary paths, and therefore its equations of motion, equivalent under the boost. Thus a variational approach can respect a symmetry without the numerical action itself being invariant. The relativistic actions used here can be written as spacetime invariants.

[^3]: For a free massive point particle, the usual action is $S=-mc^2\tau$, where **proper time**, $\tau$, is the time accumulated by a clock following the candidate path. The same expression applies to a massive test particle in a prescribed gravitational field, with proper time calculated using that spacetime's geometry. Other interactions generally require additional terms in the action.

[^4]: We are describing the probabilities predicted by quantum theory, not settling whether a particular interpretation assigns trajectories or other underlying variables. The evolution of the quantum state and the outcomes of measurements are different parts of the account. Their relationship will be discussed later.

[^5]: Here the action is a functional of the history of the quantum state itself. One such action is

    ```math
    \mathcal A[\Psi]
    =\int dt\,\langle\Psi(t)|\bigl(i\hbar\partial_t-\hat H\bigr)|\Psi(t)\rangle,
    \qquad \delta\mathcal A=0.
    ```

    Its stationarity gives the Schrödinger equation. The specified Hamiltonian and initial state determine the final state; we may hold both endpoints of that solution fixed during the variation, but cannot independently prescribe an incompatible final state. Such a variational formulation already exists in nonrelativistic quantum mechanics. In a relativistic quantum theory with a unitary representation of Poincaré symmetry, this state action is invariant under the corresponding dynamical transformations of state histories, including boosts. To make that claim precise, let $\hat H$ be the time-independent, self-adjoint time-translation generator of that representation, and let $U(g)$ act on state data at time zero. Its action on histories at fixed time is

    ```math
    W_g(t)=e^{-i\hat Ht/\hbar}U(g)e^{i\hat Ht/\hbar}.
    ```

    The identity $(i\hbar\partial_t-\hat H)W_g=W_g(i\hbar\partial_t-\hat H)$ and unitarity give $\mathcal A[W_g\Psi]=\mathcal A[\Psi]$, even before the trial history satisfies the equation of motion. This uses an already specified relativistic theory; the identity alone does not make an arbitrary Hamiltonian relativistic. In quantum field theory the state can be represented as a wave functional over spatial field configurations. The action varied here is a functional of that quantum state, distinct from the action assigned to an individual field history.

[^6]: For a spin-$\tfrac12$ state vector, a full $360^\circ$ rotation changes its sign, and a $720^\circ$ rotation restores the vector. The overall minus sign does not distinguish the physical state of an isolated system. A relative sign between rotated and unrotated branches can, however, change an interference pattern. Spin characterizes the full intrinsic rotation law, not merely the number of turns required to recover a particular vector.

[^7]: The unobservable overall phase of a quantum state is a general redundancy, shared by neutral systems too. Electric charge instead specifies how a matter field transforms under the electromagnetic $U(1)$ symmetry. A local gauge transformation changes both the matter field's phase and the electromagnetic potential while leaving observable predictions unchanged. This additional structure, and its relationship to the electromagnetic interaction, will have to wait.
