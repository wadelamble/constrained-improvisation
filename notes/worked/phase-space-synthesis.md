## Phase Space: Current Synthesis

### 1. What this note is trying to explain

The question is not merely what phase space is by definition. The question is why a theory that begins with a Lagrangian on path space should lead us to a space of instantaneous states organized into position-momentum pairs, and why that space should carry an area measure whose preservation expresses Liouville's theorem.

The pressure points are:

1. Why are the relevant variables not simply position and velocity?
2. Why does the action, which is a quantity attached to a whole path, tell us anything about the structure of a state at one time?
3. Why does the pairing exposed by the action first appear as a `1`-form, but then matter for Liouville through a `2`-form?
4. Why should the Legendre transform of the Lagrangian be expected to produce the variables and generator we want, rather than doing so by luck?

This note records a coherent answer to those questions at the present stage of understanding.

### 2. The first shift: from whole paths to states at one time

Lagrangian mechanics begins on path space. The action

```math
S[q] = \int_{t_1}^{t_2} L(q,\dot q,t)\,dt
```

is a functional of an entire history `q(t)`.

When we vary the action and integrate by parts, we obtain

```math
\delta S
=
\int_{t_1}^{t_2}
\left(
\frac{\partial L}{\partial q^i}
-
\frac{d}{dt}\frac{\partial L}{\partial \dot q^i}
\right)\delta q^i\,dt
\;+\;
\left.
\frac{\partial L}{\partial \dot q^i}\,\delta q^i
\right|_{t_1}^{t_2}.
```

The bulk term and the boundary term have different meanings.

- The bulk term determines which paths satisfy the equations of motion.
- The boundary term determines how the action responds when the state at an endpoint is changed.

This is the first important factorization. The action is still a statement about a whole history, but the boundary variation has separated from that history the structure of the state at one time. Once the question is no longer merely "which path extremizes the action?" but also "what data at one time count as a state?", the boundary term becomes decisive.

### 3. Canonical momentum comes from the boundary response

The boundary term singles out the quantity

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

It does so because the change in action produced by an infinitesimal endpoint displacement has the form

```math
p_i\,\delta q^i.
```

This is the first-order action-response to a small change in the endpoint state. It tells us that if we ask how the action changes when the state is nudged in the `q^i` direction, the coefficient of that change is `p_i`.

So canonical momentum is not introduced by habit, or by Newtonian association with `mv`, or by later Hamiltonian hindsight. It is already selected by the variational structure itself.

This is also where the inadequacy of velocity becomes clear. Velocity tells us how configuration changes along a path. But the boundary variation is asking a different question: what quantity is paired with a small change in state at a moment? That quantity is not, in general, `\dot q^i`. It is `p_i = \partial L/\partial \dot q^i`.

For simple systems those may be proportional. In general they need not be. Generalized coordinates, angular variables, constrained systems, and field theories all make the distinction unavoidable.

### 4. Why this pairing first appears as a one-form

The pairing

```math
p_i\,\delta q^i
```

is a `1`-form statement. It acts on one infinitesimal variation of one state and returns a number. It is therefore action-flavored rather than ensemble-flavored. It tells us the first-order action-cost of one infinitesimal displacement of the state.

This is not yet the object Liouville cares about.

Liouville is not about one infinitesimal variation of one state. It is about a cloud of nearby states. A cloud cannot be represented by a single infinitesimal direction. One direction gives only a line of nearby possibilities. To speak of compression, stretching, or shear, one needs at least two independent infinitesimal directions.

That is the reason the `2`-form enters.

### 5. Why the two-form is the first ensemble object

Two independent infinitesimal variations span a little parallelogram of neighboring states. The first object that can measure the extent of such a patch is

```math
dq^i \wedge dp_i.
```

This is not merely "one more dimension" added to the `1`-form. It is the first object that can register the local size of an infinitesimal family of nearby states. In that sense it is the first genuinely ensemble-facing object in the construction.

The distinction is:

- the `1`-form measures the action-response to one infinitesimal state change
- the `2`-form measures the infinitesimal extent of a patch of nearby states

This is exactly why the `2`-form is the right kind of object for Liouville. Liouville is a statement about the preservation of such patches under time evolution.

### 6. Why the two-form is more intrinsic than the one-form

The one-form is not yet the invariant object we want. It depends on a choice of Lagrangian representative. If the Lagrangian is changed by a total time derivative, the equations of motion do not change, but the corresponding `1`-form shifts by an exact differential.

By contrast, the `2`-form built from it is insensitive to that ambiguity. It is therefore the first intrinsic local geometric object naturally extracted from the boundary pairing.

So the logic is:

- the action gives the pairing
- the pairing gives a `1`-form
- the `1`-form gives an intrinsic `2`-form
- the `2`-form is what measures infinitesimal state-space patches
- those patches are exactly the objects whose preservation is the infinitesimal content of Liouville

This is the real bridge from one path to many nearby paths.

### 7. What phase space is

Phase space is the space whose points are the instantaneous states of the system when those states are expressed in terms of the conjugate variables selected by the action.

For one degree of freedom, a point of phase space is

```math
(q,p).
```

For many degrees of freedom, it is

```math
(q^1,\dots,q^n,p_1,\dots,p_n).
```

So phase space is not "position-velocity space" by default. In simple cases the momentum variable may coincide with mass times velocity, but that is a contingent simplification. In general, the correct instantaneous state variables are those defined by the variational pairing.

### 8. The role of the Legendre transform

Once `p_i = \partial L/\partial \dot q^i` has been selected, the next question is not what momentum is, but how to rewrite the theory in terms of `q` and `p` rather than `q` and `\dot q`.

That is the role of the Legendre transform.

In the abstract one-variable case, if

```math
p = \frac{df}{dq},
```

then the Legendre transform constructs

```math
g(p) = pq - f(q),
```

with `q` understood as the variable determined by the slope relation.

The point of this construction is the cancellation in the differential:

```math
dg = p\,dq + q\,dp - df.
```

Since `df = p\,dq`, the `dq` terms cancel, and the transformed function is rewritten in terms of `dp`.

The mechanical case is exactly the same pattern, but now the transform is taken with respect to velocity rather than position. The Lagrangian is

```math
L(q,\dot q,t),
```

and we define

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

The Legendre transform is then

```math
H(q,p,t) = p_i \dot q^i - L(q,\dot q,t),
```

with `\dot q` understood, when possible, as a function of `(q,p,t)`.

Its significance is not that it mysteriously creates the correct structure. The action has already selected the correct conjugate variable. What the Legendre transform does is remove the unwanted dependence on `d\dot q` and rewrite the theory cleanly in terms of the already-selected variables.

Indeed,

```math
dH
=
\dot q^i\,dp_i
+ p_i\,d\dot q^i
- \frac{\partial L}{\partial q^i}dq^i
- \frac{\partial L}{\partial \dot q^i}d\dot q^i
- \frac{\partial L}{\partial t}dt.
```

Because

```math
p_i = \frac{\partial L}{\partial \dot q^i},
```

the `d\dot q^i` terms cancel, leaving

```math
dH
=
\dot q^i\,dp_i
- \frac{\partial L}{\partial q^i}dq^i
- \frac{\partial L}{\partial t}dt.
```

This cancellation is the whole reason the transform applies here. It is the mechanism by which the theory is rewritten from `(q,\dot q)` language into `(q,p)` language.

### 9. How the movie returns

At this stage phase space is still only a space of states. The movie has not disappeared, but it has been relocated.

Before this step, the movie was described as a path

```math
q(t)
```

in configuration space.

After this step, the movie becomes a path

```math
(q(t),p(t))
```

in phase space.

So the shift is not from dynamics to statics. It is from one way of encoding dynamics to another.

The Lagrangian picture begins with histories and derives the path. The Hamiltonian picture begins by identifying the correct instantaneous state variables and then represents the history as a flow through the space of such states.

### 10. Where the fluid analogy does and does not help

The incompressible-fluid analogy is useful, but it must be handled carefully.

What it genuinely shows is:

- the idea of a flow carrying a patch of possibilities
- rearrangement without compression
- the crossed-form pattern in the two-dimensional case

In two dimensions, an area form already has the structure needed for symplectic geometry, so a divergence-free two-dimensional flow really does have Hamiltonian form in terms of a stream function.

But this does not mean that arbitrary fluid incompressibility in three dimensions is already symplectic structure. Three-dimensional incompressible flow preserves volume, not a symplectic `2`-form. So the fluid analogy can be pressed hardest only in the two-dimensional or single-canonical-pair case.

That limitation is not a problem. It means only that the analogy is a genuine local guide, not a full derivation of Hamiltonian geometry.

### 11. What is already established, and what is not

Established:

- the action, though defined on whole paths, contains in its boundary variation the structure of the state at one time
- canonical momentum is selected there
- the phase-space `2`-form is the first object that measures infinitesimal local extent of a family of nearby states
- this makes it the right object for the Liouville story
- the Legendre transform is not an arbitrary trick, but the correct rewriting once `p` has been selected

Not yet established:

- the full Hamiltonian equations
- the full proof of Liouville from Hamiltonian form
- the complete symplectic formalism
- the final reader-facing order and compression of these ideas

What has been achieved is a coherent account of why the passage from Lagrangian paths to Hamiltonian phase space is not a change of subject but a development of structure already latent in the action.
