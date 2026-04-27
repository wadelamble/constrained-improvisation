## From the Lagrangian to Canonical Momentum

If Hamiltonian Mechanics is to reveal structure in the instantaneous state, then it must first ask whether the Lagrangian snapshot of a system is already the right one. At an instant, Lagrangian Mechanics seems to give us two pieces of data, the configuration \(q^i\) and the velocity \(\dot q^i\). For describing a path, this is enough. Velocity tells us how configuration changes along the trajectory. But the question now is not only how the path proceeds. It is what object, at the level of the state itself, naturally answers to an infinitesimal displacement.

A displacement \(\delta q^i\) is a small move in configuration space. To pair naturally with such a move, one wants an object that acts linearly on displacements. That is already a different kind of thing from a rate of change along a path. Velocity is tangent data. It tells us how the system is moving. But the variational structure is asking what quantity is conjugate to a small change in position. If Hamiltonian Mechanics is to expose hidden structure in instantaneous state, it cannot stop with \(q\) and \(\dot q\) simply because those were the variables in which the trajectory was first written.

The right place to look is the action itself. For

```math
S[q] = \int_{t_1}^{t_2} L(q,\dot q,t)\,dt,
```

the variation of the action, after integrating by parts, takes the form

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

The bulk term gives the Euler-Lagrange equations. But for present purposes the crucial fact is the endpoint term. The action itself singles out the quantity

```math
\frac{\partial L}{\partial \dot q^i}
```

as the object that naturally contracts with a displacement \(\delta q^i\). Canonical momentum is therefore not introduced by taste, convenience, or later hindsight. It is already latent in the variational principle as the object conjugate to displacement at the boundary.

Only now do we define

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

This should not be read first as a sophisticated way of saying \(mv\), though in simple cases it reduces to that familiar quantity. Its structural meaning comes earlier. The displacement \(dq^i\) is the little move. The momentum \(p_i\) is what pairs with that move. The word canonical matters because this pairing is not imposed from outside. It is selected by the action itself.

This is also the right point at which to understand the beginning of the Legendre move. The Lagrangian starts as a function of \(q\) and \(\dot q\). But once the variation has exposed \(p_i = \partial L/\partial \dot q^i\) as the quantity conjugate to displacement, the state is no longer most naturally described as position together with a mere rate of change. The Legendre transformation does not create the pairing. The action has already done that. What the Legendre move does is re-express the instantaneous state in terms of configuration and the dual variable that the variational structure has already selected.

So the gain of this section is modest but decisive. The instantaneous state is no longer best understood as \(q\) together with \(\dot q\). It has been reorganized into \(q\) together with \(p\), position together with its canonically paired response to displacement. That is the threshold we needed. The next step will be to see what kind of space such states inhabit, and why the hidden geometry hinted at by Liouville becomes visible there.
