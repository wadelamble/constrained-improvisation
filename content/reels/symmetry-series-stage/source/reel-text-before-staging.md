# Symmetry to Waves — complete desktop adaptation

Twenty-seven offline reels follow the manuscript from the pool table through complex exponentials. Every desktop animation and diagram before Fourier has a place in this series. The previous sixteen-reel version remains available separately.

The Casimir and Lie algebra reels are included as **17** and **16**. The full series is numbered consecutively from 1 to 27.

An additional unitarity reel is temporarily labeled **24a**, between Reels 24 and 25. Existing reel numbers remain unchanged.

Edit the **Title** and **Caption** fields below. The gallery generates the series number, next-reel pointer, website link and hashtags automatically. Their characters count toward the caption limit. Titles and on-screen text are baked into the video and require a new render after editing.

The on-screen entries use stable ordered slots. Edit wording in place and preserve the number and order of entries. Equations use TeX for video rendering. Numeric readings are calculated from the animation. Source notes and visual checks are for offline review and are not posted.

Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/

#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics

---

## Reel 01
### Title

Symmetries of physical behavior

### Caption

Strike a pool ball with a cue, and the balls move in an expected way. Move the table over a few feet, and the balls move in recognizably the same way. Wait a few minutes, and the balls move in the same way. Turn the pool table a few degrees, and the balls still move the same way. Put the pool table on a train at constant velocity, and, again, the balls move in the same way. These are the manifest ‘**symmetries**’ of the world we live in — position and time translation, rotation, and velocity ‘boosts.’

Our pool game illustrates what we mean by symmetries of physical behavior, but why should we start our story here? We will argue that symmetry constrains both the laws that govern physical evolution and the classification of the objects that undergo that evolution. The term ‘symmetry’ in this context may not at first glance seem like the same concept as, say, a triangle’s symmetry, but it precisely is, as we will see.

The animation compares each transformed collision with the reference experiment. The positions on the screen change, and an observer moving relative to the table assigns different velocities, but the relation between the incoming and outgoing motion remains the same. That relation is what our account of the collision must preserve.

We can move the table a few feet to the right or the observer a few feet to the left. When discussing **invariants**, quantities unchanged by a symmetry, we often think in terms of what observers agree on. We will start with the familiar world of discrete symmetries and build up the definitions we need from there. Then we will turn to continuous rotations and translations, where symmetry ideas meet calculus and waves arise naturally.

### On-screen text

- Position translation
- Time translation
- Rotation
- Velocity boost
- Reference experiment
- Transformed experiment
- \mathbf{x}'=\mathbf{x}+\mathbf{a}
- t'=t+b
- \mathbf{x}'=R\mathbf{x}
- \mathbf{x}'=\mathbf{x}+\mathbf{u}t
- Equal masses · elastic collision

### Source

Symmetry opening paragraphs and Invariants observer paragraph. Opening and motivation closely preserve manuscript wording. The collision comparison clarifies what stays the same under a boost without making a relativistic claim. The series ends at the pre-Fourier wave construction.

- animations/symmetry-pool-table.mp4

### Visual check

Four transformed collisions, compared with the reference experiment.

---

## Reel 02
### Title

A triangle’s six symmetries

### Caption

We can see the obvious symmetry of an equilateral triangle. To categorize its symmetry, we can write down all the actions that leave it unchanged. We can do nothing, rotate 120°, rotate 240°, flip along an axis, flip then rotate 120°, and flip then rotate 240°. There are six actions, including the one in which we do nothing.

‘Unchanged’ needs a little care here. The labeled vertices move, but the outline of the triangle returns to itself. A vertex may arrive where another vertex began. Keeping track of A, B, and C lets us distinguish actions that leave the same outline, including the action that leaves every vertex where it began. This do-nothing action is called the **identity**.

The animation carries the vertices through each action and compares the result with the reference outline. A rotation through 100° would leave the triangle pointing somewhere else. The intermediate angles on the way to 120° are not additional triangle symmetries. The allowed rotations are **discrete**.

We say the triangle belongs to the **D₃ symmetry group**. The group contains these six actions and the way they compose. Performing one allowed action and then another always gives an action already on the list. Two 120° rotations give a 240° rotation, and three return every vertex to its starting point. Performing the same flip twice does so too.

We can plainly see the triangle’s symmetry, but we also have the beginnings of a mathematical description. Instead of treating each motion as an unrelated event, we can ask how actions combine, which action reverses another, and how to keep track of the labels through a sequence of moves.

### On-screen text

- Discrete symmetry actions
- Identity
- 120° rotation
- 240° rotation
- Reflection
- Reflection + 120°
- Reflection + 240°
- D_3=\{e,r,r^2,s,rs,r^2s\}
- r^3=e
- s^2=e
- D₃ is more general than triangles

### Source

Discrete symmetries six-action list and Representations opening. Composition examples unpack the source's use of symmetry group. The outline is invariant, while labels distinguish actions. Intermediate animation frames are explicitly not extra group elements.

- diagrams/symmetry-triangle.svg
- animations/symmetry-triangle-actions.mp4

### Visual check

Labeled triangle, all six discrete actions and return to the reference outline.

---

## Reel 03
### Title

From symmetric shapes to symmetry groups

### Caption

Any number of objects possess D₃ symmetry. We tend to think of a ‘triangle’s symmetry,’ not the symmetry of two rotations and flips about three axes, but this latter way of thinking in terms of symmetry groups is more general. The group describes the actions and how they compose, rather than the particular outline on which we first noticed them.

The triangle, three circles, three petals, and three rounded bars in the animation have different outlines. Yet a 120° rotation returns each outline to itself, and so does a reflection along an appropriate axis. Each object realizes the same six actions. The rotation cycles three positions, and the reflection exchanges two while leaving the third in place.

In physics, we ask less ‘what symmetry does this or that object have?’ and more ‘what mathematical objects realize the actions of a symmetry group?’ The change in emphasis matters. Once we identify the group, we can study its structure without choosing one particular shape as the only object it can act on.

We would like to write these actions in a symbolic form that abstracts moving a picture. Our next step is to let three positions carry labels or numerical values and describe how the symmetry moves them. The same group will then act on a vector, giving us a mathematical representation of the symmetry.

### On-screen text

- The same actions on different objects
- 120° rotation
- Reflection
- D_3=\{e,r,r^2,s,rs,r^2s\}
- r^3=e
- s^2=e

### Source

Discrete symmetries, paragraph following symmetry-d3-carriers.svg, and Representations opening. The group-versus-object argument preserves the manuscript's wording and sequence. Extra examples explain composition without introducing a second group.

- diagrams/symmetry-d3-carriers.svg

### Visual check

Triangle and all three other carriers undergo the same rotation and reflection.

---

## Reel 04
### Title

Representations — the state vector

### Caption

We can plainly see the symmetry of the triangle, but what if we want to write it down mathematically? We can find a **representation** of the symmetry group in a linear vector space, representing states with vectors and group actions with linear transformations of those vectors. Let’s start by seeing how we can map the state of our object to a vector.

Suppose we label the triangle’s three vertices A, B, C and allow each to store a number. We can record these values in an ordered column with three entries. The ordering tells us which vertex each entry describes. A state might then be written (1, 3, 5).

We are recording the three stored values, not the horizontal and vertical coordinates of a point in the drawing. One can think of this as a function with a domain consisting of three inputs. Different choices of the three values give different **state vectors** in that space.

A rotation permutes the entries in accordance with the motion of the vertices. In the convention we will use, a 120° rotation sends (1, 3, 5) to (5, 1, 3). A flip that fixes the first vertex exchanges the other two entries. These rules apply to any three values we choose.

There is nothing special about the vertices here. We could just as easily have chosen the midpoints of the edges or any other triplet of points with the triangle’s symmetries. The same rule would permute the values attached to those positions. We have separated the information being transformed from the rule that transforms it. Next we will write that rule as a matrix.

### On-screen text

- Vertex labels
- Ordered components
- A
- B
- C

### Source

Representations opening, vertex-to-vector diagram, permutation example, and stored-information paragraph. Explicitly distinguishes three component values from the two spatial coordinates of the triangle drawing. Ordered tuples stand in for columns in caption text.

- diagrams/symmetry-d3-vertices-to-vector.svg

### Visual check

A, B, C explicitly map from triangle vertices to ordered column components.


---

## Reel 05
### Title

Representations — transformation matrices

### Caption

Our state vector records the values stored at the triangle’s three vertices. We can now write the symmetry actions as matrices that transform this vector.

The matrix R for a 120° rotation sends (a, b, c) to (c, a, b). The matrix S for a flip sends (a, b, c) to (a, c, b). For example,

R(1, 3, 5) = (5, 1, 3),
S(1, 3, 5) = (1, 5, 3).

Applying R three times returns every component to its starting position. Applying S twice does the same. In matrix notation, R³ = I and S² = I, where I is the **identity matrix**. These are the same composition rules we found by turning and flipping the triangle.

We can write the defining requirement for a representation as

D(g₁g₂) = D(g₁)D(g₂).

Here g₁ and g₂ are group actions, such as a rotation and a flip, and D(g) is the matrix representing action g. D itself is the map from symmetry actions to matrices. This says that the matrix for the composed action, g₂ followed by g₁, is the product of the matrices for the separate actions. The action on the right is applied first.

The transformations are **linear** because permuting a sum of vectors gives the same result as permuting each vector and then adding.

R(u + v) = Ru + Rv,
S(u + v) = Su + Sv.

Here u and v are any two state vectors. Multiplying every component by a number also commutes with the permutation. We can therefore use the same matrix for any values stored at the vertices.

A set of actions from which all the others can be constructed is called a set of **generators**. One 120° rotation and one flip suffice for D₃. Composing them gives the remaining rotation and the other two flips. A small collection of matrices now describes every symmetry on our list.

### On-screen text

- Matrices act on component values
- Rotation
- Reflection
- Before
- After
- D(g_1g_2)=D(g_1)D(g_2)
- R^3=I
- S^2=I

### Source

Representations definition, displayed matrices, and generators paragraph. Uses a minimal generating pair, which is sufficient and consistent with the manuscript's larger generating set. Explains matrix composition order and linearity.

Additional animation of the manuscript’s equations.

### Visual check

Follow cyclic permutation and reflection of components, with the representation composition equation.


---

## Reel 06
### Title

3 dimensional representation of the D₃ group

### Caption

Let’s now take our state vector and assign any values to its components. What happens to our state vector when we cycle those values in accordance with a rotation of the triangle? Our vector rotates by 120° about the diagonal axis where all three components are equal, as we can see in the animation. Similarly, when we permute the values in accordance with flips of the triangle, our vector reflects across planes that contain that axis.

Each coordinate axis in this picture records one component value. A state (a, b, c) is a point in this space, and the vector from the origin to that point is the **state vector**. Cycling the entries sends the point to (c, a, b). Repeating the action traces a three-point orbit around the diagonal where all three components are equal.

Every vector on the diagonal axis has the form (q, q, q). Permuting its entries does nothing, so the entire axis stays fixed. This is the axis about which the rotation matrix turns the rest of the space. The animation shows each turn continuously, but only rotations by multiples of 120° belong to D₃.

The flip keeps one component and exchanges the other two. If the exchanged values already agree, the state does not move. These fixed states form a plane containing the equal-components diagonal. States away from the plane are reflected across it.

Notice a pattern in our representation. Our vector has “slots” and “values,” and the symmetry moves the values to different slots in accordance with its allowed permutations, regardless of what the values themselves are. We will see that continuous functions, which can be treated as infinite-dimensional vectors with their inputs serving as slots, are similarly suited to state representations.

### On-screen text

- Equal-components axis
- Rotation
- Reflection
- Reflection plane
- v₁
- v₂
- v₃
- R^3=I
- S^2=I

### Source

Representations 3D visualization and following plane/average discussion. Derives the fixed reflection plane and orbit plane from the source's permutation matrices. The ambient representation is three-dimensional, distinct from the triangle's physical plane.

- animations/symmetry-d3-rotations-vs-flips.mp4

### Visual check

Compare rotation about the fixed equal-components diagonal and reflection through a plane containing it. Show axes, traces and labels.

---

## Reel 07
### Title

Irreducible representations

### Caption

We may notice something about our three-dimensional visualizations. All transformed versions of a vector lie in a plane perpendicular to the diagonal, and the orbit planes are parallel. Permuting components preserves the average of their values, which fixes where each plane meets the diagonal. Subtracting that average from each component moves this intersection to the origin without changing how the group actions compose. This removes the vector’s common component, leaving the part on which the symmetry acts nontrivially in a plane through the origin.

Now we ask a question. Are there subspaces of our three-dimensional space such that every state vector starting in one stays in it under any composition of symmetry transformations? For our earlier vector, the average of the components is 3. We can separate it into a common part and a zero-sum part.

(1, 3, 5) = (3, 3, 3) + (−2, 0, 2).

The common part lies on the rotation axis and is unchanged by every permutation. The zero-sum part lies in a plane through the origin. Although written with three components, it needs only two independent numbers, since the third must make their sum zero. The three stacked orbits in the animation move into this same plane when their common parts are removed.

The three-dimensional representation decomposes into two subspaces, one one-dimensional and the other two-dimensional. Each stays within itself under every group action. Neither contains a smaller nonzero subspace preserved by every action. These are called **irreducible representations**, or **irreps** for short.

In quantum physics, particles are classified by how their states respond to symmetry transformations. In our D₃ example, state vectors with equal components in the one-dimensional irrep behave differently from those in the two-dimensional irrep. Likewise, particles of different types, such as electrons and protons, belong to different irreps of spacetime symmetry.

### On-screen text

- Common part and zero-sum part
- Common part
- Zero-sum part
- \mathbf{v}=\overline{v}(1,1,1)+\mathbf{w}
- w_1+w_2+w_3=0
- \mathbf{3}=\mathbf{1}\oplus\mathbf{2}

### Source

Representations common/zero-sum decomposition, irreducibility, and particle-motivation paragraphs. Preserves the manuscript's reason for introducing irreps. The irreducibility definition is restricted to nonzero proper invariant subspaces, avoiding the trivial zero-space exception.

- animations/symmetry-d3-irrep-collapse.mp4

### Visual check

Build all three stacked triangular orbits, subtract the common components and turn face-on.

---

## Reel 08
### Title

Invariants

### Caption

Once we have chosen a representation for a symmetry, we might well ask, how do we know our transformations preserve the symmetry? If we look at a triangle and rotate by 100°, we can see that it does not overlay itself. In a representation, we need mathematical expressions that say 
"this transformation left the triangle the same." We call these the **invariants** of the transformation.

In our two-dimensional representation of D₃, a symmetry action cannot change these expressions in the coordinates of an arbitrary vector:

r² = x² + y²,
u = x³ − 3xy² = r³ cos(3θ).

Here r is the vector’s length and θ its angle from the reference axis. The first expression gives its squared length. The second records the threefold structure of its orientation. A 120° turn adds 360° inside cos(3θ), and a flip across the x-axis changes θ to −θ. Both leave u unchanged.

These exact invariants for D₃ are not the important and are, in fact, more complicated than invariants we will encounter later. What matters is the idea that we can write an expression in coordinates that must not change under a symmetry transformation.

The “sameness” we see in our pool game is reflected in physical laws of motion that are invariant under symmetry transformations. There are, however, much simpler invariant quantities. For example, translating the table leaves distances between the balls unchanged. These simple invariants provide indispensable clues in the quest to find physical laws.

From our triangle, we have learned about **symmetry groups**, **representations**, **states**, **transformations**,  **generators**, **irreducible representations**, and **invariants**. This takes us a long way toward the symmetry concepts we need to understand modern physics.

### On-screen text

- Invariants of discrete rotations
- Allowed D₃ endpoints
- Between endpoints
- r^2=x^2+y^2
- u=x^3-3xy^2=r^3\cos(3\theta)
- Squared length
- Cubic invariant
- Current
- Reference

### Source

Invariants section, including the variational-calculus motivation omitted from the old series. Discrete invariants are compared at action endpoints. Preserves necessary invariance without claiming that two numbers certify arbitrary transformations.

Additional animation of the manuscript’s equations.

### Visual check

Squared length and cubic D3 invariant, including changing cubic value between group endpoints.

---

## Reel 09
### Title

Continuous symmetries

### Caption

What rotations return a circle to itself? All of them! Similarly, all translations return a line to itself. The symmetries of space and time are **continuous** and can therefore be represented as transformations that depend on continuously varying parameters.

The animation turns a marked circle against fixed reference marks. The full circle overlays itself at every angle, while the moving marks let us follow the transformation. The growing arc records how far it has turned. The same distinction applies to the line. Its marks move as it slides, but the unmarked mathematical line still occupies the same set of points. The frame shows only a finite window of that line.

For the triangle, rotations that return the outline to itself are separated by 120°. For the circle there is no smallest positive angle. If we can rotate by 1°, we can rotate by half a degree or a hundredth of a degree. A continuously varying angle describes a whole family of transformations. Translation distance plays the corresponding role for the line.

As we saw in D₃, we can build any action from a combination of elemental rotations and flips. Now let us ask what the generator of a continuous transformation should be. Suppose we want to rotate a circle by 10°. We could compose ten 1° rotations. But what if we want to rotate by 1°? We can see where this is going. The generators must describe infinitesimal rotations. Does this sound like calculus? It should.

Calculus gives us a way to take the derivative of a transformation with respect to its parameter, at the point where no transformation has yet occurred. This gives a local infinitesimal generator. The remaining task is to see how to integrate that generator to supply a finite transformation.

### On-screen text

- SO(2): rotation
- Translation
- \theta\in\mathbb{R}
- a\in\mathbb{R}
- R(\theta)
- T(a)

### Source

Continuous symmetries and Infinitesimal Generators opening. Marks are tracking aids rather than extra features required to remain fixed. The finite plotted line is identified as a window onto an infinite line.

- animations/symmetry-continuous-so2-translation.mp4

### Visual check

Rotate the full marked circle against fixed reference marks and grow the angle arc. Translate marked line.

---

## Reel 10
### Title

Lie algebra

### Caption

We may think of a continuous symmetry group as a smooth space, or manifold, whose points represent transformations. Such a smooth symmetry group is called a Lie group. The identity is the point representing no change. Differentiating the transformations with respect to their parameters at the identity gives the infinitesimal generators. These belong to a linear vector space, the tangent space at the identity, whose elements are linear combinations of independent generators that form a basis. This gives us an infinitesimal description of the group through its associated Lie algebra. Integrating an element in the Lie algebra supplies a family of finite transformations in the group.

We can visualize this with a 2-dimensional curved surface embedded in 3-dimensional space. If we zoom in enough, a smooth curved surface appears flat. At the identity point on this surface, a **tangent plane** describes changes in the transformation to first order in its parameters. The surface may bend away as we move farther from the point, but sufficiently small displacements can be described by vectors in that plane.

The two arrows shown in the tangent plane are independent basis generators. Linear combinations describe every tangent direction in this plane, supplying the local directions available to a symmetry. In general a tangent space can be of any dimension. The "plane" is just convenient for visualization.

Here the object being differentiated is a transformation, which we can write as a matrix whose entries depend on the transformation’s parameter. Its derivative with respect to that parameter will also be a matrix. Acting on a state, that generator will produce the tangent to the state’s path. To be clear, the tangent vector the generator produces is not in the space of transformations (visualized here) but in the representation space in which the state lives. 

### On-screen text

- Curved surface
- Tangent plane
- Two independent tangent directions
- \mathbf{e}_1
- \mathbf{e}_2

### Source

Infinitesimal Generators opening and tangent-plane illustration. Expands the manuscript's compact geometric analogy, distinguishing tangent vectors in the group at identity from their induced tangents on state space. Does not identify an arbitrary pictured surface as a specific group.

- diagrams/tangent-plane-curved-surface.png

### Visual check

Curved surface, local tangent plane and two independent tangent vectors.

---

## Reel 11
### Title

The exponential map of SO₂ rotations

### Caption

In the two-dimensional representation of SO₂ rotations, the single parameter θ specifies the operator matrix R(θ). To obtain the matrix that generates an infinitesimal nudge, we differentiate R with respect to θ and evaluate the derivative at θ = 0, where R(0) = I is the identity transformation.

This gives the generator

J = [[0, −1], [1, 0]].

The two bracketed pairs are the rows of the matrix. Applied to v = (x, y), J gives (−y, x). At the point (1, 0), it produces the tangent vector (0, 1). J acts on any point on a circle centered at the origin to produce the tangent vector at that point. Putting this into calculus notation,

dv/dθ = Jv.

We now have a differential equation for the transformation that uses the generator. We found it by starting with a known transformation and deducing its generator. But we can just as well go in the opposite direction. Given this differential equation, we can find the transformation:

v(θ) = exp(θJ)v(0).

The exponential of a matrix is defined in terms of the Taylor expansion for an exponential. Here exp(θJ) means I + θJ + θ²J²/2! + θ³J³/3! + ⋯. Since J² = −I, its even powers alternate between I and −I, while its odd powers alternate between J and −J. Collecting the terms gives the familiar series for cosine and sine:

exp(θJ) = cos(θ)I + sin(θ)J = R(θ).

This is an **exponential map**. It takes the Lie algebra element θJ and returns the finite symmetry transformation R(θ). 

### On-screen text

- Infinitesimal rotation
- State
- Tangent
- \frac{d\mathbf{v}}{d\theta}=J\mathbf{v}
- J^2=-I
- e^{\theta J}=\cos\theta\,I+\sin\theta\,J
- R(\theta)=e^{\theta J}

### Source

Infinitesimal Generators derivative-at-identity calculation through exponential map. Preserves the source's differential equation, J² identity, Taylor-series argument, and concluding language. Caption matrix rows are explicitly identified.

- diagrams/so2-tangent-at-identity.png

### Visual check

Identity point and tangent, derivative generator, finite exponential action.

---

## Reel 12
### Title

Vector field flows

### Caption

We can think of a symmetry transform as a ‘uniform looking’ vector field. Here we ask not what happens when the transformation is applied to a single set of starting conditions, but what the transformation does to all starting conditions. This view lends itself to seeing the structure in the evolution of a collection of nearby states.

For rotation, the generator J sends the point (x, y) to the tangent vector (−y, x). We first draw that vector at one point, then apply the same rule throughout the plane. The resulting arrows form a **vector field**. Each arrow says how the state at that position changes when the angle increases by an infinitesimal amount.

Releasing the colored points lets us see the flow generated by this field. At each point along a trail, the motion follows the local tangent. The direction changes continuously, carrying the state around a circle. Farther from the origin, the tangent arrows are longer because the same change in angle sweeps out a greater distance. The origin remains fixed.

Every starting point obeys the same differential equation,

dv/dθ = Jv,

and its finite transformation is v(θ) = exp(θJ)v(0). The different arrow directions do not represent different generators. They are the result of one generator acting on different states.

Following nearby points together shows more than following a single point. Their whole arrangement turns, and the trails reveal the family of circular paths across the plane. This is the geometric content of the transformation acting on its entire representation space. The parameter here is the angle θ. The animation unfolds a rotation as that parameter changes, so its playback need not describe the physical motion of objects through time.

### On-screen text

- One state
- Every state
- Flow
- Tangent
- J(x,y)=(-y,x)
- \mathbf{v}(\theta)=e^{\theta J}\mathbf{v}(0)
- x
- y

### Source

Symmetry Flows, with the already-derived state equation from Infinitesimal Generators. Opens with manuscript prose and explains the source animation's one-tangent, field, and flow sequence. Explicitly identifies the flow parameter as angle.

- animations/symmetry-so2-vector-field-flow.mp4

### Visual check

One tangent, the tangent field everywhere, release colored points and draw growing colored trails.

---

## Reel 13
### Title

Rotations preserve the inner product

### Caption198

What is the invariant of rotation in this representation? It is just the length of vectors and the angles between them. The two arrows turn together, so their directions change while their relationship does not. The length of one arrow’s projection onto the other remains the same.

These relationships are expressed by a single invariant, the **dot product**, or more generally, the **innner product**. If u and v are vectors in the plane,

u · v = uₓvₓ + uᵧvᵧ = |u||v| cos θ.

Here uₓ and uᵧ are the components of u, and similarly for v. The vertical bars mean length, and θ is the angle between the arrows. Rotating both changes the individual component values but leaves the sum uₓvₓ + uᵧvᵧ unchanged.

Taking the dot product of a vector with itself gives its squared length, u · u = |u|². Taking the dot product of two different vectors tells us their angle once their lengths are known. One mathematical relationship therefore accounts for both the lengths and the angle preserved in the animation.

A mathematical structure that supplies reliable rulers for measuring lengths and angles in a space is called a **metric**. Rotations preserve this metric. We can use these rulers to compare vectors before and after a transformation, even though their coordinate values have changed. For an ordinary rotation, this is intuitive. 


### On-screen text

- Lengths and angles stay fixed
- (R\mathbf{u})\cdot(R\mathbf{v})=\mathbf{u}\cdot\mathbf{v}
- \mathbf{u}\cdot\mathbf{v}=|\mathbf{u}|\,|\mathbf{v}|\cos\theta
- |\mathbf{u}|=1,\quad |\mathbf{v}|=\frac{3}{4},\quad \theta=60^\circ
- \mathbf{u}\cdot\mathbf{v}=\frac{3}{8}
- x
- y
- u
- v
- θ

### Source

Invariants and Metrics, retaining the source's question, dot product, reliable-rulers description, and hyperbolic transition. Dot product notation is defined locally. Does not conflate vector norm with distance of translated point coordinates from a fixed origin.

- animations/symmetry-rotation-vector-invariants.mp4

### Visual check

Two unequal vectors rotate while their lengths and angle stay fixed.

---

## Reel 14
### Title

The invariant interval of hyperbolic rotation

### Caption

If we replace x² + y² with x² − y², we obtain a different geometry. Rotations preserving this expression are called **hyperbolic rotations**. As it turns out, spacetime is described with this geometry. We label the coordinates t and x, giving t² − x². Separation between points can stretch out without bound as the rotation approaches its asymptotes, leaving the invariant interval unchanged even though the separation appears to grow using our everyday notion of distance.

Here we choose units in which the speed of light is 1, so time t and position x can appear on the same plot. The transformation is

t′ = t cosh η + x sinh η,
x′ = x cosh η + t sinh η.

The parameter η plays a role similar to the angle in ordinary rotation. The functions cosh and sinh are the hyperbolic counterparts of cosine and sine. Their identity cosh²η − sinh²η = 1 ensures that t′² − x′² = t² − x². The point follows a hyperbola instead of a circle.

The animation follows two points and the segment between them. Each point keeps its own interval from the origin. Because both undergo the same linear transformation, their coordinate differences do too. If Δt and Δx are the differences between their time and position coordinates, then

Δt′² − Δx′² = Δt² − Δx².

The ordinary length of the connecting segment changes, but its hyperbolic interval remains fixed. The new ruler gives a different answer from the familiar sum of squares, and the symmetry preserves precisely that new answer.

Such a hyperbolic metric encodes the asymptotic limit of light speed in relativistic spacetime. Different inertial observers assign different times and positions to events while agreeing on their spacetime interval. The diagonal asymptotes are the light-speed directions. We are introducing the geometry here, with its physical meaning to be developed in the next chapter.

### On-screen text

- Two points under the same boost
- (ct)^2-x^2=1\qquad(c=1)
- η
- x
- ct
- A
- B
- Ordinary tip distance
- B(\eta)=
- \cosh\eta
- \sinh\eta
- A:\ (ct_A)^2-x_A^2=1
- B:\ (ct_B)^2-x_B^2=1

### Source

Invariants and Metrics hyperbolic paragraph and two-point source animation. Adds the explicit positive-η transformation and separation invariant to explain the depicted pair. Units c = 1 are stated. The connecting segment is not claimed to be a spacelike proper distance.

- animations/symmetry-hyperbolic-rotation.mp4

### Visual check

Two points on the hyperbola, connecting segment, changing ordinary separation and fixed hyperbolic intervals.

---

## Reel 15
### Title

Commutation in symmetry groups

### Caption

We're familiar with operations on numbers like addition and multiplication being commutative. That is, $a + b = b + a$ and $ab = ba$. But when transformations that are elements of a symmetry group are composed, the order of their application may produce different states. For example, in the three-dimensional rotation group, **SO(3)**, rotating about the x-axis then the y-axis leaves a marked sphere in a different state than applying the same actions in the opposite order.

### On-screen text

- Same rotations, different order
- R_yR_x\ne R_xR_y
- R_x\;\longrightarrow\;R_y
- R_y\;\longrightarrow\;R_x
- x
- y
- z
- [J_x,J_y]=J_z

### Source

Commutators, Lie Algebra, and Invariants and Casimir operators. Includes the small-parameter exponential correction, curved-surface consequence, local/global distinction, and Casimir motivation. Omits the full Casimir calculation and translation-mass example for space. L² is the angular-momentum convention from the manuscript, not J².

- animations/symmetry-so3-rotation-order.mp4

### Visual check

Same start, opposite orders of two 90-degree rotations, different final orientations.

---

## Reel 16
### Title

The commutator encodes group structure locally

### Caption

In a Lie algebra, these ordering relations are expressed by the **commutator**

[X, Y] = XY − YX. 

The commutator is itself an element of the Lie algebra. That is, it must be some linear combination of the full set of generators. For rotation generators, this takes a simple form:

[Jₓ, Jᵧ] = J_z,
[Jᵧ, J_z] = Jₓ,
[J_z, Jₓ] = Jᵧ,

where Jₓ, Jᵧ, and J_z generate rotations about the x-, y-, and z-axes, respectively.

This is a clever bit of math. The overall order-dependence of finite actions is encoded into the relations of infinitesimal generators. (There are global features that cannot be anticipated from a local view, such as a space wrapping around on itself, such as in the video game “Asteroids.”)

We can see how this works visually. As in the previous animation, rotations about different axes depend on their order. But now, we make the rotation angles smaller, bringing the two results closer toward the infinitesimal. 

Let Rₓ(a) and Rᵧ(b) rotate through small angles a and b. Applied to a vector v, the two orders agree through first order in the angles. Their leading difference is proportional to the product ab. The animation magnifies that difference by dividing by ab, so it remains visible as both angles shrink:

(Rₓ(a)Rᵧ(b) − Rᵧ(b)Rₓ(a))v / (ab) → J_zv.

Here J_zv is the infinitesimal change in v produced by rotation about z.

The commutation relations encode the group’s local structure independently of the representation. Every representation must preserve them.

### On-screen text

- Run the same two rotations
- Overlay the two results
- Shrink both angles
- Cycle the axis pairs
- The generators close
- y then x
- x then y
- z then y
- y then z
- x then z
- z then x
- First rotation
- Second rotation
- Same starting frame
- Rightmost rotation acts first
- Blue minus red
- Magnified mismatch
- Magnification = 1/(ab)
- rad
- Lie algebra
- Generators + commutators
- x
- y
- z
- R_x(a)R_y(b)\mathbf{v}
- R_y(b)R_x(a)\mathbf{v}
- R_y(a)R_z(b)\mathbf{v}
- R_z(b)R_y(a)\mathbf{v}
- R_z(a)R_x(b)\mathbf{v}
- R_x(b)R_z(a)\mathbf{v}
- R_x(a)R_y(b)\ne R_y(b)R_x(a)
- R_i(\theta)=e^{\theta J_i}
- a=b
- \Delta\mathbf{v}
- \frac{\Delta\mathbf{v}}{ab}
- \Delta\mathbf{v}=(R_x(a)R_y(b)-R_y(b)R_x(a))\mathbf{v}
- \Delta\mathbf{v}=(R_y(a)R_z(b)-R_z(b)R_y(a))\mathbf{v}
- \Delta\mathbf{v}=(R_z(a)R_x(b)-R_x(b)R_z(a))\mathbf{v}
- \frac{\Delta\mathbf{v}}{ab}\longrightarrow J_z\mathbf{v}
- \frac{\Delta\mathbf{v}}{ab}\longrightarrow J_x\mathbf{v}
- \frac{\Delta\mathbf{v}}{ab}\longrightarrow J_y\mathbf{v}
- J_z\mathbf{v}
- J_x\mathbf{v}
- J_y\mathbf{v}
- [J_x,J_y]=J_z
- [J_y,J_z]=J_x
- [J_z,J_x]=J_y
- \mathfrak{so}(3)=\mathrm{span}\{J_x,J_y,J_z\}
- [A,B]=AB-BA
- \mathbf{v}
- Target angles

### Source

Commutators and Lie Algebra. Visual continuation of Reel 15, now Reel 16 in the complete review series.

### Visual check

Compare two orders of actual rotation matrices. Shrink the angles and divide the vector difference by their product. It approaches the third generator's action. Repeat for all three cyclic pairs. The magnification is explicitly labeled and the finite-angle difference is not presented as an exact third-axis rotation.

---

## Reel 17
### Title

Building a Casimir operator

### Caption
Just as symmetry transformations preserve an invariant expression built from the state, they also preserve an invariant operator built from the symmetry's generators. A **Casimir operator** is built from generators and commutes with every generator. Within an irreducible representation, it rescales every vector by the same amount. In direct analogy to the way the squared length of a vector is invariant under rotations, the sum of squared rotation generators has an invariant scaling action:

C = −(Jₓ² + Jᵧ² + J_z²).

The animation follows this construction in the ordinary three-dimensional vector representation. Here v is a vector on which rotation matrices act, and Jₓ, Jᵧ, and J_z generate infinitesimal rotations about the three coordinate axes. Squaring a generator means applying it twice.

In this representation, −Jₓ² removes the x component of v and retains its y and z components. The other two terms do the corresponding operations for their own axes:

−Jₓ²v = (0, vᵧ, v_z),
−Jᵧ²v = (vₓ, 0, v_z),
−J_z²v = (vₓ, vᵧ, 0).

The three colored arrows show these output vectors. Bringing them tip to tail adds the contributions. Every component of v appears twice, so their sum is exactly 2v.

As v turns, the individual contributions change. Their sum continues to point along v with twice its length. The operator therefore acts as multiplication by 2 throughout this representation, C = 2I. This also makes its commutation with rotations visible: rotating v preserves the relation Cv = 2v.

The value 2 belongs to this particular representation. In other irreducible representations, Casimir operators can take different fixed values. Their scale factors, or eigenvalues, help label the irreps. For massive particles, mass and spin label irreps of spacetime symmetry. The same construction extends beyond rotations. A Casimir built from spacetime translation generators, for example, determines invariant mass.

### On-screen text

- Three generators, one invariant
- Add the three contributions
- Turn the vector
- C=-(J_x^2+J_y^2+J_z^2)
- -J_x^2\mathbf{v}
- -J_y^2\mathbf{v}
- -J_z^2\mathbf{v}
- x\to0
- y\to0
- z\to0
- x
- y
- z
- Input
- Sum
- \mathbf{v}
- 2\mathbf{v}
- C\mathbf{v}=2\mathbf{v}
- C=2I
- Ordinary 3D vector representation

### Source

Invariants and Casimir operators. New visual construction in the ordinary three-dimensional vector representation, with C = −(Jₓ² + Jᵧ² + J_z²). Reel 17 in the complete review series.

### Visual check

Apply the three squared-generator terms on fixed axes, bring their output arrows tip to tail, then turn the input while recomputing every contribution. Their sum remains 2v.

---

## Reel 18
### Title

Translations cannot be represented by position coordinates alone

### Caption

We have discussed rotations, both circular and hyperbolic. Our other type of spacetime symmetry is translation. Translation is, to the eye, the simplest possible symmetry, and, if we can represent rotation in a plane, it  be natural to think we can represent translation in one dimension by sliding a number line. But there is a problem.

If an operation moves x by some amount a, then 0 is moved to a. A linear transformation must leave the zero vector fixed. This is a special case of the rule for **linearity**. A linear operation must preserve addition and multiplication by numbers. Adding two vectors and then transforming must give the same result as transforming each vector and then adding.

For translation of points, the candidate operation is Tₐ(x) = x + a. Compare the two orders in the animation. First add 2 and 3 to get 5, then translate by 10 to get 15. In the other order, translate each number first. The 2 becomes 12 and the 3 becomes 13. Adding them gives 25.

T₁₀(2 + 3) = 15,
T₁₀(2) + T₁₀(3) = 25.

One procedure adds the displacement once, while the other adds it twice. In general,

Tₐ(x₁ + x₂) = x₁ + x₂ + a,
Tₐ(x₁) + Tₐ(x₂) = x₁ + x₂ + 2a.

These are not equal unless a = 0. Translation does act sensibly on a number line, but it is not a linear operation when acting on this space. We cannot obtain the representation we want by treating the point coordinate itself as the state vector.

This asks us to reconsider what should be transformed. Our triangle representation worked by putting information at vertices and permuting the stored values. We can do something similar on the number line. A **function** assigns a value to each input coordinate, and we can translate that whole assignment. On the space of functions, translation will preserve linear combinations.

### On-screen text

- The same inputs, two orders
- T_{10}(x)=x+10
- Add, then translate
- Translate, then add
- 2+3=5
- T_{10}(2+3)=15
- T_{10}(2)=12,\qquad T_{10}(3)=13
- 12+13=25
- T_{10}(2)+T_{10}(3)=25
- +10
- 2
- 3
- 5
- 12
- 13
- 15
- 25
- 0
- 10
- 20
- T_{10}(2+3)\ne T_{10}(2)+T_{10}(3)
- 15\ne25

### Source

Translations and Function Representation point-space failure and transition to function space. Uses the source animation's concrete 2 + 3, displacement 10 example. Says linear transformations fix zero, rather than implying every map on a vector space must do so.

- animations/symmetry-translation-point-linearity-failure.mp4

### Visual check

Perform 2+3 then +10, compared with 2+10 and 3+10 then addition. Show 15 versus 25.

---

## Reel 19
### Title

Function representations of translations

### Caption


Translational symmetry needs a "shape" to translate, just as D₃ symmetry needs a triangly thing. A translation moves that shape while preserving the relationships among its features. The "shape" is a function of a coordinate parameter. Functions provides a linear representation of translation. Instead of translating the point x, we translate a function by shifting its argument:

(Tₐf)(x) = f(x − a).

Now the state is the whole function f, and Tₐ is an operator on the vector space of functions. An **operator** plays the role of a matrix. We can think of a function as an **infinite-dimensional vector**, with input coordinates labeling the components and function values giving the component values. This arrangement is analogous to our three-dimensional representation of D₃. There a vertex contained a component value, here an input coordinate does.

Linearity works because function addition is pointwise. At each x, the value of f + g is f(x) + g(x). Translating this sum gives

Tₐ(f + g)(x) = (f + g)(x − a)
= f(x − a) + g(x − a).

That is what we obtain by translating f and g separately and then adding them. The animation performs both procedures. In the upper panel, the functions are added before the result moves. In the lower panel, they move before being added. Both give the same final curve.

Multiplying a function by a number also commutes with translation. Shifting 3f gives the same result as shifting f and multiplying every resulting value by 3. The zero function remains the zero function, since its value is zero wherever we sample it. Translation therefore preserves all linear combinations.

### On-screen text

- The same functions, two orders
- (T_af)(x)=f(x-a),\qquad a=1.35
- Add, then translate
- Translate, then add
- f
- g
- f+g
- T_a(f+g)
- T_af
- T_ag
- T_af+T_ag
- x
- +a
- T_a(f+g)=T_af+T_ag

### Source

Translations and Function Representation function-space paragraphs and D3 analogy. Clarifies an operator's matrix role without claiming every operator can be written as an ordinary finite matrix. The sign convention matches Tₐf(x) = f(x − a).

- animations/symmetry-translation-function-linearity.mp4

### Visual check

Actually add then translate in one pane and translate then add in the other.

---

## Reel 20 [remove]
### Title

Translation preserves a function’s shape

### Caption

Translational symmetry needs a "shape" to translate, just as D₃ symmetry needs a triangly thing. A translation moves that shape while preserving the relationships among its features. The "shape" is a function of a coordinate parameter.

The rule is (Tₐf)(x) = f(x − a). Every peak, dip, and zero crossing moves by the same amount a. A feature that was at x₀ appears at x₀ + a because the new function there has value f(x₀ + a − a) = f(x₀). Its height is unchanged, and the spacing between any two features is unchanged.

The animation compares this with a motion that also deforms the function. The faint earlier curves let us compare the shapes at different locations. In the translation-only case, sliding the old curve into the new position makes them coincide. In the other case, the moving curve also changes shape, so one common displacement no longer brings the curves into agreement.


### On-screen text

- The same starting shape
- (T_af)(x)=f(x-a)
- Translation
- Translation + deformation
- Shape preserved
- Shape distorted
- Same values, new position
- New position and new shape
- x
- +a

### Source

Translations and Function Representation shape and dynamics distinction, followed by Generator of Translations. The original source's 'triangly thing' is retained with 'transform' replacing its evident 'translate' slip. Distinguishes the defined group action from a symmetry of a physical law.

- animations/symmetry-function-translation-shape.mp4

### Visual check

Full translation-only versus translation-plus-deformation comparison, with ghosts.

---

## Reel 21
### Title

The derivative of a function generates translation

### Caption

We have a function representation. Now we want to find an infinitesimal generator that acts on functions to produce a translation. We can do so by considering what happens to a function’s value under tiny displacements.

The new value f(x − a) is close to the old value f(x), and the correction is given, in the infinitesimal limit, by the slope at x. This is the same idea that a smooth curve appears straight when we zoom in sufficiently. The tangent line supplies the first approximation to the shifted value.

f(x − a) = f(x) − a f′(x) + O(a²).

This is the **first-order Taylor expansion**. The symbol f′ means the derivative, and O(a²) collects corrections of second order and higher in the displacement. As a approaches zero, these corrections become smaller relative to the first-order change. The animation compares the curve and tangent while magnifying the region between x and x − a.

A positive a moves the whole graph to the right. At the fixed coordinate x, the translated function takes its value from x − a. If the function slopes upward there, this earlier value is lower. That gives the minus sign in the first-order change.

The derivative operation therefore generates translation, with the sign fixed by our chosen direction. In the notation we will use for waves,

K = −i d/dx,
Tₐ = exp(−iaK).

Here i is the **imaginary unit**, defined by i² = −1. The exponent −iaK equals −a d/dx, so the finite action remains (Tₐf)(x) = f(x − a).

For rotation, the generator gave a tangent vector at each state. Here it gives the change in the function’s values as its graph shifts. Exponentiating the generator assembles those infinitesimal changes into a finite translation. We have again recovered a finite transformation from a local differential rule.

### On-screen text

- A small shift follows the tangent
- f(x-a)=f(x)-a f'(x)+O(a^2)
- ×[magnification]
- a = 0.035
- x − a
- x
- −a
- \hat K=-i\frac{d}{dx}
- T_a=e^{-ia\hat K}

### Source

Generator of Translations and its tangent-zoom animation. Defines O(a²), derivative notation, and i when first needed here. Verified −ia(−i d/dx) = −a d/dx, consistent with the manuscript's translation convention.

- animations/symmetry-translation-tangent-zoom.mp4

### Visual check

Zoom from smooth curve to local tangent, x and x-a marked, signs consistent.

---

## Reel 22
### Title

Finding an eigenbasis

### Caption

Imagine a rubber sheet. We pull on its corners. What does this do to the x- and y-axes? It rotates their images toward each other while stretching them. Now instead choose diagonal axes aligned with the stretch. The long axis is stretched but not rotated and the short axis is compressed but not rotated.

The action on these directions is now simple scalar multiplication of the original vector. ‘**Scalar**’ here means a single number. An arrow may grow or shrink, but its transformed version still lies along the same line.

The animation shows the same deformation with two choices of basis. A **basis** is a set of independent vectors from which every vector in the space can be built by addition and scaling. In the ordinary x,y basis, the transformed basis vectors point in new directions, so each needs components along both original axes. The transformation mixes those components.

In the diagonal basis, each basis vector changes only by an overall factor. If s is the factor stretching the long direction, the short direction is scaled by 1/s. These reciprocal factors preserve the area in this example. Finding the special directions makes the transformation easier to describe.

Now for a bunch of terminology. These natural basis vectors are the **eigenvectors**. The values by which a transformation scales them are the **eigenvalues**, and the basis they form is called an **eigenbasis**. Since the transformation matrix is diagonal in this basis, the procedure for finding it is called **diagonalization**.

Choosing the basis does not change the deformation of the sheet. It changes how we describe that deformation. Once the basis vectors no longer mix, any other vector, which is a linear combination of them, transforms by having its components scaled independently. We can therefore understand an arbitrary vector’s transformation by separating it into these simpler parts.

### On-screen text

- Ordinary basis
- Eigenbasis
- a=\frac{s+s^{-1}}{2},\qquad b=\frac{s-s^{-1}}{2}
- s = [value]
- x
- y
- u
- v
- x′
- y′
- s u
- s⁻¹ v
- x'=ax+by,\qquad y'=bx+ay
- u'=su,\qquad v'=s^{-1}v

### Source

Primer — Eigenfunctions rubber-sheet example and terminology. Splits the source animation at the transition from transforming basis vectors to transforming an arbitrary vector. Defines basis and scalar without assuming the reader already knows them.

- animations/symmetry-eigenbasis-stretch.mp4

### Visual check

First act of source. Ordinary basis vectors mix, eigenbasis vectors only scale.

---

## Reel 23
### Title

A vector as a sum of eigencomponents

### Caption

Once the basis vectors no longer mix, any other vector, that is, any linear combination of the basis vectors, transforms by having its components scaled independently. We can see this by separating an arbitrary arrow into parts along the two diagonal directions of our stretched sheet.

Call the unit vectors in those directions eᵤ and eᵥ. A vector r with components u and v is

r = u eᵤ + v eᵥ.

The animation places the two component arrows tip to tail. Their sum is the original arrow. The transformation stretches eᵤ by a factor s and compresses eᵥ by 1/s. Because the transformation is linear, we can transform the two component arrows separately and add the results:

r′ = su eᵤ + (v/s)eᵥ.

The transformed components recombine into the same final arrow we would obtain by applying the transformation directly to r. Nothing has been lost by resolving it into the special directions. Each component simply receives the scale factor associated with its own eigenvector.

In this basis, the matrix is diagonal, with rows [s, 0] and [0, 1/s]. The zeros say that the u component contributes nothing to the new v component, and the v component contributes nothing to the new u component. In the ordinary x,y basis, both new components depend on both old ones.

This is the usefulness of an eigenbasis. A transformation that mixes the original coordinates becomes a set of independent scalings. When our vectors are functions, we call the corresponding special vectors **eigenfunctions**. The same question then applies to the derivative operator that generates translation. Which functions does it return unchanged except for multiplication by a number? Solving that problem will take us directly to exponentials, and then to complex exponentials, which we will see are waves. In quantum theory, linear combinations of waves are, poetically enough, representations of the states of systems in spacetime.

### On-screen text

- Resolve the vector into its components
- Scale each component independently
- \mathbf{r}_{\mathrm{in}}=u\hat{\mathbf{u}}+v\hat{\mathbf{v}}
- s
- u
- v
- u component
- v component
- Result
- \mathbf{r}_{\mathrm{in}}
- \mathbf{r}
- \mathbf{r}=su\hat{\mathbf{u}}+s^{-1}v\hat{\mathbf{v}}
- \mathbf{r}=
- s
- s^{-1}
- 0

### Source

Primer — Eigenfunctions arbitrary-vector table and terminology. Uses eᵤ/eᵥ to distinguish basis vectors from scalar components in plain Unicode. Keeps the same reciprocal stretches and diagonal matrix as the source.

- animations/symmetry-eigenbasis-stretch.mp4

### Visual check

Second act of source. Decompose arbitrary vector tip to tail, scale components, recombine, display diagonal matrix.

---

## Reel 24
### Title

Translation eigenfunctions are exponentials

### Caption

Since a function is an infinite-dimensional vector, and the generator d/dx plays the role of a matrix, we can solve an eigenvalue equation here too. It now takes the form of a differential equation:

df/dx = λf.

We are looking for a function whose derivative returns the same function, scaled by a single number. The solution is f(x) = Ce^(λx), since differentiating gives Cλe^(λx). Here C is a constant and λ is the eigenvalue of d/dx.

A finite translation also returns a multiple of the same function:

f(x − a) = e^(−λa)f(x).

The multiplier differs from the derivative’s eigenvalue, but the eigenfunction is the same. One fixed multiplier relates the translated and original curves at every position x.

We now have a potential way to represent a state using exponential functions. There is an additional condition when symmetry must preserve the relationship between states. Their **overlap**, the function-space counterpart of the dot product, must remain unchanged. This property is known as **unitarity**. It preserves the lengths and relative relationships of the state vectors.

For a translation eigenfunction, the multiplying factor must then have magnitude one. Real nonzero λ makes e^(−λa) grow or shrink. Choosing λ = ik, with real k, instead gives e^(−ika), which has magnitude one. The eigenfunction becomes Ce^(ikx), with eigenvalue k for K = −i d/dx. Translation changes its **phase**, the angle of its complex value, without changing its magnitude.

A sum of these waves translates by changing the component phases while preserving their magnitudes. When translation is a symmetry of the dynamics, its distribution over generator eigenvalues is conserved. This is the structure behind momentum and energy conservation. Momentum will be associated with wave number, and energy with frequency. First, we need to see why a complex exponential describes a wave.

### On-screen text

- Blue is the exponential. Gold is its derivative.
- Halve every height of a copy. Watch it meet the gold derivative.
- The scaled copy matches the derivative at every x.
- Now slide a copy to the right. Its shape stays the same.
- Keep the translated curve in place.
- Scale a fresh copy of the original vertically.
- It matches the translated curve at every x. A shift is also a rescaling.
- \frac{df}{dx}=\lambda f,\qquad f(x)=e^{\lambda x}
- λ = 0.50
- f
- f'=\lambda f
- f(x-a)=e^{-\lambda a}f(x)
- x

### Source

Eigenfunctions of Translational Symmetry and Unitarity. Preserves the conservation-law motivation while reserving measurement and Fourier developments. Distinguishes derivative eigenvalue λ from finite-translation multiplier and sets λ = ik only after imposing the unit-modulus condition. Real exponentials serve as formal eigenfunction illustrations, not normalized full-line states.

Additional animation of the manuscript’s equations.

### Visual check

Derivative and finite translation act on exponential by a scalar factor.

---

## Reel 24a
### Title

Translation of complex exponentials preserves the inner product

### Caption

We now have a potential way to represent a state using exponential functions. We also want symmetry transformations to preserve the relationship between states, expressed by their **inner product**. This property is called **unitarity**.

Take two multiples of the same exponential, with coefficients c₁ and c₂. In this one-dimensional space of functions, their inner product is c₁* c₂, where the star means complex conjugation, used here to extend the dot product to complex values. The magnified cross-section shows these coefficients as the function values at x = 0.

When we translate the real exponentials to the left, both coefficients grow. Their product grows too. Translation multiplies them by a factor whose magnitude changes.

Now translate two complex exponentials. Their values turn in the complex plane, but their magnitudes and relative angle stay the same. The common phase cancels in c₁* c₂, leaving the inner product unchanged throughout the translation. We can see this relationship visually. The relative structure of the complex exponential "spirals" stays the same.

This gives us a reason to choose complex exponentials. They represent translations by turning amplitudes without stretching them. We've looked ahead here a bit. Why complex exponentials look like spirals whose projections are sinusoidal functions is what we will explain next. 

### On-screen text

- Two copies of one exponential. Translate them together.
- Real exponential factors stretch both amplitudes.
- Their inner product changes with the translation.
- Now translate the two complex exponentials.
- Their lengths and relative angle stay the same.
- Their inner product is unchanged. This is unitarity.

- REAL EXPONENTIALS
- f(x)=c_1e^{\lambda x},\qquad g(x)=c_2e^{\lambda x}
- At x = 0
- c_1^*c_2=
- COMPLEX EXPONENTIALS
- f(x)=c_1e^{ikx},\qquad g(x)=c_2e^{ikx}
- Inner product of the amplitudes
- \langle Tf,Tg\rangle=\langle f,g\rangle
- x

### Source

Unitarity bridge between translation eigenfunctions and the complex-exponential primer. Temporary insertion after Reel 24, without renumbering the existing reels.

The animation compares the action of translation within a single exponential mode. The displayed inner product is that of its coefficients, not an integral over the cropped plotting window. The real exponentials are formal modes, not normalizable functions on the whole line. Translations of ordinary real wave packets also preserve their inner product.

The complex example uses k = 2π/3. A leftward shift of three units therefore makes one full turn. The inner product stays fixed at every intermediate displacement as well.

- [Animation preview](../../../content/reels/symmetry-series-v2/translation-unitarity/index.html)
- [Generator](../../../scripts/symmetry_reels_v2/translation_unitarity.py)

### Visual check

Two copies of one real exponential translate left, then two copies of one complex exponential. Enlarged cross-sections show the coefficients at x = 0. The real coefficient inner product grows, while the complex coefficient inner product stays fixed. One pass over 32 seconds with timed narration and a final hold.

---

## Reel 25
### Title

The complex plane

### Caption

Complex valued functions are not directly a part of our exposition about symmetry, but they are so pervasive as the solutions to the differential equations entailed by translation symmetry that we really must gain some intuition abput them to continue. 

A **complex number** has two real-number degrees of freedom. We define z = x + iy, where x and y are real numbers and i² = −1. The number z therefore maps to a vector (x, y) in the **complex plane**. The horizontal axis records the **real part** x, and the vertical axis records the **imaginary part** y.

The diagram builds z from these two parts. An arrow along the real axis supplies x. An arrow along the imaginary direction supplies iy. Placing them tip to tail gives the resultant z, just as adding the two coordinate components of an ordinary vector gives the whole vector.

In the complex plane, both x and y are real coordinate values, and together they specify one complex number. One complex dimension therefore has the same number of real degrees of freedom as a two-dimensional real plane.

This answers a question raised by complex exponentials. How can a single number i play the role of the two-by-two matrix J that generated rotations? A complex number has enough components for the same geometry. Multiplication by i acts on them as

iz = i(x + iy) = −y + ix.

The corresponding real-vector operation sends (x, y) to (−y, x), exactly the action of J. Applying it twice gives −z, just as J² = −I reverses a real vector.

We have repackaged the rotation generator in complex notation. This makes it possible to describe a turn by complex multiplication, and an oscillating wave by a complex exponential. Before adding position and time, we can follow the action at one point and recover the circle from its tangent rule.

### On-screen text

- A sum in the complex plane
- z=x+iy
- Re
- Im
- x
- iy
- z
- Complex form
- Vector form
- z=x+iy\quad\longleftrightarrow\quad(x,y)

### Source

Primer — Complex exponentials and Wave Packets, complex-number definition and two-real-degrees-of-freedom argument. Expands the tip-to-tail source diagram and computes iz explicitly. The matrix/complex equivalence is the same one used by the manuscript.

- diagrams/symmetry-complex-plane-vector.png

### Visual check

Real x plus imaginary iy as tip-to-tail arrows, resultant z and explicit (x,y) correspondence.

---

## Reel 26
### Title

i generates rotations

### Caption

What action does multiplication by i have at the identity element 1? The point 1 = 1 + 0i lies on the positive real axis. Multiplying by i gives i = 0 + 1i, a perpendicular vector. Draw that vector at the tip of the original one and it gives the tangent to the unit circle.

This is exactly the action the J matrix generator had in two dimensions. More generally, if z = x + iy, then iz = −y + ix. The vector iz is perpendicular to z and has the same length. Anchored at the tip of z, it supplies the tangent to the circle through that point.

Since multiplication by i produces the tangent vector at every point, and the tangent vector is the geometric version of the derivative, we have

dz/dθ = iz(θ).

With z(0) = 1, solving this differential equation gives z(θ) = e^(iθ). The parameter θ is the angle. At each point along the circle, the derivative supplies the direction and rate of change needed to continue the turn. The multiplication by i gives the tangent rule, while exponentiating it gives the finite rotation.

Halfway around the unit circle, θ = π, yielding **Euler's identity**:

e^(iπ) = −1. 

Our discussion of symmetry has led us directly to an otherwise mysterious identity relating four of math’s iconic constants: e, i, π, and 1. 
 
Mapping z back to its real and imaginary coordinates gives **Euler’s formula**,

e^(iθ) = cos θ + i sin θ.

The real coordinate oscillates as cosine and the imaginary coordinate as sine. Their combination has length one throughout the turn, because cos²θ + sin²θ = 1. Multiplying by an **amplitude** A gives a circle of radius A.

Engineers often represent real sinusoidal waves with complex exponentials and read off the real part, since exponentials simplify the algebra. We now have the geometry behind that practice. Letting the angle vary with position and time will turn this circular motion into a travelling complex wave.

### On-screen text

- At the identity
- At every point on the circle
- z=1,\qquad iz=i
- z=e^{i\theta},\qquad iz=ie^{i\theta}
- Re
- Im
- 1
- i
- z
- iz
- |z|=|iz|=1
- \frac{dz}{d\theta}=iz(\theta)

### Source

Primer — Complex exponentials and Wave Packets, identity tangent through Euler formula and engineering note. Distinguishes the quarter-turn linear map z ↦ iz from the infinitesimal evolution dz/dθ = iz and finite exponential. The tangent is explicitly anchored at the state's tip.

- diagrams/symmetry-complex-unit-tangent.png

### Visual check

Identity 1, unit tangent i anchored at the tip, then generalize to z and iz during rotation.

---

## Reel 27
### Title

A travelling wave as a complex exponential

### Caption

Now let us turn from circular motion to a travelling complex wave. Let the **phase**, the angle of the complex value in the complex plane, vary with position x and time t:

θ(x,t) = kx − ωt,
z(x,t) = Ae^(i(kx − ωt)).

Here A is the wave’s **amplitude**, λ is its **wavelength**, k = 2π/λ is its **wave number**, and ω sets how quickly the phase changes with time. Increasing x by one wavelength increases that angle by 2π, one complete turn.

In the animation, position runs along the helix. The other two directions show the real and imaginary parts of the complex value at each position. As time advances, these values rotate and the wave pattern travels along x. The highlighted coordinate stays fixed while its complex value turns in the accompanying circle.

The helix is a picture of a complex-valued function. Its transverse directions record two components of the value at each x. The synchronized curves show those components separately:

Re z = A cos(kx − ωt),
Im z = A sin(kx − ωt).

Their values oscillate, while the length of the complex value stays fixed at A. A crest of the real component occurs at a fixed phase. As t increases, x must increase to keep kx − ωt constant, so the pattern travels in the positive x direction for the positive k and ω shown.

Applying the translation operator Tₐ gives

(Tₐz)(x,t) = z(x − a,t) = e^(−ika)z(x,t).

The **phase factor** e^(−ika) is the eigenvalue of Tₐ and has magnitude one. It turns each complex value without stretching it, the phase-only scaling allowed by unitarity.

We arrived here by asking how to represent translation on functions, finding the derivative as its generator, and seeking functions that return as multiples of themselves. Requiring the symmetry to preserve overlap brought us to complex exponentials. The circular geometry of those exponentials now gives us waves.

### On-screen text

- A complex wave
- z(x,t)=e^{i(kx-\omega t)}
- Re z
- Im z
- \cos(kx-\omega t)
- \sin(kx-\omega t)
- Re
- Im
- x
- x_0=4
- |z|=1
- z(x-a,t)=e^{-ika}z(x,t)
- \lambda=\frac{2\pi}{k}

### Source

Final pre-Fourier paragraphs of Primer — Complex exponentials and Wave Packets. Preserves the phase, amplitude, wavelength, wave-number, helix, component, and translation-factor content. Clarifies that the helix axes depict function values, not a literal material trajectory. Ends before Fourier and quantum-measurement material.

- animations/symmetry-complex-plane-wave-v2.mp4

### Visual check

Helix, synchronized real/imaginary components, fixed x slice, rotating value, amplitude and wavelength bracket.
