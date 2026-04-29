## The Symplectic Geometry of Phase Space and Hamiltonian Dynamics

### From histories to states

Lagrangian mechanics begins on path space. The action is a functional of an entire history \(q(t)\), not of a state at one time. At first sight, that seems to make it the wrong starting point for any discussion of phase space, which is supposed to be a space of instantaneous states. The first task is therefore to explain how a theory of whole paths can contain any state-at-a-time structure at all.

Start with

```math
S[q] = \int_{t_1}^{t_2} L(q,\dot q,t)\,dt.
```

Now vary the path \(q(t)\to q(t)+\delta q(t)\). Then

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

The difficulty is the second term, because it contains \(\delta \dot q^i\) rather than \(\delta q^i\). So integrate that term by parts:

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

This is the key decomposition. The variation has separated into:

- a bulk term, which determines which paths satisfy the Euler-Lagrange equations
- a boundary term, which records how the action changes when the endpoint state is infinitesimally changed

The bulk term still belongs to the theory of whole histories. The boundary term does something new. It extracts from that whole-history formalism the action's sensitivity to changing the state at a moment. This is the first decisive shift. The action remains a statement about an entire path, but the boundary variation factors out from that path the structure of a state at one time.

`[INSERT ANIMATION LATER: a single path between t_1 and t_2, with the interior variation contributing the bulk term and the endpoint displacements contributing the boundary term.]`

### Why momentum appears

The boundary term has the form \(p_i\,\delta q^i\), with

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```
This tells us what quantity is paired with an infinitesimal change in the state at a moment. That quantity is not, in general, the velocity. Velocity answers the question of how configuration changes along a path. The boundary variation answers a different question: if the endpoint state is nudged in the \(q^i\) direction, what coefficient measures the first-order change in the action? The answer is \(p_i\).

This is why conjugate or canonical momentum should not be treated as an afterthought imported from Newtonian habit. Its role is already selected by the variational structure. At the same time, its detailed form is not arbitrary. The exact expression for \(p_i\) is determined by the Lagrangian. In simple free systems, the kinetic part of the Lagrangian is inherited from spacetime kinematics, so the role of momentum is exposed by the boundary term while the form of momentum traces back to the earlier kinematical structure.

### From the one-form to the two-form

The pairing \(p_i\,\delta q^i\) is a one-form statement. It acts on one infinitesimal variation of one state and returns a number. In that sense it is action-flavored rather than ensemble-flavored. It tells us the first-order action-response to one infinitesimal state change. That is an important fact, but it is not yet the object needed for the Liouville story.

Liouville is not about one infinitesimal variation of one state. It is about clouds of nearby states. One infinitesimal direction gives only a line of nearby possibilities. A line can certainly be moved through phase space, but in a two-dimensional phase space it has zero area and so cannot support an ordinary phase-space density. A generic ensemble must instead be represented by local patches that can tile the ambient space. That is why the first genuinely ensemble-facing object is not the one-form but the two-form

```math
dq^i \wedge dp_i.
```
It is the first local object that measures the extent of a patch of nearby states rather than the action-response to one infinitesimal displacement.

### Why the two-form is intrinsic

There is a second reason the two-form matters. The one-form is not yet fully intrinsic. If the Lagrangian is changed by adding a total time derivative, the equations of motion do not change, but the one-form extracted from the boundary term can shift. The two-form built from that pairing is insensitive to this ambiguity. It is therefore the first intrinsic local geometric object naturally extracted from the action.

The logic is now visible. The action yields a boundary pairing. The pairing yields a one-form. The one-form yields an intrinsic two-form. The two-form measures local patches of nearby states. That is the object on which a later Liouville theorem can act.

### What phase space is

Phase space can now be defined without hand-waving. It is the space whose points are instantaneous states expressed in the conjugate variables selected by the action. For one degree of freedom, a point is \((q,p)\). For many degrees of freedom, a point is \((q^1,\dots,q^n,p_1,\dots,p_n)\). This is why phase space is not, in general, position-velocity space. In simple systems momentum may be proportional to velocity, but that coincidence is not the principle.

The move to phase space is therefore not a change of subject. It is a reorganization of what counts as an instantaneous state. Once the boundary variation has told us what variable is paired with \(q\), the state is no longer most naturally described by \((q,\dot q)\), but by \((q,p)\).

### Why the Legendre transform belongs here

Once \(p_i = \partial L/\partial \dot q^i\) has been identified, the next question is how to rewrite the theory in terms of \((q,p)\) rather than \((q,\dot q)\). That is the role of the Legendre transform. It is not a trick that creates the canonical pairing. The pairing is already in hand. The transform is the device that follows that pairing and rewrites the dynamics in its terms.

The abstract pattern is simple. A Legendre transform replaces one chosen variable by its derivative-conjugate variable, while leaving any untouched variables in place as parameters. That is why the many-variable case is not a problem. In mechanics, one transforms only with respect to the velocity variables \(\dot q^i\), not with respect to the position variables \(q^i\). The transformed function is

```math
H(q,p,t) = p_i \dot q^i - L(q,\dot q,t),
```
with \(\dot q\) understood, when possible, as a function of \((q,p,t)\).

Its significance is the cancellation in the differential. Differentiating \(H\) produces terms involving \(d\dot q^i\), but because \(p_i = \partial L/\partial \dot q^i\), those terms cancel. What remains is a differential written in terms of \(dq^i\), \(dp_i\), and \(dt\). At that stage the theory has been genuinely rewritten in \((q,p)\) language. When the Euler-Lagrange equations are then substituted in, the differential takes the cross-coupled form from which Hamilton's equations can be read off. This is why the Hamiltonian matters mechanically. It is not merely a new function of new variables. It is the function whose differential packages the same dynamics as first-order evolution on the space of instantaneous states.

### Turning the movie on

At this point the geometry has been earned, but it is still static. The next step is not a new derivation but a new picture. A point of phase space is one exact instantaneous state. As time evolves, that point traces out a curve. A family of nearby points traces out a moving patch. This is the first object on which the later Liouville story can be seen.

The fluid analogy can help here, but only lightly. What matters is not ordinary fluid space but phase space itself. One should imagine not a parcel of water in physical space, but a tiny patch of possible states being carried by the dynamics through the space of states. The patch may bend, stretch, and shear as the motion proceeds. That is the right movie with which to end this section. The full proof of what is preserved under that motion belongs next. Here the point is to have reached the arena in which that proof can even be stated.
