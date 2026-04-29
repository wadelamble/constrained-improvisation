## 8. The role of the Legendre transform

Once $p_i = \partial L / \partial \dot q^i$ has been selected, the next question is not what momentum is, but how to rewrite the theory in terms of $q$ and $p$ rather than $q$ and $\dot q$. That is, how do we replace velocity by momentum as one of the variables describing the state, without losing any of the dynamics?

That is the role of the Legendre transform.

The best way to understand it is to start with the simplest possible case and only then return to mechanics.

### One variable

Suppose we have an ordinary one-variable function

```math
f(q).
```

Here $q$ is just an input variable. The derivative

```math
\frac{df}{dq}
```

tells us how fast $f$ changes when $q$ changes. It is the slope of the graph of $f$ as a function of $q$.

The Legendre transform begins by introducing a new variable equal to that slope:

```math
p = \frac{df}{dq}.
```

The idea is that instead of describing the function in terms of the original variable $q$, we would like to describe it in terms of the slope variable $p$.

The new function is defined by

```math
g(p) = pq - f(q),
```

with $q$ understood as the value determined by the relation

```math
p = \frac{df}{dq}.
```

So the procedure is:

1. Differentiate $f$ to get the slope variable $p$.
2. Solve for $q$ in terms of $p$.
3. Form $pq - f(q)$.
4. Rewrite the result entirely in terms of $p$.

At first this combination $pq - f(q)$ looks arbitrary. It is not. Its purpose is to make a cancellation happen.

To see that, write down the differential of $g$:

```math
dg = d(pq - f).
```

Using the product rule, this becomes

```math
dg = p\,dq + q\,dp - df.
```

Now note that for a one-variable function $f(q)$, the total differential is

```math
df = \frac{df}{dq}\,dq.
```

This is called a **total derivative** because $f$ depends on only one variable, so when $q$ changes, there is only one way for $f$ to change. Since we defined

```math
p = \frac{df}{dq},
```

we have

```math
df = p\,dq.
```

Substituting this into the expression for $dg$, we get

```math
dg = p\,dq + q\,dp - p\,dq = q\,dp.
```

So the $dq$ terms cancel. That is the whole point. The transformed function is now naturally written in terms of $dp$ rather than $dq$.

### A concrete example

Take the function

```math
f(q) = q^2.
```

Its derivative is

```math
p = \frac{df}{dq} = 2q.
```

So

```math
q = \frac{p}{2}.
```

Now form the Legendre transform:

```math
g(p) = pq - f(q).
```

Substitute $f(q) = q^2$:

```math
g(p) = pq - q^2.
```

Now replace $q$ by $p/2$:

```math
g(p) = p\left(\frac{p}{2}\right) - \left(\frac{p}{2}\right)^2
= \frac{p^2}{2} - \frac{p^2}{4}
= \frac{p^2}{4}.
```

So the Legendre transform of $f(q) = q^2$ is

```math
g(p) = \frac{p^2}{4}.
```

This example is simple, but it shows the whole pattern. We started with a function of $q$, introduced the slope variable $p$, and produced a new function of $p$.

### More than one input variable

The next worry is natural. The Lagrangian is not a function of one variable. Why should a one-variable example help?

The answer is that a Legendre transform does not need to transform all the variables of a function. It can transform only a chosen subset, leaving the others alone.

Suppose we have a function of two variables:

```math
f(x,y).
```

We might choose to transform only with respect to $y$, leaving $x$ untouched. Then we define

```math
p = \frac{\partial f}{\partial y},
```

and form

```math
g(x,p) = py - f(x,y).
```

Here the notation has changed slightly. We now use a **partial derivative**

```math
\frac{\partial f}{\partial y}
```

instead of an ordinary derivative

```math
\frac{df}{dq}.
```

The reason is that $f$ now depends on more than one variable. A partial derivative means: vary $y$, hold the other variables fixed, and see how $f$ changes.

So:

- a total derivative tracks the full change of a function along all the ways its variables may vary
- a partial derivative tracks the change with respect to one chosen variable, holding the others fixed

That is exactly what we need in mechanics.

### The mechanical case

The Lagrangian is a function of position, velocity, and time:

```math
L(q,\dot q,t).
```

For many degrees of freedom it is

```math
L(q^1,\dots,q^n,\dot q^1,\dots,\dot q^n,t).
```

The Legendre transform in mechanics is not taken with respect to all of these variables. It is taken only with respect to the velocity variables $\dot q^i$. The position variables $q^i$ and the time variable $t$ are carried along.

This is why we define

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

We do **not** define the transform using $\partial L/\partial q^i$, because we are not replacing $q$. We are keeping $q$ and replacing $\dot q$.

The transformed function is then

```math
H(q,p,t) = p_i \dot q^i - L(q,\dot q,t),
```

with $\dot q$ understood, when possible, as a function of $(q,p,t)$ obtained by solving

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

So the one-variable example and the mechanical case are exactly the same pattern. The only difference is:

- in the simple example there is one variable to transform
- in mechanics there are several velocity variables to transform
- the position variables and time are left untouched

### Why this transform is the right one here

Its significance is not that it mysteriously creates the correct structure. The action has already selected the correct conjugate variable. What the Legendre transform does is remove the unwanted dependence on $d\dot q$ and rewrite the theory cleanly in terms of the already-selected variables.

To see this, differentiate $H$:

```math
dH
= \dot q^i\,dp_i
+ p_i\,d\dot q^i
- \frac{\partial L}{\partial q^i}dq^i
- \frac{\partial L}{\partial \dot q^i}d\dot q^i
- \frac{\partial L}{\partial t}dt.
```

Here $dH$ is the total differential of $H$. It records how $H$ changes when all of its variables are allowed to change.

Now use the defining relation

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

Then the terms involving $d\dot q^i$ cancel:

```math
p_i\,d\dot q^i
- \frac{\partial L}{\partial \dot q^i}d\dot q^i
= 0.
```

So we are left with

```math
dH
= \dot q^i\,dp_i
- \frac{\partial L}{\partial q^i}dq^i
- \frac{\partial L}{\partial t}dt.
```

This cancellation is the whole reason the transform applies here. It is the mechanism by which the theory is rewritten from $(q,\dot q)$ language into $(q,p)$ language.

It is important to pause here, because this equation is only the first stage.

At this point we have used only the definition of the Legendre transform and the definition of momentum. We have **not** yet used the equations of motion. So this formula tells us what the differential of $H$ looks like as a consequence of the change of variables alone.

The next step is to bring in the Euler-Lagrange equations:

```math
\frac{d}{dt}\frac{\partial L}{\partial \dot q^i}
- \frac{\partial L}{\partial q^i}
= 0.
```

Since

```math
p_i = \frac{\partial L}{\partial \dot q^i},
```

this becomes

```math
\dot p_i = \frac{\partial L}{\partial q^i}.
```

Now substitute this into the expression for $dH$. Then the previous formula becomes

```math
dH
= \dot q^i\,dp_i
- \dot p_i\,dq^i
- \frac{\partial L}{\partial t}dt.
```

If the Lagrangian has no explicit time dependence, then the last term vanishes and we get the especially clean form

```math
dH
= \dot q^i\,dp_i
- \dot p_i\,dq^i.
```

This is the stage at which the Hamiltonian form of the dynamics comes into view.

### Why this differential matters

One might still object: so what? We have found a new function of $q$ and $p$. Why should this function matter mechanically?

The answer is that the usefulness of $H$ is not merely that it is a new function. It is that its differential has exactly the form needed to read off the equations of motion in the new variables.

Any function $H(q,p,t)$ has a total differential of the form

```math
dH
= \frac{\partial H}{\partial q^i}dq^i
+ \frac{\partial H}{\partial p_i}dp_i
+ \frac{\partial H}{\partial t}dt.
```

But we have just shown that, for the Legendre transform of the Lagrangian,

```math
dH
= \dot q^i\,dp_i
- \dot p_i\,dq^i
- \frac{\partial L}{\partial t}dt.
```

So by comparing the coefficients of the independent differentials $dq^i$ and $dp_i$, we obtain

```math
\frac{\partial H}{\partial p_i} = \dot q^i,
\qquad
\frac{\partial H}{\partial q^i} = -\dot p_i.
```

These are Hamilton's equations, except for the explicit time term, which can be treated separately.

So the reason we care about $H$ is not just that it is a function that can be written in terms of $q$ and $p$. We care because it packages the same mechanics in a form whose derivatives directly generate the time evolution of the state.

Under suitable conditions, no physics has been lost in passing from $L$ to $H$. The Legendre transform is a rewrite of the same theory in different variables:

- $L(q,\dot q,t)$ describes the dynamics in terms of position and velocity
- $H(q,p,t)$ describes the same dynamics in terms of position and momentum

The point of the transform is that, once $p$ has already been identified as the variable conjugate to $q$, the Hamiltonian rewrite is the one that makes the equations of motion first-order in time and expresses them directly on the space of instantaneous states.

That is the point to keep in mind. The Legendre transform is not a random algebraic trick attached to mechanics from outside. It is the correct rewriting once the action has already told us that the variable conjugate to $q$ is

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```
