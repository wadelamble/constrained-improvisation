# From the canonical commutator to the uncertainty relation

In quantum mechanics, $|\psi(x)|^2$ and $|\widetilde\psi(k)|^2$ are the position and wave-number probability densities. Normalize them:

```math
\|\psi\|^2
=
\int_{-\infty}^{\infty}|\psi(x)|^2\,dx
=
\int_{-\infty}^{\infty}|\widetilde\psi(k)|^2\,dk
=1.
```

Normalization is needed for their widths to be standard deviations.

Define

```math
(\Delta x)^2
=
\int_{-\infty}^{\infty}x^2|\psi(x)|^2\,dx,
\qquad
(\Delta k)^2
=
\int_{-\infty}^{\infty}k^2|\widetilde\psi(k)|^2\,dk.
```

In the position representation,

```math
(\hat X\psi)(x)=x\psi(x),
\qquad
(\hat K\psi)(x)=-i\frac{d\psi}{dx},
```

so

```math
(\Delta x)^2=\|\hat X\psi\|^2,
\qquad
(\Delta k)^2=\|\hat K\psi\|^2.
```

Now use

```math
[\hat X,\hat K]=iI.
```

A squared norm cannot be negative:

```math
\begin{aligned}
0
&\le
\left\|
\left(
\frac{\hat X}{\Delta x}
+i\frac{\hat K}{\Delta k}
\right)\psi
\right\|^2
\\
&=
\frac{\|\hat X\psi\|^2}{(\Delta x)^2}
+
\frac{\|\hat K\psi\|^2}{(\Delta k)^2}
+
\frac{i\langle\psi,[\hat X,\hat K]\psi\rangle}
{\Delta x\,\Delta k}
\\
&=
2-
\frac{1}{\Delta x\,\Delta k}.
\end{aligned}
```

Therefore

```math
\boxed{
\Delta x\,\Delta k\ge\frac12.
}
```

Equality requires the squared norm above to vanish:

```math
\left(
\frac{\hat X}{\Delta x}
+i\frac{\hat K}{\Delta k}
\right)\psi=0.
```

Using $\Delta k=1/(2\Delta x)$, this becomes

```math
\frac{d\psi}{dx}
=
-\frac{x}{2(\Delta x)^2}\psi.
```

A normalized solution is

```math
\psi(x)
=
\frac{1}{[2\pi(\Delta x)^2]^{1/4}}
\exp\!\left[-\frac{x^2}{4(\Delta x)^2}\right].
```

For this Gaussian,

```math
\|\hat K\psi\|^2
=
\frac{1}{4(\Delta x)^4}\|\hat X\psi\|^2
=
\frac{1}{4(\Delta x)^2},
```

so $\Delta k=1/(2\Delta x)$ and

```math
\boxed{
\Delta x\,\Delta k=\frac12.
}
```

The commutator therefore fixes $1/2$ as the minimum possible product, reached by a Gaussian.
