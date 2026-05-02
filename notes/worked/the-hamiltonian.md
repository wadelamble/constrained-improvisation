# The Hamiltonian

Once the variables $(q,p)$ have been identified, the next task is not merely to rename the Lagrangian. The Lagrangian is a function on configuration and velocity. It evaluates possible motions through configuration space. Hamiltonian mechanics needs a different kind of object. It needs a function on phase space whose differential tells an instantaneous state how to move.

This is the reason a transformation is needed. We have learned from the boundary term that $p_i$ is the quantity paired with $q^i$ in the first-order variation of the action. The state variables are therefore $(q,p)$ rather than $(q,\dot q)$. But the Lagrangian is still written as

```math
L(q,\dot q,t).
```

To build mechanics on phase space, we need a function written as

```math
H(q,p,t).
```

That requirement is not only a change of notation. Velocity should no longer be an independent coordinate of the state. It may reappear, but only as something computed from the phase-space law. In Hamiltonian mechanics, $\dot q$ is not supplied as part of the state. It is recovered from the Hamiltonian.

The Legendre transform is the operation that performs this trade. It replaces the velocity variable $\dot q^i$ by its conjugate momentum

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

The position variables $q^i$ are not transformed. They are carried along. The transform is taken only with respect to the velocity variables. The resulting function is

```math
H(q,p,t) = p_i\dot q^i - L(q,\dot q,t),
```

where $\dot q$ is understood, when possible, as the function of $(q,p,t)$ determined by

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

The point of this construction is not that it looks clever. The point is that it removes $\dot q$ as an independent differential. Start from

```math
H = p_i\dot q^i - L.
```

Taking the differential gives

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
-
\frac{\partial L}{\partial t}\,dt.
```

Now use the definition of conjugate momentum:

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

The two $d\dot q^i$ terms cancel. This is the key algebraic fact. The transform works because it follows the pairing already discovered in the boundary variation. What remains is

```math
dH
=
\dot q^i\,dp_i
-
\frac{\partial L}{\partial q^i}\,dq^i
-
\frac{\partial L}{\partial t}\,dt.
```

At this point the theory has been moved onto phase space. The differential of $H$ is expressed in terms of $dq^i$, $dp_i$, and $dt$, not $d\dot q^i$. Velocity has not disappeared from physics. It has changed status. It is no longer an input variable of the state.

To see the equations of motion, bring in the Euler-Lagrange equation:

```math
\frac{d}{dt}\frac{\partial L}{\partial \dot q^i}
=
\frac{\partial L}{\partial q^i}.
```

Since $p_i=\partial L/\partial \dot q^i$, this says

```math
\dot p_i
=
\frac{\partial L}{\partial q^i}.
```

Substituting into the differential gives

```math
dH
=
\dot q^i\,dp_i
-
\dot p_i\,dq^i
-
\frac{\partial L}{\partial t}\,dt.
```

But if $H$ is a function of $(q,p,t)$, its differential is also

```math
dH
=
\frac{\partial H}{\partial q^i}\,dq^i
+
\frac{\partial H}{\partial p_i}\,dp_i
+
\frac{\partial H}{\partial t}\,dt.
```

Matching the coefficients of $dq^i$ and $dp_i$ gives Hamilton's equations:

```math
\dot q^i
=
\frac{\partial H}{\partial p_i},
\qquad
\dot p_i
=
-
\frac{\partial H}{\partial q^i}.
```

This is the payoff. The Legendre transform does not merely produce a new function of new variables. It produces the function whose differential packages the same dynamics as first-order evolution on phase space. The original Lagrangian theory selected whole paths by extremizing action. The Hamiltonian theory gives a local rule for how an instantaneous state moves.

In familiar conservative systems, the Hamiltonian is the total energy. For example, if

```math
L(q,\dot q)
=
\frac{1}{2}m\dot q^2 - V(q),
```

then

```math
p = m\dot q,
\qquad
\dot q = \frac{p}{m},
```

and

```math
H(q,p)
=
p\dot q - L
=
\frac{p^2}{2m}+V(q).
```

So in this standard case the Hamiltonian is kinetic energy plus potential energy. That is why it is tempting to introduce $H$ simply as "the energy." But for the logic of Hamiltonian mechanics, energy is not the best starting definition. The deeper fact is that $H$ is the phase-space function whose differential generates the motion. Energy is the familiar face this function has in ordinary conservative systems.

This also explains why level sets of $H$ matter. If $H$ has no explicit time dependence, then along a Hamiltonian trajectory

```math
\frac{dH}{dt}
=
\frac{\partial H}{\partial q^i}\dot q^i
+
\frac{\partial H}{\partial p_i}\dot p_i.
```

Using Hamilton's equations,

```math
\frac{dH}{dt}
=
\frac{\partial H}{\partial q^i}
\frac{\partial H}{\partial p_i}
+
\frac{\partial H}{\partial p_i}
\left(
-
\frac{\partial H}{\partial q^i}
\right)
=
0.
```

So when $H$ does not depend explicitly on time, the motion stays on a surface of constant Hamiltonian. In the ordinary energy case, this is conservation of energy. Geometrically, it means that the Hamiltonian organizes phase space into level sets, and the dynamics flows along them rather than across them.

This is where the static geometry of phase space begins to turn into a movie. A point $(q,p)$ is an exact instantaneous state. Hamilton's equations give the velocity of that point in phase space. A collection of nearby initial states becomes a moving patch. The next question is not merely where one point goes, but what happens to the patch. That is the question Liouville's theorem answers.

