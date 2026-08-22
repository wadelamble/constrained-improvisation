# From Symmetry to Variation

## 1. Begin with a complex function

Let $f(x)$ be a complex-valued function of one real variable. To keep the ordinary integrals and derivatives well behaved, suppose initially that $f$ is smooth and rapidly decaying. Such functions belong to $L^2(\mathbb R)$:

```math
\|f\|^2
=
\int_{-\infty}^{\infty}|f(x)|^2\,dx
<\infty.
```

Wherever $f(x)\neq 0$, it can be written in polar form:

```math
f(x)=A(x)e^{i\phi(x)},
```

where

```math
A(x)=|f(x)|
```

and

```math
\phi(x)=\arg f(x)
```

is defined modulo $2\pi$. The amplitude $A(x)$ is not generally constant. Square-integrability constrains the single number $\int |f|^2dx$; it does not require $|f(x)|$ to have the same value at every $x$. For example,

```math
f(x)=e^{-x^2}e^{ik_0x}
```

has

```math
A(x)=e^{-x^2},
\qquad
\phi(x)=k_0x.
```

The amplitude decays, while the phase turns at a uniform rate.

## 2. Plane waves

A plane wave is

```math
u_k(x)=e^{ikx}.
```

Its magnitude is constant:

```math
|u_k(x)|=1,
```

and its phase is

```math
\phi_k(x)=kx.
```

Because

```math
\int_{-\infty}^{\infty}|u_k(x)|^2\,dx
=
\int_{-\infty}^{\infty}1\,dx
=\infty,
```

a plane wave is not an element of $L^2(\mathbb R)$. It is a **generalized** basis vector. The square-integrable objects will be wave packets assembled by continuously superposing these generalized vectors.

If we want literal square-integrable plane-wave basis vectors, we can temporarily place $x$ in a periodic interval of length $L$. Then

```math
u_n(x)
=
\frac{1}{\sqrt L}e^{i2\pi nx/L}
```

are normalized basis functions. The generalized plane waves on $\mathbb R$ arise as the limit $L\to\infty$.

## 3. Wave packets as superpositions of plane waves

Define the Fourier transform by

```math
\widetilde f(k)
=
\frac{1}{\sqrt{2\pi}}
\int_{-\infty}^{\infty}
f(x)e^{-ikx}\,dx.
```

The inverse transform is

```math
f(x)
=
\frac{1}{\sqrt{2\pi}}
\int_{-\infty}^{\infty}
\widetilde f(k)e^{ikx}\,dk.
```

Thus $\widetilde f(k)$ gives the coefficient of the generalized plane-wave component $e^{ikx}$. The Fourier transform is unitary on $L^2$:

```math
\int |f(x)|^2\,dx
=
\int |\widetilde f(k)|^2\,dk.
```

This is how a square-integrable function can be composed of plane waves that are not individually square-integrable. Their continuously weighted sum can interfere destructively at large $|x|$ and produce a localized envelope.

When the relevant moments exist, we can define the center of the function in the two representations:

```math
x_c(f)
=
\frac{\displaystyle\int x|f(x)|^2\,dx}
{\displaystyle\int |f(x)|^2\,dx},
```

and

```math
k_c(f)
=
\frac{\displaystyle\int k|\widetilde f(k)|^2\,dk}
{\displaystyle\int |\widetilde f(k)|^2\,dk}.
```

A plane wave has no $x$-center. A localized packet can have both an $x$-center and a $k$-center, although it is not concentrated at an exact value of both.

## 4. Translation in $x$

Define translation through a distance $a$ by

```math
(T_a f)(x)=f(x-a).
```

These operators obey the translation-group rule

```math
T_aT_b=T_{a+b},
\qquad
T_0=I,
\qquad
T_a^{-1}=T_{-a}.
```

They are linear. They also preserve the inner product:

```math
\begin{aligned}
\langle T_af,T_ag\rangle
&=
\int f^*(x-a)g(x-a)\,dx
\\
&=
\int f^*(y)g(y)\,dy
\\
&=
\langle f,g\rangle,
\end{aligned}
```

where $y=x-a$. Thus $T_a$ is unitary on $L^2(\mathbb R)$.

A plane wave is an eigenfunction of every translation:

```math
T_au_k(x)
=
e^{ik(x-a)}
=
e^{-ika}u_k(x).
```

The eigenvalue $e^{-ika}$ has magnitude one, as it must for a unitary operator.

In Fourier space, translation acts by the same phase factor:

```math
\widetilde{T_af}(k)
=
e^{-ika}\widetilde f(k).
```

Translation shifts the packet's $x$-center while leaving the magnitude of its Fourier distribution unchanged:

```math
x_c(T_af)=x_c(f)+a,
\qquad
k_c(T_af)=k_c(f).
```

To find the infinitesimal generator, differentiate at the identity $a=0$:

```math
\left.\frac{d}{da}T_af(x)\right|_{a=0}
=
-\frac{df}{dx}.
```

Writing

```math
T_a=e^{-ia\hat K}
```

therefore gives

```math
\hat K=-i\frac{d}{dx}.
```

Indeed,

```math
e^{-ia\hat K}
=
e^{-a\partial_x},
```

and the exponential of the derivative translates the function:

```math
e^{-a\partial_x}f(x)=f(x-a).
```

The eigenvalue equation

```math
\hat Ku_k=ku_k
```

is

```math
-i\frac{du_k}{dx}=ku_k,
```

whose solutions are

```math
u_k(x)=Ce^{ikx}.
```

## 5. Translation in $k$

Define another family of operators by

```math
(M_bf)(x)=e^{ibx}f(x).
```

Its Fourier transform is

```math
\widetilde{M_bf}(k)
=
\widetilde f(k-b).
```

Thus $M_b$ translates the Fourier distribution through $b$:

```math
x_c(M_bf)=x_c(f),
\qquad
k_c(M_bf)=k_c(f)+b.
```

Let $\hat X$ denote multiplication by the coordinate:

```math
(\hat Xf)(x)=xf(x).
```

Then

```math
M_b=e^{ib\hat X}.
```

We now have two continuous transformations acting on the same function space:

```math
T_a=e^{-ia\hat K}
```

shifts the function in $x$, while

```math
M_b=e^{ib\hat X}
```

shifts it in $k$.

## 6. The two translations do not commute

Apply the operators in one order:

```math
\begin{aligned}
(T_aM_bf)(x)
&=
(M_bf)(x-a)
\\
&=
e^{ib(x-a)}f(x-a).
\end{aligned}
```

Reverse the order:

```math
\begin{aligned}
(M_bT_af)(x)
&=
e^{ibx}(T_af)(x)
\\
&=
e^{ibx}f(x-a).
\end{aligned}
```

Therefore

```math
T_aM_b
=
e^{-iab}M_bT_a.
```

This is an operator identity on the whole function space. A plane wave is a convenient function on which to demonstrate it, but the identity is not defined only for plane waves.

Complete the corresponding operator loop:

```math
C(a,b)
=
T_aM_bT_{-a}M_{-b}.
```

Using the preceding relation,

```math
\begin{aligned}
C(a,b)
&=
e^{-iab}M_bT_aT_{-a}M_{-b}
\\
&=
e^{-iab}I.
\end{aligned}
```

Hence, for every suitable function,

```math
C(a,b)f=e^{-iab}f.
```

If

```math
f(x)=A(x)e^{i\phi(x)},
```

then

```math
C(a,b)f(x)
=
A(x)e^{i[\phi(x)-ab]}.
```

The loop restores the function's $x$- and $k$-distributions exactly, but changes its common phase by $-ab$. On a localized packet, the four transformations move $(x_c,k_c)$ around a rectangle and return it to its starting point. The residual phase is present even though both centers have returned.

## 7. The infinitesimal commutator and the order of the loop phase

Acting on an arbitrary smooth function,

```math
\begin{aligned}
[\hat X,\hat K]f
&=
\hat X\hat Kf-\hat K\hat Xf
\\
&=
-ixf'(x)+i\frac{d}{dx}[xf(x)]
\\
&=
-ixf'(x)+if(x)+ixf'(x)
\\
&=
if(x).
\end{aligned}
```

Therefore

```math
[\hat X,\hat K]=iI.
```

This is the infinitesimal form of the finite relation

```math
T_aM_bT_{-a}M_{-b}=e^{-iab}I.
```

To see why the loop phase is second order, let both side lengths shrink with a single small parameter $\epsilon$:

```math
a=\alpha\epsilon,
\qquad
b=\beta\epsilon.
```

Then

```math
\begin{aligned}
C(\epsilon)
&=
e^{-i\alpha\beta\epsilon^2}I
\\
&=
\left[
I-i\alpha\beta\epsilon^2I+O(\epsilon^4)
\right].
\end{aligned}
```

There is no first-order term. The forward and backward displacements cancel at first order; only their failure to commute remains. More generally,

```math
e^{\epsilon A}
e^{\epsilon B}
e^{-\epsilon A}
e^{-\epsilon B}
=
I+\epsilon^2[A,B]+O(\epsilon^3).
```

Thus an open infinitesimal step produces a first-order change, while a closed commutator loop produces a second-order change proportional to its oriented area.

## 8. A second translation direction before it is called evolution

We can now introduce a second coordinate $s$ without assigning it any special interpretation. Consider functions of two variables, $f(x,s)$, and the joint Fourier modes

```math
u_{k,q}(x,s)=e^{i(kx+qs)}.
```

The corresponding translation generators are

```math
\hat K=-i\partial_x,
\qquad
\hat Q=-i\partial_s,
```

with

```math
\hat Ku_{k,q}=ku_{k,q},
\qquad
\hat Qu_{k,q}=qu_{k,q}.
```

Introduce the coordinate-multiplication operators

```math
(\hat Xf)(x,s)=xf(x,s),
\qquad
(\hat Sf)(x,s)=sf(x,s).
```

On the unconstrained two-variable function space, there are two symmetric conjugate pairs:

```math
[\hat X,\hat K]=iI,
\qquad
[\hat S,\hat Q]=iI.
```

All cross-commutators vanish:

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

There can therefore be one commutator loop in the $x$-$k$ plane and another in the $s$-$q$ plane. Their oriented areas contribute to the same common phase coordinate. Using consistent orientations, a combined loop has phase

```math
\Delta\phi
=
-A_{xk}-A_{sq}.
```

The two areas do not create two different kinds of phase: both commutators are proportional to the same identity operator $I$.

At this stage, $x$ and $s$ are mathematically symmetric. We have not yet said that $s$ is an evolution parameter. We have only constructed the Fourier representation of a two-dimensional translation group.

## 9. Relating the two translation generators

Now supply a real function $\Omega(k)$ and impose the relation

```math
q=-\Omega(k).
```

This relation is not determined by translation symmetry. It is additional information selecting a subset of the joint Fourier modes. Substituting it into the general mode gives

```math
u_k(x,s)
=
e^{i[kx-\Omega(k)s]}.
```

A general superposition of the selected modes is

```math
f(x,s)
=
\frac{1}{\sqrt{2\pi}}
\int
c(k)e^{i[kx-\Omega(k)s]}
\,dk.
```

In the unconstrained two-dimensional Fourier representation, the same restriction can be written

```math
\widetilde f(k,q)
\propto
c(k)\delta\bigl(q+\Omega(k)\bigr).
```

The proportionality factor depends only on the chosen two-dimensional Fourier normalization. The substantive statement is

```math
\operatorname{supp}\widetilde f
\subseteq
\left\{(k,q):q=-\Omega(k)\right\}.
```

The Fourier weight is supported only on the curve $q=-\Omega(k)$.

This is no longer an arbitrary function of two independent variables. Once $c(k)$, or equivalently the entire slice $f(x,0)$, is given, every other $s$-slice is fixed.

In the one-parameter language, define

```math
\hat\Omega=\Omega(\hat K)
```

and

```math
U(s)=e^{-is\hat\Omega}.
```

Then

```math
f_s=U(s)f_0.
```

In the $k$-representation,

```math
\widetilde{U(s)f}(k)
=
e^{-i\Omega(k)s}\widetilde f(k).
```

Because $\Omega(k)$ is real,

```math
\left|e^{-i\Omega(k)s}\right|=1,
```

and therefore

```math
\|U(s)f\|=\|f\|.
```

Thus $U(s)$ is unitary on $L^2(\mathbb R)$; only the possibly unbounded generator $\hat\Omega$ requires a restricted domain.

More generally, any two slices are related by

```math
f(\,cdot\,,s+\sigma)
=
U(\sigma)f(\,\cdot\,,s).
```

This is the exact sense in which the one-parameter flow is still translation in the second coordinate: shifting the coordinate from $s$ to $s+\sigma$ applies the group element $U(\sigma)$ to the function on the original slice.

The family $U(s)$ obeys

```math
U(0)=I,
\qquad
U(s_1+s_2)=U(s_1)U(s_2),
\qquad
U(-s)=U(s)^{-1}.
```

These equations make $U(s)$ a reversible one-parameter flow. Its infinitesimal generator is

```math
\hat\Omega
=
i\left.\frac{dU(s)}{ds}\right|_{s=0}.
```

Nothing in these equations makes $s$ intrinsically temporal. We could call it $y$ and interpret the same family as propagation in a second spatial direction. The word **evolution** means only that we choose to regard $s$ as the parameter ordering successive slices, so that the current slice determines the next one.

This is simultaneously the same as and different from adding an unconstrained second translation direction:

- It is the same because $U(s)$ is a continuous representation of the additive translation group in $s$.
- It is different because its generator is no longer independent: $\hat\Omega$ has been specified as a function of $\hat K$.

In the unconstrained two-coordinate picture, $\hat Q$ and $\hat K$ were independent generators. The constraint

```math
q=-\Omega(k)
```

selects a curve in their joint eigenvalue space. Equivalently, on the selected functions,

```math
\hat Qf=-\Omega(\hat K)f.
```

The operator $\Omega(\hat K)$ generally does not belong to the finite-dimensional Heisenberg--Weyl algebra

```math
\operatorname{span}\{\hat X,\hat K,I\}
```

unless $\Omega(k)$ is affine. It is an additional operator acting on the same function space.

### Why translation symmetry makes the flow diagonal in $k$

Suppose a one-parameter family $U(s)$ commutes with every $x$-translation:

```math
U(s)T_a=T_aU(s).
```

Because

```math
T_au_k=e^{-ika}u_k,
```

we have

```math
\begin{aligned}
T_a[U(s)u_k]
&=
U(s)T_au_k
\\
&=
e^{-ika}U(s)u_k.
\end{aligned}
```

Thus $U(s)u_k$ remains in the same translation-eigenspace. In the one-dimensional case, it can only be a scalar multiple of $u_k$:

```math
U(s)u_k=u_s(k)u_k.
```

If $U(s)$ is unitary, then

```math
|u_s(k)|=1.
```

If it is continuous and obeys the group-composition rule, then its scalar multiplier must be a continuous character of the additive $s$-group:

```math
u_s(k)=e^{-i\Omega(k)s}
```

for some real $\Omega(k)$. Translation symmetry therefore makes the flow diagonal in $k$. It does not force $\Omega(k)$ to depend nontrivially on $k$. The constant choice

```math
\Omega(k)=\Omega_0
```

is allowed and gives only a common phase. The function $\Omega(k)$ is the remaining information needed to specify which translation-compatible flow we mean.

### The first-order update rule

For a small step $\delta s$,

```math
\widetilde f(k,s+\delta s)
=
e^{-i\Omega(k)\delta s}
\widetilde f(k,s).
```

Expanding,

```math
\widetilde f(k,s+\delta s)
=
\left[
1-i\Omega(k)\delta s+O(\delta s^2)
\right]
\widetilde f(k,s).
```

Subtracting $\widetilde f(k,s)$, dividing by $\delta s$, and taking the limit gives

```math
i\frac{\partial\widetilde f(k,s)}{\partial s}
=
\Omega(k)\widetilde f(k,s).
```

In the $x$-representation,

```math
i\frac{\partial f(x,s)}{\partial s}
=
\Omega(-i\partial_x)f(x,s).
```

This is why specifying $\Omega(k)$ turns translation in $s$ into an evolution rule: the complete function on one slice determines the complete function on the next slice. In Fourier space, the rule tells every $k$-component how much phase to acquire. It does not move the label $k$ itself.

## 10. First-order phase accumulation and second-order loop phase

For a selected mode,

```math
u_k(x,s)=e^{i\phi_k(x,s)},
```

with

```math
\phi_k(x,s)=kx-\Omega(k)s.
```

At fixed $x$, an infinitesimal $s$-translation gives

```math
u_k(x,s+\delta s)
=
e^{-i\Omega(k)\delta s}u_k(x,s),
```

so

```math
\delta\phi_k=-\Omega(k)\delta s.
```

At fixed $s$, an infinitesimal $x$-translation gives

```math
\delta\phi_k=k\delta x.
```

Allowing both coordinates to change,

```math
d\phi_k
=
k\,dx-\Omega(k)\,ds.
```

This phase change is first order in the open displacement. For a packet, it applies separately to each Fourier component; different values of $k$ generally accumulate different phases.

The commutator loop is different. For a loop with infinitesimal side lengths $da$ and $db$,

```math
T_{da}M_{db}T_{-da}M_{-db}
=
e^{-i\,da\,db}I.
```

Thus the whole packet receives the common phase

```math
\delta\phi_{\mathrm{loop}}
=
-da\,db.
```

This is second order because both side lengths are infinitesimal. The open $s$-step phase and the closed $x$-$k$ loop phase are therefore related but distinct structures:

```math
\text{open one-parameter step}
\quad\longrightarrow\quad
\delta\phi=O(\delta s),
```

whereas

```math
\text{closed two-parameter loop}
\quad\longrightarrow\quad
\delta\phi=O(da\,db).
```

For the complete packet itself, wherever $f(x,s)\neq 0$, we may also write

```math
f(x,s)=A(x,s)e^{i\phi(x,s)}.
```

The pointwise phase of the packet is $\phi(x,s)=\arg f(x,s)$. If $x=x_c(s)$ is a chosen curve, such as the magnitude-squared centroid, then the chain rule gives

```math
\frac{d}{ds}\phi(x_c(s),s)
=
\frac{\partial\phi}{\partial s}
+
\dot x_c
\frac{\partial\phi}{\partial x}.
```

Defining the local derivatives

```math
\kappa(x,s)=\frac{\partial\phi}{\partial x},
\qquad
\nu(x,s)=-\frac{\partial\phi}{\partial s},
```

we can write

```math
d\phi=\kappa\,dx-\nu\,ds.
```

For a single mode, $\kappa=k$ and $\nu=\Omega(k)$. For a general interfering packet, the pointwise quantities $\kappa$ and $\nu$ need not equal the center values of its Fourier distribution. The exact statement is always componentwise; the single local-mode description requires an additional narrow-band or slowly varying approximation.

## 11. What an integral kernel is

The expression

```math
\widetilde f(k,s+\delta s)
=
e^{-i\Omega(k)\delta s}\widetilde f(k,s)
```

is simple because the operator is diagonal in the $k$-representation. We now want to express the same operator in the $x$-representation.

For a finite-dimensional vector, a matrix acts by

```math
v'_i=\sum_j U_{ij}v_j.
```

The entry $U_{ij}$ tells how much the old component at index $j$ contributes to the new component at index $i$.

For a function, the coordinate label is continuous rather than discrete. To avoid confusing the kernel with the translation generator $\hat K$, denote it by $\mathcal K$. The corresponding formula is

```math
(Uf)(x')
=
\int \mathcal K(x',x)f(x)\,dx.
```

The **kernel** $\mathcal K(x',x)$ is therefore a matrix with continuous indices. It tells how the input value at $x$ contributes linearly to the output value at $x'$. A kernel may be an ordinary function or a generalized function such as a delta function.

Because our operator commutes with $x$-translations, it cannot depend on the absolute location of $x$ and $x'$ separately. It can depend only on their difference:

```math
\mathcal K_{\delta s}(x',x)
=
\mathcal K_{\delta s}(x'-x).
```

### Deriving the kernel rather than guessing it

Start with the Fourier-space update and transform back:

```math
\begin{aligned}
(U(\delta s)f)(x')
&=
\frac{1}{\sqrt{2\pi}}
\int
e^{ikx'}e^{-i\Omega(k)\delta s}
\widetilde f(k)\,dk.
\end{aligned}
```

Now substitute

```math
\widetilde f(k)
=
\frac{1}{\sqrt{2\pi}}
\int e^{-ikx}f(x)\,dx.
```

Then

```math
\begin{aligned}
(U(\delta s)f)(x')
&=
\frac{1}{2\pi}
\int dk\int dx\;
e^{ikx'}e^{-i\Omega(k)\delta s}e^{-ikx}f(x)
\\
&=
\int dx
\left[
\frac{1}{2\pi}
\int dk\;
e^{i[k(x'-x)-\Omega(k)\delta s]}
\right]
f(x).
\end{aligned}
```

Therefore the short-step kernel is

```math
\boxed{
\mathcal K_{\delta s}(x'-x)
=
\frac{1}{2\pi}
\int
e^{i[k(x'-x)-\Omega(k)\delta s]}
\,dk.
}
```

The kernel is not an additional law. It is the same diagonal multiplier $e^{-i\Omega(k)\delta s}$ rewritten in the $x$-representation.

The exponent contains the phase associated with a short displacement:

```math
\delta\phi
=
k(x'-x)-\Omega(k)\delta s.
```

The kernel sums this contribution over every Fourier label $k$.

### Three simple kernels

If

```math
\Omega(k)=\Omega_0,
```

then

```math
\mathcal K_{\delta s}(x'-x)
=
e^{-i\Omega_0\delta s}\delta(x'-x).
```

The output remains at the same $x$ and acquires only a common phase.

If

```math
\Omega(k)=vk,
```

then

```math
\begin{aligned}
\mathcal K_{\delta s}(x'-x)
&=
\frac{1}{2\pi}
\int
e^{ik[(x'-x)-v\delta s]}
\,dk
\\
&=
\delta[(x'-x)-v\delta s].
\end{aligned}
```

Consequently,

```math
(U(\delta s)f)(x')
=
f(x'-v\delta s),
```

which is rigid translation through $v\delta s$.

If

```math
\Omega(k)=\alpha k^2,
```

then, with the standard square-root branch,

```math
\mathcal K_{\delta s}(x'-x)
=
\frac{1}{\sqrt{4\pi i\alpha\delta s}}
\exp\left[
\frac{i(x'-x)^2}{4\alpha\delta s}
\right].
```

This kernel is spread over all $x'-x$. The new value at one point receives contributions from many old points, with phases that alternate rapidly as the displacement changes.

## 12. Composing kernels produces a sum over paths

The group rule

```math
U(s_1+s_2)=U(s_1)U(s_2)
```

becomes kernel composition:

```math
\mathcal K_{s_1+s_2}(x_2,x_0)
=
\int
\mathcal K_{s_2}(x_2,x_1)
\mathcal K_{s_1}(x_1,x_0)
\,dx_1.
```

This is continuous matrix multiplication: we sum over the intermediate index $x_1$.

Divide a total interval

```math
S=s_N-s_0
```

into $N$ steps of length

```math
\delta s=\frac{S}{N}.
```

Repeated composition gives

```math
\mathcal K_S(x_N,x_0)
=
\int
\prod_{j=1}^{N-1}dx_j
\prod_{j=0}^{N-1}
\mathcal K_{\delta s}(x_{j+1}-x_j).
```

Insert the Fourier expression for every short-step kernel:

```math
\mathcal K_{\delta s}(x_{j+1}-x_j)
=
\int\frac{dk_j}{2\pi}
\exp\left\{
i\left[
k_j(x_{j+1}-x_j)
-
\Omega(k_j)\delta s
\right]
\right\}.
```

The complete kernel becomes

```math
\begin{aligned}
\mathcal K_S(x_N,x_0)
&=
\int
\left[
\prod_{j=1}^{N-1}dx_j
\right]
\left[
\prod_{j=0}^{N-1}\frac{dk_j}{2\pi}
\right]
e^{i\Phi_N[x,k]},
\end{aligned}
```

where

```math
\Phi_N[x,k]
=
\sum_{j=0}^{N-1}
\left[
k_j(x_{j+1}-x_j)
-
\Omega(k_j)\delta s
\right].
```

A sequence

```text
x_0,k_0,x_1,k_1,\ldots,x_{N-1},k_{N-1},x_N
```

is a discrete path through the intermediate $x$- and $k$-values. The sum over such paths has not been independently postulated. It appears because composing linear operators requires summing over every intermediate matrix index, and changing between the $x$- and $k$-representations introduces the intermediate $k_j$ integrals.

For finite $N$, this is an ordinary multiple integral representing repeated operator composition. The continuous path notation is shorthand for the limit. In that limit,

```math
x_{j+1}-x_j
\longrightarrow
\dot x\,ds,
```

and the discrete phase becomes

```math
\boxed{
\Phi[x,k]
=
\int_{s_0}^{s_1}
\left[
k\dot x-\Omega(k)
\right]ds
=
\int_\gamma
\left[
k\,dx-\Omega(k)\,ds
\right].
}
```

Thus the first-order phase functional is the accumulated exponent generated by composing the infinitesimal translation kernels.

## 13. The local-loop view of the same phase functional

Define the phase one-form

```math
\alpha
=
k\,dx-\Omega(k)\,ds.
```

For a path $\gamma$ in $(x,k,s)$ space,

```math
\Phi[\gamma]=\int_\gamma\alpha.
```

Let $\gamma$ and $\gamma'$ share the same endpoints. Traversing $\gamma'$ forward and $\gamma$ backward makes a closed loop. Their phase difference is

```math
\Phi[\gamma']-\Phi[\gamma]
=
\oint\alpha.
```

If the loop bounds a ribbon $R$, Stokes' theorem gives

```math
\Phi[\gamma']-\Phi[\gamma]
=
\iint_R d\alpha.
```

For $\Omega=\Omega(k)$,

```math
\begin{aligned}
d\alpha
&=
dk\wedge dx
-
d\Omega\wedge ds
\\
&=
dk\wedge dx
-
\Omega'(k)dk\wedge ds
\\
&=
dk\wedge
\left[
dx-\Omega'(k)ds
\right].
\end{aligned}
```

The term

```math
dk\wedge dx
```

is the local $x$-$k$ commutator-loop contribution. It is not the entire variation of the accumulated phase. The second term,

```math
-d\Omega\wedge ds,
```

comes from translation in the second parameter. A diagram drawn only in the $x$-$k$ plane displays the first contribution but omits the second.

This can also be seen from the unconstrained two-translation picture. Before imposing $q=-\Omega(k)$, the phase one-form is

```math
\theta=k\,dx+q\,ds,
```

with

```math
d\theta
=
dk\wedge dx+dq\wedge ds.
```

Restricting to

```math
q=-\Omega(k)
```

gives

```math
\theta
\longrightarrow
\alpha
=
k\,dx-\Omega(k)\,ds,
```

and

```math
d\theta
\longrightarrow
d\alpha
=
dk\wedge dx-d\Omega\wedge ds.
```

Thus the two initially symmetric Heisenberg--Weyl planes combine, after imposing the relation between their Fourier labels, into the curvature of the single accumulated-phase form.

## 14. Stationary phase and the Euler--Lagrange equations

The composed kernel sums terms of the form

```math
e^{i\Phi_N}.
```

When the phase varies rapidly, neighboring contributions whose phases change linearly cancel one another. Contributions near a stationary point of the phase remain aligned longer. The relevant condition is therefore

```math
\delta\Phi=0.
```

This means **stationary**, not necessarily smallest or largest.

### Stationarity in the discrete kernel

For

```math
\Phi_N
=
\sum_j
\left[
k_j(x_{j+1}-x_j)
-
\Omega(k_j)\delta s
\right],
```

varying one $k_j$ gives

```math
\frac{\partial\Phi_N}{\partial k_j}
=
x_{j+1}-x_j
-
\Omega'(k_j)\delta s.
```

Stationarity therefore requires

```math
\frac{x_{j+1}-x_j}{\delta s}
=
\Omega'(k_j).
```

Varying an intermediate $x_j$ gives contributions from the two adjoining steps:

```math
\frac{\partial\Phi_N}{\partial x_j}
=
k_{j-1}-k_j.
```

Thus

```math
k_j=k_{j-1}.
```

In the continuous limit,

```math
\dot x=\frac{d\Omega}{dk},
\qquad
\dot k=0.
```

These equations describe the stationary path for the translation-invariant choice $\Omega(k)$.

### Allowing local $x$-dependence

To display the general first-order variational structure, allow

```math
\Omega=\Omega(x,k).
```

This goes beyond strict $x$-translation invariance, because the flow can now depend on location. At the operator level, mixed $x$- and $k$-dependence requires a choice of ordering. At the level of the phase functional itself, the expression is

```math
\Phi[x,k]
=
\int_{s_0}^{s_1}
\left[
k\dot x-\Omega(x,k)
\right]ds.
```

Vary $x(s)$ and $k(s)$ independently:

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
\frac{\partial\Omega}{\partial x}\delta x
-
\frac{\partial\Omega}{\partial k}\delta k
\right]ds.
\end{aligned}
```

Integrate the $k\,\delta\dot x$ term by parts:

```math
\int k\,\delta\dot x\,ds
=
\left[k\,\delta x\right]_{s_0}^{s_1}
-
\int\dot k\,\delta x\,ds.
```

Fixing the $x$-endpoints makes

```math
\delta x(s_0)=\delta x(s_1)=0,
```

so the boundary term vanishes. We obtain

```math
\delta\Phi
=
\int_{s_0}^{s_1}
\left[
\left(
\dot x-\frac{\partial\Omega}{\partial k}
\right)\delta k
-
\left(
\dot k+\frac{\partial\Omega}{\partial x}
\right)\delta x
\right]ds.
```

Because $\delta x$ and $\delta k$ are independent, stationarity requires

```math
\boxed{
\dot x
=
\frac{\partial\Omega}{\partial k},
\qquad
\dot k
=
-\frac{\partial\Omega}{\partial x}.
}
```

These are directly the Euler--Lagrange equations for the first-order function

```math
\mathcal L(x,k,\dot x,\dot k)
=
k\dot x-\Omega(x,k).
```

For $x$,

```math
\frac{d}{ds}
\frac{\partial\mathcal L}{\partial\dot x}
-
\frac{\partial\mathcal L}{\partial x}
=
\dot k+\frac{\partial\Omega}{\partial x}
=0.
```

For $k$,

```math
\frac{d}{ds}
\frac{\partial\mathcal L}{\partial\dot k}
-
\frac{\partial\mathcal L}{\partial k}
=
-\left(
\dot x-\frac{\partial\Omega}{\partial k}
\right)
=0.
```

If

```math
\dot x
=
\frac{\partial\Omega}{\partial k}
```

can be inverted to obtain $k=k(x,\dot x)$, define

```math
L(x,\dot x)
=
k(x,\dot x)\dot x
-
\Omega\bigl(x,k(x,\dot x)\bigr).
```

Then

```math
\begin{aligned}
\frac{\partial L}{\partial\dot x}
&=
k
+
\left(
\dot x-\frac{\partial\Omega}{\partial k}
\right)
\frac{\partial k}{\partial\dot x}
\\
&=k,
\end{aligned}
```

and

```math
\begin{aligned}
\frac{\partial L}{\partial x}
&=
-\frac{\partial\Omega}{\partial x}
+
\left(
\dot x-\frac{\partial\Omega}{\partial k}
\right)
\frac{\partial k}{\partial x}
\\
&=
-\frac{\partial\Omega}{\partial x}.
\end{aligned}
```

The ordinary Euler--Lagrange equation

```math
\frac{d}{ds}
\frac{\partial L}{\partial\dot x}
-
\frac{\partial L}{\partial x}
=0
```

therefore becomes

```math
\dot k
+
\frac{\partial\Omega}{\partial x}
=0,
```

which is exactly the second stationary-phase equation above.
