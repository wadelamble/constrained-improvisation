# Differential Mechanics

Lagrangian Mechanics gives us a remarkably deep way to formulate the laws of motion. We write down an invariant quantity in a spacetime geometry, extremize it, and recover the physical path. The particle, we may say, has "learned" what the right trajectory is by solving an optimization problem. The global formulation is conceptually prior to the local formulation in the strict sense that the central objects of the differential formulation, the quantities that will become momentum and energy in the local theory, are derived from the global formulation. 

"Hamiltonian Mechanics" is the name we give to the modern version of the local, differential perspective. Instead of selecting a whole history at once, it treats motion as the flow in time of one instantaneous state to the next. Hamiltonian mechanics is an elegant formulation of classical mechanics, but if elegance were all it provided, it would not belong here in our treatment of the conceptual foundations of physics. In fact, it does more than recast Lagrangian Mechanics in local form. It makes visible ensemble and algebraic structure that is difficult to see in Lagrangian form and that later becomes essential to quantum mechanics. First, it reveals how statistical ensembles evolve in ways not visible from individual trajectories. Second, by encoding laws of global trajectories into the local geometry of infinitesimal state changes, it allows those laws to be expressed in an algebra of generators.

## The Evolution of Ensembles in Physical Systems

One might justifiably think that the content of our physical laws is limited to predicting individual trajectories from initial conditions. Yet in conservative systems, where energy is not dissipated into inaccessible microscopic degrees of freedom, the laws guiding the evolution of single states additionally imply that the information encoded in a distribution of states is preserved. This is a categorically different kind of claim, not about one particle's initial conditions and its future, but about the collective behavior of an ensemble. The key to this emergent structure is that deterministic, reversible evolution keeps distinct initial states distinct. Once that is true, an ensemble can move through state space without losing the measure of how many states it contains.

### Example: Preserved Information in a Permutation

We can get a feel for this kind of information-preserving evolution with a simple discrete example. Take a deck of three cards labeled `A`, `B`, and `C`. The exact possible states are the six deck orders

```text
ABC, ACB, BAC, BCA, CAB, CBA.
```

Now choose one specific permutation of these states, for example, move the top card to the bottom. Then

```text
ABC -> BCA
BCA -> CAB
CAB -> ABC
ACB -> CBA
CBA -> BAC
BAC -> ACB
```

Now assign a probability distribution on these six exact states. For example,

```text
P(ABC) = 1/2
P(BAC) = 1/3
P(CBA) = 1/6
```

with all other states assigned probability `0`. After applying the permutation to all arrangements consistent with the distribution, the distribution becomes

```text
P(BCA) = 1/2
P(ACB) = 1/3
P(BAC) = 1/6
```

with all other states still assigned probability `0`. The same probability weights are still present. They have only been reassigned to different exact states.

![Three-card permutation animation contact sheet](animations/liouville-permutation-3card-contact-sheet.png)

[Open MP4: liouville-permutation-3card.mp4](animations/liouville-permutation-3card.mp4)

A few structural facts are worth making explicit:
1. An initial arrangement is unique.
2. Under a given permutation rule, a new arrangement is dictated by the previous arrangement.
3. We can run the permutation in reverse and recover the original arrangement.
4. Two arrangements under the same number of permutations remain distinct.

These properties, which we will show exist in physical situations, are what we mean by "determinism" and "reversibility" and, following from these, by "distinguishability" of the ensemble under time evolution.

We can map the elements of the card deck to Hamiltonian mechanics. There, the relevant state space is the space of positions and momenta together. This is phase space. For one body, it is position/momentum space. For many bodies, it is the product of such spaces.

1. An arrangement -> an instantaneous state
2. All possible arrangements -> phase space
3. The count of distinct arrangements in a collection -> phase space area

The last of these elements is what we call a "measure" on the space. A measure has a role analogous to a metric, though it does something different. A metric measures separation. A measure assigns size to regions or collections. What matters here is whether that size is preserved as the system evolves. In the card deck, preservation is built in. The law is a permutation, so a collection of arrangements can be rearranged, but it cannot gain or lose members. Conservative physical systems have the continuous analogue of that property. We can visualize this as state space becoming "incompressible."

### Example: Preserved Information in a Physical Ensemble

We see this same structure in conservative physical systems such as the ideal pendulum. Prepare many runs with slightly different initial angles and momenta. At the initial time, measurements across the ensemble reveal a distribution in phase space. We then let each member of the ensemble evolve under the same conservative law, and at some later time we again measure position and momentum across the ensemble. Those later measurements reveal a new distribution. Again, the distribution is not flattened or sharpened by the dynamics. Rather, each exact initial state in the ensemble is carried to one exact later state, so the later distribution is the earlier one transported by the law of motion. In a dissipative system, nearby runs can truly be driven together, so distinctions among initial conditions are washed out. The extreme example of such a dissipative system is one in which all initial conditions end at rest. But in a conservative system, such distributions are not washed out. They are transported to new regions of state space.

![Pendulum regimes animation contact sheet](animations/differential-pendulum-regimes-contact-sheet.png)

[Open MP4: differential-pendulum-regimes.mp4](animations/differential-pendulum-regimes.mp4)

The two animations emphasize different features of the same example. One separates the pendulum's regimes; the other follows a small ensemble through the same state space.

![Pendulum ensemble phase-space animation contact sheet](animations/differential-pendulum-ensemble-phase-space-contact-sheet.png)

[Open MP4: differential-pendulum-ensemble-phase-space.mp4](animations/differential-pendulum-ensemble-phase-space.mp4)

The pendulum is an analogue of the permutation example. There, the state space was a finite set, the natural measure was counting measure, and the law was a permutation. Here, the state space is continuous. Its points are instantaneous angle/momentum states, its natural measure is a measure of area on state space, and its law of motion is a Hamiltonian flow. A permutation rearranges exact states without merging them. A Hamiltonian flow does the same for a continuum of exact states. Area in state space plays the role that counting measure played before. In conservative physical systems, this behavior is known as Liouville's theorem. Formally, if $\Phi_t$ is the Hamiltonian time-evolution map and $A$ is any measurable region of phase space, then

```math
\mu(\Phi_t(A)) = \mu(A),
```

where $\mu$ is the natural measure on phase space.

### Information as an Incompressible Fluid

In the examples above, we looked at spaces of possible arrangements. A useful analogy is a planar incompressible flow. Imagine marking out a connected patch in the plane and then tracking that same patch as it is carried by the flow. The patch may be stretched into a long filament, bent, folded, or sheared almost beyond recognition. But it does not tear, split, or change its area. It remains the same material patch, carried along by the flow.

In our card example, exact states were permuted. In the pendulum ensemble example, exact initial conditions were carried by a Hamiltonian flow. Here, a material patch is carried by the velocity field of the fluid. In all three cases, the law transports a structured object without erasing its structure. A distribution over states or a marked material patch may be rearranged or distorted, but it remains distinguishable from a different starting distribution or patch.

Fluids make the geometric character of this structure easier to see. A planar flow is described by a velocity field. If a point at position $(x,y)$ has velocity $(u(x,y),v(x,y))$, then its motion is governed by

```math
\frac{dx}{dt} = u(x,y),\qquad \frac{dy}{dt} = v(x,y),
```

and incompressibility means

```math
\frac{\partial u}{\partial x} + \frac{\partial v}{\partial y} = 0.
```

The two terms measure the rate at which a small material patch carried by the flow expands or contracts along the two coordinate directions. If their sum is zero, any expansion in one direction is exactly balanced by contraction in the other, so a small material patch does not locally change area. In two dimensions this condition has a powerful consequence. There exists a scalar function $\psi(x,y)$ such that

```math
u = \frac{\partial \psi}{\partial y},
\qquad
v = -\frac{\partial \psi}{\partial x}.
```

In two dimensions, incompressibility lets the velocity field be generated from this single scalar function in a cross-coupled form. Motion in the $x$ direction is determined by how the scalar function $\psi$ varies in the $y$ direction, and motion in the $y$ direction is determined by how $\psi$ varies in the $x$ direction. Hamiltonian Mechanics shares this cross-coupled differential structure.

![Incompressible fluid patch animation contact sheet](animations/differential-incompressible-fluid-patch-contact-sheet.png)

[Open MP4: differential-incompressible-fluid-patch.mp4](animations/differential-incompressible-fluid-patch.mp4)

### Embodied Information
We have described systems as evolving "information." The term may sound metaphorical, as information feels like an abstract rather than a physical notion. But it is meant literally. Information cannot exist without some embodiment, be that in switches in a computer or molecules in a gas. To understand how physical systems embody information, we need to understand a bit about information theory itself.

How much information does a penny showing heads contain? A good way to think about this is as a question about surprise. If a coin were weighted so that heads always appeared, seeing heads would contain no information at all. If it showed heads 90% of the time, seeing heads would confirm what I already expected, and would therefore contain only a small amount of information. But if it came up tails, it would force a revision of my expectations. That is the sense in which it would be informative. Let us call this quantity "surprisal." We want surprisal to go up as probability goes down.

We also want information to count independent distinctions additively. If one fair coin toss resolves one binary uncertainty, then two independent fair coin tosses resolve two such uncertainties. We do not want to say that the second coin makes the information four times larger simply because the joint probability of two heads is $1/4$. The number of possible outcomes multiplies, but the number of independent binary distinctions adds. This is why an 8-bit register is said to hold 8 bits, even though it can realize $2^8$ possible bit strings. These two requirements are met by defining the information content of an outcome using a base-2 logarithm:

```math
I(H) = -\log_2 P(H),
```

When the probability of heads is 50%, this is exactly 1 bit. If the probability increases, it goes down. If it decreases, it goes up. Moreover, the information from 2 heads adds:

```math
I(HH) = -\log_2\big(P(H)P(H)\big) = -\log_2 P(H) - \log_2 P(H) = 2I(H).
```

This quantity describes the information associated with one realized outcome. When we turn from one outcome to an ensemble, the natural scalar quantity is the average surprisal over the whole distribution. This is Shannon entropy.

The same basic idea applies to an ensemble of initial conditions in a physical system. Rather than a discrete number of possibilities, there is a continuous set, so we must deal in probability densities rather than probabilities. With this change, the expression for the ensemble entropy becomes:

```math
H[\rho] = -\int \rho(x)\log_2 \rho(x)\,d\mu,
```

where $d\mu$ is the natural measure on the space of states. In this sense, an ensemble contains a quantifiable amount of information.

Liouville's theorem implies that this entropy is preserved in ideal conservative evolution. But entropy is only a scalar summary of a distribution. Different densities can have the same entropy while assigning probability to different regions of state space. The stronger statement is that Hamiltonian evolution transports the density itself. If $\rho_0$ is the initial density, then the later density is the same probability structure carried forward by the flow. The information is embodied not merely in the number $H[\rho]$, but in the full distribution over possible states.

The information-theoretic implications of conservative systems are central to statistical mechanics. There, the exact microscopic state of a system is not practically knowable. A gas, for example, has too many microscopic degrees of freedom to track directly, and even a finite partition of phase space would leave an unfathomably large number of possible microscopic arrangements. Statistical mechanics works by replacing exact microscopic knowledge with distributions over possible states, then asking how those distributions evolve. This is what lets macroscopic quantities such as temperature, pressure, volume, and particle number be connected to underlying mechanics. The role of distribution will be ontologically promoted to the state itself in quantum mechanics, where physics is no longer organized around definite classical states, but around probability distributions over possible measurement outcomes.

## Phase Space

Phase space, or position/momentum space is the arena for Hamiltonian Mechanics. To appreciate the theory, we need to understand the nature of this space.

### From histories to states

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

As advertised, we see that the variation separates into the bulk term, which governs the equations of motion, and the boundary term, which governs the action's sensitivity to endpoint configuration displacement on a time slice.

![Bulk and boundary variation diagram](animations/differential-bulk-boundary-variation.png)

### The Definition of Momentum

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

![Relativistic boundary pairing diagram](animations/differential-relativistic-boundary-pairing.png)

So far, however, this is still a statement about how the action responds when one state is infinitesimally displaced. Liouville's theorem concerns not one state, but patches of nearby states. For that we need an object that measures phase-space area rather than endpoint sensitivity.

### From the one-form to the two-form

Thus far, the action has identified $q$ and $p$ as the correct paired variables for specifying instantaneous state. But the pairing $p_i\,\delta q^i$ is a one-form statement: it acts on one infinitesimal displacement of one state and returns the first-order change in the action. Liouville's theorem and the information story ask a different question. They concern patches of nearby states in phase space, not one displaced state at a time.

Once the action has identified $q^i$ and $p_i$ as conjugate variables, the natural oriented area element on their space is the two-form

```math
dq^i \wedge dp_i.
```

It takes in two tangent directions and returns an oriented area. Integrating it over a region of phase space measures the "count," or "amount" of states in the region. Once we have the 2-form, we can see the job of Hamiltonian mechanics as finding flows under which the area measured by the 2-form is invariant.

![One-form to two-form diagram](animations/differential-one-form-to-two-form.png)

There is also a deeper reason this two-form, rather than the boundary one-form itself, is the intrinsic object. The equations of motion are determined by the bulk term in the action and are unchanged if the Lagrangian is modified by an endpoint-only term. Such a modification shifts the boundary one-form, but leaves the two-form unchanged. This matches the physics: Hamiltonian flows will preserve area in phase space, not any notion of length or absolute endpoint accounting.

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

### What Phase Space Is

We are now able to define phase space. It is the space whose points are instantaneous states expressed in the paired, or conjugate, variables selected by the action. For one degree of freedom, a point is $(q,p)$. For many degrees of freedom, a point is $(q^1,\dots,q^n,p_1,\dots,p_n)$. Phase space is a reorganization of what counts as an instantaneous state with respect to action extremization. Once the boundary variation has told us what variable is paired with $q$, the state is no longer most naturally described by $(q,\dot q)$, but by $(q,p)$.

## Hamiltonian Flows

Compare phase space plots to spacetime diagrams $Galilean or Minkowskian$. There, motion is baked into the shape of the worldline. The history is contained in a static plot. In phase space, there is no motion, no history, until a point or region begins to flow. Our next task, then, is to describe the flows that characterize conservative physical systems. The function that encodes flow in phase space, the flow of state through time, is the formulation's eponymous function, the Hamiltonian. Let's see how we can arrive at its form and the equation.

![Worldline to phase-space bridge diagram](animations/differential-worldline-phase-space-bridge.png)

### Functions on phase space

We have already seen in our example of an incompressible fluid that any flow can be encoded by a generating function. Let's spell this out more carefully and put it in the arena of phase space.

Picture a contour map on the $q,p$ plane. The value of a function, $F(q(t),p(t))$, assigns a height to each point. This 3-dimensional "hilly" picture can, as with topographic maps, be represented in 2 dimensions with contours, or level sets. Now, we have a rule that the denser the level sets are, equivalently, the steeper the surface is, the faster the flow along that contour. This flow can then be represented as a vector field, that is, a phase-space velocity arrow at every point.

![Function-to-flow animation contact sheet](animations/differential-function-to-flow-contact-sheet.png)

[Open MP4: differential-function-to-flow.mp4](animations/differential-function-to-flow.mp4)

The way to turn $F$'s level set density into such a vector field is:

```math
\dot q^i = \frac{\partial F}{\partial p_i},
\qquad
\dot p_i = -\frac{\partial F}{\partial q^i}.
```

These cross-coupled equations are the dynamical face of the same pairing that appeared geometrically as $dq^i \wedge dp_i$. What there showed up as an oriented area form here shows up as motion in one direction driven by variation in the other.

One can work through this visually step by step to convince themselves it works, but the way it works can be thought of simply as taking the function gradient vector and turning it 90 degrees to create the flow.

In phase space with one degree of freedom, if the vector field is

```math
\dot q = \frac{\partial F}{\partial p},
\qquad
\dot p = -\frac{\partial F}{\partial q},
```

then we can solve these differential equations for $q(t)$ and $p(t)$ to find the flow.

A trivial example is $F=p$. Then

```math
\dot q = 1,
\qquad
\dot p = 0.
```

And integrating gives

```math
q(t) = q_0 + t,
\qquad
p(t) = p_0.
```

We see in these cross-coupled differential equations the shadow of symplectic area preservation:

```math
\omega = dq^i \wedge dp_i
```

Change of $F$ in the $p_i$ direction determines motion in the $q^i$ direction. Change of $F$ in the $q^i$ direction determines motion in the $p_i$ direction, with a minus sign.

We can define a flow this way for any two variables, but it only has a physical interpretation in the kinds of cases we've discussed, like fluid flow, that is, in cases where the area form is preserved.

### Preservation of the Symplectic Area Form

Let's now show a bit more rigorously that such a flow does in fact preserve the symplectic 2-form. In one degree of freedom, preserving $\omega$ means preserving the area of phase-space patches. A small quadrilateral may shear, stretch, or rotate, but its area must not change.

![Symplectic patch preservation animation contact sheet](animations/differential-symplectic-patch-preservation-contact-sheet.png)

[Open MP4: differential-symplectic-patch-preservation.mp4](animations/differential-symplectic-patch-preservation.mp4)

Let's first be precise in saying what $\omega$ is. It is a measure of the count of states. If we imagine phase space as a discrete lattice, it counts the number of nodes in a patch. If we were to "squeeze" that patch, the node count would stay the same, thus the 2-form would measure the same area. (If we think of the continuous case as a lattice with infinite node density, then "squeezing" becomes impossible, and our area measure becomes, in fact, a measure of area on a plot of phase space.) Thus the only way for an area patch to increase is for states to enter or exit it, that is, for there to be some source or sink of states, which in turn implies that the flow generated by $F$ has a non-zero divergence. But we can see that this flow has zero divergence. For the flow generated by $F$,

```math
\frac{\partial \dot q^i}{\partial q^i}
+
\frac{\partial \dot p_i}{\partial p_i}
=
\frac{\partial}{\partial q^i}\left(\frac{\partial F}{\partial p_i}\right)
-
\frac{\partial}{\partial p_i}\left(\frac{\partial F}{\partial q^i}\right).
```

Since mixed partial derivatives agree,

```math
\frac{\partial^2 F}{\partial q^i \partial p_i}
-
\frac{\partial^2 F}{\partial p_i \partial q^i}
=
0.
```

The divergence vanishes:

```math
\frac{\partial \dot q^i}{\partial q^i}
+
\frac{\partial \dot p_i}{\partial p_i}
=
0.
```

Thus, any smooth function on phase space preserves our area 2-form, which, as we have discussed, is the condition for maintaining the information structure of an ensemble.

We should note that we have shown this by choosing a set of coordinates first, describing flows, then showing these preserve our 2-form. This is a bit unsatisfying for two reasons. First, logically, we would prefer to show that having a conserved 2-form defines Hamiltonian flows because our procedure for defining the flows tacitly presupposed symplectic geometry. Second, to demonstrate consistency of a flow with the preservation of the 2-form, we had to commit to a coordinate system, whereas one can show Hamiltonian flows arise from the 2-form without choosing coordinates. The approach of defining flows from the area form is readily doable, but makes the geometric intuition more opaque and requires learning some dedicated language from differential geometry.

### The Hamiltonian as Energy

We have already seen the deep connection between energy and time in Relativity. In relativity, the action for a free particle is built from spacetime length:

```math
S = -m \int ds = -\int E\,dt + \int p_x\,dx + \int \cdots
```

In this picture, 4-momentum is the covector, or 1-form, that measures the contribution of a displacement in spacetime to action. And energy is the component that measures the contribution of a time displacement.

![Action decomposition diagram](animations/differential-action-decomposition.png)

We are attempting to find the function to generate the flow in phase space that represents time evolution. Since that evolution is dictated by an action extremization principle, we may suspect this function would be related to the form that measures the effect of a time displacement on action accumulation.

In fact this is exactly right. Ignoring important exceptions that don't change the spirit of the structure, the Hamiltonian function we wish to find is the energy function. One may say somewhat poetically "energy generates time."

### Hamilton's Equations of Motion from the Legendre Transform

Once the variables $(q,p)$ have been identified, the next task is to find the function on phase space that generates the physical time-evolution flow. The Lagrangian is not yet that function. It is written as

```math
L(q,\dot q),
```

so it still treats velocity as an independent variable. The function we want must instead be written on phase space:

```math
H(q,p).
```

The Legendre transform is the operation that performs this trade. It uses the momentum relation we have established:

```math
p_i = \frac{\partial L}{\partial \dot q^i}
```

to replace the velocity variables by their conjugate momenta, while carrying the position variables along. The transformed function is

```math
H(q,p) = p_i\dot q^i - L(q,\dot q),
```

with $\dot q$ understood, when possible, as a function of $(q,p,t)$ determined by the momentum equation above.

![Legendre transform trade diagram](animations/differential-legendre-transform-trade.png)

We can do a quick test that $H$ is indeed the total energy by looking at a free particle.

For a non-relativistic free particle,

```math
L(q,\dot q) = \frac{1}{2}m\dot q^2.
```

The conjugate momentum is therefore

```math
p = \frac{\partial L}{\partial \dot q} = m\dot q,
```

so

```math
\dot q = \frac{p}{m}.
```

Substituting this into the Legendre transform gives

```math
H(q,p) = p\dot q - L(q,\dot q)
= p\left(\frac{p}{m}\right) - \frac{1}{2}m\left(\frac{p}{m}\right)^2
= \frac{p^2}{m} - \frac{p^2}{2m}
= \frac{p^2}{2m}.
```

But this is exactly the kinetic energy of the particle. So in this simplest case, the Legendre transform gives the energy function directly.

The importance of this construction is not only that it rewrites the function in the desired variables. In the earlier phase-space discussion, we saw what differential structure a function must have if it is to generate a flow. We now want to see that the Legendre-transformed function has exactly that structure. Taking the differential of $H$ gives

```math
dH
=
\dot q^i\,dp_i
+
p_i\,d\dot q^i
-
\frac{\partial L}{\partial q^i}\,dq^i
-
\frac{\partial L}{\partial \dot q^i}\,d\dot q^i
```

Now use the definition

```math
p_i = \frac{\partial L}{\partial \dot q^i}.
```

The $d\dot q^i$ terms cancel. What remains is

```math
dH
=
\dot q^i\,dp_i
-
\frac{\partial L}{\partial q^i}\,dq^i
```

At this stage the transform has done its essential job. Velocity is no longer appearing as an independent differential. The theory has been rewritten in phase-space terms.

To connect this with the original dynamics, use the Euler-Lagrange equations:

```math
\frac{d}{dt}\frac{\partial L}{\partial \dot q^i}
=
\frac{\partial L}{\partial q^i}.
```

Since $p_i = \partial L/\partial \dot q^i$, this becomes

```math
\dot p_i = \frac{\partial L}{\partial q^i}.
```

Substituting this into the expression for $dH$ gives

```math
dH
=
\dot q^i\,dp_i
-
\dot p_i\,dq^i
```

But because $H$ is now a function of $(q,p)$, its differential is also

```math
dH
=
\frac{\partial H}{\partial q^i}\,dq^i
+
\frac{\partial H}{\partial p_i}\,dp_i
```

Matching coefficients then yields the actual point of Hamiltonian mechanics for solving classical physics problems, Hamilton's equations of motion:

```math
\dot q^i = \frac{\partial H}{\partial p_i},
\qquad
\dot p_i = -\frac{\partial H}{\partial q^i}.
```

We can check this works using the example of a simple harmonic oscillator.

The total energy, and thus the Hamiltonian is:

```math
H(q,p) = T + V = \frac{p^2}{2m} + \frac{1}{2}kq^2.
```

Hamilton's equations then give:

```math
\dot q = \frac{\partial H}{\partial p} = \frac{p}{m},
\qquad
\dot p = -\frac{\partial H}{\partial q} = -kq.
```

Using $p = m\dot q$, this becomes:

```math
m\ddot q = -kq,
```

or

```math
\ddot q + \frac{k}{m}q = 0.
```

At this point we have the local differential formulation of mechanics in hand. The next step is not to change that mechanics, but to rewrite the same structure in a new language. The flow picture we have just developed can also be expressed as an algebra of functions on phase space, and that repackaging will make further structure visible.

## Lie Algebra of Phase Space

### What we mean by an algebra

We can now re-express Hamiltonian mechanics as an algebra of functions on phase space. To say this clearly, we should first say what an algebra is. An algebra begins with some class of objects and then specifies two things: what operations may be performed on those objects, and what laws those operations satisfy. Different algebras may involve different objects, different operations, and different laws, but these differences still fall into a common taxonomy. Numbers with addition and multiplication are the familiar schoolroom example. Let us first examine that taxonomy, and then turn to the specific algebra relevant here.

#### Taxonomy of operations

| Category | Meaning | Example |
|---|---|---|
| Unary | Takes one input | Negation: $x \mapsto -x$ |
| Binary | Takes two inputs | Addition: $(x,y) \mapsto x+y$ |
| Internal | Takes allowed objects as input and returns another allowed object of the same kind | Sum of two functions is a function |
| External | Combines an allowed object with something outside the class | Scalar multiplication |

Algebras are "closed," meaning that when allowed objects are combined, the result is again an allowed object of the same kind.

#### Taxonomy of laws

| Category | Meaning | Example |
|---|---|---|
| Symmetry law | Governs what happens when inputs are swapped | Commutativity, antisymmetry |
| Grouping law | Governs what happens when an operation is repeated | Associativity |
| Linearity law | Governs behavior under sums and scalar multiples | Linearity, bilinearity |
| Compatibility law | Governs how two different operations interact | Distributive law, Leibniz rule |
| Consistency law | Governs deeper structural coherence | Jacobi identity |

### Poisson Algebra

We can now turn from this general taxonomy to the specific algebra built from functions on phase space called Poisson algebra. This does not replace the flow picture just developed. It reorganizes that same mechanics into algebraic form. In Hamiltonian mechanics, the objects will be smooth functions on phase space. These include the familiar physical quantities position, momentum, energy, and angular momentum, but also arbitrary smooth functions with no associated physical observable. At the same time, these functions define vector fields on phase space under which the variation of any other function can be found. Through the algebraic lens, one may study not only the motion of states through phase space, but also the relationships in the full space of functions defined on it. The "Poisson" algebra is the structure that organizes these functions.

A Poisson algebra belongs to the broader class of Lie algebras. In the usual symmetry setting, the finite objects are transformations that preserve some invariant quantity. For example, planar rotations preserve the Euclidean length $x^2+y^2$, and may be written as a one-parameter family of matrices $R_{\theta}$. The infinitesimal objects are the generator matrices $A$ from which the finite transformations are built. In that setting one writes

```math
R_\theta = e^{\theta A},
```

so exponentiation turns an infinitesimal generator into a parameterized family of finite transformations.

The Hamiltonian case has the same broad architecture, but with different objects. The finite objects are canonical transformations, meaning transformations of phase space that preserve the symplectic form. If we write one such family as $\phi_t$, then for each fixed value of $t$ the map $\phi_t$ is one canonical transformation, while the whole family $t \mapsto \phi_t$ is the flow. The infinitesimal objects are vector fields on phase space. Integrating such a vector field gives the corresponding flow. In this setting, integration of a differential equation plays the same structural role that exponentiation played in the matrix example: it turns an infinitesimal generator into a finite transformation.

Poisson algebra has one extra layer not usually visible in the standard matrix picture. We do not usually write the infinitesimal generators directly as vector fields. Instead, we write functions on phase space. Each smooth function $f$ determines a vector field $X_f$, and that vector field in turn determines a flow of canonical transformations. The word "generate" is therefore being used in two nearby senses: functions determine vector fields, and vector fields determine flows. The chain of objects is

```text
function -> vector field -> flow -> canonical transformations.
```

![Function-vector-field-flow-canonical-transformation stack diagram](animations/differential-function-flow-stack.png)

This is the sense in which functions participate in a Lie algebra. The bridge between the vector-field level and the function level is

```math
[X_f,X_g] = X_{\{f,g\}},
```

up to sign convention. The bracket on the left is the Lie bracket of vector fields. The bracket on the right is the Poisson bracket of functions. This identity says that the Lie algebra of infinitesimal canonical transformations persists when one passes from vector fields to the functions that encode them.

The payoff is that one can work in the flat space of infinitesimal generators rather than in the curved space of finite transformations. That is what makes an algebra possible here, and it is what makes relations and theorems available through algebraic manipulation.

#### The operations of the algebra

The objects of Poisson algebra are smooth functions on phase space. The first operations on this space are the obvious ones:

| Operation | Type | Specific operation | Result |
|---|---|---|---|
| $f+g$ | Binary, internal | Addition of functions | Another smooth function |
| $cf$ | Binary, external | Scalar multiplication | Another smooth function |
| $fg$ | Binary, internal | Pointwise multiplication of functions | Another smooth function |

These operations already make smooth functions into a familiar algebraic object. Hamiltonian mechanics adds one more binary internal operation, the Poisson bracket:

```math
\{f,g\}
=
\frac{\partial f}{\partial q^i}\frac{\partial g}{\partial p_i}
-
\frac{\partial f}{\partial p_i}\frac{\partial g}{\partial q^i}.
```

With $f$ held fixed, $\{f,g\}$ is the infinitesimal change of $g$ when the state is moved along the phase-space vector field determined by $f$. The result is again a smooth function on phase space, so the function space is closed under the bracket.

#### The laws of the algebra

The Poisson bracket is not an arbitrary new operation. It satisfies the laws that make the function space into a Lie algebra:

```math
\{af_1 + bf_2,g\}
=
a\{f_1,g\}+b\{f_2,g\},
```

and likewise in the second slot, so the bracket is bilinear.

It is antisymmetric:

```math
\{f,g\} = -\{g,f\}.
```

And it satisfies the Jacobi identity:

```math
\{f,\{g,h\}\}+\{g,\{h,f\}\}+\{h,\{f,g\}\}=0.
```

This is the Lie-bracket analogue of the kind of coherence that associativity gives in ordinary multiplication. It does not say that different nestings are equal. It says instead that the failure of the bracket to associate is controlled in a consistent way.

In addition, because the objects are still ordinary functions, the bracket is compatible with function multiplication through the Leibniz, or product, rule:

```math
\{f,gh\}=\{f,g\}h+g\{f,h\}.
```

This is the familiar product rule from calculus in a new setting. With $f$ held fixed, the operation $g \mapsto \{f,g\}$ behaves like a derivative acting on functions. The bracket does not treat the product $gh$ as an opaque whole. It acts on one factor and then on the other.

#### Physical Relationships Illuminated by Poisson Algebra

Once the Poisson bracket is in hand, physical relationships that previously had to be written as separate differential statements can be compressed into algebraic ones. The simplest example is the canonical pairing itself:

```math
\{q,p\}=1,
\qquad
\{p,q\}=-1.
```

This says that position and momentum are not just two coordinates placed side by side. They are paired in a specific algebraic way. The sign flip under reversal reflects the antisymmetry of the bracket.

The master dynamical statement is that, for any smooth function $f$ on phase space,

```math
\dot f = \{f,H\},
```

assuming $f$ has no explicit time dependence. In this form, time evolution itself becomes a bracket relation. Hamilton's equations are the special cases obtained by taking $f=q$ and $f=p$:

![Poisson algebra compression diagram](animations/differential-poisson-compression.png)

```math
\dot q = \{q,H\} = \frac{\partial H}{\partial p},
\qquad
\dot p = \{p,H\} = -\frac{\partial H}{\partial q}.
```

Conservation laws also become algebraic statements. If

```math
\{p,H\}=0,
```

then $\dot p=0$, so momentum is conserved along the Hamiltonian evolution. More generally, if

```math
\{f,H\}=0,
```

then the quantity $f$ is conserved in time.

Because the bracket is antisymmetric, the same vanishing relation may be read in reverse:

```math
\{f,H\}=0
\qquad \Longleftrightarrow \qquad
\{H,f\}=0.
```

This is the compact meeting point of the two Noether directions. Read one way, it says that $f$ is conserved under the time evolution generated by $H$. Read the other way, it says that the transformation generated by $f$ leaves $H$ unchanged. Conservation and symmetry thus appear as two readings of the same algebraic relation.

#### Look Ahead to Quantum Mechanics

This algebraic viewpoint provides a bridge from Hamiltonian mechanics into quantum mechanics. There, the classical geometry of states as points moving through phase space no longer carries over in the same direct form, and much of the new theory remains to be understood on its own terms. What does carry over cleanly is the algebraic structure of observables, generators, and their bracket relations. By replacing functions with operators and Poisson brackets with commutators, one can lift a large part of Hamiltonian structure forward before learning the geometry native to the quantum theory. The geometry changes, but the algebra transports.

![Classical-to-quantum bridge diagram](animations/differential-quantum-bridge.png)
