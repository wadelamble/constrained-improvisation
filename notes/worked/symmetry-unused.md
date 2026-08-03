

### attempts at eigenbasis
[=move]
Both real and imaginary exponential functions can function as an eigenbasis, but one of our directions of translational symmetry is time, and time being the symmetry with respect to which we understand the concept of identity -- an identity is, by definition, preserved over time -- our physical representation of translation must make stronger restrictions than the preservation of metric length. Not only must we be able to measure distances between events, but we must also be able to distinguish the identity of states -- expressed as functions -- over time translation.

Complex exponentials provide this. For complex-valued functions on an interval, the measure that is preserved is not the dot product but the complex inner product, a generalized dot product. This is defined as:

```math
\langle f,g\rangle
=
\int_a^b f^*(x)g(x)\,dx.
```

Here $f^*(x)$ is the complex conjugate of $f(x)$. For the function's length, or norm, we set $g=f$:

```math
\langle f,f\rangle
=
\int_a^b |f(x)|^2\,dx.
```

The complex inner product returns a complex number, and any complex number has a real and imaginary part:

```math
\langle f,g\rangle
=
\operatorname{Re}\langle f,g\rangle
+
i\,\operatorname{Im}\langle f,g\rangle.
```

These two parts carry two different structures. The metric part is the real part:

```math
G(f,g)
=
\operatorname{Re}\langle f,g\rangle.
```

This behaves like a generalized dot product. In particular,

```math
G(f,f)
=
\operatorname{Re}\langle f,f\rangle
=
\int_a^b |f(x)|^2\,dx.
```

So it gives length, or norm. The symplectic part is the imaginary part:

```math
\Omega(f,g)
=
\operatorname{Im}\langle f,g\rangle.
```

This is antisymmetric:

```math
\Omega(g,f)
=
-
\Omega(f,g).
```

So the complex inner product contains both structures:

```math
\langle f,g\rangle
=
G(f,g)
+
i\Omega(f,g).
```

Unitarity means preserving the whole complex inner product:

```math
\langle Uf,Ug\rangle
=
\langle f,g\rangle.
```

Therefore it preserves both parts:

```math
G(Uf,Ug)
=
G(f,g),
\qquad
\Omega(Uf,Ug)
=
\Omega(f,g).
```

The metric component of this invariance allows us to measure distances and angles in space. The area component, or the **symplectic form** says 

[=endmove]

## CCR and Action Variation

Work in one spatial dimension and consider a uniform system, so the frequency depends only on the wave number:

```math
\omega=\omega(k).
```

A proposed history of a localized wave packet is a path

```math
t\longmapsto \bigl(x(t),k(t)\bigr).
```

Here $x(t)$ is the packet's location, $k(t)$ is its central wave number, and

```math
\dot x
=
\frac{dx}{dt}
```

is the packet's velocity.

The phase/action assigned to this path is

```math
S[x,k]
=
\int_{t_i}^{t_f}
\left(
k\dot x-\omega(k)
\right)dt.
```

Equivalently, because $dx=\dot x\,dt$,

```math
S[x,k]
=
\int
\left(
k\,dx-\omega\,dt
\right).
```

The term $k\,dx$ is phase accumulated through displacement in position, while $-\omega\,dt$ is phase accumulated through temporal evolution. We are writing action in phase units, so the corresponding wave factor is $e^{iS}$.

### Varying the path

To vary the action, replace the proposed histories by nearby ones:

```math
x(t)
\longrightarrow
x(t)+\varepsilon\,\delta x(t),
\qquad
k(t)
\longrightarrow
k(t)+\varepsilon\,\delta k(t).
```

We seek a path for which the first-order change in $S$ vanishes for every small deformation $\delta x(t)$ and $\delta k(t)$.

First vary $k(t)$ while holding $x(t)$ fixed:

```math
\delta_k S
=
\int
\left[
\dot x\,\delta k
-
\frac{d\omega}{dk}\delta k
\right]dt.
```

Factoring out $\delta k$ gives

```math
\delta_k S
=
\int
\left(
\dot x-\frac{d\omega}{dk}
\right)\delta k\,dt.
```

Because $\delta k(t)$ can be chosen independently at every time, this can vanish for every variation only if

```math
\dot x
=
\frac{d\omega}{dk}.
```

Thus the packet moves at the group velocity $d\omega/dk$.

Now vary $x(t)$ while holding $k(t)$ fixed. Only $\dot x$ changes:

```math
\delta_x S
=
\int k\,\delta\dot x\,dt
=
\int k\frac{d}{dt}\delta x\,dt.
```

Integrating by parts gives

```math
\delta_x S
=
\left[k\,\delta x\right]_{t_i}^{t_f}
-
\int\dot k\,\delta x\,dt.
```

The original and varied paths are required to have the same endpoints, so

```math
\delta x(t_i)
=
\delta x(t_f)
=
0.
```

The endpoint term therefore vanishes:

```math
\delta_x S
=
-
\int\dot k\,\delta x\,dt.
```

Because $\delta x(t)$ is otherwise arbitrary,

```math
\dot k
=
0.
```

The stationary path therefore satisfies

```math
k(t)
=
k_0,
\qquad
x(t)
=
x_0
+
\omega'(k_0)t.
```

This is the trajectory followed by the center of the localized wave packet. It is not a ray in the projective-Hilbert-space sense. A projective Hilbert ray is an equivalence class of wavefunctions that differ only by global phase. The path above contains only the packet's location and central wave number and therefore carries much less information than the complete wavefunction.

### Where the curvature enters the variation

The curvature enters precisely when the original path is compared with the varied path.

The paths share the same endpoints. Travel forward along the original path and backward along the varied path: together they form a very thin closed loop in $x$-$k$ space. The difference between their actions is the phase accumulated around this loop.

At each time, the motion along the original path,

```math
\bigl(\dot x,\dot k\bigr)dt,
```

and the displacement toward the neighboring path,

```math
\bigl(\delta x,\delta k\bigr),
```

span a tiny parallelogram. The phase assigned to that parallelogram is

```math
\dot x\,\delta k
-
\dot k\,\delta x.
```

This appears directly in the variation:

```math
\delta\int k\,dx
=
\int
\left(
\dot x\,\delta k
-
\dot k\,\delta x
\right)dt.
```

In geometric notation, this is the area form

```math
dk\wedge dx
```

evaluated on the direction of the path and the direction of its variation:

```math
(dk\wedge dx)
\left(
(\delta x,\delta k),
(\dot x,\dot k)
\right)
=
\delta k\,\dot x
-
\dot k\,\delta x.
```

Thus varying a path automatically constructs infinitesimal closed loops between that path and its neighbors. The phase curvature determines the action difference around those loops, so it enters directly into the first variation of the action.

The change in the other part of the action, $-\omega\,dt$, must cancel this curvature-generated change:

```math
\delta S
=
\int
\left[
\left(
\dot x-\frac{d\omega}{dk}
\right)\delta k
-
\dot k\,\delta x
\right]dt
=
0.
```

This cancellation gives

```math
\dot x
=
\frac{d\omega}{dk},
\qquad
\dot k
=
0.
```

### The commutator and the curvature

The canonical commutator is

```math
[X,K]
=
iI.
```

Its exponentiated form says that translating by $a$ in $x$, then by $b$ in $k$, and then undoing both translations returns to the same point in $x$-$k$ space but adds a phase:

```math
T(a)M(b)T(-a)M(-b)
=
e^{-iab}I.
```

For the corresponding rectangular loop,

```math
\oint k\,dx
=
-ab,
```

so

```math
e^{i\oint k\,dx}
=
e^{-iab}.
```

The commutator is therefore the operator statement that the $x$-$k$ plane carries constant phase curvature. More precisely, the commutator fixes the curvature

```math
F
=
dk\wedge dx.
```

To write the action, we choose a local phase potential whose derivative is this curvature. One convenient choice is

```math
\alpha
=
k\,dx,
\qquad
d\alpha
=
dk\wedge dx.
```

The choice is not unique. For example,

```math
\alpha'
=
-x\,dk
```

has the same curvature. The two choices differ by a total differential:

```math
k\,dx
-
(-x\,dk)
=
d(xk).
```

They therefore give the same closed-loop phases and the same variational equations when the endpoints are fixed.

The $x$-$k$ plane itself is flat. The nonzero curvature belongs to the phase connection defined over that plane, not to the plane's metric geometry. Moreover, the curvature is uniform:

```math
[X,K]
=
iI
```

has the same value everywhere, so equal-area loops produce equal phase advances wherever they are placed. This is a local $U(1)$ phase structure over phase space, distinct from electromagnetic gauge symmetry over spacetime.

### From the action phase to the whole wave

Varying $S[x,k]$ gives the trajectory of the packet's center. To recover the evolution of the whole wave, use $S$ as a phase rather than retaining only the stationary path.

For one short interval $\Delta t$, suppose the position changes from $x$ to $x'$. Then

```math
\dot x
\approx
\frac{x'-x}{\Delta t},
```

and the action for that step is

```math
\begin{aligned}
S_{\Delta t}
&=
\left(
k\dot x-\omega(k)
\right)\Delta t
\\
&=
k(x'-x)-\omega(k)\Delta t.
\end{aligned}
```

Write the wave in its Fourier decomposition:

```math
\psi(x,t)
=
\int\frac{dk}{2\pi}\,
\widetilde\psi(k,t)e^{ikx}.
```

During $\Delta t$, each $k$-component acquires the temporal phase determined by its frequency:

```math
\widetilde\psi(k,t+\Delta t)
=
e^{-i\omega(k)\Delta t}
\widetilde\psi(k,t).
```

Transforming back to the $x$-representation gives

```math
\psi(x',t+\Delta t)
=
\int\frac{dk}{2\pi}\,
e^{ikx'}
e^{-i\omega(k)\Delta t}
\widetilde\psi(k,t).
```

The initial Fourier coefficient is

```math
\widetilde\psi(k,t)
=
\int dx\,
e^{-ikx}\psi(x,t).
```

Substituting this expression gives

```math
\psi(x',t+\Delta t)
=
\int dx\,\frac{dk}{2\pi}\,
e^{\,i[k(x'-x)-\omega(k)\Delta t]}
\psi(x,t).
```

Because the exponent is precisely $S_{\Delta t}$,

```math
\psi(x',t+\Delta t)
=
\int dx\,\frac{dk}{2\pi}\,
e^{iS_{\Delta t}}
\psi(x,t).
```

Thus $e^{iS_{\Delta t}}$ is exactly the Fourier phase that propagates the wave through one short time step.

In $k$-space,

```math
\widetilde\psi(k,t+\Delta t)
=
e^{-i\omega(k)\Delta t}
\widetilde\psi(k,t).
```

Expanding the exponential gives

```math
e^{-i\omega(k)\Delta t}
=
1
-
i\omega(k)\Delta t
+
O(\Delta t^2).
```

Therefore

```math
i\partial_t\widetilde\psi(k,t)
=
\omega(k)\widetilde\psi(k,t).
```

Fourier transformation turns multiplication by $k$ into differentiation with respect to $x$:

```math
k
\longleftrightarrow
-i\partial_x.
```

Consequently,

```math
\omega(k)
\longleftrightarrow
\omega(-i\partial_x),
```

and the position-space wave equation is

```math
i\partial_t\psi(x,t)
=
\omega(-i\partial_x)\psi(x,t).
```

Repeating the short-time Fourier step introduces integrations over every intermediate $x$ and $k$. The product of the short-time phases becomes

```math
\exp
\left[
i\sum_j
\left(
k_j(x_{j+1}-x_j)
-
\omega(k_j)\Delta t
\right)
\right].
```

In the continuous limit, the sum in the exponent becomes

```math
S[x,k]
=
\int
\left(
k\,dx-\omega\,dt
\right).
```

The sum over paths is therefore repeated Fourier decomposition in time. Histories for which the phase changes rapidly tend to cancel one another. Near a history satisfying $\delta S=0$, neighboring phases change only to second order and reinforce. This is why the stationary path follows the packet's center while the full phase sum evolves the entire wave.

### Where the CCR was used

The commutator was already present when the action was written with the canonical term $k\,dx$. That term is a phase potential for the curvature fixed by

```math
[X,K]
=
iI.
```

The commutator appears again in the Fourier calculation. In the $x$-representation,

```math
X
=
x,
\qquad
K
=
-i\partial_x,
```

which satisfies

```math
[X,K]
=
iI.
```

The $K$-eigenfunctions obey

```math
-i\partial_x\langle x|k\rangle
=
k\langle x|k\rangle,
```

and therefore

```math
\langle x|k\rangle
\propto
e^{ikx}.
```

Thus both the Fourier kernel

```math
e^{ik(x'-x)}
```

and the replacement

```math
k
\longrightarrow
-i\partial_x
```

are the canonical commutator represented in the $x$-basis.

The resulting chain is:

```math
[X,K]=iI
\quad\Longleftrightarrow\quad
\text{constant phase curvature in }x\text{-}k
```

```math
\Longrightarrow
\quad
S[x,k]
=
\int
\left(
k\,dx-\omega\,dt
\right)
```

```math
\Longrightarrow
\quad
e^{iS}
\text{ gives the exact Fourier evolution}
```

```math
\Longrightarrow
\quad
i\partial_t\psi
=
\omega(-i\partial_x)\psi.
```

Meanwhile,

```math
\delta S
=
0
```

extracts the trajectory of the packet center from that full wave evolution.

If one instead wants to obtain the whole wave equation directly by variation, one uses a different action: an action whose variable is the complete wavefunction rather than the two functions $x(t)$ and $k(t)$:

```math
\mathcal S[\psi,\psi^*]
=
\int dt\,dx\,
\psi^*
\left[
i\partial_t
-
\omega(-i\partial_x)
\right]\psi.
```

Varying $\psi^*$ gives

```math
i\partial_t\psi
=
\omega(-i\partial_x)\psi.
```

This whole-wave action packages the same operator evolution into a variational form. It should not be confused with varying the phase-space path action $S[x,k]$, which produces the packet-center trajectory.

## phase energy dispersion ...


....curvature expresses through the commutator?...the metric??....





Once we associate $k$ and $\omega$ with momentum and energy, this phase places spatial and temporal translation in a single structure. The **dispersion relation** $\omega=\omega(\mathbf k)$ then tells us how quickly each spatial Fourier component accumulates phase in time and therefore how a wave packet spreads as it travels. Replacing $k$ and $\omega$ by their translation generators converts the dispersion relation directly into a wave equation.

All that is left to do to determine how unfolding in time relates to freely unfolding in space, that is, how energy determines momentum is to establish the dispersion relation. but for a free system, as we will soon show when discussing spacetime geometry is nothing more than:

```math
\omega^2
=
\omega_0^2+c^2\lvert\mathbf k\rvert^2,
\qquad
\omega(\mathbf k)
=
\sqrt{\omega_0^2+c^2\lvert\mathbf k\rvert^2},
```

where $\omega_0$ is the rest-frequency constant associated with mass.

## states and operators
Here the vector is the **state** of the triangly thing, and the matrix is the **operator** on that state. Why should we use such general-sounding terms when we already have the perfectly well-defined terms "vector" and "matrix"? As we will see soon, we will make use of representation spaces comprised of functions. A function can be treated as an infinite-dimensional vector, with its input values serving like labels for components. A "matrix" that "operates" on this infinite-dimensional vector can be captured in a single symbol. The canonical example is the derivative operator, $d/dx$, which maps a whole function $f(x)$ to a new function $f'(x)$. Calling $d/dx$ a matrix is a bit awkward, so we use the term "operator." But beyond this, a given "state" in reality may be represented in a variety of interchangeable ways. The phrasing that an "operator" acts on a "state" serves to provide a representation-independent vocabulary. But if the words feel abstract, one can always ground them in the framing that a "matrix" acts on a "vector."

## triangle invariants
In our 2-dimensional irrep of $D_3$, we only need to check how a transformation acts on a single vector. The question "does the triangle overlay itself" becomes "is an arbitrary vector rotated by 120 degrees or flipped along a given axis." Let's pick a specific example to make this more concrete:

Rotation:
$$
\begin{bmatrix}
-2.2\\
-0.1
\end{bmatrix}
=
\begin{bmatrix}
\cos(120^\circ) & -\sin(120^\circ)\\
\sin(120^\circ) & \cos(120^\circ)
\end{bmatrix}
\begin{bmatrix}
1\\
2
\end{bmatrix}
$$

Choosing the \(x\)-axis, flip:
$$
\begin{bmatrix}
1\\
-2
\end{bmatrix}
=
\begin{bmatrix}
1 & 0\\
0 & -1
\end{bmatrix}
\begin{bmatrix}
1\\
2
\end{bmatrix}
$$

These transformations have two invariants. First, because they are a subclass of rotations and flips generally, they leave the distance to the origin unchanged:

\(r^2=x^2+y^2\)

Then, to limit rotations to 120 degrees and flips to those about the three axes implied by an equilateral triangle, we have an additional invariant:

\(u=x^3-3xy^2\)

It's not hard to show this is the case using the example transformations above, but in the interest of not boring the reader, we will skip it. 

When we move on to deal with symmetries we encounter in physics, the invariants typically turn out to be simpler than this because the symmetries are less restrictive. Specifically, the invariants we will use are variations on the distance invariant above. 

In physics, invariants do more than provide a way to check that a transformation represents an element of a group action. Physics is about finding equations of motion that all observers separated by a symmetry transformation, that is, observers at different places, times, orientations, or velocities, agree on. A way to find these equations, as we will see later, is to build them from invariant quantities of the symmetry action.

### juicy bits from previous go-around
1. A general principle of geometry is that everything is flat when you zoom in far enough. Since "infinitesimal" is fully zoomed in, such a rotation is "flat," that is, it is a tangent vector.
2. As every calculus student learns, the tangent vector of any function is the derivative of the function. Thus the tangent is ...
3. it does into momentum and space quotients. not sure we want all that here.

### quick flow
generators / operators?  -> example for 2d rotation in 2d rep (is this an irrep) -> translations -> need for function reps

### taking limit to get R(theta) diff eq

For a tiny additional rotation $\Delta\theta$,

```math
\mathbf v(\theta+\Delta\theta)
=
\mathbf v(\theta)
+
\Delta\theta\,J\mathbf v(\theta)
+
O(\Delta\theta^2).
```

Subtract $\mathbf v(\theta)$ and divide by $\Delta\theta$:

```math
\frac{
\mathbf v(\theta+\Delta\theta)
-
\mathbf v(\theta)
}
{\Delta\theta}
=
J\mathbf v(\theta)
+
O(\Delta\theta).
```

Now take the limit as $\Delta\theta\to 0$:

```math
\frac{d\mathbf v}{d\theta}
=
J\mathbf v.
```


#### Euler Identity
:::: details Euler identity derivation

Show

```math
e^{i\pi}=-1.
```

Start by defining constants:

```math
i:\quad i^2=-1
```

```math
\pi:\quad C=2\pi r
```

```math
e:\quad \frac{de^x}{dx}=e^x
```

Next, describe the geometric action of multiplication by $i$:

```math
iz
=
i(x+iy)
=
ix+i^2y
=
-y+ix.
```

This says

```math
(x,y)\mapsto(-y,x),
```

which is a $90$ degree rotation, e.g.

![Euler identity derivation sketches](diagrams/symmetry-euler-identity-derivation.png)

Next, note that if we consider a unit circle in the complex plane, we can represent

```math
z(x,y)\rightarrow z(\theta).
```

Next, note that $dz/d\theta$, which is the tangent vector, equals the point it is tangent to rotated by $90$ degrees.

Since $dz/d\theta$ is a rotation by $90$ degrees, we have:

```math
\frac{dz}{d\theta}
=
iz(\theta).
```

The well-known solution to this differential equation is:

```math
z(\theta)=e^{i\theta}.
```

We can check this directly:

```math
\frac{dz}{d\theta}
=
\frac{d}{d\theta}e^{i\theta}
=
ie^{i\theta}
=
iz.
```

Next, from $C=2\pi r$, we know the circumference of the unit circle is $2\pi$, and half is $\pi$.

Now,

```math
-1+0i=-1,
```

thus:

```math
e^{i\pi}=-1.
```

::::
[wording all bad in hurry, also may move until we get to function reps]

## Topology
We should say that there is some global structure, the **topology**, that remains invisible to the local generators and commutators. For example, translation in $x$ and $y$ commute (moving in $x$ then $y$ is the same as $y$ then $x$), but this is true both on the surface of a plane and a cylinder, which have different global behavior: on a cylinder, a translation may return a point back to its starting point. This is familiar to anyone who has played Asteroids.

![A cylinder unrolls into an arcade-style wraparound plane](animations/symmetry-cylinder-topology-wrap-contact-sheet.png)

[Open MP4: symmetry-cylinder-topology-wrap.mp4](animations/symmetry-cylinder-topology-wrap.mp4)

### commutator exponential map identity
The generators and commutators together determine any transformation in the complete symmetry group.

Using the commutator we can generate composed actions. That is:


```math
e^{aX}e^{bY}
=
e^{aX+bY+\frac12ab[X,Y]+\cdots}.
```

This identity comes from using the definition of the commutator and Taylor expanding the exponentials. We will spare the reader the algebra.

