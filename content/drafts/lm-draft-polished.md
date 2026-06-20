# Variational Mechanics
We have discussed the symmetries that characterize the world we live in, the geometry defined by these symmetry transformations, the objects that inhabit this geometry, and the implications this structure has on causality. We can now turn our attention to how, under these constraints, physical systems evolve in reality.

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

### From Action to Momentum and Energy
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
(\hat E,\hat P_x,\hat P_y,\hat P_z).
```

Poincare symmetry also tells us that the norm of momentum gives an invariant value:

```math
P_\mu P^\mu=m^2,
```

in natural units where $c=1$. This invariant value is what we call mass. In ordinary energy-momentum variables this is the mass-shell condition

```math
m^2=E^2-\mathbf{P}^2.
```

Here $\mathbf{P}$ denotes the spatial momentum.

This gives us the abstract structure. Momentum is the translation generator, and its invariant norm defines the mass shell. What Poincare symmetry does not give us is the actual momentum value carried by a particular physical path. For that, we need the action.

#### Action Variation at the Endpoints
The action evaluated along the physically valid path ending at $x$ is a function on spacetime. We write it as $S_{\text{phys}}(x)$. This is the function the momentum operator acts on to return the momentum function:

```math
\hat P_\mu S_{\text{phys}}(x)=\frac{\partial S_{\text{phys}}}{\partial x^\mu}=P_\mu(x).
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

Thus, the abstract generator supplied by Poincare symmetry is filled in by the gradient of the action along the physical path:

```math
\text{translation generator}
\quad\longleftrightarrow\quad
\text{endpoint gradient of physical action}.
```

#### Momentum as Worldline Tangent
Now we may ask whether this definition of momentum matches our intuitive expectation that momentum "points" in the direction of the next step along the path in spacetime. Let's examine this by considering the free particle, whose action is proportional to proper time:

```math
S=-\alpha\int d\tau .
```

Since proper time accumulates along a physical history, the action accumulates as well. The corresponding action-gradient is

```math
\partial_\mu S=-\alpha u_\mu.
```

Thus the endpoint-gradient of the action is the tangent to the worldline, scaled by $\alpha$. This is the sense in which momentum points in the direction of the next step through spacetime.

We can loosen the free-particle assumption by allowing the scale that converts proper time into action to depend on position:

```math
S=-\int \alpha(x)\,d\tau .
```

This is equivalent to introducing a position-dependent effective mass, or a scalar background whose gradient acts like a force. The local relation becomes

```math
\partial_\mu S=-\alpha(x)u_\mu.
```

The action is no longer pure proper time, but weighted proper time. The physical path therefore does not simply maximize proper time. It extremizes the weighted proper time supplied by the action. That is, an accelerating body ages more slowly than a non-accelerating one. We already saw this from purely geometric reasoning in the twin paradox. Now we see that the form of the action that causes acceleration leads to the same conclusion.

There are cases, most famously that of a magnetic force acting on a moving charge, in which the force has a velocity dependence and momentum is *not* simply tangent to the worldline. Instead, momentum balances the existing velocity with the effect of the velocity-dependent force. We will see that these cases arise when the Lagrangian includes terms from different fields. Thus the definition of momentum in terms of the action remains intact, while the interpretation of momentum as tangent to the worldline is generalized.

#### Rest Energy
As we have seen, for a free particle, the proper-time action is

```math
S=-\alpha\int d\tau=-\alpha\int dt_{\text{rest}}=-mc^2\int dt_{\text{rest}}.
```

Since energy is the generator conjugate to time translation,

```math
E_{\text{rest}}=-\frac{\partial S}{\partial t_{\text{rest}}}.
```

Giving the Promethean result:

```math
E=mc^2
```

#### The Non-relativistic Lagrangian
Consider the case in which the proper-time scale depends on position:

```math
\alpha(x)=mc^2+V(x).
```

The action is

```math
S=-\int (mc^2+V(x))\,d\tau .
```

and so the proper-time Lagrangian is:

```math
L_\tau=-(mc^2+V(x)).
```

After writing $d\tau$ in coordinate time:

```math
d\tau=dt\sqrt{1-\frac{v^2}{c^2}}.
```

We have:

```math
L=-(mc^2+V(x))\sqrt{1-\frac{v^2}{c^2}}.
```

For $v\ll c$,

```math
\sqrt{1-\frac{v^2}{c^2}}
\approx
1-\frac{v^2}{2c^2}.
```

Therefore

```math
L
\approx
-(mc^2+V)
\left(1-\frac{v^2}{2c^2}\right)
=
-mc^2
-V
+
\frac{1}{2}mv^2
+
\frac{Vv^2}{2c^2}.
```

Dropping the constant term $-mc^2$ as it does not appear in the pre-relativistic understanding of mechanics, and ignoring the small correction $Vv^2/(2c^2)$, we have:

```math
L\approx \frac{1}{2}mv^2-V.
```

Thus, the non-relativistic lab-frame Lagrangian is

```math
L=T-V.
```
This is the familiar starting point for non-relativistic Lagrangian mechanics some readers may have seen. One can try to puzzle out why $\int (T-V)dt$ should be the quantity the physical path minimizes. Working through examples one can convince themselves of the intuition that the path is "trading off" potential for kinetic "as economically as possible." To minimize the action, a falling ball gradually gains speed, it doesn't levitate then race to the ground.

### Fermat's Theorem
Light takes the path between two points that takes the least time, even when it has to bend to account for passing through media with different propagation speeds. This is Fermat's theorem.

![Fermat path through a medium band](animations/lm-fermat-medium-band.png)

This requirement fixes the bending angle through Snell's law:

```math
\frac{\sin\theta_{\text{incidence}}}{v_{\text{incident}}}
=
\frac{\sin\theta_{\text{refraction}}}{v_{\text{refracted}}}
```

We will skip the proof, but the intuition is exactly that of any time-optimized route-finding. Say a person were running a race that required swimming across a body of water. To optimize their time, they would balance taking the shortest swim against taking the shortest total route. In the case of running a race, we would say that the racer calculated all this beforehand and chose the optimal route. But how does light do this? Does it "peek ahead"? It certainly can't see the future, but is there some way it can effectively "peek ahead" without actually seeing the future?

Light's optimization of travel time is a specific case of action extremization. While showing this requires material we have not yet covered, what we care about here is not solving the underlying variational problem but exploring the mechanism by which path optimization seems somehow to "look ahead." Any variational problem entails the same seeming paradox, for it is the entirety of the integrated path that is extremized. One could argue that there is no mystery here for the full path is generated from the local equations of motion, but those equations provide a description of the local rules that give rise to the next step of the path, not a reason for those rules. 

The solution to light's ability to find the optimal path was given by Huygens' principle in the late 1600s. The principle states that every point on a wavefront emits spherical wavelets whose envelope is the next wavefront, where the wavelets interfere constructively. Elsewhere, they are out of phase and the wavelets interfere destructively.

![Huygens transverse interference cascade contact sheet](animations/lm-huygens-transverse-interference-cascade-contact-sheet.png)

[Open MP4: lm-huygens-transverse-interference-cascade.mp4](animations/lm-huygens-transverse-interference-cascade.mp4)

What happens when we apply this to a light ray impinging on a medium?

![Huygens Snell symmetric reference animation contact sheet](animations/lm-huygens-snell-symmetric-reference-contact-sheet.png)

[Open MP4: lm-huygens-snell-symmetric-reference.mp4](animations/lm-huygens-snell-symmetric-reference.mp4)

The key fact is that each secondary wavelet expands at the wave speed of the medium it enters. After the same elapsed time,

```math
\text{wavelet radius}=v_{\text{medium}}\Delta t .
```
After a time $\Delta t$, the incoming wavefront reaches B. During that same time, the incoming wavefront has advanced a distance $v_1\Delta t$ in the first medium. Also during that same time, the wavelet from A has expanded to radius $v_2\Delta t$ in the second medium.

![Huygens two-point Snell construction](animations/lm-huygens-snell-two-point-construction.png)

Now both pieces use the same boundary distance $AB$. For the incoming side,

```math
\sin\theta_1=\frac{v_1\Delta t}{AB}.
```

For the refracted side,

```math
\sin\theta_2=\frac{v_2\Delta t}{AB}.
```

Therefore,

```math
\frac{\sin\theta_1}{v_1}
=
\frac{\sin\theta_2}{v_2}.
```

This is Snell's law, or equivalently Fermat's theorem that light optimizes its travel time.

What has happened here? If we focus on the light ray rather than the wave, it seems to have "peeked ahead" and found the optimal path. If we focus on the wave instead, the mystery changes. The wave does not choose a path in advance, it sends contributions through the available possibilities, and the contributions away from the travel-time optimum cancel by destructive interference. Would we ever see those interfering contributions before the cancellation has narrowed into a clean ray? Yes, when the wavelength is long compared to the region over which the wavefront is being reflected or refracted. A long-wavelength radio wave reflecting from a narrow mirror, for example, would not produce a sharp reflected ray. The cancellation would be incomplete, and the reflected signal would spread into a diffraction pattern. As we will see, in quantum mechanics, the wavefunction carries the phase information whose interference determines the probabilities of particle observations. In the macroscopic limit, where the wavelength of the quantum wavefunction is very small compared to the scale over which the path is varied, contributions away from the classical path cancel by destructive interference. Thus, in the quantum context, Huygens' principle provides a mechanism by which "nature solves" the variational problem to find the optimal path.

We can then lift the mathematical idea of phase cancellation out of the specific wave picture and assign a phase to every possible path. Paths whose phases fail to line up contribute little to the final amplitude, while paths near the stationary path reinforce. This is, as we will discuss later, Feynman's path integral formulation of quantum mechanics.


