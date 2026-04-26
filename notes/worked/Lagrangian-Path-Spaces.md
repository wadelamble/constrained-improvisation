There are really three spaces in play, and the consistency gap comes from sliding between them.

1. `Path space`
The action is a functional on the space of all possible curves. Extremizing happens here.

2. `Configuration space`
The resulting curve usually lives here: `q^i(t)`. For an `N`-particle system, this is the `3N`-dimensional space of positions.

3. `Spacetime`
Only in special cases, like a free relativistic particle, is the extremal curve literally a spacetime geodesic.

So the clean answer is:

- action extremization always picks out an extremal curve in `path space`
- that curve is often interpretable as a geodesic in some underlying space
- but `which space` depends on the form of the action

The main cases are:

- `free relativistic particle`
Geodesic in spacetime, with metric `g_{\mu\nu}`.

- `ordinary L = T - V mechanics`
Not directly a geodesic of physical space.
At fixed energy, the trajectory can be recast as a geodesic in `configuration space` with the `Jacobi metric`
\[
J_{ij}(q)=2(E-V(q))\,m_{ij}(q).
\]

- `more general Lagrangians`
Often not Riemannian geodesics at all, but geodesics of a more general metric-like structure, often `Finsler`.

So if you want the manuscript-safe version:

- `LM does not in general say trajectories are geodesics of ordinary space.`
- `More carefully, LM selects extremal paths, and for standard conservative systems these can be reinterpreted as geodesics of a metric on configuration space.`
