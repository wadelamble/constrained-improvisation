## Phase Space
In our mass on a spring example, we saw that information content is preserved and suggested some "phase space measure" that should be preserved. Given that the instantaneous state was made up of position and velocity, we might think that phase space is a position versus velocity space. This is correct for some straightforward systems in which momentum equals mass times velocity <equation>. A key insight from incompressible 2d fluids was that compression in one direction necessitates, or generates, extension in the perpendicular direction. In fact, this relationship is that of a local generator to a global symmetry action, as we have seen in our discussion of symmetry and Lie algebra. However, the correct quantities to pair are not, generally, cartesian position and velocity. <equation> A trivial example of this is that angular position may pair with angular momentum. Our mission is to find the correct quantities to pair such that each generates the other. The measure will then be the infinitesimal area formed by the differentials of the members of this pair. This area measure is called the symplectic form. <equation>

A good place to start is to observe that whatever variables we use to describe the instantaneous state are paramaterized by some common parameter. Since this is physics, that parameter is time. When we say the the symplectic area is preserved we mean preserved over time. In analogy to our 2d fluid example we said:

This condition says that a small material patch does not locally compress or expand. In two dimensions it has a powerful consequence. There exists a scalar function \(\psi(x,y)\) such that

```math
u = \frac{\partial \psi}{\partial y},
\qquad
v = -\frac{\partial \psi}{\partial x}.
```

This is the functin that generates the flow. That is, the fluid flow along the level sets of this function. <is this correct?>

We want a function in phase space that defines a flow along which the area formed by our paired dynamical variables is preserved. Energy, which, from relativistic mechanics we know generates and is conserved (excluding explicit time dependence) in time must be the correct choice as the level set of energy is the flow of time (ok, i know this is super botched now, hang with me).

But we don't know what our paired variables are, and we don't have a definition of energy for a given system yet. All we have is a Lagrangian and a procedure for extremizing action. 

The question before us is, given the Lagrangian and what we know about its role in action extremization, how can we arive at the correct paired variables and correct energy, or Hamiltonian, function.

We will accomplish this by performing a "Legendre transform" on the Lagrangian. a legendre transform maps the derivative of a function wrt to one of its variables <any one is a legendgre transformatin, but we only care about one for L??> and blah, blah, blah, what a legendre transform is. <\what i describe above and also something you said about boundary condition (in the action??)??>

Now <bot: I'm talking to you>, we can at this point -do- the transformation and declare "this gives us p and q and H." But we don't want to do that. This is the crux: we want to say -why- the Legendre transformation of the Lagrangian -should- produce the q,p,H we desire as described above.

Then we actually do the transformation.

Then we derive Hamilton's equations.

Then we step back and comment on what's in front of us.