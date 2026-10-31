for now 10/30:
1. introduce eigenvalues earlier?
2. clarify dynamic vs kinematic in intro and later
3. redo last section as "kinematic structure"
4. unitarity as extra condition?
5. add some of the foundational equations for symmetry arguments. commuting with time, etc.
6. comment that qunatum principle is really getting rid of old principle that definite things have definite locations and follow definite paths that move smoothly from one definite location to another.
7. state space: lead with commutation structure has to be and then, voi la, actual wave structure (H3) fits the bill. 
8. change action/phase to more cut a dried: two views: particles moving on paths, wave propogation. what has to give: particles move on -many- paths at once.
9. Variation of whole QFT field.

voice overs
share with miles
relativity
introduce eigenvalues earlier
clarify dynamic vs kinematic in intro and later
redo last section as "kinematic structure"
reel 15 and 17 dedup
unitarity as extra condition?
add some of the foundational equations for symmetry arguments. commuting with time, etc.
write introduction outline

3 changes:
1. comment that qunatum principle is really getting rid of old principle that definite things have definite locations and follow definite paths that move smoothly from one definite location to another.
2. state space: lead with commutation structure has to be and then, voi la, actual wave structure (H3) fits the bill. 
3. change action/phase to more cut a dried: two views: particles moving on paths, wave propogation. what has to give: particles move on -many- paths at once.


2. per bot: 
Let $X$ represent position and $T(a)$ a unitary translation by distance $a$. Translating a preparation by $a$ must shift its possible position outcomes by $a$:

```math
T(a)^\dagger X T(a)=X+aI.
```

Continuous unitary translations have a self-adjoint generator $K$:

```math
T(a)=e^{-iaK}.
```

Differentiating the first equation at $a=0$ gives:

```math
i[K,X]=I
\qquad\Longrightarrow\qquad
[X,K]=iI.
```

The canonical commutation relation follows from requiring quantum position and physical displacement to agree, before introducing the Heisenberg group.

FULL QFT field action variation per bot:
```math
\mathcal A[\Psi,\Psi^*]
=
\int dt\int\mathcal D\varphi\,
\left[
\frac{i\hbar}{2}
\left(
\Psi^*\partial_t\Psi
-
(\partial_t\Psi^*)\Psi
\right)
-
\Psi^*\hat H\Psi
\right],
\qquad
\Psi=\Psi[\varphi,t],
\qquad
\delta\mathcal A=0.
```

the argument:
spacetime symetries evident. pool table misrepresents, need relativity, but consituents the same. call this overall symmetry P (for poincare). This means laws of motion (E[phi]) are same under any poincare transformation.  the vector space where these operators act on this state has to be of a certain form to abide the symmetry. (P => L2) this tells us the form of the state. Once we know that, we know its waves and, if Ut is to be unitary (what unitary is) global phase translations must not change the laws. but since waves can represented by X and K, and [x,k] = i (=> phi), x,k area must be preserved. this gives rise to the canonical relations. And the canoncial relations tell us the laws. (what have we done? we've done this w/o a variational procedure, the fuck)

check this w/ last few chats

check w/ LLM

the intro:
when we hear the ideas of modern physics -- objects are in two place at once, time slows down when we speed up, gravity is the curvature of spacetime -- they seem trippy, but beyond the reach of any but those who can't explain what they mean to the rest of us. they seem like secrets understood only to the monastic order of physics graduate students. they seem relegated for the rest of us said trippiness without hope of greater depth. Similarly, when we dig a little and hear formulation like "energy generates time translations" or "particles are representations of symmetry," we hear something metaphorically promising -- the same energy we dig out of the plastocene sediment and that we see in a golden retriever puppy -- that energy? The same symmetry we see in a snowflake? A thing is a representation of a relationship? But tantalizingly, if we make just a little progress in understanding the mathematical meaning of such statements, we realize this amazing thing. Their metaphorical richness coincides with mathematical definition, which is just to say, precise definitions. It is this promise that has led me to trying to understand these statement precisely and to subsequently write this book. Perhaps it will be met with the reaction that "you are decidely not a member of the order and have not understood its secrets." But if it can be blessed as a tiny bit explicative, the claim it makes is that it is often easier to learn from someone who has scratched and clawed for an understanding than from someone who is fluent in it.

what follows doesn't quite fit into the popular science mold. it is more technical and mathematical. but neither is it textbook. it is assuredly unreliable as such. It attempts to say nothing new, either about physics or its philosophical interpretation, but only to retell the bedtime story that is the physicist's favorite. however, while no new physics claims are intendend, several pedagogical claims are. First, borrowing inspiration from the great math and physics explainers on Youtube, we believe that visualization can aid tremendously in understanding. When the content of an equation can be conveyed in an animation, it is so much easier to understand. Second, we can skip the details. A nongoal of this book is to train working physicists to solve problems. (All the goal decidedly is to help physicists in training get the big picture that alluded me and so many in undergraduate physics and math.) Skipping details does not mean skipping rigor. It means saying as little as possible to advance the conceptual framework of the theory. Third, we treat math a learnable. Calculus and basic linear algebra (vectors and matrices) is expected, but everything else is explained along with the physical arguments contained in the mathematical expresssions. Third, while this is 99.9% a book about physics and 0.1% a book about philosophy, we think of it as natural philosophy. That is, we think we can "argue" for the form of modern physical theory from "principles" we can agree on. Our goal is that anything conclusion that can be derived is, and any detail that doesn't advance the argument is left out. Fourth, we explicitly do not present ideas in the order they were discovered historically. Typical physics curriculuum does this to an extent, largely because the older theories tend to be in a way less abstract, and for training a physicist, universities need to help students gain  problem solving skills alongside understanding theory. But when struggling to lay out the conceptual map, having to decipher logical order from historical order only confuses matters. Our goal is purely to explicate that current theory. 

The hope of this book is to make supposedly inaccessible material accessible. At one level, this is a matter of understanding different specific concepts. That is its own gratifications, and one which I very much wish to pay forward from the enjoyment I've experienced consuming the explanations of various creators, especially devoted pedagogs and autodidacts in visual media. At another level, the book is about making the physical theory feel neither god given, nor ingeniousl data fitting, but the result of reasoning from first principles. Einstein's lay writing on relativity is my model for this kind of story-telling. It conveys that the high-barrier equations are secondary to and derivative of more general reasoning. A cautionary note is in order here. The logical structure for which I argue is, I hope, a decently economical argument for the most orthodox version of existing theory. It is neither an elucidation of the only theory, nor the only elucidation of the orthodox theory for which argues. It's not easy to avoid the linguistic trope of "this therefore that," which conveys a sense of absolutism which is not at all the case. Beyond the fact that science is, as a fully committed call to action, never settled, there are, in practice, competing variations of current theory, and here, we present just one route, to one version. But is, hopefully, a route about which the reader could say, "I could have come up with that."

With that, let's enumerate our bag of principles from which we will argue for the equations and methods on contemporary physics:

- An overarching them, is that fulfilling the following principle is a property of physical laws. We may think the laws "just are" and the principles are not principles, but just attributes of the laws. But in practice, starting with the principles and using them to motivate and assess laws is the way theorizing tends to proceed. This is emphasized when an existing theory can be to violate a principle and is then replaced new theories that do fulfill the principle. This is not to say our principles are inviolable. It may well be the evidence requires us to abandon them.
- Our first principle is so obvious it barely deserves mentioning and will not really be mentiond again. We adhere unwaveringly to experiment evidence. Where such evidence contradicts deeply intuitive, instinctive preconceptions, we abide the evidence. This has two corrallaries which we will employ more specifically.
-- When we consider phenomenological evidence, but we must put the observer at the center of the evidence. We are strict that every experiment has an observed and an observer that play equal roles in the formulation of laws. We never work out a law for an "omniscient" or "preferred" observer. Our laws always specify the frame of the observer on equal footing with the system under observation.
-- When no conceivalble observations can distinguish intuitively different phenomena, we have only one theoretical element corresponding to those phenomena. That is, we consier them the same phenomena.
 - The laws of physics are the same in the future as they are now and the same in one part of the universe as in another. We can call this the "symmetry of physical behavior" for reasons we will explain. There are other symmetries as well that we will enumerate. At first blush, this sounds like a property of physical behavior, or laws, which it is, but, as we will see, if we adopt the view that it is a requirement of the laws, that requirement goes enormously far toward constraining and motivating the laws. This idea of working from the symmetry of space and time toward the laws of physics will occupy a large poriton of this webbook.
 - Physical evolution (of a fully specified isolated sysetm) cannot erase information. Imagine a board with sliding tiles labelled with numbers. We can count the number of possible configurations. No matter how we move the tiles around, the count is the same. What if we were to sand off the numbers on two tiles? We've now expanded the system to include the sandpaper, and the sanding process leaves grains of sand in some information-carrying configuration. There is no way to lose information because there is nowhere for information to hide. This idea will manifest in various guises -- as distinguishability of states, as determinism and reversibility of evolution, as conservation of probability. In the model we will work toward, this principle will be realized by  a mathematical property called "unitarity." 
- Influence and signalling cannot happen across a distance without mediation. We can think of this as "there has to be a handshake from one neighbor to the next for influence to propagate." This is often called the "local causality." An upshot of this principle is our theories must provide specify some value at every point in space. That is, we must think of "fields," like ponds of water, and not isolated bodies, like model solar systems. A further upshot is that fields must be physically active. They cannot transmit "handshakes" if they are inert.
- The evolution a system undergoes in reality can be found by first finding some functional of the history (the history is a function over state variables, and a functional is a function of a function) that is stationary (doesn't change to first order) with history variations. This is often referred to as the principle of least action, where action is the functional of paths (or histories, in a field evolution context), and minimization is one case of being stationary. 
- Even if we could "deduce" valid theories from these principles, empirical observation must supply the values of constants in the theory. There are mathematical constants like pi and e that we can know from theory, but there is no way to deduce physical constants like the speed of light, the strength of gravitation, or the scale at which energy is quantized. 
- There is guesswork in devising theories. Applying the principles above can greatly narrow down that guesswork. But theorizing proceeds by trying out different assumptions that are consistent with some set of principles and working out the consequences of those assumptions.
- The last principle is more elusive as it is not apparent from instinct or intuition. It is the nexus of postulates, above and beyond our other principles, that form quantum mechanics. Summarizing these in a single slogan cannot do the theory justice, but that caution notwithstanding, we can say that the the new principle centers around the notion that the observations of an object's state always presents as distribution of outcomes. This principle is more extreme than merely saying observations of a system's state do present as distributions, it is saying they can must always present as distributions, that the theory rules out predicting definite values for all possible measurements of a systme.

The webbook is organized into chapters. First, we will discuss symmetry, mostly as a primer on vocabulary we will need throughout the remaining chapters. But we will sketch some derviations of results in quantum mechanics that come directly from symmetry relationships. Next, we will discuss the structure of spacetime, also known as special relativity. This will provide us with the full spacetime symmetry physical descriptions must abide, unify space and time into a single geometry, and, in terms of this geometry, give us an understanding of the maximum speed at which signals can travel, of the defining relationship between momentum and energy, and of defintion of mass. We will also discuss the different kinds of fields that can carry spacetime symmetry. Next, we will discuss the principle of least action. Here we will adopt the view that the description of forces acting on objects can be described equivalently, and with greater adherence to spacetime constraints, in terms of geometric structure, where paths are, in an abstract sense, some variation on the "shortest distance between two points." Next, we combine our understanding of spacetime and variational reasoning, along with an assumption that matter and forces are fields that permeate space, to describe two field theories -- gravitation and electromagnetism. In fact, we will not fully describe electromagnetism which requires later material, but will discuss enough to motivate the ideas of "gauge theory," which grows out of a consideration of symmetry and extends to the weak and strong forces as well. Next, we will delve into quantum mechanics. We'll look at some the key experiments that force us to reject classical assumptins, and then apply our understanding of symmetry and spacetime to work out a theory that explains these experiments. We will take time here to meditate on the strange ideas of superposition, uncertainty, wave collapse, and entanglement that seem to strain our ability to maintain all our principles. We will also describe the origin of particle classifications. Finally, we will put quantum mechanics into a relativistically compliant field setting, called quantum field theory. Here we will revisit motivating electromagnetism, with the language of QFT to bring to bear on the derivation.

I will hopefully keep philosophical ruminations to a minimum, but let's close with one here. Science seems to progress toward humility. We learn again and again, that we do not have an omniscient perspective, and things in the world are not obliged to fit into a structure that reflects our preconceptions. Modern physics pushes the humility to the limit. In relativity, we ask not "how do objects move through space in time that must be the same for everyone" but "how can observers from differnt perspectives relate their ruler and clock measurements to agree on a sequence of events?" With quantum mechanics, we take a radical step toward even greater humility, saying, as some would have it, that "our theory makes no claim, indeed, relies on making on no claim, about what takes place between observations." 






Yes. The organizing mathematics fits into a handful of equations. Your “two groups and time evolution” is a useful way to organize it. Two implications need adjusting, which we can see directly in that compact account.

Write $U_t$ for time evolution.

Poincaré transformations preserve Minkowski geometry:

$$
\Lambda^{T}\eta\Lambda=\eta.
$$

Here $\eta$ supplies the spacetime interval. This preservation is built into the definition of the group. It does not follow from how its elements interact with time evolution.

The laws must also respect those transformations:

$$
\mathcal E[\Phi]=0
\quad\Longrightarrow\quad
\mathcal E[g\Phi]=0.
$$

Here $\Phi$ is an entire history, and $\mathcal E[\Phi]=0$ says it obeys the laws. Transforming that history must produce another history obeying the same laws. This includes boosts. For a time-independent transformation that leaves the time coordinate unchanged, it reduces to $gU_t=U_tg$. Thus preserving the geometry and respecting the laws are separate requirements.

Closed-system evolution preserves the wave-state inner product:

$$
\langle U_t\psi,U_t\chi\rangle
=
\langle\psi,\chi\rangle.
$$

This is the independent physical requirement of unitarity. Your broader description can be “preservation of the relevant geometry of state space.”

The already-established Heisenberg relationship therefore survives evolution:

$$
[X_t,K_t]
=
U_t^\dagger[X,K]U_t
=
iI,
$$

where $X_t=U_t^\dagger XU_t$, and likewise for $K_t$. This constrains how the two operators can change together.

Global phase also commutes with evolution:

$$
U_t e^{i\phi}I
=
e^{i\phi}I\,U_t.
$$

But phase commutation is not the intermediate step that forces preservation of the Heisenberg relationship. Phase commutation follows from complex linearity. Preservation of the commutation relationship follows from evolving both operators through the same unitary transformation. They are parallel consequences, rather than successive links in the argument.

**why H3 unitarity matters**
In the derivation I just gave, I made it redundant by already treating \(X\) and \(K\) as valid quantum observables. That assumes something important that \(H_3\)’s unitarity supplies.
Unitary position and wave-number shifts have self-adjoint generators—operators suitable for representing real-valued measured quantities. The bare commutation relation does not guarantee this. Woit’s formulation
For example, replace \(K\) with
\[
K'=K+i\alpha X,
\qquad \alpha\text{ real and nonzero}.
\]
Then
\[
[X,K']=[X,K]=iI.
\]
The commutation structure survives perfectly. But \(K'\) is no longer self-adjoint under our original inner product, and its transformations no longer preserve that inner product.
Requiring a unitary \(H_3\) representation excludes this possibility. It ensures that our canonical operators fit the probability geometry of the states. We then construct the generator of time evolution using physical observables, subject to its own requirements.
So its substantive role comes when we establish the physical position–wave-number representation.

--- derivation of EOMs from symmetry ---
1. symmetyr => function rep
2. reqquire unitarity
3. unit => self-adjoint generator
4. spacetime translation must act on wave functions unitarily to preserve probabilities 
5. waves carry H3
6. H3 gives generator eigenvalue eqs: \[X\psi=x\psi,\qquadK\psi=-i\partial_x\psi,\qquad[X,K]=iIx`\]
7. Og = f(K) b/c each mode must evolve independently

