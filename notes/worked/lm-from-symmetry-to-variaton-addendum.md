# From the Exact Kernel to Variation

Let $\omega(k)$ be real. This addendum begins with the selected Fourier modes

```math
u_k(x,s)
=
e^{i[kx-\omega(k)s]}
```

and the exact Fourier-space evolution rule

```math
\widetilde f(k,s_1)
=
e^{-i\omega(k)(s_1-s_0)}
\widetilde f(k,s_0).
```

Write

```math
\sigma=s_1-s_0.
```

Nothing below requires $\sigma$ to be small.

The Fourier integrals below may be ordinary integrals or oscillatory integrals understood as generalized functions. The delta functions in the first two examples are instances of the latter.

## 1. The exact full-interval kernel

Let

```math
f_0(x)=f(x,s_0),
\qquad
f_1(x')=f(x',s_1).
```

In Fourier space, evolution through the full interval $\sigma$ is simply

```math
\widetilde f_1(k)
=
e^{-i\omega(k)\sigma}\widetilde f_0(k).
```

Transforming back to the $x$-representation gives

```math
f_1(x')
=
\frac{1}{\sqrt{2\pi}}
\int
e^{ikx'}e^{-i\omega(k)\sigma}
\widetilde f_0(k)
\,dk.
```

Now substitute

```math
\widetilde f_0(k)
=
\frac{1}{\sqrt{2\pi}}
\int
e^{-ikx}f_0(x)
\,dx.
```

Then

```math
\begin{aligned}
f_1(x')
&=
\frac{1}{2\pi}
\int dk\int dx\;
e^{ikx'}e^{-i\omega(k)\sigma}e^{-ikx}f_0(x)
\\
&=
\int dx
\left[
\frac{1}{2\pi}
\int dk\;
e^{i[k(x'-x)-\omega(k)\sigma]}
\right]
f_0(x).
\end{aligned}
```

Therefore

```math
\boxed{
f_1(x')
=
\int
\mathcal K_\sigma(x'-x)f_0(x)
\,dx
}
```

with the exact full-interval kernel

```math
\boxed{
\mathcal K_\sigma(x'-x)
=
\frac{1}{2\pi}
\int
e^{i[k(x'-x)-\omega(k)\sigma]}
\,dk.
}
```

The kernel is the continuous analogue of a matrix. The kernel $\mathcal K_\sigma(x'-x)$ tells how the old value at $x$ contributes to the new value at $x'$ after the entire interval $\sigma$.

The kernel is not an additional law. It is the Fourier-space multiplier

```math
e^{-i\omega(k)\sigma}
```

rewritten in the $x$-representation.

## 2. Three exact kernels

If

```math
\omega(k)=\omega_0,
```

then

```math
\mathcal K_\sigma(x'-x)
=
e^{-i\omega_0\sigma}\delta(x'-x).
```

Therefore

```math
f_1(x')
=
e^{-i\omega_0\sigma}f_0(x').
```

The function remains at the same $x$ and acquires only a common phase.

If

```math
\omega(k)=vk,
```

then

```math
\begin{aligned}
\mathcal K_\sigma(x'-x)
&=
\frac{1}{2\pi}
\int
e^{ik[(x'-x)-v\sigma]}
\,dk
\\
&=
\delta\bigl((x'-x)-v\sigma\bigr).
\end{aligned}
```

Consequently,

```math
f_1(x')
=
f_0(x'-v\sigma),
```

which is rigid translation through $v\sigma$.

If

```math
\omega(k)=\alpha k^2,
```

then, with the standard square-root branch,

```math
\mathcal K_\sigma(x'-x)
=
\frac{1}{\sqrt{4\pi i\alpha\sigma}}
\exp\left[
\frac{i(x'-x)^2}{4\alpha\sigma}
\right].
```

This kernel is spread over every value of $x'-x$. The new value at one point receives contributions from many old points, with phases that alternate as the displacement changes.

## 3. What the full kernel sums

Introduce the endpoint displacement

```math
\xi=x'-x.
```

The kernel is

```math
\mathcal K_\sigma(\xi)
=
\frac{1}{2\pi}
\int e^{i\Phi(k;\xi,\sigma)}\,dk,
```

where

```math
\boxed{
\Phi(k;\xi,\sigma)
=
k\xi-\omega(k)\sigma.
}
```

For fixed endpoints and a fixed interval, every $k$ contributes one complex number. The kernel sums those Fourier-mode contributions. It does **not** yet sum over paths through intermediate $x$- and $k$-values.

When the phase oscillates rapidly enough for stationary-phase reasoning to apply, neighboring $k$-contributions mostly cancel. Contributions near a stationary value $k_*$ remain aligned longer. The stationary-phase condition is

```math
\left.
\frac{\partial\Phi}{\partial k}
\right|_{k_*}
=
0.
```

Since

```math
\frac{\partial\Phi}{\partial k}
=
\xi-\omega'(k)\sigma,
```

the condition becomes

```math
\boxed{
\frac{x'-x}{\sigma}
=
\omega'(k_*).
}
```

Thus stationary-phase analysis of the exact full-interval kernel supplies the relation between endpoint displacement, interval length, and the Fourier labels that contribute coherently in that regime.

For a translation-invariant rule $\omega(k)$, no division into short intervals is required. The one Fourier integral gives the complete evolution.

## 4. Variation from two exact intervals

The exact group rule

```math
U(\sigma_1+\sigma_2)
=
U(\sigma_2)U(\sigma_1)
```

becomes exact kernel composition:

```math
\mathcal K_{\sigma_1+\sigma_2}(x_2-x_0)
=
\int
\mathcal K_{\sigma_2}(x_2-x_1)
\mathcal K_{\sigma_1}(x_1-x_0)
\,dx_1.
```

Neither $\sigma_1$ nor $\sigma_2$ is assumed to be small. The integral simply sums over every possible intermediate coordinate $x_1$, just as matrix multiplication sums over an intermediate matrix index.

Insert the exact Fourier expression for both kernels. Their combined phase is

```math
\begin{aligned}
\Phi
&=
k_1(x_1-x_0)
-
\omega(k_1)\sigma_1
\\
&\quad+
k_2(x_2-x_1)
-
\omega(k_2)\sigma_2.
\end{aligned}
```

Thus

```math
\mathcal K_{\sigma_1+\sigma_2}(x_2-x_0)
=
\int
dx_1
\frac{dk_1}{2\pi}
\frac{dk_2}{2\pi}
e^{i\Phi}.
```

The integral sums over $x_1$, $k_1$, and $k_2$. Its $x_1$-dependence is

```math
e^{i(k_1-k_2)x_1},
```

so the $x_1$ integral gives

```math
\int
e^{i(k_1-k_2)x_1}
\,dx_1
=
2\pi\delta(k_1-k_2).
```

Exact composition therefore enforces

```math
k_1=k_2.
```

The stationary-phase expression of the same fact is

```math
\frac{\partial\Phi}{\partial x_1}
=
k_1-k_2
=
0.
```

When stationary-phase reasoning applies to the $k_1$ and $k_2$ integrals, stationarity with respect to those Fourier labels gives

```math
\frac{x_1-x_0}{\sigma_1}
=
\omega'(k_1),
\qquad
\frac{x_2-x_1}{\sigma_2}
=
\omega'(k_2).
```

A stationary candidate route therefore has the same Fourier label on both sides of the intermediate point. There may be more than one stationary candidate. For example, when

```math
\omega(k)=\alpha k^2,
```

stationarity in each $k_j$ reduces the combined phase to

```math
\Phi_*(x_1)
=
\frac{(x_1-x_0)^2}{4\alpha\sigma_1}
+
\frac{(x_2-x_1)^2}{4\alpha\sigma_2}.
```

Then

```math
\frac{d\Phi_*}{dx_1}=0
```

requires

```math
\frac{x_1-x_0}{\sigma_1}
=
\frac{x_2-x_1}{\sigma_2}.
```

An arbitrary $x_1$ describes a candidate broken route. The stationary choice joins its two parts with the same rate of displacement.

This already exhibits the basic variational idea using only exact full-interval kernels: hold the endpoints fixed, vary the intermediate route, and find where its phase is stationary.

## 5. Why introduce a path functional at all?

The exact kernel above works so simply because $\omega$ depends only on $k$. Every $k$-mode remains independent throughout the whole interval.

Now allow the local relation to depend on position as well:

```math
\omega=\omega(x,k).
```

This abandons strict $x$-translation invariance. A single global Fourier transform no longer diagonalizes the rule, so the preceding one-integral formula is no longer available in the same simple form.

At the operator level, a rule involving both $x$ and $k$ also requires a prescription for ordering the noncommuting operators $\hat X$ and $\hat K$. Here we work directly with the scalar phase function $\omega(x,k)$.

The endpoint phase

```math
k(x'-x)-\omega(k)(s_1-s_0)
```

can be written, when $k$ and $\omega$ remain constant, as

```math
\int_\gamma
\left[
k\,dx-\omega\,ds
\right].
```

This motivates, but does not uniquely derive, a local additive extension when $x$, $k$, and $\omega$ may change along the curve:

```math
\boxed{
\Phi[\gamma]
=
\int_\gamma
\left[
k\,dx-\omega(x,k)\,ds
\right].
}
```

Writing the curve as

```math
\gamma:s\longmapsto\bigl(x(s),k(s),s\bigr),
```

the same expression is

```math
\boxed{
\Phi[x,k]
=
\int_{s_0}^{s_1}
\left[
k\dot x-\omega(x,k)
\right]ds.
}
```

At each point, $k$ is the phase change per unit displacement in $x$, while $-\omega$ is the phase change per unit displacement in $s$. The integral accumulates those local phase changes along the curve.

This is the step at which a path functional enters. It is the smooth, local generalization of the two-segment phase above. Deriving an arbitrary-path sum from operator composition would require many intervals and a limiting procedure. Here we state the resulting phase functional directly and calculate its variation.

## 6. Comparing two paths by a loop

Define the phase one-form

```math
\alpha
=
k\,dx-\omega(x,k)\,ds.
```

Then

```math
\Phi[\gamma]=\int_\gamma\alpha.
```

Let $\gamma$ and $\gamma'$ have the same endpoints. Traverse $\gamma'$ forward and $\gamma$ backward. Together they form a closed loop, so

```math
\Phi[\gamma']-\Phi[\gamma]
=
\oint\alpha.
```

If the loop bounds a ribbon $R$, Stokes' theorem gives

```math
\boxed{
\Phi[\gamma']-\Phi[\gamma]
=
\iint_R d\alpha.
}
```

The difference between the accumulated phases can therefore be obtained by tiling the ribbon with small loops and adding their local contributions.

For general $\omega(x,k)$,

```math
\begin{aligned}
d\alpha
&=
dk\wedge dx-d\omega\wedge ds
\\
&=
dk\wedge dx
-
\frac{\partial\omega}{\partial x}
dx\wedge ds
-
\frac{\partial\omega}{\partial k}
dk\wedge ds.
\end{aligned}
```

For the translation-invariant case $\omega=\omega(k)$, this reduces to

```math
\begin{aligned}
d\alpha
&=
dk\wedge dx
-
\omega'(k)dk\wedge ds
\\
&=
dk\wedge
\left[
dx-\omega'(k)ds
\right].
\end{aligned}
```

The term

```math
dk\wedge dx
```

is the local $x$-$k$ commutator-loop contribution. It is only one part of the variation of the accumulated phase. A picture drawn solely in the $x$-$k$ plane omits the terms containing $ds$.

## 7. Varying the phase functional

The variational principle asks for curves on which the first-order change in $\Phi$ vanishes:

```math
\delta\Phi=0.
```

This means that $\Phi$ is stationary, not necessarily that it is smallest or largest.

Begin with

```math
\Phi[x,k]
=
\int_{s_0}^{s_1}
\left[
k\dot x-\omega(x,k)
\right]ds.
```

Change the two functions by small amounts:

```math
x(s)\longrightarrow x(s)+\delta x(s),
\qquad
k(s)\longrightarrow k(s)+\delta k(s).
```

The resulting first-order change is

```math
\begin{aligned}
\delta\Phi
&=
\int_{s_0}^{s_1}
\left[
\delta k\,\dot x
+
k\,\delta\dot x
-
\frac{\partial\omega}{\partial x}\delta x
-
\frac{\partial\omega}{\partial k}\delta k
\right]ds.
\end{aligned}
```

Here

```math
\delta\dot x
=
\frac{d}{ds}\delta x.
```

Integrate the $k\,\delta\dot x$ term by parts:

```math
\int_{s_0}^{s_1}
k\,\delta\dot x
\,ds
=
\left[k\,\delta x\right]_{s_0}^{s_1}
-
\int_{s_0}^{s_1}
\dot k\,\delta x
\,ds.
```

The paths being compared have the same $x$-endpoints, so

```math
\delta x(s_0)=\delta x(s_1)=0.
```

The boundary term therefore vanishes. After collecting the $\delta x$ and $\delta k$ terms,

```math
\delta\Phi
=
\int_{s_0}^{s_1}
\left[
\left(
\dot x-
\frac{\partial\omega}{\partial k}
\right)
\delta k
-
\left(
\dot k+
\frac{\partial\omega}{\partial x}
\right)
\delta x
\right]ds.
```

The functions $\delta x(s)$ and $\delta k(s)$ can be varied independently. For $\delta\Phi$ to vanish for every allowed variation, each coefficient must vanish:

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

For the translation-invariant case $\omega=\omega(k)$,

```math
\dot k=0,
\qquad
\dot x=\omega'(k).
```

Therefore

```math
k(s)=k_*
```

is constant and

```math
x(s)
=
x(s_0)+\omega'(k_*)(s-s_0).
```

At the endpoints,

```math
\boxed{
\frac{x(s_1)-x(s_0)}{s_1-s_0}
=
\omega'(k_*).
}
```

This reproduces the stationary-phase condition obtained directly from the full-interval kernel. It is a consistency check: the path functional was introduced directly here rather than derived from the full kernel by subdivision.

## 8. The Euler--Lagrange form

Define

```math
\mathcal L(x,k,\dot x,\dot k)
=
k\dot x-\omega(x,k).
```

Then

```math
\Phi[x,k]
=
\int_{s_0}^{s_1}\mathcal L\,ds.
```

Applying the Euler--Lagrange equation to $x$ gives

```math
\frac{d}{ds}
\frac{\partial\mathcal L}{\partial\dot x}
-
\frac{\partial\mathcal L}{\partial x}
=
\dot k
+
\frac{\partial\omega}{\partial x}
=
0.
```

Applying it to $k$ gives

```math
\frac{d}{ds}
\frac{\partial\mathcal L}{\partial\dot k}
-
\frac{\partial\mathcal L}{\partial k}
=
-\left(
\dot x-
\frac{\partial\omega}{\partial k}
\right)
=
0.
```

These are the same two equations obtained by varying $\Phi$ directly.

If

```math
\dot x
=
\frac{\partial\omega}{\partial k}
```

can be solved for

```math
k=k(x,\dot x),
```

define

```math
L(x,\dot x)
=
k(x,\dot x)\dot x
-
\omega\bigl(x,k(x,\dot x)\bigr).
```

Then

```math
\frac{\partial L}{\partial\dot x}=k,
\qquad
\frac{\partial L}{\partial x}
=
-\frac{\partial\omega}{\partial x},
```

and the ordinary Euler--Lagrange equation

```math
\frac{d}{ds}
\frac{\partial L}{\partial\dot x}
-
\frac{\partial L}{\partial x}
=
0
```

becomes

```math
\dot k
+
\frac{\partial\omega}{\partial x}
=
0.
```

## 9. What was gained by using the full interval

For $\omega=\omega(k)$, the full-interval kernel gives the exact evolution immediately:

```math
\mathcal K_\sigma(x'-x)
=
\frac{1}{2\pi}
\int
e^{i[k(x'-x)-\omega(k)\sigma]}
\,dk.
```

When stationary-phase reasoning applies, its stationary phase gives

```math
\frac{x'-x}{\sigma}=\omega'(k_*).
```

The path functional is needed only when we want to describe a locally changing $x(s)$ and $k(s)$, compare neighboring curves, or allow $\omega$ to depend on position. Its stationary curve reproduces the same result in the translation-invariant case and extends it to

```math
\dot x
=
\frac{\partial\omega}{\partial k},
\qquad
\dot k
=
-\frac{\partial\omega}{\partial x}.
```

Composing two full intervals already reveals the elementary variational idea. A many-interval limiting construction is needed only if we also want to derive the arbitrary-path sum from repeated operator composition.
