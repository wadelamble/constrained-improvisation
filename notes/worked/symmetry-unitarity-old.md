
[Comment: this is all really unitarity and moves to the fourier structure section]

Suppose we could assign real exponential functions finite, positive squared lengths:

```math
\begin{gathered}
f_k(x)=e^{kx},\qquad g_l(x)=e^{lx},\qquad k,l\in\mathbb R,\\
0<\langle f_k,f_k\rangle<\infty,\qquad
0<\langle g_l,g_l\rangle<\infty.
\end{gathered}
```
The exponent can be, and in most of what we discuss, will be, imaginary. The mystery of $i^2=-1$ is less mysterious when we recall that the rotation operator in the two-dimensional representation had the same property:

```math
J^2=-I.
```

Under translation,

```math
(T_a f_k)(x)
=
f_k(x-a)
=
e^{-ka}f_k(x),
```

and

```math
(T_a g_l)(x)
=
g_l(x-a)
=
e^{-la}g_l(x).
```

Therefore

```math
\begin{aligned}
\langle T_a f_k,T_a f_k\rangle
&=e^{-2ka}\langle f_k,f_k\rangle,\\
\langle T_a g_l,T_a g_l\rangle
&=e^{-2la}\langle g_l,g_l\rangle.
\end{aligned}
```

Both squared lengths are preserved for every translation only when

```math
e^{-2ka}=e^{-2la}=1
\quad(\forall a\in\mathbb R)
\quad\Longleftrightarrow\quad k=l=0.
```

For real $k$ and $l$, this is not generally true. Thus nonconstant real exponentials are eigenfunctions of translation, but they are not compatible with translation as an inner-product-preserving symmetry. Complex exponentials encode circular motion, and, when acted upon by a translation symmetry operator, encode waves. Let's see how this works.
