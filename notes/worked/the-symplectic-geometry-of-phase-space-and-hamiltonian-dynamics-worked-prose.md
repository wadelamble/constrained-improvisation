## The Symplectic Geometry of Phase Space and Hamiltonian Dynamics

### Phase Space
Phase space, or position/momentum space is the arena for Hamiltonian Mechanics. To appreciate the theory, we need to understand the nature of this space.

#### From histories to states

The objects in Hamiltonian Mechanics -- the state variables and the Hamiltonian function on those variables are obtained from Lagrangian Mechanics. We know that Lagrangian mechanics selects whole paths from path space by extremizing action. The task we thus need to perform is to somehow extract the essential objects of a local theory of instantaneous state from the Lagrangian global theory.

The impact of instantaneous state displacements on action appears when the action is varied. After integrating by parts, the variation separates into a "bulk" term and a "boundary" term. The bulk term determines which paths satisfy the Euler-Lagrange equations. The boundary term, on the other hand, records how the action changes when the endpoint state is infinitesimally changed. Isolating the boundary term's contribution to the variation "factors out" the contribution of state displacements from that of the full path history.

To see this explicitly, start with the expression for the action:

```math
S[q] = \int_{t_1}^{t_2} L(q,\dot q,t)\,dt.
```

Now vary the path $q(t)\to q(t)+\delta q(t)$. Because the Lagrangian depends on both $q$ and $\dot q$, varying the path also varies the velocity: $\dot q(t)\to \dot q(t)+\delta \dot q(t)$. The first-order change in $L$ is therefore just the multivariable chain rule applied to those two arguments. Then

```math
\delta S
=
\int_{t_1}^{t_2}
\left(
\frac{\partial L}{\partial q^i}\,\delta q^i
+
\frac{\partial L}{\partial \dot q^i}\,\delta \dot q^i
\right)dt.
```

The second term contains $\delta \dot q^i$ rather than $\delta q^i$, so integrate it by parts:

```math
\int_{t_1}^{t_2}
\frac{\partial L}{\partial \dot q^i}\,\delta \dot q^i\,dt
=
\left.
\frac{\partial L}{\partial \dot q^i}\,\delta q^i
\right|_{t_1}^{t_2}
-
\int_{t_1}^{t_2}
\frac{d}{dt}\!\left(\frac{\partial L}{\partial \dot q^i}\right)\delta q^i\,dt.
```

Substituting this back in gives

```math
\delta S
=
\int_{t_1}^{t_2}
\left(
\frac{\partial L}{\partial q^i}
-
\frac{d}{dt}\frac{\partial L}{\partial \dot q^i}
\right)\delta q^i\,dt
+
\left.
\frac{\partial L}{\partial \dot q^i}\,\delta q^i
\right|_{t_1}^{t_2}.
```

As advertised, we see that the variation separates into the the bulk term, which governs the equations of motion, and the boundary term, which governs the action's sensitivity to endpoint configuration displacement on a time slice.

`[INSERT ANIMATION LATER: a single path between t_1 and t_2, with the interior variation contributing the bulk term and the endpoint displacements contributing the boundary term.]`

#### The Definition of Momentum

The boundary term has the form $p_i\,\delta q^i$, with

```math
p_i := \frac{\partial L}{\partial \dot q^i}.
```

This tells us what quantity is paired with an infinitesimal change in the state at a moment. That quantity is not, in general, the velocity. Velocity answers the question of how configuration changes along a path. The boundary variation answers a different question: if the endpoint state is nudged in the $q^i$ direction, what coefficient measures the first-order change in the action? The answer is $p_i$.

The functional form of the momentum is determined by the form of the Lagrangian function. In a free system, in which only the kinetic term appears in the Lagrangian, $p$ arises inevitably from the theory's kinematics. In the Newtonian free-particle theory, the kinetic term is proportional to the square of the velocity, a fact that can be shown to follow from Galilean symmetry, so

```math
L = \frac{1}{2}m\dot q^2,
\qquad
p = \frac{\partial L}{\partial \dot q} = m\dot q.
```

In that setting the familiar formula $p=mv$ is inherited from the kinetic term. In a relativistic theory, by contrast, the free kinematics is constrained by Minkowski structure and the mass-shell relation

```math
E^2 = p^2 + m^2
```

in units with $c=1$. The corresponding free Lagrangian then yields the relativistic momentum instead.

Relativity makes this same structure visible from another angle. For a free relativistic particle, the action is built from spacetime length,

```math
S = -m\int ds.
```

Varying an endpoint of the worldline gives a boundary term of the form

```math
\delta S_{\partial} = p_\mu\,\delta x^\mu.
```

So four-momentum is already the covector paired with spacetime displacement in the variation of the action. If we choose a time coordinate, this pairing splits into spatial and temporal pieces,

```math
p_\mu\,\delta x^\mu = p_i\,\delta q^i - E\,\delta t,
```

up to sign convention. Holding endpoint time fixed leaves precisely the spatial boundary pairing $p_i\,\delta q^i$. Thus the Hamiltonian pairing is not a new structure invented after Lagrangian mechanics. It is the time-sliced form of a relation that relativistic mechanics displays directly among action, displacement, and momentum.

#### From the one-form to the two-form

Thus far, we have identified $q$ and $p$ as the correct variables for specifying instantaneous state vis-a-vis action variation. However, the pairing $p_i\,\delta q^i$ is a "one-form" statement, that is, it takes in one vector and returns a number. Specifically, it acts on one infinitesimal variation of one state and returns the action. But to tell the story of Liouville's theorem and statistical behavior, we need something different. We need a way to combine $p$ and $q$ to represent an ensemble of states.

The entire $q,p$ plane contains all possible states. An ensemble is a subset of this set of all possible states. To form such subsets, we need some way to "tile" the space, which we can do with a 2-form, which takes in two vectors and returns an area:

```math
dq^i \wedge dp_i.
```

Integrating this 2-form over a region of phase space measures the "count," or "amount" of states in the region. Once we have the 2-form, we can see the job of Hamiltonian mechanics as finding flows under which the area measured by the 2-form is invariant.

The two-form is not only the measure we need for counting states, it is the instrinsic form that expresses the geometry phase space. We defined momentum by looking at the one-form measuring the contribution of the boundary term to the variation of the action. That boundary term is real, but it also carries a redundancy. The equations of motion are determined by the bulk term, and those equations are unchanged if the Lagrangian is modified by an endpoint-only term. The boundary one-form changes under that modification, while the two-form remains agnostic to it. This is expected in that the physical, or "Hamiltonian," flows we will find do not preserve any notion of length in phase space, but only the notion of area. 

We derive this below, though this can be skipped if desired. Add a total time derivative to the Lagrangian:

```math
L' = L + \frac{dF(q,t)}{dt}.
```

This changes the action by an endpoint term:

```math
S'
=
\int_{t_1}^{t_2} L'\,dt
=
S + F(q(t_2),t_2)-F(q(t_1),t_1).
```

Intuitively, this is like adding "final elevation minus initial elevation" to the cost of a hike with fixed endpoints. It changes the endpoint accounting, but it does not change which interior route extremizes the cost.

The boundary one-form shifts by the differential of that added endpoint function:

```math
\theta' = \theta + dF.
```

Here

```math
\theta = p_i\,dq^i.
```

But the two-form is built by taking the exterior derivative of the one-form:

```math
\omega = d\theta.
```

So after the shift,

```math
\omega'
=
d\theta'
=
d(\theta + dF)
=
d\theta + d(dF)
=
d\theta
=
\omega.
```

#### What Phase Space Is

We are now able to define phase space. It is the space whose points are instantaneous states expressed in the paired, or conjugate, variables selected by the action. For one degree of freedom, a point is $(q,p)$. For many degrees of freedom, a point is $(q^1,\dots,q^n,p_1,\dots,p_n)$. Phase space is a reorganization of what counts as an instantaneous state as with respect to action extremization. Once the boundary variation has told us what variable is paired with $q$, the state is no longer most naturally described by $(q,\dot q)$, but by $(q,p)$.

### Hamiltonian Flows
Compare phase space plots to spacetime diagrams \(Galilean or Minkowskian\). There, motion is baked into the shape of the worldline. The history is contained in a static plot. In phase space, there is no motion, no history, until a point or region begins to flow. Our next task, then, is to describe the flows that characterize conservative physical systems. 

#### Why the Legendre transform belongs here
Once $p_i = \partial L/\partial \dot q^i$ has been identified, the next question is how to rewrite the theory in terms of $(q,p)$ rather than $(q,\dot q)$. That is the role of the Legendre transform. It is not a trick that creates the canonical pairing. The pairing is already in hand. The transform is the device that follows that pairing and rewrites the dynamics in its terms.

The abstract pattern is simple. A Legendre transform replaces one chosen variable by its derivative-conjugate variable, while leaving any untouched variables in place as parameters. That is why the many-variable case is not a problem. In mechanics, one transforms only with respect to the velocity variables $\dot q^i$, not with respect to the position variables $q^i$. The transformed function is

```math
H(q,p,t) = p_i \dot q^i - L(q,\dot q,t),
```
with $\dot q$ understood, when possible, as a function of $(q,p,t)$.

Its significance is the cancellation in the differential. Differentiating $H$ produces terms involving $d\dot q^i$, but because $p_i = \partial L/\partial \dot q^i$, those terms cancel. What remains is a differential written in terms of $dq^i$, $dp_i$, and $dt$. At that stage the theory has been genuinely rewritten in $(q,p)$ language. When the Euler-Lagrange equations are then substituted in, the differential takes the cross-coupled form from which Hamilton's equations can be read off. This is why the Hamiltonian matters mechanically. It is not merely a new function of new variables. It is the function whose differential packages the same dynamics as first-order evolution on the space of instantaneous states.

### Turning the movie on

At this point the geometry has been earned, but it is still static. The next step is not a new derivation but a new picture. A point of phase space is one exact instantaneous state. As time evolves, that point traces out a curve. A family of nearby points traces out a moving patch. This is the first object on which the later Liouville story can be seen.

The fluid analogy can help here, but only lightly. What matters is not ordinary fluid space but phase space itself. One should imagine not a parcel of water in physical space, but a tiny patch of possible states being carried by the dynamics through the space of states. The patch may bend, stretch, and shear as the motion proceeds. That is the right movie with which to end this section. The full proof of what is preserved under that motion belongs next. Here the point is to have reached the arena in which that proof can even be stated.

### The symplectic geometry of phase space

It is worth pausing to consider the geometry of phase space itself. The same broad kind of geometry appears in many areas of science, but here its first important feature is negative. Phase space does not come equipped with a canonical distance. One can certainly impose a distance on it by hand. Given two points $(q_1,p_1)$ and $(q_2,p_2)$, one might write down something like

```math
d\big((q_1,p_1),(q_2,p_2)\big)
=
\sqrt{(q_2-q_1)^2 + (p_2-p_1)^2}.
```

Nothing is mathematically wrong with this. The problem is that Hamiltonian mechanics does not single it out. It is extra structure. What phase space comes with intrinsically is not a rule of length but a rule of area:

```math
\omega = dq^i \wedge dp_i.
```

This is the crucial contrast with Euclidean or Minkowski geometry. There the invariant object is a metric, and the metric determines which lengths and intervals are preserved under the allowed transformations. Here the invariant object is not a length but an area. Symplectic geometry asks not how long a vector is, but what oriented area is spanned by an infinitesimal patch of neighboring states.

One can see this directly in the simplest one-degree-of-freedom case. Consider the transformation

```math
(Q,P) = (2q,p/2).
```

It preserves the symplectic area form, since

```math
dQ \wedge dP
=
2\,dq \wedge \frac{1}{2}\,dp
=
dq \wedge dp.
```

So from the symplectic point of view this is a perfectly acceptable change of phase-space coordinates. But it certainly does not preserve an ordinary Euclidean distance. A unit step in the $q$ direction is doubled, while a unit step in the $p$ direction is halved. Lengths change, but areas do not. This is exactly what it means to say that phase space has a canonical symplectic structure but no canonical metric.

Once the invariant is identified, the corresponding allowed transformations are identified with it. In Euclidean or Minkowski geometry, the relevant transformations are those that preserve the metric. In phase space, the relevant transformations are those that preserve the symplectic form. These are the canonical transformations.

A canonical transformation is therefore not merely a convenient change of variables. It is a change of phase-space coordinates that leaves intact the area structure in which Hamiltonian dynamics is written. Because Liouville's theorem is ultimately a statement about the preservation of ensemble structure in that symplectic measure, a canonical transformation is precisely the kind of change of variables under which that structure remains visible as the same structure. It preserves the local phase-space geometry in which time evolution carries points into curves and patches into deformed but uncrushed patches.

Some canonical transformations also preserve ordinary distance, but that is an extra fact about them, not part of what makes them canonical. A translation

```math
(Q,P) = (q+a,p+b)
```

preserves both Euclidean distance and symplectic area. An ordinary rotation in the $(q,p)$ plane does the same. But a shear such as

```math
(Q,P) = (q+kp,p)
```

is also canonical, since

```math
dQ \wedge dP
=
(dq+k\,dp)\wedge dp
=
dq \wedge dp,
```

yet it does not preserve Euclidean distance. Points at different values of $p$ are shifted by different amounts in the $q$ direction, so lengths and angles change even though areas do not. This is the point. Symplectic geometry does not demand rigid shape. It demands preservation of the area structure.

So one should not imagine canonical transformations as only shearing and squeezing. They may move a patch around as a whole, they may rotate it, and they may deform it internally. What unifies them is not that they preserve metric shape, but that they preserve symplectic area. In this sense, canonical transformations stand to symplectic geometry as isometries stand to metric geometry.

Hamiltonian time evolution should be understood against this background. It is not one single canonical transformation, but a one-parameter family of them. For each fixed time $t$, the evolution map from the initial state to the state at time $t$ is a canonical transformation. The Hamiltonian picks out one particular continuous path through the much larger space of allowable canonical transformations. That is why a phase-space patch may be advected as a whole while simultaneously being sheared, rotated, or squeezed, yet still preserve the ensemble structure that Liouville's theorem will later formalize.
