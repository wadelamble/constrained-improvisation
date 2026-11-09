# Symmetry
Strike a pool ball with a cue, and the balls move in an expected way. Move the table over a few feet, and the balls move in recognizably the same way. Wait a few minutes, and the balls move in the same way. Turn the pool table a few degrees, and the balls still move the same way. Put the pool table on a train at constant velocity, and, again, the balls move in the same way. These are the manifest "symmetries" of the world we live in -- position and time translation, rotation, and velocity "boosts."

![The same pool-ball collision under position and time translations, rotation, and a velocity boost](animations/symmetry-pool-table-poster.png)

[Open MP4: symmetry-pool-table.mp4](animations/symmetry-pool-table.mp4)

*Symmetry transforms don't change how pool balls behave*

These changes in the orientation or location of the pool table are equally well expressed as changes in the orientation or location of the observer. As such, we can call them changes to the **reference frame**.  The sense in which the behavior of our pool balls is the same in different reference frames is intuitively obvious, but going forward, we will work with a more specific definition. While observers in different frames record different coordinates for balls' paths, they agree on the **equations of motion** that predict those paths. Thus when we say a change of reference is a symmetry, we specifically mean that the equations of motion are preserved under such a change. 

In addition to these symmetries of **evolution**, we will show that there are symmetries of the instantaneous **state** of a system whose structure must be preserved through the system's evolution if that evolution is to be information-preserving. We will see that this structure is then reflected in the equations of motion.

Our pool game illustrates what we mean by symmetries of physical behavior, but why should we start our story here? We will argue that symmetry constrains both the laws that govern physical evolution and the classification of the objects that undergo that evolution. The term "symmetry" in this context may not at first glance seem like the same concept as, say, a triangle's symmetry, but it precisely is, as we will see.

We will start with the familiar world of these "discrete symmetries" and build up the definitions we need from there. Then we will turn to “continuous symmetries,” specifically rotations and translations, where we will encounter a new branch of math, Lie algebra, that joins symmetry ideas with calculus. We will discover that waves arise naturally as state objects when we represent translational symmetry, and this will lead us to a discussion of Fourier analysis and the symmetry that preserves the information contained in wave states. Finally, we will situate these ideas in the context of quantum mechanics. 

Let’s start, then, with the humble triangle.

## Discrete Symmetries
Consider a triangle:

![](diagrams/symmetry-triangle.svg)

*An equilateral triangle*

We can see its obvious symmetry. To categorize its symmetry we can write down all the actions that leave it unchanged:
1. Do nothing
2. Rotate 120°
3. Rotate 240°
4. Flip along an axis
5. Flip then rotate 120°
6. Flip then rotate 240°

![Triangle symmetry actions](animations/symmetry-triangle-actions-poster.png)

[Open MP4: symmetry-triangle-actions.mp4](animations/symmetry-triangle-actions.mp4)

*A triangle's symmetries*

We say the triangle "belongs to the $D_3$ symmetry **group**." Any number of objects possess $D_3$ symmetry.

![](diagrams/symmetry-d3-carriers.svg)

*$D_3$ is more general than triangles*

We tend to think of a "triangle's symmetry" not the "symmetry of two rotations and flips about 3 axes," but this latter way of thinking in terms of symmetry groups is more general and is the sense we use in physics, where we ask not "what symmetry does this or that object have?" but "what mathematical objects realize the actions of this symmetry group?"


### Representations
We can plainly "see" the symmetry of the triangle, but what if we want to write it down mathematically? Specifically, can we write group actions in terms of how they transform labels on an object? For example, suppose we label our triangle's vertices \(A, B, C\) and ask, if we rotate twice, flip once, then rotate again, where is vertex \(A\) sent? Recognizing that the triangle's state has three ordered components, we might guess that we could represent the triangle as a vector with 3 components. We could then represent 120° rotations as **transformations** of the labels that permute the vertices in accordance with the symmetry group actions. 

There is nothing special about the vertices here, we could just as easily have chosen the midpoints of the edges or any other triplet of points with the triangle's symmetries, and the same matrix that permutes the vertices would permute those vectors. That is, the group actions are represented by some set of **linear** transformations. A **representation** of a symmetry group is such a vector space and set of linear transformations that compose in the same way as the group actions:

$$
D(g_1g_2)=D(g_1)D(g_2),
$$

where $g_1$ and $g_2$ are group actions, such as a rotation and a flip, and $D(g_n)$ is the matrix representing the $g_n$ action, and $D$ itself is the map from symmetry actions to matrices in the representation. This says that the matrix for the composed action \($g_2$ followed by $g_1$\) is the product of the matrices for the separate actions.

To construct a 3-dimensional representation of $D_3$, we map the 3 vertices to components of a vector.

![](diagrams/symmetry-d3-vertices-to-vector.svg)

We can represent rotations and flips, respectively, with the following matrices:

Rotation:
$$
\begin{pmatrix}
0 & 0 & 1\\
1 & 0 & 0\\
0 & 1 & 0
\end{pmatrix}
$$

Flip:
$$
\begin{pmatrix}
1 & 0 & 0\\
0 & 0 & 1\\
0 & 1 & 0
\end{pmatrix}
$$

For example, a single rotation would be represented as

$$
\begin{pmatrix}
0 & 0 & 1\\
1 & 0 & 0\\
0 & 1 & 0
\end{pmatrix}
\begin{pmatrix}
1\\
3\\
5
\end{pmatrix}
=
\begin{pmatrix}
5\\
1\\
3
\end{pmatrix}.
$$

![Rotation and flip matrices move the component values between slots](animations/symmetry-d3-transformation-matrices-poster.png)

[Open MP4: symmetry-d3-transformation-matrices.mp4](animations/symmetry-d3-transformation-matrices.mp4)

*Three rotations or two flips return the vector to its starting state*

The matrices that provide a set of transformations from which all other symmetric transformations can be constructed are the symmetry's **generators**. For example, in the 3-dimensional representation of $D_3$, all operations can be constructed from one rotation matrix and 3 flip matrices, one for each axis. 

Visually, permutations that correspond to rotations of the triangle are 120-degree rotations about a diagonal axis in this vector space, while those that correspond to flips are flips about three planes that contain the diagonal axis.

![D3 rotations and flips with labeled component axes and a fixed equal-components axis](animations/symmetry-d3-rotations-vs-flips-poster.png)

[Open MP4: symmetry-d3-rotations-vs-flips.mp4](animations/symmetry-d3-rotations-vs-flips.mp4)

*$D_3$ in 3-dimensional representation*

Now, we might notice something about these visualizations. The transformation of any vector lies in a plane, and all such planes are parallel to one another. Thus, if we subtract the average of a vector's components from each component, that is, if we move the point where the plane intersects the axis of rotation to the origin, we preserve the permutation structure of the transformations. We thus see that the $D_3$ symmetry is just as well represented as 120-degree rotations in the subspace of a 2-dimensional plane.

For our earlier example vector, the average of the components is 3. We can decompose the vector into one vector whose components are all the average value and one whose components add to zero.

```math
\begin{pmatrix}1\\3\\5\end{pmatrix}
=
\begin{pmatrix}3\\3\\3\end{pmatrix}
+
\begin{pmatrix}-2\\0\\2\end{pmatrix}.
```

The common part lies on the rotation axis and is unchanged by every permutation. The zero-sum part lies in a plane through the origin. Although written with three components, it needs only two independent numbers since the third is constrained by the sum being zero.

![Subtracting the common component leaves the D3 representation in the zero-sum plane](animations/symmetry-d3-irrep-collapse-poster.png)

[Open MP4: symmetry-d3-irrep-collapse.mp4](animations/symmetry-d3-irrep-collapse.mp4)

*Reducing 3-dimensional representation to 2-dimensional*

We also notice that vectors that lie on the axis of rotation itself are left unchanged by the transformation. A way to think of this is to allow the triangle's vertices to store some information, like a number. If the value they store is the same for all vertices, the symmetry actions have no effect, whereas if they are different, the actions permute those values in a way that can be represented in a 2-dimensional vector space. The 3-dimensional representation space we began with is thus decomposable into 2 subspaces, one 1-dimensional, the other 2-dimensional. These cannot be decomposed further. That is, there is no lower-dimensional space such that an allowable transformation of any state remains in that space. The 1-dimensional and 2-dimensional representations are called **irreducible representations** or **irreps** for short. This is admittedly heavy math. Why do we bother? In the story we have to tell of quantum physics, where constituents of matter must abide the symmetry of the laws of evolution each type of **particle** such as electron or photon, corresponds to an irreducible representation of nature's symmetry. A particular state of the particle is encoded in an element in the corresponding irrep.


### Invariants
Once we have chosen a representation for a symmetry, we might well ask, how do we know our transformations preserve the symmetry? If we look at a triangle and rotate by 100 degrees we can "see" that doesn't preserve the symmetry. In a representation, we need some set of mathematical expressions that say "this transformation left the triangle the same." We call these the **invariants** of the transformation. 

In our 2-dimensional irrep of $D_3$, we only need to check how a transformation acts on a single vector. The question "does the triangle overlay itself" becomes "is an arbitrary vector rotated by 120 degrees or flipped along a given axis." And this has a precise answer. Given the coordinates of a vector a transformation cannot change these invariants:

```math
r^2=x^2+y^2
\qquad\text{(the squared length of the vector),}
```

```math
u=x^3-3xy^2=r^3\cos(3\theta)
\qquad\text{(its orientation relative to reference).}
```

These invariants are a bit obscure without seeing the derivation, but what is important for our purposes is to appreciate that we can write an expression in terms of coordinates that must not change under the symmetry transformation. 

#### Invariants in Physics
The equations of motion of a system are, by definition, an invariant of the unified **spacetime** geometry in which systems evolve. That is, we defined these symmetries as those transformations under which the laws do not change. Generalizing the idea of a path of a single body to a **history** of a system, we can express what it means for to be a symmetry of the laws motion in a compact schematic equation. Here $\Phi$ is a history and $\mathcal E$ is the equations for motion:

```math
\mathcal E[\Phi]=0
\quad\Longrightarrow\quad
\mathcal E[g\Phi]=0
\qquad\text{for every }g\in G.
```

To make this concrete, let's work through a quick example. Let the equation of motion be $\ddot x+x=0$ and the history be $\Phi(t)=\cos t$:

```math
\mathcal E[\Phi](t)
=
\frac{d^2}{dt^2}\cos t+\cos t
=
-\cos t+\cos t
=
0.
```

Translate the history by a time $t_0$:

```math
(g\Phi)(t)=\Phi(t-t_0)=\cos(t-t_0).
```

Then

```math
\mathcal E[g\Phi](t)
=
\frac{d^2}{dt^2}\cos(t-t_0)+\cos(t-t_0)
=
-\cos(t-t_0)+\cos(t-t_0)
=
0.
```

But the equations of motion are not the only invariant of spacetime symmetry. As we would imagine, there are much simpler invariants, akin to distance between objects, that will define the allowable transformations of spacetime symmetry. 

Later, we will discuss the idea that varying a functional of possible paths an object could travel can be used to single out the physically valid path. In the context of complex systems or **fields** we generalize the idea of a path to a **history**. We can vary a functional of this history and find a stationary point, that is a history near which the functional changes only in higher powers of the variation. Such a history will satisfy the equations of motion. We might guess that since the equations of motion that describe the history are invariants of the symmetry, this functional would be also, and in fact, in the full symmetry of spacetime, apart from terms that do not affect which histories are stationary, this is the case. This functional is called the **action** and is itself a spacetime invariant. We might guess further that if the functional is an invariant, it is constructed by using the simple invariants, like those akin to distance between points. This is also generally the case. Thus we see a roadmap emerge provided by symmetry. Symmetry leads us to simple invariants, those invariants are arranged to construct an invariant functional, and finding the stationary points of that functional leads to equations of motion, which are themselves invariants of the symmetry.


#### Invariants and Groups
A group is defined by formal properties.

- **Closure**: combining actions stays within the group
- **Associativity**: regrouping a sequence without reordering it leaves the result unchanged
- **Identity**: there is a do-nothing action
- **Inverses**: every action can be undone

It is a deep mathematical truism that any group of actions that fulfill these properties is a "symmetry" in the intuitive sense that they preserve an invariant. Let the group act on its own elements by composition (written for the general case as multiplication). Now start with two elements $a,b$ and their "relative difference" $a^{-1}b$. Applying $g$ changes them to $ga,gb$, but leaves that relationship unchanged:

```math
\underbrace{(ga)^{-1}(gb)}_{\text{after}}
=a^{-1}g^{-1}gb
=\underbrace{a^{-1}b}_{\text{before}}.
```

We can see how this works for real numbers under addition: inverses are negatives, so the original difference is $-a+b=b-a$. Adding $g$ to both positions preserves it:

```math
\underbrace{(g+b)-(g+a)}_{\text{difference after}}
=\underbrace{b-a}_{\text{difference before}}.
```

The positions change, but their separation is invariant. Addition acts as a translation of the number line.

## Continuous Symmetries
What rotations return a circle to itself? All of them! Similarly, all translations return a line to itself. The symmetries of space and time are continuous and can therefore be represented as transformations that depend on continuously varying parameters. 

![Continuous rotation and translation symmetries](animations/symmetry-continuous-so2-translation-contact-sheet.png)

[Open MP4: symmetry-continuous-so2-translation.mp4](animations/symmetry-continuous-so2-translation.mp4)

*Continuous symmetries*

### Infinitesimal Generators
As we saw, in the $D_3$ symmetry group, we can build any action from a combination of the elemental actions of rotations and flips about an axis. Now let us ask the question, what is the generator of a continuous transformation? Let's say we want to rotate a circle by 10°. We could compose 10 1° rotations. But what if we want to rotate by 1°? We can see where this is going. The generators must be infinitesimal rotations. Noting that if we zoom in enough, any curved surface appears flat, we see that a continuous symmetry's infinitesimal generators are basis vectors in the tangent plane to the symmetry's action. 

![Curved surface with tangent plane and tangent vectors](diagrams/tangent-plane-curved-surface.png)

*Infinitesimal generators are vectors in the plane tangent to the space of symmetry transformations*

In the case of a circle, in the 2-dimensional representation, we have a single variable that parameterizes the operator matrix:

```math
R(\theta)
=
\begin{pmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{pmatrix}.
```

As every high school calculus student learns, a derivative of a function is the slope of the tangent line to that function. We can take the derivative of the matrix valued function of $\theta$. This is

```math
\frac{dR}{d\theta}
=
\begin{pmatrix}
-\sin\theta & -\cos\theta\\
\cos\theta & -\sin\theta
\end{pmatrix}.
```

To obtain a single matrix representing this infinitesimal nudge, we evaluate the derivative at $\theta=0$, where $R(0)=I$ is the identity transformation. In that case,

```math
\left.\frac{dR}{d\theta}\right|_{\theta=0}
=
\begin{pmatrix}
-\sin 0 & -\cos 0\\
\cos 0 & -\sin 0
\end{pmatrix}
=
\begin{pmatrix}
0 & -1\\
1 & 0
\end{pmatrix}.
```

This is the infinitesimal generator matrix:

```math
\hat J
=
\begin{pmatrix}
0 & -1\\
1 & 0
\end{pmatrix}.
```

Now apply this tangential nudge to a state vector

```math
\mathbf v(\theta)
=
\begin{pmatrix}
x(\theta)\\
y(\theta)
\end{pmatrix}.
```

![Circle with tangent vector at theta equals zero](diagrams/so2-tangent-at-identity.png)

*The generator matrix \(\hat J\) acts on the point \((1,0)\) to produce the tangent vector \((0,1)\) shown here.*

$\hat J$ acts on any point on the circle to produce the tangent vector at that point. Putting this into differential notation,

```math
\frac{d\mathbf v}{d\theta}
=
\hat J\mathbf v.
```

We now have a differential equation for the transformation that uses the generator. We found this by starting with a known transformation and deducing its generator. But we can just as well go in the opposite direction. Given this differential equation, we can find the transformation:

```math
\mathbf v(\theta)
=
e^{\theta \hat J}\mathbf v(0).
```

The exponential of a matrix is defined in terms of the Taylor expansion for an exponential:

```math
e^{\theta \hat J}
=
I
+
\theta \hat J
+
\frac{\theta^2}{2!}\hat J^2
+
\frac{\theta^3}{3!}\hat J^3
+
\cdots .
```

This is an **exponential map**. It takes the infinitesimal generator $\hat J$ and returns the finite symmetry transformation $R(\theta)$. Exponential maps give exponentiation, which one tends to think of as purely algebraic concept, a geometric meaning of connecting tangent vectors to symmetry transformations.

#### Flows under Symmetry Transformations

We can think of a symmetry transformation as a "uniform looking" vector field, as illustrated below:

![Rotation generator as a vector field](animations/symmetry-so2-vector-field-flow-contact-sheet.png)

[Open MP4: symmetry-so2-vector-field-flow.mp4](animations/symmetry-so2-vector-field-flow.mp4)

*Symmetry flows provide a rich picture of symmetry transformations*

Here we ask not what happens when the transformation is applied to a single set of starting conditions, but what the transformation does to all starting conditions. Such a constructions allows us to more easily see what is preserved by the symmetry.

#### Invariants and Metrics
What is the invariant of rotation in this representation? It is the length of vectors and the angles between them.

![Rotation preserves vector lengths and angles](animations/symmetry-rotation-vector-invariants-contact-sheet.png)

[Open MP4: symmetry-rotation-vector-invariants.mp4](animations/symmetry-rotation-vector-invariants.mp4)

*Metric structure*

These relationships are expressed by a single invariant, the dot product.

```math
\mathbf u\cdot\mathbf v
=
u_xv_x+u_yv_y.
```

An invariant of this sort, that fixes some notion of placing reliable rulers and protractors on the space, is a **metric**. For normal rotations and translations, these relationships are intuitive, but a symmetry may preserve a less intuitive metric. If we define invariant length not as \(x^2+y^2\) but as \(t^2-\mathbf{x}^2\), we have a "hyperbolic rotation." Separation between points stretches out to infinity as the rotation approaches its asymptotes, leaving the invariant interval unchanged even though the separation appears to grow using our everyday notion of distance. Such a hyperbolic metric, as we will see, encodes the asymptotic limit of light speed in the relativistic geometry **spacetime**.

![Hyperbolic rotation preserving the interval](animations/symmetry-hyperbolic-rotation-contact-sheet.png)

[Open MP4: symmetry-hyperbolic-rotation.mp4](animations/symmetry-hyperbolic-rotation.mp4)

*Hyperbolic rotations*

### Commutators
In the case of a single continuous symmetry transformation, the generator combined with a parameter, like angle in the case of rotation, specifies an arbitrary transformation. However, when there are multiple independent transformations that can be composed to form a closed, multi-dimensional group, the order of the composition may also need to be taken into account because it can produce different resultant states. For example, in the 3-dimensional rotation group, called $SO(3)$, rotating about the $x$-axis then the $y$-axis leaves a sphere in a different state than applying the same actions in the opposite order.

![Noncommuting 90-degree rotations in three dimensions](animations/symmetry-so3-rotation-order-contact-sheet.png)

[Open MP4: symmetry-so3-rotation-order.mp4](animations/symmetry-so3-rotation-order.mp4)

*Non-commuting operations of $SO_3$*

This order-dependence is expressed by the **commutator**:

```math
[\hat X,\hat Y]
=
\hat X\hat Y-\hat Y\hat X.
```

For example, for $\mathfrak{so}(3)$, the commutators are

```math
[\hat J_x,\hat J_y]=\hat J_z,
\qquad
[\hat J_y,\hat J_z]=\hat J_x,
\qquad
[\hat J_z,\hat J_x]=\hat J_y.
```

For small rotations about $x$ and $y$, the leading difference between the two orders points along the change generated by $\hat J_z$.

![Opposite rotation orders leave a mismatch that approaches the Jz tangent as the rotations shrink](animations/symmetry-commutator-sphere-poster.png)

[Open MP4: symmetry-commutator-sphere.mp4](animations/symmetry-commutator-sphere.mp4)

*Shrinking the rotations reveals $\hat J_z$ in the magnified mismatch*

We can see the commutator arise from a different angle. In $SO(3)$, we know that rotating about $x$ rotates the $y$ axis into $z$. We would write such a composite action as a product of exponential maps:

```math
e^{a\hat J_x}e^{b\hat J_y}.
```

We expect to be able to write a single exponential map for the combined action of $\hat J_x$ and $\hat J_y$. For ordinary numbers, and for commuting operators,

```math
e^Ae^B=e^{A+B}.
```

But this identity does *not* hold for noncommuting generators.

```math
e^{a\hat J_x+b\hat J_y}
```

generates a rotation about a single axis in the $x$-$y$ plane, which is not the same as performing the two rotations sequentially. We can correct the exponent so that the product can again be written as a single exponential. Keeping terms through second order in the small parameters $a$ and $b$,

```math
e^{a\hat J_x}e^{b\hat J_y}
=
\exp\!\left(
a\hat J_x+b\hat J_y+\frac12ab[\hat J_x,\hat J_y]+\cdots
\right)
=
\exp\!\left(
a\hat J_x+b\hat J_y+\frac12ab\hat J_z+\cdots
\right).
```

The commutator supplies $\hat J_z$.

Moving on the surface of a sphere provides another visual intuition for noncommutativity. On a flat plane, translations in two perpendicular directions commute. On a sphere of radius $R$, we can instead move along the surface by rotating about two perpendicular axes. Near the north pole, these motions act locally like translations in $x$ and $y$. Their generators are

```math
\hat T_x=\frac{\hat J_y}{R},\qquad \hat T_y=-\frac{\hat J_x}{R},
\qquad [\hat T_x,\hat T_y]=\frac{\hat J_z}{R^2}.
```

Here $\hat J_z$ generates rotation about the pole. The factor $1/R^2$ is the sphere's curvature. For fixed small travel distances, the residual rotation from moving, then undoing the movements in the same order, shrinks as the sphere flattens.

#### Lie Algebra

Taken together, the dimension of the symmetry group and the commutators specify a **Lie algebra** that contains the structure of the symmetry group, up to global topological features -- such as a symmetry group wrapping around onto itself such as a plane wrapped around a cylinder -- that are invisible to local structure. This algebra consists of the group generators, linear combinations of them, and their commutator. Every representation must preserve this commutator structure. Therefore, if we know the Lie algebra, we can use it to assess if a representation is valid.

#### Invariants and Casimir Operators

Just as symmetry transformations preserve an invariant expression built from the state, they also preserve an invariant operator built from the symmetry's generators. (A non-invariant operator would be the operator "rotate about the x-axis." If we rotate first around the y-axis, that changes the orientation of the x-axis, so the operator changes.) We can construct an invariant operator for a given irreducible representation by ensuring that it commutes with all the algebra's generators. The invariant operator rescales every vector by the same amount. In direct analogy to the invariant squared length of a vector, the invariant operator is the sum of squared rotation generators:

```math
\hat J^2=\hat J_x^2+\hat J_y^2+\hat J_z^2.
```

![Building a Casimir operator from rotation generators](animations/symmetry-casimir-operator-poster.png)

[Open MP4: symmetry-casimir-operator.mp4](animations/symmetry-casimir-operator.mp4)

*The SO(3) Casimir operator in a 3 dimension irrep has an eigenvalue of 2*

This animation shows that the action on any vector is to rescale it by a factor of 2. 

```math
\hat C=-\hat J^2=2I.
```

An eigenvalue is the amount by which an operator scales a vector. The Casimir eigenvalue for this representation is then 2. In other irreducible representations of SO(3), the Casimir operator can take different eigenvalues. A full set of Casimir eigenvalues label an irrep. 

In the theory we will build up to, "mass" and "spin" are examples of invariant operators derived from Casimir operators. The classification of particles (protons, electrons, etc.) is then mapped to associated labels of irreps of the full symmetry of physical evolution. We may say, if we like saying such things, "an electron is an irreducible representation of the symmetry of physical laws." Sick.

### Translations and Function Representation
Translation is, to the eye, the simplest possible symmetry. It would be natural to think the ideal representation space for a translation is simply a "sliding number line." But there is a problem. If an operation is to move $x$ by some amount $a$

```math
x\mapsto x+a,
```

then $0$ is moved to $a$, but the origin must remain fixed in a linear vector space. This is a special case of the rule for linearity. A linear operation $T$ must preserve linear combinations:

```math
T(\alpha u+\beta v)
=
\alpha T(u)+\beta T(v).
```

For translation of points on the number line, the candidate operator is

```math
T_a(x)=x+a.
```

But this does not preserve addition. For two points $x_1$ and $x_2$,

```math
T_a(x_1+x_2)
=
x_1+x_2+a,
```

while

```math
T_a(x_1)+T_a(x_2)
=
(x_1+a)+(x_2+a)
=
x_1+x_2+2a.
```

These are not equal unless $a=0$. Translation does act sensibly on a number line, but it is not a linear operation when acting on this space.

![Point translation failing linearity](animations/symmetry-translation-point-linearity-failure-contact-sheet.png)

[Open MP4: symmetry-translation-point-linearity-failure.mp4](animations/symmetry-translation-point-linearity-failure.mp4)

*Shifting a number line is not a linear operation*

On the other hand, the space of functions on a number line does form a linear representation. Instead of translating the point $x$, we translate a function by shifting its argument:

```math
(T_a f)(x)=f(x-a).
```

Now the state is the whole function $f$, and $T_a$ is an **operator** on the vector space of functions. An operator is a generalization of a matrix when applied to continuous functions. A continuous function is as an infinite-dimensional vector, in which its domain values are "axes," or component labels, and its range values are the component values. We can transform one function to another with an infinite dimensional matrix, but in practice, we can condense this into a well-known operation, such as the derivative operation. The derivative is a linear operator on the vector space of continuous functions.

Linearity works because function addition is pointwise:

```math
T_a(f+g)(x)
=
(f+g)(x-a)
=
f(x-a)+g(x-a)
=
(T_a f)(x)+(T_a g)(x).
```

So

```math
T_a(f+g)
=
T_a f+T_a g.
```

The zero function is also fixed:

```math
T_a0=0.
```

![Function translation preserving linearity](animations/symmetry-translation-function-linearity-contact-sheet.png)

[Open MP4: symmetry-translation-function-linearity.mp4](animations/symmetry-translation-function-linearity.mp4)

*A function representation is linear*

Indeed, this representation is completely analogous to our 3 dimensional representation of $D_3$. There a vertex contained a component value, here an input value does. Indeed, the $D_3$ representation is itself a function representation, with a domain of three points.

The invariant of the function representation of translation is simply the shape of the function. Preserving that shape preserves the distances between its features, measured along the domain. The familiar distance invariant is therefore still present in this representation.

It's a good time to pause for a moment and clarify something that could cause confusion. When we say the laws of physics have certain symmetries, such as rotational or translational, we do not mean that evolution in time must preserve their elementary geometric invariants. Instead, observers related by one of these symmetry transformations agree on those invariants. Say, for example, we have a temperature field. Observers whose coordinate origins are at different points will report the same distance between two temperature peaks at a given instant. But those peaks can definitely change separation as time passes. (This takes a little care when applied to time translation itself. In that case, we compare identically prepared systems started at different times, observing each after the same amount of elapsed time.)

#### Generator of Translations
Now that we have a function representation of translation, we want to find an infinitesimal generator that acts on functions to produce a translation. We can do so by considering what happens to a function's value under infinitesimal displacements. In that case, the new value $f(x-a)$ is close to the old value $f(x)$, and correction is given, in the limit, by the slope at $x$. This is the same idea that any curve becomes flat when zoomed in sufficiently:

![Tangent approximation under local zoom contact sheet](animations/symmetry-translation-tangent-zoom-contact-sheet.png)

[Open MP4: symmetry-translation-tangent-zoom.mp4](animations/symmetry-translation-tangent-zoom.mp4)

*A function value is translated by the function's slope*

That is the visual version of the first-order **Taylor expansion** that relates a function's derivatives to its value under translation:

```math
f(x-a)
=
f(x)
-
a\frac{df}{dx}
+
O(a^2).
```
The translation operator is then obtained from the derivative operator through the exponential map:

```math
T_a=\exp\left(-a\frac{d}{dx}\right).
```

#### Primer -- Eigenfunctions 
Readers familiar with eigenvectors can [skip this primer](#eigenfunctions-of-translational-symmetry).

An **eigenvector** is a vector that is rescaled by a parameterized class of operators, as opposed to changing direction under their action. We will see that in a function representation of translation, waves are eigenvectors of translation operators and, as such, are at the center of understanding physical states. We will be well served, then, to build some intuition about eigenvectors before delving further into wave function states.

Imagine pulling on the corners of a rubber sheet whose sides are aligned with a coordinate grids $x$ and $y$ axes. What does this action do to those axes? It rotates them toward each other while stretching them. Now, instead choose $u$ and $v$ to be diagonal axes. Now, when we stretch, the long axis is stretched but not rotated and the short axis is compressed but not rotated. The stretching action is now simple represented as scalar multiplication of the axes.

![The same stretch in ordinary and eigenvector bases](animations/symmetry-eigenbasis-comparison-poster.png)

[Open MP4: symmetry-eigenbasis-comparison.mp4](animations/symmetry-eigenbasis-comparison.mp4)

*A parameterized operation scales eigenvectors*

Beyond the simplified action on eigenvectors, once basis vectors are chosen to be eigenvectors, any other vector written as a linear combination of these transforms by having its components scaled independently:

Letting $s$ be the factor by which the long-axis component is stretched, we can see how the transformation of an arbitrary vector $\mathbf{r}$ simplifies using the system's natural basis:

| $(x,y)$ basis: components mix | $(u,v)$ basis: components do not mix |
|---|---|
| $\displaystyle \begin{aligned}\mathbf r&=\frac12\begin{pmatrix}s+s^{-1}&s-s^{-1}\\s-s^{-1}&s+s^{-1}\end{pmatrix}\mathbf r_{\mathrm{in}}\\&=\frac12\left[(s+s^{-1})x+(s-s^{-1})y\right]\hat{\mathbf x}\\&\quad+\frac12\left[(s-s^{-1})x+(s+s^{-1})y\right]\hat{\mathbf y}\end{aligned}$ | $\displaystyle \begin{aligned}\mathbf r&=\begin{pmatrix}s&0\\0&s^{-1}\end{pmatrix}\mathbf r_{\mathrm{in}}\\&=su\hat{\mathbf u}+s^{-1}v\hat{\mathbf v}\end{aligned}$ |

This is readily understood visually:

![An arbitrary vector transforms by scaling its eigenvector components](animations/symmetry-eigenbasis-components-poster.png)

[Open MP4: symmetry-eigenbasis-components.mp4](animations/symmetry-eigenbasis-components.mp4)

*Linear combinations of eigenvectors transform under diagonal matrices*

Now for a bunch of terminology. The values an operation scales eigenvectors by are its **eigenvalues**. A basis made from eigenvectors is an **eigenbasis**. When the scaled "vectors" are functions, we tend to call them **eigenfunctions**. When our vector space is a representation and is thus thought of as a state space, we may call the eigenfunctions **eigenstates**. As the transformation matrix is diagonal in the eigenbasis, the procedure for finding an eigenbasis is typically called **diagonalization**. 

An eigenvalue equation is an equation that can be solved to find the eigenvectors and eigenvalues of an operator. It takes the form:

```math
\hat A\mathbf v=\lambda\mathbf v,
\qquad \mathbf v\ne\mathbf 0.
```

Here $\hat A$ is the operator, $\mathbf v$ is an eigenvector, and $\lambda$ is its eigenvalue.

#### Eigenfunctions of Translational Symmetry
Since a function is an infinite-dimensional vector and the generator $d/dx$ is a way of writing an infinite-dimensional matrix, we can solve a similar eigenvalue equation here, which now takes the form of a differential equation:

```math
\frac{d}{dx}f(x)
=
\lambda f(x).
```

This says we are looking for a function whose derivative returns the same function, scaled by a single number. The solution is

```math
f(x)=Ce^{\lambda x}.
```

Since

```math
\frac{d}{dx}Ce^{\lambda x}
= C\lambda e^{\lambda x},
```

the eigenvalue of $d/dx$ is $\lambda$. 

We can now take note that a finite translation of an exponential functions also acts by scalar multiplication:

```math
f(x-a)=e^{-\lambda a}f(x).
```

![Differentiation and translation each reproduce an exponential multiplied by a number](animations/symmetry-translation-eigenfunctions-poster.png)

[Open MP4: symmetry-translation-eigenfunctions.mp4](animations/symmetry-translation-eigenfunctions.mp4)

*Differentiation and translation each scale an exponential*

#### Unitarity
We have determined that the eigenfunction of translation is the exponential function, but a question remains. Is the exponent real, imaginary, or complex? We will discuss imaginary numbers more below, but the bare-bones definition is

```math
i = \sqrt{-1}.
```

To resolve this, we will introduce the concept of unitary transformations. We will set the exponent question aside for a moment to explore some of the implications of unitary evolution in time. We should say that, while we are in a chapter about symmetry, in our treatment unitary evolution is not a consequence of symmetry, but follows from an additional physical principle. 

Before we go further, we need to step back and add context about where the idea of representations enters in physics. We've said that a vector in a representation space is a "state" that is acted upon by operators built from a symmetry group. In and of itself, this is a purely mathematical statement. The group we want to act on the representation space is spacetime symmetry, but we've said nothing about why physics requires a representation space up to this point. And in fact, our **classical** system of hard balls does not require a representation space to store state. Instead, we simply store all the positions and momenta of the system in a single, finite **phase space** vector. Symmetry representations are not required until we move from classical to quantum mechanics, where, as we will see, evolution must act linearly on a linear combination, or **superposition**, of states.

Thus, when we appeal to unitarity to choose our state representation, we are doing so in the context of quantum mechanics. Bearing that in mind, we can think of unitarity as being, in a way, the preservation of a principle that is self-evident in classical physics -- because objects occupy definite locations, have definite velocities, and follow definite, reversible trajectories, two states of a system, two different initial preparations, remain *distinguishable* as they evolve.

![Reversible and distinguishable histories](animations/symmetry-reversible-histories-poster.png)

[Open MP4: symmetry-reversible-histories.mp4](animations/symmetry-reversible-histories.mp4)

*States are self-evidently distinguishable in classical physics*

In such a classical system, distinguishability is absolute. In a quantum system, distinguishability is statistical. Two states may be more or less distinguishable in the sense that the best possible measurement gives us more or less chance of correctly identifying which state was supplied. However, time evolution preserves the *degree* of distinguishability of states. Unitarity is this preservation, and is defined mathematically as the preservation of "overlap" or **inner product** (a generalization of the dot product) of states:

```math
\langle U\psi_1,U\psi_2\rangle
=
\langle\psi_1,\psi_2\rangle,
\qquad
\text{where }U\text{ is by definition a unitary operator.}
```

In the animation below, the wave states evolve unitarily, preserving their overlap.

![Unitary and distinguishable histories](animations/symmetry-unitary-histories-poster.png)

[Open MP4: symmetry-unitary-histories.mp4](animations/symmetry-unitary-histories.mp4)

*Unitary evolution preserves the overlap between states*

In addition to distinguishability, unitary evolution ensures determinism and reversibility of a state's evolution. (Note that while quantum measurements are famously non-deterministic, the state evolution, nonetheless, is. This can be reconciled as the state in quantum mechanics is not the location of things, but a device for predicting the probability distribution of the location of things.) Unitarity also ensures, as we will show immediately below, that the integral of a function’s squared magnitude remains unchanged. If the function is initially normalized to one, it stays normalized. In quantum mechanics, where the squared magnitude of the wave function gives a probability density, this ensures that total probability remains one.

Let's now return to finding a suitable eigenbasis for the position translation operator. Since moving the observer cannot change distinguishability, translations must likewise preserve the inner product. This requires exponential eigenfunctions to have purely imaginary exponents. Consider a wave packet $v$ with $\langle v,v\rangle=1$ whose translation approximately satisfies $Uv\approx\mu v$. Preservation of the inner product gives

```math
1
=\langle Uv,Uv\rangle
\approx|\mu|^2\langle v,v\rangle
=|\mu|^2.
```

As the approximation becomes arbitrarily accurate, $|\mu|=1$.

We need to add a technical caveat. Because single-\(k\) complex exponentials extend across all space without decaying, they cannot be normalized. This is not an issue in practice, as wave packets made from combinations of them are normalizable.

Translating $e^{\lambda x}$ by $a$ multiplies it by $\mu=e^{-\lambda a}$. Therefore,

```math
e^{-2a\,\operatorname{Re}\lambda}=1
\quad\text{for all }a
\quad\Longrightarrow\quad
\lambda=ik,\qquad k\in\mathbb R.
```

A more intuitive way to understand this is to visualize the multiplying factors produced by translation. For a growing or decaying real exponential, translation multiplies its coefficient by a factor that stretches or shrinks it. A unitary action on an eigenmode must instead multiply its coefficient by a factor of magnitude one. Translating a complex exponential \(e^{ikx}\) supplies exactly such a factor. It rotates the coefficient without stretching or shrinking it.

![Translations rescale real exponential coefficients but rotate complex exponential coefficients while preserving their inner product](animations/symmetry-translation-unitarity-poster.png)

[Open MP4: symmetry-translation-unitarity.mp4](animations/symmetry-translation-unitarity.mp4)

*Two coefficients of the same complex exponential rotate together, preserving their inner product*

Since complex exponential functions are the eigenbasis for the representation space we will use for quantum states, let's spend some time gaining intuition about them. Spoiler, they are, up to a lack of complete generality, waves.

#### Primer - Complex Exponentials and Wave Packets
If you are familiar with complex exponential functions, feel free to [skip this section](#fourier-analysis).

We suggested above that the complex exponential function describes a wave. Let's explain that and generally build intuition around the complex exponential function. A single parameter complex exponential, $e^{i\theta}$, describes a circle. It is a way to repackage the rotation operator we have already seen:

```math
e^{i\theta}
\quad\longleftrightarrow\quad
e^{\theta \hat J}
=
R(\theta)
=
\begin{pmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{pmatrix},
\qquad
\hat J
=
\begin{pmatrix}
0 & -1\\
1 & 0
\end{pmatrix}.
```

$i$ is the generator of rotation in this 1-dimensional complex representation and plays the role $\hat J$ did in the 2-dimensional representation:

```math
i^2=-1
\quad\longleftrightarrow\quad
\hat J^2
=
\begin{pmatrix}
0 & -1\\
1 & 0
\end{pmatrix}^{\!2}
=
-I.
```
How is it possible to replace a $2x2$ matrix with a single number $i$? The answer is that $z$ has two real-number degrees of freedom. That is, we define a complex number $z$:

```math
z:=x+iy,
```

thus a complex number is mapped to a vector in the complex plane.

![A complex number as a vector in the complex plane](diagrams/symmetry-complex-plane-vector.png)

*The complex plane*

What action does multiplication by $i$ have at the identity vector $1$?

Here,

```math
\begin{aligned}
z&=1=1+0i,\\
z_{\mathrm{tan}}&=zi=1\cdot i=i=0+1i.
\end{aligned}
```

This is a vector in the complex plane that is perpendicular to the identity.

![The unit vector 1 and its unit tangent i in the complex plane](diagrams/symmetry-complex-unit-tangent.png)

*The action of $i$*

This is exactly the action the $\hat J$ matrix generator had in 2-dimensions, which we already argued exponentiates to rotation. Let's redo that argument here, as it leads to a gratifying result. Since multiplication by $i$ produces the tangent vector at every point and the tangent vector is the geometric version of the derivative, we have

```math
\frac{dz}{d\theta}=i\,z(\theta).
```

With $z(0)=1$, solving this differential equation, we then have

```math
z(\theta)=e^{i\theta}.
```

At $\theta=\pi$, halfway around the unit circle, we then have
```math
e^{i\pi}=-1.
```

This is Euler's identity, satisfyingly relating three of nature's most fundamental constants. 

We can map $z$ back to $x,y$ coordinates and obtain Euler's formula:

```math
e^{i\theta}=\cos\theta+i\sin\theta.
```

Engineers often represent real sinusoidal waves with complex exponentials using this formula and reading off the real part as multiplying exponentials is algebraically simpler than multiplying trigonometric functions.

Now let us turn from circular motion to an evolving complex wave. Let the **phase** vary with position $x$ and time $t$:

```math
\theta(x,t)=kx-\omega t,
\qquad
z(x,t)=Ae^{i(kx-\omega t)}.
```

Here $A$ is the wave's amplitude, $\lambda$ is its wavelength, $k=2\pi/\lambda$ is its **wave number**, and $\omega$ sets how quickly the phase changes with time.

In the animation, position runs along the helix. The other two directions show the real and imaginary parts of the complex value at each position. As time advances, these values rotate and the wave pattern travels along $x$.

![A complex plane wave, its two components, and the rotating value at a fixed position](animations/symmetry-complex-plane-wave-v2-poster.png)

[Open MP4: symmetry-complex-plane-wave-v2.mp4](animations/symmetry-complex-plane-wave-v2.mp4)

*The complex value rotates while its length stays fixed.*

The two components are $A\cos\theta$ and $A\sin\theta$. Their values oscillate, while the length of the complex value stays fixed:

```math
|z|=\sqrt{A^2\cos^2\theta+A^2\sin^2\theta}=A.
```

Translating this wave multiplies it by a phase factor:

```math
z(x-a,t)=e^{-ika}z(x,t).
```

The eigenvalue $e^{-ika}$ has magnitude one. This is the phase-only scaling allowed by unitarity.

#### Fourier Analysis
If you strike a chord on a piano, some complicated function of time describes how the sound pressure reaches your ear. It starts soft, gets louder, softens again. It has discernible main tones, but also a clutter of overtones that comprise the timbre of the piano. While you hear a clear tonal structure, a plot of the sound pressure level over time reaching your ear would completely obscure that structure. 

![Three-tone chord packet and its Fourier decomposition](animations/symmetry-fourier-three-tone-packet-contact-sheet.png)

[Open MP4: symmetry-fourier-three-tone-packet.mp4](animations/symmetry-fourier-three-tone-packet.mp4)

But we know something about this random-seeming function reaching your ear. We know it is comprised of mostly 3 pitches, and some overtones. If we plot the sound pressure level as a function of these pitches rather than as a function of time, the structure of our plot clearly reveals what we hear naturally with our ear. What we call a "pitch" is the frequency of a pure **mode**. The pattern of sound pressure over time is the sum, or "composition," of these modes. We can transform back and forth between the wave number and position representations. Typically we label the wave number representation with a tilde:

```math
\psi(x)\;\longleftrightarrow\;\tilde{\psi}(k).
```

The complex coefficient $\tilde{\psi}(k)$ specifies how strongly each mode contributes and with what phase. We recover the original function by adding these contributions:

```math
\psi(x)
=
\frac{1}{\sqrt{2\pi}}
\int_{-\infty}^{\infty}
\tilde{\psi}(k)e^{ikx}\,dk.
```

The integral is a continuous sum over wave numbers. The factor $1/\sqrt{2\pi}$ fixes our normalization convention.

Because wave number is conserved, while listeners at different distances from the piano hear the chord at different times, they agree on the tonal and timbral character.

This idea of **decomposing** a wave packet into its "Fourier modes" is remarkably general. Any function whose inner product with itself is finite can be decomposed into a linear combination, or **superposition**, of plane waves.

```math
\int_{-\infty}^{\infty}|f(x)|^2\,dx<\infty.
```

But this is not new to us. It is exactly what we have shown by carefully constructing the eigenbasis of the function representation of translation. 

As we've mentioned before, an exact plane wave extends uniformly to infinity in the limit, so its own squared magnitude has an infinite integral. It is an ideal building block. Superpositions of these waves can nevertheless form packets with finite total squared magnitude, which we can normalize as quantum states. The transformation from an amplitude over translation coordinate to amplitude over wave number coordinate is called a **Fourier transformation**.

Quantum mechanics uses this structure to represent quantum states. Extending the quantum description to the universe as a whole, some physicists propose that the universe is a single wave function from which observations are, in a very loose manner of speaking, sampled. If we're inclined to channel our inner hippie, we might trip out to the formulation that the structure of the complexity that unfolds in time is that of a single cosmic chord. Or, perhaps, as a quote attributed to Pythagoras has it: "There is geometry in the humming of the strings. There is music in the spacings of the spheres.”

## The Canonical Structure of State Space
We now understand that complex wave functions form a representation space for translations. Because translations describe changes in position, the complex wave function space provides a suitable representation space for physical evolution. A state is taken here to mean an instantaneous state, $\psi(x)$, upon which time evolution acts. Now we can ask ourselves the following startlingly fruitful questions. Do wave functions evolve into new wave functions? They better. And if they do, evolution must preserve the commutation structure of symmetry groups this space carries, for changing the wave function does not change that structure. We then ask, what implications does the preservation of this symmetry structure have for evolution? We will find that answering these questions, together with the principles that evolution must be unitary and that future states must be determined only by the current state, leads us, as a good argument can, to the abstract form of the quantum mechanical equations of motion.

### The Heisenberg Symmetry Group on State Space
Wave functions comprise our state space, that is the state at one instant. 
The Fourier duality of wave functions provides us with two paired translation operators, one in position and one in wave number. 

![Separate translations in position and wave number, each shown in its own representation](../../content/drafts/animations/symmetry-ccr-x-k-translations-symmetric-poster.png)

[Open MP4: symmetry-ccr-x-k-translations-symmetric.mp4](../../content/drafts/animations/symmetry-ccr-x-k-translations-symmetric.mp4)

*Wave Packet translated in position and momentum space*

Are these part of a symmetry group? To answer this, we need to first look at their commutator. We can compute the commutator directly with the generator definitions, but the more instructive route is to consider the equivalent of the commutator definition for finite translations, that is, to transport a function around a loop in $x$-$k$ space, ask how the function changes, and then shrink the loop to its infinitesimal limit. 

A position translation replaces $x$ by $x-a$. A wave-number translation shifts each mode from $k$ to $k+b$, which is done by multiplying the function by $e^{ibx}$:

```math
e^{ibx}e^{ikx}=e^{i(k+b)x}.
```

Now follow the loop:

| Action | Result |
|---|---|
| Start | $\psi(x)$ |
| Shift wave number by $b$ | $e^{ibx}\psi(x)$ |
| Shift position by $a$ | $e^{ib(x-a)}\psi(x-a)$ |
| Shift wave number by $-b$ | $e^{-iab}\psi(x-a)$ |
| Shift position by $-a$ | $e^{-iab}\psi(x)$ |

Both shifts have been undone, but the function has acquired a uniform phase of $-ab$, or $\phi$. Since phase shift is rotation in the complex plane, it “turns” the whole "spiral" of the wave function, much like a barbershop sign.

![Rotating barbershop sign](https://i.pinimg.com/originals/bc/5f/5d/bc5f5d496a9cf2a7bd6038541b4501f2.gif)

*A barbershop sign illustrates a phase shift on a complex wave function*

We have learned that phase rotations in the complex plane are generated by $i$. As we shrink the loop around $x$ / $k$ space, the finite transformation approaches the commutator. And because the transformation induced by travelling around the loop is a phase translation, and phase translations are generated by $iI$, we make the identification that the commutation relation is

```math
[\hat X,\hat K]
=
iI.
```

We give this a special name, the **canonical commutation relation**
![A complex spiral follows an x–k loop and returns to its original magnitude envelope with a quarter-turn of phase remaining](../../content/drafts/animations/symmetry-ccr-loop-complex-poster.png)

[Open MP4: symmetry-ccr-loop-complex.mp4](../../content/drafts/animations/symmetry-ccr-loop-complex.mp4)

*Phase as the $[\hat X,\hat K]$ commutator*

We can find the commutator directly from the operator definitions, but first we have to give the operator definitions. We have already given one:

```math
\hat K = -i d/dx.
```

But we have not defined $\hat X$. One definition, on account of Fourier duality, is to define $\hat X$ in the $k$-space representation:

```math
\hat X=i\frac{d}{dk}.
```

But this doesn't help us as we need to define both operators in the same representation. However, we can find the position generator directly in its own representation. We just saw that a wave-number shift is given by

```math
e^{ikx}\longrightarrow e^{i(k+b)x}=e^{ibx}e^{ikx}:
```

the translation operator is identified as

```math
(T_k(b)\psi)(x)=e^{ibx}\psi(x).
```

And since the generator is defined by $T_k(b)=e^{ib\hat X}$, expanding both sides for small $b$ gives

```math
\psi(x)+ib(\hat X\psi)(x)+\cdots
=
\psi(x)+ibx\psi(x)+\cdots.
```

Comparing the first-order terms,

```math
{(\hat X\psi)(x)=x\psi(x).}
```

The position operator in the position basis is just the wave function multiplied by the position coordinate. We can make sense of this as follows. Suppose the wave function is an idealized spike at some position that integrates to $1$ around that spike. The position operator multiplies the spike by $x$, so integrating the result yields the value of the position where the spike is.

From these definitions, we can compute the commutator.

```math
(\hat X\psi)(x)=x\psi(x),
\qquad
(\hat K\psi)(x)=-i\frac{d\psi}{dx}.
```

```math
\begin{aligned}
[\hat X,\hat K]\psi
&=\hat X(\hat K\psi)-\hat K(\hat X\psi)\\
&=-ix\frac{d\psi}{dx}
+i\frac{d}{dx}(x\psi)\\
&=-ix\frac{d\psi}{dx}
+i\psi+ix\frac{d\psi}{dx}\\
&=i\psi.
\end{aligned}
```

```math
[\hat X,\hat K]=iI.
```

The additional generator is $I$, which generates a global phase shift. 


![Nine complex modes and their exact sum rotate through five phase turns while their magnitude envelopes remain fixed](../../content/drafts/animations/symmetry-complex-phase-modes-poster.png)

[Open MP4: symmetry-complex-phase-modes.mp4](../../content/drafts/animations/symmetry-complex-phase-modes.mp4)

*Visualizing Phase Change*

Since the phase shift generator commutes with both $\hat X$ and $\hat K$, no further generator is needed and can conclude that $x$, $k$, and $\phi$ translation constitute a symmetry group.

```math
[\hat X,\hat K]=iI,
\qquad
[\hat X,I]=0,
\qquad
[\hat K,I]=0.
```

This group has a name, the Heisenberg-Weyl or $H_3$ group.

#### Preservation of the Canonical Commutation Relation
Now let us ask how these $H_3$ generators evolve. Since we require time evolution to be unitary in any case, we can take it as an assumption that the evolution operators are unitary. To make progress in our conceptual argument, we need to do a little linear algebra first. In contrast to transforming a vector by acting on the left with a matrix, we transform an operator by acting on the right with $U$ and on the left with its adjoint:

```math
\hat A_s=U(s)^\dagger \hat A\,U(s).
```

Here $\dagger$ denotes the adjoint, or conjugate transpose for matrices. For unitary $U$, the adjoint is its inverse: $U^\dagger=U^{-1}$.

![Rotating a stretch operator and constructing the same transformation by rotating space, stretching, and rotating back](../../content/drafts/animations/symmetry-operator-sandwich-poster.png)

[Open MP4: symmetry-operator-sandwich.mp4](../../content/drafts/animations/symmetry-operator-sandwich.mp4)

*Transforming an operator*

Using this procedure for transforming operators, we can now show that unitary evolution (invertibility is the necessary condition) preserves the commutator:

```math
\begin{aligned}
[\hat X_t,\hat K_t]
&=U_t^\dagger\hat X\underbrace{U_tU_t^\dagger}_{I}\hat KU_t
-U_t^\dagger\hat K\underbrace{U_tU_t^\dagger}_{I}\hat XU_t\\
&=U_t^\dagger[\hat X,\hat K]U_t\\
&=U_t^\dagger(iI)U_t\\
&=iI.
\end{aligned}
```

This tells us that the commutation structure must be preserved by time evolution. This is to say, evolution must transform wave functions such they continue represent $H_3$. 

As an important aside, we note that, since the generator of phase shifts is preserved under unitary evolution, phase is a symmetry of the equations of motion. We can add it to position and time translation, rotation, and velocity boosts as a transformation under which equations of motion do not change.

We can see in the preservation of the commutator the geometric imprint of the result that states remain distinguishable under unitary evolution. Let us imagine evolving a patch enclosed by our $x$-$k$ parallelogram. We map a collection of states to the patch using each state's average position and wave number:

```math
\psi\longmapsto\bigl(\langle\hat X\rangle_\psi,\langle\hat K\rangle_\psi\bigr).
```

Here the angle brackets denote average values. Evolving the collection moves its representative points. This area-preserving picture holds for some kinds of unitary evolution where our map of averages is valid, with the patch undergoing simple stretches, rotations, or shears. In these cases, commutator preservation is reflected in preservation of the patch's area. Unitary evolution ensures that the members of the collection do not *merge into one another* and are thus distinguishable. Beyond distinguishability, since the area of our $x$-$k$ parallelogram must be preserved in these cases, a change in one side’s length must be balanced by a change in the other side’s perpendicular reach, through changes in length, angle, or both. In this, we see the geometric imprint of the cross-coupled generator structure inherent in Fourier duality, which we will see appear as coupling between $\hat X$ and $\hat K$ in the equations of motion.

*Distinguishability and generator coupling visualized on state space*

#### The Suitability of $H_3$ Generators for Building the Evolution Generator
Now that we have established that our state space carries the $H_3$ symmetry group and this is preserved under evolution, we can ask two questions that will allow us to ascertain how this groups shapes the evolution of states. First, do the operators representing this group span the space of linear operators on our state space? Second, are its transformations unitary? If we can answer 'yes' to both of these, we will be justified in writing our time evolution generator *in terms of* $\hat X$ and $\hat K$.

We won't show that $H_3$ generators span the operator space but will take it as a given. By way a justification, we can imagine that, just as Fourier waves form a complete set for expressing functions, position and wave-number shifts form a complete set for expressing operators on those functions. By taking weighted combinations of these transformations, we can describe a general linear operation on our state space.

We already have shown that position translations are unitary. Since wave-number space is the dual of position space, wave-number translations are also unitary. And phase shifts, which are nothing more than scalar multiplication are unitary. In sum, the Heisenberg group's transformations preserve are unitary, or preserve inner product between states:

```math
\langle U\psi_1,U\psi_2\rangle
=
\langle\psi_1,\psi_2\rangle
\qquad
\text{for every symmetry action }U.
```


```math
\langle T_x(a)\psi,T_x(a)\chi\rangle
=
\langle\psi,\chi\rangle.
```

```math
\langle T_k(b)\psi,T_k(b)\chi\rangle
=
\langle\psi,\chi\rangle.
```

```math
\langle T_\phi(\beta)\psi,T_\phi(\beta)\chi\rangle
=
\langle\psi,\chi\rangle.
```

![Four panes show two wave functions translating in x or k while their overlap is preserved, with schematic state-space projections for a real, positive overlap](../../content/drafts/animations/symmetry-ccr-unitarity-poster.png)

[Open MP4: symmetry-ccr-unitarity.mp4](../../content/drafts/animations/symmetry-ccr-unitarity.mp4)

*Unitarity of position and wave-number translations*

The fact that $H_3$'s transformations are unitary lends itself to using $H_3$'s generators to build the unitary time evolution operator. For example, a real linear combination of $\hat X$ and $\hat K$ generates unitary evolution. In summary, the principle that current state determines future state demands that we build the evolution operator from operators on the instantaneous state space. The completeness of the operators generated by $\hat X$ and $\hat K$ makes this possible. And their self-adjointness makes building a unitary evolution operator straightforward.

#### Constructing an Evolution Operator
Knowing that time evolution preserves the structure of state space and that the evolution operator can be reasonably built from $H_3$'s generators, we can now see how remarkably much these constraints tell us about the evolution operator. 

Let's start by considering the action of any single-parameter unitary operator on our representation on any self-adjoint (unitary transformation generating) operator.

Let

- $U(s)$ be a unitary transformation,
- $\hat G$ be its generator,
- $\hat A$ be the generator of another unitary transformation.

The question we will ask is, what is the effect of $U$ on $\hat A$, expressed as a differential equation for $\hat A$. A differential equation on the generator is just the inverse of a differential equation on a state, in the exact sense that rotating coordinates one way is the same as rotating a vector the opposite way, or shifting a system one way is the same as shifting an observer the opposite way. The advantage of working with the evolution of the generator is that structural relations can be seen more directly than in when working with state evolution, which requires expanding the state in position or wave-number basis and defining representation-specific operators.

As usual, we define a unitary transformation as

```math
U(s)=e^{-is\hat G}.
```
and recall that

```math
\hat A_s=U(s)^\dagger \hat A\,U(s).
```
We can differentiate this expression for $\hat A_s$ using the product rule:

```math
\frac{d\hat A_s}{ds}=\frac{dU^\dagger}{ds}\hat A\,U+U^\dagger \hat A\frac{dU}{ds}.
```

Then substituting back in the definition of $U$, we arrive at

```math
\frac{d\hat A_s}{ds}=i\hat G \hat A_s-i\hat A_s\hat G=i[\hat G,\hat A_s].
```

This is very general result that will guide our next steps, so we want to understand what it is saying. The rate of change of a generator under a unitary transformation is ($i$ times) the commutator of the transformation’s generator with it. This identity is more a kind of definition of the commutator than any unexpected discovery. The best way to understand it may be some examples. Perpendicular translations commute, so the vertical displacement generator does not change as a system flows horizontally. In contrast, the generator of 3-dimensional rotation around the $x$-axis does change as a system flows around the $z$-axis. We saw this same idea in the animation above about evolving a stretch operator under rotation. Because the operator did change, it does not commute. On the other hand, an operator that stretched in all directions does commute with rotation and doesn't change as it evolves under rotation.

![A uniform stretch remains unchanged under rotation](../../content/drafts/animations/symmetry-uniform-operator-sandwich-poster.png)

[Open MP4: symmetry-uniform-operator-sandwich.mp4](../../content/drafts/animations/symmetry-uniform-operator-sandwich.mp4)

*Uniform stretch operator is constant under rotation evolution*

Let's now adopt the terminology that $U_s$ is an "evolution" operator that is written in terms of the generators of a suitable (complete and unitary) symmetry group on the state space. With this in mind, let's rewrite $\hat G$ as

```math
\hat G = \hat G(\hat X, \hat K).
```

We then have

```math
\frac{d\hat A_s}{ds}=i[\hat G(\hat X, \hat K),\hat A_s],
```

a perfectly lifeless geometric statement. But we breathe life into it when we apply the canonical commutator:

```math
[\hat X, \hat K] = iI.
```

When we do so, we find that

```math
\frac{d\hat X_s}{ds}
=
\frac{\partial \hat G}{\partial \hat K_s}.
```

This tells us that *if we know $\hat G$*, we can say exactly $\hat X$ and $\hat K$ evolve in time. But we have already said that weighted combinations of transformations generated by $\hat X$ and $\hat K$ can express a general linear operator on our state space. That is, if we know $\hat G$, we know the equations of motion governing our state.

Let's now show this identity 

```math
\frac{d\hat X_s}{ds}
=
i[\hat G(\hat X_s,\hat K_s),\hat X_s]
=
\frac{\partial \hat G}{\partial \hat K_s}.
```

The main idea is that, since $\hat X$ generates shifts of $\hat K$, commuting $\hat G$ with $\hat X$ measures how $\hat G$ changes when $\hat K$ shifts. The canonical relation $[\hat X,\hat K]=iI$ tells us:

```math
e^{-i\epsilon \hat X}\,\hat K\,e^{i\epsilon \hat X}
=
\hat K+\epsilon I.
```

We can apply this to the arguments to $\hat G$:

```math
e^{-i\epsilon \hat X}\,\hat G(\hat X,\hat K)\,e^{i\epsilon \hat X}
=
\hat G(\hat X,\hat K+\epsilon I).
```

Differentiate both sides with respect to $\epsilon$, at zero. As we have shown above, the left hand becomes

```math
-i\hat X\hat G+i\hat G\hat X=i[\hat G,\hat X].
```

On the right, we are changing $\hat K$ while holding $\hat X$ fixed so that

```math
\frac{\partial \hat G}{\partial \hat K}.
```

Thus, 

```math
i[\hat G,\hat X]=\frac{\partial \hat G}{\partial \hat K}.
```
Repeating the argument with the partners exchanged gives the other equation. The reversed commutator supplies the minus sign:

```math
i[\hat G,\hat K]=-\frac{\partial \hat G}{\partial \hat X}.
```

#### The Abstract Form of Wave Mechanical Equations of Motion             
Now, let's shift our notation to move from an abstract evolution operator to time evolution on our Fourier state:

| Notation | Meaning |
|---|---|
| $s \to t$ | The parameter is time. |
| $U_s \to U_t$ | The operator describes time evolution. |
| $\hat G \to \hat H$ | The generator is the time evolution generator. |

With these substitutions, we arrive the wave-mechanical prototype of the quantum "Heisenberg", or operator, form of "Hamilton's" equations of motion for unitary wave mechanics:


```math
\begin{aligned}
\frac{d\hat X_t}{dt}
&=i[\hat H,\hat X_t]
=\frac{\partial \hat H}{\partial \hat K_t},\\[0.5em]
\frac{d\hat K_t}{dt}
&=i[\hat H,\hat K_t]
=-\frac{\partial \hat H}{\partial \hat X_t}.
\end{aligned}
```

As we mentioned earlier, while the operator form of these equations leads naturally to their cross-coupled form, it obscures how the state itself evolves. Let's then take the opposing perspective and hold the operators fixed and evolve the state. Again, starting with

```math
U_t=e^{-it\hat H},
```
the evolved state is

```math
\psi_t=U_t\psi_0.
```

Differentiate the evolving state:

```math
\begin{aligned}
\frac{d\psi_t}{dt}
&=\frac{dU_t}{dt}\psi_0\\
&=-i\hat HU_t\psi_0\\
&=-i\hat H\psi_t.
\end{aligned}
```

Thus,

```math
i\frac{d\psi_t}{dt}=\hat H\psi_t.
```

That is the "Schrödinger equation" counterpart to the prototype Heisenberg/Hamiltonian equations above. We do not see the $\hat X$-$\hat K$ cross-coupling. But we also have not yet committed to a position or wave-number representation for the state. Once we do so, we have specific operator definitions for $\hat X$ and $\hat K$:

```math
\hat X\psi=x\psi,
\qquad \hat K\psi=-i\frac{\partial\psi}{\partial x}.
```

Consequently, writing $\hat H$ in terms of those operators gives

```math
i\frac{\partial\psi(x,t)}{\partial t}
=
\hat H\!\left(x,-i\frac{\partial}{\partial x}\right)\psi(x,t),
```

We may now ask, where is the canonical pairing between $\hat X$ and $\hat K$? The answer is that it is baked into the generator definitions. We can illustrate this by rewriting Schrödinger equation in the wave-number representation:

```math
i\frac{\partial\tilde{\psi}(k,t)}{\partial t}
=
\hat H\!\left(i\frac{\partial}{\partial k},k\right)\tilde{\psi}(k,t).
```

At this point, we have said nothing about the form $H$ takes. Spoiler alert, it is the energy function, leading to the poetic result that "energy generates time translation." We cannot say what the functional form of $H$ is without getting further into the geometry of spacetime as elucidated by special relativity.

### Position / Wave Number Uncertainty
As we know, a single-mode wave function has a single wave number. But what position does it have? There is no way to answer this as the wave is uniform over all position space. The same statement holds in reverse. A wave packet ideally localized at one position is uniform over all $k$-space. Anywhere in between these extremes, as a wave packet is more localized in one space, it is more spread out in the dual space. 

![A complex wave function and its Fourier transform sweep between the localization extremes](../../content/drafts/animations/symmetry-xk-fourier-complex-poster.png)

[Open MP4: symmetry-xk-fourier-complex.mp4](../../content/drafts/animations/symmetry-xk-fourier-complex.mp4)

*Trading off spread in position for spread in wave number*

We can easily see this relationship drawn on paper, but we also hear it in music. The precise pitch of a tuning fork requires long sustain, while the percussive clap of a clave has no clear pitch. This tradeoff is the root of the Heisenberg uncertainty principle, or what is known in popular science as "quantum fuzziness."

With this visual understanding of the tradeoff in the spread of the magnitude envelopes in $x$ and $k$ space, we can define the corresponding statistical standard deviation, or uncertainty, in position and wave number.

For simplicity, set the wave's mean position and wave number at their respective origins. Then

```math
(\sigma_x)^2
=
\int_{-\infty}^{\infty}x^2|\psi(x)|^2\,dx,
```

and likewise for $\sigma_k$.

$\sigma^2$ is a probability-weighted average of squared distances from the distribution’s center. This is the textbook definition of variance.

From the commutation relation

```math
[\hat X,\hat K]=iI,
```

one can derive the position/wave-number "uncertainty relation":

```math
\Delta x\,\Delta k\ge\frac12.
```
This derivation is rather involved, but we can get a feel for the result by plotting the squared magnitude of a wave function and labelling the standard deviation.

![The squared magnitudes trade position and wave-number widths](../../content/drafts/animations/symmetry-xk-squared-magnitudes-contact-sheet.png)

[Open MP4: symmetry-xk-squared-magnitudes.mp4](../../content/drafts/animations/symmetry-xk-squared-magnitudes.mp4)

*Trade-off in uncertainty of position and wave number*

## Wave Amplitude, Interference, and Path Summation 
1. include propagators, show integrals, be organized.

Let's ask the question, given an initial wave function, what is its amplitude at a given position at a later time? If we know the wave function, $\psi(x,t)$, we already know the answer. But what if we don't know $\psi(x,t)$ but instead a differential equation with boundary conditions that we solve to find the wave function. We just plug in $x$ and $t$. of a wave at any point? easy to answer with wave mechanics. at least in simple cases like free waves. but let's look at a different way to calculate. to do this calculation imaging a bunch of balls, each making more or less contribution to the amplitude.

my idea: start w/ free wave. (maybe planar so we can write it directly in eigenbasis, maybe spherical as it make "rays coming from a source built-in and eases the transition to double slit). Tell Huygens principle and do the construction (visually and in words, no math) with wavefront secondary sources. say we sum up contributions. don't worry about how (phase), just that we do. again, say just huygens, just that this recovers the wave function. now switch to double slit. ask, how do we solve this? method 1 (tried and true) use a different wave eq. method 2, exploit (the part of) Huygens that we can add the contributions for sources where the wavefronts from each meet.  (explain how its ok that we're not using all of huygens to each infinitesimal layer, but only adding the contributions at the destination. (the argument -if- we can decompose into constituents whose wave functions we know, we don't need to know what happens in between the the source and destination). now, introduce rays. (no balls, just rays, more legit sounding and avoid bouncing back and forth, just always rays, and we don't need "imagine balls" just "use rays as you think you would") the rays tell us "where the wave constituents meet". that's where we need to add them. now answer: how do we add them. (magnitude and phase). then ask, of, but how do we know the 'phase of a ray (now a line segment). well first, we know it relative to the beginning of the line segment. so care is needed to ensure the phase was the same at the two sources (is this right, am i saying this right). and then we're off to the races to talk about phases cancel away from the stationary path.

bot on why we don't need successive barriers:
Yes—and Huygens–Fresnel already allows exactly that: choose a destination and sum the contributions arriving there. You needn’t first calculate the field everywhere the waves overlap. Huygens–Fresnel calculation

The justification is linearity. Where waves overlap, they add, but that overlap does not alter how their separate contributions propagate.

For two successive propagation steps:
\[
\underbrace{U_2(U_1\psi_1+U_1\psi_2)}_{\text{add partway, then propagate}}
=
\underbrace{U_2U_1\psi_1+U_2U_1\psi_2}_{\text{propagate separately, then add}}.
\]
We can therefore postpone the addition until the destination.

There are two requirements:
- Propagation must be linear. Both contributions follow the same propagation law, including the medium and boundaries.
- We must know how each contribution propagates across the whole gap. That finite-distance rule replaces the explicit intermediate calculations. Linearity alone does not supply it.
In our idealized slit setup, the slit amplitudes are given and the gap is unobstructed, so this works. Calculating the intervening interference pattern would tell us more about the field, but would not change the amplitude at our chosen destination.

Interference along the way is not an additional interaction we have neglected.






Yes. And Huygens–Fresnel already allows exactly that: choose a destination and add the secondary-wave contributions arriving there. You needn’t calculate the field at every intervening point first. Huygens–Fresnel calculation

The justification is linearity. Where two waves overlap, their values add, but that overlap does not alter how their individual contributions propagate.

Schematically, if \(U\) propagates the field to the destination \(P\),
\[
[U(\psi_1+\psi_2)](P)
=
[U\psi_1](P)+[U\psi_2](P).
\]
Combine, then propagate—or propagate separately, then combine. The destination amplitude is the same.

There are two requirements:
- Propagation must be linear, with both contributions governed by the same medium and boundary conditions.
- We must know the propagation rule across the whole gap. Linearity lets us postpone addition, but does not itself supply that rule.
For our idealized double slit, we specify the amplitudes at the openings and use the known free-wave propagation beyond them. Calculating the intervening interference pattern would tell us more about the field, but would not change the answer at \(P\).


bot response to my proposal:
Yes. This sequence works: the reader sees what the contributions are before being asked how to add them. Phase then enters to answer a question the construction has already raised.

I would start with a plane wave. It connects directly to your existing modes, and normal incidence gives the two openings equal starting phases. Huygens’s secondary waves then supply the outward spreading and radial lines you wanted from a spherical starting wave.

I’d retain your order, with these points pinned down:
1. Method 1 uses the same wave equation with new boundary conditions. The barrier changes the problem we must solve, rather than requiring a different propagation law.
2. Choose the destination, then draw the rays to it. The constituent waves overlap throughout the region. The rays identify the contributions we are evaluating at our chosen point. “Here each ray connects a secondary source to the point where we calculate its contribution” gives them a concrete role without importing ball mechanics.
3. We need to know the relative starting phase, not necessarily make it equal. Your equal-phase setup is the simplest choice. Suppressing the common time dependence, the accounting is:
   \[
   \text{arrival phase}
   =
   \text{starting phase}
   +
   k\,\text{segment length}.
   \]
   With equal starting phases, the difference at the destination comes entirely from the difference in lengths. That is exactly why normal plane-wave illumination is convenient. Slit-phase accounting
4. Return from two contributions to many before stationary phase. Two slits establish reinforcement and cancellation. Then return to your original Huygens construction, now equipped to add all its contributions. You can examine neighboring routes to the same destination and show how, in the short-wavelength regime, rapidly varying phases largely cancel while neighborhoods of stationary paths contribute coherently.
That return to the opening construction is especially useful: first show that the contributions recover the wave, then reveal how their phases accomplish it.

next: stationarity, where does it really appear here.

---question all this, just stick to waves atm---

Anyone who has taken a high-school physics class has seen that, given a particular setup, the equations of motion tell us the path an object follows. For example, under constant acceleration,

```math
x = x_0 + v_0t + \frac{1}{2}at^2.
```

Such "physically valid" paths in the macroscopic world have a fascinating quality that can be leveraged to find the laws of motion that predict them. They are such that some quantity associated with possible paths, which is called **action**, is extremized at the valid path. In the next sections, we will explore the relationship between objects following paths and wave propagation. Just as an object following a definite path extremizes action, a wave, in the regime where it behaves like a ray, follows a path that extremizes accumulated phase. We will establish how contributions from many possible paths combine to produce this behavior, giving us a bridge between wave propagation and action extremization. We will then see how this stationary-path limit connects the quantum wave description we have alluded to with the well-defined paths that action extremization predicts for everyday macroscopic objects.

![Waves through fixed openings becoming narrow beams as the wavelength decreases](../../content/drafts/animations/symmetry-short-wave-beams-poster.png)

[Open MP4: symmetry-short-wave-beams.mp4](../../content/drafts/animations/symmetry-short-wave-beams.mp4)

*Interference and Rays*

---end question---
We would now like to switch perspectives from time evolving instananeous state to considering entire histories, where time becomes another parameter of the wave function. In notation:

We would now like to switch perspectives from evolving instantaneous states to considering entire histories, with time written explicitly as another argument of the wave function. In notation:

```math
\psi(x,t)=\psi_t(x)=(U_t\psi_0)(x).
```

At any fixed time, this gives an instantaneous state. Taken over all times, it describes the history.


---confusing---

Thus far we have described the symmetry group of a wave with a single translation direction $x$ and wave number, $k$. If the wave is to propagate, we also require that the wave represent time translation. We also need to require that time translation commute with spatial translation, for otherwise, it would change the mode composition over time, and spatial translation would no longer be a symmetry of nature. A single-mode evolving wave is then given by

---end confusing---



```math
M_0e^{i\left[kx-\omega t\right]}.
```

Because time is special, $\omega$ is called (angular) **frequency**, not wave number, but from a mathematical perspective, it is just another wave number.

Let us now ask the question: how do we find the amplitude at some point $B$ from some initial state of a wave? To do this, we can decompose the contributions into those from individual paths, starting with a very simple model. First, let's construct a point source of single-mode spherical waves emanating from $A$. Then let's add a barrier with two slits through which the wave can pass, $C$ and $D$. This setup allows us to calculate the amplitude at $B$ by combining only the amplitudes associated with the two paths $ACB$ and $ADB$.

![The two contributions $ACB$ and $ADB$ from a point source through two narrow openings](../../content/drafts/animations/symmetry-double-slit-candidate-paths-shortwave-arcs-poster.png)

[Open MP4: symmetry-double-slit-candidate-paths-shortwave-arcs.mp4](../../content/drafts/animations/symmetry-double-slit-candidate-paths-shortwave-arcs.mp4)

*Two Path Interference*

First, let's figure out how any one straight segment of a plane wave contributes to the amplitude at its endpoint. From

```math
e^{i\left[kx-\omega t\right]},
```

we can identify that

```math
\Delta\phi
=
k\,\Delta\ell
-
\omega\,\Delta t,
```

where $\Delta\ell$ is distance along the ray. In our setup, the segments combine into two candidate paths from $A$ to $B$:

```math
A \to C \to B
\qquad\text{and}\qquad
A \to D \to B.
```

We can now ask how each path contributes to the amplitude at $B$. The magnitude simply falls off as $1/r$ in accordance with spherical geometry. Also, since all contributions arrive at $B$ at the same observation time, their time-dependent phase is the same. The remaining things to calculate are their path-dependent spatial phases. Let $\ell_{AC}$ be the length of segment $AC$, and likewise for the other segments. The phase advances are

```math
\begin{aligned}
\phi_{AC}&=k\ell_{AC},
&
\phi_{CB}&=k\ell_{CB},
\\
\phi_{AD}&=k\ell_{AD},
&
\phi_{DB}&=k\ell_{DB}.
\end{aligned}
```

To transform the wave function along the path, we compose, or multiply, the phase actions. Because multiplying phase factors adds the angles in their exponents, we can simply add the phase angle contributions to calculate the total phase advance along $ACB$ and $ADB$, respectively. Letting $\phi_0$ include the original phase at $A$ and the temporal phase advance common to both paths, we have

```math
\begin{aligned}
\Phi_{ACB}
&=
\phi_0+\phi_{AC}+\phi_{CB}
=
\phi_0+k(\ell_{AC}+\ell_{CB}),
\\
\Phi_{ADB}
&=
\phi_0+\phi_{AD}+\phi_{DB}
=
\phi_0+k(\ell_{AD}+\ell_{DB}).
\end{aligned}
```

If we let $M_{ACB}$ and $M_{ADB}$ denote the magnitudes of the two path contributions, we then have the total contributions of each path at $B$:

```math
\Psi_{ACB}(B)
=
M_{ACB}
e^{i(\phi_0+\phi_{AC}+\phi_{CB})}.
```

```math
\Psi_{ADB}(B)
=
M_{ADB}
e^{i(\phi_0+\phi_{AD}+\phi_{DB})}.
```

What then is the total amplitude at $B$? It is just the sum of the two contributions arriving there. This is the principle of superposition which manifests visually as interference:

```math
\Psi_B
=
M_{ACB}
e^{i(\phi_0+\phi_{AC}+\phi_{CB})}
+
M_{ADB}
e^{i(\phi_0+\phi_{AD}+\phi_{DB})}.
```

Compose phase actions along a route. Add amplitudes across candidate routes.

We can plot the contribution from each path $ACB$ and $ADB$ in the complex plane, showing their sum by drawing them tip-to-tail. The vector from the beginning of the first arrow to the end of the second is the amplitude at $B$. Its length is the magnitude at $B$ and its angle is the phase at $B$.

![The two path contributions added tip-to-tail](../../content/drafts/diagrams/symmetry-double-slit-two-path-phasor-sum-shortwave.png)

*Amplitude at $B$ is the sum of contributions from $ACB$ and $ADB$*

We can repeat the same procedure with many more paths. As the path deviates more from a straight, minimum length path, it has a greater first-order change in phase. (This is the common result from calculus that near a function's minimum, there is no change to the value of the function in the first order of the argument.) When the candidate paths are far from the stationary value, their phases vary greatly, effectively cancelling out their contributions to the total sum. On the other hand, the phases of the paths near the stationary path align and dominate the sum. The green line in the tip-to-tail pane of the animation shows the sum of each of these contributions, giving the amplitude at $B$. The resulting intensity on the projection screen is the square of this magnitude.

![Many paths, their complex sum, and the resulting interference pattern](../../content/drafts/animations/symmetry-many-slit-paths-phasors-interference-contact-sheet.png)

[Open MP4: symmetry-many-slit-paths-phasors-interference.mp4](../../content/drafts/animations/symmetry-many-slit-paths-phasors-interference.mp4)

*Seeing stationarity emerge in closely spaced paths*

We can extend this procedure to its limit and include infinitely many screens with infinitely many slits, and recover unobstructed propagation. In the following animation, we start with a plane wave and recover that same wave. This construction, which provides a bridge to Feynman’s path integral formulation of quantum mechanics, has its roots in Huygens’ wavelets from the late 1600s, extended by Fresnel to include interference in the early 1800s.

![Huygens wavelets and their coherent sum as slits and screens are added](../../content/drafts/animations/symmetry-schematic-screens-v3-concise-poster.png)

[Open MP4: symmetry-schematic-screens-v3-concise.mp4](../../content/drafts/animations/symmetry-schematic-screens-v3-concise.mp4)

*Huygens–Fresnel principle*

Let us now ask one more question. What happens to our tip-to-tail diagram of the path contributions when we vary the wavelength relative to the slit? As the wavelength becomes small, even a slight change in path length can produce a large phase change:

```math
\phi=\frac{2\pi L}{\lambda}=2\pi n+\theta,
\qquad 0\leq\theta<2\pi.
```

Away from a stationary path, the phase winds through many cycles over a small range of paths, leaving an effectively random phase remainder so that contributions away from stationary paths largely cancel, while those near stationary paths dominate the sum.

![Three trials accumulate a quarter turn at the longer wavelength while the shorter wavelength produces many rotations](../../content/drafts/animations/symmetry-phase-remainder-spinners-run-3.png)

[Open MP4: symmetry-phase-remainder-spinners.mp4](../../content/drafts/animations/symmetry-phase-remainder-spinners.mp4)

In this limit, waves passing through slits behave as rays. A narrow beam through one opening reaches a small region of the screen, much as a thrown ball does.

Each path shares its color with its contribution to the tip-to-tail sum. As the wavelength shrinks, an increasingly narrow range of paths around the straight path carries the sum forward.

![Matching colors connect candidate paths to their contributions in the tip-to-tail sum as wavelength decreases](../../content/drafts/animations/symmetry-spectrum-path-diamond-wavelength-scan-lambda-3.png)

[Open MP4: symmetry-spectrum-path-diamond-wavelength-scan.mp4](../../content/drafts/animations/symmetry-spectrum-path-diamond-wavelength-scan.mp4)

## From Wave Mechanics to Quantum Mechanics
Quantum mechanics gives wave intensity a new physical interpretation. For a normalized wave function, the squared magnitude gives the probability density for a position measurement:

```math
\rho(x)=|\psi(x)|^2,
\qquad
\int_{-\infty}^{\infty}\rho(x)\,dx=1.
```

We could write the same relationship in the wave-number representation. In either case, the interpretation is as follows. A state is a superposition of the eigenstates in the chosen basis. An ideal measurement leaves the state in a specific eigenstate of the measured operator. The value of the measurement is the eigenvalue of that state. The squared magnitudes of the coefficients multiplying those eigenstates determine the outcome probabilities. They must sum to one for discrete outcomes. For continuous quantities such as position and wave number, they give probability densities that integrate to one. In this view, we may say, loosely, and only if we are so inclined, that the thing that "is" is a wave packet, and the wave-number distribution we measure is given by the squared magnitudes of its Fourier components.

![A complex amplitude and its squared magnitude predict the distribution of repeated position measurements at two wavelengths](../../content/drafts/animations/symmetry-amplitude-probability-poster.png)

[Open MP4: symmetry-amplitude-probability.mp4](../../content/drafts/animations/symmetry-amplitude-probability.mp4)

*From intensity to position measurement probability density*

To connect our wave description to mechanics, we need to relate phase to action.

Action, the quantity extremized by a physically valid path, can be constructed from the structure of **spacetime**, as articulated in the theory of special relativity, which will be the topic of our next chapter. Crudely speaking, because the quantity to be extremized must be agreed upon by all observers, it is natural that it should be an invariant of symmetry actions on spacetime. This leads to the result that the action is, in free motion, for massive bodies, proportional to an invariant built from translations — the time elapsed along a path as measured in a body's rest frame — times a dual invariant built from time and space translation generators. The former quantity is called **proper time** while the latter is the body's **mass**.

```math
S = -m\tau \qquad(c=1).
```

At the same time, we can calculate how phase advances along a path in spacetime. Introducing $\kappa$, the invariant built from wave function spacetime-translation generators, a single-mode plane wave along its inertial **worldline**, or path in a position vs time plot, is

```math
e^{-i\kappa\tau}.
```

We then have

```math
\mathrm{constant} = \frac{S}{\phi} = \frac{m}{\kappa}.
```

For a single free massive particle, multiplying the action by a constant leaves its stationary paths unchanged. A collision couples the variations of two particle types.

Let's consider an idealized brief collision with free motion before and after. Neglecting the interaction region's contribution to first-order changes in action and phase, each segment contributes $-m_i\tau_i$ to the action and, in the limit where waves follow definite paths, $-\kappa_i\tau_i$ to its propagation phase. The wave and mechanical descriptions must predict the same collision. We can hold the initial and final positions and times fixed and slightly shift the candidate collision point. At the stationary-phase point, the two particles' first-order phase changes cancel.

```math
\delta\phi_{\mathrm{total}}
=\delta\phi_1+\delta\phi_2=0.
```

With $a_i=m_i/\kappa_i$, this gives

```math
\begin{aligned}
\delta\phi_1&=\epsilon,\qquad\delta\phi_2=-\epsilon,\\
\delta S&=a_1\delta\phi_1+a_2\delta\phi_2=(a_1-a_2)\epsilon.
\end{aligned}
```

If the collision changes a particle’s speed or direction, we can shift the candidate collision point so that its phase changes to first order. Choose such a shift, so \(\epsilon\ne0\). For the action to be stationary at the same point, $a_1=a_2$. The shared conversion factor is $\hbar$.

![Varying a candidate collision point leaves phase and action stationary at different points for unequal conversion factors, and at the same point for a shared factor](animations/symmetry-collision-shared-scale-poster.png)

[Open MP4: symmetry-collision-shared-scale.mp4](animations/symmetry-collision-shared-scale.mp4)

*A shared conversion factor makes phase and action select the same collision*

We can measure its numerical value in the lab by comparing mass, as measured through collisions, to wavelength, as measured through interference. We then find

```math
\frac{S}{\phi}:=\hbar\approx 1.055\times10^{-34}\,\mathrm{J\,s}.
```

The smaller $\hbar$ is, the more phase cycles a given action difference produces. For candidate paths, we use the wave mode appropriate to each segment and add the accumulated phases, following the procedure described earlier. For two candidate paths,

```math
\Delta\phi=\frac{\Delta S}{\hbar}.
```

![Three wave-number shells share the same proper-time interval while phase cycles and action accumulates at corresponding rates](../../content/drafts/animations/symmetry-action-phase-desktop-poster.png)

[Open MP4: symmetry-action-phase-desktop.mp4](../../content/drafts/animations/symmetry-action-phase-desktop.mp4)

But this is exactly our condition for the path sum to be dominated by stationary paths. For everyday bodies, $\hbar$ is tiny compared with action differences so that their motion is effectively deterministic. Are we saying that the laws of motion we learn in high school physics are an approximation? Yes, a very good approximation.

We can now express our $H_3$ commutation relation in units of action:

```math
[\hat X,\hat K]=iI
\;\xrightarrow{\times\hbar}\;
[\hat X,\hbar\hat K]=i\hbar I.
```

We then have

```math
\hat P := \hbar\hat K,
```
where $\hat P$ generates position translations with the same scaling that relates phase to action. Its eigenvalue is **momentum**, $p$, giving us the quantum **canonical commutation relation**:

```math
[\hat X, \hat P] = i\hbar I.
```

Recall that $x$ and $p$ are the eigenvalues of the $\hat X$ and $\hat P$ operators, respectively, acting on the wave function. We then have

```math
\Delta x\,\Delta k\ge\frac{1}{2}
\;\xrightarrow{\Delta p=\hbar\Delta k}\;
\Delta x\,\Delta p\ge\frac{\hbar}{2}.
```

This is the Heisenberg uncertainty relation, which states that a quantum state cannot have perfectly sharp values of both position and momentum, which becomes relevant at subatomic scales.

The canonical commutation relation, along with the definitions of $\hat X$ and $\hat P$, is also useful as a starting point from which to derive quantum theory’s general law of motion.


