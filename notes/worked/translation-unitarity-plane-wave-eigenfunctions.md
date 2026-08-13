# From Translation Unitarity to Plane-Wave Eigenfunctions

Define translation of a function by

```math
(T_a f)(x)=f(x-a).
```

On square-integrable functions, use the inner product

```math
\langle f,g\rangle
=
\int_{-\infty}^{\infty}f^*(x)g(x)\,dx.
```

Translation preserves this inner product:

```math
\begin{aligned}
\langle T_a f,T_a g\rangle
&=
\int_{-\infty}^{\infty}
f^*(x-a)g(x-a)\,dx
\\
&=
\int_{-\infty}^{\infty}
f^*(u)g(u)\,du
\\
&=
\langle f,g\rangle,
\end{aligned}
```

where we substituted $u=x-a$. Translation is also reversible because

```math
T_{-a}T_a=I.
```

Thus $T_a$ is unitary: it is linear, preserves the inner product, and has an inverse.

Now let

```math
D=\frac{d}{dx}.
```

Since translating by $a$ shifts $f(x)$ to $f(x-a)$,

```math
T_a=e^{-aD}.
```

We now solve the differential eigenvalue equation

```math
Df=\lambda f.
```

Because $f$ is an eigenfunction of $D$, exponentiating $D$ gives

```math
T_a f
=
e^{-aD}f
=
e^{-a\lambda}f.
```

Thus $e^{-a\lambda}$ is the factor by which a finite translation scales this eigenfunction. Unitarity restricts that factor. Since $T_a$ preserves the norm,

```math
\begin{aligned}
\langle f,f\rangle
&=
\langle T_a f,T_a f\rangle
\\
&=
\left\langle e^{-a\lambda}f,e^{-a\lambda}f\right\rangle
\\
&=
\left|e^{-a\lambda}\right|^2
\langle f,f\rangle.
\end{aligned}
```

For a nonzero $f$, this requires

```math
\left|e^{-a\lambda}\right|=1.
```

The scaling factor may therefore change the phase of the eigenfunction, but its magnitude must remain one. Write

```math
\lambda=\alpha+ik,
```

where $\alpha$ and $k$ are real. Then

```math
\left|e^{-a\lambda}\right|
=
e^{-a\alpha}.
```

This equals one for every translation $a$ only when

```math
\alpha=0.
```

Therefore the eigenvalue of the derivative generator must be imaginary:

```math
\lambda=ik.
```

The differential eigenvalue equation is now

```math
\frac{df}{dx}=ikf,
```

whose solution is

```math
f_k(x)=Ce^{ikx}.
```

Under a finite translation,

```math
\begin{aligned}
(T_a f_k)(x)
&=
f_k(x-a)
\\
&=
Ce^{ik(x-a)}
\\
&=
e^{-ika}f_k(x).
\end{aligned}
```

The eigenfunction retains its form and acquires only a phase. The complete chain is therefore

```math
\text{translation preserves the inner product}
\Longrightarrow
T_a\text{ is unitary}
\Longrightarrow
\lambda=ik
\Longrightarrow
f_k(x)=Ce^{ikx}.
```

Equivalently, defining the self-adjoint generator

```math
\hat K=-iD=-i\frac{d}{dx}
```

gives the real eigenvalue equation

```math
\hat K f_k=kf_k,
```

and

```math
T_a=e^{-ia\hat K}.
```

On the full real line, individual plane waves are generalized eigenfunctions rather than square-integrable vectors. Square-integrable wave packets are formed from their superpositions. The same calculation can be made fully literal in a finite periodic interval and then extended to the real line.
