# Outline: From the Canonical Commutator to the Stationary Wave-Packet Ray, Version 2

## Editorial placement remains open

This version is deliberately portable. It does not begin by calling the second translation coordinate time or its Fourier label frequency. It begins with two mathematically ordinary translation coordinates, $x$ and $s$, with Fourier labels $k$ and $q$.

That leaves three possible placements open:

- the complete argument can remain in the symmetry chapter as a major payoff of function representations and commutators;
- the symmetry chapter can carry the construction through the selected $x$-$s$ flow and point forward to the stationary-path result;
- the entire argument can appear in the action/Lagrangian section, with only the $x$-$k$ commutator loop retained in symmetry.

Nothing in the mathematical spine below decides that editorial question. The identification $s=t$ and the physical interpretation of $\Omega$ are postponed to separate sections at the end.

## Starting point and destination

The reader already knows:

- translation eigenfunctions are complex plane waves;
- plane waves superpose into localized packets;
- shifting in $x$ and shifting in $k$ fail to commute;
- the closed $x$-$k$ commutator loop returns a function to the same $x$- and $k$-distribution while advancing its phase.

This outline begins immediately after that result. It adds a second translation coordinate $s$, selects a relation between the two Fourier labels, and follows the resulting wave flow until stationary phase produces first-order ray equations and, after eliminating $k$, an Euler--Lagrange equation.

The complete dependency chain is:

```math
\text{CCR phase structure}
+
\text{two-coordinate Fourier representation}
+
\text{imported relation }q=-\Omega(k)
+
\text{linear wave composition}
+
\text{stationary-phase regime}
\longrightarrow
\text{ray equations}
\longrightarrow
\text{Euler--Lagrange form}.
```

The CCR does **not** by itself supply the relation $q=-\Omega(k)$, a flow through $s$, stationarity, or physical action.

## Annotation key

- **[TEXT]**: the conceptual statement the prose must establish.
- **[MATH]**: mathematics needed in the main line.
- **[MATH BOX]**: a derivation needed for completeness but suitable for a collapsible or worked aside.
- **[VISUAL]**: a diagram or animation should carry most of the explanation.
- **[GUARDRAIL]**: a claim that must be qualified to remain correct.
- **[PAYOFF]**: a result worth emphasizing.

---

## 1. Recall the closed-loop result, then say what remains missing

**[TEXT]**

Recall rather than rederive the established result: an $x$-$k$ commutator loop closes in $x$ and $k$ but leaves a phase advance. The loop is a hypothetical composition of transformations, not yet a history through any evolution parameter. It gives the canonical phase relation between conjugate translation directions, but it does not say how a packet proceeds from one slice to another.

The useful distinction is:

```math
\text{closed }x\text{-}k\text{ loop}
\longrightarrow
\text{second-order phase difference},
```

whereas the construction below will require

```math
\text{open displacement through }x\text{ and }s
\longrightarrow
\text{first-order accumulated phase}.
```

The commutator returns when two open candidate histories are compared: together they make a closed ribbon of local loops.

**[VISUAL]**

Briefly reuse the already-established Weyl-loop visual, followed by a simple card:

> Phase structure: obtained.  
> A rule connecting successive slices: still missing.

Do not yet reuse the existing $x$-$k$ path-variation animation. It depicts only one contribution to the later variation.

---

## 2. Add a second translation coordinate without calling it time

**[TEXT]**

Introduce a second coordinate $s$ without assigning it a physical interpretation. Consider functions $f(x,s)$ and the joint Fourier modes of the two translation directions.

**[MATH]**

```math
u_{k,q}(x,s)
=
e^{i(kx+qs)}.
```

The two translation generators are

```math
\hat K=-i\partial_x,
\qquad
\hat Q=-i\partial_s,
```

and the modes satisfy

```math
\hat K u_{k,q}=k u_{k,q},
\qquad
\hat Q u_{k,q}=q u_{k,q}.
```

With the coordinate-multiplication operators

```math
(\hat Xf)(x,s)=xf(x,s),
\qquad
(\hat Sf)(x,s)=sf(x,s),
```

there are two symmetric canonical pairs:

```math
[\hat X,\hat K]=iI,
\qquad
[\hat S,\hat Q]=iI,
```

while the cross-commutators vanish:

```math
[\hat X,\hat S]
=
[\hat X,\hat Q]
=
[\hat K,\hat S]
=
[\hat K,\hat Q]
=0.
```

**[TEXT]**

At this stage, $x$ and $s$ are mathematically symmetric. There is a complete two-dimensional Fourier representation, but there is not yet a rule saying that one $s$-slice determines another.

**[VISUAL]**

Use a contour plot of a general two-variable wave to establish the still-symmetric situation: arbitrary Fourier weight may occupy arbitrary pairs $(k,q)$.

---

## 3. Import a relation between the Fourier labels

**[TEXT]**

Now supply a real function $\Omega(k)$ and select only the joint modes satisfying

```math
\boxed{
q=-\Omega(k).
}
```

This is additional information. Neither two-dimensional translation symmetry nor the canonical commutators determine $\Omega(k)$.

The **minus sign is also imported at this stage**. Before $s$ has been given a physical orientation, one could instead choose $q=+\Omega(k)$, reverse the direction called positive $s$, or reverse the Fourier-sign convention. We choose the minus sign so that the subsequent formulas have one consistent orientation. Its later spacetime interpretation is treated separately in §14.

Substitution gives the selected modes

```math
u_k(x,s)
=
e^{i[kx-\Omega(k)s]}.
```

A general superposition of those modes is

```math
f(x,s)
=
\frac{1}{\sqrt{2\pi}}
\int
c(k)e^{i[kx-\Omega(k)s]}
\,dk.
```

**[TEXT]**

The relation $q=-\Omega(k)$ selects a curve from the previously unrestricted $(k,q)$ plane. It says that once the $k$ label is chosen, the corresponding $q$ label is fixed. Consequently, once the coefficients $c(k)$—equivalently the complete slice $f(x,0)$—are known, every other $s$-slice is fixed.

**[MATH BOX]**

In the full two-dimensional Fourier representation, the same restriction is

```math
\widetilde f(k,q)
\propto
c(k)\delta\!\left(q+\Omega(k)\right),
```

or, more substantively,

```math
\operatorname{supp}\widetilde f
\subseteq
\left\{(k,q):q=-\Omega(k)\right\}.
```

This distributional notation is correct but need not appear in the main reader-facing route.

**[VISUAL]**

Use `symmetry-dispersion-subset-contours.png` or its source visual:

1. show the full $(k,q)$ plane of possible joint modes;
2. draw one test curve $q=-\Omega(k)$;
3. show an allowed surface assembled only from modes on that curve;
4. contrast it with a disallowed surface containing Fourier weight away from the curve.

Call this a selected Fourier slope or dependence, not yet a dispersion relation in physical spacetime.

---

## 4. Show that the selected relation creates a one-parameter flow

**[TEXT]**

Define the operator obtained by applying the real function $\Omega$ to the $x$-translation generator:

```math
\hat\Omega=\Omega(\hat K).
```

The selected relation may then be written

```math
\hat Qf=-\hat\Omega f
=
-\Omega(\hat K)f.
```

Because $hat Q=-i\partial_s$, this is equivalently

```math
\boxed{
i\frac{\partial f}{\partial s}
=
\Omega(-i\partial_x)f.
}
```

This equation should not yet be given a physical name. It simply says that the relation between the two Fourier labels has converted the formerly independent $s$-translation into a rule taking one complete $x$-slice to another.

Define

```math
U(s)=e^{-is\Omega(\hat K)}.
```

Then

```math
f(\,\cdot\,,s)=U(s)f(\,\cdot\,,0),
```

and more generally

```math
f(\,\cdot\,,s+\sigma)
=
U(\sigma)f(\,\cdot\,,s).
```

In the $k$-representation,

```math
\widetilde{U(\sigma)f}(k)
=
e^{-i\Omega(k)\sigma}\widetilde f(k).
```

If $\Omega(k)$ is real, each multiplier has magnitude one, so the flow preserves the function-space inner product.

**[GUARDRAIL]**

The word *flow* means only that $s$ orders a family of slices. Nothing here makes $s$ intrinsically temporal. The same mathematics could describe propagation through a second spatial coordinate.

---

## 5. Show what the selected phase does to a mode and to a packet

**[TEXT]**

A pure mode has no center. Increasing $s$ rotates its complex value everywhere by the common factor

```math
e^{-i\Omega(k)\sigma}.
```

For one nonzero mode, this phase advance looks exactly like translating its repeating pattern through $x$:

```math
e^{-i\Omega(k)\sigma}u_k(x)
=
u_k(x-a),
\qquad
a=\frac{\Omega(k)}{k}\sigma.
```

This equivalence holds mode by mode. It does not make a common phase rotation the same operation as translating an arbitrary packet.

For a packet, an $x$-translation multiplies each component by $e^{-ika}$, while an $s$-step multiplies it by $e^{-i\Omega(k)\sigma}$. The entire packet therefore translates rigidly only when $\Omega(k)$ is affine over the occupied range:

```math
\Omega(k)=vk+\Omega_0
\quad\Longrightarrow\quad
f(x,s)
=
e^{-i\Omega_0s}f(x-vs,0).
```

Nonlinear $\Omega(k)$ changes the relative phases of the components and generally makes the packet spread or distort as $s$ changes.

**[VISUAL]**

A two-act animation:

1. one plane wave: rotating every complex arrow by the same amount is visually identical to sliding its crests along $x$;
2. one packet: compare affine phase advance, producing rigid movement through the $x$-$s$ plot, with nonlinear phase advance, producing movement plus spreading.

**[GUARDRAIL]**

Do not say that phase advance always preserves packet shape. It preserves a pure mode's shape; a packet's shape depends on $\Omega(k)$.

---

## 6. Establish the central-slope result directly from a narrow packet

**[TEXT]**

Before introducing candidate histories, show the concrete result the variational argument must later reproduce. For a narrow packet centered near $k_0$, linearize $\Omega(k)$ over the occupied Fourier range.

**[MATH BOX]**

```math
\Omega(k)
\approx
\Omega(k_0)
+
\Omega'(k_0)(k-k_0).
```

Substitution into the packet gives

```math
f(x,s)
\approx
e^{i[k_0x-\Omega(k_0)s]}
F\!\left(x-\Omega'(k_0)s\right),
```

so the packet envelope is organized approximately by

```math
\boxed{
\frac{dx}{ds}=\Omega'(k_0).
}
```

**[PAYOFF]**

For now this is the slope of the packet's central ray in the $x$-$s$ plane. If $s$ is later identified with time, it becomes the group velocity. The stationary-phase variation must return the same equation without requiring that interpretation in advance.

**[GUARDRAIL]**

This identifies a central ray for a narrow, sufficiently coherent packet. A broad packet, a splitting packet, or a strongly dispersive packet may not have one sharp ray.

---

## 7. Translate the exact slice-to-slice flow from Fourier language into position language

**[TEXT]**

The next question is not yet “Which path does the wave take?” It is “How does the complete wave on one $s$-slice contribute to the complete wave on another?”

In Fourier space, the answer is diagonal: multiply each $k$-component by its phase. In the $x$-representation, the same linear operation is represented by a continuous matrix, or kernel.

Let the two slices be separated by

```math
\sigma=s_1-s_0.
```

Let $x$ label an input point on the first slice and $x'$ an output point on the second.

**[MATH]**

```math
f(x',s_1)
=
\int
\mathcal K_\sigma(x'-x)f(x,s_0)
\,dx,
```

where

```math
\boxed{
\mathcal K_\sigma(x'-x)
=
\frac{1}{2\pi}
\int
e^{i[k(x'-x)-\Omega(k)\sigma]}
\,dk.
}
```

**[TEXT]**

The kernel tells how the old function value at $x$ contributes to the new value at $x'$. Its exponent has two independently sourced parts:

```math
\underbrace{k(x'-x)}_{\text{translation/Fourier/CCR structure}}
-
\underbrace{\Omega(k)\sigma}_{\text{imported relation between Fourier labels}}.
```

This is the bridge that earlier drafts compressed too far. The CCR supplies the canonical $k\Delta x$ phase. The selected curve $q=-\Omega(k)$ supplies the second-coordinate phase.

**[MATH BOX: derivation for completeness]**

Start from

```math
\widetilde f(k,s_1)
=
e^{-i\Omega(k)\sigma}\widetilde f(k,s_0),
```

insert the inverse Fourier transform of $\widetilde f(k,s_0)$, and collect

```math
e^{ikx'}e^{-ikx}e^{-i\Omega(k)\sigma}
=
e^{i[k(x'-x)-\Omega(k)\sigma]}.
```

The full-interval kernel is the reader-facing starting point. Dividing the interval into smaller pieces will enter only when composition is used to expose the candidate-history bookkeeping.

---

## 8. Show how linear wave propagation becomes a sum over candidate histories

**[TEXT]**

Lead with physical waves and Huygens' construction, but keep the coordinate label $s$.

Start a wave on one slice and ask for its amplitude at a later $s$-slice. On an intermediate slice, the wave is spread over many $x$ values. Every point on that intermediate wave contributes a complex amplitude to the final point. Choosing one such point draws one two-segment route. Inserting more intermediate slices and choosing one point on each draws a polygonal candidate history.

The polygon is not a measured trajectory and not the route secretly taken by a fragment of the wave. It labels one term produced when the same linear wave flow is repeatedly composed.

**[VISUAL: primary bridge]**

Use or convert `wave-snapshots-become-paths.html`:

1. a wave spreads from the first endpoint across an intermediate $s$-slice;
2. every point on that slice contributes to the final endpoint;
3. highlight one point and the corresponding two-segment term;
4. add slices, selecting one point on each;
5. keep the wave visible while the highlighted polygon appears over it.

On-screen labels:

> Along one sequence: multiply propagation factors.  
> Across different sequences: add complex contributions.

and

> One term in the expansion—not a measured trajectory.

**[MATH: one exact foothold]**

One intermediate slice gives

```math
\mathcal K(B,A)
=
\int
\mathcal K(B,x_1)\mathcal K(x_1,A)
\,dx_1.
```

This is continuous matrix multiplication, but the wavefront visual should explain it before that phrase appears.

**[MATH BOX: many-slice form]**

For $x_0=A,x_1,\ldots,x_N=B$ and a Fourier label $k_j$ on each segment,

```math
\mathcal K(B,A)
=
\int
\left[\prod_{j=1}^{N-1}dx_j\right]
\left[\prod_{j=0}^{N-1}\frac{dk_j}{2\pi}\right]
e^{i\Phi_N},
```

with

```math
\Phi_N
=
\sum_{j=0}^{N-1}
\left[
k_j(x_{j+1}-x_j)
-
\Omega(x_j,k_j)\Delta s
\right].
```

For $\Omega=\Omega(k)$ this follows from exact translation-invariant kernels. Writing $\Omega(x_j,k_j)$ is the local, nonuniform extension and deliberately relaxes strict $x$-translation symmetry. At the operator level it requires a discretization or ordering convention. That technical choice changes prefactors and higher-order details, not the leading stationary-ray equations derived below.

**[ESSENTIAL CLARIFICATION]**

The notation $k(s)$ used later does not mean that one pure mode's fixed label changes mysteriously. Each segment has been independently Fourier-decomposed and receives a label $k_j$. The continuous function $k(s)$ is the limit of the sequence

```math
k_0,k_1,k_2,\ldots.
```

The fixed endpoints are points in the two-coordinate base space:

```math
A=(x_0,s_0),
\qquad
B=(x_N,s_N).
```

The $k_j$ are internal Fourier labels, not additional endpoint coordinates.

---

## 9. Accumulate one phase for each candidate history

**[TEXT]**

On one segment, the two translation phases multiply:

**[MATH]**

```math
e^{ik_j\Delta x_j}
e^{-i\Omega_j\Delta s_j}
=
e^{i\Delta\phi_j},
\qquad
\Delta\phi_j
=
k_j\Delta x_j-\Omega_j\Delta s_j.
```

Along one candidate sequence, the segment factors multiply, so their phase angles add:

```math
\prod_j e^{i\Delta\phi_j}
=
e^{i\sum_j\Delta\phi_j}.
```

Define

```math
\Phi_N
=
\sum_j\Delta\phi_j.
```

In continuous notation,

```math
\boxed{
\Phi[x,k]
=
\int_{s_0}^{s_1}
\left[
k\frac{dx}{ds}-\Omega(x,k)
\right]ds
=
\int_\gamma
\left[
k\,dx-\Omega\,ds
\right].
}
```

The candidate history contributes one complex arrow with final angle $\Phi[x,k]$:

```math
e^{i\Phi[x,k]}.
```

**[VISUAL]**

Build the phase-dial visual described in `lm-path-to-phase-visualization.md`, replacing $t$ with the still-agnostic $s$:

- draw the candidate in the $x$-$s$ plane;
- carry a unit-circle phase dial along it;
- label each segment with its local $k_j$;
- $Delta x$ turns the dial by $k_j\Delta x$;
- $Delta s$ turns it by $-\Omega_j\Delta s$;
- the final dial orientation is $e^{i\Phi}$.

This avoids asking the reader to picture a three-dimensional curve in $(s,x,k)$ space.

---

## 10. Reconnect the accumulated phase to the CCR by comparing nearby histories

**[TEXT]**

The phase along one open history is not itself a commutator loop. The commutator becomes relevant when that history is compared with a nearby candidate sharing the same endpoints. Follow one forward and the other backward; their phase difference is a closed-loop quantity.

**[MATH]**

Define

```math
\alpha
=
k\,dx-\Omega(x,k)\,ds,
\qquad
\Phi[\gamma]
=
\int_\gamma\alpha.
```

Then

```math
\Phi[\gamma']-\Phi[\gamma]
=
\oint\alpha.
```

If the two candidates bound a ribbon $R$,

```math
\boxed{
\Phi[\gamma']-\Phi[\gamma]
=
\iint_R d\alpha.
}
```

For general local $\Omega(x,k)$,

```math
\boxed{
d\alpha
=
dk\wedge dx
-
\frac{\partial\Omega}{\partial x}
dx\wedge ds
-
\frac{\partial\Omega}{\partial k}
dk\wedge ds.
}
```

**[TEXT: central conceptual sentence]**

The term $dk\wedge dx$ is the local phase curvature already encoded by the canonical commutator. The terms containing $ds$ come from the imported relation between the two Fourier labels. The stationary history is found by balancing the complete phase variation, not from the CCR term alone.

The same statement is especially transparent before the constraint is imposed. The unconstrained phase one-form is

```math
\theta=k\,dx+q\,ds,
```

with

```math
d\theta=dk\wedge dx+dq\wedge ds.
```

Restricting to $q=-\Omega(k)$ gives

```math
\theta
\longrightarrow
\alpha=k\,dx-\Omega(k)\,ds,
```

and

```math
d\theta
\longrightarrow
d\alpha=dk\wedge dx-d\Omega\wedge ds.
```

The two initially symmetric canonical planes have been tied together by the selected curve in $(k,q)$ space.

**[VISUAL]**

Do not use `symmetry-ccr-action-variation.mp4` unchanged as the picture of the complete variation. Its axes are only $x$ and $k$, so it displays only the canonical $dk\wedge dx$ contribution.

Preferred replacement:

1. main panel: two nearby paths with fixed endpoints in the $x$-$s$ plane;
2. a narrow tiled ribbon between them;
3. a small $k$ label or color strip carried along each path;
4. inset: one local $x$-$k$ commutator cell;
5. each tile's phase difference shown as the sum of the canonical contribution and the selected-flow contribution.

The existing animation can survive as that inset if relabeled “the $x$-$k$ contribution to phase variation.”

**[MATH PRECISION NOTE]**

The endpoint data fix $x$ and $s$, not necessarily $k$. For a literal closed ribbon in extended $(s,x,k)$ space, either compare the sufficient subset of variations that agree in $k$ at the ends or join differing $k$ endpoints by $k$-only segments. Those closing segments contribute no phase because $\alpha$ has no $dk$ term.

---

## 11. Explain why candidate histories are added and why stationarity appears

**[TEXT]**

For one fixed final point $B=(x_1,s_1)$, every candidate history ending at $B$ contributes one complex arrow. Its length is the magnitude of that contribution; its direction is the accumulated phase $\Phi[\gamma]$.

Place the arrows tip to tail:

- for ordinary neighboring histories, a small path change changes $\Phi$ to first order, so their arrows turn and largely cancel;
- near a stationary history, a small path change changes $\Phi$ only at second order, so neighboring arrows remain aligned longer and reinforce.

**[VISUAL]**

Use or convert `stationary-phase-path-arrows-restored.html`:

- show a one-parameter family of nearby candidate paths;
- map each candidate to one phasor;
- place the phasors tip to tail;
- show cancellation away from stationarity and an aligned cluster near stationarity;
- label the large resultant “total amplitude at this endpoint,” not “phase of the stationary path.”

Repeat conceptually for every endpoint on the final $s$-slice to reconstruct the complete later wave. For an ordinary classical wave, all those field values coexist. No endpoint is selected as a random outcome.

**[MATH]**

The reinforcing neighborhood satisfies

```math
\boxed{
\delta\Phi=0.
}
```

The complete wave propagation is schematically

```math
\mathcal K(B,A)
\sim
\int_{\gamma:A\to B}
\mathcal A[\gamma]
e^{i\Phi[\gamma]}.
```

The factor $\mathcal A[\gamma]$ reminds the reader that equal-length phasors are an explanatory idealization; candidate contributions need not all have equal magnitude.

**[GUARDRAIL]**

The full sum is the exact wave description. Replacing it by stationary rays is an approximation requiring accumulated phases to run through many cycles across neighboring candidates—the short-wavelength, geometrical-optics, WKB, or semiclassical regime. There can be more than one stationary ray, and a finite neighborhood contributes around each one.

**[THEMATIC SENTENCE]**

> Euler--Lagrange tests neighboring paths; wave propagation adds their complex contributions. In the short-wavelength limit, the paths that pass the Euler--Lagrange test are precisely the neighborhoods that survive the addition.

---

## 12. Calculate the stationary ray without identifying $s$ as time

**[MATH]**

Begin with

```math
\Phi[x,k]
=
\int_{s_0}^{s_1}
\left[
k\frac{dx}{ds}-\Omega(x,k)
\right]ds.
```

Vary $x(s)$ and $k(s)$ independently while fixing the $x$-endpoints:

```math
\delta x(s_0)=\delta x(s_1)=0.
```

To first order,

```math
\delta\Phi
=
\int_{s_0}^{s_1}
\left[
\delta k\frac{dx}{ds}
+
k\frac{d(\delta x)}{ds}
-
\frac{\partial\Omega}{\partial x}\delta x
-
\frac{\partial\Omega}{\partial k}\delta k
\right]ds.
```

Integrating the $k\,d(\delta x)/ds$ term by parts and using the fixed endpoints gives

```math
\delta\Phi
=
\int_{s_0}^{s_1}
\left[
\left(
\frac{dx}{ds}
-
\frac{\partial\Omega}{\partial k}
\right)\delta k
-
\left(
\frac{dk}{ds}
+
\frac{\partial\Omega}{\partial x}
\right)\delta x
\right]ds.
```

Because $\delta x$ and $\delta k$ are independent,

```math
\boxed{
\frac{dx}{ds}
=
\frac{\partial\Omega}{\partial k},
\qquad
\frac{dk}{ds}
=
-\frac{\partial\Omega}{\partial x}.
}
```

**[TEXT]**

These are the first-order ray equations in the $x$-$s$ plane:

- the local slope of the ray is set by how $\Omega$ changes with $k$;
- local $x$-dependence in the selected rule changes $k$ and bends the ray.

For the strictly $x$-translation-invariant case,

```math
\Omega=\Omega(k),
```

so

```math
\boxed{
\frac{dk}{ds}=0,
\qquad
\frac{dx}{ds}=\Omega'(k).
}
```

This reproduces the central-slope result obtained directly from the narrow packet. No temporal interpretation was needed.

**[PAYOFF]**

Direct Fourier analysis of the packet and variational analysis of the candidate-history phase arrive at the same ray.

---

## 13. Recognize the Euler--Lagrange form

**[TEXT]**

The first-order phase rate already has a Lagrangian form:

**[MATH]**

```math
\ell_\phi
\left(x,k,\frac{dx}{ds}\right)
=
k\frac{dx}{ds}-\Omega(x,k),
\qquad
\Phi
=
\int\ell_\phi\,ds.
```

Applying the Euler--Lagrange equations to $x$ and $k$ reproduces the two first-order ray equations above.

If

```math
\frac{dx}{ds}
=
\frac{\partial\Omega}{\partial k}
```

can be solved locally for

```math
k=k\!\left(x,\frac{dx}{ds}\right),
```

eliminate $k$ and define

```math
L_\phi
\left(x,\frac{dx}{ds}\right)
=
k\frac{dx}{ds}
-
\Omega(x,k),
```

where the solved expression for $k$ is understood on the right. Then

```math
\boxed{
\frac{d}{ds}
\frac{\partial L_\phi}{\partial(dx/ds)}
-
\frac{\partial L_\phi}{\partial x}
=0.
}
```

**[GUARDRAIL]**

This Legendre step requires the relation between $dx/ds$ and $k$ to be locally invertible. The first-order ray equations remain meaningful even when an ordinary one-coordinate Lagrangian is singular.

**[TEXT]**

At this point the mathematical result is complete. A two-translation wave representation, supplemented by a selected relation between its Fourier labels, has produced a phase functional whose stationary histories obey Euler--Lagrange equations. Nothing in that result has yet said that $s$ is time, $\Omega$ is frequency, or $\Phi$ is physical action.

---

## 14. Separate later argument: what Lorentz symmetry says about the sign

**[TEXT]**

At the abstract two-translation stage, the sign in

```math
q=-\Omega(k)
```

was conventional. Once the second coordinate is identified as time, Lorentz symmetry supplies a deeper reason that the temporal and spatial contributions to invariant phase carry opposite signs.

In one spatial dimension, take

```math
x^\mu=(ct,x),
\qquad
k^\mu=\left(\frac{\omega}{c},k\right),
```

and the metric convention

```math
\eta_{\mu\nu}
=
\operatorname{diag}(+1,-1).
```

The Lorentz-invariant pairing is

```math
k_\mu x^\mu
=
\omega t-kx.
```

Using the Fourier convention $e^{-ik_\mu x^\mu}$ gives

```math
\boxed{
e^{-ik_\mu x^\mu}
=
e^{i(kx-\omega t)}.
}
```

Under a Lorentz transformation,

```math
x'^\mu=\Lambda^\mu{}_{\nu}x^\nu,
\qquad
k'^\mu=\Lambda^\mu{}_{\nu}k^\nu,
```

and therefore

```math
k'x'-\omega't'
=
kx-\omega t.
```

**[TEXT: precise conclusion]**

Lorentz symmetry explains the **opposite-sign spacetime structure**: boosts mix $\omega$ with $k$ while preserving the combined phase. It does not uniquely decree that the printed expression must be $kx-\omega t$ rather than its negative. Reversing the Fourier convention, reversing the metric signature, or taking the complex conjugate changes the printed signs without changing the Lorentzian content. A time orientation and the convention that $\omega>0$ denotes the positive-frequency branch finish the choice.

Thus the earlier imported minus sign is not retroactively derived as the only legal notation. Rather, after $s=t$ it becomes the convention naturally matching the Lorentz-invariant phase pairing.

**[GUARDRAIL]**

Do not say that Lorentz symmetry is required merely to write a wave as $e^{i(kx-\omega t)}$; the same Fourier convention is used for nonrelativistic waves. The specifically Lorentzian claim is that the combined spacetime phase is invariant under boosts because its temporal and spatial labels transform together as a covector.

---

## 15. Make the physical action identification only after spacetime

**[TEXT]**

After identifying

```math
s=t,
\qquad
\Omega=\omega,
```

the dimensionless phase functional becomes

```math
\Phi[x,k]
=
\int
\left[
k\frac{dx}{dt}-\omega(x,k)
\right]dt.
```

Physical mechanics supplies a scale $\kappa$ relating the Fourier labels to momentum and energy:

```math
p=\kappa k,
\qquad
H=\kappa\omega,
\qquad
S=\kappa\Phi.
```

Then

```math
\boxed{
S
=
\int
\left[
p\frac{dx}{dt}-H(x,p)
\right]dt
=
\int L\,dt.
}
```

Because multiplication by a nonzero constant does not change stationarity,

```math
\boxed{
\delta\Phi=0
\quad\Longleftrightarrow\quad
\delta S=0.
}
```

Quantum mechanics later identifies

```math
\kappa=\hbar,
\qquad
e^{i\Phi}=e^{iS/\hbar}.
```

This gives the precise version of the earlier “graininess” intuition: action differences comparable with $\hbar$ produce appreciable phase differences, while differences spanning many $\hbar$ produce many phase turns and strong cancellation. It does not divide phase space into literal square grains.

**[CLOSING CLAIM]**

> Lagrangian extremization does not replace the wave with a tiny rigid body. It identifies the stationary ray organizing the motion of a localized wave packet when interference makes such a ray a good approximation.

---

## Compact ingredient ledger

| Ingredient | What it supplies | What it does not supply |
|---|---|---|
| Plane-wave translation representation | Fourier labels and the phase of displacement | A relation between the two labels |
| Canonical commutator | Closed-loop phase curvature in each conjugate coordinate-label plane | The selected curve $q=-\Omega(k)$ |
| Second translation coordinate $s$ | A second, initially symmetric Fourier pair $(s,q)$ | An interpretation as time or evolution |
| Relation $q=-\Omega(k)$ | A one-parameter slice-to-slice flow and the phase $k\Delta x-\Omega\Delta s$ | Its own physical origin |
| Linear wave composition | A sum over intermediate contributions, reorganizable as candidate histories | A literal trajectory followed by a wave fragment |
| Stationary-phase regime | Why narrow neighborhoods of some candidates reinforce | Exact replacement of the full wave by one path |
| Variation | The local first-order ray equations | The complete wave equation |
| Legendre transform | Ordinary Euler--Lagrange form when invertible | A guarantee that every $\Omega$ admits a regular one-coordinate Lagrangian |
| Lorentz symmetry after $s=t$ | The invariant pairing with opposite temporal and spatial signs | A unique overall Fourier-sign convention |
| Phase-to-action scale | Mechanical momentum, energy, and action units | The phase structure, which already existed |

## Source and discussion coverage map

| Source or discussion | Material retained here | Outline location |
|---|---|---|
| `notes/worked/symmetry-ccr.md` | Weyl loop, $[\hat X,\hat K]=iI$, phase meaning | Starting assumption and §1 |
| `notes/worked/lm-from-symmetry-to-variation.md`, §§8–9 | Symmetric $x,s$ translations, $k,q$ labels, curve selection | §§2–4 |
| Same note, §10 | Open phase accumulation versus closed-loop phase | §§5 and 9–10 |
| Same note, §§11–12 | Exact kernel and repeated composition | §§7–9 |
| Same note, §§13–14 | Complete phase one-form, local-loop comparison, variation | §§10–13 |
| `notes/worked/lm-from-symmetry-to-variaton-addendum.md` | Full-interval kernel, distinction between exact propagation and stationary approximation, Euler--Lagrange/Legendre step | Mathematical backbone of §§7–13 |
| `notes/worked/lm-path-to-phase-visualization.md` | Phase dial carried along a candidate path | §9 visual |
| `notes/worked/lm-stationarity-as-huyghens-in-small-wavelength-limit.md` | Euler--Lagrange tests candidates; waves add them; ray is the short-wavelength limit | §11 |
| `notes/worked/qm-se-derivation-from-commutator.md` | CCR/Fourier representation versus separately supplied relation between generators | Dependency distinction in §§1–4 |
| `content/outline/wavemechanics-first-presentation.md` | Wave-first interpretation; particle paths are not presupposed | §§8, 11, and closing claim |
| Recent discussion: why $q=-\Omega(k)$ makes $s$ a parameter | One $k$ fixes one $q$; one full slice fixes the family | §§3–4 |
| Recent discussion: global phase versus translation | Same for one mode; different on a packet; affine versus nonlinear $\Omega$ | §5 |
| Recent discussion: what $k(s)$ means | Sequence of segmentwise Fourier labels, not one mode changing label | §8 |
| Recent discussion: endpoints | Fixed points are $(x_0,s_0)$ and $(x_1,s_1)$; $k$ is internal | §§8 and 10 |
| Recent discussion: two layers of alternatives | Sum histories for one endpoint; repeat over final endpoints for the whole wave | §11 |
| Recent discussion: sign choice | Arbitrary in the agnostic construction; Lorentz-covariant interpretation supplied later | §§3 and 14 |
| `wave-snapshots-become-paths.html` | Wavefront expansion into candidate-history bookkeeping | §8 visual |
| `stationary-phase-path-arrows-restored.html` | Tip-to-tail cancellation and aligned stationary neighborhood | §11 visual |
| `symmetry-ccr-action-variation.mp4` | Only the $dk\wedge dx$ part of variation | §10 inset only; must be relabeled or replaced |
| `symmetry-dispersion-subset-contours.png` | What $q=-\Omega(k)$ selects | §3 |

## Material deliberately deferred or cut from the main line

### Physical naming before the Lorentz section

Do not call $s$ time, $q$ negative frequency, $\Omega$ energy, or $dx/ds$ velocity in §§1–13. Those names are interpretations added in §§14–15, not prerequisites for the mathematics.

### Full wave equation and Schrödinger-form branch

The selected relation already implies

```math
i\partial_s f
=
\Omega(-i\partial_x)f.
```

After $s=t$, $p=\hbar k$, and $H=\hbar\omega$, this becomes the general Schrödinger form. This is a separate payoff: it governs the complete wave, while the phase functional above governs a stationary ray or packet center. Keep it for the wave-equation/QM section or a collapsible cross-reference.

### Field-action variation

Varying

```math
\Phi[x,k]
```

varies a candidate ray and yields ray equations. Varying a functional of the entire field,

```math
\mathcal S[f,f^*],
```

is the separate route to the complete wave equation. Do not merge these two variational problems here.

### Full two-coordinate Fourier support notation

The delta-function expression for $\widetilde f(k,q)$ verifies the selected spectral subset but is unnecessary if the curve-selection visual carries the idea.

### Three sample kernels and operator-ordering details

The exact examples and ordering problem verify the machinery but interrupt the conceptual arc. Retain them in worked notes or a collapsible appendix.

### Heisenberg--Weyl group geometry

The lifted central direction and nonintegrable plane-field visual explain the global group structure behind the CCR. They belong with the CCR itself, not in this stationary-ray payoff.

---

## Three-pass audit

### Pass 1: logical dependencies

- The outline no longer introduces time or frequency before it needs them.
- The second coordinate $s$ and Fourier label $q$ enter symmetrically with $x$ and $k$.
- The curve $q=-\Omega(k)$ is explicitly imported as new information, including its provisional sign.
- Candidate histories arise from repeated composition of linear wave flow, not from assuming particles or postulating paths.
- The phase functional is obtained from accumulated segment exponents before it is varied.
- Stationarity is explained by interference only after the candidate sum exists.
- Euler--Lagrange appears only after the first-order ray equations and the elimination of $k$.
- Lorentz symmetry and physical action enter only after the agnostic derivation is complete.

### Pass 2: mathematical completeness and claim strength

- The main line includes joint modes, the spectral constraint, one-parameter flow, packet, exact kernel, one-slice composition, segment phase, continuum functional, stationary-phase condition, full variation, ray equations, and Legendre transform.
- The exact wave sum is distinguished from the stationary-ray approximation.
- The $x$-$k$ CCR term is distinguished from the complete $s$-dependent curvature $d\alpha$.
- The uniform case $\Omega(k)$ is separated from the generalized nonuniform case $\Omega(x,k)$, which abandons strict $x$-translation symmetry.
- The endpoints and the meaning of $k(s)$ are stated explicitly.
- The Lorentz discussion claims only that the spacetime phase has an invariant opposite-sign structure, not that Lorentz symmetry uniquely chooses one printed exponential convention.
- The physical action identification and $\hbar$ enter only after dimensionless phase stationarity is complete.

### Pass 3: economy and visual clarity

- The hard abstraction is concentrated in one move: selecting the curve $q=-\Omega(k)$ from the joint Fourier plane.
- Only one kernel equation is needed in the main text; its Fourier derivation is collapsible.
- The support/delta notation, sample kernels, full wave-equation branch, field action, and ordering details are deferred.
- Four visuals carry the hardest transitions:
  1. selecting a curve in the $(k,q)$ plane;
  2. phase advance of a mode versus a packet;
  3. wavefront composition reorganized as candidate histories;
  4. candidate histories mapped to tip-to-tail phasors.
- A corrected ribbon visual reconnects the stationary variation to the CCR without pretending that an $x$-$k$ diagram is itself an $x$-$s$ history.
- The direct packet-slope result appears before the variational machinery, giving the reader a concrete destination and a later consistency check.

## Final one-line spine

```math
\boxed{
\text{CCR/Fourier phase}
\rightarrow
\text{second translation pair}
\rightarrow
q=-\Omega(k)
\rightarrow
\text{slice-to-slice wave flow}
\rightarrow
\text{candidate-history phase sum}
\rightarrow
\text{stationary-phase reinforcement}
\rightarrow
\text{ray equations}
\rightarrow
\text{Euler--Lagrange form}.
}
```
