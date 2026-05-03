# The Legendre Transform

Once the variables $(q,p)$ have been identified, the next task is to find the function on phase space that generates the physical time-evolution flow. The Lagrangian is not yet that function. It is written as

```math
L(q,\dot q),
```

so it still treats velocity as an independent variable. The function we want must instead be written on phase space:

```math
H(q,p).
```

The Legendre transform is the operation that performs this trade. It uses the momentum relation we have established:

```math
p_i = \frac{\partial L}{\partial \dot q^i}
```

to replace the velocity variables by their conjugate momenta, while carrying the position variables along. The transformed function is

```math
H(q,p) = p_i\dot q^i - L(q,\dot q),
```

with $\dot q$ understood, when possible, as a function of $(q,p,t)$ determined by the momentum equation above.

We can do quick test that $H$ is indeed the total energy by looking at a free particle.

For a non-relativistic free particle,

```math
L(q,\dot q) = \frac{1}{2}m\dot q^2.
```

The conjugate momentum is therefore

```math
p = \frac{\partial L}{\partial \dot q} = m\dot q,
```

so

```math
\dot q = \frac{p}{m}.
```

Substituting this into the Legendre transform gives

```math
H(q,p) = p\dot q - L(q,\dot q)
= p\left(\frac{p}{m}\right) - \frac{1}{2}m\left(\frac{p}{m}\right)^2
= \frac{p^2}{m} - \frac{p^2}{2m}
= \frac{p^2}{2m}.
```

But this is exactly the kinetic energy of the particle. So in this simplest case, the Legendre transform gives the energy function directly.

The importance of this construction is not only that it rewrites the function in the desired variables. In the earlier phase-space discussion, we saw what differential structure a function must have if it is to generate a flow. We now want to see that the Legendre-transformed function has exactly that structure. Taking the differential of $H$ gives

```math
dH
=
\dot q^i\,dp_i
+
p_i\,d\dot q^i
-
\frac{\partial L}{\partial q^i}\,dq^i
-
\frac{\partial L}{\partial \dot q^i}\,d\dot q^i
```

Now use the definition

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

The $d\dot q^i$ terms cancel. What remains is

```math
dH
=
\dot q^i\,dp_i
-
\frac{\partial L}{\partial q^i}\,dq^i
```

At this stage the transform has done its essential job. Velocity is no longer appearing as an independent differential. The theory has been rewritten in phase-space terms.

To connect this with the original dynamics, use the Euler-Lagrange equations:

```math
\frac{d}{dt}\frac{\partial L}{\partial \dot q^i}
=
\frac{\partial L}{\partial q^i}.
```

Since $p_i = \partial L/\partial \dot q^i$, this becomes

```math
\dot p_i = \frac{\partial L}{\partial q^i}.
```

Substituting this into the expression for $dH$ gives

```math
dH
=
\dot q^i\,dp_i
-
\dot p_i\,dq^i
```

But because $H$ is now a function of $(q,p)$, its differential is also

```math
dH
=
\frac{\partial H}{\partial q^i}\,dq^i
+
\frac{\partial H}{\partial p_i}\,dp_i
```

Matching coefficients then yields the actual point of Hamiltonian mechanics for solving classical physics problems, Hamilton's equations or motion:

```math
\dot q^i = \frac{\partial H}{\partial p_i},
\qquad
\dot p_i = -\frac{\partial H}{\partial q^i}.
```

We can check this works using the example of a simple harmonic oscillator.

The total energy, and thus the Hamiltonian is:

```math
H(q,p) = T + V = \frac{p^2}{2m} + \frac{1}{2}kq^2.
```

Hamilton's equations then give:

```math
\dot q = \frac{\partial H}{\partial p} = \frac{p}{m},
\qquad
\dot p = -\frac{\partial H}{\partial q} = -kq.
```

Using $p = m\dot q$, this becomes:

```math
m\ddot q = -kq,
```

or

```math
\ddot q + \frac{k}{m}q = 0.
```
```


