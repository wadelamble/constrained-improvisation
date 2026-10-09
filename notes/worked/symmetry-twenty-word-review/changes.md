# Changes under the 40-word prose budget

Original: `content/drafts/symmetry-draft-shorter-intro.md`
Copy: `content/drafts/symmetry-draft-shorter-intro-critic-copy.md`

Equation corrections are excluded by the author’s instruction. Counts are cumulative across passes.

## Pass 1

Prose cost: 20.

### Prose — cost 4

```diff
- in simple cases, proportional
+ in free motion, proportional
```

### Prose — cost 6

```diff
- a single-mode plane wave in spacetime is:
+ a single-mode plane wave along its inertial worldline is:
```

### Prose — cost 4

```diff
- sufficient to serve
+ useful
```

### Prose — cost 4

```diff
- in quantum mechanics, a measurement always results
+ in quantum mechanics, an ideal measurement results
```

### Prose — cost 2

```diff
- an "electron" is a specific irreducible representation
+ an "electron" inhabits a specific irreducible representation
```

### Equation — cost 0

```diff
- \hat K
- =
- -
- \frac{d}{dx}.
+ -i\hat K
+ =
+ -
+ \frac{d}{dx},
+ \qquad
+ \hat K=-i\frac{d}{dx},
+ \qquad
+ T_a=e^{-ia\hat K}.
```

### Equation — cost 0

```diff
- [L_x,L_y]=L_z
+ L_i=i\hbar J_i,
+ \qquad
+ [L_x,L_y]=i\hbar L_z
```

### Equation — cost 0

```diff
- &=-L_yL_z-L_zL_y+L_zL_y+L_yL_z\\
+ &=i\hbar(-L_yL_z-L_zL_y+L_zL_y+L_yL_z)\\
```

### Equation — cost 0

```diff
- S = -m\tau
+ S = -m\tau \qquad(c=1)
```

### Equation — cost 0

```diff
- (T_x(a)\psi_{k_0})(x)
- =
- \psi_{k_0}(x-a).
+ (T_x(a)\psi_{k_0})(x)
+ =
+ \left(e^{-ia\hat K}\psi_{k_0}\right)(x)
+ =
+ \psi_{k_0}(x-a).
```

### Equation — cost 0

```diff
- e^{-ib(x+a)}e^{i(k_0+b)x}
- =
- e^{-iab}\psi_{k_0}(x).
+ e^{-ib(x+a)}e^{i(k_0+b)x}
+ =
+ e^{-ab[\hat X,\hat K]}\psi_{k_0}(x)
+ =
+ e^{-iab}\psi_{k_0}(x).
```

### Equation — cost 0

```diff
- [\hat X,\hat K]=iI,
- \qquad
- [\hat X,I]=[\hat K,I]=0.
+ [i\hat X,-i\hat K]=iI,
+ \qquad
+ [i\hat X,iI]=[-i\hat K,iI]=0.
```

## Pass 2

Prose cost: 20.

### Prose — cost 4

```diff
- generalized eigenbasis
+ translation eigenfunctions
```

### Prose — cost 5

```diff
- for the case of real exponentials
+ on the span of nonconstant real exponentials
```

### Prose — cost 2

```diff
- It is the property that ensures different states remain
+ It is a property that ensures different states remain
```

### Prose — cost 1

```diff
- remain *distinguishable*
+ remain equally *distinguishable*
```

### Prose — cost 2

```diff
- and that those transformations are *reversible*. Let
+ and that those transformations are *reversible*. Suppose
```

### Prose — cost 1

```diff
- Thus real exponentials are eigenfunctions of translation
+ Thus nonconstant real exponentials are eigenfunctions of translation
```

### Prose — cost 2

```diff
- is the tangent line to that function
+ is the tangent slope to that function
```

### Prose — cost 2

```diff
- The answer is that $i$ has two real-number degrees of freedom.
+ The answer is that $z$ has two real-number degrees of freedom.
```

### Prose — cost 1

```diff
- provide a minimal set of transformations
+ provide a set of transformations
```

### Equation — cost 0

```diff
- f_k(x)=e^{kx},
- \qquad
- g_l(x)=e^{lx}.
+ \begin{gathered}
+ f_k(x)=e^{kx},\qquad g_l(x)=e^{lx},\qquad k,l\in\mathbb R,\\
+ 0<\langle f_k,f_k\rangle<\infty,\qquad
+ 0<\langle g_l,g_l\rangle<\infty.
+ \end{gathered}
```

### Equation — cost 0

```diff
- \langle T_a f_k,T_a g_l\rangle
- =
- e^{-(k+l)a}
- \langle f_k,g_l\rangle.
+ \begin{aligned}
+ \langle T_a f_k,T_a f_k\rangle
+ &=e^{-2ka}\langle f_k,f_k\rangle,\\
+ \langle T_a g_l,T_a g_l\rangle
+ &=e^{-2la}\langle g_l,g_l\rangle.
+ \end{aligned}
```

### Equation — cost 0

```diff
- e^{-(k+l)a}=1.
+ e^{-2ka}=e^{-2la}=1
+ \quad(\forall a\in\mathbb R)
+ \quad\Longleftrightarrow\quad k=l=0.
```

