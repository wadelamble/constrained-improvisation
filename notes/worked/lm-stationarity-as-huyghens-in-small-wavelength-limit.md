# Stationarity as Huygens' Principle in the Small-Wavelength Limit

Euler--Lagrange uses candidate paths as **test variations**. It begins with a phase functional

```math
\Phi[\gamma]
```

and identifies paths satisfying

```math
\delta\Phi[\gamma]=0.
```

The neighboring paths are used only to test whether the phase is stationary. They are not added together.

Wave mechanics gives the candidate paths a different role. The propagation between two endpoints can be represented schematically as

```math
K
=
\int\mathcal D\gamma\;
e^{i\Phi[\gamma]}.
```

Every candidate path contributes a complex phase. This resembles Huygens' construction: propagation is built by adding many overlapping wave contributions rather than by selecting one trajectory in advance.

For neighboring paths whose phases change rapidly, the complex contributions point in many different directions and largely cancel. Near a stationary path,

```math
\delta\Phi[\gamma]=0,
```

the phase changes only at second order under a small deformation. Contributions from a neighborhood of that path therefore remain aligned longer and reinforce one another.

The complete sum over paths is analogous to **Huygens wave optics**. Interference and diffraction remain, so propagation has a finite fuzziness. Euler--Lagrange describes the **geometrical-optics limit** of the same construction. When the wavelength becomes small compared with the scale on which the system changes, phase varies so rapidly that cancellation removes nearly every contribution except narrow neighborhoods around stationary paths.

```math
\text{full path sum}
\quad\longleftrightarrow\quad
\text{Huygens wave propagation},
```

```math
\text{stationary-phase limit}
\quad\longleftrightarrow\quad
\text{sharp Euler--Lagrange rays}.
```

At finite wavelength, the stationary path remains surrounded by contributing nearby paths. Those residual contributions produce the wave effects that a single classical trajectory omits. In the strict small-wavelength limit, the contributing neighborhood becomes increasingly narrow and is idealized as a sharp path.

Thus the sum over paths adds something that the Euler--Lagrange calculation alone does not: it supplies a wave-mechanical reason that stationary paths emerge. Euler--Lagrange **tests** candidate paths; wave propagation **adds** them, and stationary paths survive the resulting interference in the small-wavelength limit.
