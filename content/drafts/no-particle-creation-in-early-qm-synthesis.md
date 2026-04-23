## No Particle Creation in Early Quantum Mechanics

Early quantum mechanics fixes the particle count at the start. For $N$ particles, the state is a wave function on an $N$-particle configuration space,

$$
\psi(x_1,\dots,x_N,t).
$$

The number of particles is built into the space the state lives on. Time evolution can move amplitude around inside that space, but it cannot leave it. An $N$-particle Schrödinger theory can reshuffle the state of $N$ particles. It cannot turn $N$ into $N+1$ or $N-1$.

But particle creation in nature is commonplace. An excited atom emits a photon, and an energetic collision produces new particles. Matter and radiation exchange quanta. One may model different particle compositions with different Hilbert spaces, but that is exactly the point. The theory does not contain one unified state space in which particle composition may change.

QFT will fix this by changing what a particle is. In second quantization, a particle is not a primitive object that happens to carry energy. It is one step in the discrete excitation spectrum of a field mode. Once a mode is quantized, its occupation number, how many particles are in a given momentum mode, comes in levels $n=0,1,2,\dots$, and there are operators that move up and down that ladder,

$$
\hat a^\dagger |n\rangle \propto |n+1\rangle,
\qquad
\hat a |n\rangle \propto |n-1\rangle.
$$

These ladder operators imply an extension of state space to the direct sum of all fixed-particle-number spaces, called Fock space.
