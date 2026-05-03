Need a function that satisfies two props: 1. f(q,p) 2. encodes a vector field on phase space along which states will flow.

# The Hamiltonian
The function that encodes flow in phase space, the flow of state through time is the formulation's eponymous function, the Hamiltonian. Let's see how we can arrive at its form. 

## Functions on phase space
We have already see in our example of a incompressible fluid that any flow can be encoded by a generating function. Let's spell this out more carefully and put it in the arena of phase space.

Picture a contour map on the $q,p$ plane. The value of a function, $F(q(t),p(t))$, assigns a height to each point. This 3 dimensional "hilly" picture can, as with topographic maps, be represented in 2 dimensions with contours, or level sets. Now, we have a rule that the denser the level the sets are, equivalently, the steeper the surface is, the faster the flow along that contour. This flow can then be represented as a vector field, that is, a phase space velocity arrow at every point.

`[INSERT ANIMATION LATER: a scalar function on the q,p plane shown first as contours only, then with a small arrow attached at each point to indicate the induced flow.]`

The way to turn $F$'s level set density into such a vector field is:

```math
\dot q^i = \frac{\partial F}{\partial p_i},
\qquad
\dot p_i = -\frac{\partial F}{\partial q^i}.
```

One can work through this visually step by step to convince themselves it works, but the way it works can be thought of simply as taking the function gradient vector and turning it 90 degrees to create the flow. 

In phase space with one degree of freedom, if the vector field is

```math
\dot q = \frac{\partial F}{\partial p},
\qquad
\dot p = -\frac{\partial F}{\partial q},
```

then we can solve these differential equations for $q(t)$ and $p(t)$ to find the flow.

A trivial example is $F=p$. Then

```math
\dot q = 1,
\qquad
\dot p = 0.
```

And integrating gives

```math
q(t) = q_0 + t,
\qquad
p(t) = p_0.
```
We see in these cross-couple differential equations the shadow of the symplectic area preservation:

```math
\omega = dq^i \wedge dp_i
```

Change of $F$ in the $p_i$ direction determines motion in the $q^i$ direction. Change of $F$ in the $q^i$ direction determines motion in the $p_i$ direction, with a minus sign.

Let's show that such a flow does in fact preserve the symplectic 2-form. The quadrilateral may shear, stretch, or rotate, but its area must not change.

`[INSERT ANIMATION LATER: a small phase-space patch carried by the flow, changing shape while keeping the same area.]`



## next section
The vector field is the flow of time (one state to the next). from relativity, energy pairs with time to give action. so we may expect the function that encodes this flow is related to energy.

Now write Legendre transform

[codex:insert]

The basic Legendre transformation has the form

```math
p = \frac{df}{dx},
\qquad
g(p) = px - f(x),
```

with $x$ then understood as a function of $p$ if the first relation can be inverted.

In mechanics, the same move is made with respect to the velocity variables:

```math
p_i = \frac{\partial L}{\partial \dot q^i},
\qquad
H(q,p,t) = p_i\dot q^i - L(q,\dot q,t).
```

This is not yet the statement that $H$ is a function of $q$ and $p$ alone. It is the defining formula from which that statement will follow.

Then, show H is a function of q,p

[codex:insert]

The definition of momentum,

```math
p_i = \frac{\partial L}{\partial \dot q^i},
```

is an equation relating $q$, $\dot q$, $p$, and possibly $t$. If this can be inverted, then it allows us to solve for velocity as a function of phase-space variables:

```math
\dot q^i = \dot q^i(q,p,t).
```

Substituting this into the defining expression for the Hamiltonian gives

```math
H(q,p,t)
=
p_i\,\dot q^i(q,p,t)
-
L\big(q,\dot q(q,p,t),t\big).
```

Now every visible occurrence of $\dot q$ has been replaced by a function of $q$, $p$, and $t$, so $H$ genuinely lives on phase space.

Then define what a differential is

[codex: insert]

The differential of a function is its local first-order change rule. Geometrically, if a function is imagined as a surface, the differential is the infinitesimal tilt information at one point on that surface. It tells us how the function changes under a tiny displacement from that point.

For a function of two variables, this local change rule is written

```math
dH
=
\frac{\partial H}{\partial q^i}\,dq^i
+
\frac{\partial H}{\partial p_i}\,dp_i
+
\frac{\partial H}{\partial t}\,dt.
```

So the differential is not the full surface, and it is not yet the motion. It is the local linear data from which nearby change is read off.

Then analogize is to a gradient 

Then show that dH from H preserves EL dynamics

[codex: insert]

Start from the defining expression

```math
H(q,p,t) = p_i\dot q^i - L(q,\dot q,t).
```

Differentiate it:

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

Now use the definition

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

The $d\dot q^i$ terms cancel, leaving

```math
dH
=
\dot q^i\,dp_i
-
\frac{\partial L}{\partial q^i}\,dq^i
-
\frac{\partial L}{\partial t}\,dt.
```

Now use the Euler-Lagrange equations:

```math
\frac{d}{dt}\frac{\partial L}{\partial \dot q^i}
=
\frac{\partial L}{\partial q^i}.
```

Since $p_i=\partial L/\partial \dot q^i$, this becomes

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
-
\frac{\partial L}{\partial t}\,dt.
```

But because $H$ is now a function of $q$, $p$, and $t$, its differential is also

```math
dH
=
\frac{\partial H}{\partial q^i}\,dq^i
+
\frac{\partial H}{\partial p_i}\,dp_i
+
\frac{\partial H}{\partial t}\,dt.
```

Matching coefficients of the independent differentials $dq^i$ and $dp_i$ gives Hamilton's equations:

```math
\dot q^i = \frac{\partial H}{\partial p_i},
\qquad
\dot p_i = -\frac{\partial H}{\partial q^i}.
```

 
