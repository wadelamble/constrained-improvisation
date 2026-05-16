# LM Proto Draft

Copied from `content/manuscript-markdown/hum-non-drm.md`, from `## Symmetry, Parallel Transport, and Extremization` through the free-particle worldline derivation, stopping before `## Gravity and General Relativity`.

## Symmetry, Parallel Transport, and Extremization

In a generalized sense, fundamental constituents of matter, particles like electrons and photons, always travel is in a â€œstraightâ€ line in full space constructed from the symmetry they represent. To make sense of â€œfelt forces,â€ we have to be very careful about what spaces we are talking about. If an object is traversing a geodesic in spacetime, it will feel no force. However, if, in following a geodesic through a fiber bundle, it deviates from a spacetime geodesic, it will experience a â€œfelt force.â€ We will unpack this as we get deeper into this chapter. As alluded to already, we will generalize the idea of â€œstraightâ€ in â€œflat spaceâ€ to â€œstraightest possible,â€ or geodesical, in â€œcurved space.â€ This is nothing more in essence than the idea that following lines of longitude on earth, or more generally â€œgreat circles,â€ or geodesics, on the surface of a sphere. We want to call such a path â€œstraightâ€ because it is the shortest possible path between two points. This informal definition of â€œstraightest possibleâ€ contains two elements that we can use to rigorously define *parallel transport*. The first element is that the space has an invariant structure derived from symmetry that allows an agreed upon definition local definition of length. The second element is that what we intuitively see as â€œstraightestâ€ or â€œsimplestâ€ arises from *extremizing* (often â€œminimizingâ€) the integral of the invariant length over a path. We will make the bridge from geometry to physics by taking care to build our invariant structure from physical symmetry. Before we do that, letâ€™s â€œdo a little geometryâ€ to make sure these ideas are well grounded. We will show how minimizing length in flat space defines a straight line and how doing the same on a sphere defines a geodesic.

### Using Extremization to Find Geodesics 

Letâ€™s start with a straight line in flat space.

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
L\lbrack x,y\rbrack = \int_{\lambda_{1}}^{\lambda_{2}}\sqrt{\left( \frac{dx}{d\lambda} \right)^{2} + \left( \frac{dy}{d\lambda} \right)^{2}}\text{â€‰}d\lambda.
```

Define

``` math
\dot{x} = \frac{dx}{d\lambda},\dot{y} = \frac{dy}{d\lambda},\ \ \ \ \ \ R = \sqrt{{\dot{x}}^{\text{â€‰}2} + {\dot{y}}^{\text{â€‰}2}}.
```

Then

``` math
L\lbrack x,y\rbrack = \int_{\lambda_{1}}^{\lambda_{2}}{R\text{â€‰}d\lambda.}
```

Now require that this functional (function of functions) be stationary under small variations of the curve that keep the endpoints fixed.

Let

``` math
x(\lambda) \rightarrow x(\lambda) + \varepsilon\text{â€‰}\eta(\lambda),\ \ \ \ \ y(\lambda) \rightarrow y(\lambda) + \varepsilon\text{â€‰}\xi(\lambda),
```

Here:

- $`\eta(\lambda)`$ and $`\xi(\lambda)`$ are arbitrary test functions that vanishe at the endpoints\
  (so the endpoints stay fixed: $`\eta\left( \lambda_{1} \right) = \eta\left( \lambda_{2} \right) = 0,\ \ \ \ \xi(\lambda_{1}) = \xi(\lambda_{2}) = 0`$)

- $`\varepsilon`$ is an infinitesimal number that controls the size of the change

Then

``` math
\dot{x} \rightarrow \dot{x} + \varepsilon\text{â€‰}\dot{\eta},\dot{y} \rightarrow \dot{y} + \varepsilon\text{â€‰}\dot{\xi}.
```

The varied length is

``` math
L(\varepsilon) = \int_{\lambda_{1}}^{\lambda_{2}}\sqrt{\left( \dot{x} + \varepsilon\dot{\eta})^{2} + (\dot{y} + \varepsilon\dot{\xi})^{2} \right.\ }\text{\:\,}d\lambda.
```

Differentiate with respect to $`\varepsilon`$ and evaluate at $`\varepsilon = 0`$:

``` math
{\frac{dL}{d\varepsilon} \mid}_{\varepsilon = 0} = \int_{\lambda_{1}}^{\lambda_{2}}\frac{\dot{x}\text{â€‰}\dot{\eta} + \dot{y}\text{â€‰}\dot{\xi}}{\sqrt{{\dot{x}}^{\text{â€‰}2} + {\dot{y}}^{\text{â€‰}2}}}\text{\:\,}d\lambda.
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
\int_{\lambda_{1}}^{\lambda_{2}}\frac{\dot{x}\text{â€‰}\dot{\eta}}{R}\text{â€‰}d\lambda = \left\lbrack \frac{\dot{x}}{R}\eta \right\rbrack_{\lambda_{1}}^{\lambda_{2}} - \int_{\lambda_{1}}^{\lambda_{2}}\frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right)\eta\text{â€‰}d\lambda.
```

The boundary term vanishes because $`\eta(\lambda_{1}) = \eta(\lambda_{2}) = 0`$.

Similarly for $`y`$. Therefore the stationarity condition becomes

``` math
\int_{\lambda_{1}}^{\lambda_{2}}\left\lbrack - \frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right)\eta - \frac{d}{d\lambda}\left( \frac{\dot{y}}{R} \right)\xi \right\rbrack d\lambda = 0.
```

Because $`\eta\`$and $`\xi`$can be any functions that vanish at the endpoints, the only way the integral can be zero for all such choices is for the coefficients of $`\eta`$and $`\xi`$to vanish pointwise. $`\frac{d}{d\lambda}\left( \frac{\dot{x}}{R} \right) = 0,\ \ \ \ \frac{d}{d\lambda}\left( \frac{\dot{y}}{R} \right) = 0.`$*\*

Define $`A,B`$:

``` math
\frac{\dot{x}}{\sqrt{{\dot{x}}^{\text{â€‰}2} + {\dot{y}}^{\text{â€‰}2}}} = A,\ \ \ \ \frac{\dot{y}}{\sqrt{{\dot{x}}^{\text{â€‰}2} + {\dot{y}}^{\text{â€‰}2}}} = B.
```

Square and add:

``` math
A^{2} + B^{2} = 1.
```

From the first equation,

``` math
\dot{x} = A\sqrt{{\dot{x}}^{\text{â€‰}2} + {\dot{y}}^{\text{â€‰}2}}.
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

Letâ€™s sketch how we would modify the procedure above to show that geodesics on a sphere are the shortest possible paths in that space.

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image442.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image443.png)

![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image444.png)![](C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image445.png)

Figure 54 - Geodesics on a sphere

The procedure proceeds just as for a line in flat space except that our invariant metric change from:*\*
$`ds^{2} = dx^{2} + dy^{2}`$

to:\
``` math
ds^{2} = R^{2}\left( d\theta^{2}+{\sin}^{2}\theta\text{â€‰}d\phi^{2} \right)
```

After carrying out the procedure, we find that:\
\
``` math
{\ddot{\theta} - \sin{\theta\cos{\theta\text{â€‰}{\dot{\phi}}^{2}}} = 0,\ \ \ \ \ \ \ \ \ddot{\phi} + 2\cot\theta\text{â€‰}\dot{\theta}\text{â€‰}\dot{\phi} = 0
}
{which\ are\ the\ equations\ for\ a\ geodesic\ on\ a\ sphere.\ 
}
```

### From Geometry to Physics

A few observations are evident from this discussion. First, the description of curves in terms parameterized equations and their derivatives is the exact same machinery we use for describing physical trajectories. Second, we see that in flat space â€œaccelerationâ€ (second derivative) is zero, while it is non-zero in curved space. Third, the extremization approach we used is identical to the approach used in â€œLagrangian Mechanics.â€ The path length is equivalent to the â€œLagrangian,â€ the differential equations are equivalent to the â€œEuler Lagrangeâ€ equations, and the invariant distance is equivalent to the invariant Minkowski metric on spacetime.\
\
We can now simply reappropriate this approach to find that a inertial path in spacetime is a straight world line. First, we write down the Lagrangian. For a free particle in spacetime, take the Lagrangian proportional to the invariant interval:

``` math
L = - mc\text{â€‰}\sqrt{- \text{â€‰}\eta_{\mu\nu}\text{â€‰}{\dot{x}}^{\mu}{\dot{x}}^{\nu}}
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
\frac{\partial L}{\partial{\dot{x}}^{\mu}} = \frac{m\text{â€‰}\eta_{\mu\nu}{\dot{x}}^{\nu}}{\sqrt{- \eta_{\alpha\beta}{\dot{x}}^{\alpha}{\dot{x}}^{\beta}}}.
```

With proper time parametrization the denominator is constant, giving

``` math
\frac{d^{2}x^{\mu}}{d\tau^{2}} = 0.
```

This is precisely the statement that in flat spacetime, a free particle follows a straight worldline. We will now see how extending this procedure to curved spacetime leads to General Relativity and its explanation of gravity.

