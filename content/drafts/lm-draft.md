# LM Draft

Cleaned copy of `lm-proto-draft.md`, originally copied from `content/manuscript-markdown/hum-non-drm.md`, from `## Symmetry, Parallel Transport, and Extremization` through the free-particle worldline derivation, stopping before `## Gravity and General Relativity`.

[move to lm-reusable-material:
## Symmetry, Parallel Transport, and Extremization

In a generalized sense, fundamental constituents of matter, particles like electrons and photons, always travel is in a "straight" line in full space constructed from the symmetry they represent.Particles travel in a straight line in the full spacetime bundle to which their species belongs. also, this is talking about fiber bundles which is post-quantum. we need to remove it and save in lm-reusable-material. To make sense of "felt forces," we have to be very careful about what spaces we are talking about. If an object is traversing a geodesic in spacetime, it will feel no force. However, if, in following a geodesic through a fiber bundle, it deviates from a spacetime geodesic, it will experience a "felt force."We will unpack this as we get deeper into this chapter. As alluded to already, we will generalize the idea of "straight" in "flat space" to "straightest possible," or geodesical, in "curved space."

This is nothing more in essence than the idea that following lines of longitude on earth, or more generally "great circles," or geodesics, on the surface of a sphere. We want to call such a path "straight" because it is the shortest possible path between two points. This informal definition of "straightest possible" contains two elements that we can use to rigorously define *parallel transport*. The first element is that the space has an invariant structure derived from symmetry that allows an agreed upon definition local definition of length. The second element is that what we intuitively see as "straightest" or "simplest" arises from *extremizing* (often "minimizing") the integral of the invariant length over a path. We will make the bridge from geometry to physics by taking care to build our invariant structure from physical symmetry. Before we do that, let's "do a little geometry" to make sure these ideas are well grounded. We will show how minimizing length in flat space defines a straight line and how doing the same on a sphere defines a geodesic.]

## The Spacetime Path

1. The path and the mass is all there is.
2. The mass is also geometric, so geometry is all there is. this isn't hand-wavy, its literal, we will say it in a literal way.
3. Therefore, if we know the path, we can say everything that can be said abou the "dynamics" (we need to define the term)
4. But that requires we already have a history, our job is to figure out a future history.
5. for a free particle, we just pick a straight line, that's telling us a lot
5.1 it leads us to guess we pick the shortest path using some weighted length measure which goes to 1 for a free path.
5.2 it tells us that the weighting reflects the dynamics, the forces acting. worldline curvature  is equated to force, and weighting maps to a "virtual" straight path"
5.a Action (or higher)
6. this is in a sense the most "relaxed path" under the circumstance, easy to see for free particle, and easy to see in fixed case like catenary.
6.1 This gives LM an architectural vs a dynamic feel.
7. weighting is L = T + V, define what these terms mean intuitively
8. The weighting is the "potential landscape". 
8.1 A skier going up and down hills is a clean expample.
8.2 if the skier take the same time on more hilly terrain, she has more action. changiness of the potential manifests as changiness of the worldline.
9. But where does the potential come from?
9.1 Answer -- deeper in the geometry
9.2 While LM feels more global, the need to L(x,v) makes it feel local all over again. When it's origin is found deeper in the geometry, this sleight of hand is unsleighted and the idea of "relaxation" is equated with following a geodesic or of the full geometry."
9.2 Gravity: spacetime curvature.
9.3 EM: curvature of fiber bundle that only makes sense once we define state in QM.
9.4 But all this weill be discussed in subsequent sections.
extra: action definition, centrality of action, lagrangian needs dynamic origin. inevitible architectural

A worldline and its mass shell specify a particle's history completely. The mass is read from the geometry. It is an expression of how the spacetime interval is apportioned over time and space separations under changes of velocity. [equation wtih ds, v, dx and dt, plus animation]. If we know the worldline and the mass, then, we can read off all "the physics," all the "forces" that acted on the particle during its history. But this only tells us the physics of a history that has already happened. Our job is to find a future history not characterize a past history. We can pick out the worldline of a free particle geometrically. It is a straight line as curvature in spacetime is acceleration and "free" means non-accelerating. A straight line is the minimization of pathlength, suggesting that the correct choice of worldline is some "extremization" of pathlength: [eq. S = mass*integra(ds)] The action, as a measure of path curvature, is a measure of the "dynamics" of the history, of all the forces that acted during it. The fact that a free particle travels a straight line in spacetime also suggests that, whatever the actual path is, it shoud be inevitible in the right geometry.  In fact, we can construct spaces in which the actual path in spacetime is the shortest path. The map to these spaces is encoded in the Lagrangian function, which tells us how find the action of a history: [eq: S = hmm, i want Ldt, but in proper spacetime geometry/notation]. One then extremizes the action to find the the correct path [eq: functional [] equation]. If someone hands us a Lagrangian, we can then hnad them back a future history. 

This begs the question where the Langranian came from. We will say it should fill two requirements. First, it should be mediated by proper spacetime objects. Second, it should part of deeper geometric considerations of the spaces a physical theory provides. This will be the topic of the "Gravitation" and "Gauge theory" sections.  


also what goes in it? invariat terms, t and v, something that encodes the presence of inertia and acceleration. 

We can guess, correctly it turns out, that the condition of being "free" is equivalent to a uniform "weighting" of the spacetime interval such that, under this weighting, the shortest weighted path is simply the shortest path. And we can go on then to guess that whatever the actual path is, the it is the shortest incorparing the weights. [equation. just path length and weigthing function and integral, nothing here about L or S or even the minkowski interval, just showing integrating a function over a path.] Whatever the actual path is, finding the "shortest" path under the weighting has an evocative meaning along the lines that the path is "as relaxed as possible." We can see this intuively in the static case of a catenary, the shape a rope assumes when dangled from two fix points. [diagram (not animation) of catenary.] In a sense, this path-based approach to mechanics  seems to pick out architectural elements used in nature rather than focusing on local details. The weight we give to the path length is the Lagrangian, in its most typical from [schematic: Lagrangian = Kinetic Energy - Potential energy]. This is a measure of the inertia a system has and the variability of the energy landscape, of how fast how massive an object moves through how "hilly" a landcape.  For the same wordline endpoints, the longer the worldline is, the more massive the object and the more "ups and downs" getting from endpoint to endpoint, the more longer the pathlength. d




For a given mass, to assign the history a number is to assign its path length as it is the only invariant scalar associated with a line segment. Force is the curvature of the worldline. The more force acting over the history, the longer the pathlength. the pathlength wants to be short, so when a force acts, the pathlength only bends "as much as is necessary" to embed the action of the force. 

If we are looking back at our worldline, we would not ask "where will we go next?" but "why did we choose this path?". In answering that, because paths are lawful, we will also supply the answer to "where will we go next" for the same function on configuration space.

lagrangian(q,q-dot) is problematic. It is static throughout spacetime. The origin replaces it with mediators that move through spacetime. This gives a physicality to the potential. Otherwise influence would be mediated w/o abiding c.
### Using Extremization to Find Geodesics 

Let's start with a straight line in flat space.

#### Straight Line in Flat Space\
\
\
\

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image439.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image440.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image441.png)

Figure 53 - Minimizing a curve in the plane

We can write any curve in the (x,y) plane in parametric form

``` math
\lambda \mapsto (x(\lambda),y(\lambda)),
```

with fixed endpoints

``` math
\left( x\left( \lambda_{1} \right),y\left( \lambda_{1} \right) \right) = \left( x_{1},y_{1} \right),\ \ \ \ \ \ (x(\lambda_{2}),y(\lambda_{2})) = (x_{2},y_{2}).
```

The length of such a curve is

``` math
L\lbrack x,y\rbrack = \int_{\lambda_{1}}^{\lambda_{2}}\sqrt{\left( \frac{dx}{d\lambda} \right)^{2} + \left( \frac{dy}{d\lambda} \right)^{2}}\,d\lambda.
```

Define

``` math
\dot{x} = \frac{dx}{d\lambda},\dot{y} = \frac{dy}{d\lambda},\ \ \ \ \ \ R = \sqrt{{\dot{x}}^{\,2} + {\dot{y}}^{\,2}}.
```

Then

``` math
L\lbrack x,y\rbrack = \int_{\lambda_{1}}^{\lambda_{2}}{R\,d\lambda.}
```

Now require that this functional (function of functions) be stationary under small variations of the curve that keep the endpoints fixed.

Let

``` math
x(\lambda) \rightarrow x(\lambda) + \varepsilon\,\eta(\lambda),\ \ \ \ \ y(\lambda) \rightarrow y(\lambda) + \varepsilon\,\xi(\lambda),
```

Here:

- $`\eta(\lambda)`$ and $`\xi(\lambda)`$ are arbitrary test functions that vanishe at the endpoints\
  (so the endpoints stay fixed: $`\eta\left( \lambda_{1} \right) = \eta\left( \lambda_{2} \right) = 0,\ \ \ \ \xi(\lambda_{1}) = \xi(\lambda_{2}) = 0`$)

- $`\varepsilon`$ is an infinitesimal number that controls the size of the change

Then

``` math
\dot{x} \rightarrow \dot{x} + \varepsilon\,\dot{\eta},\dot{y} \rightarrow \dot{y} + \varepsilon\,\dot{\xi}.
```

The varied length is

``` math
L(\varepsilon) = \int_{\lambda_{1}}^{\lambda_{2}}\sqrt{\left( \dot{x} + \varepsilon\dot{\eta})^{2} + (\dot{y} + \varepsilon\dot{\xi})^{2} \right.\ }\text{\:\,}d\lambda.
```

Differentiate with respect to $`\varepsilon`$ and evaluate at $`\varepsilon = 0`$:

``` math
{\frac{dL}{d\varepsilon} \mid}_{\varepsilon = 0} = \int_{\lambda_{1}}^{\lambda_{2}}\frac{\dot{x}\,\dot{\eta} + \dot{y}\,\dot{\xi}}{\sqrt{{\dot{x}}^{\,2} + {\dot{y}}^{\,2}}}\text{\:\,}d\lambda.
```

Stationarity requires

``` math
{{\frac{dL}{d\varepsilon} \mid}_{\varepsilon = 0} = 0.
}
{That\ is:}
```

1.  Take some original test curve and test end-point vanishing functions.

2.  Now L($`\varepsilon)`$ is function of $`\varepsilon`$ only.

3.  Thus, for this test curve, epsilon is 0, and if and only if $`{\frac{dL}{d\varepsilon} \mid}_{\varepsilon = 0} = 0`$, the test path is an extremum (stationary point).

Now integrate this by parts, leading to an integrand containing only $`\eta`$ and $`\xi`$ (not their derivatives) and x, y and their derivatives.

``` math
\int_{\lambda_{1}}^{\lambda_{2}}\frac{\dot{x}\,\dot{\eta}}{R}\,d\lambda = \left\lbrack \frac{\dot{x}}{R}\eta \right\rbrack_{\lambda_{1}}^{\lambda_{2}} - \int_{\lambda_{1}}^{\lambda_{2}}\frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right)\eta\,d\lambda.
```

The boundary term vanishes because $`\eta(\lambda_{1}) = \eta(\lambda_{2}) = 0`$.

Similarly for $`y`$. Therefore the stationarity condition becomes

``` math
\int_{\lambda_{1}}^{\lambda_{2}}\left\lbrack - \frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right)\eta - \frac{d}{d\lambda}\left( \frac{\dot{y}}{R} \right)\xi \right\rbrack d\lambda = 0.
```

Because $`\eta\`$and $`\xi`$can be any functions that vanish at the endpoints, the only way the integral can be zero for all such choices is for the coefficients of $`\eta`$and $`\xi`$to vanish pointwise. $`\frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right) = 0,\ \ \ \ \frac{d}{d\lambda}\left( \frac{\dot{y}}{R} \right) = 0.`$*\*

Define $`A,B`$:

``` math
\frac{\dot{x}}{\sqrt{{\dot{x}}^{\,2} + {\dot{y}}^{\,2}}} = A,\ \ \ \ \frac{\dot{y}}{\sqrt{{\dot{x}}^{\,2} + {\dot{y}}^{\,2}}} = B.
```

Square and add:

``` math
A^{2} + B^{2} = 1.
```

From the first equation,

``` math
\dot{x} = A\sqrt{{\dot{x}}^{\,2} + {\dot{y}}^{\,2}}.
```

This implies that the ratio $`\dot{y}/\dot{x}`$ is constant. Indeed,

``` math
\frac{\dot{y}}{\dot{x}} = \frac{B}{A} = \text{constant}.
```

Therefore both $`\dot{x}`$and $`\dot{y}`$ are constant up to an overall multiplicative factor. Integrating,

``` math
x(\lambda) = a\lambda + b,\ \ \ \ \ \ \ y(\lambda) = c\lambda + d,
```

for constants $`a,b,c,d`$.

The curves that make the length functional stationary are precisely functions of the form:

``` math
(x(\lambda),y(\lambda)) = (a\lambda + b,\text{\:\,}c\lambda + d),
```

which are straight lines.

#### Minimizing Length on Sphere

Let's sketch how we would modify the procedure above to show that geodesics on a sphere are the shortest possible paths in that space.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image442.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image443.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image444.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image445.png)

Figure 54 - Geodesics on a sphere

The procedure proceeds just as for a line in flat space except that our invariant metric change from:*\*
$`ds^{2} = dx^{2} + dy^{2}`$

to:\
``` math
ds^{2} = R^{2}\left( d\theta^{2}+{\sin}^{2}\theta\,d\phi^{2} \right)
```

After carrying out the procedure, we find that:\
\
``` math
{\ddot{\theta} - \sin{\theta\cos{\theta\,{\dot{\phi}}^{2}}} = 0,\ \ \ \ \ \ \ \ \ddot{\phi} + 2\cot\theta\,\dot{\theta}\,\dot{\phi} = 0
}
{which\ are\ the\ equations\ for\ a\ geodesic\ on\ a\ sphere.\ 
}
```

### From Geometry to Physics

A few observations are evident from this discussion. First, the description of curves in terms parameterized equations and their derivatives is the exact same machinery we use for describing physical trajectories. Second, we see that in flat space "acceleration" (second derivative) is zero, while it is non-zero in curved space. Third, the extremization approach we used is identical to the approach used in "Lagrangian Mechanics." The path length is equivalent to the "Lagrangian," the differential equations are equivalent to the "Euler Lagrange" equations, and the invariant distance is equivalent to the invariant Minkowski metric on spacetime.\
\
We can now simply reappropriate this approach to find that a inertial path in spacetime is a straight world line. First, we write down the Lagrangian. For a free particle in spacetime, take the Lagrangian proportional to the invariant interval:

``` math
L = - mc\,\sqrt{- \,\eta_{\mu\nu}\,{\dot{x}}^{\mu}{\dot{x}}^{\nu}}
```

Treat $`x^{\mu}(\tau)`$ as generalized coordinates and apply

``` math
\frac{d}{d\tau}\left( \frac{\partial L}{\partial{\dot{x}}^{\mu}} \right) - \frac{\partial L}{\partial x^{\mu}} = 0.
```

Because $`L`$does not depend explicitly on $`x^{\mu}`$,

``` math
\frac{\partial L}{\partial x^{\mu}} = 0,
```

so we get

``` math
\frac{d}{d\tau}\left( \frac{\partial L}{\partial{\dot{x}}^{\mu}} \right) = 0.
```

Compute the momentum-like term:

``` math
\frac{\partial L}{\partial{\dot{x}}^{\mu}} = \frac{m\,\eta_{\mu\nu}{\dot{x}}^{\nu}}{\sqrt{- \eta_{\alpha\beta}{\dot{x}}^{\alpha}{\dot{x}}^{\beta}}}.
```

With proper time parametrization the denominator is constant, giving

``` math
\frac{d^{2}x^{\mu}}{d\tau^{2}} = 0.
```

This is precisely the statement that in flat spacetime, a free particle follows a straight worldline. We will now see how extending this procedure to curved spacetime leads to General Relativity and its explanation of gravity.

