# Outline: From the Canonical Commutator to the Stationary Wave-Packet Ray

## Editorial placement

Write this material now, but place the finished argument in the action/Lagrangian section, after spacetime and basic wave/Fourier material have been established. The symmetry section should stop after showing that the canonical commutator produces a phase advance around an $x$-$k$ loop and point forward to this payoff.

This placement lets the main text use $t$ and $\omega$ openly. If the argument were placed before spacetime, it would need the more abstract construction with a second translation coordinate $s$, its Fourier label $q$, and the added relation $q=-\omega(k)$. That construction remains useful as a correctness check, but it is not the economical reader-facing route.

## Starting point and destination

The reader already knows:

- translation eigenfunctions are complex plane waves;
- plane waves superpose into localized packets;
- shifting in $x$ and shifting in $k$ fail to commute;
- the closed $x$-$k$ commutator loop returns the function to the same $x$- and $k$-distribution but advances its phase.

This outline begins immediately after that result. It ends by showing why, in the short-wavelength or ray regime, the center of a localized packet is organized by a stationary path satisfying first-order ray equations and, after eliminating $k$, an Euler--Lagrange equation.

The complete dependency chain is:

```math
\text{CCR phase structure}
+
\text{dispersion/evolution rule}
+
\text{linear wave composition}
+
\text{stationary-phase regime}
\longrightarrow
\text{ray equations}
\longrightarrow
\text{Euler--Lagrange form}.
```

The CCR does **not** by itself supply the dispersion relation, evolution, stationarity, or physical action.

## Annotation key

- **[TEXT]**: the conceptual statement the prose must establish.
- **[MATH]**: mathematics needed in the main line.
- **[MATH BOX]**: a derivation needed for completeness but suitable for a collapsible or worked aside.
- **[VISUAL]**: a diagram or animation should carry most of the explanation.
- **[GUARDRAIL]**: a claim that must be qualified to remain correct.
- **[PAYOFF]**: a result worth emphasizing.

---

## 1. Recall the closed-loop result, then distinguish it from evolution

**[TEXT]**

Recall rather than rederive the established result: an $x$-$k$ commutator loop closes in $x$ and $k$ but leaves a phase advance. Then say what it has **not** yet done. The loop is a hypothetical composition of transformations, not a history in time. It gives the canonical phase relation between conjugate translation directions, but it does not say how a packet moves.

The useful distinction is:

```math
\text{closed }x\text{-}k\text{ loop}
\longrightarrow
\text{second-order phase difference},
```

whereas the evolution argument will require

```math
\text{open displacement through space and time}
\longrightarrow
\text{first-order accumulated phase}.
```

The commutator returns later when two open candidate histories are compared: together they make a closed ribbon of local loops.

**[VISUAL]**

Briefly reuse the already-established Weyl-loop visual, followed by a simple card:

> Phase structure: obtained.  
> Evolution rule: still missing.

Do not yet reuse the existing $x$-$k$ path-variation animation. It depicts only one contribution to the later variation.

---

## 2. Add the missing ingredient: how every Fourier mode advances

**[TEXT]**

Once time translation and the space/time Fourier convention are available, supply a real dispersion relation $\omega=\omega(k)$. This is new information. Spatial translation symmetry makes a translation-compatible evolution diagonal in $k$; it does not determine the function $\omega(k)$.

**[MATH]**

For one mode,

```math
u_k(x,t)
=
e^{i[kx-\omega(k)t]}.
```

A packet is

```math
\psi(x,t)
=
\frac{1}{\sqrt{2\pi}}
\int
c(k)e^{i[kx-\omega(k)t]}
\,dk.
```

Equivalently, its Fourier coefficient evolves as

```math
\widetilde\psi(k,t+\tau)
=
e^{-i\omega(k)\tau}
\widetilde\psi(k,t).
```

**[TEXT]**

The minus sign is part of the chosen Fourier/time-orientation convention. It is not being derived here from the CCR, and it is not by itself the Lorentzian metric sign.

For an ordinary real classical wave, the complex expression may describe one frequency branch; adding its complex conjugate recovers the real field. The phase and stationary-ray reasoning can be performed on that complex branch without claiming that the physical field is intrinsically complex.

**[OPTIONAL PRE-SPACETIME VERSION]**

If this material is ever moved before the spacetime discussion, introduce two mathematically symmetric translation coordinates first:

```math
u_{k,q}(x,s)=e^{i(kx+qs)},
```

then add

```math
q=-\omega(k),
```

to obtain

```math
u_k(x,s)=e^{i[kx-\omega(k)s]}.
```

The relation $q=-\omega(k)$ selects a curve from all possible pairs $(k,q)$; it is not supplied by translation symmetry. The existing `symmetry-dispersion-subset-contours.png` can illustrate this optional route.

---

## 3. Show what phase advance looks like for a mode and for a packet

**[TEXT]**

A pure mode has no center, so its phase advance cannot yet be called a path. For one nonzero mode, temporal phase advance looks exactly like a spatial shift of its repeating pattern:

**[MATH]**

```math
e^{-i\omega(k)\tau}u_k(x)
=
u_k(x-a),
\qquad
a=\frac{\omega(k)}{k}\tau.
```

This equivalence holds mode by mode. It does not make a common global phase the same operation as translating a packet.

For a packet, a spatial translation gives every Fourier component the phase $e^{-ika}$, while evolution gives it $e^{-i\omega(k)\tau}$. The entire packet therefore translates rigidly only when $\omega(k)$ is affine over the occupied range of $k$:

```math
\omega(k)=vk+\omega_0
\quad\Longrightarrow\quad
\psi(x,t)
=
e^{-i\omega_0t}\psi(x-vt,0).
```

Nonlinear $\omega(k)$ changes the relative phases of the components and generally makes the packet spread or distort.

**[VISUAL]**

A two-act animation:

1. One plane wave: turning every complex arrow by the same amount is visually identical to sliding its crests along $x$.
2. A packet: show the same Fourier magnitudes under (a) affine phase advance, producing rigid motion, and (b) nonlinear phase advance, producing motion plus spreading.

**[GUARDRAIL]**

Do not say that phase advance always preserves packet shape. It preserves a pure mode's shape; a packet's shape depends on $\omega(k)$.

---

## 4. Establish the ray result directly from an ordinary packet

**[TEXT]**

Before introducing candidate histories, show the concrete result the variational argument must later reproduce. For a narrow packet centered near $k_0$, linearize the dispersion relation over the packet's occupied Fourier range.

**[MATH BOX]**

```math
\omega(k)
\approx
\omega(k_0)
+
\omega'(k_0)(k-k_0).
```

Substitution into the packet gives the form

```math
\psi(x,t)
\approx
e^{i[k_0x-\omega(k_0)t]}
F\!\left(x-\omega'(k_0)t\right),
```

so the packet envelope moves approximately according to

```math
\boxed{
\dot x=\omega'(k_0).
}
```

**[PAYOFF]**

This is the familiar group velocity. The later stationary-phase variation must return the same equation.

**[GUARDRAIL]**

This identifies a central ray for a narrow, sufficiently coherent packet. A broad packet, a packet that splits, or a strongly dispersive packet may not have one sharp path.

**[VISUAL]**

Show the packet and its central ray together. The envelope may widen while its center follows the ray. This prevents the ray from being mistaken for the complete wave.

---

## 5. Translate exact wave evolution from Fourier language into position language

**[TEXT]**

The next question is not yet “Which path does the wave take?” It is “How does the complete wave at one slice contribute to the complete wave at a later slice?”

In Fourier space the answer was diagonal: multiply each $k$-component by its phase. In position space the same linear operation is represented by a continuous matrix, or kernel.

Let $A=(x,t)$ be an input point and $B=(x',t+\tau)$ an output point.

**[MATH]**

```math
\psi(x',t+\tau)
=
\int
\mathcal K_\tau(x'-x)\psi(x,t)
\,dx,
```

where

```math
\boxed{
\mathcal K_\tau(x'-x)
=
\frac{1}{2\pi}
\int
e^{i[k(x'-x)-\omega(k)\tau]}
\,dk.
}
```

**[TEXT]**

The kernel tells how the old wave component at $x$ contributes to the new wave component at $x'$. Its exponent has two independently sourced parts:

```math
\underbrace{k(x'-x)}_{\text{translation/Fourier/CCR structure}}
-
\underbrace{\omega(k)\tau}_{\text{supplied evolution rule}}.
```

This is the rigorous bridge that the earlier drafts often compressed too far. The CCR supplies the canonical $k\Delta x$ phase; the dispersion relation supplies $-\omega\Delta t$.

**[MATH BOX: derivation for completeness]**

Start from

```math
\widetilde\psi(k,t+\tau)
=
e^{-i\omega(k)\tau}\widetilde\psi(k,t),
```

insert the inverse Fourier transform of $\widetilde\psi(k,t)$, and collect

```math
e^{ikx'}e^{-ikx}e^{-i\omega(k)\tau}
=
e^{i[k(x'-x)-\omega(k)\tau]}.
```

No three-example tour of kernels is needed in the main narrative.

---

## 6. Show how ordinary wave propagation becomes a sum over candidate histories

**[TEXT]**

Lead with physical waves and Huygens' construction, not matrix notation.

Start a wave at $A$ and ask for its amplitude at a later point $B$. At an intermediate time slice, the wave is spread over many positions. Every point on that intermediate wavefront contributes a complex amplitude to $B$. Choosing one such point draws one two-segment route. Inserting more intermediate wavefronts and choosing one point on each draws a polygonal candidate history.

The polygon is not a measured trajectory and not the route secretly taken by a fragment of the wave. It labels one term produced when the same linear wave evolution is repeatedly composed.

**[VISUAL: primary bridge]**

Use or convert `wave-snapshots-become-paths.html`:

1. a wave spreads from $A$ across an intermediate slice;
2. every point on that slice contributes to $B$;
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

For positions $x_0=A,x_1,\ldots,x_N=B$ and a Fourier label $k_j$ on each segment,

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
\omega(x_j,k_j)\Delta t
\right].
```

For $\omega=\omega(k)$ this comes directly from exact translation-invariant kernels. Writing $\omega(x_j,k_j)$ is the local, nonuniform extension and deliberately relaxes strict spatial translation symmetry. At the operator level it requires a discretization or ordering convention. That technical choice changes prefactors and higher-order details, not the leading stationary-ray equations derived below.

**[ESSENTIAL CLARIFICATION]**

The notation $k(t)$ used later does not mean that one pure mode's fixed Fourier label mysteriously changes with time. Every segment has been independently Fourier-decomposed and receives a label $k_j$. The continuous function $k(t)$ is the limit of the sequence

```math
k_0,k_1,k_2,\ldots.
```

The fixed endpoints are spacetime events

```math
A=(x_0,t_0),
\qquad
B=(x_N,t_N).
```

The $k_j$ are internal Fourier labels, not additional spacetime endpoint coordinates.

---

## 7. Accumulate one phase for each candidate history

**[TEXT]**

On one segment, the spatial and temporal phase factors multiply:

**[MATH]**

```math
e^{ik_j\Delta x_j}
e^{-i\omega_j\Delta t_j}
=
e^{i\Delta\phi_j},
\qquad
\Delta\phi_j
=
k_j\Delta x_j-\omega_j\Delta t_j.
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

In the continuous notation,

```math
\boxed{
\Phi[x,k]
=
\int_{t_0}^{t_1}
\left[
k\dot x-\omega(x,k)
\right]dt
=
\int_\gamma
\left[
k\,dx-\omega\,dt
\right].
}
```

The candidate history contributes a complex arrow with final angle $\Phi[x,k]$:

```math
e^{i\Phi[x,k]}.
```

**[VISUAL]**

Build the phase-dial visual described in `lm-path-to-phase-visualization.md`:

- draw the candidate only in the familiar $x$-$t$ plane;
- carry a unit-circle phase dial along it;
- label each segment with its local $k_j$;
- $\Delta x$ turns the dial by $k_j\Delta x$;
- $\Delta t$ turns it by $-\omega_j\Delta t$;
- the final dial orientation is $e^{i\Phi}$.

This avoids asking the reader to picture a three-dimensional curve in $(t,x,k)$ space.

---

## 8. Reconnect the accumulated phase to the CCR by comparing nearby histories

**[TEXT]**

The phase along one open history is not itself a commutator loop. The commutator becomes relevant when that history is compared with a nearby candidate sharing the same spacetime endpoints. Follow one forward and the other backward; their phase difference is a closed-loop quantity.

**[MATH]**

Define

```math
\alpha
=
k\,dx-\omega(x,k)\,dt,
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

For general local dispersion,

```math
\boxed{
d\alpha
=
dk\wedge dx
-
\frac{\partial\omega}{\partial x}
dx\wedge dt
-
\frac{\partial\omega}{\partial k}
dk\wedge dt.
}
```

**[TEXT: central conceptual sentence]**

The term $dk\wedge dx$ is the local phase curvature already encoded by the canonical commutator. The terms containing $dt$ come from the supplied dispersion/evolution rule. The stationary history is found by balancing the complete phase variation, not from the CCR term alone.

**[VISUAL]**

Do not use `symmetry-ccr-action-variation.mp4` unchanged as the picture of physical histories. Its axes are only $x$ and $k$, so it displays only the canonical $dk\wedge dx$ contribution.

Preferred replacement:

1. main panel: two nearby paths with fixed endpoints in the $x$-$t$ plane;
2. a narrow tiled ribbon between them;
3. a small $k$ label or color strip carried along each path;
4. inset: one local $x$-$k$ commutator cell;
5. each tile's phase difference is shown as the sum of the CCR contribution and the dispersion contribution.

The existing animation can survive as that inset if it is relabeled “the $x$-$k$ contribution to phase variation,” with all claims about being the complete action variation removed.

**[MATH PRECISION NOTE]**

The physical endpoint data fix $x$ and $t$, not necessarily $k$. For a literal closed ribbon in extended $(t,x,k)$ space, either compare the sufficient subset of variations that also agree in $k$ at the ends, or join differing $k$ endpoints by $k$-only segments. Those closing segments contribute no phase because $\alpha$ has no $dk$ term.

---

## 9. Explain why candidate histories are added and why stationarity appears

**[TEXT]**

For one fixed final spacetime point $B$, every candidate history ending at $B$ contributes one complex arrow. Its length is the magnitude of that contribution; its direction is the accumulated phase $\Phi[\gamma]$.

Place the arrows tip to tail:

- for ordinary neighboring histories, a small path change changes $\Phi$ to first order, so their arrows turn and largely cancel;
- near a stationary history, a small path change changes $\Phi$ only at second order, so neighboring arrows remain aligned longer and reinforce.

**[VISUAL]**

Use or convert `stationary-phase-path-arrows-restored.html`:

- show a one-parameter family of nearby candidate paths;
- map each candidate to one phasor;
- place the phasors tip to tail;
- show cancellation away from stationarity and an aligned cluster near stationarity;
- label the large resultant as “total amplitude at this endpoint,” not “phase of the stationary path.”

Repeat conceptually for every endpoint $B$ to reconstruct the entire later wave. For an ordinary classical wave, all those field values coexist. No endpoint is selected as a random outcome.

**[MATH]**

The reinforcing neighborhood satisfies

```math
\boxed{
\delta\Phi=0.
}
```

The full wave propagation is schematically

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

## 10. Calculate the stationary ray

**[MATH]**

Begin with

```math
\Phi[x,k]
=
\int_{t_0}^{t_1}
\left[
k\dot x-\omega(x,k)
\right]dt.
```

Vary $x(t)$ and $k(t)$ independently while fixing the spatial endpoints:

```math
\delta x(t_0)=\delta x(t_1)=0.
```

To first order,

```math
\delta\Phi
=
\int_{t_0}^{t_1}
\left[
\delta k\,\dot x
+
k\,\delta\dot x
-
\frac{\partial\omega}{\partial x}\delta x
-
\frac{\partial\omega}{\partial k}\delta k
\right]dt.
```

Integrate the $k\,\delta\dot x$ term by parts. The fixed endpoints remove the boundary term:

```math
\delta\Phi
=
\int_{t_0}^{t_1}
\left[
\left(
\dot x-
\frac{\partial\omega}{\partial k}
\right)\delta k
-
\left(
\dot k+
\frac{\partial\omega}{\partial x}
\right)\delta x
\right]dt.
```

Because $\delta x$ and $\delta k$ are independent,

```math
\boxed{
\dot x
=
\frac{\partial\omega}{\partial k},
\qquad
\dot k
=
-\frac{\partial\omega}{\partial x}.
}
```

**[TEXT]**

These are the first-order ray equations:

- the local slope of the ray is the group velocity;
- spatial change in the wave rule changes the local wave number and bends the ray.

For the strictly translation-invariant case,

```math
\omega=\omega(k),
```

so

```math
\boxed{
\dot k=0,
\qquad
\dot x=\omega'(k).
}
```

This exactly reproduces the group-velocity result previewed from the narrow packet. In the uniform case, the stationary ray has constant $k$ and constant velocity.

**[PAYOFF]**

Direct Fourier analysis of the packet and variational analysis of the candidate-history phase arrive at the same ray.

---

## 11. Recognize and recover the Euler--Lagrange form

**[TEXT]**

The first-order phase rate already has a Lagrangian form:

**[MATH]**

```math
\ell_\phi(x,k,\dot x)
=
k\dot x-\omega(x,k),
\qquad
\Phi
=
\int\ell_\phi\,dt.
```

Applying the Euler--Lagrange equations to $x$ and $k$ reproduces the two first-order ray equations above.

If

```math
\dot x
=
\frac{\partial\omega}{\partial k}
```

can be solved locally for

```math
k=k(x,\dot x),
```

eliminate $k$ and define the configuration-space phase Lagrangian

```math
L_\phi(x,\dot x)
=
k(x,\dot x)\dot x
-
\omega\!\left(x,k(x,\dot x)\right).
```

Then

```math
\boxed{
\frac{d}{dt}
\frac{\partial L_\phi}{\partial\dot x}
-
\frac{\partial L_\phi}{\partial x}
=
0.
}
```

**[GUARDRAIL]**

This Legendre step requires the relation between $\dot x$ and $k$ to be locally invertible. The first-order ray equations remain meaningful even when an ordinary configuration-space Lagrangian is singular.

---

## 12. Make the physical action identification only at the end

**[TEXT]**

Up to this point, $\Phi$ is dimensionless accumulated wave phase and $L_\phi$ is phase accumulated per unit time. Physical mechanics supplies a scale relating the wave labels to momentum and energy. Write that scale generically as $\kappa$ until quantum mechanics fixes it universally.

**[MATH]**

```math
p=\kappa k,
\qquad
H(x,p)
=
\kappa\,\omega\!\left(x,\frac{p}{\kappa}\right),
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
p\dot x-H(x,p)
\right]dt
=
\int L(x,\dot x)\,dt.
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

This also gives the precise version of the earlier “graininess” intuition: action differences comparable with $\hbar$ produce appreciable phase differences, while action differences spanning many $\hbar$ produce many phase turns and strong cancellation. It does not divide phase space into literal square grains.

**[CLOSING VISUAL]**

Show one localized packet, its finite width, and the stationary central ray. Nearby candidate rays fade by phasor cancellation, but the packet remains visibly extended and may spread.

**[CLOSING CLAIM]**

> Lagrangian extremization does not replace the wave with a tiny rigid body. It identifies the stationary ray organizing the motion of a localized wave packet when interference makes such a ray a good approximation.

---

## Compact ingredient ledger

| Ingredient | What it supplies | What it does not supply |
|---|---|---|
| Plane-wave translation representation | Fourier labels and spatial phase $k\Delta x$ | Evolution or a preferred path |
| Canonical commutator | Closed-loop phase curvature in $x$-$k$ | The dispersion relation or equations of motion |
| Dispersion relation $\omega(x,k)$ | Temporal phase $-\omega\Delta t$ and a rule of evolution | Stationarity by itself |
| Linear wave composition | A sum over intermediate contributions, reorganizable as candidate histories | A literal trajectory followed by a wave fragment |
| Stationary-phase regime | Why narrow neighborhoods of some candidates reinforce | Exact replacement of the full wave by one path |
| Variation | The local first-order ray equations | The full wave equation |
| Legendre transform | Ordinary Euler--Lagrange form when invertible | A guarantee that every dispersion admits a regular configuration-space Lagrangian |
| Phase-to-action scale | Mechanical momentum, energy, and action units | The underlying phase structure, which already existed |

## Source and discussion coverage map

| Source or discussion | Material retained here | Outline location |
|---|---|---|
| `notes/worked/symmetry-ccr.md` | Weyl loop, $[\hat X,\hat K]=iI$, phase meaning | Starting assumption and §1 |
| `notes/worked/lm-from-symmetry-to-variation.md`, §§8–10 | Second translation direction, dispersion selection, mode and packet phase | §§2–4; abstract $s,q$ route demoted to optional prelude |
| Same note, §§11–12 | Kernel and repeated composition | §§5–7; long derivation collapsed |
| Same note, §§13–14 | Complete phase one-form, local-loop comparison, variation | §§8–11 |
| `notes/worked/lm-from-symmetry-to-variaton-addendum.md` | Exact full-interval kernel, careful distinction between exact propagation and stationary approximation, EL/Legendre step | Mathematical backbone of §§5–11 |
| `notes/worked/lm-path-to-phase-visualization.md` | Phase dial carried along a candidate path | §7 visual |
| `notes/worked/lm-stationarity-as-huyghens-in-small-wavelength-limit.md` | Euler--Lagrange tests candidates; waves add them; ray is small-wavelength limit | §9 |
| `notes/worked/qm-se-derivation-from-commutator.md` | CCR/Fourier representation versus separately supplied temporal generator and dispersion | Dependency distinction in §§1–2 and deferred branch below |
| `content/outline/wavemechanics-first-presentation.md` | Wave-first thematic interpretation; particle paths are not presupposed | §§6, 9, and closing claim |
| Recent discussion: global phase versus translation | Same for one mode; different on a packet; affine versus nonlinear dispersion | §3 |
| Recent discussion: what $k(t)$ means | Sequence of local Fourier labels, not one mode changing label | §6 |
| Recent discussion: endpoints | Fixed events are $(x_0,t_0)$ and $(x_1,t_1)$; $k$ is internal | §6 and §8 precision note |
| Recent discussion: two layers of alternatives | Sum histories for one endpoint; repeat over endpoints for the whole wave | §9 |
| Recent discussion: classical observation points | Every spacetime field value coexists; no random endpoint selection | §9 |
| `wave-snapshots-become-paths.html` | Wavefront expansion into candidate-history bookkeeping | §6 visual |
| `stationary-phase-path-arrows-restored.html` | Tip-to-tail cancellation and aligned stationary neighborhood | §9 visual |
| `symmetry-ccr-action-variation.mp4` | Only the $dk\wedge dx$ part of variation | §8 inset only; must be relabeled or replaced |
| `symmetry-dispersion-subset-contours.png` | What $q=-\omega(k)$ selects | Optional pre-spacetime version in §2 |

## Visual asset disposition

| Asset | Status | Recommended use |
|---|---|---|
| `differential-weyl-order-phase.mp4` | Ready | Brief recall of the already-established CCR loop in §1 |
| `lm-huygens-transverse-interference-cascade.mp4` | Ready | Optional physical-wave anchor before the candidate-history construction in §6 |
| `wave-snapshots-become-paths.html` | Strong prototype | Convert to a manuscript animation for the principal bridge in §6 |
| `stationary-phase-path-arrows-restored.html` | Strong prototype | Convert to the tip-to-tail stationarity animation in §9 |
| `lm-one-parameter-variation-slice.mp4` | Ready | Optional mathematical check that stationarity means zero first-order response |
| `symmetry-ccr-action-variation.mp4` | Conceptually partial | Retain only as the $dk\wedge dx$ inset in §8, or replace |
| Phase dial along an $x$-$t$ candidate | Missing | New visual specified in §7 |
| Mode phase versus packet translation/spreading | Missing as a focused asset | New or adapted visual specified in §§3–4 |

## Material deliberately deferred or cut from the main line

### Full wave equation and Schrödinger-form branch

The same Fourier evolution gives

```math
i\partial_t\psi
=
\omega(-i\partial_x)\psi.
```

After $p=\hbar k$ and $H=\hbar\omega$, this becomes the general Schrödinger form. This is a separate payoff: it governs the whole wave, while the phase functional above governs the stationary ray or packet center. Keep it for the wave-equation/QM section or a collapsible cross-reference.

### Field-action variation

Varying

```math
\Phi[x,k]
```

varies a candidate ray and yields ray equations. Varying a functional of the entire field,

```math
\mathcal S[\psi,\psi^*],
```

is the separate route to the full wave equation. Do not merge these two variational problems here.

### Full two-coordinate Fourier support notation

The distributional statement

```math
\widetilde f(k,q)
\propto
c(k)\delta\!\left(q+\omega(k)\right)
```

is correct but unnecessary on the main path. The curve-selection visual carries the idea more effectively.

### Three sample kernels and operator-ordering details

The exact examples and ordering problem verify the machinery but interrupt the conceptual arc. Retain them in worked notes or a collapsible appendix.

### Heisenberg--Weyl group geometry

The lifted central direction and nonintegrable plane-field visual explain the global group structure behind the CCR. They belong with the CCR itself, not in this action/ray payoff.

---

## Three-pass audit

### Pass 1: logical dependencies

- The outline no longer asks the CCR to provide dynamics. Dispersion is introduced explicitly as new information.
- Time and the sign convention are available because the argument is placed after spacetime; the neutral $s,q$ construction is retained only as an optional fallback.
- Candidate histories arise from repeated composition of linear wave evolution, not from assuming particles or postulating paths.
- The phase functional is obtained from the accumulated segment exponents before it is varied.
- Stationarity is explained by interference only after the candidate sum exists.
- Euler--Lagrange appears only after the first-order ray equations and the Legendre elimination of $k$.

### Pass 2: mathematical completeness and claim strength

- The main line includes the mode evolution, packet, kernel, one-slice composition, segment phase, continuum functional, stationary-phase condition, full variation, ray equations, and Legendre transform.
- The exact wave sum is distinguished from the stationary-ray approximation.
- The $x$-$k$ CCR term is distinguished from the complete time-dependent curvature $d\alpha$.
- The uniform case $\omega(k)$ is separated from the generalized nonuniform case $\omega(x,k)$, which abandons strict spatial translation symmetry.
- The endpoints and the meaning of $k(t)$ are stated explicitly.
- The result is described as a ray organizing a suitable packet, not the exact trajectory of every wave.
- The physical action identification and $\hbar$ enter only after the dimensionless phase argument is complete.

### Pass 3: economy and visual clarity

- The reader-facing route uses $t$ directly and avoids the full $s,q$ detour.
- Only one kernel equation is needed in the main text; its Fourier derivation is collapsible.
- The three sample kernels, support/delta notation, Schrödinger derivation, field action, and ordering details are deferred.
- Three visuals carry the hardest conceptual transitions:
  1. phase advance of mode versus packet;
  2. physical wavefronts reorganized as candidate histories;
  3. candidate histories mapped to tip-to-tail phasors.
- A fourth, corrected ribbon visual reconnects the argument to the CCR without pretending that an $x$-$k$ diagram is itself spacetime evolution.
- The direct packet group-velocity result appears before the variational machinery, giving the reader a concrete destination and a later consistency check.

## Final one-line spine

```math
\boxed{
\text{CCR/Fourier phase}
\rightarrow
\text{dispersion-driven wave evolution}
\rightarrow
\text{candidate-history phase sum}
\rightarrow
\text{stationary-phase reinforcement}
\rightarrow
\text{ray equations}
\rightarrow
\text{Euler--Lagrange mechanics}.
}
```
