# Symmetry to Waves — reel review

Offline first cut of the chapter before Fourier. The existing Waves to Quanta series is separate.

Edit each **Title** and **Caption** directly. The title is used in the video and in the posted caption. The preview and caption files are generated from this document, which the generator never overwrites.

The final caption adds the series and episode number, the title, the next reel’s current title, the full-chapter link, and the five tags below. All of these count toward the limit. The gallery shows the complete assembled caption and its count.

Shared footer

Full chapter: https://wadelamble.github.io/constrained-improvisation/symmetry/

#Physics #ScienceExplained #Symmetry #NaturalPhilosophy #Mathematics

The **On-screen text** lists below are review notes for the first cuts. Labels and equations are laid out inside the videos. If you change them, the video needs to be rendered again. Source notes are not posted.

The on-screen lists use stable ordered slots. Edit their wording in place; preserve the order and number of entries. Equation entries use raw TeX and are rendered as mathematics. Numerical labels below describe calculated readings and fixed symbols.

---

## Reel 01

### Title

The same game

### Caption

Strike a pool ball with a cue, and the balls move in an expected way. Move the table over a few feet, and the balls move in recognizably the same way. Wait a few minutes, and the balls move in the same way. Turn the pool table a few degrees, and the balls still move the same way. Put the pool table on a train at constant velocity, and, again, the balls move in the same way. These are the manifest “symmetries” of the world we live in — position and time translation, rotation, and velocity “boosts.”

The animation repeats the same collision under each transformation. The positions on the screen change, and a moving observer may describe different velocities, but the relation between the incoming and outgoing motion remains the same. This is what we mean by symmetries of physical behavior.

Our pool game illustrates the idea, but why should we start our story here? We will argue that symmetry constrains both the laws that govern physical evolution and the classification of the objects that undergo that evolution. The term “symmetry” in this context may not at first glance seem like the same concept as, say, a triangle’s symmetry, but it precisely is, as we will see.

We can also move the table a few feet to the right or the observer a few feet to the left. When discussing invariants, we often think in terms of what observers agree on. The task is to say mathematically what is preserved when we make these changes of perspective. We will start with the familiar world of discrete symmetries and build up the definitions we need from there.

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

### Numerical labels

Clock t and calculated elapsed times. The same equal-mass elastic-disk collision is transformed in both panels; ball radius and collision separation use the same spatial scale.

### Source

Symmetry — opening pool-table example; Invariants — active transformation and observer perspective.

The collision description makes explicit what 'the same way' means when coordinates or observed velocities change. It does not add a relativistic claim to the pool-table example.

---

## Reel 02

### Title

A triangle’s six symmetries

### Caption

We can see the obvious symmetry of an equilateral triangle. To categorize its symmetry, we can write down all the actions that leave it unchanged. We can do nothing, rotate 120°, rotate 240°, flip along an axis, flip then rotate 120°, and flip then rotate 240°. There are six actions, including the one in which we do nothing.

The animation carries the labeled vertices through these actions. A vertex may arrive where a different vertex began, but at the end the triangle overlays itself. Keeping track of the labels lets us distinguish actions that leave the same outline. A turn through 100° would leave the triangle pointing somewhere else and would not belong on this list.

We say the triangle belongs to the D₃ symmetry group. Any number of objects possess D₃ symmetry. The next scene puts the triangle beside three circles, three petals, and three rounded bars. The same rotation and flip return each outline to itself. The shapes differ, but the group actions are the same. We tend to think of a “triangle’s symmetry,” rather than the symmetry of two rotations and flips about three axes, but this latter way of thinking in terms of symmetry groups is more general.

This is the definition of symmetry used in physics, where we ask not “what symmetry does this or that object have?” but “what mathematical objects realize the actions of a symmetry group?” The group describes the actions and the way they compose, so we can recognize the same structure in different objects.

For example, suppose we label our triangle’s vertices A, B, C and ask, if we rotate twice, flip once, then rotate again, where is vertex A sent? But if we want to write this down mathematically, we need a way to represent each action and its effect on the labels.

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

### Numerical labels

Vertex labels A, B, C. Action selector e, r, r², s, rs, r²s. Intermediate rotation and reflection frames show the motion between discrete group actions. The second scene applies the same actions to the triangle and the three objects from the manuscript's D₃ diagram.

### Source

Discrete symmetries — triangle actions and diagrams/symmetry-d3-carriers.svg; Representations — labeled vertices and composed actions.

---

## Reel 03

### Title

Writing symmetry as matrices

### Caption

We can plainly see the symmetry of the triangle, but what if we want to write it down mathematically? Specifically, what if we want to write group actions in terms of how they transform labels on an object? Recognizing that the triangle’s state has three ordered components, we might guess that we could represent it as a vector with three components.

We can then represent 120° rotations as transformations that permute those components in accordance with the symmetry group actions. For our example, a single rotation gives

R(1, 3, 5) = (5, 1, 3).

A flip that keeps the first vertex in place exchanges the other two components. There is nothing special about the vertices here. We could just as easily have chosen the midpoints of the edges or any other triplet of points with the triangle’s symmetries, and the same matrix would permute those values.

A representation of a symmetry group is a vector space and a set of linear transformations that compose in the same way as the group actions.

D(g₁g₂) = D(g₁)D(g₂).

This says that the matrix for the composed action, g₂ followed by g₁, is the product of the matrices for the separate actions. D is the map from symmetry actions to matrices in the representation.

These permutations also have a geometric interpretation. Those that correspond to rotations of the triangle are 120° rotations about a diagonal axis in this vector space. Those that correspond to flips are reflections in planes that contain the diagonal axis. In the animation, the colored values are reassigned among the three component positions. This lets us follow each matrix’s action on the state (1, 3, 5).

### On-screen text

- Matrices act on component values
- Rotation
- Reflection
- Before
- After
- D(g_1g_2)=D(g_1)D(g_2)
- R^3=I
- S^2=I

### Numerical labels

R = [[0, 0, 1], [1, 0, 0], [0, 1, 0]]; S = [[1, 0, 0], [0, 0, 1], [0, 1, 0]]. The displayed state starts at (1, 3, 5), follows three cyclic permutations, then two reflections. Colors follow the values.

### Source

Representations — definition, matrices, and 3D permutation geometry.

The animation displays the two permutation matrices and follows their action on component values. “Reflections in planes” clarifies the source’s “flips about planes.”

---

## Reel 04

### Title

Separating the common part

### Caption

Now we can notice something about these transformations. The transformed versions of any vector lie in a plane, and all such planes are parallel to one another. If we subtract the average of a vector’s components from each component, we move the point where that plane intersects the axis of rotation to the origin and preserve the permutation structure of the transformations.

For our earlier vector, the average of the components is 3. We can separate it into a common part and a zero-sum part.

(1, 3, 5) = (3, 3, 3) + (−2, 0, 2).

The common part lies on the rotation axis and is unchanged by every permutation. The zero-sum part lies in a plane through the origin. Although written with three components, it needs only two independent numbers, since the third must make their sum zero. In the animation, subtracting the common part brings the permuted states into this plane.

A way to think of this is to allow the triangle’s vertices to store some information, like a number or any numerical quantity. If the value they store is the same for all vertices, the symmetry actions have no effect. If the values differ, the actions permute them in a way that can be represented in a two-dimensional vector space.

The three-dimensional representation space we began with is therefore decomposable into two subspaces, one one-dimensional and the other two-dimensional. Each stays within itself under every group action. Neither can be decomposed into smaller nonzero subspaces with this property. These are called irreducible representations, or irreps for short.

### On-screen text

- Common part and zero-sum part
- Common part
- Zero-sum part
- \mathbf{v}=\overline{v}(1,1,1)+\mathbf{w}
- w_1+w_2+w_3=0
- \mathbf{3}=\mathbf{1}\oplus\mathbf{2}

### Numerical labels

(1, 3, 5) = (3, 3, 3) + (−2, 0, 2). The component axes are x₁, x₂, x₃. The common part lies on the equal-components axis; the zero-sum part turns in its perpendicular plane.

### Source

Representations — common component, zero-sum plane, and irreducible decomposition.

The irreducibility sentence specifies smaller nonzero subspaces preserved by every group action. This is a minimal clarification of the manuscript's definition. The particle connection is reserved for the manuscript and is unnecessary for this series.

---

## Reel 05

### Title

What a symmetry preserves

### Caption

Once we have chosen a representation for a symmetry, we might well ask, how do we know our transformations preserve the symmetry? If we look at a triangle and rotate by 100°, we can see that it does not overlay itself. In a representation, we need mathematical expressions that say “this transformation left the triangle the same.” We call these the invariants of the transformation.

In our two-dimensional irrep of D₃, we can describe the action on an arbitrary vector using two expressions that a symmetry transformation cannot change.

r² = x² + y²

u = x³ − 3xy² = r³ cos(3θ).

The first is the squared length of the vector. The second records its orientation relative to the reference axes. Rotating by 120° adds 360° to the angle inside cos(3θ), so u returns to the same value. A flip across the x-axis changes θ to −θ and also leaves u unchanged.

The animation compares the vector before and after each allowed action. These two values agree at the endpoints. Intermediate positions during a turn are not themselves triangle symmetries, so the cubic expression varies until the turn is complete. Length alone would allow every rotation. The cubic expression carries the threefold structure that distinguishes the triangle’s symmetry from the continuous symmetry of a circle.

These exact invariants are not the important part. They are obscure without seeing the derivation, but what matters is that we can write an expression in terms of coordinates that must not change under the symmetry transformation. This gives the “sameness” of our picture a precise mathematical meaning. We can ask the same kind of question about the pool game. What is preserved when we translate, rotate, or change our state of motion?

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

### Numerical labels

Axes x and y; live θ in degrees; actual current values of r² and u. The reference values are 1.000 and +0.707. Cubic u varies during intermediate angles and returns at the allowed 120° endpoints.

### Source

Invariants — D₃ quadratic and cubic invariants; Symmetry — pool-table example.

The explanation fixes the reference reflection axis as the x-axis, consistent with u = r³ cos(3θ). The caption states necessary preservation rather than suggesting that two scalar values certify an unrestricted transformation. Invariants are compared at discrete-action endpoints. Interpolated motion between those endpoints is not a D3 symmetry.

---

## Reel 06

### Title

From discrete to continuous

### Caption

What rotations return a circle to itself? All of them! Similarly, all translations return a line to itself. The symmetries of space and time are continuous and can therefore be represented as transformations that depend on continuously varying parameters.

The animation lets the rotation angle and the translation distance vary smoothly. A marked point on the circle moves, but the circle returns to itself at every angle. A marked point on the line moves as the line is translated, but the line itself remains the same. As with the labels on our triangle, the marks let us follow an action whose effect on the unmarked object would otherwise be invisible.

For the triangle, the angles that return it to itself are separated by 120°. For the circle, there is no smallest nonzero angle on the list. If we can rotate by 1°, we can rotate by half a degree or a hundredth of a degree. The transformation depends on a parameter that we can vary by an arbitrarily small amount.

As we saw in the D₃ symmetry group, we can build any action from a combination of the elemental actions of rotations and flips about an axis. Now let us ask the question, what is the generator of a continuous transformation? Let’s say we want to rotate a circle by 10°. We could compose ten 1° rotations. But what if we want to rotate by 1°? We can see where this is going. The generators must be infinitesimal rotations.

This is where symmetry ideas meet calculus. We will take the derivative of a transformation with respect to its parameter and use that infinitesimal change to recover the finite transformation.

### On-screen text

- Continuously varying parameters
- Rotation
- Translation
- R(\theta)
- T(a)
- \theta\in\mathbb{R}
- a\in\mathbb{R}

### Numerical labels

The translation parameter a is displayed numerically as the marked line moves. The circle has a tracked radial direction.

### Source

Continuous symmetries; Infinitesimal Generators — composing progressively smaller rotations.

Marked points are described as tracking aids rather than additional features that the symmetry must preserve. Translation refers to the full mathematical line, even when the frame shows only a finite window.

---

## Reel 07

### Title

From a nudge to a rotation

### Caption

In the two-dimensional representation of rotations, we have a single variable, θ, that parameterizes the operator matrix R(θ). We can take the derivative of this matrix-valued function. To obtain a single matrix representing the infinitesimal nudge, we evaluate the derivative at θ = 0, where R(0) = I is the identity transformation.

This gives the infinitesimal generator

J = [[0, −1], [1, 0]].

Applied to a vector v = (x, y), J gives (−y, x). At the point (1, 0), it produces the tangent vector (0, 1). J acts on any point on the circle to produce the tangent vector at that point. Putting this into calculus notation,

dv/dθ = Jv.

We now have a differential equation for the transformation that uses the generator. We found this by starting with a known transformation and deducing its generator. But we can just as well go in the opposite direction. Given this differential equation, we can find the transformation.

v(θ) = exp(θJ)v(0).

The exponential of a matrix is defined in terms of the Taylor expansion for an exponential. Since J² = −I, its even powers alternate between I and −I, while its odd powers alternate between J and −J. Collecting them gives the familiar series for cosine and sine.

exp(θJ) = cos(θ)I + sin(θ)J = R(θ).

The animation follows the vector around its circle while J supplies the tangent direction at each point. This is an exponential map. It takes the infinitesimal generator J and returns the finite symmetry transformation R(θ). Exponential maps give what one would think is the familiar purely algebraic quality of exponentiation a rich geometric interpretation.

### On-screen text

- Infinitesimal rotation
- State
- Tangent
- \frac{d\mathbf{v}}{d\theta}=J\mathbf{v}
- J^2=-I
- e^{\theta J}=\cos\theta\,I+\sin\theta\,J
- R(\theta)=e^{\theta J}

### Numerical labels

J = [[0, −1], [1, 0]]. Vector labels v and Jv, and axes x and y. State and tangent arrows use the same scale.

### Source

Infinitesimal Generators — derivative at identity, tangent equation, and exponential map.

The nested lists record matrix rows in editable plain text. Render J as two stacked rows. The motion should follow the exact rotation, with the tangent indicating the derivative rather than a finite straight step.

---

## Reel 08

### Title

Seeing the whole symmetry flow

### Caption

We can think of a symmetry transform as a “uniform looking” vector field. Here we ask not what happens when the transformation is applied to a single set of starting conditions, but what the transformation does to all starting conditions. This view lends itself to seeing the structure in the evolution of a collection of nearby states.

For rotation, the generator J acts on any point to produce its tangent vector. At (x, y), that vector is (−y, x). Placing one of these arrows at each point gives the field in the animation. Each arrow tells us how the state at that position changes when we increase the angle by an infinitesimal amount.

The same equation governs every starting point.

dv/dθ = Jv.

As θ increases, the points follow circles centered at the origin. Points farther from the origin travel farther for the same change of angle, so their tangent arrows are longer. The origin stays fixed. These different arrows all express one rotation generator acting on different states.

We found the generator by starting with a known transformation, but we can go in the opposite direction. The finite transformation is

v(θ) = exp(θJ)v(0).

Applying it to a collection of starting points lets us watch the whole collection turn. A single trajectory shows where one state goes. Following nearby states together shows how the transformation acts across the space of states. The parameter in this picture is the rotation angle, so the motion on screen is the symmetry transformation unfolding as that angle changes.

### On-screen text

- The same generator at every state
- Vector field
- Flow
- J(x,y)=(-y,x)
- \frac{d\mathbf{v}}{d\theta}=J\mathbf{v}
- \mathbf{v}(\theta)=e^{\theta J}\mathbf{v}(0)

### Numerical labels

Axes x and y. The dots and marked quadrilateral undergo the same rotation; vector-field arrow lengths use one common display scale.

### Source

Symmetry Flows; Infinitesimal Generators — tangent vector and finite transformation.

This entry stays on the generator field and its flow. It does not introduce metrics. The caption identifies θ as the animation parameter so playback is not mistaken for a physical equation of motion.

---

## Reel 09

### Title

Rotation preserves lengths and angles

### Caption

What is the invariant of rotation in this representation? It is just the length of vectors and the angles between them. The two arrows turn together, so their directions change while their relationship does not. The length of one arrow's projection onto the other remains the same.

These relationships are expressed by a single invariant, the dot product. If u and v are vectors in the plane,

u · v = uₓvₓ + uᵧvᵧ = |u||v| cos θ.

Here θ is the angle between the arrows. Rotating both arrows changes their individual components, uₓ, uᵧ, vₓ, and vᵧ, but leaves the sum uₓvₓ + uᵧvᵧ unchanged. The coordinate values change together in just the way needed to preserve this quantity.

Taking the dot product of an arrow with itself gives its squared length, u · u = |u|². Taking the dot product of two different arrows tells us their angle once their lengths are known. We therefore have one mathematical relationship that accounts for both the lengths and the angle we see preserved in the animation.

An invariant of this sort, that fixes some notion of placing reliable rulers on the space, is a metric. For ordinary rotations, these relationships are intuitive. We are turning a pair of arrows without stretching them or moving them relative to each other. The representation expresses this familiar geometry in terms of component values that transform.

A symmetry may preserve a less intuitive metric. We will next keep the idea of an invariant relationship between coordinates, but change the expression that serves as our ruler. This leads to a different kind of rotation and a first glimpse of the geometry of spacetime.

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

Invariants and Metrics.

---

## Reel 10

### Title

Hyperbolic rotations preserve a different interval

### Caption

For an ordinary rotation, x² + y² stays fixed. If we instead define the invariant interval using a difference, t² − x², we have a hyperbolic rotation. Here we choose units in which the speed of light is 1, so time and position can appear on the same plot.

The point moves along a hyperbola rather than a circle. Its time and position coordinates change, and its distance from the origin grows according to our everyday notion of distance. Yet the difference between the squares of its coordinates stays fixed.

t′ = t cosh η + x sinh η
x′ = x cosh η + t sinh η
t′² − x′² = t² − x².

The parameter η plays a role similar to the angle in an ordinary rotation. The functions cosh and sinh are the hyperbolic counterparts of cosine and sine. Their identity cosh²η − sinh²η = 1 does the work that cos²θ + sin²θ = 1 did for the circle.

Watch both the moving point and the interval readout. The point changes its apparent distance from the origin while the interval stays the same. Increasing the magnitude of η carries it farther out along the hyperbola, toward the diagonal asymptotes. The animation shows a finite part of this motion. The hyperbola continues beyond the frame.

Such a hyperbolic metric, as we will see, encodes the asymptotic limit of light speed in relativistic spacetime. A change of inertial observer changes the time and position assigned to events while preserving their spacetime interval. Here we are introducing the geometry that makes that agreement possible. The next chapter will put its physical meaning to work.

### On-screen text

- Hyperbolic rotation
- (ct)^2-x^2=1\qquad(c=1)
- η = [value]
- ct
- x
- ct = −x
- ct = x
- (x, ct)
- ct = [value], x = [value]
- ct=\cosh\eta,\qquad x=\sinh\eta
- \cosh^2\eta-\sinh^2\eta=1

### Source

Invariants and Metrics.

States the c = 1 units convention explicitly. The drawn boost uses the positive-η convention in both equations.

---

## Reel 11

### Title

The order of rotations matters

### Caption

When there are multiple independent transformations, the order in which we apply them may produce different resultant states. In the three-dimensional rotation group, called SO(3), rotating about the x-axis and then the y-axis leaves an object in a different orientation than applying the same actions in the opposite order.

The two views begin with the same orientation and use the same two rotations. Only their order changes. Following the marked directions makes the difference visible. A featureless sphere would hide the orientation we need to compare.

For infinitesimal generators, this order-dependence is expressed by the commutator,

[X, Y] = XY − YX.

For three-dimensional rotations, the generators satisfy [Jₓ, Jᵧ] = J_z, with corresponding relations for the other two pairs of axes. The commutator gives another rotation generator. It records the leading difference between composing two small rotations in opposite orders.

For ordinary numbers, eᴬeᴮ = e⁽ᴬ⁺ᴮ⁾. This identity does not hold for noncommuting generators. Combining two rotations into one exponential requires correction terms, beginning with a term involving their commutator. We cannot simply add the two exponents and expect the same final orientation.

Taken together, the generators, their linear combinations, and their commutators form a Lie algebra. It captures the group's local structure, while some global features, such as wrapping around onto itself, require additional information. Every representation must preserve this commutator structure. This is why the relations between the generators matter just as much as the individual motions they produce.

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

Commutators; Lie Algebra.

The Casimir calculation has no dedicated animation in this first-cut series. It remains in the linked chapter rather than being compressed into an unrelated video.

---

## Reel 12

### Title

Translations act linearly on functions

### Caption

Translation is, to the eye, the simplest possible symmetry. It would be natural to think the ideal representation space for a translation is simply a one-dimensional vector space, where points move by sliding a number line. But there is a problem if we want this action to be linear.

Moving x by an amount a sends 0 to a, while a linear transformation must leave the zero vector fixed. More generally, a linear operation T must preserve addition and scaling. For a translation of points, Tₐ(x) = x + a, we have

Tₐ(x₁ + x₂) = x₁ + x₂ + a,
Tₐ(x₁) + Tₐ(x₂) = x₁ + x₂ + 2a.

These are not equal unless a = 0. Translation acts sensibly on a number line, but it is not a linear operation on the point coordinates themselves.

On the other hand, the space of functions on a number line does form a linear representation. Instead of translating the point x, we translate a function by shifting its argument,

(Tₐf)(x) = f(x − a).

Now the state is the whole function f. Function addition is pointwise, so translating a sum gives the same result as translating both functions and then adding them.

Tₐ(f + g) = Tₐf + Tₐg.

The zero function also remains the zero function. The animation first shows the mismatch for points, then the agreement for functions. A translation preserves each function's shape while moving its location. This describes how the function transforms. Whether a physical system described by that function behaves the same way after translation is a separate question about the dynamics.

### On-screen text

- Translating points
- Translating functions
- T_a(x)=x+a
- a = [value]
- T_a(2+3)=5+a
- T_a(2)+T_a(3)=5+2a
- T_a(u+v)\ne T_a(u)+T_a(v)\quad(a\ne0)
- T_a(f+g)=T_af+T_ag
- (f+g)(x-a)
- f(x-a)+g(x-a)
- (T_af)(x)=f(x-a),\qquad T_a0=0
- x

### Source

Translations and Function Representation.

---

## Reel 13

### Title

The derivative generates translation

### Caption

We have a function representation. Now we want to find an infinitesimal generator that acts on functions to produce a translation. We can do so by considering what happens to a function's value under tiny displacements.

For a small shift a, the new value f(x − a) is close to the old value f(x). The correction is given, to first order, by the slope at x. This is the same idea that any smooth curve appears straight when we zoom in sufficiently.

f(x − a) = f(x) − a f′(x) + O(a²).

The term O(a²) collects corrections of second order and higher in the shift. As a becomes smaller, the tangent-line estimate becomes more accurate. The animation lets us compare the actual function value with the value predicted by that local slope.

A positive a moves the whole graph to the right. At a fixed coordinate x, the translated function therefore takes its value from the earlier coordinate x − a. That is why the first-order correction has a minus sign.

The generator acting on functions is the derivative operation, with this sign fixed by our direction convention. In the notation we will use for waves,

K̂ = −i d/dx,
Tₐ = e^(−iaK̂),
(Tₐf)(x) = f(x − a).

The exponent −iaK̂ is therefore −a d/dx. This is the function-space counterpart of the rotation generator J. There, a tangent vector specified a small change in orientation. Here, the derivative specifies a small change in the function's values as its graph shifts. Exponentiating the generator assembles those infinitesimal changes into a finite translation.

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

Generator of Translations.

---

## Reel 14

### Title

Eigenvectors simplify a transformation

### Caption

Imagine a rubber sheet. We pull on its corners. What does this do to the x- and y-axes? It rotates their images toward each other while stretching them. Now instead choose diagonal axes aligned with the stretch. The long-axis component is stretched and the short-axis component is compressed, with neither of these directions rotated.

The action on these axes is simple scalar multiplication of the original vector. Once the basis vectors no longer mix, any other vector, which is a linear combination of them, transforms by having its components scaled independently.

Let u and v be the components in the diagonal directions, and let s be the factor by which the long-axis component is stretched. In this example,

u′ = su,
v′ = v/s.

The reciprocal factors keep the area fixed. In the ordinary x,y basis, each new component depends on both old components. In the diagonal basis, each depends only on its own earlier value. The animation shows the same deformation in both descriptions. Changing the basis simplifies our account of what happens.

Now for a bunch of terminology. These special basis vectors are the eigenvectors. The values by which a transformation scales them are the eigenvalues, and the basis they form is called an eigenbasis. Since the transformation matrix is diagonal in this basis, the procedure for finding it is called diagonalization.

When the vectors are functions, we call them eigenfunctions. The geometric idea carries over. We look for functions that the operator returns with only an overall scaling, without mixing them into other functions. That will be our next question for the derivative operator that generates translation.

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

Primer -- Eigenfunctions.

---

## Reel 15

### Title

Translation eigenfunctions are exponentials

### Caption

Since a function is an infinite-dimensional vector, and the generator d/dx is a way of writing an infinite-dimensional matrix, we can solve an eigenvalue equation here too. It now takes the form of a differential equation,

df/dx = λf.

We are looking for a function whose derivative returns the same function, scaled by a single number. The solution is f(x) = Ce^(λx), since differentiating this expression gives Cλe^(λx). The eigenvalue of d/dx is λ.

Translating an exponential also returns a multiple of the same function,

f(x − a) = e^(−λa)f(x).

The factor is different from the derivative's eigenvalue, but the eigenfunction is the same. The animation compares the original exponential with its translated version. One fixed multiplier relates them at every position x. The ratio does not depend on which point we inspect.

We now have a potential way to represent a state using exponential functions. There is an additional requirement when symmetry actions must preserve the overlap between states. This property is called unitarity. For a translation eigenfunction, the multiplying factor must then have magnitude one.

For a real nonzero λ, e^(−λa) stretches or shrinks the function. Choosing λ = ik instead gives a factor e^(−ika) of magnitude one. The function becomes a complex exponential, Ce^(ikx). Translating it changes its phase without changing its magnitude.

We will look into overlaps more fully in the wave series. For now, this gives us the route from a translation generator, through its eigenfunctions, to the complex exponentials that describe waves.

### On-screen text

- The derivative returns a multiple
- A shift returns a multiple
- \frac{df}{dx}=\lambda f,\qquad f(x)=e^{\lambda x}
- λ = [value]
- f
- f'=\lambda f
- f(x-a)=e^{-\lambda a}f(x)
- a = [value], exp(−λa) = [value]
- x

### Source

Eigenfunctions of Translational Symmetry; Unitarity.

Keeps derivative eigenvalue λ distinct from finite-translation eigenvalue e^(−λa). The real exponential is a formal eigenfunction illustration, not a normalized state on the full real line.

---

## Reel 16

### Title

A complex exponential is a travelling wave

### Caption

A single-parameter complex exponential, e^(iθ), describes a circle. It is a way to repackage the rotation operator we have already seen. Multiplication by i supplies the tangent direction in the complex plane, just as the matrix J did in the two-dimensional real representation.

i² = −1 corresponds to J² = −I.

A complex number z = x + iy has two real-number degrees of freedom. Euler's formula makes the connection to rotation explicit,

e^(iθ) = cos θ + i sin θ.

Now let us turn from circular motion to a travelling complex wave. Let the phase vary with position x and time t,

θ(x,t) = kx − ωt,
z(x,t) = Ae^(i(kx − ωt)).

Here A is the amplitude, k = 2π/λ is the wave number, λ is the wavelength, and ω sets how quickly the phase changes with time.

In the animation, position runs along the helix. The other two directions show the real and imaginary parts of the complex value at each position. As time advances, these values rotate and the wave pattern travels along x. The highlighted coordinate stays fixed while its complex value turns in the accompanying circle.

The two components are A cos θ and A sin θ. Their values oscillate, while the length of the complex value stays fixed at A. Translating this wave multiplies it by a phase factor, z(x − a,t) = e^(−ika)z(x,t). The multiplier has magnitude one, so it turns each value without stretching it.

We have arrived at waves by asking how to represent translation while preserving overlap. The existing Waves to Quanta series takes up the story from here, exploring wave packets, Fourier duality, and the connection to quantum mechanics.

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

### Source

Primer - Complex exponentials and Wave Packets.

---
