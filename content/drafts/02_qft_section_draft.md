# Quantum Field Theory

*Repository draft note.* This file is the first major prose pass for the QFT chapter. It is meant to read like actual chapter material, not like notebook scaffolding. This pass covers the opening movement of the chapter through the point where a relativistic classical field model has been built and justified. It stops before the momentum-basis diagonalization and full canonical quantization, which belong to the next constructional block.

## Quantum Field Theory

Relativity and quantum mechanics are the two decisive conceptual upheavals of modern physics. Relativity forces us to surrender the comfortable idea that space and time are fixed containers within which events occur. Quantum mechanics forces an even stranger surrender. It does not merely revise the geometry of experience. It revises the kind of thing a physical description is. In classical mechanics we imagine a world made of objects with positions and motions. In quantum mechanics we instead work with a state that yields probabilities for measurement outcomes. The theory is extraordinarily successful, but it leaves us with a fractured picture. Relativity tells us that influence must respect the causal structure of spacetime. Early quantum mechanics gives us a probability machine whose basic objects do not obviously live in spacetime at all. Quantum field theory is the synthesis that repairs this mismatch.

That repair is not just a matter of adding a few technical embellishments to quantum mechanics. It requires a deeper reallocation of roles. Ordinary quantum mechanics already contains states, observables, unitary evolution, momentum operators, and so on. What it does not contain, at least not in its early fixed-particle form, is a local relativistic medium of influence. Nor does it naturally account for the fact that particles can be created and destroyed. Nor does it explain why forces should arise from anything more concrete than a potential inserted into the Hamiltonian by hand. Quantum field theory answers these deficiencies by placing operator-valued observables into spacetime, and by identifying particles not as primitive little objects but as quantized excitations of fields.

This chapter therefore has a very specific task within the larger manuscript. It is not here merely to introduce a toolbox of Feynman diagrams. It is here to complete the conceptual story. We will begin by asking what, exactly, was missing from early quantum mechanics. We will then approach QFT from two sides at once. One side is ontological. Starting from ordinary quantum theory, we will move observables into spacetime and see what it means to have local operator-valued fields. The other side is constructive. We will build a simple classical field model that already respects relativistic propagation, and then prepare it for quantization. These two roads meet in the same theory. One explains what sort of object QFT says the world contains. The other gives us a concrete mechanism for quantizing that object.

In this first major block we will go as far as building the relativistic field and understanding why it has to look the way it does. That means three things. First, we must isolate the limits of early quantum mechanics without caricaturing it. Second, we must make clear what it means to attach observables to spacetime. Third, we must construct a classical field model whose equation of motion already respects finite-speed causal propagation, so that quantization will later take place on an object compatible with relativity rather than in conflict with it.

## Why early quantum mechanics is not enough

Early quantum mechanics is one of the great intellectual achievements of the twentieth century. Its inventors were not merely patching classical theory. They were inventing a new framework under severe pressure from experiment. In the process they gave us a formalism of breathtaking power. But it would be a mistake to read that success backward and pretend the original theory was already a finished ontological account of matter and interaction. It was not. It was a brilliant and partially incomplete structure whose gaps only become fully visible once one asks it to coexist with relativity and once one asks it to explain, rather than merely encode, interaction.

There are several ways to say what was missing. The simplest is that early quantum mechanics did not yet know what a particle really was. It assumed particles as operational givens. An electron was a thing that could be detected at a point, whose behavior was governed by a wave function. Light was a wave that also behaved in particle-like ways when detected. The theory was forced to live with this duality because experiment forced it there. But it did not yet push beneath the duality and ask whether both particle-like and wave-like behavior might grow out of a deeper common object. In bound systems it certainly explained discrete energy levels, because the wave function had to fit into the potential in allowed standing-wave patterns. But that is not yet the claim that free energy itself comes in countable quanta because the underlying system is a quantized field. That latter claim belongs to QFT.

A second incompleteness concerns locality. In non-relativistic quantum mechanics, the state evolves according to a law like the Schrödinger equation. That equation tells us how a complex-valued object on configuration space changes in time. It does not describe a local relay of influence from one spacetime neighborhood to the next. The state is a global object. When it evolves, it evolves as a whole. That is not a problem if one only asks the theory to predict probabilities. It becomes a conceptual problem the moment one demands that the description itself exhibit the causal structure relativity says the world has. In a relativistic world, no event may influence another outside the light cone. A theory in which the primary object is a global amplitude over configuration space does not obviously display that local causal handshake.

A third incompleteness is the fixed-particle assumption. Early quantum mechanics typically treats the number of particles as fixed. One may solve for the hydrogen atom, or for a finite set of interacting particles, but the formalism is not naturally built for processes in which particles appear or disappear. Yet in the real microscopic world such processes are routine. An excited atom emits a photon. An energetic collision creates new particles. Matter and radiation exchange quanta. A framework that presumes from the start that the particle count is fixed is too small for the world it seeks to describe.

A fourth incompleteness concerns forces and potentials. In early quantum mechanics the Hamiltonian often contains a potential that is simply written down. The electron in hydrogen feels a Coulomb potential. A particle in a box feels infinite walls. A harmonic oscillator feels a quadratic restoring force. These are legitimate models, and immensely useful ones, but the theory itself does not explain where those potentials come from. They are inputs. The force is not yet understood as arising from another dynamical field with its own spacetime existence and its own quantized excitations. QFT will not treat potentials as primitive givens in this way. It will treat them as emergent descriptions of interactions between fields.

These deficiencies are related. If a theory has no local field degrees of freedom in spacetime, then it has nowhere for influence to reside between source and detector. If it has nowhere for influence to reside, then potentials are likely to be inserted rather than explained. If it takes particles as primitive rather than as excitations of something deeper, then particle creation and annihilation are awkward add-ons rather than native possibilities. And if all of this sits inside a state-space formalism whose time evolution is global, then the relation to relativistic locality remains obscure.

It is important not to overstate the indictment. Early quantum mechanics was not useless until QFT saved it. On the contrary, it remains exactly correct in the domain where particle number is effectively fixed and where one is content to treat interactions through prescribed potentials. QFT does not abolish quantum mechanics. It contains it. The point is not that ordinary quantum mechanics is wrong. The point is that it is not the final level of description if one wants a theory that is at once quantum, relativistic, locally mediated, and able to describe changing particle number.

Seen this way, QFT is not just "quantum mechanics plus relativity." It is a reorganization of the ontology. Instead of beginning with particles and then attaching a wave function to them, it begins with fields spread over spacetime. Instead of treating particles as primitive objects, it treats them as discrete excitations of those fields. Instead of inserting forces by hand through static potentials, it describes interaction through couplings among dynamical fields. Instead of asking a global state in configuration space to shoulder the entire explanatory burden, it distinguishes between global states and local operator-valued fields.

This is why the transition to QFT is more than a technical escalation. It is a change in what kind of thing we take the world to be made of, or at least what kind of mathematical object our best theory requires in order to respect the constraints already laid down by relativity, probability conservation, and symmetry.

## Two ways into QFT

There are two complementary ways to approach quantum field theory, and both are worth keeping in view because they illuminate different aspects of the theory.

The first route begins inside ordinary quantum mechanics and asks how its observables ought to behave if the theory is to become local and relativistic. In the Schrödinger picture the state carries the time dependence while observables are fixed. In the Heisenberg picture the state is fixed while observables carry the time dependence. This shift is formally conservative. Nothing physical changes. But it teaches a crucial lesson. The observable is just as much a bearer of dynamics as the state. Once that is appreciated, it becomes natural to ask whether observables can be attached not just to moments of time but to points of spacetime. That question leads directly to local operator-valued fields. This route is the ontological one. It tells us what sort of object a quantum field is supposed to be.

The second route begins from a classical field and prepares it for quantization. Here one does not start by reinterpreting quantum observables. One starts by constructing a classical system with infinitely many coupled degrees of freedom distributed over space. One makes sure this classical system already respects relativistic propagation. One then diagonalizes it into independent modes and quantizes those modes. This route is constructive. It shows how the mathematics of field quantization actually gets built.

The two routes do not compete. They converge. The first tells us why local operator-valued fields are the right sort of entities to consider. The second tells us how such a field can be quantized in practice. If we followed only the first, QFT might remain a beautiful but abstract declaration that observables live in spacetime. If we followed only the second, QFT might look like a technical trick for quantizing infinitely many oscillators without revealing why that is exactly the structure nature seems to demand. Taken together, the routes show both why the theory is shaped as it is and how it is made to work.

In this first constructional movement we will mostly keep the second route in our hands, because it lets us build something tangible. But before turning fully to the field model, we should see more clearly what the first route is saying.

## Operators in spacetime

Ordinary quantum mechanics already gives us the raw ingredients for QFT. What changes is not the existence of operators, but their status and placement.

In the Schrödinger picture a state $|\psi(t)\rangle$ evolves in time according to

$$
i\hbar \frac{d}{dt} |\psi(t)\rangle = \hat H |\psi(t)\rangle.
$$

Observables such as position or momentum are represented by operators $\hat O$ that, unless they carry explicit time dependence, are treated as fixed. The state moves. The observables wait.

In the Heisenberg picture the same physics is written differently. One defines

$$
\hat O_H(t) = e^{i\hat H t/\hbar}\,\hat O_S\,e^{-i\hat H t/\hbar},
$$

while the state vector is fixed once and for all. Then the operator obeys

$$
\frac{d\hat O_H}{dt} = \frac{i}{\hbar}[\hat H,\hat O_H] + \left(\frac{\partial \hat O_H}{\partial t}\right)_{\text{explicit}}.
$$

This is already a profound shift in emphasis. Dynamics is no longer something that belongs only to a state. It can be carried equally well by observables.

That matters because the Schrödinger formulation tends to encourage a picture in which the state is the primary thing and everything else is derivative. In field theory that instinct becomes misleading. The state remains indispensable, but the observables must now be local. We want to talk about what can be measured at one spacetime event and how that relates to what can be measured at another. So the natural next move is to attach operators to spacetime points. Instead of one position operator and one momentum operator, we introduce a field operator $\hat\phi(x,t)$ and its conjugate momentum operator $\hat\pi(x,t)$. These are not numbers assigned to each point. They are operators associated with each point.

At equal times they obey canonical commutation relations of the form

$$
[\hat\phi(\mathbf x,t),\hat\phi(\mathbf y,t)] = 0,
$$

$$
[\hat\pi(\mathbf x,t),\hat\pi(\mathbf y,t)] = 0,
$$

$$
[\hat\phi(\mathbf x,t),\hat\pi(\mathbf y,t)] = i\hbar\,\delta^{(3)}(\mathbf x-\mathbf y).
$$

This is the field-theoretic generalization of the familiar $[\hat x,\hat p]=i\hbar$. Instead of one canonical pair for a single degree of freedom, we now have a canonical pair at each spatial point. The field is therefore an infinite-dimensional system even before quantization. Quantization does not create the infinity. The infinity is already there because a field assigns a degree of freedom to every point in space.

But the real relativistic constraint is stronger than these equal-time commutators. Relativity does not merely ask us to distinguish one time slice from another. It asks that spacelike separated observables be unable to influence one another. In operator language that requirement becomes microcausality. For suitable observables $\hat O(x)$ and $\hat O(y)$ associated with spacetime points $x$ and $y$, one demands

$$
[\hat O(x),\hat O(y)] = 0
\qquad \text{whenever } (x-y)^2 < 0.
$$

Spacelike separation means there is no frame in which one event lies in the causal future of the other. The vanishing of the commutator is the algebraic way of saying that the order of these measurements cannot matter because no physical influence can propagate from one to the other. This is one of the deepest ways relativity enters QFT. It is not a decorative requirement added after the fact. It is built into the local operator algebra.

At this stage it becomes clear why the field cannot simply be identified with a wave function. A wave function in ordinary quantum mechanics is a complex-valued amplitude over configuration space. A field operator in QFT is an observable-valued object associated with spacetime points. The two live in different conceptual slots. One is part of the state's representation. The other is part of the observable algebra.

There is, however, a useful Schrödinger-picture analogue that makes the relation less mysterious. In the Schrödinger version of a field theory, the state can be represented not as a wave function $\psi(x)$ on ordinary space, but as a wave functional $\Psi[\phi(\mathbf x),t]$ on the space of whole field configurations. Instead of asking for the amplitude that a particle sits at one point, one asks for the amplitude that the entire field has a certain shape across space. In that language the field operator acts by multiplication,

$$
\hat\phi(\mathbf x)\Psi[\phi] = \phi(\mathbf x)\Psi[\phi],
$$

while the conjugate momentum acts by functional differentiation,

$$
\hat\pi(\mathbf x)\Psi[\phi] = -i\hbar \frac{\delta}{\delta \phi(\mathbf x)}\Psi[\phi].
$$

So the same theory can be viewed from two complementary angles. In one, states live over the space of possible field configurations. In the other, operators are attached to spacetime. The field-theoretic version of the Schrödinger picture has not disappeared. It has simply become the functional picture of an infinite-dimensional system.

This is the first route into QFT in a nutshell. It begins from ordinary quantum mechanics, takes seriously the Heisenberg lesson that observables can carry dynamics, then localizes those observables in spacetime and constrains their algebra by relativistic causality. That already tells us what sort of mathematical object QFT must traffic in. But it does not yet tell us how to build one concretely. For that we turn to the second route.

## The classical field we will quantize

If a field is to serve as the basic local carrier of influence, it should already make physical sense before quantization. Quantization will later impose discrete excitation structure, commutators, and a Hilbert-space interpretation. But it would be odd to quantize a classical object whose own equation of motion already violates the relativistic structure we are trying to respect. So we begin with a classical field model whose propagation is local and whose continuum limit has exactly the right causal form.

A simple and extremely useful toy model is a one-dimensional lattice of identical masses. At each lattice site $n$ we have a single displacement variable $q_n(t)$. You can picture each mass as allowed to move only vertically while the sites themselves are arranged along a horizontal line. Neighboring masses are connected by springs of strength $K$. In addition, each mass is attached to a local tether of strength $K_0$ pulling it toward equilibrium. The neighbor springs make disturbances propagate from site to site. The local tether makes even the uniform mode cost energy. That latter fact will turn out to be the seed of a mass term.

The Lagrangian is

$$
L = \sum_n \left[
\frac{M}{2}\dot q_n^{\,2}
- \frac{K_0}{2}q_n^{\,2}
- \frac{K}{2}(q_{n+1}-q_n)^2
\right].
$$

This expression is already telling us the whole story in embryo. The kinetic term says each site has inertia. The local quadratic term says each site resists displacement even if its neighbors move with it. The nearest-neighbor term says differences between adjacent sites cost energy. Uniform motion of the whole chain is therefore not treated the same way as spatial variation along the chain.

Applying the Euler–Lagrange equation to $q_n$ gives

$$
M\ddot q_n + K_0 q_n + K(2q_n - q_{n+1} - q_{n-1}) = 0.
$$

This is the lattice equation of motion. It is local in the precise sense we want. The acceleration of site $n$ depends only on that site and its immediate neighbors. There is no instantaneous consultation with the whole lattice. Influence propagates by local coupling.

To understand what kinds of motion this system supports, use a normal-mode ansatz

$$
q_n(t) = A\,e^{i(kna - \omega t)},
$$

where $a$ is the lattice spacing. Substituting into the equation of motion yields

$$
M\omega^2 = K_0 + 2K(1-\cos ka)
           = K_0 + 4K\sin^2\!\left(\frac{ka}{2}\right).
$$

Dividing by $M$, define

$$
\omega_0^2 = \frac{K_0}{M},
\qquad
\Omega^2 = \frac{K}{M},
$$

so that the dispersion relation becomes

$$
\omega^2(k) = \omega_0^2 + 4\Omega^2\sin^2\!\left(\frac{ka}{2}\right).
$$

Every feature of later field theory is hiding in this modest formula. The $\sin^2(ka/2)$ piece comes from spatial coupling. It vanishes for the uniform mode $k=0$. The $\omega_0^2$ piece comes from the local tether. It does not vanish for the uniform mode. So even a mode with no spatial variation at all still oscillates with nonzero frequency. That is why the local tether is conceptually so important. A chain with only neighbor springs supports waves, but its uniform mode costs no spring energy because all sites move together and no spring is stretched. The local term changes that. It gives the zero-momentum mode a nonzero oscillation frequency. In the continuum relativistic interpretation, that is exactly what later becomes the rest-energy scale.

Take now the long-wavelength limit. For small $ka$,

$$
\sin\left(\frac{ka}{2}\right)\approx \frac{ka}{2},
$$

so

$$
\omega^2 \approx \omega_0^2 + \Omega^2 a^2 k^2.
$$

If we define

$$
c^2 = \Omega^2 a^2 = \frac{Ka^2}{M},
$$

then the dispersion relation becomes

$$
\omega^2 \approx \omega_0^2 + c^2 k^2.
$$

This is already the dispersion relation of a relativistic scalar field in units where later one may identify $\omega$ with energy and $k$ with momentum up to factors of $\hbar$.

Now pass from the discrete lattice to the continuum. Let $x = na$ and replace $q_n(t)$ by a continuous field $\phi(x,t)$. The second difference becomes a second spatial derivative, and the equation of motion turns into

$$
\partial_t^2 \phi - c^2 \partial_x^2 \phi + \omega_0^2 \phi = 0.
$$

In higher dimensions this generalizes to

$$
\partial_t^2 \phi - c^2 \nabla^2 \phi + \omega_0^2 \phi = 0.
$$

If we identify the characteristic propagation speed $c$ with the speed of light, and if we write the mass parameter as $m$ through $\omega_0 = mc^2/\hbar$ or simply $\omega_0 = m$ in natural units, then we have the Klein–Gordon equation

$$
\left(\partial_t^2 - c^2\nabla^2 + m^2\right)\phi = 0,
$$

or in covariant notation,

$$
(\Box + m^2)\phi = 0,
$$

with

$$
\Box = \partial_\mu \partial^\mu.
$$

This is the first decisive victory. We have not yet quantized anything. But we have built a classical field whose propagation is local, whose dispersion relation has the right relativistic form, and whose uniform mode carries a nonzero oscillation frequency that can be interpreted as a rest-energy scale. That is exactly the sort of object one would want to quantize if the goal is to reconcile quantum theory with relativistic locality.

Notice what did not happen. We did not impose relativity by decree on an arbitrary quantum system. We built a classical medium whose local couplings and continuum limit naturally produce a hyperbolic wave equation with the same sign structure as Minkowski spacetime. The theory is therefore not merely finite-speed in a vague engineering sense. Its differential operator is of the right relativistic type.

This classical field is not yet a quantum field. It is a relativistic classical field. But that is precisely the point. Quantization will later supply the operator structure, the vacuum, and the particle interpretation. Before any of that, the underlying field must already be the sort of thing whose disturbances propagate in a way compatible with spacetime.

## Why Klein–Gordon belongs and Schrödinger does not

At this point it is worth pausing to compare the equation we have just obtained with the Schrödinger equation. The contrast is not cosmetic. It is the mathematical heart of why a relativistic field theory wants a Klein–Gordon-like structure rather than an ordinary non-relativistic wave equation.

The Schrödinger equation is

$$
i\hbar \partial_t \psi
=
-\frac{\hbar^2}{2m}\nabla^2\psi + V\psi.
$$

The free Klein–Gordon equation is

$$
\partial_t^2 \phi - c^2\nabla^2 \phi + m^2\phi = 0,
$$

or, in natural units,

$$
(\partial_t^2 - \nabla^2 + m^2)\phi = 0.
$$

The difference that matters most is simple to state. The Schrödinger equation is first order in time and second order in space. Klein–Gordon is second order in both. That single structural difference places them in very different families of differential equations.

The Schrödinger equation belongs, broadly speaking, to the same mathematical family as diffusion equations. To see the analogy, ignore the potential and compare it with the heat equation

$$
\partial_t u = D\nabla^2 u.
$$

The crucial feature of such equations is not that they literally describe heat in every context. It is that they smooth and spread rather than propagate with a strict causal front. A disturbance at one point instantly develops tails everywhere else, however tiny. That is acceptable in diffusion. It is not acceptable as a fundamental relativistic propagation law.

One can make this even clearer by trying a plane-wave form. For a parabolic equation, the time dependence is not naturally oscillatory in the same way a genuine wave equation's is. The mode structure tends toward decay, growth, or immediate spreading rather than a sharply causal propagation with a characteristic cone.

By contrast, Klein–Gordon is hyperbolic. Its time and space derivatives enter on an equal footing except for the sign demanded by Minkowski geometry. That sign structure is everything.

The classification can be stated more abstractly. Elliptic equations have second-derivative terms of the same sign. They govern static balance. Parabolic equations have an asymmetric treatment of time and space and govern diffusion-like smoothing. Hyperbolic equations have the mixed-sign structure that supports wave propagation with characteristics. The Klein–Gordon operator is hyperbolic. The Schrödinger operator is not.

This is not an accident. The spacetime interval in relativity is

$$
ds^2 = c^2 dt^2 - d\mathbf x^2.
$$

Because of the minus sign, the null condition

$$
c^2 dt^2 - d\mathbf x^2 = 0
$$

has nontrivial solutions. Those solutions define the light cone. The differential operator in Klein–Gordon has exactly the same mixed-sign pattern. In spacetime geometry, that sign structure produces null directions and light cones. In the differential equation, it produces characteristic surfaces along which disturbances propagate at finite speed. The same underlying sign logic appears in both places.

So when we say that Klein–Gordon is compatible with relativity in a way the Schrödinger equation is not, we are saying something precise. We are not merely saying that one equation "feels more wave-like." We are saying that the operator

$$
\partial_t^2 - c^2 \nabla^2
$$

has the same Minkowskian signature structure as the spacetime interval itself, and that this is what confines propagation to a causal cone.

This is why the spring-lattice derivation mattered so much. It showed that a local medium in the continuum limit naturally produces exactly this kind of operator. Neighbor-to-neighbor coupling yields the spatial derivative term. Inertia yields the second time derivative. The local tether yields the mass term. Together they produce the simplest relativistic scalar field equation.

At this stage one might object that none of this yet makes the field quantum. That objection is exactly right. We have only built the correct classical stage. We have identified the sort of field equation that respects relativistic locality. But nothing yet tells us why its excitations should come in quanta, why particle number should be countable, or how local field values become operators. All of that lies ahead. The point of the present section is narrower and indispensable. If we are going to quantize a field at all, it had better be a field whose own classical propagation already respects the causal structure of spacetime. Klein–Gordon is the simplest such model.

One final remark is worth making here because it points forward. Klein–Gordon is not the full matter story. It is the simplest relativistic scalar field. Real matter fields such as the electron are not scalar. They are spinorial, and their fundamental equation is not second order in time and space but first order in both. That is the Dirac equation, and it will matter later. But this does not diminish the importance of Klein–Gordon. As a first model it isolates the central structural issue cleanly. The real lesson is not "all matter is Klein–Gordon." The real lesson is that relativistic quantum theory wants local fields whose equations of motion carry the Minkowski sign structure required for causal propagation. Klein–Gordon is the simplest place where that becomes visible without distraction.

That is enough for the first major block. We now have the problem, the two routes into the solution, the operator-in-spacetime idea, and a concrete classical relativistic field ready to be decomposed into modes and quantized.


## Working in the momentum basis

The classical field is now in hand, but in the form we currently have it the system is still awkward to quantize. In position space the lattice variables are coupled. Each site talks to its neighbors. The continuum field version tells the same story in smoother language, but the difficulty remains. A field written as $\phi(x,t)$ is not yet presented as a collection of independent degrees of freedom. If we tried to quantize it immediately in this coupled form, we would be trying to quantize an infinite system whose parts are all mixed together. That is possible in principle, but it conceals the physical structure we most want to see.

The natural next move is therefore not yet "make everything quantum," but "find the right coordinates." This is one of the most general lessons in physics and mathematics. When a system looks complicated, it is often because it is being written in a bad basis. A basis is not just a convenience for calculation. It is a way of exposing which aspects of the system are genuinely independent and which are artifacts of how we chose to describe it.

A finite-dimensional example is enough to remind us of the logic. Suppose we have a matrix $H$ acting on a vector space. In an arbitrary basis it may contain off-diagonal entries, meaning the basis vectors are mixed under the action of $H$. But if we diagonalize $H$, then in the new basis it acts independently on each basis vector:

$$
H \mathbf v_i = \lambda_i \mathbf v_i.
$$

The system has not changed. Only our coordinates have changed. Yet the new basis often reveals what the true dynamical modes of the system are. Instead of a tangled motion in the original coordinates, we get independent stretching or oscillation along special directions.

Exactly the same thing happens for fields. Position space is not usually the basis in which translation-invariant dynamics is simplest. If the system is uniform in space, then the natural modes are not localized spikes at individual sites but extended waves. That is not a mysterious choice. It follows from symmetry. A translation-invariant system should be described in a basis adapted to translations. The eigenfunctions of translation are plane waves. So the momentum basis is not merely fashionable. It is the basis singled out by spatial symmetry itself.

This is also why momentum already entered the manuscript much earlier as the generator of translations. Once that was established, a later move to a momentum-basis description of a field was almost inevitable. Translation symmetry does not just give us a conserved quantity. It gives us the natural language in which a uniform system decomposes into independent pieces.

For the lattice, assume periodic boundary conditions on a chain of $N$ sites with spacing $a$. Then the total length is $L = Na$, and the allowed wave numbers are discrete:

$$
k_m = \frac{2\pi m}{L}, \qquad m = 0,1,\dots,N-1.
$$

The displacement variables can be expanded as a discrete Fourier series:

$$
q_n(t) = \frac{1}{\sqrt{N}} \sum_k Q_k(t)\,e^{ikna}.
$$

Because the original displacement $q_n(t)$ is real, the Fourier amplitudes are not all independent. They obey the reality condition

$$
Q_{-k}(t) = Q_k^*(t).
$$

So the field is not being replaced by some unrelated object. It is being rewritten in a basis of spatial wave modes.

This expansion looks at first like a mere change of notation, but it does something profound. In position space the energy contained in the neighbor-spring term is a sum over differences such as $(q_{n+1}-q_n)^2$. These terms visibly couple adjacent sites. In the Fourier basis those couplings reorganize into independent contributions for each $k$. That is the field-theoretic analogue of diagonalizing a matrix.

To see this concretely, start with the lattice Lagrangian

$$
L = \sum_n \left[
\frac{M}{2}\dot q_n^{\,2}
- \frac{K_0}{2}q_n^{\,2}
- \frac{K}{2}(q_{n+1}-q_n)^2
\right].
$$

Insert the Fourier expansion. Orthogonality of the discrete exponentials ensures that cross terms with different $k$ values vanish when summed over $n$. The Lagrangian becomes

$$
L = \sum_k \left[
\frac{M}{2}\dot Q_k \dot Q_{-k}
- \frac{M}{2}\omega_k^2 Q_k Q_{-k}
\right],
$$

where

$$
\omega_k^2 = \omega_0^2 + 4\Omega^2 \sin^2\!\left(\frac{ka}{2}\right).
$$

The same dispersion relation that we derived earlier reappears, but now it has a new meaning. Previously it told us what frequency a mode of wave number $k$ must have. Now it tells us that each $k$-mode behaves like a simple harmonic oscillator with its own characteristic frequency $\omega_k$.

The corresponding canonical momentum is

$$
P_k = \frac{\partial L}{\partial \dot Q_{-k}} = M \dot Q_k,
$$

up to the usual bookkeeping conventions for the complex-conjugate mode pair. The Hamiltonian becomes

$$
H = \sum_k \left[
\frac{1}{2M} P_k P_{-k}
+ \frac{M\omega_k^2}{2} Q_k Q_{-k}
\right].
$$

This is the key structural simplification. The Hamiltonian is now a sum of independent oscillator Hamiltonians, one for each wave number. In position space we had an enormous coupled system. In momentum space we have a collection of decoupled normal modes.

Nothing genuinely quantum has happened yet. But this is the moment at which the path to quantization becomes conceptually transparent. A field is not an incomprehensible ocean of infinitely many coupled values. Once translation symmetry is used to choose the right basis, it becomes an infinite collection of harmonic modes. Quantizing a free field therefore means quantizing an infinite family of harmonic oscillators.

This is the real reason the momentum basis matters so much. It is not that particles "really are" momentum eigenstates in some naive metaphysical sense. It is that for a free, translation-invariant field, momentum space is the basis in which the dynamics separates into independent degrees of freedom, and independent oscillators are exactly the systems we already know how to quantize.

The continuum field tells the same story with integrals instead of sums. A real scalar field in a box can be expanded as

$$
\phi(\mathbf x,t) = \frac{1}{\sqrt{V}} \sum_{\mathbf k} Q_{\mathbf k}(t)\,e^{i\mathbf k\cdot \mathbf x},
$$

or in infinite volume,

$$
\phi(\mathbf x,t) = \int \frac{d^3k}{(2\pi)^3}\, Q_{\mathbf k}(t)\,e^{i\mathbf k\cdot \mathbf x}.
$$

For the free Klein–Gordon field, the mode amplitudes satisfy

$$
\ddot Q_{\mathbf k} + \omega_{\mathbf k}^2 Q_{\mathbf k} = 0,
$$

with

$$
\omega_{\mathbf k}^2 = \mathbf k^2 + m^2
$$

in natural units. Again the message is that each Fourier mode is a simple harmonic oscillator. The entire free field is an infinite direct sum, or in the continuum a direct integral, of such oscillators.

This is one of the reasons the transition from ordinary quantum mechanics to QFT is less alien than it first appears. We already understand the quantum harmonic oscillator. We already understand that its energies are quantized. QFT is not replacing that understanding. It is multiplying it — one oscillator for each allowed mode of the field.

Before quantization, however, it is worth noticing the shift in ontology that has already occurred. In classical mechanics one often imagines a small number of objects moving in space. In the field picture, the more natural object is the full field configuration. But when translation symmetry allows the field to be decomposed into normal modes, another picture becomes available: the field as a superposition of independent waviness-patterns, each carrying its own amplitude and phase. The same system can thus be seen in three mutually compatible ways: as local values in position space, as a global field configuration, or as a spectrum of normal modes in momentum space. QFT will use all three descriptions, each where it is most natural.

## Quantizing the modes

We are now finally in the position to quantize.

The conceptual burden has been carefully arranged so that this step will not feel like magic. We began by identifying the need for local relativistic fields. We then built a classical field whose propagation respects the causal structure of spacetime. Next we rewrote that field in the basis where its dynamics decomposes into independent modes. Each mode turned out to be a harmonic oscillator. Quantization therefore enters not as an inexplicable new decree, but as the application of a familiar quantum procedure to each independent mode of the field.

The quantum harmonic oscillator is familiar enough that it is easy to forget what is structurally remarkable about it. A classical oscillator can vibrate with any amplitude and hence any energy. A quantum oscillator still has an amplitude-like degree of freedom, but the allowed stationary energies are discrete:

$$
E_n = \hbar\omega\left(n+\frac{1}{2}\right), \qquad n=0,1,2,\dots
$$

The zero-point term $\frac{1}{2}\hbar\omega$ already tells us that the quantum system is not just a classical oscillator with some additional noise sprinkled on top. The ground state is not a state of perfect stillness. More importantly for us, the excitations come in countable steps. That discrete stepping is the pattern we now transfer to every field mode.

Take one mode of the free scalar field with wave vector $\mathbf k$. Classically it behaves as an oscillator of frequency $\omega_{\mathbf k} = \sqrt{\mathbf k^2+m^2}$. Quantum mechanically we promote its mode coordinate and mode momentum to operators obeying canonical commutation relations. For a single oscillator those would be

$$
[\hat Q,\hat P] = i\hbar.
$$

For field modes we similarly impose

$$
[\hat Q_{\mathbf k}, \hat P_{\mathbf k'}] = i\hbar\,\delta_{\mathbf k\mathbf k'}
$$

in discrete normalization, or the corresponding delta-function relation in the continuum.

At this point one could continue using $\hat Q_{\mathbf k}$ and $\hat P_{\mathbf k}$ directly, but the oscillator teaches us a more natural language. Define creation and annihilation operators by

$$
\hat a_{\mathbf k}
=
\sqrt{\frac{\omega_{\mathbf k}}{2\hbar}}\,\hat Q_{\mathbf k}
+
\frac{i}{\sqrt{2\hbar\omega_{\mathbf k}}}\,\hat P_{\mathbf k},
$$

$$
\hat a_{\mathbf k}^\dagger
=
\sqrt{\frac{\omega_{\mathbf k}}{2\hbar}}\,\hat Q_{-\mathbf k}
-
\frac{i}{\sqrt{2\hbar\omega_{\mathbf k}}}\,\hat P_{-\mathbf k}.
$$

These are chosen so that the commutation relations become

$$
[\hat a_{\mathbf k},\hat a_{\mathbf k'}^\dagger] = \delta_{\mathbf k\mathbf k'},
$$

with all other commutators vanishing. In terms of these operators the Hamiltonian takes the diagonal form

$$
\hat H = \sum_{\mathbf k} \hbar\omega_{\mathbf k}
\left(
\hat a_{\mathbf k}^\dagger \hat a_{\mathbf k}
+ \frac{1}{2}
\right),
$$

or in the continuum version the sum becomes an integral.

This expression says almost everything at once. The operator $\hat a_{\mathbf k}^\dagger \hat a_{\mathbf k}$ counts how many quanta of momentum $\mathbf k$ occupy the mode. The field is therefore not quantized by assigning tiny particles to each point in space. It is quantized by turning each normal mode into a quantum oscillator whose excitation level is integer-valued. The field’s energy comes in packets because each mode’s energy comes in packets.

The vacuum state $|0\rangle$ is defined by

$$
\hat a_{\mathbf k}|0\rangle = 0
\qquad \text{for all } \mathbf k.
$$

This means not that the field vanishes pointwise, but that every mode is in its lowest allowed quantum state. The vacuum is therefore the ground state of the whole field, not the absence of the field itself. This is a distinction that becomes crucial later. In ordinary language one says "empty space," but in QFT empty space means a state of the field, not the nonexistence of the field.

Acting once with a creation operator produces a one-quantum excitation:

$$
|\mathbf k\rangle = \hat a_{\mathbf k}^\dagger |0\rangle.
$$

Acting repeatedly produces multiparticle states:

$$
|\mathbf k_1,\mathbf k_2,\dots,\mathbf k_n\rangle
=
\hat a_{\mathbf k_1}^\dagger
\hat a_{\mathbf k_2}^\dagger
\cdots
\hat a_{\mathbf k_n}^\dagger
|0\rangle.
$$

Because the creation operators for a scalar bosonic field commute, the order does not matter. These excitations are bosons. Nothing in the notation insists that they be interpreted as little pellets localized in space. They are momentum-labeled excitations of the field. But in scattering experiments, cloud chambers, detectors, and beamlines, these excitations are exactly what present themselves as particles.

This is the point where the particle concept is genuinely recovered rather than assumed. A particle is not put in by hand as a primitive object. It appears as a one-quantum excitation above the vacuum of a field mode. A many-particle state is simply a state with occupation numbers in many modes. The theory did not begin by saying "there are particles, and by the way they have waves." It began with a field and discovered countable excitations.

That is why Fock space enters naturally here. The Hilbert space of a single fixed-number quantum system is too small. For a field, any mode can be excited zero times, once, twice, and so on. The full state space is therefore built from all occupation-number possibilities across all modes. In the bosonic case one writes basis states schematically as

$$
|n_{\mathbf k_1}, n_{\mathbf k_2}, n_{\mathbf k_3}, \dots \rangle,
$$

where each $n_{\mathbf k}$ is a nonnegative integer. This enormous Hilbert space is called Fock space. Its defining feature is that particle number is not fixed by construction. There is a zero-particle sector, a one-particle sector, a two-particle sector, and so on, all living inside one unified space. This is exactly what early quantum mechanics lacked.

One can now rewrite the field operator itself in terms of the creation and annihilation operators. For a real free scalar field,

$$
\hat\phi(\mathbf x,t)
=
\int \frac{d^3k}{(2\pi)^3}
\frac{1}{\sqrt{2\omega_{\mathbf k}}}
\left(
\hat a_{\mathbf k} e^{i\mathbf k\cdot\mathbf x - i\omega_{\mathbf k} t}
+
\hat a_{\mathbf k}^\dagger e^{-i\mathbf k\cdot\mathbf x + i\omega_{\mathbf k} t}
\right),
$$

again in natural units and with conventions depending on normalization. The important point is conceptual, not conventional. The field operator contains both annihilation and creation parts. Acting on a state, one part can lower the occupation of a mode and the other can raise it. The field is therefore the local operator whose algebra encodes the possibility of removing or adding quanta.

This compact formula repays slow reading. The exponentials are the plane-wave mode functions. The coefficients are the operators that change the mode occupation numbers. So the field is not "made of particles" in any naive bottom-up sense. Rather, the particle states are particular states of the field, and the field operator is the object that locally mediates changes among those states.

This also helps resolve a recurring conceptual worry. Earlier we said that the momentum basis is privileged for a free, translation-invariant field because it diagonalizes the Hamiltonian. But one may still ask whether the particle concept therefore exists only in the momentum basis. The right answer is subtle. The basis adapted to free propagation is indeed the momentum basis, and that is where the number operators have their cleanest interpretation. But localized wave packets can be built as superpositions of momentum eigenstates, so the particle concept is not confined to exact momentum eigenvectors. What *is* true is that "particle" in QFT is fundamentally a statement about excitation structure in the mode decomposition of a field, not a primitive label attached independently of basis. The momentum basis makes that structure visible in its simplest form.

Another way to say the same thing is this. In ordinary non-relativistic quantum mechanics one often imagines a particle first and then assigns it a wave function. In free QFT the more fundamental description is a field with quantized modes, and the one-particle sector emerges as a special subspace of the field’s full Fock space. That is why the field concept is deeper. It contains the particle concept as a derived limit, but not the other way around.

It is also now clear why changing particle number becomes natural. In a free field theory, the total particle number operator can be defined and is conserved because the Hamiltonian is just a sum of decoupled oscillators. But once fields interact, the interaction terms in the Hamiltonian will contain products of several creation and annihilation operators. Then the time evolution can mix sectors of different occupation number. In other words, particle creation and annihilation are no longer an embarrassment. They are the normal language of interacting fields. That development belongs to the next major stages of the chapter, but the groundwork is already laid here.

Before leaving the free theory, it is worth pausing over the vacuum once more, because it encodes several of the conceptual shifts at once. In classical mechanics the lowest-energy state of an oscillator would be perfect rest at zero amplitude. In quantum mechanics the uncertainty principle forbids a state with simultaneously sharp position and momentum, so the oscillator retains zero-point energy. In the field version, every mode has such a zero-point contribution. Formally, the vacuum energy is therefore

$$
E_{\text{vac}} = \frac{1}{2}\sum_{\mathbf k}\hbar\omega_{\mathbf k},
$$

which is infinite in the continuum. That infinity will require careful treatment later. For the moment, the lesson is simpler: even the quietest possible state of a quantum field is still a state of a dynamical entity with nontrivial structure. One should therefore stop imagining the vacuum as blank nothingness. It is the lowest-energy state of a field, and it is defined only relative to that field’s operator algebra and Hamiltonian.

We are now in a position to summarize what the free scalar field has taught us. A relativistic classical field, once written in the basis selected by translation symmetry, decomposes into independent harmonic modes. Quantizing those modes yields a Fock space of countable excitations. The field operator becomes a local operator-valued distribution built from creation and annihilation operators. Particle states emerge as low-occupation sectors of the field’s state space. This is already a complete answer to one of the chapter’s central questions: what is a particle in QFT? It is an excitation of a field mode, not a primitive corpuscle to which waves are later attached.

## The spaces of QFT

At this stage it becomes useful to step back and notice that QFT does not live in a single "space." One of the reasons the theory feels slippery when first encountered is that it simultaneously uses several different spaces, each carrying a different part of the physical structure. Confusion often arises because these spaces are quietly collapsed into one another in casual exposition. To keep our footing, it helps to separate them.

The first is spacetime itself. This is the arena of locality, causality, and symmetry under translations, rotations, and boosts. The field operator $\hat\phi(x)$ is attached to spacetime points. Microcausality is stated in spacetime language. The distinction between timelike, lightlike, and spacelike separation belongs here. If one asks where interactions are local, or where a detector is placed, or what it means for two events to be causally disconnected, one is talking about spacetime.

The second is momentum space. Because spatial translations are a symmetry of the free theory, momentum space is the natural space in which the free field decomposes into independent modes. Plane waves live here. The dispersion relation $\omega_{\mathbf k}^2 = \mathbf k^2 + m^2$ lives here. Creation and annihilation operators are most naturally labeled by momentum. If one asks what the free propagating modes are, or what basis diagonalizes the free Hamiltonian, one is talking about momentum space.

The third is the space of field configurations. In the functional Schrödinger picture the state is a functional $\Psi[\phi(\mathbf x)]$ on the set of all possible field shapes over space. This is the natural space in which the field operator acts by multiplication and the conjugate momentum acts by functional differentiation. If one asks what amplitudes are assigned to entire field profiles, one is talking about configuration space for the field.

The fourth is Hilbert space, and more specifically for QFT, Fock space. This is the space of quantum states. It is not a space of points in the ordinary geometric sense. It is the vector space in which superposition, inner products, amplitudes, and unitary time evolution live. Number states, one-particle states, coherent states, and vacuum all live here. If one asks what state the system is in, one is talking about Hilbert or Fock space.

These spaces are related, but they are not interchangeable. Spacetime is not Hilbert space. Momentum space is not the same thing as field-configuration space. The field operator bridges some of them. It is a local object in spacetime, but it acts on Hilbert space. The Fourier transform bridges position-space field descriptions and momentum-space mode descriptions. The functional Schrödinger representation bridges Hilbert space and field-configuration space. Much of the conceptual labor of QFT consists in learning which question belongs to which space.

This multi-space structure also helps explain why QFT can feel at once more abstract and more concrete than ordinary quantum mechanics. It is more abstract because the state space is typically a vast Fock space rather than the wave function of one particle in ordinary space. It is more concrete because observables are attached locally to spacetime points, so the theory finally says where interactions happen and how locality is enforced.

Seen in this light, the transition from ordinary quantum mechanics to QFT is not the replacement of one space by another. It is the differentiation of roles among several spaces that had previously been blurred together. Early quantum mechanics trained us to think primarily in terms of states. QFT forces us to think simultaneously about states, local operators, mode decompositions, and configuration amplitudes.

That is why the chapter has proceeded in the order it has. We began from the problem of locality and the insufficiency of a fixed-particle framework. We then moved observables into spacetime, constructed a classical field, decomposed it into momentum modes, and quantized those modes into a Fock-space structure. Each step corresponded to one of the spaces coming into focus.

The next question is then unavoidable. Once we have a quantized field with creation and annihilation operators, what do we actually compute with it? How do these operators give rise to measurable amplitudes, propagators, and scattering processes? That will be the next major block. For now, the conceptual foundation is in place. We have a local relativistic quantum field, a clear particle interpretation for its free excitations, and a map of the several spaces in which the theory simultaneously lives.


## What the theory calculates

Up to this point we have built the free field and understood what its excitations are. That already answers a major ontological question. We know what sort of object the theory contains, and we know how the particle concept re-emerges from quantized field modes. But a physical theory is not only an ontology. It is also a machine for producing numbers that can be compared with experiment. So the next question is unavoidable. Once we have field operators, vacuum, and Fock space, what do we actually calculate?

There are several possible first answers, and they are all correct at different levels. One may say that the theory calculates amplitudes for transitions between states. One may say that it calculates correlation functions of fields. One may say that it calculates propagators and scattering matrix elements. One may even say that it calculates expectation values of operators in chosen states. All of these are true, but they belong to different layers of the formalism. It is therefore worth putting them in the right order.

The most basic local objects are the field operators themselves. They act on the Hilbert space and can create or destroy excitations. But a single field operator at a single point is usually not the directly measurable quantity of most interest. What we can calculate more naturally are vacuum expectation values of products of fields, such as

$$
\langle 0|\hat\phi(x)\hat\phi(y)|0\rangle,
$$

or, more importantly in relativistic perturbation theory, time-ordered products such as

$$
\langle 0|T\{\hat\phi(x)\hat\phi(y)\}|0\rangle.
$$

These are correlation functions. They tell us how the field at one spacetime point is related to the field at another. In a loose phrase one sometimes says that they measure how an excitation inserted at one point can be felt at another. That phrase should not be taken too literally, but it points in the right direction. The correlation function is the theory’s most primitive book-keeping device for how local insertions are connected.

For the free scalar field, the time-ordered two-point function plays an especially central role. It is called the Feynman propagator:

$$
\Delta_F(x-y) = \langle 0|T\{\hat\phi(x)\hat\phi(y)\}|0\rangle.
$$

The name "propagator" is apt but also potentially misleading. It does not mean that a little classical object literally travels along a single path from $y$ to $x$. Rather, it is the kernel that encodes how the free field’s disturbance structure connects those two points inside the quantum theory. It is simultaneously a Green’s function for the field equation and a vacuum correlation function of field operators. That dual character is one of the most beautiful compressions in QFT: the same object solves the differential equation and encodes the amplitude structure of the quantum field.

To see the Green’s-function character, recall that the free Klein–Gordon operator is $(\Box + m^2)$. The Feynman propagator satisfies

$$
(\Box + m^2)\,\Delta_F(x-y) = -\,i\,\delta^{(4)}(x-y)
$$

up to convention-dependent factors. In other words, it is the inverse kernel of the free field operator. If one knows the source, one can convolve with the propagator to obtain the field produced by that source. This is exactly the Green’s-function logic already familiar from classical differential equations. The difference is that the object now also appears as a vacuum expectation value in the quantum theory.

In momentum space the same propagator takes the form

$$
\Delta_F(p) = \frac{i}{p^2 - m^2 + i\epsilon},
$$

again in a common convention. This compact expression contains several important lessons. The denominator vanishes on the mass shell, $p^2 = m^2$, which is where real free particles live. The tiny $i\epsilon$ prescription tells us how to navigate the poles when performing Fourier integrals, and therefore how causality is implemented in the time-ordered object. The propagator is not just an algebraic fraction. It is a precise rule for turning the field equation, the vacuum structure, and relativistic time ordering into a calculable kernel.

Why do products of fields show up rather than single fields? Because local interactions in QFT are encoded by products of field operators. If one wants to compute amplitudes in which particles are emitted, absorbed, scattered, or converted, one naturally ends up with expressions involving several field insertions. The theory does not begin by saying "here are particles flying in, here are particles flying out, now let us attach probabilities to their trajectories." It begins with local operator insertions and the vacuum or some chosen state. From those one builds the amplitudes for the processes that in the lab appear as beams, collisions, emissions, and detections.

For a free theory the two-point function already tells the essential story. But real physics lies in interactions. Once the Hamiltonian contains interaction terms, or equivalently once the Lagrangian contains nonlinear couplings among fields, the important objects are higher-point time-ordered correlation functions, such as

$$
\langle 0|T\{\hat\phi(x_1)\hat\phi(x_2)\cdots \hat\phi(x_n)\}|0\rangle.
$$

These are often called $n$-point functions. They are not mere mathematical decorations. They are the raw material from which scattering amplitudes and observable cross sections are extracted.

At first this may seem like an odd detour. If one wants the probability that two incoming particles scatter into two outgoing particles, why not calculate that directly? The answer is that the field formalism naturally gives us local correlation functions first. The asymptotic particle language of beams and detectors emerges from them at large times and large separations, where the states behave like collections of free particles. The theory’s local language and the laboratory’s asymptotic language are therefore not identical, and one of the technical achievements of QFT is to connect them cleanly.

This is why the free-particle Fock space was so important. In and out states are built from that free asymptotic structure. When two particles are very far apart before a collision, and when the outgoing products are very far apart after the collision, they can be described as free field excitations. Interactions matter in the middle, during the region where the fields overlap and exchange influence. So the theory naturally divides the story into three parts: a free incoming state, an interacting middle, and a free outgoing state.

If $|i\rangle$ denotes an incoming state and $|f\rangle$ an outgoing state, then the object of central interest is the transition amplitude

$$
\langle f|S|i\rangle,
$$

where $S$ is the scattering operator, or scattering matrix. The $S$-matrix is the rule that takes asymptotic free states in the far past to asymptotic free states in the far future. Once again, however, this must not be mistaken for a fundamentally particle-first ontology. The in and out states are the free-particle sectors extracted from the field theory at asymptotic times. The theory underneath remains a theory of interacting fields.

This can be stated more carefully by separating the Hamiltonian into a free part and an interaction part:

$$
\hat H = \hat H_0 + \hat H_{\mathrm{int}}.
$$

The free part defines the normal modes, the creation and annihilation operators, and the Fock space of asymptotic particles. The interaction part mixes those free modes and allows particle number to change. In the interaction picture, where the free evolution is carried by the operators and the interaction is treated explicitly, the scattering operator can be written formally as

$$
S = T\exp\left[-\,i\int d^4x\,\mathcal H_{\mathrm{int}}(x)\right],
$$

again in natural units and with conventional factors understood. Expanding this exponential produces a series of spacetime integrals over products of interaction terms. That series is what eventually becomes perturbation theory and, when drawn diagrammatically, Feynman diagrams.

Even before drawing a single diagram, one can see the logic. The interaction density is local in spacetime. The scattering operator is therefore built by integrating local interaction insertions over all spacetime. That is exactly how a local theory should work. The interaction is not attached to a single worldline or a single collision point chosen in advance. The theory sums over all possible local insertions weighted by the dynamics.

Now we can see more sharply how propagators, correlation functions, and scattering amplitudes fit together. The local interaction insertions bring down products of field operators. Evaluating vacuum expectation values of time-ordered products then requires contracting those fields pairwise in the free theory. Those contractions are propagators. Thus propagators are not ad hoc lines invented for drawing pictures. They are the two-point building blocks out of which perturbative correlation functions are assembled.

This is where one begins to understand the practical power of QFT. The theory does not require us to solve the full interacting dynamics exactly every time. Instead, it allows us to expand around a free theory whose modes we already understand. Correlation functions in the interacting theory can be built perturbatively from free propagators and local interaction vertices. The same formalism that gave us the ontology of particles as field excitations now also gives us a calculational grammar.

Still, one crucial bridge remains. Correlation functions are local field-language objects. Experiments are usually described in terms of particles entering and particles leaving. How exactly do we move from one to the other?

The deep answer is that the poles of the correlation functions know about the particle states. A one-particle excitation of mass $m$ manifests itself as a pole at $p^2=m^2$ in momentum space. More generally, the residues of the appropriate poles encode the overlap between the field operators and the asymptotic particle states. This is one of the reasons the field point of view is so powerful. Particle content is not introduced separately. It is already encoded in the analytic structure of the field correlators.

The standard formal expression of this bridge is the LSZ reduction formula. At a schematic level it says that scattering amplitudes are obtained from time-ordered correlation functions by amputating the external propagators and putting the external legs on shell. The exact formula is not important to memorize here. What matters is the conceptual content. The local field correlator contains more information than the eventual scattering amplitude. To extract the amplitude for real incoming and outgoing particles, one isolates the singular parts associated with the asymptotic one-particle states. The propagator pieces attached to the outer legs reflect the free propagation of those particles into and out of the interacting region, and these are removed to obtain the core interaction amplitude.

The phrase "amputate the external propagators" sounds grotesque the first time one hears it, but the logic is simple. A full correlation function includes both the dynamical heart of the interaction and the trivial fact that free particles propagate before and after the interaction region. If the goal is the scattering amplitude itself, one strips away those external free-propagation factors. What remains is the genuinely interacting core.

One can therefore picture the formal flow like this. The fundamental theory gives local fields. From them one computes time-ordered correlation functions. Their pole structure identifies asymptotic particle states. LSZ reduction extracts the scattering amplitudes relevant for beam experiments. Finally, squaring amplitudes and combining with phase-space factors yields observable rates and cross sections.

This is not merely a technical ladder. It reflects the layered ontology of the theory. The microscopic language is the local field. The intermediate language is the correlator. The asymptotic language is particle scattering. Each layer is real, but each answers a different kind of question.

It is worth spelling out what this means in laboratory terms. Imagine two electrons prepared far apart and directed toward one another. The experimentalist naturally describes this as a two-particle incoming state. QFT agrees, but only asymptotically. At very early times the state is well approximated by a free two-electron Fock-space state. During the interaction region the more faithful description is not "two little balls talking at a distance," but a coupled electron-photon field configuration evolving according to the interacting theory. At very late times the result again resolves into an outgoing free-particle state. The experimenter sees tracks or detector clicks corresponding to asymptotic particles. The theory underneath passes through a local field description in the middle. That is exactly the synthesis we wanted from the start.

This also helps with a common conceptual mistake. One sometimes hears that a propagator is "the amplitude for a particle to go from one point to another." That is not wrong as a mnemonic, but it can become misleading if taken too classically. A propagator is a two-point Green’s function of the field. It becomes connected to particle propagation because the field has particle poles and because the asymptotic states are one-particle excitations of that field. The field is primary. The particle language is extracted from it. Keeping that order straight prevents many later confusions.

For the free scalar field the explicit form of the propagator can be derived directly from the mode expansion. Insert

$$
\hat\phi(x)
=
\int \frac{d^3k}{(2\pi)^3}\frac{1}{\sqrt{2\omega_{\mathbf k}}}
\left(
\hat a_{\mathbf k} e^{-ik\cdot x}
+
\hat a_{\mathbf k}^\dagger e^{ik\cdot x}
\right)
$$

into the time-ordered two-point function and use the commutation relations together with the vacuum condition $\hat a_{\mathbf k}|0\rangle=0$. One finds

$$
\Delta_F(x-y)
=
\int \frac{d^4p}{(2\pi)^4}
\frac{i\,e^{-ip\cdot(x-y)}}{p^2-m^2+i\epsilon}.
$$

This compact expression is a small miracle of compression. The creation and annihilation algebra, the relativistic dispersion relation, the vacuum structure, and the causal time-ordering prescription are all packed into it.

In an interacting theory, however, life becomes richer. The exact two-point function is no longer just the inverse of the free operator. It contains corrections from the interaction. One can still think of it as a propagator, but now it carries information about self-energy corrections, renormalized masses, and the possibility that the field couples to multiparticle states. The free pole at $p^2=m^2$ broadens into a more subtle analytic structure. Yet the basic principle remains: the two-point function’s singularities tell us what the particle content of the theory is.

The higher-point functions likewise acquire interaction-dependent structure. A four-point function, for example, contains the information needed for two-to-two scattering. In a theory with a quartic scalar interaction, one may extract the tree-level scattering amplitude from the connected part of the four-point correlator after amputation and on-shell reduction. In QED, electron-electron scattering is extracted from a correlator involving the electron field and the photon field, with the internal photon propagator encoding the exchange interaction. The formalism is always the same in spirit. Local fields first, correlators next, amplitudes last.

One can now see why QFT is so naturally suited to the beam-lab setting that came to dominate twentieth-century particle physics. Beams prepare asymptotic incoming particle states. Detectors register asymptotic outgoing particle states. Between them lies an interaction region in which locality, relativity, and changing particle number must all be handled cleanly. A fixed-particle Schrödinger theory with inserted potentials is not shaped for this task. A local field theory with asymptotic Fock states is.

This is also why the chapter has insisted so strongly on not beginning with particles as primitive givens. In the beam-lab context particles are indeed what experimentalists prepare and detect. But if one begins there and stays there, one misses the underlying reason the calculation works. The local object carrying the dynamics in the middle is not the particle but the field. Particles are the asymptotic language in which the field’s excitations become experimentally legible.

At this point we have reached another important plateau. We know what the free field is, how it is quantized, what its excitations are, and what sorts of mathematical objects the interacting theory asks us to compute. We have propagators, correlation functions, and the $S$-matrix in view. The remaining question is how best to organize those calculations in practice.

One route is to continue in the operator formalism, expanding the time-ordered exponential of the interaction Hamiltonian and evaluating the resulting vacuum expectation values. That route is fully legitimate, and conceptually it remains closest to the ontology we have been building. Another route is to recast the same theory in a form that looks like a sum over field histories weighted by the action. That is the path-integral formulation. It does not replace the operator picture with a new ontology, but it reorganizes the same amplitudes in a form that often makes perturbation theory and diagrammatics more transparent.

That is the next major block.


---

## Reconstructed second major block

*Repository reconstruction note.* The next major block of the chapter is appended here explicitly as a restoration pass. Its job is to carry the argument forward from the classical relativistic field to the point where the field has been diagonalized into normal modes, quantized, and interpreted in terms of Fock space and the multiple spaces QFT uses. This block is written to preserve continuity with the opening movement of the chapter rather than to behave like an isolated essay.

## Working in the momentum basis

At the end of the first block we had a classical relativistic field, but not yet a quantum field in the full sense. The equation of motion had the right causal structure. The field was local in spacetime. Its continuum limit was Klein–Gordon rather than Schrödinger. But none of that yet told us why the field’s excitations should come in countable quanta, nor how the particle concept re-enters at all. To reach that, one more conceptual turn is needed.

The turn is not, at first, “quantize.” It is “change basis.”

This matters because the field, as written in position space, still looks like a huge coupled system. Every site in the lattice talks to its neighbors. Every small region of the continuum field is coupled to nearby regions through spatial derivatives. In that form the system is physically clear, because locality is explicit. But it is not yet in the best form for quantization, because the degrees of freedom are not separated into independent dynamical pieces. If we quantized the field in that coupled description without further preparation, the underlying structure would be harder to see than it needs to be.

A good way to say this is that the field in position space is honest but entangled. It shows us locality, but it hides independence.

This is an old story in physics. A system may look complicated in one set of variables because the chosen coordinates are badly adapted to its symmetries. The cure is not to change the physics, but to find the coordinates in which the dynamics becomes simplest. For a rotation-invariant matrix one looks for its principal axes. For a quadratic form one diagonalizes. For a vibrating string or drumhead one passes from arbitrary displacements to normal modes. For a free field with translation symmetry, one passes to momentum space.

The deeper reason is symmetry. A free, spatially uniform field is translation-invariant. If the laws are unchanged when the whole system is shifted in space, then the natural basis should be built from functions that transform simply under translations. Plane waves do exactly that. Translate a plane wave and it merely picks up a phase. That is why momentum space is not just a calculational convenience. It is the basis singled out by spatial translation symmetry itself.

This point links back to the earlier chapters in a satisfying way. Momentum was already identified there as the generator of spatial translations. So when the field later gets expanded in momentum modes, that is not an arbitrary Fourier trick imposed from the outside. It is the natural representation-theoretic continuation of the symmetry story.

For the discrete spring lattice, suppose there are $N$ sites with spacing $a$, and for simplicity impose periodic boundary conditions. Then the allowed wave numbers are discrete:

$$
k_m = \frac{2\pi m}{Na}, \qquad m=0,1,\dots,N-1.
$$

The lattice displacement can then be expanded as

$$
q_n(t)=\frac{1}{\sqrt N}\sum_k Q_k(t)e^{ikna}.
$$

Because the original displacement $q_n(t)$ is real, the Fourier coefficients obey

$$
Q_{-k}(t)=Q_k^*(t).
$$

So the new variables are not unrelated to the old ones. They are just the field rewritten in a basis of spatial wave modes.

Now comes the crucial simplification. Insert this Fourier expansion into the lattice Lagrangian. The orthogonality of the exponentials means that different wave numbers do not mix. The coupled neighbor terms in position space reorganize into independent quadratic terms in mode space. One finds a Lagrangian of the form

$$
L = \sum_k \left[\frac{M}{2}\dot Q_k \dot Q_{-k} - \frac{M\omega_k^2}{2}Q_kQ_{-k}\right],
$$

with

$$
\omega_k^2 = \omega_0^2 + 4\Omega^2\sin^2\!\left(\frac{ka}{2}\right).
$$

This is the same dispersion relation derived earlier, but its meaning has now sharpened. Earlier it told us that a disturbance of wave number $k$ oscillates with frequency $\omega_k$. Now it tells us that each $k$-mode behaves dynamically like a simple harmonic oscillator with its own characteristic frequency.

That is the hidden gift of the momentum basis. The field is no longer one giant coupled system. It is a family of independent oscillators, one for each allowed value of $k$.

The Hamiltonian makes this especially clear. If $P_k$ is the momentum conjugate to $Q_k$, then the Hamiltonian is

$$
H = \sum_k \left[\frac{1}{2M}P_kP_{-k} + \frac{M\omega_k^2}{2}Q_kQ_{-k}\right].
$$

This is just a sum of oscillator Hamiltonians. In position space the field looked like an interacting network. In momentum space the free field becomes a decoupled set of modes.

The continuum field tells the same story more elegantly. A real scalar field can be written as

$$
\phi(\mathbf x,t)=\int \frac{d^3k}{(2\pi)^3}\,Q_{\mathbf k}(t)e^{i\mathbf k\cdot \mathbf x},
$$

with the appropriate reality condition relating $Q_{-\mathbf k}$ to $Q_{\mathbf k}^*$. For the free Klein–Gordon field, each mode obeys

$$
\ddot Q_{\mathbf k} + \omega_{\mathbf k}^2 Q_{\mathbf k}=0,
$$

where

$$
\omega_{\mathbf k}^2 = \mathbf k^2 + m^2
$$

in natural units. Again, each mode is an oscillator. The free field is therefore an infinite collection of oscillators indexed by momentum.

This is one of the most important conceptual compression points in the whole chapter. It is where the field view and the particle view begin to meet. The field is primary. But once its free dynamics are diagonalized, each independent mode becomes a candidate for quantized excitation. That is the bridge to quanta.

It is also where a common confusion can be avoided. When people say that QFT “works in momentum space,” the worry sometimes arises that position and locality have somehow been abandoned. But that is not what is happening. Position space and momentum space are not rival realities. Position space remains the place where locality, sources, detectors, and microcausality are most natural. Momentum space is the place where free propagation and mode structure are simplest. A mature understanding of QFT uses both without trying to collapse one into the other.

So the chapter’s order up to this point was not accidental. We first needed locality and relativistic propagation visible in position space. Only then was it appropriate to pass to the basis in which the free dynamics separate.

## Quantizing the modes

Once the field has been decomposed into independent normal modes, quantization is no longer mysterious in form. We do not quantize an amorphous continuum all at once. We quantize each independent oscillator mode.

This is where the humble simple harmonic oscillator becomes one of the deepest prototypes in modern physics. The oscillator is not just a toy model from early quantum mechanics. It is the local grammar out of which a free bosonic field is built.

For one classical oscillator with coordinate $Q$ and momentum $P$, the Hamiltonian is

$$
H = \frac{P^2}{2M} + \frac{M\omega^2Q^2}{2}.
$$

Quantization promotes $Q$ and $P$ to operators obeying

$$
[\hat Q,\hat P]=i\hbar.
$$

One then introduces the ladder operators

$$
\hat a=\sqrt{\frac{M\omega}{2\hbar}}\hat Q + \frac{i}{\sqrt{2M\hbar\omega}}\hat P,
$$

$$
\hat a^\dagger=\sqrt{\frac{M\omega}{2\hbar}}\hat Q - \frac{i}{\sqrt{2M\hbar\omega}}\hat P,
$$

which satisfy

$$
[\hat a,\hat a^\dagger]=1.
$$

In terms of these, the Hamiltonian becomes

$$
\hat H = \hbar\omega\left(\hat a^\dagger \hat a + \frac{1}{2}\right).
$$

This form says everything essential. The operator $\hat a^\dagger \hat a$ counts excitations. The allowed energies are discrete. The ground state still carries zero-point energy. The oscillator’s dynamics are therefore not continuous in energy the way the classical oscillator’s are. They come in quanta.

Field quantization simply repeats this structure for each mode of the field.

For a scalar field mode labeled by $\mathbf k$, the mode variables become operators $\hat Q_{\mathbf k}$ and $\hat P_{\mathbf k}$, and the canonical commutators become

$$
[\hat Q_{\mathbf k},\hat P_{\mathbf k'}]=i\hbar\,\delta_{\mathbf k\mathbf k'}
$$

in discrete normalization, or the corresponding delta-function statement in the continuum. One then defines mode ladder operators $\hat a_{\mathbf k}$ and $\hat a_{\mathbf k}^\dagger$ so that

$$
[\hat a_{\mathbf k},\hat a_{\mathbf k'}^\dagger]=\delta_{\mathbf k\mathbf k'}.
$$

The Hamiltonian becomes

$$
\hat H = \sum_{\mathbf k}\hbar\omega_{\mathbf k}\left(\hat a_{\mathbf k}^\dagger \hat a_{\mathbf k} + \frac{1}{2}\right),
$$

or, in infinite volume, the sum becomes an integral over momenta.

Now the free field has become a quantum field in the first fully explicit sense. Each mode carries an integer-valued excitation level. The field’s energy therefore comes in packets because each mode’s oscillator energy comes in packets.

The vacuum state $|0\rangle$ is defined by

$$
\hat a_{\mathbf k}|0\rangle=0
\qquad \text{for all } \mathbf k.
$$

This should be read carefully. It does not mean the field vanishes everywhere. It means each mode is in its lowest allowed quantum state. The vacuum is therefore not the nonexistence of the field. It is the ground state of the field.

Acting with a creation operator produces a one-mode excitation:

$$
|\mathbf k\rangle = \hat a_{\mathbf k}^\dagger |0\rangle.
$$

Acting repeatedly gives multiparticle states:

$$
|\mathbf k_1,\mathbf k_2,\dots,\mathbf k_n\rangle
=
\hat a_{\mathbf k_1}^\dagger
\hat a_{\mathbf k_2}^\dagger \cdots
\hat a_{\mathbf k_n}^\dagger |0\rangle.
$$

Because the scalar field is bosonic, the creation operators commute, and any given mode may be occupied any nonnegative integer number of times.

This is where the particle concept re-enters, but in a transformed role. A particle is no longer something assumed at the start and then adorned with quantum behavior. It is a one-quantum excitation above the vacuum of a field mode. A many-particle state is a state with occupation numbers in multiple modes. The particle concept has therefore been derived from the field, not the field from the particle.

This is a major conceptual payoff and one the project has cared about repeatedly. It is the cleanest way to say what modern physics means when it claims that fields are more fundamental than particles. The claim does not mean that particles are unreal, nor that detectors somehow stop clicking. It means that the theory’s fundamental dynamical object is the field, and the thing detectors register as a particle corresponds to an excitation structure inside that field.

The field operator itself can now be written in terms of the creation and annihilation operators. For a real free scalar field,

$$
\hat\phi(\mathbf x,t)
=
\int \frac{d^3k}{(2\pi)^3}\frac{1}{\sqrt{2\omega_{\mathbf k}}}
\left(
\hat a_{\mathbf k}e^{i\mathbf k\cdot \mathbf x - i\omega_{\mathbf k}t}
+
\hat a_{\mathbf k}^\dagger e^{-i\mathbf k\cdot \mathbf x + i\omega_{\mathbf k}t}
\right),
$$

again up to standard normalization conventions. The important point is structural. The field operator contains a lowering part and a raising part. Acting locally, it can remove or create field quanta.

This compact expansion is where several ideas finally meet. The exponentials are the mode functions singled out by translation symmetry. The operators attached to them are the quanta-changing operators inherited from oscillator quantization. The whole expression is local in spacetime even though it is built from momentum-space modes. So the free quantum field is simultaneously:

- a local operator-valued field in spacetime,
- a superposition of momentum modes,
- and a generator of changes in occupation number inside Fock space.

This also clarifies why particle number can be flexible in QFT. For the free theory, the number operators

$$
\hat N_{\mathbf k}=\hat a_{\mathbf k}^\dagger\hat a_{\mathbf k}
$$

commute with the Hamiltonian, so particle numbers in the free modes are conserved. But once interactions are introduced, the Hamiltonian includes products of several creation and annihilation operators, and the time evolution can mix sectors of different total particle number. In other words, the formalism is structurally ready for emission, absorption, and pair creation. That possibility is not patched in from outside. It is exactly what one should expect once the theory is built on a Fock space rather than on a fixed-particle Hilbert space.

The vacuum deserves one more moment of attention. In ordinary language, “vacuum” sounds like emptiness. In QFT it means something far more precise and far less trivial: the lowest-energy state of the field. Every mode contributes its zero-point piece, so formally the vacuum energy is

$$
E_{\text{vac}} = \frac{1}{2}\sum_{\mathbf k}\hbar\omega_{\mathbf k}.
$$

This sum diverges in the continuum, which raises famous questions that must be handled later with care. But even before those issues are addressed, the conceptual lesson is already important. Empty space is not the absence of the field. It is a state of the field. That state is as structurally defined as any one-particle or many-particle state.

This is another reason the field picture is deeper than the particle picture. If one starts with particles as primitive, the vacuum tends to look like simple emptiness between them. If one starts with fields, the vacuum is immediately understood as the field’s ground state.

## Fock space

The right state space for a quantum field is therefore not the Hilbert space of one fixed-particle system. It is the direct sum of all particle-number sectors. This is Fock space.

For a bosonic field, a convenient basis is the occupation-number basis:

$$
|n_{\mathbf k_1},n_{\mathbf k_2},n_{\mathbf k_3},\dots\rangle,
$$

where each $n_{\mathbf k}$ is a nonnegative integer telling us how many quanta occupy that mode. The vacuum is the special case in which all occupation numbers vanish. One-particle states occupy one mode once. Two-particle states may occupy two different modes or the same mode twice, and so on.

This is not just a bigger warehouse of states. It is a different logical structure from the fixed-particle Hilbert spaces of early quantum mechanics. In a fixed-particle theory, the number of particles is part of the theory’s setup. In a field theory, it is part of the state. That difference is decisive.

It is now possible to say with unusual clarity why early quantum mechanics was too small. It was not merely that the equations were insufficiently relativistic. Its state space was also structurally too rigid. Real microscopic physics requires a framework in which the “how many particles are present?” question can itself have different answers in different states. Fock space provides exactly that.

There is also a nice conceptual balance here. The local field operator picture told us where the observables live: on spacetime. Fock space tells us where the states live: in the quantum state space of the field’s excitations. The distinction is essential. If one confuses the field with the state, or spacetime with Hilbert space, the subject quickly becomes foggy. QFT becomes much clearer once one sees that the theory genuinely uses both.

## The spaces of QFT

This is a good moment to stop and name the several spaces the theory is using, because much beginner confusion comes from letting them blur together.

The first is spacetime. This is where events occur, where locality is defined, where detectors are placed, and where causal order is constrained by light cones. The field operator $\hat\phi(x)$ lives here in the sense that it is attached to spacetime points.

The second is momentum space. This is where the free field diagonalizes. Translation symmetry makes plane waves the natural basis, and the momentum label $\mathbf k$ indexes the independent oscillatory modes. Creation and annihilation operators are most naturally labeled in this space.

The third is field-configuration space. In the functional Schrödinger picture, a state assigns amplitudes to whole field profiles $\phi(\mathbf x)$ across space. This is the space in which one thinks of a wave functional over all possible field shapes.

The fourth is Hilbert space, and more specifically Fock space. This is where the quantum states themselves live: vacuum, one-particle states, many-particle states, coherent states, and superpositions of all of these.

These spaces are related, but they are not the same. Spacetime is not Hilbert space. Momentum space is not field-configuration space. The field operator bridges some of them. It is local in spacetime, but it acts on Hilbert space. The Fourier transform bridges position-space and momentum-space field descriptions. The wave functional bridges Hilbert space and configuration space. QFT feels slippery partly because it is always moving among these spaces. Naming them explicitly helps keep the reader oriented.

This is also where the manuscript’s larger thematic concern with “spaces” pays off. Classical mechanics already taught us that configuration space and phase space are not the same. Quantum mechanics taught us that Hilbert space is not ordinary physical space. QFT intensifies this lesson. It forces us to keep straight a whole ecology of spaces, each carrying a different aspect of the physics.

Now the chapter is finally positioned to answer the next practical question. Once fields have been quantized and particles have reappeared as excitations, what does the theory actually calculate? What are propagators, correlators, and scattering amplitudes in this framework? That is the next major block.
