Your instinct is essentially right: quantum probability is not needed for phase stationarity to become action stationarity. The mass shell supplies the common geometry. What it does not supply is the conversion scale between dimensionless phase and mechanically measured action.

For a classical Klein–Gordon field,

\[
(\Box+\mu^2)\phi=0,
\]

each Fourier mode satisfies

\[
k_\mu k^\mu=\mu^2.
\]

Writing the field locally as

\[
\phi=Ae^{i\theta},
\qquad
k_\mu=\partial_\mu\theta,
\]

gives the eikonal equation

\[
\partial_\mu\theta\,\partial^\mu\theta=\mu^2.
\]

Now introduce any constant \(\alpha\) having units of action:

\[
S=\alpha\theta,
\qquad
p_\mu=\alpha k_\mu,
\qquad
m=\frac{\alpha\mu}{c}.
\]

The wave mass shell immediately becomes

\[
p_\mu p^\mu=m^2c^2,
\]

and the phase equation becomes the relativistic Hamilton–Jacobi equation:

\[
\partial_\mu S\,\partial^\mu S=m^2c^2.
\]

Moreover,

\[
\delta S=\alpha\,\delta\theta,
\]

so

\[
\delta S=0
\quad\Longleftrightarrow\quad
\delta\theta=0.
\]

That equivalence requires no probability interpretation whatsoever. Classical optics already works this way: stationary optical phase produces stationary rays.

Where, then, is \(\hbar\)? The classical wave equation determines \(\mu\), an inverse-length mass parameter, but it does not determine the constant \(\alpha\) that converts wave number into mechanical momentum. Experiment supplies

\[
\alpha=\hbar,
\]

giving

\[
p_\mu=\hbar k_\mu,
\qquad
m=\frac{\hbar\mu}{c},
\qquad
S=\hbar\theta.
\]

Thus \(\hbar\) is not needed to locate the stationary path. Multiplying the entire phase by any nonzero constant leaves stationarity unchanged. It is needed to calibrate wave phase in units of mechanical action—and to determine how rapidly different actions separate in phase.

The mass does not cancel. It is hidden inside \(S\) and inside the dispersion relation. For a free mode,

\[
\theta
=
\mathbf k\cdot\mathbf x-\omega t,
\]

while

\[
S
=
\mathbf p\cdot\mathbf x-Et
=
\hbar\theta,
\]

with

\[
E^2=c^2|\mathbf p|^2+m^2c^4.
\]

Along the free worldline,

\[
\Delta S=-mc^2\Delta\tau,
\]

so

\[
\boxed{
\Delta\theta
=
-\frac{mc^2}{\hbar}\Delta\tau
}.
\]

At rest, the field therefore accumulates phase at the mass-dependent Compton frequency

\[
\omega_0=\frac{mc^2}{\hbar}.
\]

One final distinction matters. A classical KG field has a field action such as

\[
S_{\mathrm{KG}}[\phi]
=
\frac12\int d^4x
\left(
\partial_\mu\phi\,\partial^\mu\phi
-
\mu^2\phi^2
\right).
\]

Varying this produces the KG equation. That entire field functional is not what appears in the local relation \(\theta=S/\hbar\). There, \(S\) is the Hamilton–Jacobi or ray action associated with a mode or packet path.

So the clean conclusion is:

> The mass shell already makes wave-phase stationarity and mechanical-action stationarity mathematically equivalent up to a constant scale. Quantum mechanics identifies that scale as \(\hbar\) and gives the wave amplitudes their probabilistic interpretation. The stationary-path correspondence itself is older and more general than that interpretation.
