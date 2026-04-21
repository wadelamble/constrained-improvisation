## Relativity Failure in Early Quantum Mechanics

Relativity demands that influence be local. Were this not the case, spatially separate locations on the same equal-time slice could influence one another, that is, their influence could act outside their light cones. But the wave function is not, in the classical sense, a field spread through spacetime that passes influence from neighbor to neighbor. It is an amplitude over position space or other dynamical variables, in the one-particle case over position space or some other dynamical variable, and in the many-particle case over configuration space. As such, it does not move through space. It is simply given on the whole slice at once, or, equivalently, moves at infinite speed. While this structure appears to present a causal contradiction, knowing what a slippery thing the wave function is, we will specify experiments that pin down what sort of spacelike influence this quantum formalism implies.

We can see this relativistically impermissible structure directly in the Schrödinger equation,

$$
i\hbar \frac{\partial \psi}{\partial t}
=
\left(
-\frac{\hbar^2}{2m}\nabla^2 + V
\right)\psi.
$$

It is first order in time and second order in space, but in spacetime space and time stand, modulo the metric sign, on equal footing. That mismatch is already a strong clue that something is wrong. Equations of this kind belong to the broad family of diffusion equations, such as those describing heat flow, in which an amplitude spreads with exponential falloff but becomes immediately nonzero everywhere. In a relativistic setting that is impermissible, since influence should remain confined to the light cone.

From the Schrödinger equation’s solutions, we can find the dispersion relation,

$$
\omega = \frac{\hbar k^2}{2m},
$$

from which we find the group velocity,

$$
v_g = \frac{\partial \omega}{\partial k} = \frac{\hbar k}{m}.
$$

The speed of light appears nowhere in this equation, and thus the group velocity is unbound. In early quantum mechanics, barring pathological exceptions, group velocity is particle velocity, so the theory predicts that particle velocity can exceed lightspeed in an experimentally observable way. This is exactly what one should expect from a theory built for Galilean rather than Minkowskian spacetime.

We can devise an experiment to test this. Prepare a narrow free-particle wave packet with sufficiently large central wavenumber, let it propagate across a known baseline, and compare the arrival time of the packet peak to the light-travel time across the same distance. Since the group velocity in the theory is unbounded, the theory permits choosing the packet so that its peak arrives sooner than any light signal could.

One can see the same problem by starting from a localized state. Suppose that on some equal-time slice the particle is sharply confined to a small spatial region. Under Schrödinger evolution, that localization does not spread by advancing outward through neighboring points at some finite characteristic speed. It evolves according to

$$
\psi(x,t) = \int_{-\infty}^{\infty} \phi(k)\, e^{i(kx-\omega t)}\, dk,
$$

with

$$
\omega = \frac{\hbar k^2}{2m}.
$$

Since every Fourier mode is immediately present in the evolved state, the wave function acquires nonzero support arbitrarily far away after any nonzero time, however short. The tails may be tiny, but they are there at once. In a relativistic theory that matters. If a particle is localized here now, there must be regions elsewhere now that remain exactly outside causal reach. 

Here too the experiment is straightforward. Localize the particle near one detector on an equal-time slice, place a second detector far enough away that for a chosen short time window it is spacelike separated from the first, and then allow the state to evolve for that short time. Schrödinger evolution immediately assigns the distant detector a nonzero amplitude where relativity demands it be exactly zero.

