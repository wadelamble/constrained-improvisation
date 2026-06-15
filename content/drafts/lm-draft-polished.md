# Path Mechanics
We have discussed the symmetries that characterize the world we live in, the geometry defined by invariants of these symmetry transformations, the objects that inhabit this geometry, and the constraints this structure places on causality. We can now turn our attention to how physical systems, under these constraints, evolve.

## The Principle of Least Action
Imagine the possible paths between some endpoints in a time vs position plot. [diagram].

![Possible spacetime paths](animations/lm-possible-spacetime-paths.png)

Without any training in physics, could we guess which path is the physical one? Einstein is purported to have said that "the difference between genius and stupidity is that genius has its limits." If we think nature has a certain genius, and notice that simple or elegant paths are the rarest among all possible paths, we might suspect that nature chooses the most elegant. We cannot take this too literally. In complicated systems, physical paths can be complicated. But the intuition is essentially on target. Whatever the physical path is for a given system, it is the one that, when all constraints are taken into account, is the most "something." We don't need to characterize this ineffable "something" -- simple, elegant, short, lazy, relaxed, efficient, obvious -- but only define it as a function such that the physical history corresponds to a unique feature of the function. This is the "principle of least action." Action is the quantity assigned to possible paths, and the physical path is the one whose action is "stationary," or unchanged under first-order perturbations, typically a minimum or maximum.

The simplest example of the principle is that of a free particle that moves at constant velocity so that its path in a spacetime diagram is a straight line. A slightly more interesting case is that of an object falling in uniform gravity which traces a parabola in spacetime. We can see the pattern that the complexity of the path scales to the complexity of the constraints.

![Free particle and uniform force spacetime paths](animations/lm-free-vs-uniform-force-spacetime.png)


### The Lagrangian Function
How would we go about putting these ideas on a mathematical footing? We can map paths, just as we could the members of any set, to numbers.  [diagram] We call this map a "functional" (a map from functions to numbers, as opposed to a "function," which is a map from numbers to numbers). Now, we could map a path to a number as follows.

```math
F[x]=x(t_2)-x(t_1).
```

This is a perfectly valid functional, but it won't do for physics. Why? Because it ignores everything that happens between the endpoints, and that is exactly where the physics happens! We need a functional that accounts for each infinitesimal step. A path integral does this by assigning a contribution to each segment of the path and adding those contributions into one number.

$S[\gamma]=\int_\gamma dS$

Once we use $t$ to parameterize the path, each infinitesimal contribution can be written as some function times $dt$.

$dS=L\,dt$

That function is the Lagrangian. Since the action is built locally along a path, the local weighting must be able to see the infinitesimal piece of path being added. The minimal geometric data for that infinitesimal piece are the point $\gamma(t)$, the tangent $\dot{\gamma}(t)$, and the parameter value $t$. Thus we write

$L=L(\gamma(t),\dot{\gamma}(t),t)$

and therefore

$dS=L(\gamma(t),\dot{\gamma}(t),t)\,dt$

Adding all those little contributions from $t_1$ to $t_2$ gives

$S[\gamma]=\int_{t_1}^{t_2}L(\gamma(t),\dot{\gamma}(t),t)\,dt$

### Action Stationary Points

This behaves like a smooth function when the local function $L$ is smooth. If we choose one allowed wiggle shape $\eta(t)$ and scale it by a number $\epsilon$, then

```math
\gamma_\epsilon(t)=\gamma_0(t)+\epsilon\,\eta(t)
```

turns the action into an ordinary one-variable function.

```math
S(\epsilon)=S[\gamma_\epsilon].
```

The original path $\gamma_0$ is stationary along this chosen wiggle when $dS/d\epsilon=0$ at $\epsilon=0$. For $\gamma_0$ to be a stationary path, this must hold for every allowed wiggle $\eta(t)$.

![One-parameter variation slice](animations/lm-one-parameter-variation-slice-contact-sheet.png)

*A local wiggle slides along the path. The orange dot follows the chosen wiggle amplitude, while the tangent at $\epsilon=0$ tests stationarity.*

[Open MP4: lm-one-parameter-variation-slice.mp4](animations/lm-one-parameter-variation-slice.mp4)


### Spacetime Invariance
If the action encodes the physical path, the action must be spacetime invariant. That is, if all observers agree on the same physical behavior, and if that behavior extremizes the action for all observers, then all observers must agree on the action. We typically write the action, as we have above, in terms of coordinate time since that is what observers directly measure. But we are free to compute the action in any frame, including the local rest frame along the path, where we can integrate over proper time, $S=\int_{\tau_1}^{\tau_2}L\,d\tau$. When we do so, since the proper time differential is a Lorentz invariant, the Lagrangian must be as well so that the entire integral is invariant. In the simplest case without any cancellation between terms, the Lagrangian's individual terms must be invariant as well. Candidate invariants are $x^\mu x_\mu$ and $u^\mu u_\mu$. The former cannot be physically relevant since empty spacetime has no preferred origin, and the latter reduces to $c^2$ (or 1 in natural units). We can scale an invariant, certainly when it is just $1$, as it is here. Thus the action for a free particle in spacetime is $S=-\alpha\int_{\tau_1}^{\tau_2}d\tau$. We define mass as being precisely this scale factor. $S=-m\int_{\tau_1}^{\tau_2}d\tau$. We may now ask what happens to "non-free" particles, those that are acted upon by some "force." At this level, a "force" seems to require some additional fact about position, some way for one location to differ physically from another; in typical non-relativistic systems, we represent this "force field" with a position-dependent "potential energy" term in the Lagrangian. But in the fundamental relativistic formulation for a single particle, we cannot have such a term, because spatial position by itself is not a Lorentz invariant. This leads to a deep conclusion. In the single-particle picture, the only relativistically valid Lagrangian we can build is the free one. We can introduce potentials for convenience, but in this single-particle picture there is no invariant object for them to depend on. However, when we move from particles to fields, we will have a new, rich set of invariants to work with, and we will have interactions between different fields. When we cross that bridge, we will be able to build richer Lagrangians that are Lorentz invariant, and potentials will be seen to arise from interacting fields.

### Curvature
If the only single-particle path we can build from spacetime invariance alone is a straight line, how does an object ever curve in spacetime, that is, accelerate? One answer is that, if spacetime itself were curved, objects would accelerate toward one another.

![Geodesic convergence animation contact sheet](animations/lm-geodesic-convergence-contact-sheet.png)

*Longitude lines are straight paths on the sphere, yet beads following them approach each other.*

[Open MP4: lm-geodesic-convergence.mp4](animations/lm-geodesic-convergence.mp4)

Likewise, any accelerated motion can be viewed as the projection of motion in an enlarged geometric setting, where a curved or straight path in the larger structure appears as acceleration in spacetime. At one level, this is nothing more than a shift in perspective from a force imposed against a flat background to constrained motion on a curved background. This shift puts the principle of least action in the geometric setting where the Lagrangian can be constructed to be Lorentz invariant from geometric considerations. This in turn allows curvature itself to evolve dynamically, in accordance with relativity. This idea -- that curvature evolves as fields on spacetime -- is the essence of how force is conceived in modern physics.

### Action, Momentum, and Energy
We know from the Lie algebra that translations have a generator, and in relativity we call this generator momentum:

```math
\hat P^\mu:=\frac{\partial}{\partial x_\mu}.
```

Splitting time and position, this becomes

```math
\hat P^\mu
=
\left(
\frac{\partial}{\partial t},
-\frac{\partial}{\partial x},
-\frac{\partial}{\partial y},
-\frac{\partial}{\partial z}
\right)
=
(\hat E,\hat p_x,\hat p_y,\hat p_z).
```

We know furthermore that the norm of momentum gives an invariant value,

```math
P_\mu P^\mu=m^2,
```
in natural units where $c=1$. This invariant value is what we call mass. In ordinary energy-momentum variables this is the mass-shell condition

```math
m^2 = E^2 - p^2
```

What we do not know from Poincare symmetry alone is what function on spacetime the momentum operator acts on to yield the momentum value. The action evaluated along the physically valid path ending at $x$, written $S_{\text{phys}}(x)$, supplies this function, and in doing so yields the value of the momentum for physically valid paths.

```math
\hat P_\mu S_{\text{phys}}(x)=\frac{\partial S_{\text{phys}}}{\partial x^\mu}=P_\mu .
```

Let us now argue for this by considering the free particle, which can then be generalized to more complex systems. We know that action is proportional to proper time:

```math
S=-\alpha\int d\tau .
```

That tells us that action must accumulate over a physical history as proper time must accumulate. We can separate the action variation into interior and boundary terms. For a path $x^\mu(\lambda)$,

```math
S[x]=\int_{\lambda_1}^{\lambda_2}L(x,\dot x,\lambda)\,d\lambda ,
```

and therefore

```math
\delta S
=
\int_{\lambda_1}^{\lambda_2}
\left(
\frac{\partial L}{\partial x^\mu}
-
\frac{d}{d\lambda}\frac{\partial L}{\partial \dot x^\mu}
\right)\delta x^\mu\,d\lambda
+
\left[
\frac{\partial L}{\partial \dot x^\mu}\delta x^\mu
\right]_{\lambda_1}^{\lambda_2}.
```

The interior term gives the equations of motion. We can rewrite the boundary term as:

```math
p_\mu:=\frac{\partial L}{\partial \dot x^\mu},
```

which identifies momentum as the gradient of the action with respect to endpoint displacement. That is, on an extremal path, where the interior term vanishes, if one endpoint is displaced along the physically available path, then

```math
dS=P_\mu dx^\mu=E\,dt-\mathbf{P}\cdot d\mathbf{x}.
```

We expect from our everyday understanding of momentum that it should "point" in the direction of the next step along the path in spacetime. Indeed, that is exactly what the action gradient supplies:

```math
\partial_\mu S=-\alpha u_\mu.
```
Schematically, we have:

```math
\text{translation generator}
\quad\longleftrightarrow\quad
\text{endpoint gradient of extremal action path}.
```

We can loosen the free-particle assumption by allowing the scale that converts proper time into action to depend on position:

```math
S=-\int \alpha(x)\,d\tau .
```
This is equivalent to introducing a position-dependent effective mass, or a scalar background whose gradient acts like a force. We then maintain the relation that the action gradient is the tangent to the worldline:

```math
\partial_\mu S=-\alpha(x) u_\mu.
```

Now, this leads to a fascinating and wonderful conclusion. We argued that the action for the free particle case simply scaled proper time as this was the only invariant available. Now, however, a position-dependent effective mass enters (and we will have much to say about how it does), and the implication is that the physical path does *not* maximize proper time. That is, an accelerating body ages more slowly than a non-accelerating one. We already saw this from purely geometric reasoning in the twin paradox. Now we see that the form of the action that causes acceleration leads to the same conclusion.

### Action, Momentum, and Energy (machine generated)
We know from the Lie algebra that translations have a generator, and in relativity we call this generator momentum:

```math
\hat P^\mu:=\frac{\partial}{\partial x_\mu}.
```

Splitting time and position, this becomes

```math
\hat P^\mu
=
\left(
\frac{\partial}{\partial t},
-\frac{\partial}{\partial x},
-\frac{\partial}{\partial y},
-\frac{\partial}{\partial z}
\right)
=
(\hat E,\hat p_x,\hat p_y,\hat p_z).
```

Poincare symmetry also tells us that the norm of momentum gives an invariant value:

```math
P_\mu P^\mu=m^2,
```

in natural units where $c=1$. This invariant value is what we call mass. In ordinary energy-momentum variables this is the mass-shell condition

```math
m^2=E^2-P^2.
```

This gives us the abstract structure. Momentum is the translation generator, and its invariant norm defines the mass shell. What Poincare symmetry does not give us is the actual momentum value carried by a particular physical path. For that, we need the action.

The action evaluated along the physically valid path ending at $x$ is a function on spacetime. We write it as $S_{\text{phys}}(x)$. This is the function the momentum operator acts on to yield the momentum value:

```math
\hat P_\mu S_{\text{phys}}(x)
=
\frac{\partial S_{\text{phys}}}{\partial x^\mu}
=
P_\mu .
```

As we have seen, varying the action separates its first-order change into an interior term and a boundary term:

```math
\delta S
=
\int_{\lambda_1}^{\lambda_2}
\left(
\frac{\partial L}{\partial x^\mu}
-
\frac{d}{d\lambda}\frac{\partial L}{\partial \dot x^\mu}
\right)\delta x^\mu\,d\lambda
+
\left[
\frac{\partial L}{\partial \dot x^\mu}\delta x^\mu
\right]_{\lambda_1}^{\lambda_2}.
```

The interior term gives the equations of motion. The boundary term gives the endpoint-gradient of the action:

```math
P_\mu:=\frac{\partial L}{\partial \dot x^\mu}.
```

On the physically valid path, the interior term vanishes. If one endpoint is displaced along the physically available path, then

```math
dS=P_\mu dx^\mu=E\,dt-\mathbf{P}\cdot d\mathbf{x}.
```

So the abstract generator supplied by Poincare symmetry is filled in by the gradient of the physical action:

```math
\text{translation generator}
\quad\longleftrightarrow\quad
\text{endpoint gradient of physical action}.
```

For the free particle, the action is proportional to proper time:

```math
S=-\alpha\int d\tau .
```

Since proper time accumulates along a physical history, the action accumulates as well. The corresponding action-gradient is

```math
\partial_\mu S=-\alpha u_\mu.
```

Thus the endpoint-gradient of the action gives the lowered tangent to the worldline, scaled by the constant that converts proper time into action. This is the sense in which momentum points in the direction of the next step through spacetime.

We can loosen the free-particle assumption by allowing the scale that converts proper time into action to depend on position:

```math
S=-\int \alpha(x)\,d\tau .
```

This is equivalent to introducing a position-dependent effective mass, or a scalar background whose gradient acts like a force. The local relation becomes

```math
\partial_\mu S=-\alpha(x)u_\mu.
```

The action is no longer pure proper time, but weighted proper time. The physical path therefore does not simply maximize proper time. It extremizes the weighted proper time supplied by the action. That is, an accelerating body ages more slowly than a non-accelerating one. We already saw this from purely geometric reasoning in the twin paradox. Now we see that the form of the action that causes acceleration leads to the same conclusion.
