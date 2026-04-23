# Unused material

## Quantum Field Theory - Notes

### Random notes

- There’s a procedure. Quantize/operators, path integrals, propagators, S-matrix. We can’t poopoo the procedure contains the ontology, but still, trudging through the procedure on its on, is, ugh.

- What’s the “alternative” to path integral?

- Is path integral “why” action is minimized. How do path integral formulation and minimization work together if so, is there not really minimization in QFT.

- Propagators are greens functions and greens functions are inverses of what again

- Fields are force fields classical, not particle fields. Field are operators, but maybe its fair to “picture” expectation values, but expectation values of what? Not particle positions (which is tempting) right. What even is a, e.g., photon, what is a force particle.

- What is the whole “qm didn’t handle causality” argument?

- Causality =\> \[Oi(x,t), Oj(x,t)\] = 0

- local operators can be constructed from the fields

- Realizing that the energy in a quantized field comes in quantized energy packages, which in all respects behave like elementary particles, and, conversely, realizing that operators in the form of fields could be defined also when one starts up with Hilbert spaces consisting of elementary particles, it was discovered that quantized fields do indeed describe subatomic particles.

- Quantization requires that all interactions can be given in the form of a Lagrange function \[Why?\]

- relativity requires this L to be Lorentz invariant. \[This is wonderfully distilled. What else is ‘needed’ for relativity.\]

- exponents, integrals, powers, lagrangians, hamiltonians, soup!

-  the field operator inserts an excitation

-  propagators describe how that excitation spreads

-  interactions describe how excitations convert into others

- Expectation value of the field operator is zero for fix particle states – only the expectation value of the field operator squared carries observable densities

- Are propagators about continuous travel of in/out matrix elements?

- what are we saying. so suppose your x' state is the particle is at x=0 with 100% certainty. we're saying at x=\<very large\> there's a tiny amplitude and at x=\<very small\>, there a large amplitude. is that right? brief.

- This is the same as the heat diffusion equation, which likewise breaks at relativistic llimits.

- Hyperbolic\|elliptical\|parabolic PDEs, one vs two energy branches.

- The Hamiltonian determines the above. So if you have an E = p^2 hamiltonian, your screwed.

- Whole project is \|in\> -\> \|out\>, scattering matrix has elements

- Interactions arise from non-linear terms

- <span class="mark">Dispersion – the frequency response at one point depends on integrating the frequency response everywhere.</span>

- <span class="mark">Frequency is energy b/c its inverse length. Mass is inverse length. Units aside, why should this be – because of Compton wavelength?</span>

- <span class="mark">Need to define propagator in terms of matrix elements</span>

- <span class="mark">In at infinity out at infinity</span>

- <span class="mark">Lab setup (cloud chamber) mimics math. In lab do we create at a point or at a momentum? And detection?</span>

- <span class="mark">Hyperbolic PDE requirement: Lorentz-invariant field equations typically take the form1 (∂2 µ − m2 (i))φi = Fi(φ) ; ∂2 µ ≡ ∂2 x − ∂2 t .</span>

- <span class="mark">Spontaneous symmetry breaking – potential has two (or many) minima and the vacuum state just happens to be one or the other</span>

  - <span class="mark">Goldstone modes are like a field around the different-state-same-potential “valley” so they have no mass, no change in potential, no change in energy</span>

- <span class="mark">Guessing – or playing with options – value type, powers, symmetries</span>

- <span class="mark">Quantize field really means start with a lattice then take the limit.</span>

- <span class="mark">Lattice restricts DOF – but is that saying it restrict number of particles? That’s not really correct.</span>

- <span class="mark">{} -\> \[\]</span>

  - <span class="mark">Lattice of springs</span>

  - <span class="mark">Need a section on HM, including PE</span>

- <span class="mark">H/E/t special b/c you must have continuous time evolution</span>

- <span class="mark">It’s tempting to think of lattice spacing as being more particles, but particles are modes (coupled modes in position space), not the “springs”</span>

- <span class="mark">But the moment you diagonalize the system into normal modes, you have already changed what counts as a “thing.” The physical objects (masses) are no longer the natural independent motions. The normal modes are.</span>

- <span class="mark">No, you have to do the operator version. Why? Because it bakes in the right epistemology. I'm not sure how, it's just a feeling at this point. Your somehow promoting measurement rather than "the thing" to your currency. GPT: In the operator-first formulation, the theory is built out of local questions and their consistent joint statistics. The ‘field’ is a tool for generating those questions. Reality is cashed out in what can be measured, locally, without causal contradiction.</span>

- <span class="mark">Different field values buy you different (bosonic v fermionic) statistics</span>

- <span class="mark">J is a driving term. What role does it play besides computation trick? Viz a viz creation/detection</span>

- <span class="mark">Greens</span>

  - <span class="mark">the Green’s function becomes an **expectation value of field operators** Specifically</span> $`G(x - y)\text{\:\,} \longrightarrow \text{\:\,}\langle 0 \mid T\{\phi(x)\phi(y)\} \mid 0\rangle`$

  - <span class="mark"> **Free theory**: the Green’s function *is* the theory.</span>

  - <span class="mark"> **Interacting theory**: you glue Green’s functions together.</span>

  - <span class="mark"> **Feynman diagrams**: visual bookkeeping for products of Green’s functions.</span>

  - <span class="mark"> **Scattering amplitudes**: built from Green’s functions.</span>

  - <span class="mark"> **Causality**: enforced by which Green’s function you choose (retarded, advanced, Feynman).</span>

  - <span class="mark">A Green’s function answers one question:</span>

  - <span class="mark">If the field is poked here, what does the theory say happens there?</span>

  - <span class="mark">What the Green’s function did. It answered this concrete question: If I push the string at point</span> $`y`$<span class="mark">, how much does point</span> $`x`$<span class="mark">move? Then integration just added up all those little pushes.</span>

  - <span class="mark">*Try* to understand this: (□+m2)G(x−y)=δ(4)(x−y). what’s x-y, just what’s it saying</span>

  - <span class="mark">A Green’s function *is the inverse* of the field equation’s differential operator; in QFT it becomes the basic object that tells you how disturbances—or correlations—propagate through spacetime.</span>

  - <span class="mark">Why is the is driving function (f(x)) in the 4-panel animation swept out with the greens function, it seems it should be independent of it. And why is the driving function an operator on the field, and why do we even have a ‘thwack’ and a driving function, they seem like the same thing.</span>

  - <span class="mark">G(x1​,…,xn​)=⟨0∣T{ϕ(x1​)⋯ϕ(xn​)}∣0⟩</span>

  - <span class="mark">it replaces “field response” with **quantum correlation**</span>

- greens function is the sum of responses to pokes

- is greens function the position rep in a sense

- why’s it easier, why’s it a thing?

- When I poke the system what particles come out at what momentum. NOT: where is the + particle

- What do I now about the incoming state?

- This must be understood: This diagram literally stands for an integral like:

> 
> ``` math
> \int d^{4}x'd^{4}x^{''}d^{4}x^{'''}d^{4}x^{\nu}\text{\:\,}g_{123}\text{ }\lambda_{2456}\text{\:\,}G_{12}(x - x')G_{23}(x' - x^{\nu})G_{24}(x' - x^{''})G_{25}(x' - x^{'''})G_{26}(x' - x^{\nu})\text{\:\,}J_{4}(x^{''})J_{5}(x^{'''})J_{6}(x^{\nu})J_{3}(x^{\nu})
> ```

- Quantization : finite lattice, classical field, convert poisson brackets to commutators

- ?: if the path integral is “another quantization technology” what is the “quantization step” – what does the classical approach look like.

- ?: in operator picture, wave function doesn’t change. Therefore its abstraction is complete. Why even have it at that point? Relatedly, even when you add a particle you don’t change the wave function? How is that even possible?

- Relativistic solution look like regular wave equations, but instand of omega^2 - Ak^2 = B, just have omega^2 - k^2 = B

- Length is the only dimension – mass sets length from E = frequency

- No negative mass dimension coupling constant

  - ?: why? Something blows up at high energy. What? Why?

- Add in “J” – forcing functions is part of machinery of pertubative solutions, not sure how deep we need to get into it.

  - The original equation is schematically $`\left( m_{i}^{2} - \partial_{\mu}^{2})\text{ }\phi_{i}(x) = - \frac{\partial V_{\text{int}}}{\partial\phi_{i}}(\phi(x) \right)`$. What “original eq. is this? EL?

  - He adds an **external source** $`J_{i}(x)`$: $`\left( m_{i}^{2} - \partial_{\mu}^{2})\text{ }\phi_{i}(x) = \varepsilon J_{i}(x) - \frac{\partial V_{\text{int}}}{\partial\phi_{i}}(\phi(x) \right)`$

  - Why does adding the source “help”?

  - The long line $`\phi_{i}(x) = \int d^{4}y\text{ }G_{ij}(x - y)\lbrack\varepsilon J_{j}(y) - F_{j}(\varepsilon\phi^{(1)}(y) + \varepsilon^{2}\phi^{(2)}(y) + \cdots)\rbrack`$.

  - This is the origin of Feynman diagrams

  - ?: So is this assuming path integrals? Does feynman diagram \<-\> path integral

  - ?: Each term in this expansion corresponds to a tree diagram. What expansion, the integrand or the do you integrate term by term

- **Why QFT *needs* Green’s functions.** In QFT you don’t even have a classical field configuration to solve for.What you can compute are:correlation functions,responses to sources, amplitudes, Those *are* Green’s functions. So the question “why is this easier?” becomes: because there is no alternative object to compute

- In QFT, the basic objects are **Green’s functions**: $`G(x_{1},\ldots,x_{n}) = \langle 0 \mid T\{\phi(x_{1})\cdots\phi(x_{n})\} \mid 0\rangle`$

- **How interactions enter** For free fields: the two-point Green’s function is known exactly. For interacting fields: you expand perturbatively everything reduces to products of free Green’s functions. internal lines in Feynman diagrams **are Green’s function.**vertices come from interaction terms. amplitudes are integrals of products of Green’s functions

- ?: If retarded Gs are the only causals one’s what are Faynman’s Gs for?

- In QFT, Gs become primary and Gs are correlations. Gs are defined in terms of phi, so we talk about the field as being primary, but really it’s the field supporting this correlation structure that is why we start with a field

- ?: Why is \<0\|x\|0\> = 0. What’s that mean? It extends to \<0\|phi\|0\> = 0. But \<0\|phi(x)phi(y)\|0\> !=0 What’s going on here? Partial answer: \<0\|phi(x)phi(y)\|0\> is measuring correlation not averages of one operator

- **Introduce the bookkeeping parameter** $`\mathbf{\varepsilon.\ }`$He writes $`\phi_{i}(x) = \varepsilon\phi_{i}^{(1)}(x) + \varepsilon^{2}\phi_{i}^{(2)}(x) + \varepsilon^{3}\phi_{i}^{(3)}(x) + \cdots`$ . Why are the powers in ()s. ?: why expand a single linear term??

- ?: J becomes particle creation and detection. But why aren’t those the field operators themselves rather than a forcing term?

- ?: What: You compute correlation functions **as functionals of** $`J.`$ Because functional derivatives with respect to $`J`$**pull out fields** $`\frac{\delta}{\delta J(x)}\text{\:\,} \longleftrightarrow \text{\:\,}\phi(x)`$.

- Lines in FD are Gs: In equations, the same diagram would contain: $`\int d^{4}x\text{ }d^{4}y\text{\:\,}G_{ij}(x - y)\text{ }(\cdots\text{ })`$ The diagram **replaces the integral expression**.

- ?: Are the maximum dimensions allowed to the coupling constant dimension concern the same as the powers in the perturbative expansion?

- This diagram literally stands for an integral like: $`\int d^{4}x'd^{4}x^{''}d^{4}x^{'''}d^{4}x^{\nu}\text{\:\,}g_{123}\text{ }\lambda_{2456}\text{\:\,}G_{12}(x - x')G_{23}(x' - x^{\nu})G_{24}(x' - x^{''})G_{25}(x' - x^{'''})G_{26}(x' - x^{\nu})\text{\:\,}J_{4}(x^{''})J_{5}(x^{'''})J_{6}(x^{\nu})J_{3}(x^{\nu})`$*\*

- The diagrams up to this point are not particles – that requires more massaging including switching to momentum rep.

- Choosing the right Green’s function among allowable ones gives the right causal structure. (See eq. 2.8 in Hooft)

- ?: you Fourier transform, the Green’s function looks lik $`G(x - y) \sim \int d^{4}k\text{ }\frac{e^{ik \cdot (x - y)}}{k^{2} + m^{2}}`$ But the denominator is zero at certain $`k_{0}`$values (“poles”). Does this mean k is complex??

- PI = \<in\|O\|out\>

- ?: Just write out the whole equation for a scattering matrix.

- The SE isn’t non-relativistic – the Hamiltonian is. Wtf, sold a bill of goods.

- If you’re led to the inevitability of QFT, you should be able to say what it is.

- Chat “unpacking Scattering matrix has the “whole equation for S” – from an operator and path integral formulation

  - Is operator “differential,” while path integral is “global”

- Of course you have operators in the field – you have have values in the field classically.

- Leave out: fermionic vs bosonic algebra

- *It's funny. You can assume a mass field and derive a guage field. But you can also play this game of "what fields can we construct that don't blow up for some reason" and using that arrive at a photon field. Then you can say, "now couple this matter field"*

- Two routes to gauge fields

  -  **Route A**:\
    start with a phase symmetry → demand locality → introduce a gauge field

  -  **Route B**:\
    start with a well-behaved spin-1 field → enforce gauge redundancy → *discover* that matter must carry a local phase

- Why is the gauge field “redundant” but the coupled matter field is “locally symmetric”

- Non-abelian field curvature terms are the general pattern from which abelian are a degenerate case: he’s foreshadowing the non-Abelian case, where the gauge transformation includes an extra commutator term.

-   Once transformations mix components, they form a **non-Abelian group**

  - **YM** is just gauge theory for non-abelian

  - *The equations you quoted show something sharper:*

  - $`F_{\mu\nu}^{a} = \partial_{\mu}A_{\nu}^{a} - \partial_{\nu}A_{\mu}^{a} + gf^{abc}A_{\mu}^{b}A_{\nu}^{c}`$*\*

  - *This term is not optional, aesthetic, or physical intuition–driven.*

  - *It is **forced** by:*

  - *the Lie algebra*

  - *locality*

  - *covariance of* $`D_{\mu}`$

  - *So Yang–Mills is not “connection + curvature” in general — it is **connection valued in a Lie algebra**. That algebraic fact is what forces nonlinearity.*

- *Short answer first: **yes** — what you wrote before (the Behiel-style “connection / bookkeeping / local comparison” story) **is a correct folk description of Yang–Mills**. It is not wrong. But it is **structurally incomplete**, and the passage you quoted is precisely filling in what the folk story leaves implicit.*

- *Let me say exactly **what your description captures**, and then **what it necessarily omits**.*

- 

- ***What your Behiel-style description gets right***

- *Your earlier framing (which I’d summarize as):*

- *“When a local redundancy exists, comparing fields at nearby points requires extra bookkeeping; the gauge field is that bookkeeping, and curvature measures failure of consistency”*

- *is **exactly** the geometric heart of Yang–Mills.*

- *Specifically, you already had:*

- *gauge transformations as **identifications**, not physical motions*

- $`A_{\mu}`$*as a **connection**, not a force-field substance*

- $`F_{\mu\nu}`$*as **curvature / non-closure**, not a primitive object*

- *interactions as arising from **local comparison**, not added by hand*

- *All of that is genuinely Yang–Mills thinking.*

- *So: ✔ conceptually right.*

- 

- ***What the folk picture necessarily leaves out***

- *What you were doing was **ontology-first**.\
  What the text you pasted is doing is **representation-first**.*

- *That difference explains the omissions.*

- *Here are the important ones.*

- 

- ***1. You did not specify which local redundancies are allowed***

- *Your description treated “local phase / orientation” abstractly.*

- *Yang–Mills makes this precise by saying:*

- *the redundancy forms a **Lie group***

- *with **generators*** $`T_{a}`$

- *with **structure constants*** $`f^{abc}`$

- *This is not cosmetic. It fixes:*

- *how many gauge fields exist (*$`N_{V} = dimG`$*)*

- *how they mix under transformations*

- *which self-interactions are forced*

- *Without this, you can talk about a gauge field, but not **non-Abelian gauge structure**.*

- 

- ***2. You didn’t pin down why vector self-interactions appear***

- *In your folk picture, self-interactions feel like:*

- *“a natural consequence of curvature”*

- *True — but vague.*

- *The equations you quoted show something sharper:*

- $`F_{\mu\nu}^{a} = \partial_{\mu}A_{\nu}^{a} - \partial_{\nu}A_{\mu}^{a} + gf^{abc}A_{\mu}^{b}A_{\nu}^{c}`$*\*

- *This term is not optional, aesthetic, or physical intuition–driven.*

- *It is **forced** by:*

- *the Lie algebra*

- *locality*

- *covariance of* $`D_{\mu}`$

- *So Yang–Mills is not “connection + curvature” in general — it is **connection valued in a Lie algebra**. That algebraic fact is what forces nonlinearity.*

- *Your description gestured at this, but didn’t lock it down.*

- 

- ***3. You treated matter as conceptually secondary — YM doesn’t***

- *Your narrative made it sound like:*

- *first there is a gauge field, then you optionally couple matter*

- *But in the formal structure:*

- *matter fields **define representations***

- *representations determine **how*** $`T_{a}`$***act***

- *those actions determine **which covariant derivatives exist***

- *those derivatives determine **what*** $`A_{\mu}^{a}`$***even means***

- *So YM is not just “fields + coupling”. It is:*

- *a **single shared symmetry structure** acting on all fields at once*

- *Your folk picture captured the logic, but not the **tight mutual dependence**.*

- 

- ***4. You did not emphasize adjoint vs fundamental structure***

- *This is subtle but important.*

- *In the equations:*

- *matter fields transform in some representation* $`R`$

- *vector fields transform in the **adjoint representation***

- *field strength transforms homogeneously (no derivative term)*

- *That distinction is what makes:*

- $`F_{\mu\nu}^{2}`$*gauge invariant*

- $`A_{\mu}^{2}`$*not gauge invariant*

- *mass terms forbidden (without symmetry breaking)*

- *This is why YM theories look the way they do.*

- *Your folk story didn’t distinguish these layers.*

- 

- ***5. You did not foreground the closure requirement***

- *Yang–Mills is not just “local symmetry”.*

- *It is:*

- ***the unique way to realize a local Lie algebra symmetry with first-order derivatives that closes consistently***

- *The entire structure — covariant derivative, field strength, self-interactions — exists so that:*

- $`\lbrack D_{\mu},D_{\nu}\rbrack \sim F_{\mu\nu}`$*\*

- *and transforms **covariantly**.*

- *That closure condition is the algebraic backbone.\
  Your description talked about “failure to commute” conceptually, but YM shows that this is the theory.*

- 

- ***A clean verdict***

- *Your Behiel-style description is:*

- *✔ conceptually correct*

- *✔ geometrically faithful*

- *✔ ontologically honest*

- *But it is:*

- *❌ not algebraically specific*

- *❌ not representation-theoretic*

- *❌ not strong enough to derive non-Abelian structure*

- *Yang–Mills is what you get when you take your folk picture and **nail it down so hard that nothing else is allowed**.*

- 

- ***One-sentence synthesis***

- ***Your description is Yang–Mills seen from 30,000 feet; the text you quoted is what remains when you insist that every step be implementable by a Lie algebra acting locally and consistently on all fields.***

- *If you want, the next natural step is to reverse the question:*

- *Which parts of Yang–Mills survive if you throw away Lie algebras and keep only the geometric idea?*

- *That’s exactly where modern gauge-gravity and information-theoretic reformulations live.*

- 2\. The adjoint representation, definitionally

- Take a Lie group with generators $`T_{a}`$satisfying

- $`\lbrack T_{a},T_{b}\rbrack = - if_{abc}T_{c}`$

- The **adjoint representation** is the representation where:

- the generators act on *each other* by commutation.

- Concretely:

- $`(\text{ad}_{T_{a}})\text{ }T_{b} \equiv \lbrack T_{a},T_{b}\rbrack`$

- So in components, the adjoint matrices are:

- $`\left( \text{ad}_{T_{a}})_{bc} = - if_{abc} \right.\`$

- That’s it. No extra structure.

- *a way the group acts linearly on some vector space.*

- *For matter fields, that vector space is “components of the field.”\
  For the adjoint rep, the vector space is **the Lie algebra itself**.*

- *That’s the key idea.*

- 

- ***2. The adjoint representation, definitionally***

- *Take a Lie group with generators* $`T_{a}`$*satisfying*

- $`\lbrack T_{a},T_{b}\rbrack = - if_{abc}T_{c}`$*\*

- *The **adjoint representation** is the representation where:*

- *the generators act on each other by commutation.*

- *Concretely:*

- $`(\text{ad}_{T_{a}})\text{ }T_{b} \equiv \lbrack T_{a},T_{b}\rbrack`$*\*

- *So in components, the adjoint matrices are:*

- $`\left( \text{ad}_{T_{a}})_{bc} = - if_{abc} \right.\`$*\*

- *That’s it. No extra structure.*

- 

- ***3. Why gauge fields live in the adjoint rep***

- *Your gauge field is written as*

- $`A_{\mu}(x) = A_{\mu}^{a}(x)\text{ }T_{a}`$*\*

- *That is already a big clue.*

- *The coefficients* $`A_{\mu}^{a}`$*are not just labels — they are the components of a vector **in the Lie algebra direction**.*

- *So under a local gauge transformation*

- $`\Omega(x) = e^{i\Lambda^{a}(x)T_{a}}`$*\*

- *the Lie algebra itself transforms by conjugation:*

- $`T\text{\:\,} \rightarrow \text{\:\,}\Omega T\Omega^{- 1}`$*\*

- *Infinitesimally, that is:*

- $`\delta T_{a} = f_{abc}\text{ }\Lambda^{b}\text{ }T_{c}`$*\*

- *And therefore:*

- $`\delta A_{\mu}^{a} = f_{abc}\text{ }\Lambda^{b}\text{ }A_{\mu}^{c}`$*\*

- *That transformation law is the adjoint representation.*

- *So:*

- ***Gauge fields transform in the adjoint rep because they are Lie-algebra–valued objects.***

- *No matter fields required for this statement.*

- 

- ***4. Contrast with matter representations***

- *Matter fields transform as*

- $`\psi \rightarrow \Omega\psi`$*\*

- *Here:*

- $`\psi`$*lives in some representation* $`R`$

- $`T_{a}`$*are matrices acting on* $`\psi`$*’s components*

- *the dimension of* $`R`$*can be anything (doublet, triplet, etc.)*

- *Gauge fields are different:*

- *they don’t live in “matter space”*

- *they live in **symmetry space itself***

- *That’s why:*

- *fermions can be in fundamental reps*

- *scalars can be in various reps*

- *gauge bosons are always adjoint*

- *There is no freedom here.*

- 

- ***5. Why the adjoint rep forces self-interaction***

- *This is the payoff.*

- *Because the adjoint action is a commutator,*

- $`\lbrack T_{a},T_{b}\rbrack \neq 0`$*\*

- *the field strength*

- $`F_{\mu\nu} = \partial_{\mu}A_{\nu} - \partial_{\nu}A_{\mu} + g\lbrack A_{\mu},A_{\nu}\rbrack`$*\*

- *necessarily contains*

- $`gf_{abc}A_{\mu}^{b}A_{\nu}^{c}`$*\*

- *So:*

- *self-interactions are not “added”*

- *they are not “because non-Abelian is fancy”*

- *they are the algebra acting on itself*

- *That’s what adjoint really means physically.*

- 

- ***6. A geometric way to say it (matches your instincts)***

- *If matter fields are **vectors being parallel transported**,\
  then gauge fields are **the rule for parallel transport itself**.*

- *Changing the rule must be done by the rule acting on itself.*

- *That self-action is the adjoint representation.*

- 

- ***7. One-sentence takeaway***

- ***The adjoint representation is how a symmetry acts on its own generators, and gauge fields live there because they are the local bookkeeping device for that symmetry, not objects being acted on by it.***

- *If you want next, the most clarifying follow-up is usually:*

- *why the field strength* $`F_{\mu\nu}`$*transforms adjointly but homogeneously, while* $`A_{\mu}`$*does not*

- *—that’s where the connection/curvature distinction really locks in.*

- *ow man, that's heavy, i didn't understand much at all. reviewing all this, i think its this self-adjoint, non-abelian, an algebraic provability that my folk version is missing the most. non-abelian is certainly a whole world to leave out, but i can squint and say its non-essential. algebraic provability is huge, but maybe we just hint at that. say "all these ideas are captured in a self-consitent, extendible algebra, blah, blah. the reason not to cover it in earnest is just that it is hard. but i'd rank it above non-abelian. (though you get non-abelian for free if you cover algebraic provability. but this self-adjoint stuff seems to carry some physics that were blithely asserting. I feel this ranks as the most important thing to cover. though, like the non-abelian, maybe we can't get there without diving into the algebra. (btw -- there's something really profound here -- what makes a theory good isn't how compelling it is, it's how consistent it is. geometry is more compelling than algebra. machines are more compelling that stats. but algebra and stats can (have) been employed to build a larger self-consistent theory. maybe they are also more compelling and its lost on me because its not accessible)*

-  Instead, he asks a harder question:\
  *Can a Lorentz-covariant vector field have a Hamiltonian bounded from below at all?*

-  The answer forces the high-energy Lagrangian into the form

- $`\mathcal{L = -}\frac{1}{4}F_{\mu\nu}F^{\mu\nu}`$

-  That form **automatically introduces gauge redundancy**:

- $`A_{\mu} \rightarrow A_{\mu} + \partial_{\mu}\Lambda`$

-  Gauge redundancy removes exactly **one degree of freedom**.

Only *after* that does the familiar statement emerge:

- massive spin-1 → 3 physical polarizations

- massless spin-1 → 2 physical polarizations

- Guage invariance (local symmetry) comes from (w/o matter fields) the fact that w/o redundancy infinitely many -different- state are all 0 energy

- Ok, right so choose your axiom. Matter couples to vector field (=\> has local symmetry) or Matter field has local symmetry (=\> must couple to a vector field)

- ?: nothing forces vector/spin1 particles b/c they are massless? But what if they’re not?

- ?: Wazzuh?: *Matter fields are taken to live in representation spaces of the gauge group, so a local gauge transformation acts on them by point-dependent matrix multiplication.*

- That’s all this line is asserting — but it’s the hinge that lets gauge fields and matter talk to each other.

- An abelian Lie group with one generator (vector potential shifts) is **isomorphic to** $`U(1)`$.

- **Global U(1) multiplies the wavefunctional; gauge symmetry relabels its arguments.**

- That is the exact structural difference.

- 

- $`D_{\mu}\psi = (\partial_{\mu} + ieA_{\mu})\psi`$

- transforms the same way as ψ:

- $`D_{\mu}\psi \rightarrow e^{iq\Lambda(x)}D_{\mu}\psi`$ They do.

- Because that pair of equations is the entire reason the photon field exists.

- Here’s why they punch.

- Start with a local phase rotation:

- $`\psi(x) \rightarrow e^{iq\Lambda(x)}\psi(x)`$

- Now take a plain derivative:

- $`\partial_{\mu}\psi \rightarrow e^{iq\Lambda(x)}\left( \partial_{\mu}\psi + iq(\partial_{\mu}\Lambda)\psi \right)`$

- That extra term

- $`iq(\partial_{\mu}\Lambda)\psi`$

- is the problem.

- The derivative “sees” that the phase varies from point to point.\
  So ordinary differentiation is not compatible with local symmetry.

- Now introduce

- $`D_{\mu} = \partial_{\mu} + ieA_{\mu}`$

- and demand that

- $`D_{\mu}\psi \rightarrow e^{iq\Lambda(x)}D_{\mu}\psi`$

- This requirement forces the gauge field to transform as

- $`A_{\mu} \rightarrow A_{\mu} - \frac{1}{e}\partial_{\mu}\Lambda`$

- so that the bad derivative term cancels exactly.

- Summary: fields have to transform under Lorentz transformation to match Hilbert space. Massless spin one is 4-vector but represent 3-d spin state, so has an extra internal dimension. This is a-physical therefore redundant. If other fields couple to it, they must have local symmetry. In GPTs word:

- ***Weinberg / ’t Hooft condensed chain***

- ***Particles are irreducible representations of the Poincaré group.**\
  Massless spin-1 particles have only **two helicity states**.*

- ***A local Lorentz-covariant vector field*** $`A_{\mu}`$***has four components.**\
  Therefore it necessarily contains **redundant, unphysical components**.*

- ***Redundancy appears as a shift freedom:***

- $`A_{\mu} \rightarrow A_{\mu} + \partial_{\mu}\Lambda`$*\*

- *which leaves the physical photon states unchanged.*

- ***Any interaction must not depend on the redundant part.**\
  This forces coupling only to **conserved currents:***

- $`A_{\mu}J^{\mu},\partial_{\mu}J^{\mu} = 0`$*\*

- ***Local conservation requires replacing ordinary derivatives with covariant ones:***

- $`\partial_{\mu} \rightarrow \partial_{\mu} + ieA_{\mu}`$*\*

- ***Conclusion:**\
  Massless spin-1 particles inevitably lead to gauge redundancy, and if they interact at all, the interaction must be gauge coupling.*

- *Hilber space has all particle types*

- *The wavefunction encodes what is not localized — the open question we are asking about the system.\
  Operators encode what is localized — the structure of our experimental interventions.\
  By placing operators in spacetime and states in a global space of possibilities, quantum field theory preserves local causality without requiring localized hidden variables.*

- *?: How does QFT handle entanglement. What does it say that single-particle doesn’t*

- *A fundamental force field is a spacetime-dependent connection that tells you how symmetry generators are applied locally.The force on a particle is the sum of all such fields*

- *wasn't going to talk about non-abelion fields, but now i'm going to because the most economical formulation of abelion fields has the non-abelian term (equalling zero). when something is rightly understood as a degenerate case, so be it*

-  Its curvature is

- $`F = dA + A \land A`$*\*

-  In components, that second term is exactly the $`f^{abc}A^{b}A^{c}`$term

- *The various gauge choices differ not in physics but in which spacetime directions are used to anchor the redundancy inherent in a gauge description.*

- *Ok: The Fourier transform is introduced because it turns the derivative operators in the quadratic part of the Lagrangian into algebraic factors, allowing the propagators—and hence the Feynman rules—to be read off directly. Notes: 1) the beam actually is (almost) single momentum 2) A pure momentum mode doesn’t propagate by moving its shape — it propagates by accumulating phase in time. 3) propagators are “in time”*

- ***1) Perturbation theory (general)***

- *Write problem as: **simple part + small interaction***

- *Expand exponential / integrand in powers of coupling:* $`1 + g + g^{2} + \ldots`$

- *Each power = additional interaction event*

- *Integrate / sum each term separately*

- *Valid only if **true expansion parameter is dimensionless and ≪ 1***

- 

- ***2) Dimensionful coupling ⇒ “smallness” depends on scale***

- *Dimensionless* $`g`$*: smallness absolute (0.3 → 0.09 → …)*

- *Dimensionful* $`g`$*: must combine with scale to form dimensionless quantity*

- *Actual expansion parameter is:*

- $`g \times (\text{relevant scale})^{\mid d \mid}`$*\*

- *Integrals automatically introduce scales (momentum cutoff, mass, wavelength, region size)*

- *So interaction may be weak at large distances but strong at short distances (or vice versa)*

- 

- ***3) This constrains allowed interaction terms (given chosen fields)***

- *Fields fixed first by symmetry / spin / consistency*

- *Interactions = products of fields and derivatives at a point*

- *That structure fixes dimension of coupling constant*

- *Coupling dimension predicts how interaction strength scales with scale*

- ***Non-negative dimension coupling → perturbation stays controlled → renormalizable***

- ***Negative dimension coupling → effective strength grows with scale → needs infinite new parameters → effective theory only***

- *So dimensional analysis filters **which interaction terms can be fundamental**, not which fields exist*

- *L = free field 1 + free field 2 + interaction*

- *The propagator is literally the measurable amplitude for a particle created at one point to be detected at another point.*

- *?: NOTE: this is an important point: why is each interaction a power. (this both central and deep)*

- In a local classical field theory the action is additive over spacetime,

- $`S\lbrack\phi\rbrack = \int d^{4}x\text{ }\mathcal{L(}\phi(x),\partial\phi(x)),`$*\*

- which you can picture by dividing spacetime into tiny cells so that

- $`S \approx \sum_{\text{cells}}^{}{\mathcal{L(}x)\text{ }}\Delta^{4}x.`$

- Quantum mechanics adds the rule that amplitudes for successive regions multiply, so the amplitude for an entire field history must be the product of infinitesimal factors, and locality and smoothness require each small cell to contribute something close to unity with a correction proportional to the local action density,

- $`A(x) \approx 1 + i\text{ }\mathcal{L(}x)\text{ }\Delta^{4}x.`$

- Multiplying over all cells gives

- $`\prod_{\text{cells}}^{}\left( 1 + i\text{ }\mathcal{L(}x)\text{ }\Delta^{4}x \right)\text{\:\,} \rightarrow \text{\:\,}\exp\text{ ⁣}\left( i\mathcal{\sum L(}x)\text{ }\Delta^{4}x \right) = e^{iS\lbrack\phi\rbrack},`$*\*

- so the exponential arises precisely because multiplication of amplitudes over spacetime maps to addition of the action in the exponent. Splitting the Lagrangian into free and interaction parts, $`\mathcal{L =}\mathcal{L}_{0} + \mathcal{L}_{\text{int}}`$, isolates the interaction contribution

- $`e^{iS_{\text{int}}} = \exp\text{ ⁣}\left( i\int d^{4}x\text{ }\mathcal{L}_{\text{int}}(x) \right),`$*\*

- and perturbation theory is simply the Taylor expansion of this exponential,

- $`e^{iS_{\text{int}}} = 1 + i\int d^{4}x_{1}\text{ }\mathcal{L}_{\text{int}}(x_{1}) + \frac{i^{2}}{2!}\int d^{4}x_{1}d^{4}x_{2}\text{ }\mathcal{L}_{\text{int}}(x_{1})\mathcal{L}_{\text{int}}(x_{2}) + \cdots\text{ },`$*\*

- where the $`n`$th term integrates over all possible spacetime locations $`x_{1},\ldots,x_{n}`$of $`n`$interaction insertions, reflecting that the fields interact continuously but the expansion reorganizes the amplitude according to how many times the interaction term contributes. When the free-field Gaussian integrals are evaluated, each insertion point becomes a vertex and each pairing of fields becomes a propagator, so a Feynman diagram is a compact representation of one term in this expansion, while the full quantum amplitude is the sum over diagrams at all orders.

- *this is all freaking sick. i feel like we have a good chunk our feyneman story now. , path integrals -\> propagators are defined for free fields and we have our greens function "inversion" to make them. symmetry group action's exponential mapping tells us each power is a number of interactions (very good explanation, bot). Now we have some work. how do we use the expansion and propagators to get to correlations.*

- *Expansion + propagators -\> correlation*

- That two-point function *is* the propagator:

- $`\langle\phi(x)\phi(y)\rangle_{0} = D(x - y)`$*\*

- Interpretively:

- the propagator is the primitive unit of correlation in the free theory.

- Everything else is built from it.

- *Correlation functions are built by summing over all possible ways disturbances can propagate between the points being measured and influence one another along the way, where propagation is described by the propagator (the Green’s function of the free wave equation) and interactions are described by insertions of the interaction Lagrangian at spacetime points, represented diagrammatically as vertices.*

- *Correlation functions arise by probing the path integral with localized sources and observing the system’s response. In the free theory these responses are entirely determined by the propagator, the inverse of the quadratic kernel. When interactions are present, the exponential expansion of the interaction action introduces additional field insertions, which are paired by the free propagator. The resulting correlations are sums over all allowed ways influence may propagate and interact between the points being measured, naturally organizing themselves into diagrams.*

6\. Why the exponential appears

This connects directly to the point you raised earlier.

Each infinitesimal spacetime region contributes a factor

``` math
\exp\text{ ⁣}\left( \frac{i}{\hslash}L(x)d^{4}x \right)
```

Multiplying over all regions gives

``` math
\prod_{x}^{}{\exp\text{ }\text{⁣}}\left( \frac{i}{\hslash}L(x)d^{4}x \right) = \exp\text{ ⁣}\left( \frac{i}{\hslash}\int d^{4}xL \right) = \exp(iS/\hslash)
```

So the partition function is literally:

**the product of amplitude contributions from every spacetime point.**

- Path -\> transition

- break

- Z\[0\]=⟨0out​∣0in​⟩

- S-matrix. Z\[0\] is one element.

- ?: do we care about dispersion? So “dispersion” here refers to\
  the way amplitude information is *spread* across energies through analyticity, not to the propagation of a wave packet. Something about you find amplitude at energy by integrating over all other energies

- ?: Huh? The first is the identification of unitarity with *cutting*. This is the deep idea behind the Cutkosky rules and the optical theorem. Unitarity is not an abstract operator equation floating above diagrams. It shows up diagrammatically as the statement that imaginary parts of amplitudes come from intermediate states that can go on shell, with positive energy. That’s real physics content: probability only leaks into channels that correspond to actual physical states. The whole largest-time equation formalism is a clever way of making that precise without waving hands.

- the general formula

- $`S = \mathcal{T}\exp\text{ ⁣}\left( - i\int d^{4}x\text{ }\mathcal{H}_{\text{int}}(x) \right),`$*\*

- or its path-integral equivalent

- \<out\|S\|in\>

- Z\[J\]=∫DϕeiS\[ϕ\]+i∫Jϕ or Z=∫DϕeiS\[ϕ\] – partition function weighted history. With J “if I poke here, how does the weighted history change.

- dZ/dJ = ⟨0∣T{ϕ(x1​)⋯ϕ(xn​)}∣0⟩

> <u>More refined notes</u>

- QFT can’t tell you about forces because things aren’t at definite place. What can it tell you?

- But finding “force” in the classical approximation can be a good target

- Bridging Path integral 1) Show operator formulation leads directly to path integral formulation first, not both lead to scattering matrix first, 2) To build intuition, show the equivalency for single particle first.

- Symmetry and Unitarity gate admissible field theories

  - **Geometry (spacetime structure):**\
    Symmetry determines the invariant structure of spacetime. Requiring Lorentz symmetry fixes the invariant interval $`ds^{2} = \eta_{\mu\nu}dx^{\mu}dx^{\nu}`$, which defines Minkowski geometry. This geometry establishes the causal structure (light cones) and the rules for how coordinates transform between observers. All subsequent physics must respect this spacetime symmetry.

  - **Objects (fields / representations):**\
    Physical degrees of freedom must transform under representations of the spacetime symmetry group. For Lorentz symmetry this yields the admissible field types: scalars, spinors, vectors, tensors, etc. These transformation rules determine how fields seen by one observer relate to fields seen by another. In QFT, these fields become operators acting on a Hilbert space of states. Synopsized by: v2​=D(g1​)v1​=D(g1​)D(g2​)v

  - **Dynamics (allowed field theories):**\
    The laws governing those fields must satisfy several constraints simultaneously:\
    • **Lorentz covariance** — equations must retain the same form under Lorentz transformations.\
    • **Unitarity** — time evolution in Hilbert space must preserve probability (no negative-norm states or runaway energies).\
    • **Locality / microcausality** — influences propagate through neighboring spacetime points and operators commute at spacelike separation, ensuring no faster-than-light signaling. In practice these constraints are enforced by constructing a **Lorentz-invariant action** from local field operators; extremizing that action produces covariant equations of motion consistent with unitary quantum evolution.

- Adding field operators is most obvious way (minimal) way to add relativistic structure without throwing out the baby with bath water of QM

- NRQM fails structurally, fixing it with a relativistic Hamiltonian still leads to structure failures, but the phenomenonological proof in the pudding is NRQM fails to predict particle creation (See chat: “minimal fix in QFT”)

- Particle number becomes a derived thing

  - Fock space sectors

  - creation/annihilation as Fourier mode coordinates

  - “particle” as an asymptotic excitation and detector click

- Scattering is the end goal, from that you get

  - Theory consistency

  - Particle invariant measurements.

  - Coupling strengths

  - Momentum/amplitude deps -\> force laws in limit

- free theory is linear PDE, Green’s function is impulse response

- G(x−y) = response kernel = 2-point correlator (bridge the two meanings)

- Nonlinearities = interactions: perturbation theory as Volterra/Taylor series in the nonlinearity

- Feynman diagrams

  - Lines = props = Gs = Kernels

  - Vertices = field multiplication at a point

- Massless Vector fields are naturally longintudinally redundant and can couple to field s with conservative currents.

- Renomalizability constrains higher power interactions to “effective” theories

- How positive energy guides choice of correct QFT. (This relates to the NRQM -\> Upgraded Hamiltonian -\> field theory progression above)

- Vacuum is “drum head with no vibrations, but for uncertainty built into the ground state of a QSHO

- The procedural chain

  - \<out\|S\|in\> is the goal

  - Somewhere in here is Z\[J\] as “field response” / partition of histories

  - define Green’s function as inverse of □+m²

  - show its Fourier representation

  - relate that to time-ordered vacuum correlator

  - show how sources pull down fields via δ/δJ s

  - how how perturbation expands into products of G’s

  - then: amputation/on-shell gives scattering data

  - More on this

    - $`{\widetilde{G}}^{(4)} \sim \left( \frac{iZ}{p_{1}^{2} - m^{2} + i\epsilon} \right)\left( \frac{iZ}{p_{2}^{2} - m^{2} + i\epsilon} \right)\left( \frac{iZ}{p_{3}^{2} - m^{2} + i\epsilon} \right)\left( \frac{iZ}{p_{4}^{2} - m^{2} + i\epsilon} \right)\text{ }i\mathcal{M}`$

    - correlators know about fields,

    - poles in correlators identify particles,

    - external poles represent free propagation of asymptotic particles,

    - amputation removes those free-propagation factors,

    - the leftover on-shell core is the scattering amplitude.

    - the literal schematic LSZ statement for a scalar*:*$`\langle p_{3},p_{4}\text{ out} \mid p_{1},p_{2}\text{ in}\rangle \propto \prod_{i = 1}^{4}(p_{i}^{2} - m^{2})\text{ }{\widetilde{G}}^{(4)}(p_{1},p_{2},p_{3},p_{4}) \mid_{p_{i}^{2} \rightarrow m^{2}}.`$

    - **(See end of “Particle as asymptotic excitation” chat)**

    - Correlator: ⟨0∣T{ϕ(x1​)ϕ(x2​)ϕ(x3​)ϕ(x4​)}∣0⟩

    - Propagator is 2-point correlator

- Particles are probability distribution over momentum modes in the field

- Need mini-lecture on perturbation theory and where it fits in feynman diagram procedure

- fieldize the operators, not quantize the field

- non-abelian gauge fields

- “particles are poles” means the fields have “resonances” for real (on-shell) particles

## Outline 1

> Not part of QFT section – a different section – primer on Hamiltonian mechanics to motivate the role of the Hamiltonian as time evolution operator – this comes before QM – also probably entails splitting Lagrangian section in two, so instead of Lagrangian after QM we have L w/o gauge + H + QM + L w/gauge + QFT\]

1.  Why QFT

    1.  Relativistic structure

    2.  Assumes fixed number / No particle creation

    3.  Absence of fields as self-evident locality issue.

2.  The candidate fix – relativistice Hamiltonian

    1.  Identify the p^2 2<sup>nd</sup> vs 1<sup>st</sup> derivative problem

        1.  Parabolic vs hyperbolic

        2.  Try a sqrt(p^2) Hamiltonian

        3.  Show it still doesn’t work

        4.  Particle creation

        5.  Negative energy

3.  The fix – put “observations” into a via operators

    1.  What are the operators – the square in number density – there’s some intuition

    2.  To really answer, we need to think of field as lattice of coupled springs

    3.  Work through above \[need help, but below are some breadcrumbs\]

        1.  Fourier transform to momentum basis

        2.  See quanta in SHO amplitudes in momentum basis

        3.  Note the concept of ladder operators, label what we’re doing ladder operators, math possible optional?

        4.  Operators are now seen to be creation/annihilation operators

    4.  Alternate Schrodinger picture

    5.  Now relativistic structure and quanta creation are first class citizens

    6.  Vacuum state is quantum fluctuating but otherwise unexcited field.

    7.  What a particle now is – superposition of momentum modes in the field

        1.  A derived quantity from field configuration. – the particles can be constructed by the field, but the vacuum state cannot be constructed by the particles

4.  An alternate arguabley more elegant view: quantize the field

    1.  Describe classical field via Poisson operators

    2.  Switch to commutators

    3.  Make the bridge that this leads to the spring lattice / ladder operator results

5.  What do we calculate with this model/ontology

    1.  Correlations between time separated events

    2.  What do we calculate with NRQM - \<in\|out\>

    3.  Now we want interactions \[wait, what NRQM didn’t have interactions?\] \<in\|S\|out\>

    4.  This is very limited thing to calculate – black box interactions –

        1.  But from “black box fundamental interactions” we’ll build “white box forces” in the classical limit. To show this, at the end, coulomb force law

        2.  \<in\|S\|out\> = Operator(x)\|state\>

            1.  Flesh this out with words and equations, and Hamiltonian

            2.  Show where same objects – Hamiltonian, Green’s functions, etc show up in both formulations

        3.  Why we can express Operator\|state\> as path integral

            1.  Analogy to fixed particle

            2.  Ontology suggested by path integral

            3.  Why path integral is better for calculating than operator equation

            4.  

6.  Path integral, Feynman diagrams, and interactions

    1.  Propagators and interactions

    2.  Action and phase accumulation

    3.  Sketch of the PI procedure

    4.  Procedure step by step \[much to fill in here\]

        1.  \[Many things, below are a couple nuggets to hit\]

        2.  Exponential maps action to amplitude – same thing as exponentiating generators

        3.  How the math is a reappropriation of signal processing techniques

7.  Types of fields

    1.  Representations

    2.  Scalar/spinor/vector :: massive/massless

8.  Gauge field derivation without starting with mass field

    1.  Reminder about allowable representations

    2.  Redundancy from unused vector dimensions

        1.  Massless case, transverse/longitudinal

    3.  Non-abelian gauge field

    4.  Abelian covartiant derivative in Lagrangian as degenerate case of non-abelian

    5.  Why vector fields are ready-made for gauge coupling – redundancy is U(1) isomorphism

9.  Limits of QFT

    1.  Non-renormalizability

        1.  Effective theories

        2.  Dimensional analysis can reasoned about as length

10. Calculations

    1.  Scattering amplitudes

    2.  Coulomb force in limit

        1.  QED Lagrangian

        2.  Classical limit

11. Reflections

    1.  Ontology restores spacetime ontology, but we already knew that had to be

    2.  More of a synthesis than sledgehammer to prior understanding the way relativity and QM are

12. Things that are missing

    1.  What unitarity requires of field theory

    2.  Leaning hard on commutation relationships

13. Things that are not covered on purpose

    1.  \[many, so many things, obviously\]

    2.  Spontaneous symmetry breaking

## Outline 2

GPT:\
**QFT Outline v3**

**1. Pre-QFT setup elsewhere in the book**

**1.1. Lagrangian mechanics without gauge structure**

- Action as a functional of a path

- Euler–Lagrange equations

- Why second-order equations arise naturally

- Symmetry and conservation in the ordinary mechanical setting

**1.2. Hamiltonian mechanics as reformulation**

- Phase space: $`\left( q,p \right)`$

- Hamiltonian as generator of time evolution

- Hamilton’s equations

- Why the Hamiltonian is not merely “energy,” but the object that advances the system in time

**1.3. Quantum mechanics**

- States in Hilbert space

- Observables as operators

- Schrödinger evolution

- Transition amplitudes

- Classical observables as functions on phase space replaced by operators on Hilbert space

- Why the Hamiltonian now becomes the generator of unitary time evolution

**1.4. Return later to Lagrangians with gauge structure**

- Global vs local symmetry

- Why local symmetry requires connection fields

- This will set up the QFT section rather than interrupt it

**2. Why QFT**

**2.1. Ordinary quantum mechanics does not fit naturally with relativistic spacetime structure**

- Schrödinger theory treats time and space asymmetrically

- Relativity demands a more local spacetime-centered framework

**2.2. Ordinary quantum mechanics assumes fixed particle number**

- But nature allows particles to be created and destroyed

- A final theory must make variable particle number natural, not exceptional

**2.3. A deeper issue: no local fields**

- Ordinary QM is fundamentally organized around particle states

- Relativity teaches us to care about what can happen locally in spacetime

- A relativistic theory should let us talk about local quantities at spacetime points

- Once one becomes a “relativistic field believer,” it is hard to go back to particles as fundamental

**2.4. The conceptual demand**

- We want a framework that is:

  - quantum,

  - relativistic,

  - local,

  - and able to handle variable particle number

**2.5. The candidate answer**

- Assign operator-valued field content to spacetime

- Let particles emerge as excitations of those fields

**3. First failed repair: relativistic single-particle quantum mechanics**

**3.1. Start from the ordinary Schrödinger equation**

``` math
i\hslash\partial_{t}\psi = \widehat{H}\psi
```

- First order in time

- In the nonrelativistic case, $`\widehat{H} \sim {\widehat{p}}^{2}/2m + V`$, so second order in space

- This already treats time and space asymmetrically

**3.2. Why this asymmetry becomes a problem in relativity**

- Relativity places time and space into one geometric structure

- Relativistic propagation should reflect that symmetry more directly

- PDE language:

  - Schrödinger-type evolution is parabolic-like

  - relativistic propagation is hyperbolic

**3.3. Natural guess: use relativistic energy**

``` math
E^{2} = p^{2} + m^{2} \Rightarrow H = \sqrt{p^{2} + m^{2}}
```

and therefore

``` math
i\hslash\partial_{t}\psi = \sqrt{{\widehat{p}}^{2} + m^{2}}\text{ }\psi
```

**3.4. Why this does not really solve the problem**

- It gets the energy relation right

- But in position space it becomes a nonlocal operator

``` math
\sqrt{- \hslash^{2}\nabla^{2} + m^{2}}
```

- So it does not give the kind of local relativistic dynamics we want

- It does not make causality/local propagation transparent

- It repairs the dispersion relation without giving a satisfying local relativistic theory

**3.5. Try instead to square the equation: Klein–Gordon**

``` math
\left( \partial_{t}^{2} - \nabla^{2} + \frac{m^{2}}{\hslash^{2}} \right)\phi = 0
```

or, in covariant form,

``` math
(\square + m^{2})\phi = 0
```

with units/conventions adjusted as needed

- Now time and space enter symmetrically

- This is hyperbolic

- This looks much more relativistic

**3.6. But new problems appear**

- The equation is now second order in time

- Interpreting $`\phi`$as a single-particle wavefunction runs into trouble

- The naive probability-density interpretation fails

- Negative-frequency / negative-energy structure appears

**3.7. Dirac as the more refined relativistic wave equation**

- Dirac restores first-order time evolution while preserving relativity

- It handles spin-$`\frac{1}{2}`$ and improves the probability-current story

- But it still does not solve the deeper fixed-particle-number problem

- Once antiparticles appear naturally, the single-particle ontology is already straining

**3.8. Verdict on this whole route**

- Relativistic single-particle quantum mechanics is a useful transitional idea

- But it is not the final framework

- The real lesson is:

  - relativity wants local fields,

  - quantum theory wants operator structure,

  - so the right synthesis is operator-valued fields

**4. The real repair: local operator-valued fields**

**4.1. The central move**

- In ordinary QM, observables are operators on a Hilbert space

- In QFT, the theory assigns operator-valued field content to spacetime points

- Saucy version:

  - QFT “puts observations into space”

- More careful version:

  - QFT localizes the building blocks of observables

  - local observable densities are built from fields at spacetime points

**4.2. Important caution**

- A field operator is not usually itself an observable in the same sense as number, charge, or energy density

- Rather, it is a local operator-valued building block

- Observable densities are typically bilinears or other composites built from field operators

**4.3. First concrete example: number density**

- For a nonrelativistic bosonic field operator,

``` math
\widehat{n}(x) = {\widehat{\psi}}^{\dagger}(x)\widehat{\psi}(x)
```

- So number density is local in space

- Global particle number is

``` math
\widehat{N} = \int d^{3}x\text{ }\widehat{n}(x)
```

- This is the prototype for the slogan:

  - global observables arise as integrals of local densities

**4.4. Why this is the right kind of object for relativity**

- Relativity wants the theory expressed in terms of local spacetime quantities

- QFT gives local operators and local densities

- The theory is no longer fundamentally “about particles moving around”

- It is about local field content whose excitations can later look particle-like

**4.5. To understand where these operators come from, start classically**

- Model a field as a lattice of coupled oscillators / springs

- Each site has a displacement

- Neighboring sites are coupled

- This gives a discrete mechanical picture of a field

**4.6. Diagonalize the coupled system**

- Fourier transform from position-space lattice variables to momentum-space normal modes

- The coupled system becomes a collection of independent modes

- Each mode behaves like a simple harmonic oscillator

**4.7. Quantize each mode**

- Each normal mode is now quantized like an SHO

- Introduce ladder operators

``` math
{\widehat{a}}_{k},{\widehat{a}}_{k}^{\dagger}
```

- They lower or raise the occupation number of mode $`k`$

**4.8. Reinterpretation**

- These are not just abstract oscillator operators anymore

- They create and annihilate quanta of the field

- Variable particle number is now built into the formalism

**4.9. Reconstruct the field operator**

- The field operator is built as a superposition of modes

- Schematic form:

``` math
\widehat{\phi}(x) \sim \int\frac{d^{3}k}{\left( 2\pi)^{3} \right.\ }({\widehat{a}}_{k}e^{- ik \cdot x} + {\widehat{a}}_{k}^{\dagger}e^{ik \cdot x})
```

- This is the local spacetime field built from creation and annihilation operators

**4.10. What a particle now is**

- A particle is not fundamental matter-stuff

- It is an excitation of the field

- A one-particle state is typically a superposition of momentum modes

- A localized particle is a wave packet in field language

**4.11. Why the field/vacuum is prior to the particles**

- The vacuum is the underlying state of the field, and its structure determines what excitations are possible

- If you know the vacuum and the field dynamics, you can determine what particle excitations the theory supports

- But observing one or many excitations does not determine the vacuum that supports them

- In that sense, the field is prior to the particles, as a drumhead is prior to the modes it supports

**4.12. Vacuum**

- The vacuum is the lowest-energy state

``` math
{\widehat{a}}_{k} \mid 0\rangle = 0
```

for all $`k`$

- It contains no particles

- But it is not mere emptiness

- More fundamentally, it is the structured ground state that supports excitations

- Its properties determine what excitations can exist

- It also exhibits quantum fluctuations

- So the vacuum is “non-empty” in two senses:

  - it is the structured ground state of the field,

  - and it is quantum mechanically fluctuating

**4.13. Brief note on pictures**

- Schrödinger picture: states evolve, operators fixed

- Heisenberg picture: operators evolve, states fixed

- Mention only enough to orient:

  - Schrödinger picture makes state evolution feel primary

  - Heisenberg picture makes local field evolution feel primary

- Refine the “inverse” relation between pictures later

**5. What kinds of fields can there be?**

**5.1. The field cannot be just anything**

- Once fields are fundamental, we must ask what sort of mathematical object a field is allowed to be

- Different fields transform differently under spacetime symmetries

**5.2. Particle type from symmetry**

- In relativity, physical systems are classified by representations of the spacetime symmetry group

- Mass and spin label the kinds of excitations a field can support

- So “what kind of particle is this?” becomes “what representation is this field carrying?”

**5.3. Scalar, vector, spinor, tensor**

- Scalar field: transforms trivially under Lorentz transformations

- Vector field: transforms like a spacetime vector

- Spinor field: transforms in the spinor representation

- Tensor field: carries more elaborate transformation structure

- These are not just different notations; they encode different physical possibilities

**5.4. Why this matters physically**

- The transformation law determines what counts as the same object for different observers

- It constrains what equations the field can satisfy

- It constrains what interactions are allowed

- It determines what kind of excitation spectrum the field supports

**5.5. Examples**

- Klein–Gordon field as scalar example

- Dirac field as spinor example

- Electromagnetic potential / gauge field as vector example

**5.6. Little-group / spin interpretation, at the altitude you want**

- Fix momentum and ask how the object transforms under the remaining symmetry

- That is where spin / polarization content appears

- So spin is not an add-on label; it is part of the representation structure of the field

**5.7. Transition forward**

- So far these are fields classified by how they transform under spacetime symmetry

- But some of the most important symmetries are not spacetime symmetries

- They are internal symmetries

- Once those are made local, gauge fields enter

**6. Why gauge fields appear**

**6.1. Global internal symmetry**

- A field may have an internal phase or multiplet structure

- Under a global symmetry transformation, the same change is applied everywhere

- Example schematic:

``` math
\psi(x) \rightarrow e^{i\alpha}\psi(x)
```

with constant $`\alpha`$

**6.2. Local internal symmetry**

- Now let the transformation vary from point to point:

``` math
\psi(x) \rightarrow e^{i\alpha(x)}\psi(x)
```

- This is a much stronger demand

- Ordinary derivatives no longer transform nicely under this change

**6.3. Why the derivative fails**

- The derivative acts on the changing phase as well as the field

- So naive local symmetry breaks the form of the equations

- If we want local symmetry, we must repair the derivative

**6.4. Introduce a connection / gauge field**

- Define a covariant derivative

``` math
D_{\mu} = \partial_{\mu} + iqA_{\mu}
```

(or equivalent sign convention)

- The new field $`A_{\mu}`$compensates for local phase changes

- Gauge field is not added arbitrarily; it is required by the demand for local symmetry

**6.5. Physical meaning of the gauge field**

- The gauge field tells neighboring spacetime points how to compare internal phase directions

- It is a connection field

- It is the spacetime bookkeeping required by local internal symmetry

**6.6. Curvature / field strength**

- From the connection one builds curvature

``` math
F_{\mu\nu} = \partial_{\mu}A_{\nu} - \partial_{\nu}A_{\mu}
```

- This is the gauge-invariant local field strength

- The “force field” is the curvature associated with the connection

**6.7. Why this belongs before full interaction theory**

- This tells us what kind of field mediates interaction

- It explains why interaction fields are not ad hoc extras

- It gives the local geometric meaning of electromagnetism and later nonabelian generalizations

**6.8. Relation to matter fields**

- Matter fields carry representations of both spacetime symmetry and internal symmetry

- Gauge fields tell matter fields how to compare those internal states from point to point

- Interactions arise through the covariant derivative

**6.9. Lagrangian anchor**

- A schematic matter-plus-gauge Lagrangian belongs here

``` math
\mathcal{L \sim}\overset{ˉ}{\psi}(i\gamma^{\mu}D_{\mu} - m)\psi - \frac{1}{4}F_{\mu\nu}F^{\mu\nu}
```

or a simpler scalar-QED version if lower entry cost is better

- This is the first clear place where field type and gauge necessity come together in one equation

**6.10. Transition forward**

- We now know:

  - what a field is,

  - how fields are classified,

  - why gauge fields appear,

  - and how local interactions enter the Lagrangian

- Next we define quantization abstractly and then ask what the theory computes

**7. What quantization changed: from phase-space functions to operator fields**

**7.1. Why the physical picture is not enough**

- Section 4 gave the picture and logical sounding propositions

- Sections 5 and 6 told us what kinds of fields exist and why gauge fields arise

- Now we need abstract definitions that support precise reasoning

**7.2. Classical mechanics: observables as functions on phase space**

- In classical mechanics, an observable is a function $`f(q,p)`$

- Time evolution acts on phase-space variables

- The Poisson bracket gives the algebraic structure

``` math
\{ q,p\} = 1
```

**7.3. Quantum mechanics: observables as operators on Hilbert space**

- In quantum theory, phase-space functions are replaced by operators

- The Poisson bracket is replaced schematically by the commutator

``` math
\lbrack\widehat{q},\widehat{p}\rbrack = i\hslash
```

- Observables are no longer numerical functions of a state-space point

- They are operators acting on states

**7.4. Crucial new feature**

- Some operators do not merely report the value of an observable

- They change the state into one with a different observable value

- This is what makes ladder operators natural rather than strange

**7.5. Apply this logic to fields**

- A classical field is a numerical function $`\phi(x)`$

- Its conjugate momentum is $`\pi(x)`$

- The field-theory version of canonical structure is

``` math
\{\phi(x),\pi(y)\} = \delta(x - y)
```

**7.6. Quantize the field canonically**

- Promote $`\phi(x)`$and $`\pi(x)`$to operators

``` math
\widehat{\phi}(x),\widehat{\pi}(x)
```

- Replace the Poisson bracket by the commutator

``` math
\lbrack\widehat{\phi}(x),\widehat{\pi}(y)\rbrack = i\hslash\text{ }\delta(x - y)
```

- This is the field-theory analog of

``` math
\lbrack\widehat{q},\widehat{p}\rbrack = i\hslash
```

**7.7. Why this reproduces the ladder-operator story**

- Expand the field in modes

- Each mode behaves like an SHO

- The canonical commutator becomes the oscillator commutator

``` math
\lbrack{\widehat{a}}_{k},{\widehat{a}}_{k'}^{\dagger}\rbrack \propto \delta(k - k')
```

- So the lattice picture and the abstract canonical definition land on the same structure

**7.8. Where local observable densities come from**

- Once the field is operator-valued, one can build local densities:

  - number density,

  - charge density,

  - current density,

  - energy density,

  - momentum density

**7.9. Summary of the section**

- Classical field: numerical field over spacetime

- Quantized field: operator-valued field over spacetime

- Mode amplitudes become operators

- Those operators create and annihilate quanta

- This is the precise abstract backbone under the physical picture of section 4

**8. What QFT calculates**

**8.1. Fixed-particle quantum mechanics computes transition amplitudes**

- General state-to-state form:

``` math
\langle f \mid U(t_{f},t_{i}) \mid i\rangle
```

- Position-basis special case:

``` math
\langle x_{f},t_{f} \mid x_{i},t_{i}\rangle
```

- This is the amplitude for a system prepared in one state to be found in another after time evolution

**8.2. Field theory computes the analogous asymptotic transition amplitudes**

- General scattering form:

``` math
\langle\text{out} \mid S \mid \text{in}\rangle
```

- This is the relativistic many-particle analog of the ordinary transition amplitude

- Just as ordinary QM can be written in different bases, QFT can also be specialized to particular incoming and outgoing particle states

**8.3. But QFT also computes local matrix elements**

``` math
\langle f \mid \widehat{O}(x) \mid i\rangle
```

- This is the amplitude for a local operator insertion between states

**8.4. And especially vacuum correlators**

``` math
\langle 0 \mid T\{\widehat{\phi}(x_{1})\widehat{\phi}(x_{2})\cdots\text{ }\} \mid 0\rangle
```

- These are correlation functions / Green’s functions

- They are the natural language of a local field theory

**8.5. Why correlators matter**

- They encode propagation and response

- They tell us how local disturbances are related across spacetime

- Scattering amplitudes can ultimately be extracted from them

**8.6. Free theory first**

- In a free theory, the two-point correlator is the propagator

- This is the field-theoretic analog of a kernel / Green’s function

- It tells how disturbances propagate in the free theory

**8.7. Interaction changes the story**

- Once interactions are present, exact solutions are usually hard

- We therefore need perturbation theory or some alternative nonperturbative method

- The path integral becomes especially useful here

**8.8. A philosophical caution about the S-matrix**

- $`\langle\text{out} \mid S \mid \text{in}\rangle`$is powerful but black-box-like

- It gives asymptotic input/output data

- It does not by itself give the internal spacetime story many readers want

- Correlators and local field language partially restore that internal structure

**8.9. End goal of the formalism**

- Compute local correlators

- Extract scattering amplitudes

- Potentially go further to decay rates, cross sections, or effective classical forces

**9. Setting up the path integral**

**9.1. Why introduce the path integral at all**

- It is not a different theory

- It is another representation of the same quantum dynamics

- It is especially well adapted to:

  - Lagrangians,

  - relativistic covariance,

  - perturbation theory,

  - generating correlation functions

**9.2. Start in ordinary one-particle QM**

- Begin with the transition amplitude

``` math
\langle x_{f},t_{f} \mid x_{i},t_{i}\rangle
```

- This is the natural precursor to everything that follows

**9.3. Slice time into many small intervals**

- Insert many intermediate times

- Write the total evolution operator as a product of short-time evolution operators

``` math
U(t_{f},t_{i}) = \prod_{n}^{}{U(}t_{n + 1},t_{n})
```

**9.4. Insert resolutions of identity**

- Between short-time factors, insert position states

``` math
1 = \int dx\text{ } \mid x\rangle\langle x \mid 
```

- This turns one amplitude into an integral over many intermediate positions

**9.5. Evaluate the short-time kernel**

- For small $`\Delta t`$, approximate the exponential of the Hamiltonian

- Convert the product into something like

``` math
\exp\left( \frac{i}{\hslash}\sum_{n}^{}L\text{ }\Delta t \right)
```

- In the continuum limit, this becomes

``` math
\exp\left( \frac{i}{\hslash}S\lbrack x\rbrack \right)
```

**9.6. Arrive at the path integral**

``` math
\langle x_{f},t_{f} \mid x_{i},t_{i}\mathcal{\rangle = \int D}x\text{ }e^{iS\lbrack x\rbrack/\hslash}
```

- The integral is over all paths joining the endpoints

- The action weights each path by phase

**9.7. What this means conceptually**

- This is not “nature literally tries every path” in a naive mechanical sense

- But the formalism suggests a sum-over-histories viewpoint

- It ties quantum evolution directly to the action principle

**9.8. Why this helps**

- It connects naturally to Lagrangian thinking

- It sets up the field-theory generalization very cleanly

**10. From particle paths to field histories**

**10.1. Replace a path by a field history**

- In particle QM, the basic variable is a path $`x(t)`$

- In field theory, the basic variable is a spacetime field configuration $`\phi(x)`$

**10.2. The field-theory analog**

``` math
Z = \int\mathcal{D}\phi\text{ }e^{iS\lbrack\phi\rbrack/\hslash}
```

- Now we integrate over entire field histories, not particle trajectories

**10.3. What the action now means**

- The action is no longer for one coordinate moving in time

- It is the spacetime integral of a Lagrangian density

``` math
S\lbrack\phi\rbrack = \int d^{4}x\text{ }\mathcal{L(}\phi,\partial\phi)
```

**10.4. Why this is natural for relativity**

- The action is built from a spacetime field

- Covariance is easier to express

- Local interaction terms are easy to write down in $`\mathcal{L}`$

**10.5. But** $`\mathbf{Z}`$**by itself is too empty**

- The vacuum functional alone does not yet tell us the correlators we want

- We need a way to “poke” the theory

**11. Sources, generating functionals, and correlators**

**11.1. Introduce a source**

``` math
Z\lbrack J\rbrack = \int\mathcal{D}\phi\text{ }\exp\left( \frac{i}{\hslash}S\lbrack\phi\rbrack + \frac{i}{\hslash}\int d^{4}x\text{ }J(x)\phi(x) \right)
```

- $`J(x)`$is an external bookkeeping field

- It lets us generate correlation functions by differentiation

**11.2. Why this is the key move**

- Without sources, the path integral is a broad object

- With sources, it becomes an engine for producing correlators systematically

**11.3. Correlators from functional derivatives**

- Functional differentiation with respect to $`J(x)`$brings down factors of $`\phi(x)`$

- Repeated differentiation generates objects like

``` math
\langle 0 \mid T\{\widehat{\phi}(x_{1})\cdots\widehat{\phi}(x_{n})\} \mid 0\rangle
```

**11.4. What this achieves**

- Local field insertions become calculable

- The path integral and operator pictures are now visibly connected

- We have a clean route from action to correlators

**11.5. Free theory as Gaussian integral**

- For quadratic actions, the path integral is Gaussian

- Gaussian integrals can be done exactly

- The result is controlled by the inverse of the differential operator in the action

**11.6. Propagator as inverse operator**

``` math
\left( \square + m^{2})\text{ }G(x - y) = \delta^{(4)}(x - y \right)
```

- The two-point function is the Green’s function / propagator

- This is where the free-theory machinery becomes concrete

**12. Interactions and perturbation theory**

**12.1. Add an interaction term**

- Example:

``` math
\mathcal{L =}\mathcal{L}_{\text{free}} + \mathcal{L}_{\text{int}}
```

such as

``` math
\mathcal{L}_{\text{int}} \sim - \frac{\lambda}{4!}\phi^{4}
```

**12.2. Why exact evaluation usually fails**

- Interacting path integrals are generally not Gaussian

- So one expands around the free theory

**12.3. Perturbative expansion**

- Expand the exponential of the interaction term

- Each term in the expansion is evaluated using free-theory Gaussian rules

**12.4. Wick contraction logic**

- Free-theory correlators reduce to sums of pairings

- Each pairing contributes a propagator

**12.5. Feynman diagrams as bookkeeping**

- Propagators become internal lines

- Field insertions become external legs

- Interaction terms become vertices

- The diagram is not the physics itself; it is the combinatorial bookkeeping of the perturbative series

**12.6. What diagrams compute**

- Correlation functions first

- Then, after appropriate extraction, scattering amplitudes

**13. From correlators to scattering amplitudes**

**13.1. Why correlators are not yet scattering amplitudes**

- Correlators describe local operator insertions

- Experiments often prepare incoming particles and detect outgoing particles

- So we need a bridge from local fields to asymptotic particle states

**13.2. The conceptual bridge**

- Field operators can create and annihilate particle excitations

- So correlators contain the information about scattering processes

- Scattering amplitudes are extracted from the pole structure / asymptotic particle content of correlators

**13.3. State the result schematically**

- Time-ordered Green’s functions are the raw field-theoretic objects

- Scattering amplitudes arise from amputating external propagator factors and putting the external legs on shell

**13.4. Possible anchor equation, schematic only**

``` math
\text{amplitude} \sim \text{on-shell, amputated correlator}
```

- This is the place for an LSZ-style statement if you want one later

**13.5. Why this matters**

- The operator/path-integral machinery now reaches a real measurable target:

``` math
\langle\text{out} \mid S \mid \text{in}\rangle
```

**14. How far to carry the calculation**

**14.1. First natural stopping point: amplitudes**

- At this point the reader sees:

  - how QFT is built,

  - what correlators are,

  - how path integrals generate them,

  - how perturbation theory works,

  - how amplitudes emerge

**14.2. Optional next step: cross sections and decay rates**

- To go farther, one must add:

  - squaring amplitudes,

  - state normalization,

  - flux factors,

  - phase-space integrals,

  - spin sums/averages where relevant

- This is a real additional layer, not a trivial epilogue

**14.3. Recommendation for the main line**

- Main line reaches scattering amplitudes

- Then add a short bridge:

  - amplitudes become experimental probabilities and rates after further kinematic processing

**14.4. Optional worked example**

- Either:

  - a simple tree-level scattering process,

  - or the Coulomb-force recovery story,

  - or both, with one in the main text and one in an appendix

**15. Endpoint payoff: from black-box interactions to white-box forces**

**15.1. Admit the black-box feeling**

- S-matrix language can feel like it hides the mechanism

- We compare asymptotic states and package the middle into amplitudes

**15.2. But there is still a payoff**

- In appropriate limits, these amplitudes reproduce effective classical forces

- This is where the theory returns to familiar physics

**15.3. Coulomb as the target example**

- Exchange of the electromagnetic field leads, in the low-energy / static limit, to the Coulomb potential

- Thus a force law emerges from quantum exchange

**15.4. Why this is a satisfying endpoint**

- The reader began with:

  - why do we need QFT at all?

- The reader ends with:

  - this formalism reproduces familiar macroscopic force laws in the right limit

**16. Possible appendices / sidebars**

**16.1. More careful comparison of Schrödinger and Heisenberg pictures**

- Not merely “inverse,” but two equivalent placements of time dependence related by unitary transformation

**16.2. More formal LSZ reduction**

- If the main text stays schematic, this can live here

**16.3. More careful treatment of Klein–Gordon and Dirac**

- If the main text keeps them motivational rather than exhaustive

**16.4. Cross sections from amplitudes**

- If the main line stops at amplitudes

**16.5. Representation theory deepening**

- Little group, massive vs massless cases, polarization, spin

A few things I particularly like in this version:

- **4 → 5 → 6 → 7** now has a clean ascent:\
  field picture,\
  admissible field types,\
  gauge necessity,\
  abstract quantization.

- **8 → 9 → 10 → 11 → 12 → 13** now has a clean calculational ascent:\
  what QFT computes,\
  path integral setup in QM,\
  lift to fields,\
  sources and correlators,\
  perturbation theory,\
  scattering amplitudes.

- Your stronger **vacuum-prior-to-excitation** idea is now explicit.

- Gauge fields are back where they belong: before the full calculational machinery, as part of the ontology and architecture rather than as an afterthought.

## Random Notes 2

<u>The perturbation procedure:</u>

**What problem this block is addressing**

You have a **nonlinear system of classical field equations**:

``` math
\left( m_{i}^{2} - \partial_{\mu}^{2})\text{ }\phi_{i}(x) = - \frac{\partial V_{\text{int}}}{\partial\phi_{i}}(\phi(x) \right)
```

Because the right-hand side depends nonlinearly on the fields, there is **no general closed-form solution**.

This block explains **how to systematically construct solutions anyway**, in a controlled expansion.

**Step 1: Add a temporary source** $`\mathbf{J}_{\mathbf{i}}\mathbf{(x)}`$

He modifies the equation to

``` math
\left( m_{i}^{2} - \partial_{\mu}^{2})\text{ }\phi_{i}(x) = \varepsilon J_{i}(x) - \frac{\partial V_{\text{int}}}{\partial\phi_{i}}(\phi(x) \right)
```

Facts:

- $`J_{i}(x)`$is an arbitrary external function.

- $`\varepsilon`$is a bookkeeping parameter.

- Neither is physical.

- They exist only to organize the solution.

Purpose:

- To treat the field as being “driven” weakly.

- To allow an expansion in powers of $`\varepsilon`$.

**Step 2: Assume a power-series solution**

He assumes the field can be written as

``` math
\phi_{i}(x) = \varepsilon\phi_{i}^{(1)}(x) + \varepsilon^{2}\phi_{i}^{(2)}(x) + \varepsilon^{3}\phi_{i}^{(3)}(x) + \cdots
```

This is an **ansatz**, not a result.

Meaning:

- $`\phi^{(1)}`$: response linear in the source

- $`\phi^{(2)}`$: correction due to interactions

- higher terms: repeated self-interaction effects

**Step 3: Introduce the Green’s function**

He defines $`G_{ij}(x - y)`$by

``` math
\left( m_{i}^{2} - \partial_{\mu}^{2})\text{ }G_{ij}(x - y) = \delta_{ij}\text{ }\delta(x - y \right)
```

Meaning:

- $`G_{ij}`$is the inverse of the linear differential operator.

- It tells you how a disturbance at $`y`$affects the field at $`x`$.

- The $`\delta_{ij}`$ensures it connects the correct field species.

**Step 4: Rewrite the differential equation as an integral equation**

Using the Green’s function, the field equation is rewritten as

``` math
\phi_{i}(x) = \int d^{4}y\text{\:\,}G_{ij}(x - y)\lbrack\varepsilon J_{j}(y) - F_{j}(\phi(y))\rbrack
```

where

``` math
F_{j}(\phi) \equiv \frac{\partial V_{\text{int}}}{\partial\phi_{j}}
```

This equation is **exact**.\
It is equivalent to the original differential equation.

**Step 5: Insert the power-series expansion into the integral equation**

Substitute

``` math
\phi = \varepsilon\phi^{(1)} + \varepsilon^{2}\phi^{(2)} + \cdots
```

into $`F_{j}(\phi)`$.

This produces

``` math
\phi_{i}(x) = \int d^{4}y\text{\:\,}G_{ij}(x - y)\lbrack\varepsilon J_{j}(y) - F_{j}(\varepsilon\phi^{(1)}(y) + \varepsilon^{2}\phi^{(2)}(y) + \cdots)\rbrack
```

This is what equation (2.5) is expressing.

**Step 6: What this achieves**

From this equation, you can now:

- Collect terms order-by-order in $`\varepsilon`$

- Solve sequentially:

  - first order gives $`\phi^{(1)}`$

  - second order gives $`\phi^{(2)}`$

  - etc.

Each step is linear because the nonlinearity has been pushed to lower orders already computed.

More on the same in a different section:\
\
**What he means by “we have found a recursive procedure” is this — nothing more, nothing less:**

He has turned the *nonlinear* field equation into a **step-by-step sequence of linear problems**, where each step only depends on the earlier ones.

I’ll say it concretely, using exactly his symbols.

**1. Start point: the original equation is nonlinear**

The equation is

``` math
(m_{i}^{2} - \partial_{\mu}^{2})\text{ }\phi_{i}(x) = \varepsilon J_{i}(x) - \frac{\partial V_{\text{int}}(\phi(x))}{\partial\phi_{i}}
```

The problem is the right-hand side depends **nonlinearly** on $`\phi`$.

That means you *cannot* solve it in one shot.

**2. Introduce the bookkeeping parameter** $`\mathbf{\varepsilon}`$

He writes

``` math
\phi_{i}(x) = \varepsilon\phi_{i}^{(1)}(x) + \varepsilon^{2}\phi_{i}^{(2)}(x) + \varepsilon^{3}\phi_{i}^{(3)}(x) + \cdots
```

This is **not physics** yet.\
It is a **formal expansion**: “let me track how many times the interaction appears.”

**3. Plug the expansion into the equation**

Now substitute this series into:

``` math
(m_{i}^{2} - \partial^{2})\phi_{i} = \varepsilon J_{i} - \partial V_{\text{int}}/\partial\phi_{i}
```

Because $`V_{\text{int}}`$is polynomial (cubic, quartic), the derivative produces terms like:

- $`\left( \phi^{(1)})^{2} \right.\`$

- $`\phi^{(1)}\phi^{(2)}`$

- etc.

Each of these comes with **definite powers of** $`\varepsilon`$.

**4. Collect terms order-by-order in** $`\mathbf{\varepsilon}`$

This is the key step.

You group everything multiplying:

- $`\varepsilon^{1}`$

- $`\varepsilon^{2}`$

- $`\varepsilon^{3}`$

- …

Each order gives a **separate equation**.

**5. What the equations look like**

At **first order** ($`\varepsilon^{1}`$):

``` math
\left( m_{i}^{2} - \partial^{2})\phi_{i}^{(1)}(x) = J_{i}(x \right)
```

This is linear.\
Solution:

``` math
\phi_{i}^{(1)}(x) = \int d^{4}y\text{ }G_{ij}(x - y)\text{ }J_{j}(y)
```

At **second order** ($`\varepsilon^{2}`$):

``` math
\left( m_{i}^{2} - \partial^{2})\phi_{i}^{(2)}(x) = - F_{i}(\phi^{(1)}(x) \right)
```

where $`F_{i} = \partial V_{\text{int}}/\partial\phi_{i}`$.

This is again linear in $`\phi^{(2)}`$, but the source term is built from $`\phi^{(1)}`$, which you already know.

So:

``` math
\phi_{i}^{(2)}(x) = - \int d^{4}y\text{ }G_{ij}(x - y)\text{ }F_{j}(\phi^{(1)}(y))
```

At **third order**:

``` math
(m_{i}^{2} - \partial^{2})\phi_{i}^{(3)}(x) = \text{known function of }\phi^{(1)},\phi^{(2)}
```

Same structure again.

**6. Why this is called “recursive”**

Because:

- You solve for $`\phi^{(1)}`$**first**

- Then you use that result to compute $`\phi^{(2)}`$

- Then you use both to compute $`\phi^{(3)}`$

- And so on

Each step depends only on **previous steps**, never on future ones.

That is literally the definition of a recursive procedure.

No mystery.

<u>I don’t understand this:</u>

**Why sources still appear**

You introduce a classical source $`J(x)`$and define:

``` math
Z\lbrack J\rbrack = \langle 0 \mid T\exp\text{ ⁣}\left( i\int J(x)\phi(x)\text{ }dx \right) \mid 0\rangle
```

This is a **generating device**.

You are not interested in $`J`$.\
You are interested in what happens when you differentiate with respect to it.

Example:

``` math
\frac{\delta^{2}Z}{\delta J(x)\delta J(y)} \mid_{J = 0} = i\text{ }G(x,y)
```

So in QFT:

- $`J(x)`$is a bookkeeping knob

- Green’s functions are what you extract

- the “solution” is the set of all correlators

Feynman and other propagators:

**1. What’s the *problem* he’s pointing out?**

The equation

``` math
\left( m_{i}^{2} - \partial_{\mu}^{2})G_{ij}(x - y) = \delta_{ij}\text{ }\delta(x - y \right)
```

**does not uniquely fix** $`G`$.

Why?\
Because if $`G`$solves it, then

``` math
G + (\text{any solution of }(m^{2} - \partial^{2})H = 0)
```

also solves it.

That’s just linear algebra:

- inverse of an operator is not unique

- you must choose **boundary conditions**

So the question becomes:

*Which inverse do we want?*

**2. Why does this turn into “contour choices” in Fourier space?**

When you Fourier transform, the Green’s function looks like

``` math
G(x - y) \sim \int d^{4}k\text{ }\frac{e^{ik \cdot (x - y)}}{k^{2} + m^{2}}
```

But the denominator is zero at certain $`k_{0}`$values (“poles”).

So:

- the integral is ambiguous

- you must specify **how to go around the poles**

That choice = boundary condition in spacetime.

No physics yet. Just math.

**3. Forward Green function (retarded) — “cause before effect”**

He defines

``` math
G_{+}(x - y)
```

by a tiny shift $`k_{0} \rightarrow k_{0} + i\varepsilon`$.

What does this *actually* do?

It forces:

``` math
G_{+}(x - y) = 0\text{if }x^{0} < y^{0}
```

Translation:

nothing happens **before** the source acts

This is the **classical causality** choice:

- disturbances only propagate forward in time

- no backward influence

- no superluminal nonsense

This is what you’d use for:

- classical waves

- response functions

- “poke system here, what happens later?”

**4. Backward Green function — the opposite (usually useless)**

The opposite pole choice gives

``` math
G_{-}(x - y) = 0\text{if }x^{0} > y^{0}
```

Meaning:

effects happen *before* causes

Mathematically valid.\
Physically useless for ordinary causality.

He mentions it only for completeness.

**5. Feynman propagator — *not* a causality choice**

Now the key shift:

``` math
G_{F}(x - y) = \int d^{4}k\text{ }\frac{e^{ik \cdot (x - y)}}{k^{2} - k_{0}^{2} + m^{2} - i\varepsilon}
```

This choice does **not** enforce “only forward in time.”

Instead it enforces:

**time ordering**

Explicitly:

``` math
G_{F}(x - y) = \theta(x^{0} - y^{0})\text{ }G_{+}(x - y) + \theta(y^{0} - x^{0})\text{ }G_{-}(x - y)
```

Translation:

- if $`x`$is later → propagate forward

- if $`y`$is later → propagate backward

Why would we ever want that?

**6. Why QFT wants the Feynman propagator**

Quantum theory does **not** describe:

“poke system → watch response”

It describes:

correlations between measurements

Those measurements are:

- not ordered ahead of time

- summed over all possible time orderings

The Feynman propagator exactly matches:

``` math
\langle 0 \mid T\{\phi(x)\phi(y)\} \mid 0\rangle
```

## Outline 3

1\. Pre-QFT setup elsewhere in the book

1.1. Lagrangian mechanics without gauge structure

- Action as a functional of a path

- Euler–Lagrange equations

- Why second-order equations arise naturally

- Symmetry and conservation in the ordinary mechanical setting

1.2. Hamiltonian mechanics as reformulation

- Phase space: $`\left( q,p \right)`$

- Hamiltonian as generator of time evolution

- Hamilton’s equations

- Why the Hamiltonian is not merely “energy,” but the object that advances the system in time

1.3. Quantum mechanics

- States in Hilbert space

- Observables as operators

- Schrödinger evolution

- Transition amplitudes

- Classical observables as functions on phase space replaced by operators on Hilbert space

- Why the Hamiltonian now becomes the generator of unitary time evolution

1.4. Return later to Lagrangians with gauge structure

- Global vs local symmetry

- Why local symmetry requires connection fields

- This will set up the QFT section rather than interrupt it

2\. Why QFT

2.1. Ordinary quantum mechanics does not fit naturally with relativistic spacetime structure

- Schrödinger theory treats time and space asymmetrically

- Relativity demands a more local spacetime-centered framework

2.2. Ordinary quantum mechanics assumes fixed particle number

- But nature allows particles to be created and destroyed

- A final theory must make variable particle number natural, not exceptional

2.3. A deeper issue: no local fields

- Ordinary QM is fundamentally organized around particle states

- Relativity teaches us to care about what can happen locally in spacetime

- A relativistic theory should let us talk about local quantities at spacetime points

- Once one becomes a “relativistic field believer,” it is hard to go back to particles as fundamental

2.4. The conceptual demand

- We want a framework that is:

  - quantum,

  - relativistic,

  - local,

  - and able to handle variable particle number

2.5. The candidate answer

- Assign operator-valued field content to spacetime

- Let particles emerge as excitations of those fields

3\. First failed repair: relativistic single-particle quantum mechanics

3.1. Start from the ordinary Schrödinger equation

``` math
i\hslash\partial_{t}\psi = \widehat{H}\psi
```

- First order in time

- In the nonrelativistic case, $`\widehat{H} \sim {\widehat{p}}^{2}/2m + V`$, so second order in space

- This already treats time and space asymmetrically

3.2. Why this asymmetry becomes a problem in relativity

- Relativity places time and space into one geometric structure

- Relativistic propagation should reflect that symmetry more directly

- PDE language:

  - Schrödinger-type evolution is parabolic-like

  - relativistic propagation is hyperbolic

3.3. Natural guess: use relativistic energy

``` math
E^{2} = p^{2} + m^{2} \Rightarrow H = \sqrt{p^{2} + m^{2}}
```

and therefore

``` math
i\hslash\partial_{t}\psi = \sqrt{{\widehat{p}}^{2} + m^{2}}\text{ }\psi
```

3.4. Why this does not really solve the problem

- It gets the energy relation right

- But in position space it becomes a nonlocal operator

``` math
\sqrt{- \hslash^{2}\nabla^{2} + m^{2}}
```

- So it does not give the kind of local relativistic dynamics we want

- It does not make causality/local propagation transparent

- It repairs the dispersion relation without giving a satisfying local relativistic theory

3.5. Try instead to square the equation: Klein–Gordon

``` math
\left( \partial_{t}^{2} - \nabla^{2} + \frac{m^{2}}{\hslash^{2}} \right)\phi = 0
```

or, in covariant form,

``` math
(\square + m^{2})\phi = 0
```

with units/conventions adjusted as needed

- Now time and space enter symmetrically

- This is hyperbolic

- This looks much more relativistic

3.6. But new problems appear

- The equation is now second order in time

- Interpreting $`\phi`$as a single-particle wavefunction runs into trouble

- The naive probability-density interpretation fails

- Negative-frequency / negative-energy structure appears

3.7. Dirac as the more refined relativistic wave equation

- Dirac restores first-order time evolution while preserving relativity

- It handles spin-$`\frac{1}{2}`$ and improves the probability-current story

- But it still does not solve the deeper fixed-particle-number problem

- Once antiparticles appear naturally, the single-particle ontology is already straining

3.8. Verdict on this whole route

- Relativistic single-particle quantum mechanics is a useful transitional idea

- But it is not the final framework

- The real lesson is:

  - relativity wants local fields,

  - quantum theory wants operator structure,

  - so the right synthesis is operator-valued fields

4\. The real repair: local operator-valued fields

4.1. The central move

- In ordinary QM, observables are operators on a Hilbert space

- In QFT, the theory assigns operator-valued field content to spacetime points

- Saucy version:

  - QFT “puts observations into space”

- More careful version:

  - QFT localizes the building blocks of observables

  - local observable densities are built from fields at spacetime points

4.2. Important caution

- A field operator is not usually itself an observable in the same sense as number, charge, or energy density

- Rather, it is a local operator-valued building block

- Observable densities are typically bilinears or other composites built from field operators

4.3. First concrete example: number density

- For a nonrelativistic bosonic field operator,

``` math
\widehat{n}(x) = {\widehat{\psi}}^{\dagger}(x)\widehat{\psi}(x)
```

- So number density is local in space

- Global particle number is

``` math
\widehat{N} = \int d^{3}x\text{ }\widehat{n}(x)
```

- This is the prototype for the slogan:

  - global observables arise as integrals of local densities

4.4. Why this is the right kind of object for relativity

- Relativity wants the theory expressed in terms of local spacetime quantities

- QFT gives local operators and local densities

- The theory is no longer fundamentally “about particles moving around”

- It is about local field content whose excitations can later look particle-like

4.5. To understand where these operators come from, start classically

- Model a field as a lattice of coupled oscillators / springs

- Each site has a displacement

- Neighboring sites are coupled

- This gives a discrete mechanical picture of a field

4.6. Diagonalize the coupled system

- Fourier transform from position-space lattice variables to momentum-space normal modes

- The coupled system becomes a collection of independent modes

- Each mode behaves like a simple harmonic oscillator

4.7. Quantize each mode

- Each normal mode is now quantized like an SHO

- Introduce ladder operators

``` math
{\widehat{a}}_{k},{\widehat{a}}_{k}^{\dagger}
```

- They lower or raise the occupation number of mode $`k`$

4.8. Reinterpretation

- These are not just abstract oscillator operators anymore

- They create and annihilate quanta of the field

- Variable particle number is now built into the formalism

4.9. Reconstruct the field operator

- The field operator is built as a superposition of modes

- Schematic form:

``` math
\widehat{\phi}(x) \sim \int\frac{d^{3}k}{\left( 2\pi)^{3} \right.\ }({\widehat{a}}_{k}e^{- ik \cdot x} + {\widehat{a}}_{k}^{\dagger}e^{ik \cdot x})
```

- This is the local spacetime field built from creation and annihilation operators

4.10. What a particle now is

- A particle is not fundamental matter-stuff

- It is an excitation of the field

- A one-particle state is typically a superposition of momentum modes

- A localized particle is a wave packet in field language

4.11. Why the field/vacuum is prior to the particles

- The vacuum is the underlying state of the field, and its structure determines what excitations are possible

- If you know the vacuum and the field dynamics, you can determine what particle excitations the theory supports

- But observing one or many excitations does not determine the vacuum that supports them

- In that sense, the field is prior to the particles, as a drumhead is prior to the modes it supports

4.12. Vacuum

- The vacuum is the lowest-energy state

``` math
{\widehat{a}}_{k} \mid 0\rangle = 0
```

for all $`k`$

- It contains no particles

- But it is not mere emptiness

- More fundamentally, it is the structured ground state that supports excitations

- Its properties determine what excitations can exist

- It also exhibits quantum fluctuations

- So the vacuum is “non-empty” in two senses:

  - it is the structured ground state of the field,

  - and it is quantum mechanically fluctuating

4.13. Brief note on pictures

- Schrödinger picture: states evolve, operators fixed

- Heisenberg picture: operators evolve, states fixed

- Mention only enough to orient:

  - Schrödinger picture makes state evolution feel primary

  - Heisenberg picture makes local field evolution feel primary

- Refine the “inverse” relation between pictures later

5\. What kinds of fields can there be?

5.1. The field cannot be just anything

- Once fields are fundamental, we must ask what sort of mathematical object a field is allowed to be

- Different fields transform differently under spacetime symmetries

5.2. Particle type from symmetry

- In relativity, physical systems are classified by representations of the spacetime symmetry group

- Mass and spin label the kinds of excitations a field can support

- So “what kind of particle is this?” becomes “what representation is this field carrying?”

5.3. Scalar, vector, spinor, tensor

- Scalar field: transforms trivially under Lorentz transformations

- Vector field: transforms like a spacetime vector

- Spinor field: transforms in the spinor representation

- Tensor field: carries more elaborate transformation structure

- These are not just different notations; they encode different physical possibilities

5.4. Why this matters physically

- The transformation law determines what counts as the same object for different observers

- It constrains what equations the field can satisfy

- It constrains what interactions are allowed

- It determines what kind of excitation spectrum the field supports

5.5. Examples

- Klein–Gordon field as scalar example

- Dirac field as spinor example

- Electromagnetic potential / gauge field as vector example

5.6. Little-group / spin interpretation, at the altitude you want

- Fix momentum and ask how the object transforms under the remaining symmetry

- That is where spin / polarization content appears

- So spin is not an add-on label; it is part of the representation structure of the field

5.7. Transition forward

- So far these are fields classified by how they transform under spacetime symmetry

- But some of the most important symmetries are not spacetime symmetries

- They are internal symmetries

- Once those are made local, gauge fields enter

6\. Why gauge fields appear

6.1. Global internal symmetry

- A field may have an internal phase or multiplet structure

- Under a global symmetry transformation, the same change is applied everywhere

- Example schematic:

``` math
\psi(x) \rightarrow e^{i\alpha}\psi(x)
```

with constant $`\alpha`$

6.2. Local internal symmetry

- Now let the transformation vary from point to point:

``` math
\psi(x) \rightarrow e^{i\alpha(x)}\psi(x)
```

- This is a much stronger demand

- Ordinary derivatives no longer transform nicely under this change

6.3. Why the derivative fails

- The derivative acts on the changing phase as well as the field

- So naive local symmetry breaks the form of the equations

- If we want local symmetry, we must repair the derivative

6.4. Introduce a connection / gauge field

- Define a covariant derivative

``` math
D_{\mu} = \partial_{\mu} + iqA_{\mu}
```

(or equivalent sign convention)

- The new field $`A_{\mu}`$compensates for local phase changes

- Gauge field is not added arbitrarily; it is required by the demand for local symmetry

6.5. Physical meaning of the gauge field

- The gauge field tells neighboring spacetime points how to compare internal phase directions

- It is a connection field

- It is the spacetime bookkeeping required by local internal symmetry

6.6. Curvature / field strength

- From the connection one builds curvature

``` math
F_{\mu\nu} = \partial_{\mu}A_{\nu} - \partial_{\nu}A_{\mu}
```

- This is the gauge-invariant local field strength

- The “force field” is the curvature associated with the connection

6.7. Why this belongs before full interaction theory

- This tells us what kind of field mediates interaction

- It explains why interaction fields are not ad hoc extras

- It gives the local geometric meaning of electromagnetism and later nonabelian generalizations

6.8. Relation to matter fields

- Matter fields carry representations of both spacetime symmetry and internal symmetry

- Gauge fields tell matter fields how to compare those internal states from point to point

- Interactions arise through the covariant derivative

6.9. Lagrangian anchor

- A schematic matter-plus-gauge Lagrangian belongs here

``` math
\mathcal{L \sim}\overset{ˉ}{\psi}(i\gamma^{\mu}D_{\mu} - m)\psi - \frac{1}{4}F_{\mu\nu}F^{\mu\nu}
```

or a simpler scalar-QED version if lower entry cost is better

- This is the first clear place where field type and gauge necessity come together in one equation

6.10. Transition forward

- We now know:

  - what a field is,

  - how fields are classified,

  - why gauge fields appear,

  - and how local interactions enter the Lagrangian

- Next we define quantization abstractly and then ask what the theory computes

7\. What quantization changed: from phase-space functions to operator fields

7.1. Why the physical picture is not enough

- Section 4 gave the picture and logical sounding propositions

- Sections 5 and 6 told us what kinds of fields exist and why gauge fields arise

- Now we need abstract definitions that support precise reasoning

7.2. Classical mechanics: observables as functions on phase space

- In classical mechanics, an observable is a function $`f(q,p)`$

- Time evolution acts on phase-space variables

- The Poisson bracket gives the algebraic structure

``` math
\{ q,p\} = 1
```

7.3. Quantum mechanics: observables as operators on Hilbert space

- In quantum theory, phase-space functions are replaced by operators

- The Poisson bracket is replaced schematically by the commutator

``` math
\lbrack\widehat{q},\widehat{p}\rbrack = i\hslash
```

- Observables are no longer numerical functions of a state-space point

- They are operators acting on states

7.4. Crucial new feature

- Some operators do not merely report the value of an observable

- They change the state into one with a different observable value

- This is what makes ladder operators natural rather than strange

7.5. Apply this logic to fields

- A classical field is a numerical function $`\phi(x)`$

- Its conjugate momentum is $`\pi(x)`$

- The field-theory version of canonical structure is

``` math
\{\phi(x),\pi(y)\} = \delta(x - y)
```

7.6. Quantize the field canonically

- Promote $`\phi(x)`$and $`\pi(x)`$to operators

``` math
\widehat{\phi}(x),\widehat{\pi}(x)
```

- Replace the Poisson bracket by the commutator

``` math
\lbrack\widehat{\phi}(x),\widehat{\pi}(y)\rbrack = i\hslash\text{ }\delta(x - y)
```

- This is the field-theory analog of

``` math
\lbrack\widehat{q},\widehat{p}\rbrack = i\hslash
```

7.7. Why this reproduces the ladder-operator story

- Expand the field in modes

- Each mode behaves like an SHO

- The canonical commutator becomes the oscillator commutator

``` math
\lbrack{\widehat{a}}_{k},{\widehat{a}}_{k'}^{\dagger}\rbrack \propto \delta(k - k')
```

- So the lattice picture and the abstract canonical definition land on the same structure

7.8. Where local observable densities come from

- Once the field is operator-valued, one can build local densities:

  - number density,

  - charge density,

  - current density,

  - energy density,

  - momentum density

7.9. Summary of the section

- Classical field: numerical field over spacetime

- Quantized field: operator-valued field over spacetime

- Mode amplitudes become operators

- Those operators create and annihilate quanta

- This is the precise abstract backbone under the physical picture of section 4

8\. What QFT calculates

8.1. Fixed-particle quantum mechanics computes transition amplitudes

- General state-to-state form:

``` math
\langle f \mid U(t_{f},t_{i}) \mid i\rangle
```

- Position-basis special case:

``` math
\langle x_{f},t_{f} \mid x_{i},t_{i}\rangle
```

- This is the amplitude for a system prepared in one state to be found in another after time evolution

8.2. Field theory computes the analogous asymptotic transition amplitudes

- General scattering form:

``` math
\langle\text{out} \mid S \mid \text{in}\rangle
```

- This is the relativistic many-particle analog of the ordinary transition amplitude

- Just as ordinary QM can be written in different bases, QFT can also be specialized to particular incoming and outgoing particle states

8.3. But QFT also computes local matrix elements

``` math
\langle f \mid \widehat{O}(x) \mid i\rangle
```

- This is the amplitude for a local operator insertion between states

8.4. And especially vacuum correlators

``` math
\langle 0 \mid T\{\widehat{\phi}(x_{1})\widehat{\phi}(x_{2})\cdots\text{ }\} \mid 0\rangle
```

- These are correlation functions / Green’s functions

- They are the natural language of a local field theory

8.5. Why correlators matter

- They encode propagation and response

- They tell us how local disturbances are related across spacetime

- Scattering amplitudes can ultimately be extracted from them

8.6. Free theory first

- In a free theory, the two-point correlator is the propagator

- This is the field-theoretic analog of a kernel / Green’s function

- It tells how disturbances propagate in the free theory

8.7. Interaction changes the story

- Once interactions are present, exact solutions are usually hard

- We therefore need perturbation theory or some alternative nonperturbative method

- The path integral becomes especially useful here

8.8. A philosophical caution about the S-matrix

- $`\langle\text{out} \mid S \mid \text{in}\rangle`$is powerful but black-box-like

- It gives asymptotic input/output data

- It does not by itself give the internal spacetime story many readers want

- Correlators and local field language partially restore that internal structure

8.9. End goal of the formalism

- Compute local correlators

- Extract scattering amplitudes

- Potentially go further to decay rates, cross sections, or effective classical forces

9\. Setting up the path integral

9.1. Why introduce the path integral at all

- It is not a different theory

- It is another representation of the same quantum dynamics

- It is especially well adapted to:

  - Lagrangians,

  - relativistic covariance,

  - perturbation theory,

  - generating correlation functions

9.2. Start in ordinary one-particle QM

- Begin with the transition amplitude

``` math
\langle x_{f},t_{f} \mid x_{i},t_{i}\rangle
```

- This is the natural precursor to everything that follows

9.3. Slice time into many small intervals

- Insert many intermediate times

- Write the total evolution operator as a product of short-time evolution operators

``` math
U(t_{f},t_{i}) = \prod_{n}^{}{U(}t_{n + 1},t_{n})
```

9.4. Insert resolutions of identity

- Between short-time factors, insert position states

``` math
1 = \int dx\text{ } \mid x\rangle\langle x \mid 
```

- This turns one amplitude into an integral over many intermediate positions

9.5. Evaluate the short-time kernel

- For small $`\Delta t`$, approximate the exponential of the Hamiltonian

- Convert the product into something like

``` math
\exp\left( \frac{i}{\hslash}\sum_{n}^{}L\text{ }\Delta t \right)
```

- In the continuum limit, this becomes

``` math
\exp\left( \frac{i}{\hslash}S\lbrack x\rbrack \right)
```

9.6. Arrive at the path integral

``` math
\langle x_{f},t_{f} \mid x_{i},t_{i}\mathcal{\rangle = \int D}x\text{ }e^{iS\lbrack x\rbrack/\hslash}
```

- The integral is over all paths joining the endpoints

- The action weights each path by phase

9.7. What this means conceptually

- This is not “nature literally tries every path” in a naive mechanical sense

- But the formalism suggests a sum-over-histories viewpoint

- It ties quantum evolution directly to the action principle

9.8. Why this helps

- It connects naturally to Lagrangian thinking

- It sets up the field-theory generalization very cleanly

10\. From particle paths to field histories

10.1. Replace a path by a field history

- In particle QM, the basic variable is a path $`x(t)`$

- In field theory, the basic variable is a spacetime field configuration $`\phi(x)`$

10.2. The field-theory analog

``` math
Z = \int\mathcal{D}\phi\text{ }e^{iS\lbrack\phi\rbrack/\hslash}
```

- Now we integrate over entire field histories, not particle trajectories

10.3. What the action now means

- The action is no longer for one coordinate moving in time

- It is the spacetime integral of a Lagrangian density

``` math
S\lbrack\phi\rbrack = \int d^{4}x\text{ }\mathcal{L(}\phi,\partial\phi)
```

10.4. Why this is natural for relativity

- The action is built from a spacetime field

- Covariance is easier to express

- Local interaction terms are easy to write down in $`\mathcal{L}`$

10.5. But $`Z`$by itself is too empty

- The vacuum functional alone does not yet tell us the correlators we want

- We need a way to “poke” the theory

11\. Sources, generating functionals, and correlators

11.1. Introduce a source

``` math
Z\lbrack J\rbrack = \int\mathcal{D}\phi\text{ }\exp\left( \frac{i}{\hslash}S\lbrack\phi\rbrack + \frac{i}{\hslash}\int d^{4}x\text{ }J(x)\phi(x) \right)
```

- $`J(x)`$is an external bookkeeping field

- It lets us generate correlation functions by differentiation

11.2. Why this is the key move

- Without sources, the path integral is a broad object

- With sources, it becomes an engine for producing correlators systematically

11.3. Correlators from functional derivatives

- Functional differentiation with respect to $`J(x)`$brings down factors of $`\phi(x)`$

- Repeated differentiation generates objects like

``` math
\langle 0 \mid T\{\widehat{\phi}(x_{1})\cdots\widehat{\phi}(x_{n})\} \mid 0\rangle
```

11.4. What this achieves

- Local field insertions become calculable

- The path integral and operator pictures are now visibly connected

- We have a clean route from action to correlators

11.5. Free theory as Gaussian integral

- For quadratic actions, the path integral is Gaussian

- Gaussian integrals can be done exactly

- The result is controlled by the inverse of the differential operator in the action

11.6. Propagator as inverse operator

``` math
\left( \square + m^{2})\text{ }G(x - y) = \delta^{(4)}(x - y \right)
```

- The two-point function is the Green’s function / propagator

- This is where the free-theory machinery becomes concrete

12\. Interactions and perturbation theory

12.1. Add an interaction term

- Example:

``` math
\mathcal{L =}\mathcal{L}_{\text{free}} + \mathcal{L}_{\text{int}}
```

such as

``` math
\mathcal{L}_{\text{int}} \sim - \frac{\lambda}{4!}\phi^{4}
```

12.2. Why exact evaluation usually fails

- Interacting path integrals are generally not Gaussian

- So one expands around the free theory

12.3. Perturbative expansion

- Expand the exponential of the interaction term

- Each term in the expansion is evaluated using free-theory Gaussian rules

12.4. Wick contraction logic

- Free-theory correlators reduce to sums of pairings

- Each pairing contributes a propagator

12.5. Feynman diagrams as bookkeeping

- Propagators become internal lines

- Field insertions become external legs

- Interaction terms become vertices

- The diagram is not the physics itself; it is the combinatorial bookkeeping of the perturbative series

12.6. What diagrams compute

- Correlation functions first

- Then, after appropriate extraction, scattering amplitudes

13\. From correlators to scattering amplitudes

13.1. Why correlators are not yet scattering amplitudes

- Correlators describe local operator insertions

- Experiments often prepare incoming particles and detect outgoing particles

- So we need a bridge from local fields to asymptotic particle states

13.2. The conceptual bridge

- Field operators can create and annihilate particle excitations

- So correlators contain the information about scattering processes

- Scattering amplitudes are extracted from the pole structure / asymptotic particle content of correlators

13.3. State the result schematically

- Time-ordered Green’s functions are the raw field-theoretic objects

- Scattering amplitudes arise from amputating external propagator factors and putting the external legs on shell

13.4. Possible anchor equation, schematic only

``` math
\text{amplitude} \sim \text{on-shell, amputated correlator}
```

- This is the place for an LSZ-style statement if you want one later

13.5. Why this matters

- The operator/path-integral machinery now reaches a real measurable target:

``` math
\langle\text{out} \mid S \mid \text{in}\rangle
```

14\. How far to carry the calculation

14.1. First natural stopping point: amplitudes

- At this point the reader sees:

  - how QFT is built,

  - what correlators are,

  - how path integrals generate them,

  - how perturbation theory works,

  - how amplitudes emerge

14.2. Optional next step: cross sections and decay rates

- To go farther, one must add:

  - squaring amplitudes,

  - state normalization,

  - flux factors,

  - phase-space integrals,

  - spin sums/averages where relevant

- This is a real additional layer, not a trivial epilogue

14.3. Recommendation for the main line

- Main line reaches scattering amplitudes

- Then add a short bridge:

  - amplitudes become experimental probabilities and rates after further kinematic processing

14.4. Optional worked example

- Either:

  - a simple tree-level scattering process,

  - or the Coulomb-force recovery story,

  - or both, with one in the main text and one in an appendix

15\. Endpoint payoff: from black-box interactions to white-box forces

15.1. Admit the black-box feeling

- S-matrix language can feel like it hides the mechanism

- We compare asymptotic states and package the middle into amplitudes

15.2. But there is still a payoff

- In appropriate limits, these amplitudes reproduce effective classical forces

- This is where the theory returns to familiar physics

15.3. Coulomb as the target example

- Exchange of the electromagnetic field leads, in the low-energy / static limit, to the Coulomb potential

- Thus a force law emerges from quantum exchange

15.4. Why this is a satisfying endpoint

- The reader began with:

  - why do we need QFT at all?

- The reader ends with:

  - this formalism reproduces familiar macroscopic force laws in the right limit

16\. Possible appendices / sidebars

16.1. More careful comparison of Schrödinger and Heisenberg pictures

- Not merely “inverse,” but two equivalent placements of time dependence related by unitary transformation

16.2. More formal LSZ reduction

- If the main text stays schematic, this can live here

16.3. More careful treatment of Klein–Gordon and Dirac

- If the main text keeps them motivational rather than exhaustive

16.4. Cross sections from amplitudes

- If the main line stops at amplitudes

16.5. Representation theory deepening

- Little group, massive vs massless cases, polarization, spin

A few things I particularly like in this version:

- 4 → 5 → 6 → 7 now has a clean ascent:\
  field picture,\
  admissible field types,\
  gauge necessity,\
  abstract quantization.

- 8 → 9 → 10 → 11 → 12 → 13 now has a clean calculational ascent:\
  what QFT computes,\
  path integral setup in QM,\
  lift to fields,\
  sources and correlators,\
  perturbation theory,\
  scattering amplitudes.

- Your stronger vacuum-prior-to-excitation idea is now explicit.

- Gauge fields are back where they belong: before the full calculational machinery, as part of the ontology and architecture rather than as an afterthought.


## Unused QFT material\
intro material

~~## The QFT Model~~

~~- Fields~~

~~  - nature of fields – classical maxwell field – carries energy dynamic~~

~~    - why this is needed forces~~

~~  - spring model~~

~~- The wave function is not the field~~

~~- But what is a QFT field.~~

~~  - Operators~~

~~    - Think of them as actors not values, but what -are- they, well let them act if you must~~

~~    - Put observations in space~~

~~The first step in constructing quantum field theory is to construct a field that is joined to quantum mechanics’ notion of state space. After that, we can describe how to “use” the field and state space as a foundation from which to derive physical predictions.~~

~~There are two directions from which to approach quantum fields. The more ontologically satisfying direction is to move the operators of fixed-particle quantum mechanics which exist only as actions on state space into a causal spacetime setting. This makes intuitive sense. Since quantum mechanics said nothing about how observation interact in spacetime in accordance with relativity, to put the operators in spacetime is to put observations in spacetime. But simply saying $`O(x)`$ does not give any mechanics and moreover, it does not entail the required energetic physicality of the field which is necessary to abide local causality. The more useful direction for gaining a hands-on grasp of the model is to formulate a classical field and then “quantize” it, or promote the field values to operators. This approach lends itself to ontological confusion – what was the classical field before we quantized it? And how exactly did quantizing change it? By keeping both directions in mind, we can attain a level of ontological perspective while building a model that is suitably mechanical to abide local causality.~~

~~There are two ways to think of quantum fields that start from different points, but amount to the same thing. The first way is to start with fixed-particle quantum mechanics and move the operators of which existed only as actions on state space into a causal spacetime setting:~~ $`\mathcal{O \rightarrow O}(x).`$ ~~This makes intuitive sense. Since quantum mechanics said nothing about how observation interact in spacetime in accordance with relativity, to put the operators in spacetime is to put observations in spacetime. But simply saying~~ $`O(x)`$ ~~does not itself provide the basis of a mechanical system nor entail the required energetic physicality of the field which is necessary to abide local causality. The second way, which is more useful direction for gaining a hands-on grasp quantum fields, is to formulate a classical field and then “quantize” it, or promote the field values to operators. But this approach raises puzzling questions. Was there a classical field before we quantized it? And how exactly did quantizing change it? The quantum field for photons in fact is constructed identically to Maxwell’s classic E&M field, but what about the electron field? Classical mechanics of matter was never formulated as a matter field, but we could imagine a sort of semi-classical view in which we don’t know the full formalism of quantum mechanics but we have some intuition of particle delocalization, and we could in fact express the mechanics of “rigid bodies on average” in terms of a field. What matters is that the classical field we quantize must have the same causal flow of energy as our target quantum field. In particular, in the classical field the field strength is related to the energy density and in the quantum field it is as well but with energy density in being turn related to particle density.~~

~~There are two ways to think about quantum fields. They begin from different starting points, but meet in the same theory. The first is to begin with fixed-particle quantum mechanics and place its operators, which otherwise act only on state space, into a causal spacetime setting,~~ $`\mathcal{O \rightarrow O(}x)`$~~. This makes intuitive sense. If early quantum mechanics said little about how observables are situated in spacetime in a way compatible with relativity, then to place operators in spacetime is, in an important sense, to place observations in spacetime. But simply writing~~ $`\mathcal{O(}x)`$ ~~does not yet give us a mechanical system, nor does it by itself supply the dynamical, energy-carrying physicality required for local causality.~~

~~The second route, and the more useful one for gaining a hands-on grasp of quantum fields, is to begin with a classical field and then quantize it, replacing ordinary field values with operator-valued content. But this route raises puzzling questions of its own. Was there really a classical field there before quantization, and what exactly changed when we quantized it? For photons, the situation is unusually favorable, because the quantum field is built by quantizing Maxwell’s already existing classical electromagnetic field. But what about the electron field? Classical mechanics was never formulated as a classical field theory of matter in the same straightforward way. Still, one can imagine a semi-classical point of view in which one had no full quantum formalism, but did have some grasp of delocalization, and so described the mechanics of matter in terms of distributed fields rather than perfectly localized particles. What matters is that the classical field we quantize must share with the target quantum field the same local causal flow of energy. In the classical theory, the field configuration itself determines the energy density. In the quantum theory, the corresponding energy density is encoded in local operators built from the field, and in regimes where a particle picture applies, this can also be read as a greater or lesser density of excitation from place to place.~~

~~### Operators in Spacetime~~

~~\<Comment\> a note for all formatting: your comma separated equation or hard to read. Please in all cases put a few spaces on each side of the comma\</comment\> In fixed-particle quantum mechanics, the state is written as a vector in Hilbert space and evolves according to the Schrödinger equation,~~

``` math
i\hslash\text{ }\partial_{t} \mid \psi(t)\rangle = \widehat{H} \mid \psi(t)\rangle.
```

~~This is the form in which quantum mechanics is usually first learned. The state changes with time, while the operators representing observables are held fixed. If we ask for the probability distribution of position, momentum, or spin at some later time, that changing information is carried by the evolving state.~~

~~But there is another mathematically equivalent way to package the same theory. Instead of allowing the state to evolve while the observables remain fixed, we can hold the state fixed and let the observables evolve. This is the Heisenberg picture. The relation between the two pictures is~~

``` math
\mid \psi_{H}\rangle = \mid \psi(0)\rangle,\ \ {\widehat{\mathcal{\ O}}}_{H}(t) = U^{\dagger}(t)\text{ }{\widehat{\mathcal{O}}}_{S}\text{ }U(t),\ \ U(t) = e^{- i\widehat{H}t/\hslash}.
```

~~\<insert\>where O-sub-H O-sub-S are the …\</insert\> Nothing physical has changed. We have only changed where the time dependence lives. \<insert\>An expectation value is given by \<psi\|O\|psi\> giving us the freedom to put the time dependence on either the state or the operator. \[Show the algebra of inserting U(t) and moving it onto the operator\]\</insert\> One can think of this the way one thinks of rotating a vector versus rotating the coordinate axes in the opposite direction. The geometric content is the same. \<cut\>Only the bookkeeping differs.~~\</cut\> ~~In the Schrödinger picture the \<insert\>time evolution of the expectation value is given by moving a vector through a fixed frame, while in the Heisenberg picture the frame moves around a fixed vector. This is standard linear algebra – the same linear map has different matrix representation under a change of basis.\<cut\>The measurable predictions remain identical.\</cut\> \<insert\>We can now write the U(t) in the Heisenberg picture \[equation U(t) = e^integral(…)\] This form will arise later when working through QFT calculations.\</insert\>~~

~~Once the time dependence is moved into the operators, their evolution is determined by differentiating the expression above. This gives the Heisenberg equation of motion,~~

``` math
\frac{d{\widehat{\mathcal{O}}}_{H}}{dt} = \frac{i}{\hslash}\text{ }\lbrack\widehat{H},{\widehat{\mathcal{O}}}_{H}\rbrack + \left( \frac{\partial\widehat{\mathcal{O}}}{\partial t} \right)_{H}.
```

~~Already this is suggestive. The theory is beginning to speak less in terms the evolution of an abstract state and more in terms of the evolution of observables. The commutator encodes how the Hamiltonian acts as a generator of time translations on observables. In the same way that ordinary derivatives tell us how a function changes under a small shift in its argument, commutators tell us how an operator changes under the action of the symmetry generated by another operator. \<comment\>I’m tripping on the word ‘action’ – its neither super evocative nor precise. Can we say “changes under symmetry transformations generated by another operator” is that correct?\</commend\> They also measure incompatibility. If two observables commute, they can be simultaneously sharp \<cut\>in the relevant sense\</cut\>.\<insert\>or explain what you mean by this phrase\</insert\> If they do not, the order in which they act matters. In this way the commutator encodes both dynamics and kinematics at once.\<comment\>Not sure what to do with this sentence. Either explain it better – what part of what precedes is “kinematic” and “dynamic,” or leave it out, or, if you are adding content to what precedes, say it plainer language.\</comment\>~~

~~For a single particle, this is already enough to reproduce familiar mechanics. If the Hamiltonian is~~

``` math
\widehat{H} = \frac{{\widehat{p}}^{2}}{2m} + V(\widehat{x}),
```

~~then the Heisenberg equations give~~

``` math
\frac{d\widehat{x}}{dt} = \frac{i}{\hslash}\lbrack\widehat{H},\widehat{x}\rbrack = \frac{\widehat{p}}{m},\frac{d\widehat{p}}{dt} = \frac{i}{\hslash}\lbrack\widehat{H},\widehat{p}\rbrack = - \nabla V(\widehat{x}),
```

~~\<comment\>let’s just leave out the potential term for more beauty on the page. \</comment\>which look like operator versions of Hamilton’s equations. This is one reason the Heisenberg picture is so appealing for our purposes. It begins to look like a mechanics of evolving observables rather than merely a law for updating a probability distribution.\<comment\>I guess the preceding two sentences are good. It’s weird that switching between interchangeable views would have such a profound effect. Kind of feels like smoke and mirrors. I wonder if it might be better to say something along the lines that “having this in familiar Hamilton equation form points the way to using a repurposing a Hamiltonian classical field treatment. Think about what I’m saying conceptually, not prosaically, I’m not trying to write my best.\</comment\>~~

~~Still, in fixed-particle quantum mechanics these quantities are observables of a prescribed collection of particles. They are not yet attached point by point to spacetime. Quantum field theory takes the next step. It replaces the particle observables~~ $`\widehat{x},\widehat{p},\widehat{S}`$ ~~\<comment\>S? Action? If so, cut it\</comment\> with operator-valued fields~~

``` math
\widehat{\phi}(x),\widehat{\psi}(x),{\widehat{A}}_{\mu}(x),
```

~~where now~~ $`x`$ ~~denotes a spacetime point. A quantum field is thus not a number assigned to each point, but an operator assigned to each point. The Heisenberg equation survives intact, but now it governs fields,~~

``` math
\partial_{t}\widehat{\phi}(\mathbf{x},t) = \frac{i}{\hslash}\lbrack\widehat{H},\widehat{\phi}(\mathbf{x},t)\rbrack,\partial_{t}\widehat{\pi}(\mathbf{x},t) = \frac{i}{\hslash}\lbrack\widehat{H},\widehat{\pi}(\mathbf{x},t)\rbrack,
```

~~with~~ $`\widehat{\pi}(\mathbf{x},t)`$ ~~the momentum conjugate to the field. At equal times these obey canonical commutation relations,~~

``` math
{\lbrack\widehat{\phi}(\mathbf{x},t),\widehat{\phi}(\mathbf{y},t)\rbrack = 0,
}{\lbrack\widehat{\pi}(\mathbf{x},t),\widehat{\pi}(\mathbf{y},t)\rbrack = 0,
}{\lbrack\widehat{\phi}(\mathbf{x},t),\widehat{\pi}(\mathbf{y},t)\rbrack = i\hslash\text{ }\delta^{3}(\mathbf{x} - \mathbf{y}).
}
```

~~These are the field analogues of the ordinary canonical commutators of position and momentum. They tell us that the field and its conjugate momentum are not independent. They also tell us that field values at different spatial points are coupled in a way sharp enough to support local dynamics. \<comment\>ok. Starting at “at equal times” above through where this comment begins, I want you to distinguish between which of these commutators are imposed by relativity and which come from by necessity from the Heisenberg equation.\</comment\>~~

~~At this stage we can finally state locality in a form appropriate to relativity. It is not enough that the theory have spacetime labels. The operator algebra itself must respect causal structure. For bosonic fields the required condition is~~

``` math
\lbrack\widehat{\phi}(x),\widehat{\phi}(y)\rbrack = 0\text{whenever }(x - y)^{2} < 0,
```

~~\<comment\>I don’t get the minkowski math of (x-y)^2 \< 0 being spacelike separation\</comment\> that is, whenever the two spacetime points are separated by a spacelike interval. More generally, we can impose relativistic causal structure into quantum kinematics by requiring that observables commute at spacelike separation. \<cut\>This is the mathematical expression of the statement that no observable influence can pass between spacelike-separated regions.\</cut\> The theory may still admit entangled states spread across space, but its local observables do not shake hands faster than light. In this sense, relativistic causality is built not merely into the wave equation, but into the algebra of the observables themselves.\<comment\>rather than saying “built into algebra”, can we say something like “expressing relativistic causality as commutation relations provides rules that our subsequent field model must demonstrate adherence to.”\</comment\>~~

~~\<cut\>One can now see more clearly why early quantum mechanics sat uneasily with relativity. In fixed-particle quantum mechanics, the central object is a global state over configuration space. In quantum field theory, by contrast, the central observables are local operators assigned to spacetime points, and their commutation relations explicitly encode the causal order permitted by relativity. What had been, in particle mechanics, a problem about how interactions propagate has become, in field theory, part of the kinematical structure from the start.\</cut\> \<comment\>we’re going to come back to show how QFT makes good on its promises. No need to do it inline here.\</comment\>~~

~~We can express quantum fields in the Schrödinger picture. States now are no longer wavefunctions of particle positions but wavefunctionals of entire field configurations. If~~ $`\phi(\mathbf{x})`$ ~~denotes a field configuration on a time slice, then the state is written~~

``` math
\Psi\lbrack\phi(\mathbf{x}),t\rbrack.
```

~~This is a functional, not a function, because its argument is itself a whole function of space. The field operator acts by multiplication,~~

``` math
\widehat{\phi}(\mathbf{x})\Psi\lbrack\phi,t\rbrack = \phi(\mathbf{x})\Psi\lbrack\phi,t\rbrack,
```

~~while the conjugate momentum acts by functional differentiation,~~

``` math
\widehat{\pi}(\mathbf{x})\Psi\lbrack\phi,t\rbrack = - i\hslash\text{ }\frac{\delta}{\delta\phi(\mathbf{x})}\Psi\lbrack\phi,t\rbrack.
```

~~The Schrödinger equation then becomes an equation for the time evolution of an entire distribution over field configurations,~~

``` math
i\hslash\text{ }\partial_{t}\Psi\lbrack\phi,t\rbrack = \widehat{H}\text{ }\Psi\lbrack\phi,t\rbrack.
```

~~We can see this incomplete nature in three ways. First, non-relativistic quantum mechanics is an “everything everywhere all at once” model. When the state evolves in time, the distribution over the position observable “updates” over all space. This is manifestly counter to the central tenet of relativity that an event can only influence other events within its light cone. Second, fixed-particle quantum mechanics cannot account for particles being created or destroyed, which routinely happens, for example, any time an excited atom emits a photon. Third, prior to QFE, quantum mechanics described how a particle behaves in a prescribed potential but gives no account of the origin of that potential.~~

~~What elements did early quantum mechanics “take as givens”? First, and most basically, it assumed the existence of “particles” and “waves” as operationally defined physical entities. Electrons were particles with paradoxically wave-like behavior governing the distribution of measurements, while light came in the form of waves with paradoxically particle-like properties upon detection. Of course, early quantum theory wrestled with wave/particle duality, but what it didn’t do was attempt to push the understanding of waves and particles down a level so that particle-like behavior and wave-like behavior grew out of a common substrate. One is tempted to think that early quantum mechanics suggests that that “quantization” means energy comes in “quanta” that are particles, but early quantum mechanics actually says nothing of the sort. Quantization in early quantum mechanics related to energy levels in bound systems stemming from the periodicity of the U1 symmetry of the wave function, but it did not associate such quantization with the existence of particles. However, QFT, through so-called “second quantization” does fulfill this intuition, defining particles as quanta of excitation of a field in spacetime.~~

~~Second, quantum mechanics assumes the pre-existence of potentials that particles live in. It has no account of where these potential come from, nor how there influence has no account of local mediation of influence. In Newton’s gravitation, if you were to snuff out the sun, the earth would immediately be cut loose. In Maxwell’s electromagnetism, if you were snuff out a charge, the impact would have to propagate through the field, somewhat like interconnected springs. Relativity demands such local mediation, for otherwise influence would exceed light speed. But according to Schrödinger’s equation, $`i\partial_{t}\psi = H\psi,`$ as the state evolves, the distribution over all of space updates. To say it differently, the wave function is a function over configuration space – there is simply nothing in early quantum mechanics that “shakes hands” from neighbor to neighbor in spacetime and thus abides its structure. **\[HERE\]** Third, in its early incarnation, quantum mechanics did not explain the origin of potentials. For example, in the model of the hydrogen atom, the electron was treated according to the rules of quantum mechanics, but it did so using a Hamiltonian that included the Coulomb potential due to the charge of the nucleus with no account of where that potential arose. We have discussed how potentials can arise from gauge interactions. In QFT, we will see that all potentials except gravity arise from interactions between matter and gauge fields. Finally, early quantum mechanics assumed that particles were never created or annihilated, nor converted from one type to another. In QFT, all these elements – particles as quanta of energy, dynamical behavior that adheres to relativistic local causality, potentials and forces, and particle creation – arise from a dynamic spacetime field of operators acting on a wave function in state space. One can always then ask, “but what are the fields made of”? Our answer is, sticking to our theme, that they are what is allowable under our world’s constraints – its symmetries, its causal structure, and its distinguishability of states.~~

***spaces intro material***

~~Classical mechanics incorporates spacetime, phase space, and symmetry structure. Quantum mechanics needs this classical structure in translated form, but it also needs a new space, state space, because a quantum state is not a point in phase space. Quantum field theory keeps the quantum state space, restores local objects to spacetime in the form of fields, enlarges the state space to allow variable particle number, and requires the resulting arrangement to satisfy both relativistic symmetry and unitary evolution.~~
~~***The Limits of Early Quantum Mechanics***~~

~~In this essay, we have tried to present modern physics in the most logically economical way possible, deliberately avoiding the historical twists and turns by which the subject was actually discovered. But in quantum theory we must break somewhat with that principle, partly because quantum theory is hard to digest in one gulp, and partly because quantum field theory builds on early quantum mechanics more than it replaces it. In its early phase, quantum mechanics was busy inventing a brilliant new formalism to express wildly counterintuitive evidence. It was not, at the same time, giving a full account of the ontology implied by that evidence — that is, a full account of what kinds of things the world contains and how they are represented in the theory. QFT goes much further in that direction, though it too falls short of a final ontology, most obviously in that it does not include gravitation in the same framework.~~

~~What, then, did early quantum mechanics take as givens? First, and most basically, it took for granted what “particles” and “waves” were. The experiments that led to quantum mechanics showed that entities that had seemed particle-like, such as electrons, produced interference patterns characteristic of waves, while entities that had seemed wave-like, such as light, arrived in localized detection events characteristic of particles. One therefore gets the impression that “quantization” means that energy comes in particle-like quanta. But early quantum mechanics did not yet really explain that connection. In its original form, quantization appeared most clearly as the discreteness of allowed states in bound systems, tied to the phase structure of the wave function and the periodicity of its symmetry. It did not yet supply a general account of particles themselves. QFT does.~~

~~Second, early quantum mechanics had no intrinsic account of local mediation of influence. In Newtonian gravitation, if one could somehow snuff out the sun, the earth would be cut loose immediately. In Maxwell’s electromagnetism, by contrast, if one were to snuff out a charge, the change would have to propagate through the field, more like a disturbance traveling through an interconnected medium. Relativity demands such local mediation, because otherwise influence would outrun light. But in Schrödinger’s equation,~~

``` math
i\partial_{t}\psi = H\psi,
```

~~the state evolves as a single object, and with it the amplitude distribution over all of configuration space. To say this differently, the wave function is not, in general, a thing spread point by point through ordinary space. It is a function on configuration space. Early quantum mechanics therefore does not tell its story in terms of local quantum degrees of freedom shaking hands from neighbor to neighbor through spacetime, and so does not build relativistic locality into its foundations.~~

~~Third, early quantum mechanics did not explain the origin of the potentials it used. In the hydrogen atom, for example, the electron was treated quantum mechanically, but the Hamiltonian simply included the Coulomb potential due to the nuclear charge, without any account of how that interaction itself arose. As we have discussed, potentials can arise from gauge interactions. In QFT, all nongravitational potentials are understood instead as arising from interactions between matter fields and gauge fields.~~

~~Finally, early quantum mechanics assumed that particles were neither created nor annihilated, nor converted from one species into another. The number and type of particles were built in from the start. QFT changes this completely. In it, particles appear as excitations of fields, interactions are mediated locally, and creation and annihilation are part of the formalism itself.~~

~~One can always ask, of course, what the fields themselves are made of. Our answer, in keeping with the theme of this essay, is that they are not made of anything more primitive within the theory. Rather, they are the kinds of entities permitted by the constraints the world appears to obey — its symmetries, its causal structure, and the distinguishability of its states. We can begin building toward QFT by examining one of these gaps more concretely: the way early quantum mechanics fails, by construction, to respect relativity at the level of its basic objects.~~

~~We can see the incomplete nature of quantum mechanics in three ways. First, non-relativistic quantum mechanics is an “everything everywhere all at once” model. When the state evolves in time, the distribution over the position observable “updates” over all space. This is manifestly counter to the central tenet of relativity that an event can only influence other events within its light cone. Second, fixed-particle quantum mechanics cannot account for particles being created or destroyed, which routinely happens, for example, any time an excited atom emits a photon. Third, prior to QFE, quantum mechanics described how a particle behaves in a prescribed potential but gives no account of the origin of that potential.~~

~~Given that we want to put quantum mechanics in a spacetime setting, it makes sense that we must choose to give either the state or the operators a spacetime dependency and that we must choose some set of spacetime points as our domain. We will choose to situate the operators in spacetime. After all, it is observables that define an experimental basis in which to make measurements in spacetime. And we will choose our domain to be a field~~ $`\widehat{\phi}(x)`$~~. Fields are necessary because relativity leaves only two possibilities, and one is impossible. If influence could act directly across a spacelike gap, then because spacelike separated events have no observer-independent time order, one observer’s cause could be another observer’s effect, opening the door to causal paradox. So influence cannot simply jump the gap. But once it does not jump the gap, whatever later makes a difference elsewhere must be instantiated in the intervening region while it is on its way. The moment one says that information propagates, one has already admitted local degrees of freedom that carry it from place to place. In the continuum, that distributed local state is what we call a field. While our target is a field, we will start with a discreet lattice and take the continuous limit when needed. Specifically, QFT can be modelled as a lattice of coupled springs. The mechanism of springs, or, more abstractly, simple harmonics oscillators, is somewhat justified as any well-behaved periodic motion is approximated to first order by an SHO. The sites themselves do not behave as SHOs due to their coupling to neighboring sites, however, the Fourier modes, as we will explain, do behave as independent SHOs. The associated mode amplitudes correspond to the eigenvalues of the mode operator on each mode, thus weighting the field’s components in the mode expansion. This model, we will show, ensures that disturbances to the field travel in accordance with relativity.~~ ~~As we know, scalars, vectors, and spinors all transform under Lorentz, and, indeed, in quantum fields the localized operators can transform as any of these objects.~~ ~~\<HERE: check transition.\>As we have seen \[I don’t think we showed this in the QM section, need to add it there\], levels in a quantum harmonic oscillator are discreet, or quantized. The same is true of the quantum field’s oscillators in momentum space where the overall field behavior can be decomposed into oscillations of uncoupled modes. This allows the addition of quanta to the field by stepping up a level in the energy of a mode. Each such addition is a new particle. Every species of particle is an excitation in the associated field. The collection of fields is all there is. Kinematics describes the free behavior of each field in isolation, and interaction within or between the fields is the origin of dynamics. Particles properties come from the fields. The mass of the particle is determined by the mass in term in field equation, while its spin is determined by how the operators transform. In the position basis, the expectation value of the field operator squared is the particle number density.~~

*~~We construct~~* $`\widehat{\phi}(x)`$*~~as a field — that is, as an operator attached to each spacetime point. Fields are, as we have seen, a natural way to place physics back into space, because they allow influence to pass locally, from neighbor to neighbor, rather than by mysterious action at a distance. For intuition, we may picture the field as a discrete lattice and take the continuous limit when we wish. QFT is not literally a box of springs, but it is well modeled, at this level of thought, by such a lattice of coupled oscillators. This is not an arbitrary choice. Near equilibrium, many well-behaved systems reduce to the simple harmonic oscillator, and so the spring is less a toy than a first approximation to almost anything that wiggles. In the quantum version, the local amplitudes of these oscillators become operators. They are not numbers sitting there in advance, but they yield numerical expectation values in a given state, telling us how much excitation, how much “stuff,” is present at a place. And when this local spring-lattice picture is passed to its continuum limit, the resulting wave equation has the right finite-speed structure for relativity. Different observers do not see different physics. They transform the same local propagation into their own reference frames.~~*

*~~As we have seen, the levels of a quantum harmonic oscillator are discrete, or quantized. The same becomes true of the field’s modes in momentum space, where the coupled motion of the whole field can be decomposed into independent oscillations. There, to raise the energy of a mode by one step is to add one quantum to the field. Each such quantum is a particle. In this way, particles are not little beads inserted into the theory from outside, but excitations of fields already spread throughout space. Each species of particle is an excitation of its associated field. Its mass is set by the characteristic mass term of the field equation, while its spin depends on how the field transforms — whether as a scalar, a vector, or a spinor.~~*

~~While the operators live in spacetime, physics is a story of time evolution, and so we split position and time and think of the operators over position space, and then time-evolve them. This gives us the customary field picture in which configurations evolve in time, like vibrations on a drumhead. The time evolution is given by the different equation:~~

``` math
\frac{d}{dt}\widehat{\phi}(\mathbf{x},t) = i\lbrack\widehat{H},\widehat{\phi}(\mathbf{x},t)\rbrack.
```

~~where~~ $`\widehat{H}`$ ~~the system Hamiltonian and the commutator is defined as usual. Because this is a differential equation, it is analogous to Newtonian or Hamiltonian classical equations of motion, but with quantum mechanical upgrade that rather than integrating to a path, it now integrates to a distribution of path amplitudes. Now, just as we can take an alternate approach in classical mechanics and find the entire path that extremizes the action, in QFT can integrate over complex-weighted field histories between initial and final states to assign an amplitude to each initial-to-final history:\~~

``` math
\langle\phi_{f}(x),t_{f} \mid \phi_{i}(x),t_{i}\rangle = \int_{\phi(x,t_{i}) = \phi_{i}(x)}^{\phi(x,t_{f}) = \phi_{f}(x)}{\mathcal{D}\phi(x)\text{ }}e^{iS\lbrack\phi(x)\rbrack/\hslash}
```

~~Here, the left-hand side is the amplitude of transitioning from~~$`\ \phi_{i}`$ ~~to~~ $`\phi_{f}`$~~, and the right-hand side is an integral over all possible “paths” from~~ $`\ \phi_{i}`$ ~~to~~ $`\phi_{f}`$~~, each complex-weighted by it associated action. This approach, the “path integral formulation” turns out to be more practical for do real world computations. This equation is admittedly imposing. In fact, almost all the mathematical heavy lifting we will undertake will be to build up to and employ the path integral formulation. Once we have done so, we will see that it maps directly to the familiar Feynman diagrams of particle interactions.~~

<figure>
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image499.png" style="width:1.96575in;height:1.51594in" alt="A beginner&#39;s guide to Feynman diagrams ..." />
<figcaption><p><del>Figure 66 - Feynman diagram</del></p></figcaption>
</figure>

*~~While the operators live in spacetime, physics is a story of time evolution, and so we split position and time and think of the operators over position space, then time-evolve them. This gives us the customary field picture in which configurations evolve in time, like vibrations on a drumhead. The time evolution is given by the differential equation~~*

``` math
\frac{d}{dt}\widehat{\phi}(x,t) = \frac{i}{\hslash}\text{ }\lbrack\widehat{H},\widehat{\phi}(x,t)\rbrack,
```

*~~where~~* $`\widehat{H}`$*~~is the system Hamiltonian and the commutator is defined as usual. Because this is a differential equation, it is analogous to Newtonian or Hamiltonian classical equations of motion. But with the quantum change, integrating it no longer yields a single path. It yields a time-evolved operator that, when applied to a state, yields amplitudes for possible histories.~~*

*~~Now, just as we can take an alternate approach in classical mechanics and find the entire path that extremizes the action, in QFT we can integrate over complex-weighted field histories between initial and final states to assign an amplitude to the transition between them:~~*

``` math
\langle\phi_{f}(x),t_{f} \mid \phi_{i}(x),t_{i}\rangle = \int_{\phi(x,t_{i}) = \phi_{i}(x)}^{\phi(x,t_{f}) = \phi_{f}(x)}{\mathcal{D}\phi(x)\text{ }}e^{iS\lbrack\phi(x)\rbrack/\hslash}.
```

*~~Here, the left-hand side is the amplitude of transitioning from~~* $`\phi_{i}`$*~~to~~* $`\phi_{f}`$*~~, and the right-hand side is an integral over all possible field histories between those boundary conditions, each complex-weighted by its associated action. This approach, the path integral formulation, turns out to be especially practical for real-world computations. This equation is admittedly imposing. In fact, almost all the mathematical heavy lifting we will undertake will be to build up to and employ the path integral formulation. Once we have done so, we will see that it leads directly to the familiar Feynman diagrams of particle interactions.~~*

*~~Figure 66 — Feynman diagram~~*

~~Once we have our model of operator valued fields, what do we calculate with it? In one sense, we use it to calculate the behavior of any physical system. It is, after all, currently the “only game in town.” But real-world calculations are very difficult and often involve using low-energy or fixed-particle approximations where these are sufficient. At the same time, such calculations are composed of elemental building block calculations. This is what we are after – what is the most elemental thing QFT can calculate. In fixed-particle quantum mechanics, this building block calculation is:~~

``` math
\langle f \mid U(t_{f},t_{i}) \mid i\rangle
```
~~This is saying, if I prepare an initial state~~ $`\mid i\rangle`$ ~~and time evolve it, I can calculate the amplitude for a given final state~~ $`\mid f\rangle`$~~. For example, if we have a “particle in a box” and we know its initial position, we can find the amplitude for a given final position. Now there is a subtle point in this setup in that we assumed the “box,” that is, the potential, to be given to us. In QFT, we are obliged to extract the potential from interactions. For this reason, we need our model to have an entity representing “completely free fields.” We do this by assuming “incoming” particles infinitely far in the past and “outgoing” particles infinitely far in the future. Then, the time evolution operator that that maps the amplitude of the incoming state to the outgoing state incorporates all the interactions that lead to this transition. We call this encapsulation of all interactions “scattering matrix,” as the “scattering angle” encodes for momentum is exchanged in a collision. Note that we are explicitly working in the momentum basis as we can invoke momentum conservation to constrain possible interactions. We summarize this calculation as:~~

``` math
\langle out \mid S \mid in\rangle
```

~~This is just the situation we create in the particle accelerator lab where we have a beam of particles of a narrow momentum distribution impinging on some target and producing new particles registered by a detector. The beam is~~ $`\mid in\rangle`$~~, the detected particles are~~ $`\mid out\rangle`$~~, and operator that yielded this transition is the scattering matrix. The specific calculation we make is to use observed~~ $`\mid in\rangle`$ ~~and~~ $`\mid out\rangle`$ ~~states to construct the scattering matrix.\
\
It may seem that we have “downgraded” what we claim to know about a system from a rich “movie” of evolving distributions over space or momentum, to a black-box “collision” in which we don’t know any of the details about what happened in the interaction, but only that whatever happened conserved the appropriate observables. In fact, however, the richer “knowledge of every moment” we had in quantum mechanics came at the expense of an account of the origin of dynamical behavior. We replace the tidy “box” and rich “movie” with the leaner, but conceptually prior, interactions between fields.\
\
It would be sad to arrive, after much effort, at the scattering matrix and not recover the ability to make any real-world calculations. Since we don’t want to be sad, we will use QFT and its use of gauge theory in the appropriate limit to calculate the “Coulomb force law,” that is the force electric fields exert on charge particles.~~

*~~Once we have our model of operator-valued fields, what do we calculate with it? In one sense, we use it to calculate the behavior of any physical system. It is, after all, the deepest framework we currently have for nongravitational physics. But real-world calculations are often extremely difficult, and in many low-energy settings we use nonrelativistic or fixed-particle approximations when those are sufficient. Still, such calculations are built from more elemental ones. That is what we are after here: what is the most elemental thing QFT calculates?~~*

*~~In fixed-particle quantum mechanics, the basic building-block calculation is~~*

``` math
\langle f \mid U(t_{f},t_{i}) \mid i\rangle.
```

*~~This says that if I prepare an initial state~~* $`\mid i\rangle`$*~~and let it evolve in time, I can calculate the amplitude for a final state~~* $`\mid f\rangle`$*~~. For example, if I specify a particle moving in a prescribed potential, I can ask for the amplitude that it later be found in some other state. There is already a subtlety here, however. The potential is assumed to be given. Quantum mechanics tells us how states behave in that interaction environment, but not, at that level, where the interaction itself comes from.~~*

*~~QFT goes one level deeper. Its fundamental input is not a prescribed potential, but interacting fields. For this reason, the cleanest first calculation is not the evolution of a particle inside a permanently given background, but the transition from completely free particles before an interaction to completely free particles after it. We therefore define asymptotic “in” states infinitely far in the past and asymptotic “out” states infinitely far in the future. The operator connecting them is the scattering matrix,~~*

``` math
\langle out \mid S \mid in\rangle.
```

*~~This is the amplitude for one incoming particle configuration to become another outgoing configuration after all allowed interactions have taken place.~~*

*~~This is also the situation engineered in a particle accelerator. We prepare a beam with a narrow momentum distribution, allow it to collide with another beam or a target, and record the outgoing particles in a detector. The incoming beam defines the~~* $`\mid in\rangle`$*~~state, the detected particles define the~~* $`\mid out\rangle`$*~~state, and the theory gives us amplitudes from which observable rates and cross sections can be computed.~~*

*~~At first glance this can seem like a downgrade. In ordinary quantum mechanics, we seemed to have a richer picture: an evolving wavefunction in a tidy setting like a box or well. In QFT, by contrast, the middle of the process can seem to disappear into a black box, leaving us only with asymptotic states and conserved quantities. But that richer description in quantum mechanics came with an important limitation: the interaction structure was put in by hand. QFT gives up the tidy box in exchange for something more fundamental — a description in terms of interacting fields from which effective forces and potentials can emerge.~~*

*~~If this formalism is really to deserve the name “fundamental,” it should recover the ordinary forces we already know. We will therefore use QFT, in the appropriate low-energy limit, to recover the Coulomb interaction: the familiar inverse-square electric force as the static remnant of electromagnetic field interaction.~~*

***~~Relativity flouts our intuition – measuring sticks themselves change with relative motion – but leaves our categories intact. Quantum mechanics demands a new belief system – we can no longer reason about a world filled with objects at definite locations but must instead probe nature to find statistical patterns. These theories constitute our biggest insights into nature’s fundamental structure, but do not fit together to form a coherent and complete story. “Quantum field theory” addresses this. In this section, we will not encounter any new intuition-smashing result. Instead, we will recount the – often somewhat messy – synthesis that comprises humanity’s current working physical model of nongravitational microphysics.~~***

***~~We can see the incomplete nature of non-relativistic, or “fixed particle,” quantum mechanics in three ways. First, fixed-particle quantum mechanics is an “everything everywhere all at once” model. When the state evolves in time, the distribution over the position observable “updates” over all space. This is manifestly counter to the central tenet of relativity that an event can only influence other events within its light cone. Second, fixed-particle quantum mechanics cannot account for particles being created or destroyed, which routinely happens, for example, any time an excited atom emits a photon. Third, quantum mechanics describes how a particle behaves in a prescribed potential but gives no account of the origin of the potential.~~***

***~~In classical physics, the world is described locally. At each place, there is a physical condition, and observable quantities are just functions of that condition. Ordinary quantum mechanics changes the picture. The state is no longer something sitting plainly in space, and observables are no longer just readouts of what is there. They are actions on an abstract state, and those actions matter. This creates a tension with relativity, because relativity is, above all, a theory about what can and cannot influence nearby places in space and time. So if quantum theory is going to respect relativity, something in it must be made local again. Quantum field theory makes the decisive move. Instead of keeping all the quantum machinery outside space and then asking how space enters later, it places the observables themselves at points in space and time. That is the central idea. QFT turns quantum theory into a local language.~~***

***~~We construct~~*** $`\widehat{\mathbf{\phi}}\mathbf{(x)}`$***~~as a field — that is, as an operator attached to each spacetime point. Fields are, as we have seen, a natural way to place physics back into space, because they allow influence to pass locally, from neighbor to neighbor, rather than by mysterious action at a distance. For intuition, we will use a toy mechanical model that is nicely classically analogous and allows us to think visually. QFT is not literally a box of springs, but it is well modeled, at this level of thought, by a lattice of coupled oscillators. Near equilibrium, many well-behaved systems reduce to the simple harmonic oscillator, and so the spring is less a toy than a first approximation to almost anything that wiggles. In the quantum version, the local amplitudes of these oscillators become operators. They are not numbers sitting there in advance, but they yield numerical expectation values in a given state, telling us how much excitation, how much “stuff,” is present at a place.~~***

***~~As we have seen, the levels of a quantum harmonic oscillator are discrete, or quantized. The same becomes true of the field’s modes in momentum space, where the coupled motion of the whole field can be decomposed into independent oscillations. There, to raise the energy of a mode by one step is to add one quantum to the field. Each such quantum is a particle. In this way, particles are not little beads inserted into the theory from outside, but excitations of fields already spread throughout space. Each species of particle is an excitation of its associated field. Its mass is set by the characteristic mass term of the field equation, while its spin depends on how the field transforms – whether as a scalar, a vector, or a spinor.~~***

***~~While the operators live in spacetime, physics is a story of time evolution, and so we split position and time and think of the operators over position space, then time-evolve them. This gives us the customary field picture in which configurations evolve in time, like vibrations on a drumhead. The time evolution is given by the differential equation~~***

``` math
\frac{\mathbf{d}}{\mathbf{dt}}\widehat{\mathbf{\phi}}\mathbf{(x,t) =}\frac{\mathbf{i}}{\mathbf{\hslash}}\mathbf{\lbrack}\widehat{\mathbf{H}}\mathbf{,}\widehat{\mathbf{\phi}}\mathbf{(x,t)\rbrack,}
```

***~~where~~*** $`\widehat{\mathbf{H}}`$***~~is the system Hamiltonian and the commutator is defined as usual. Because this is a differential equation, it is analogous to Newtonian or Hamiltonian classical equations of motion. But with the quantum change, integrating it no longer yields a single path. It yields a time-evolved operator that, when applied to a state, yields amplitudes for possible histories.~~***

***~~To actually calculate with this theory, however, we will often switch viewpoints. Rather than calculating directly in this operator-valued field ontology, we can use the action-based reasoning we have already met and sum over field histories between initial and final configurations. This path integral formulation turns out to be especially practical for real-world computations and leads directly to the familiar Feynman diagrams of particle interactions.~~***

***~~Once we have our model of operator-valued fields, what do we calculate with it? In one sense, we use it to calculate the behavior of any physical system. It is, after all, the deepest framework we currently have for nongravitational physics. But real-world calculations are often extremely difficult, and in many low-energy settings we use nonrelativistic or fixed-particle approximations when those are sufficient. Still, such calculations are built from more elemental ones. That is what we are after here: what is the most elemental thing QFT calculates?~~***

***~~In fixed-particle quantum mechanics, the basic building-block calculation is~~***

``` math
\mathbf{\langle f \mid U(}\mathbf{t}_{\mathbf{f}}\mathbf{,}\mathbf{t}_{\mathbf{i}}\mathbf{) \mid i\rangle.}
```

***~~This says that if I prepare an initial state~~*** $`\mathbf{\mid i\rangle}`$***~~and let it evolve in time, I can calculate the amplitude for a final state~~*** $`\mathbf{\mid f\rangle}`$***~~. Quantum mechanics tells us how states behave in an interaction environment, but not, at that level, where the interaction itself comes from.~~***

***~~QFT goes one level deeper. Its fundamental input is not a prescribed potential, but interacting fields. For this reason, the cleanest first calculation is not the evolution of a particle inside a permanently given background, but the transition from completely free particles before an interaction to completely free particles after it. We therefore define asymptotic “in” states infinitely far in the past and asymptotic “out” states infinitely far in the future. The operator connecting them is the scattering matrix,~~***

``` math
\mathbf{\langle out \mid S \mid in\rangle.}
```

***~~This is the amplitude for one incoming particle configuration to become another outgoing configuration after all allowed interactions have taken place.~~***

***~~This is also the situation engineered in a particle accelerator. We prepare a beam with a narrow momentum distribution, allow it to collide with another beam or a target, and record the outgoing particles in a detector. The incoming beam defines the~~*** $`\mathbf{\mid in\rangle}`$***~~state, the detected particles define the~~*** $`\mathbf{\mid out\rangle}`$***~~state, and the theory gives us amplitudes from which observable rates and cross sections can be computed. We will be precise about what we are calculating, how this maps to beam experiments, and how the same framework recovers familiar force laws in the appropriate limit.~~***

***~~At first glance this can seem like a downgrade. In ordinary quantum mechanics, we seemed to have a richer picture: an evolving wavefunction in a tidy setting like a box or well. In QFT, by contrast, the middle of the process can seem to disappear into a black box, leaving us only with asymptotic states and conserved quantities. But that richer description in quantum mechanics came with an important limitation: the interaction structure was put in by hand. QFT gives up the tidy box in exchange for something more fundamental — a description in terms of interacting fields from which effective forces and potentials can emerge.~~***

***~~If this formalism is really to deserve the name “fundamental,” it should recover the ordinary forces we already know. We will therefore use QFT, in the appropriate low-energy limit, to recover the Coulomb interaction: the familiar inverse-square electric force as the static remnant of electromagnetic field interaction.~~***

***~~My immediate reaction is that this version is closer to an overture than a mini-book. It still has your full arc, but it stops trying to fully develop the path integral and makes the spring model and collider story more clearly subordinate.~~***

~~In classical physics, state is described in terms of local configuration of location and either velocity or momentum, depending on the formulation, of one body, many bodies, or a field. Observable quantities are functions on this configuration. Thus, if Relativity governs how influence propagates through spacetime, classical mechanics necessarily inherits this structure as its state is composed of spacetime points. Ordinary quantum mechanics dramatically changes this picture. State is no longer composed of spacetime points and their time derivatives, and observables are no longer just readouts of points. They are instead actions on an abstract state that cannot possibly be composed of a set of spacetime points and time derivatives as the act of observation itself changes that set. For example, if we measure a precise position, we lose all information about momentum. This is wholly incompatible with relativity which is couched in a prescribed structure of evolution in spacetime. If quantum theory is to respect relativity, something in it must be made to carry local causality. Quantum field theory addresses this keeping quantum state, but placing observables, that is, operators, in spacetime. *\*~~

~~It is another to see what this actually means in a concrete case. We need~~

*~~\<The cleanest place to begin is with the Klein–Gordon field./\> It is the simplest relativistic field, and it lets us watch the entire transition from classical medium to quantum particles without yet having to worry about spin or gauge symmetry.~~*

*~~The first thing to notice is that a free classical field is not mysterious. It is not, at bottom, anything stranger than a continuous version of a familiar mechanical system. The Klein–Gordon field may be thought of as a medium that can be displaced, oscillate, and transmit disturbances. If one wants an image, the right image is not a gas of tiny point objects. It is a vast lattice of coupled oscillators. That image is not merely pedagogical. It is, in a very literal sense, what the mathematics says.~~*

*~~Start with a real scalar field~~* $`\phi(\mathbf{x},t)`$*~~. Its Lagrangian density is~~*

``` math
\mathcal{L =}\frac{1}{2}{\dot{\phi}}^{2} - \frac{1}{2}(\nabla\phi)^{2} - \frac{1}{2}m^{2}\phi^{2},
```

*~~where~~* $`\dot{\phi}`$*~~means the time derivative and~~* $`\nabla\phi`$*~~the spatial gradient. From this follows the Klein–Gordon equation,~~*

``` math
\ddot{\phi} - \nabla^{2}\phi + m^{2}\phi = 0.
```

*~~This is already worth pausing over. The equation is second order in time and second order in space. That means it belongs to the wave-like family of equations, not the diffusive family. A diffusion equation, such as the heat equation, smooths away irregularities. It is parabolic. A disturbance instantly develops tails everywhere, even if those tails become very small far away. The Klein–Gordon equation is different. It is hyperbolic. It describes oscillation and propagation. One may still build solutions that spread, interfere, and disperse, but the basic character is that of a wave-bearing medium. This matters physically. A relativistic field must transmit structure in a wave-like way. It cannot simply smear information out like ink in water.~~*

*~~The field also has a conjugate momentum. From the Lagrangian, one finds~~*

``` math
\pi(\mathbf{x},t) = \frac{\partial\mathcal{L}}{\partial\dot{\phi}} = \dot{\phi}(\mathbf{x},t).
```

*~~This pair,~~* $`\phi`$*~~and~~* $`\pi`$*~~, plays exactly the role that~~* $`q`$*~~and~~* $`p`$*~~play for an ordinary mechanical system. The difference is that now there is such a pair at every point of space. In the previous section, that was stated abstractly as a field-theoretic canonical structure. Here, in the Klein–Gordon case, we can see what that structure is really describing. It is describing the displacement-like value of a medium and the momentum-like quantity associated with its rate of change.~~*

*~~To make this fully tangible, imagine replacing continuous space by a fine cubic lattice. At each lattice site~~* $`n`$*~~, place a little oscillator with displacement~~* $`\phi_{n}(t)`$*~~. Neighboring sites are tied together by springs. The gradient term in the continuum theory becomes the spring coupling between neighboring sites. The mass term~~* $`m^{2}\phi^{2}`$*~~becomes an on-site restoring force, as though each oscillator were also tethered weakly to its equilibrium position. The Hamiltonian becomes something like~~*

``` math
H = \sum_{n}^{}\left\lbrack \frac{1}{2}\pi_{n}^{2} + \frac{1}{2}m^{2}\phi_{n}^{2} + \frac{1}{2}\sum_{\text{neighbors}}^{}(\phi_{n} - \phi_{n + \widehat{i}})^{2} \right\rbrack,
```

*~~up to lattice-spacing factors we can suppress for the moment. This is a completely ordinary coupled-oscillator problem. Each site wants to oscillate on its own because of the~~* $`m^{2}\phi_{n}^{2}`$*~~term, but each site also wants to stay aligned with its neighbors because stretching a spring costs energy.\~~*
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image500.gif" style="width:3.84234in;height:3.84234in" />*\*

*~~So the classical Klein–Gordon field is, before quantization, a giant spring network.~~*

*~~This picture immediately explains two things. First, why the field has infinitely many degrees of freedom in the continuum limit. Each point of space can wiggle independently, just as each lattice site can. Second, why the field possesses wave solutions. If one plucks one oscillator, its springs pull on neighboring ones, which then pull on their neighbors, and so on. Disturbance travels across the lattice.~~*

*~~But the most important thing about a coupled-oscillator system is that it almost never wants to be described in terms of the individual sites. In the site basis, the oscillators are coupled. Their motions are entangled with one another in the ordinary classical sense of being dynamically linked. There is, however, another basis in which the system simplifies dramatically. One passes from local displacements~~* $`\phi_{n}`$*~~to collective oscillation patterns spread across the lattice. These are the normal modes.~~*

*~~For a translationally invariant lattice, the normal modes are discrete Fourier modes. Instead of asking how much the oscillator at site~~* $`n`$*~~is displaced, one asks how much of a sinusoidal pattern of wavelength~~* $`2\pi/ \mid \mathbf{k} \mid`$*~~is present across the entire lattice. On a finite lattice this gives a discrete set of allowed wavevectors~~* $`\mathbf{k}`$*~~, and the field may be expanded as~~*

``` math
\phi_{n}(t) = \frac{1}{\sqrt{N}}\sum_{\mathbf{k}}^{}q_{\mathbf{k}}(t)e^{i\mathbf{k} \cdot \mathbf{x}_{n}},
```

*~~with a similar expansion for the momentum variables,~~*

``` math
\pi_{n}(t) = \frac{1}{\sqrt{N}}\sum_{\mathbf{k}}^{}p_{\mathbf{k}}(t)e^{i\mathbf{k} \cdot \mathbf{x}_{n}}.
```

*~~The remarkable thing is that when one inserts this into the Hamiltonian, all the coupling between different~~* $`\mathbf{k}`$*~~-modes disappears. The lattice Hamiltonian becomes a sum of independent oscillator Hamiltonians,~~*

``` math
H = \sum_{\mathbf{k}}^{}\left\lbrack \frac{1}{2}p_{\mathbf{k}}p_{- \mathbf{k}} + \frac{1}{2}\omega_{\mathbf{k}}^{2}q_{\mathbf{k}}q_{- \mathbf{k}} \right\rbrack.
```

*~~In the continuum limit this becomes the familiar decomposition into momentum modes, and the frequency takes the relativistic form~~*

``` math
\omega_{\mathbf{k}}^{2} = \mathbf{k}^{2} + m^{2}.
```

*~~This is the decisive simplification. A field that looked like an impossibly complicated infinite mechanical object in position space has become, in momentum space, an infinite collection of decoupled harmonic oscillators. Each~~* $`\mathbf{k}`$*~~labels one independent degree of oscillation. The free field is therefore not a single oscillator but an infinity of them, one for each momentum mode.~~*

*~~This point is so central that it deserves to be said in plain language. The field is one object in space, but mathematically its free motion can be resolved into independent standing or traveling patterns, and each such pattern behaves like its own oscillator. In the local picture, neighboring sites tug on one another. In the momentum picture, those collective patterns have already been chosen precisely so that no further tugging remains. Each mode simply oscillates at its own natural frequency.~~*

*~~This is just normal-mode mechanics, but now elevated to a field. Nothing quantum has happened yet. We have only taken a classical medium and written it in the basis in which its internal couplings are diagonalized.~~*

*~~That word, diagonalized, is important. It is the same move one makes in every coupled linear system. If you write a matrix describing how the coordinates talk to one another, diagonalizing that matrix picks out the natural independent motions of the system. The Fourier transform is not magic. It is simply the basis change that does this job when the system is translationally symmetric. In a crystal lattice, these are phonon modes. In the Klein–Gordon field, they are the classical precursor of momentum eigenmodes.~~*

*~~Notice also what the parameter~~* $`m`$*~~is doing in this picture. It is tempting, especially from the particle side, to think of~~* $`m`$*~~as already the mass of some little object. But at the classical field level, it is first a local stiffness. Even the~~* $`\mathbf{k} = 0`$*~~mode, where every site moves in step and no springs between neighboring sites are stretched, still oscillates with frequency~~* $`m`$*~~. So~~* $`m`$*~~measures the field’s tendency to resist displacement even in the absence of spatial variation. Later, when the theory is quantized, this same parameter will become the rest mass of the field quanta. But here, at the classical stage, it is best understood as the intrinsic restoring scale of the medium itself.~~*

*~~We can now see the logical route to quantization. If a free classical field is nothing but an infinite collection of independent harmonic oscillators in disguise, then quantizing the field means quantizing those oscillators. Not all at once by some mysterious fiat, but one mode at a time.~~*

*~~That is why the Klein–Gordon field is such a good place to begin. It strips the procedure to its essence. One starts with a classical wave-bearing medium. One rewrites it as a sum of independent normal modes. One recognizes that each normal mode is an ordinary harmonic oscillator. Then one applies to each mode the same quantization rule one already knows from elementary quantum mechanics. The field becomes operator-valued because the amplitudes of these normal modes cease to be ordinary numbers and become noncommuting operators.~~*

*~~At this stage, the physical picture is already beginning to shift. In position space, we began with a medium spread out through space. In momentum space, we found independent oscillators. After quantization, each of those oscillators will possess discrete excitation levels. Those discrete excitations are what we will call particles. A particle of the free field is, in the first instance, not a tiny billiard ball hiding inside the medium. It is one quantum of one normal mode of that medium.~~*

*~~That sentence is the hinge on which the whole subject turns.~~*

*~~The beauty of the construction is that it reconciles two pictures that at first seem incompatible. The field picture says reality is spread out, local, and continuous in space. The particle picture says energy comes in lumps. The mode decomposition shows how both can be true at once. The field is the underlying medium-like object. Its normal modes are the independent patterns into which its motion decomposes. Quantization makes the energy of each pattern discrete. The quanta of those patterns are the particles.~~*

*~~In the next step, then, we will quantize each mode, introduce the ladder operators that raise and lower its excitation number, and see how the field operator itself can be rebuilt as a superposition of those mode quanta. That will let us say precisely what it means for a field to create particles, annihilate them, and assemble a localized excitation from many momentum modes at once.~~*

~~\[momentum basis\]~~

~~Before we move on to the decisive step of quantizing our field, we need to dive into a critical attribute of our model that will prove to be decisive for the interpretation of what it means to a be “particle.” In the position basis, the oscillators are coupled by construction. This coupling is exactly the property we require, \[but it does not diagonalize the Hamiltonian.\]~~ ~~There is, however, another basis in which the system simplifies dramatically. One passes from local displacements~~ $`\phi_{n}`$~~to collective oscillation patterns spread across the lattice. These are the normal modes.~~

~~For a translationally invariant lattice, the normal modes are discrete Fourier modes. Instead of asking how much the oscillator at site~~ $`n`$ ~~is displaced, one asks how much of a sinusoidal~~ ~~pattern of wavelength~~ $`2\pi/\mathbf{k}`$ ~~is present~~ ~~across the entire lattice. On a finite lattice this gives a discrete set of allowed wavevectors~~ $`\mathbf{k}`$~~, and the field may be expanded as~~

``` math
\phi_{n}(t) = \frac{1}{\sqrt{N}}\sum_{\mathbf{k}}^{}q_{\mathbf{k}}(t)e^{i\mathbf{k} \cdot \mathbf{x}_{n}},
```

~~with a similar expansion for the momentum variables,~~

``` math
\pi_{n}(t) = \frac{1}{\sqrt{N}}\sum_{\mathbf{k}}^{}p_{\mathbf{k}}(t)e^{i\mathbf{k} \cdot \mathbf{x}_{n}}.
```

~~The remarkable thing is that when one~~ ~~inserts this into the Hamiltonian, all the coupling between different~~ $`\mathbf{k}`$~~-modes disappears. The lattice Hamiltonian becomes a sum of independent oscillator Hamiltonians,~~

``` math
H = \sum_{\mathbf{k}}^{}\left\lbrack \frac{1}{2}p_{\mathbf{k}}p_{- \mathbf{k}} + \frac{1}{2}\omega_{\mathbf{k}}^{2}q_{\mathbf{k}}q_{- \mathbf{k}} \right\rbrack.
```

~~In the continuum limit this becomes the familiar decomposition into momentum modes, and the frequency takes the relativistic form~~

``` math
\omega_{\mathbf{k}}^{2} = \mathbf{k}^{2} + m^{2}.
```

~~This is the decisive simplification. A field that looked like an impossibly complicated infinite mechanical object in position space has become, in momentum space, an infinite collection of decoupled harmonic oscillators. Each~~ $`\mathbf{k}`$ ~~labels one independent degree of oscillation.~~ ~~The free field is therefore not a single oscillator but an infinity of them, one for each momentum mode.~~

~~This point is so central that it deserves to be said in plain language. The field is one object in space, but mathematically its free motion can be resolved into independent standing or traveling patterns, and each such pattern behaves like its own oscillator. In the local picture, neighboring sites tug on one another. In the momentum picture, those collective patterns have already been chosen precisely so that no further tugging remains. Each mode simply oscillates at its own natural frequency.~~

~~This is just normal-mode mechanics, but now elevated to a field. Nothing quantum has happened yet. We have only taken a classical medium and written it in the basis in which its internal couplings are diagonalized.~~

~~That word, diagonalized, is important. It is the~~ ~~same move one makes in every coupled linear system. If you write a matrix describing how the coordinates talk to one another, diagonalizing that matrix picks out the natural independent motions of the system. The Fourier transform is not magic. It is simply the basis change that does this job when the system is translationally symmetric. In a crystal lattice, these are phonon modes. In the Klein–Gordon field, they are the classical precursor of momentum eigenmodes.~~

*~~Before we can quantize the field, we need to rewrite the free lattice in the variables in which its energy actually separates into independent pieces. In the site basis, that is not true. Each displacement~~* $`\phi_{n}`$*~~is tied to its neighbors by the coupling springs, so the Hamiltonian is not a sum of independent local oscillator energies. A disturbance placed at one site immediately talks to the others. The local variables are useful for seeing causality and propagation, but they do not diagonalize the free dynamics.~~*

*~~So the next step is not merely to find a basis that is mathematically tidier. It is to find the variables in which the Hamiltonian becomes a sum of independent quadratic terms. That is what diagonalizing the Hamiltonian means here. We are looking for coordinates in which the free field breaks apart into non-interacting oscillators. This matters because independent oscillator energies are the quantities that will later become independently countable excitations. That is the first real hint of what will eventually deserve to be called a particle.~~*

*~~For a translationally invariant lattice, the required variables are the normal modes, which are just the discrete Fourier modes. Instead of specifying the displacement of each individual site, we describe the lattice as a superposition of collective patterns spread across all sites. On a finite lattice, only a discrete set of wavelengths fits, so the allowed wavevectors~~* $`k`$*~~are discrete. We therefore write the field as~~*

``` math
\phi_{n}(t) = \frac{1}{\sqrt{N}}\sum_{k}^{}q_{k}(t)e^{ik \cdot x_{n}},
```

*~~and similarly for the conjugate momenta,~~*

``` math
\pi_{n}(t) = \frac{1}{\sqrt{N}}\sum_{k}^{}p_{k}(t)e^{ik \cdot x_{n}}.
```

*~~It is worth being very plain about what one such mode is. A mode is not one site vibrating by itself. It is a whole-lattice pattern. In a single mode, every site oscillates in time at the same angular frequency, but with fixed relative phases and amplitudes set by the spatial pattern~~* $`e^{ik \cdot x_{n}}`$*~~. The dynamical variable~~* $`q_{k}(t)`$*~~is the amplitude of that entire pattern. That amplitude is what oscillates like a simple harmonic oscillator.~~*

*~~You can see this in the simplest examples. The~~* $`k = 0`$*~~mode is the uniform mode: every site rises and falls together. The next mode is a long-wavelength ripple across the lattice: neighboring sites are slightly out of step, but the pattern as a whole simply breathes in time. Higher-~~*$`k`$ *~~modes alternate more rapidly from site to site, producing shorter wavelengths and therefore larger restoring forces from the coupling springs. Each allowed spatial pattern has one time-dependent amplitude, and that amplitude behaves as one oscillator. This is exactly what one sees in any normal-mode decomposition of a coupled mechanical system. The only difference here is that the system has many sites, and in the continuum limit infinitely many.~~*

*~~Now comes the key fact. When these Fourier expansions are inserted into the free Hamiltonian, all cross-couplings between different~~* $`k`$*~~-values disappear. The Hamiltonian becomes~~*

``` math
H = \sum_{k}^{}\left\lbrack \frac{1}{2}\text{ }p_{k}p_{- k} + \frac{1}{2}\text{ }\omega_{k}^{2}q_{k}q_{- k} \right\rbrack.
```

*~~So the Fourier transform does not merely re-label the same messy system. It identifies the variables in which the free energy is already split into independent pieces. Each~~* $`k`$*~~-mode evolves on its own, as though it were its own oscillator, with its own natural frequency~~* $`\omega_{k}`$*~~.~~*

*~~In the continuum limit, that frequency becomes~~*

``` math
\omega_{k}^{2} = k^{2} + m^{2}.
```

*~~This is the relativistic dispersion relation we have been preparing for. The same mass parameter that appeared earlier as the frequency of the uniform on-site oscillation now appears as the rest term in the mode frequency, while the inter-site coupling contributes the~~* $`k^{2}`$*~~part. The field, viewed locally, is one extended coupled medium. The same field, viewed in momentum modes, is an infinite collection of decoupled oscillators labeled by~~* $`k`$*~~.~~*

*~~That is the decisive simplification. In position space, the field looks like an enormous coupled machine. In momentum space, its free dynamics has already been resolved into its natural independent motions. This does not yet give us particles. Nothing quantum has happened. But it gives us the classical structures that quantization will act on. Once each mode is quantized, the energy in that mode will no longer vary continuously. It will come in discrete units. Those countable units of excitation, one mode at a time, are what will become the particle interpretation of the field.~~*

*~~So the point of passing to momentum modes is not just that the algebra gets easier. It is that the free field reveals its true elementary dynamical units. A local disturbance is complicated because it is a mixture of many modes. A single mode is simple because it is already one independent oscillator. The Fourier basis is therefore not a computational trick. For a translationally invariant free field, it is the basis in which the Hamiltonian tells the truth most directly.~~*

~~//cut~~

~~To solve it, we change basis. Because the lattice is translationally invariant, the natural basis is the discrete Fourier basis. Write~~

``` math
\phi_{n}(t) = \frac{1}{\sqrt{N}}\sum_{k}^{}q_{k}(t)e^{ikx_{n}},x_{n} = na.
```

~~Since the lattice is finite and periodic, the allowed wave numbers are discrete:~~

``` math
k = \frac{2\pi m}{Na},m = 0,1,\ldots,N - 1.
```

~~Substituting this into the equation of motion, we use~~

``` math
\phi_{n + 1} = \frac{1}{\sqrt{N}}\sum_{k}^{}q_{k}(t)e^{ikx_{n}}e^{ika},\phi_{n - 1} = \frac{1}{\sqrt{N}}\sum_{k}^{}q_{k}(t)e^{ikx_{n}}e^{- ika},
```

~~so that~~

``` math
2\phi_{n} - \phi_{n + 1} - \phi_{n - 1} = \frac{1}{\sqrt{N}}\sum_{k}^{}q_{k}(t)e^{ikx_{n}}\left( 2-e^{ika}-e^{- ika} \right).
```

~~But~~

``` math
2 - e^{ika} - e^{- ika} = 2 - 2\cos(ka) = 4{\sin}^{2}\text{ ⁣}\left( \frac{ka}{2} \right),
```

~~so each Fourier component satisfies its own independent equation,~~

``` math
{\ddot{q}}_{k} + \omega_{k}^{2}q_{k} = 0,
```

~~with~~

``` math
\omega_{k}^{2} = m_{0}^{2} + 4\kappa{\sin}^{2}\text{ ⁣}\left( \frac{ka}{2} \right).
```

~~That is the decisive simplification. In the site basis, we had one coupled system. In the mode basis, we have one independent oscillator equation for each~~ $`k`$~~.~~

~~Now suppose we want a solution that is a superposition of the~~ $`k = 1`$~~and~~ $`k = 2`$~~modes. In the mode basis this is straightforward. We solve~~

``` math
{\ddot{q}}_{1} + \omega_{1}^{2}q_{1} = 0,{\ddot{q}}_{2} + \omega_{2}^{2}q_{2} = 0,
```

~~so that~~

``` math
q_{1}(t) = A_{1}\cos(\omega_{1}t + \alpha_{1}),q_{2}(t) = A_{2}\cos(\omega_{2}t + \alpha_{2}).
```

~~Then the full lattice solution is just~~

``` math
\phi_{n}(t) = \frac{1}{\sqrt{N}}\left\lbrack q_{1}(t)e^{ik_{1}x_{n}} + q_{2}(t)e^{ik_{2}x_{n}} + \text{c.c.} \right\rbrack.
```

~~If we prefer a purely real form, we can write the same solution as~~

``` math
\phi_{n}(t) = A_{1}\cos(\omega_{1}t + \alpha_{1})\cos(k_{1}x_{n}) + A_{2}\cos(\omega_{2}t + \alpha_{2})\cos(k_{2}x_{n}).
```

~~That is the solution.~~

~~Notice what has happened. In the mode basis, a two-mode solution is literally just two independent oscillator amplitudes added together. In the site basis, that same motion would have to be written out as a separate time-dependent trajectory for every site~~ $`\phi_{n}(t)`$~~. Nothing would be wrong with that, but the structure would be hidden. What is transparently “two independent normal motions” in the mode basis becomes a coordinated motion of all lattice sites at once in the site basis.~~

~~That is why the mode basis is better for the free theory. It does not change the physics. It reveals the separability that was already there.~~

Next:

1.  Insert gifs

2.  Compare/contrast PDE here to SE PDE.

3.  From section below include diagnolization. Do this in the (massless) lattice framework.

~~At each lattice site~~ $`n`$~~, place an oscillator with “displacement,” or scalar value,~~ $`\phi_{n}(t)`$~~. Neighboring sites are tied together by “springs.” The gradient term in the continuum theory becomes the spring coupling between neighboring sites. The mass term~~ $`m^{2}\phi^{2}`$~~becomes an on-site restoring force, as though each oscillator were also tethered weakly to its equilibrium position. The Hamiltonian is:~~

``` math
H = \sum_{n}^{}\left\lbrack \frac{1}{2}\pi_{n}^{2} + \frac{1}{2}m^{2}\phi_{n}^{2} + \frac{1}{2}\sum_{\text{neighbors}}^{}(\phi_{n} - \phi_{n + \widehat{i}})^{2} \right\rbrack,
```

~~Where~~ $`\phi_{n}^{2}`$ ~~is the oscillator value,~~ $`\pi_{n}^{}`$ ~~is the derivative of the value, and~~ $`m`$~~, the mass term, is the “restoring force” that maps the oscillator value a potential energy\~~

~~up to lattice-spacing factors we can suppress for the moment. This is a completely ordinary coupled-oscillator problem. Each site wants to oscillate on its own because of the~~ $`m^{2}\phi_{n}^{2}`$~~term, but each site also wants to stay aligned with its neighbors because stretching a spring costs energy.~~\
<img src="C:\Users\wadela\Documents\Codex\2026-04-18-i-want-to-set-up-a\content\manuscript-markdown\hum-non-drm-media/media/image500.gif" style="width:3.84234in;height:3.84234in" />

~~So the classical Klein–Gordon field is, before quantization, a giant spring network.~~

~~This picture immediately explains two things. First, why the field has infinitely many degrees of freedom in the continuum limit. Each point of space can wiggle independently, just as each lattice site can. Second, why the field possesses wave solutions. If one plucks one oscillator, its springs pull on neighboring ones, which then pull on their neighbors, and so on. Disturbance travels across the lattice.~~

~~Notice also what the parameter~~ $`m`$~~is doing in this picture. It is tempting, especially from the particle side, to think of~~ $`m`$~~as already the mass of some little object. But at the classical field level, it is first a local stiffness. Even the~~ $`\mathbf{k} = 0`$~~mode, where every site moves in step and no springs between neighboring sites are stretched, still oscillates with frequency~~ $`m`$~~. So~~ $`m`$~~measures the field’s tendency to resist displacement even in the absence of spatial variation. Later, when the theory is quantized, this same parameter will become the rest mass of the field quanta. But here, at the classical stage, it is best understood as the intrinsic restoring scale of the medium itself.~~

~~We can now see the logical route to quantization. If a free classical field is nothing but an infinite collection of independent harmonic oscillators in disguise, then quantizing the field means quantizing those oscillators. Not all at once by some mysterious fiat, but one mode at a time.~~

~~That is why the Klein–Gordon field is such a good place to begin. It strips the procedure to its essence. One starts with a classical wave-bearing medium. One rewrites it as a sum of independent normal modes. One recognizes that each normal mode is an ordinary harmonic oscillator. Then one applies to each mode the same quantization rule one already knows from elementary quantum mechanics. The field becomes operator-valued because the amplitudes of these normal modes cease to be ordinary numbers and become noncommuting operators.~~

~~\[End old spring section roughly\]~~

~~At this stage, the physical picture is already beginning to shift. In position space, we began with a medium spread out through space. In momentum space, we found independent oscillators. After quantization, each of those oscillators will possess discrete excitation levels. Those discrete excitations are what we will call particles. A particle of the free field is, in the first instance, not a tiny billiard ball hiding inside the medium. It is one quantum of one normal mode of that medium.~~

~~That sentence is the hinge on which the whole subject turns.~~

~~The beauty of the construction is that it reconciles two pictures that at first seem incompatible. The field picture says reality is spread out, local, and continuous in space. The particle picture says energy comes in lumps. The mode decomposition shows how both can be true at once. The field is the underlying medium-like object. Its normal modes are the independent patterns into which its motion decomposes. Quantization makes the energy of each pattern discrete. The quanta of those patterns are the particles.~~

~~In the next step, then, we will quantize each mode, introduce the ladder operators that raise and lower its excitation number, and see how the field operator itself can be rebuilt as a superposition of those mode quanta. That will let us say precisely what it means for a field to create particles, annihilate them, and assemble a localized excitation from many momentum modes at once.~~

clean.

1.  Intro

2.  Gaps in quantum mechanics\
    2.1 The relativistic mismatch\
    2.1.1 Why the Schrödinger equation is not a relativistic field equation\
    2.1.2 Why fixed-particle quantum mechanics has no local carriers of influence\
    2.2 The interaction problem\
    2.2.1 Potentials are inserted rather than explained\
    2.2.2 Local causality demands intermediate degrees of freedom\
    2.3 The particle-number problem\
    2.3.1 Relativity allows creation and destruction\
    2.3.2 Fixed-$`N`$ Hilbert spaces are too small

3.  Spaces\
    3.1 Spacetime and local operators\
    3.1.1 Why operators\
    3.1.2 Why fields\
    3.1.3 What is attached to spacetime\
    3.1.4 Locality, causality, and measurement regions\
    3.2 State space and Fock space\
    3.2.1 Why a separate state space is needed\
    3.2.2 Why the state is an amplitude assignment rather than a configuration\
    3.2.3 Why relativistic theory cannot keep particle number fixed\
    3.2.4 Why Fock space is the right state space for variable excitation number

4.  Quantize a field\
    4.1 Classical Klein–Gordon\
    4.1.1 A lattice model\
    4.1.2 The continuum limit\
    4.1.3 The Klein–Gordon equation\
    4.1.4 Why this field is relativistically acceptable\
    4.2 Quantize Klein–Gordon\
    4.2.1 Canonical variables for the field\
    4.2.2 Equal-time canonical commutators\
    4.2.3 Mode expansion\
    4.2.4 Each normal mode as a quantum harmonic oscillator\
    4.3 Free-field structure\
    4.3.1 Ladder operators\
    4.3.2 Vacuum and Fock space\
    4.3.3 Time evolution of modes\
    4.3.4 What a particle is in the free theory

5.  Kinds of calculations\
    5.1 The S-matrix\
    5.1.1 In-states and out-states\
    5.1.2 What an amplitude means\
    5.1.3 Why scattering is the natural calculation\
    5.2 Beam experiments formally\
    5.2.1 Asymptotic particle states\
    5.2.2 Cross sections and what labs actually measure\
    5.2.3 Why this is the bridge from theory to experiment

6.  Path integral formulation\
    6.1 Conceptual route to the path integral\
    6.1.1 From local equations to summed histories\
    6.1.2 Why the action appears again\
    6.1.3 Why this formulation is useful for QFT\
    6.2 Perturbation theory and diagrams\
    6.2.1 Expanding around the free theory\
    6.2.2 Propagators and vertices\
    6.2.3 Feynman diagrams as terms in the expansion\
    6.2.4 What diagrams do and do not mean

7.  More fields\
    7.1 Dirac field\
    7.1.1 Why spin-$`\frac{1}{2}`$ needs a different field\
    7.1.2 Anticommutators and statistics\
    7.1.3 Matter quanta\
    7.2 Gauge fields\
    7.2.1 Why spin-1 fields are different\
    7.2.2 Local symmetry and gauge redundancy\
    7.2.3 The photon field\
    7.3 QED\
    7.3.1 Coupling matter to gauge fields\
    7.3.2 The interaction term\
    7.3.3 What QED claims exists

8.  Derive classical electromagnetism\
    8.1 The Coulomb limit\
    8.1.1 Exchange amplitudes in the static limit\
    8.1.2 Recovering the Coulomb potential\
    8.1.3 Why a force law reappears in the classical regime

\
## 

## 

## 

## 

## 

## 

## 

## 

## 

## 


Top of Form

Bottom of Form
