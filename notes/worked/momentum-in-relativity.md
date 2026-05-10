# Momentum in Relativity

For a free relativistic particle, in which there is no potential and no preferred frame, the action should be built from the worldline itself. Action is the scalar functional whose stationary value selects the physical path, so in a relativistic theory it should not depend on the inertial frame used to describe that path. Unlike Galilean geometry, Minkowski geometry combines space and time into a single invariant interval. A worldline therefore has an invariant spacetime length, rather than separate spatial and temporal measures. For a free particle, that length is the only available Lorentz-invariant quantity that distinguishes one candidate worldline from another. This also has the right physical consequence: between fixed events, the free path is the straight worldline, the path of extremal path length. The free-particle action is therefore taken to be a constant multiple of spacetime length that,

```math
S = -\alpha\int ds.
```                    

The constant $\alpha$ supplies the physical scale of the action. The geometry determines what is being measured along the worldline. The coefficient determines how that measurement enters the action.

Let $s$ measure spacetime length along the worldline, and write the unit tangent as

```math
u^\mu = \frac{dx^\mu}{ds}.
```

Varying an endpoint of the worldline changes the length, to first order, by pairing the endpoint displacement with the tangent covector. Since the action is $-\alpha$ times that length, the boundary part of the variation has the form

```math
\delta S_{\partial} \sim -\alpha u_\mu\,\delta x^\mu.
```

where the subscript $\partial$ means "boundary," so $\delta S_{\partial}$ is the boundary part of $\delta S$. The coefficient of $\delta x^\mu$ is the boundary covector:

```math
p_\mu = -\alpha u_\mu.
```

The coefficient $\alpha$ is then identified internally. Since the four-velocity has invariant norm

```math
u_\mu u^\mu = 1
```

so the momentum covector satisfies

```math
p_\mu p^\mu = \alpha^2
```

Thus $\alpha$ is the invariant magnitude of four-momentum. That invariant magnitude is the definition relativity gives to mass, so we write $\alpha=m$.

Choosing a time coordinate splits the spacetime displacement into temporal and spatial pieces. In that split,

```math
p_\mu\,\delta x^\mu = p_i\,\delta q^i - E\,\delta t,
```

If the endpoint time is held fixed, then $\delta t=0$, and the spatial part remains:

```math
p_i\,\delta q^i.
```

This is the same boundary pairing that appeared in the Lagrangian derivation of ordinary momentum. The relativistic free-particle action shows the larger spacetime form of that pairing before a time coordinate is chosen.

The mass-shell relation is the same statement written after the coefficient has been named:

```math
p_\mu p^\mu = m^2,
```

In the familiar energy-momentum split this becomes

```math
E^2 = \mathbf p^2 + m^2
```

in units with $c=1$.

By shifting to a unified spacetime, relativity ties action to worldline length, with the consequence that momentum can then be defined as the covector paired with displacement along the worldline.