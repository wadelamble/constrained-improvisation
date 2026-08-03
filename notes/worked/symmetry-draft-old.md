
# Symmetry
Strike a pool ball with a cue, and the balls move in an expected way. Move the table over a few feet, and the balls move in recognizably the same way. Wait a few minutes, and the balls move in the same way. Turn the pool table a few degrees, and the balls still move the same way. Put the pool table on a train, and, again, the balls move in the same way. These are the manifest symmetries of the space we live in -- position and time translation, rotation, and velocity "boosts."

The symmetry of physical behavior may be an interesting observeration, but why start our story here? The reason is this. Symmetry constrains patterns of motion and classifies that which moves. One may rightfully say that modern physical theories proceed by identifying what patterns symmetry permits, then honing those possibilities to match what is observed. 

The term "symmetry" in this context may not at first glance seem like the same concept as, say, a triangle's symmetry, but it precisely is. We can leverage this commonality to build up a vocabulary for symmetry from simple, concrete examples that is essential to tell our story.

## Discrete symmetries
Consider a triangle.

![](diagrams/symmetry-triangle.svg)

An equilateral triangle.

We can see its obvious symmetry. To categorize its symmetry we can write down all the actions that leave it unchanged:
1. Do nothing
2. Rotate 120°
3. Rotate 240°
4. Flip along an axis
5. Flip then rotate 120°
6. Flip then rotate 240°

![Triangle symmetry actions animation contact sheet](animations/symmetry-triangle-actions-contact-sheet.png)

[Open MP4: symmetry-triangle-actions.mp4](animations/symmetry-triangle-actions.mp4)

We say the triangle "belongs to the $D_3$ symmetry **group**." Any number of objects possess $D_3$ symmetry.

![](diagrams/symmetry-d3-carriers.svg)

We tend to think of a "triangles's symmetry" not the "symmetry of two rotations and flips about 3 axes," but this latter way of thinking in terms of symmetry groups is more general and is the defintion used in physics, where we ask not "what symmetry does this or that object have?" but "what objects can realize the symmetry evident in nature?"

### Representations
We can plainly "see" the symmetry of the triangle, but what if we want to write it down symbolically? Specifically, what if we want to track how a sequence of symmetry group actions transform an object? For example, suppose we label our triangle's vertices \(A, B, C\) and ask, if we rotate twice, flip once, then rotate again, where is vertex \(A\) sent? Recognizing that the triangle's state has three ordered components, we might guess that we could represent the triangle as a vector with 3 components. We coud then represent 120° rotations as **transformations** that permute the vertices in accordance with the symmetry group actions. 

There is nothing special about the vertices here, we could just as easily have chosen the midpoint of the edges or any other triplet of points on the triangle, and the same matrix the permutes the vertices would permute those vectors. That is, the group actions are represented as **linear** transformations. A **representation** of a symmetry group is a vector space and set of the linear transformations that compose in the same way as the group actions.

To construct a 3-dimensional representation of $D_3$, we map the 3 vertices to component of a vector.

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

For example, a single rotation would be represented as:

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
\end{pmatrix}
$$

The matrices that provide a minimal set of transformations from which all other operations can be constructed are they symmetry's **generators**. For example, in the 3-dimesional representation of $D_3$, all operations can be constructed from one rotation matrix and 3 flip matrices, one for each axis.. 

Visually, permutations that correspond to rotations of the triangle are 120-degree rotations about a diagonal axis in this vector space, while those that correspond to flips are flips about planes that contains the diagonal axis.

![D3 rotations and flips in the 3D representation](animations/symmetry-d3-rotations-vs-flips-contact-sheet.png)

[Open MP4: symmetry-d3-rotations-vs-flips.mp4](animations/symmetry-d3-rotations-vs-flips.mp4)

Now, notice something about these visualizations. The transformation of any vector lies in a plane as any 3 points do, and all such planes are parallel to one another. Thus, if we subtract off the average of the vectors, that is, if we move the point where the plane intersects the axis of rotation to the origin, we preserve the permutation structure of the transformations. We thus see that the $D_3$ symmetry is just as well represented as 120-degree rotations in the subspace of a 2-dimensional plane.

![D3 3D representation collapsing to the 2D plane](animations/symmetry-d3-irrep-collapse-contact-sheet.png)

[Open MP4: symmetry-d3-irrep-collapse.mp4](animations/symmetry-d3-irrep-collapse.mp4)

We also notice that vectors that lie on the axis of rotation itself are left unchanged the transformation. A way to think of this is to allow the triangle's vertices to store some information, like a number or any numerical quantity. If the value they store is the same for all vertices, the symmetry actions have no effect, whereas if they are different, the actions permute those values in a way that can be represented in a 2-dimensional vector space. The 3-dimensional representation space we began with is thus decomposable into 2 subspaces, one 1-dimensional, the other 2-dimensional. These cannot be decomposed further. That is, there is no lower-dimensional space such that an allowable transformation of any state remains in that space. The 1-dimensional and 2-dimensional representations are called **irreducible representations** or **irreps** for short. This is substantially heavy math. Why do we bother? The reason is that, in the story we have to tell of quantum physics, where constituents of matter must abide the symmetry of nature, each consituent, each type of particle such as electron or photon, corresponds an to irreducible representations of nature's symmetry. A particular state of the particle is encoded in a vector in the corresponding irrep.

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

These invariants are obscure without seeing the derivation, but the important point for now is that we can write an expression in terms of coordinates that must not change under the symmetry transformation. 

Why should we care about invariants? As we will see, a system’s characteristic physical behavior, the pool ball’s commonality, so to speak, is encoded by assigning a number to each possible history. For a given history, that number is the same for every **inertial** observer whose frame differs in position, time, orientation, or constant velocity.

## Continuous symmetries
What rotations return a circle to itself? All of them, of course! Similarly, all translations return a line to itself. The symmetries of space and time are continuous and can therefore be represented as transformations that depend on continuously varying parameters. 

![Continuous rotation and translation symmetries](animations/symmetry-continuous-so2-translation-contact-sheet.png)

[Open MP4: symmetry-continuous-so2-translation.mp4](animations/symmetry-continuous-so2-translation.mp4)

### Infinitesimal Generators
As we saw, in the $D_3$ symmetry group, we can build any action from a combination of the elemental actions of rotations and flips about an axis. Now let us ask the question: What is the generator of a continuous transformation? Let's say we want to rotate a circle by 10°. We could compose 10 1° rotations. But what if we want to rotate by 1°. We can see where this is going. The generators must be infinitesimal rotations. Noting that if we zoom in enough, any curved surface appears flat, we see that a continuous symmetry's infinitesimal generators are the vectors in the tangent plane to the symmetry's action. 

![Curved surface with tangent plane and tangent vectors](diagrams/tangent-plane-curved-surface.png)

*Infinitesimal generators are vectors in the plane tangent to the space of symmetry transformations*

As every high school calculus student learns, a derivative of a function is the tangent line to that function. In the case of a circle, in the 2-dimensional representation, we have a single variable that parameterizes the operator matrix:

```math
R(\theta)
=
\begin{pmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{pmatrix}.
```

We can take the derivative of the matrix valued function of $\theta$. This is:

```math
\frac{dR}{d\theta}
=
\begin{pmatrix}
-\sin\theta & -\cos\theta\\
\cos\theta & -\sin\theta
\end{pmatrix}.
```

To obtain a single matrix representing this infinitesimal nudge, we evaluate the derivative at $\theta=0$, where $R(0)=I$ is the identity transformation. In that case:

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
J
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

*The generator matrix \(J\) acts on the point \((1,0)\) to produce the tangent vector \((0,1)\) shown here.*

$J$ acts on any point on the circle to produce the tangent vector at that point. Putting this into calculus notation:

```math
\frac{d\mathbf v}{d\theta}
=
J\mathbf v.
```

We now have a differential equation for the transformation that uses the generator. We found this by starting with a known transformation and deducing its generator. But we can just well go in the opposite direction. Given this differential equation, we can find the transformation:

```math
\mathbf v(\theta)
=
e^{\theta J}\mathbf v(0).
```

The exponential of a matrix is defined in terms of the Taylor expansion for the an exponential:

```math
e^{\theta J}
=
I
+
\theta J
+
\frac{\theta^2}{2!}J^2
+
\frac{\theta^3}{3!}J^3
+
\cdots .
```

Now we notice something. Since:

```math
J^2=-I,
```

the even powers of $J$ become powers of $I$, while the odd powers become powers of $J$. Therefore

```math
e^{\theta J}
=
\left(
1-\frac{\theta^2}{2!}+\frac{\theta^4}{4!}-\cdots
\right)I
+
\left(
\theta-\frac{\theta^3}{3!}+\frac{\theta^5}{5!}-\cdots
\right)J.
```

These are the the Taylor series for sine and cosine:

```math
e^{\theta J}
=
\cos\theta\,I
+
\sin\theta\,J.
```

Substituting in $J$ gives

```math
e^{\theta J}
=
\begin{pmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{pmatrix}
=
R(\theta).
```

This is the **exponential map**. It takes the infinitesimal generator $J$ and returns the finite symmetry transformation $R(\theta)$.

#### Symmetry Flows

We can think of a symmetry transform as a "uniform looking" vector field, as illustrated below:

![Rotation generator as a vector field](animations/symmetry-so2-vector-field-flow-contact-sheet.png)

[Open MP4: symmetry-so2-vector-field-flow.mp4](animations/symmetry-so2-vector-field-flow.mp4)

Here we ask not what happens when the transformation is applied to a single set of starting conditions, but what the transformation does to all starting conditions. This view lendss itself to studying collections of histories. 

#### Invariants and Metrics
What is the invariant of rotation in this representation? It is the length of vectors and the angles between them.

![Rotation preserves vector lengths and angles](animations/symmetry-rotation-vector-invariants-contact-sheet.png)

[Open MP4: symmetry-rotation-vector-invariants.mp4](animations/symmetry-rotation-vector-invariants.mp4)

These relationships are expressed by a single invariant, the dot product.

```math
\mathbf u\cdot\mathbf v
=
u_xv_x+u_yv_y.
```

An invariant of this sort, that fixes some notion of placing reliable rulers on the space, is a **metric**. It defines the way to measure the geometric relationships that a symmetry transformation preserves. For normal rotations (and translations), these relationships are intuitive, but a symmetry may preserve a less intuitive metric. If we define invariant length not as \(x^2+y^2\) but as \(t^2-\mathbf{x}^2\), a hyperbolic rotation, or one that stretches out as it approaches assymptotes, leaves the interval unchanged even though the distance between transformed vectors appears to change using our everyday notion of distance. Such a hyperbolic metric, as we will see, encodes the asymptotic limit of light speed in the relativistic geometry **spacetime**.

![Hyperbolic rotation preserving the interval](animations/symmetry-hyperbolic-rotation-contact-sheet.png)

[Open MP4: symmetry-hyperbolic-rotation.mp4](animations/symmetry-hyperbolic-rotation.mp4)


### Translations and Function Representation
Like rotation, translation plainly does not change the distance between points. It is, in a sense, the simplest possible symmetry. It would be natural to think the ideal representation space for a translation is simply a one dimensional vector space. But there is a problem. If an operation is to move $x$ by some amount $a$

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

These are not equal unless $a=0$. Thus translation is a perfectly good action on points, but it is not a linear operation on the one-dimensional vector space of coordinate values.

![Point translation failing linearity](animations/symmetry-translation-point-linearity-failure-contact-sheet.png)

[Open MP4: symmetry-translation-point-linearity-failure.mp4](animations/symmetry-translation-point-linearity-failure.mp4)

Functions solve this problem. Instead of translating the point $x$, we translate a function by shifting its argument:

```math
(T_a f)(x)=f(x-a).
```

Now the state is the whole function $f$, and $T_a$ is an **operator** on the vector space of functions. An operator is a generalization of a matrix when applied to continuous functions. A continuous function is as an infinite-dimensional vector, in which its domain values are "axes," or components labels, and its range values are the component values. We can transform one function to another with an infinite dimensional matrix, but in practice, we can condense this into a well-known operation, such as taking a function's derivative.

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

Thus translations act linearly on functions even though they do not act linearly on points.

![Function translation preserving linearity](animations/symmetry-translation-function-linearity-contact-sheet.png)

[Open MP4: symmetry-translation-function-linearity.mp4](animations/symmetry-translation-function-linearity.mp4)

If we step back, this all makes sense. Translational symmetry needs an object to translate, just as $D_3$ symmetry needs a triangly thing to translate. We can think of the function purely as a shape. If there is translation symmetry, that shape is preserved.

![Translation preserving a function shape](animations/symmetry-function-translation-shape-contact-sheet.png)

[Open MP4: symmetry-function-translation-shape.mp4](animations/symmetry-function-translation-shape.mp4)


Such a shape is understood as a vector space in the same way that $D_3$ is. Now each point on the number line is like the vertex of a triangle, and it contains the component of a vector. Visually, it is the axis of a coordinate plot. Indeed, the $D_3$ representation is itself a function representation, with a domain that contains only three members and is cyclic. 

Functions are exactly what is needed for models. If there is some agreed-upon base space, for example location on a sphere or a grid, and some question with a quantitative answer at each point of that space, then there is by definition a function that models that. In particular, in physics we ask questions like "what is the momentum at this point?" and translation symmetry says that the shape of the $p(x)$ equation is the same when shifted to $p(x+a)$.

#### Generator of Translations
We know that we need an infinitesimal generator and that it should act on functions. How can we determine the generator? Consider the relation of the new value of a function under translation.

For a finite translation, the graph moves by a visible amount. But the generator is supposed to capture the infinitesimal version of that motion, so we ask what happens when the translation amount is very small. If the shift is small, the new value $f(x-a)$ is close to the old value $f(x)$. The correction is controlled by the slope at $x$.

![Tangent approximation under local zoom contact sheet](animations/symmetry-translation-tangent-zoom-contact-sheet.png)

[Open MP4: symmetry-translation-tangent-zoom.mp4](animations/symmetry-translation-tangent-zoom.mp4)

That is the content of the first-order Taylor expansion:

```math
f(x-a)
=
f(x)
-
a\frac{df}{dx}
+
O(a^2).
```

Since translation acts as

```math
(T_a f)(x)=f(x-a),
```

we have

```math
T_a f
=
f
-
a\frac{df}{dx}
+
O(a^2).
```

The infinitesimal part is therefore $-d/dx$. With this convention, the generator of translations is

```math
P
=
-
\frac{d}{dx}.
```


#### Eigenfunctions of Translation
Imagine a rubber sheet. You pull on the corners of the sheet. What does this do to the \(x\)- and \(y\)-axes? It rotates them. Now, instead choose \(x\) and \(y\) to be diagonal axes. Now, when you stretch, the "long" axis is stretched but not rotated and the "short" axis is compressed but not rotated. The action of this stretching "operator" on these axes is now obviously simpler -- it is just scalar (single number) multiplication of the original vector. But what about any random direction....

Write an arbitrary vector in the horizontal/vertical basis:

```math
\mathbf r
=
x\hat{\mathbf x}
+
y\hat{\mathbf y}.
```

Now stretch by a factor of $2$ along the $45^\circ$ direction and compress by a factor of $1/2$ along the perpendicular $45^\circ$ direction. In the horizontal/vertical basis, the transformed components are

```math
x'
=
\frac54x+\frac34y,
\qquad
y'
=
\frac34x+\frac54y.
```

So

```math
\mathbf r'
=
\left(\frac54x+\frac34y\right)\hat{\mathbf x}
+
\left(\frac34x+\frac54y\right)\hat{\mathbf y}.
```

The components mix. The new $x$ component depends on both the old $x$ and the old $y$, and likewise for the new $y$ component.

Now choose the $45^\circ$ basis:

```math
\hat{\mathbf u}
=
\frac{1}{\sqrt2}
\left(
\hat{\mathbf x}
+
\hat{\mathbf y}
\right),
\qquad
\hat{\mathbf v}
=
\frac{1}{\sqrt2}
\left(
\hat{\mathbf x}
-
\hat{\mathbf y}
\right).
```

In that basis,

```math
\mathbf r
=
u\hat{\mathbf u}
+
v\hat{\mathbf v}.
```

The same transformation is now

```math
u'=2u,
\qquad
v'=\frac12v.
```

So

```math
\mathbf r'
=
2u\hat{\mathbf u}
+
\frac12v\hat{\mathbf v}.
```

The components do not mix. Each component only gets scaled.

![Stretching in ordinary and eigenvector bases](animations/symmetry-eigenbasis-stretch-contact-sheet.png)

[Open MP4: symmetry-eigenbasis-stretch.mp4](animations/symmetry-eigenbasis-stretch.mp4)

We call the vectors that are scaled by an operation the **eigenvectors**. If the vectors are functions, we say **eigenfunctions**. If those functions are associated with physical states, we say **eigenstate**, and if we have a **basis**, or coordinate axes, made from eigenvectors, we call this an **eigenbasis**.

We can treat the stretching as a matrix operator. In the original basis, the matrix would be:

```math
\begin{pmatrix}
\frac54 & \frac34\\
\frac34 & \frac54
\end{pmatrix}.
```

While in the eigenbasis it would be:

```math
\begin{pmatrix}
2 & 0\\
0 & \frac12
\end{pmatrix}.
```

We can see the operator matrix in the eigenbasis is diagonal, so we often call finding the eigenbasis **diagonalizing** the operator.

We can now find the factor by which this stretching operator scales its eigenvectors, or its **eigenvalues**.

The eigenvalue equation is

```math
A\mathbf r
=
\lambda\mathbf r.
```

Using the original-basis matrix,

```math
\begin{pmatrix}
\frac54 & \frac34\\
\frac34 & \frac54
\end{pmatrix}
\begin{pmatrix}
x\\
y
\end{pmatrix}
=
\lambda
\begin{pmatrix}
x\\
y
\end{pmatrix}.
```

To find the allowed values of $\lambda$, subtract $\lambda\mathbf r$ from both sides:

```math
\begin{pmatrix}
\frac54-\lambda & \frac34\\
\frac34 & \frac54-\lambda
\end{pmatrix}
\begin{pmatrix}
x\\
y
\end{pmatrix}
=
\begin{pmatrix}
0\\
0
\end{pmatrix}.
```

This has a nonzero solution only when the determinant vanishes:

```math
\left(\frac54-\lambda\right)^2
-
\left(\frac34\right)^2
=
0.
```

So

```math
\frac54-\lambda
=
\pm\frac34.
```

Therefore

```math
\lambda=2,
\qquad
\lambda=\frac12.
```

These are exactly the stretch factors in the $45^\circ$ basis.

Since a function is an infinite-dimensional vector and the generator $d/dx$ is a way of writing an infinite-dimensional matrix, we can solve a similar eigenvalue equation here, which now takes the form of a differential equation.

The eigenvalue equation is

```math
\frac{d}{dx}f(x)
=
\lambda f(x).
```

This says we are looking for a function whose derivative returns the same function, scaled by a single number. The solution is

```math
f(x)=Ce^{\lambda x}.
```

The exponent can be, and in most of what we discuss, will be imaginary. The mystery of $i^2=-1$ is less mysterious when we recall that the rotation operator in the two-dimensional representation had the same property:

```math
J^2=-I.
```

In both the cases of real and complex exponents, the scale factor is the eigenvalue of the translation operator. Both cases generate rotation, hyperbolic in the real case and circular in the imaginary case. 

Both real and imaginary exponential functions can act as a generalized eigenbasis, but if we are to have a metric space in which some inner product \(the generalization of a dot product\) measures the similarity of functions, the translation operation must preserve the inner product. This condition is called **unitarity**, and translation is not unitary for the case of real exponentials. The condition of **unitarity** cannot be overstated. It is the property that ensures different states remain *distinguishable* under symmetry transformations and that those transformations are *reversible*. Let

```math
f_k(x)=e^{kx},
\qquad
g_l(x)=e^{lx}.
```

Under translation,

```math
(T_a f_k)(x)
=
f_k(x-a)
=
e^{-ka}f_k(x),
```

and

```math
(T_a g_l)(x)
=
g_l(x-a)
=
e^{-la}g_l(x).
```

Therefore

```math
\langle T_a f_k,T_a g_l\rangle
=
e^{-(k+l)a}
\langle f_k,g_l\rangle.
```

This equals the original inner product only when

```math
e^{-(k+l)a}=1.
```

For real $k$ and $l$, this is not generally true. Thus real exponentials are eigenfunctions of translation, but they are not compatible with translation as an inner-product-preserving symmetry. Thus the eigenfunctions of the translation operator are complex exponentials, that is $e^{ikx}$. Complex exponentials encode circular motion, and, when acted upon a translation symmetry operator, encode waves. Let's see how this works.

#### Complex exponential and waves
Understanding how complex numbers relate to circular rotation requires following a few steps, but the main idea is that complex numbers afford a way to treat rotation not as complicated mixing of $x$ and $y$ axes, but as simple scaling of the axis of rotation. In this picture, $i$ is the generator or rotation.

This scaling can map to a two-dimensional plane because complex numbers require two components. We write a complex number in terms of its real and imaginary components. If we call some complex number $z$, then

```math
z:=x+iy,
```

thus a complex number is mapped to a vector in the complex plane.

![A complex number as a vector in the complex plane](diagrams/symmetry-complex-plane-vector.png)

Using

```math
e^{i\theta}
=
\cos\theta+i\sin\theta,
```

multiply a complex number $z=x+iy$:

```math
z'
=
e^{i\theta}z
=
(\cos\theta+i\sin\theta)(x+iy).
```

Expanding gives

```math
z'
=
(x\cos\theta-y\sin\theta)
+
i(x\sin\theta+y\cos\theta).
```

Therefore

```math
x'
=
x\cos\theta-y\sin\theta,
\qquad
y'
=
x\sin\theta+y\cos\theta.
```

So multiplication by $e^{i\theta}$ is the same operation as

```math
\begin{pmatrix}
x'\\
y'
\end{pmatrix}
=
\begin{pmatrix}
\cos\theta & -\sin\theta\\
\sin\theta & \cos\theta
\end{pmatrix}
\begin{pmatrix}
x\\
y
\end{pmatrix}.
```
Thus complex scaling by $e^{i\theta}$ is a two-dimensional rotation.

If the translation direction is drawn as an axis, $e^{ik\theta}$ traces a spiral around that axis. Its two real components are $\cos\theta$ and $\sin\theta$, so each component moves back and forth like an ordinary wave. Here, $k$ is the inverse of the wavelength and is called the **wave number**. 

Below, the cylinder axis is time, though the same picture applies to any translation direction. 

![Complex exponential as a plane wave](animations/symmetry-complex-exponential-plane-wave-contact-sheet.png)

[Open MP4: symmetry-complex-exponential-plane-wave.mp4](animations/symmetry-complex-exponential-plane-wave.mp4)

For translations, the physically important case is not ordinary growth or decay, but pure phase change. So write the eigenvalue as

```math
\lambda=ik.
```

Then

```math
f_k(x)
=
Ce^{ikx}.
```

And indeed,

```math
\frac{d}{dx}e^{ikx}
=
ik e^{ikx}.
```

Thus the plane wave is an eigenfunction of the translation generator.

Under a finite translation,

```math
(T_a f_k)(x)
=
f_k(x-a)
=
e^{ik(x-a)}
=
e^{-ika}e^{ikx}.
```

The translated plane wave is the same plane wave multiplied by a single phase factor.

#### Fourier Decomposition
If I strike a chord on a piano, some complicated function of time describes how the sound reaches your ear. It starts soft, gets louder, softens again. It has discernible main tones, but also a clutter of overtones that comprise the timbre of the piano. While you hear a clear tonal structure, a plot of the sound pressure level over time reaching your ear would completely obscure that structure. 

![Three-tone chord packet and its Fourier decomposition](animations/symmetry-fourier-three-tone-packet-contact-sheet.png)

  
But we know something about this random-seeming function reaching your ear. We know it is comprised of 3 pitches, and some overtones. If we plot the sound pressure level as a function of these pitches rather than as a function of time, the structure of our plot clearly reveals what we hear with our ear. 

Why is this? It is exactly what we have just learned. Since plane waves, or pitches, are the eigenfunctions of the translation operator, the composition in terms of these **modes** is not altered by translational symmetry transformations. 

If our complicated function of loudness over time can be represented by a linear combination, or **superposition** of wave modes, perhaps any function can be. Well that's almost true. Just as we saw that real exponential functions "blow up" under translation, any function that similarly blows up cannot be decomposed into plane waves, but it is the case that any smooth function that does not blow up can be. Mathematically, "blow up" means that the norm of the function, or the inner product of the function with itself, is finite.

```math
\int_{-\infty}^{\infty}|f(x)|^2\,dx<\infty.
```

Physically, such a function is a **wave packet**. Expressing an arbitrary wave packet as a superposition of its modes is called **Fourier decomposition** and the transformation from an amplitude over translation coordinate to amplitude over wave number coordinate is called a **Fourier transformation**.

[move this to after unitarity ?]
Because nature has time and space translational symmetry, any **free**, or non-interacting, system described as a wave packet retains its Fourier composition over time and space. As we move on to discuss **fields**, or functions over space and time, localized objects will be treated as special cases of wave packets. The through line of the story we want to tell is this: nature's symmetry requires that the world is "musical," that is, that its most elemental constituents are "tones," and that all the complexities that unfold over time are the manifestation of the composition of those tones. Sip some herbal tea, grab your crystals, and ponder -- the unfolding of nature in time is, decomposed into its Fourier modes, a timeless "chord."
[move this to after unitarity]


#### Unitarity - Waves in Physics
...relate L2 functions to unitarity (don't blow up)...
...relative phase...
...identity...

...1. say we need identity 2. say waves give us this. 3. talk about what would happen to a wave packet in molasses and compare to a packet in an ideal medium. 4. talk about deterministic particle trajectories, and about incompressible fluid 5. unitarity 4 ways -- metrics and forms -- intuitive waves -- relative phase -- sine and cos components...

In the function representation of translation symmetry, which is called a **Hilbert space**, the symmetry transformation is carried out by a **unitary** operator, which is to say an operator that preserves the inner product (a generalized dot product) of functions.

```math
\langle Uf,Ug\rangle
=
\langle f,g\rangle.
```

### Commutators
In the case of a single continuous symmetry transformation, knowing the generator specifies any transformation, but in the case where there are multiple independent transformations that can be composed, the order of the composition must also be taken into account because it produces different resultant states. For example, in the 3-dimensional rotation group, or $SO(3)$, rotating about the $x$-axis then the $y$-axis leaves a sphere in a different state than applying the same actions in the opposite order.

![Noncommuting 90-degree rotations in three dimensions](animations/symmetry-so3-rotation-order-contact-sheet.png)

[Open MP4: symmetry-so3-rotation-order.mp4](animations/symmetry-so3-rotation-order.mp4)

This dependency on order is encoded in terms of the generators by the **commutator**:

```math
[X,Y]
=
XY-YX.
```

For example, for $\mathfrak{so}(3)$, the commutators are:

```math
[J_x,J_y]=J_z,
\qquad
[J_y,J_z]=J_x,
\qquad
[J_z,J_x]=J_y.
```

The generators and commutators together determine any transformation in the complete symmetry group.

We should say that there is some global structure, the **topology**, that remains invisible to the local generators and commutators. For example, translation in $x$ and $y$ commute (moving in $x$ then $y$ is the same as $y$ then $x$), but this is true both on the surface of a plane and a cylinder, which have different global behavior: on a cylinder, a translation may return a point back to its starting point. This is familiar to anyone who has played Asteroids.

![A cylinder unrolls into an arcade-style wraparound plane](animations/symmetry-cylinder-topology-wrap-contact-sheet.png)

[Open MP4: symmetry-cylinder-topology-wrap.mp4](animations/symmetry-cylinder-topology-wrap.mp4)

Using the commutator we can generate composed actions.

```math
e^{aX}e^{bY}
=
e^{aX+bY+\frac12ab[X,Y]+\cdots}.
```

This identity comes from using the definition of the commutator and Taylor expanding the exponentials. We will spare the reader the algebra.

#### Why Generators and Commutators?
Up to this point, we have said that if we know a transformation matrix, we can find the generators by finding the tangent at the identity, that is, where the transformation parameter equals zero. Then we've said we can exponentiate the generators along with their commutators to find the transformation. But wait, this is just going in a circle, what have we gained from identifying the generators and their commutation relations? 

Because the generators live in a tangent plane rather than on a a curved space, they can be linearly combined. For example, if we can write the generator of 3-dimensional rotation about an arbitrary axis as a linear compbination of rotation about the $x$, $y$, and $z$ axes:

```math
L_{\hat{\mathbf n}}
=
n_xL_x+n_yL_y+n_zL_z,
\qquad
\hat{\mathbf n}=(n_x,n_y,n_z).
```

We can then find a finite rotation about this axis by exponentiating $L_{\hat{\mathbf n}}$. By comparison, if we only new the matrices for finite rotations about each axis, we would have to multiply those matrices. While this is computationally advantageous, it is essential for finding identities that would otherwise be opaque in matrix multiplication. For example, if we can construct an operator from the generators that commutes with all the generators, we know that operator is an invariant under the symmetry. As an illustration, in 3-dimensional rotation we can see that the square of the rotation generators is invariant:

```math
[L_x,L_y]=L_z
\quad\text{(cyclically)},
\qquad
L^2=L_x^2+L_y^2+L_z^2,
```

```math
\begin{aligned}
[L^2,L_x]
&=[L_y^2,L_x]+[L_z^2,L_x]\\
&=L_y[L_y,L_x]+[L_y,L_x]L_y
+L_z[L_z,L_x]+[L_z,L_x]L_z\\
&=-L_yL_z-L_zL_y+L_zL_y+L_yL_z\\
&=0.
\end{aligned}
```

By the same calculation,

```math
[L^2,L_y]=[L^2,L_z]=0.
```

An invariant constructed this way is a **Casimir operator**, and Casimir eigenvalues are crucial in physics because their combined values classify representations of a symmetry. For example, as we will see later, the invariant mass of a particle is the eigenvalue of a Casimir operator built from the generators of time and space translations. In fact, the particles familiar from the Standard Model are classified by combinations of Casimir eigenvalues of the symmetries they represent. To say this again, in the **Standard Model**, particles are modeled using representations of symmetry, and the Casimir eigenvalues identify the representation to which a particle state belongs.

Generators have a clear physical interpretation. They are the familiar conserved quantities associated with free motion. For example, momentum generates translation, and if a system's translational symmetry is unbroken, **momentum** is conserved. Similarly, angular momentum generates rotation, and if a system posseses rotational symmetry, angular momentum is conserved. The momentum component that generates time translation has a name that is as common as its meaning is rich  -- **energy**.

#### The Symmetry Generators of Physics
As we have said nature includes translation symmetry in time and position, rotational symmetry, and velocity boost symmetry. This group is lives in a complex function representation. In addition, in quantum theory, the complex phase of function representations will be seen to be an extra symmetry as it will be not appear in observables, which are encoded into the complex norm of the representing function, where phase cancels. This extra symmetry is not one of time and space, but rather lives in its own fiber on each point in time and space. Such a construction is called a **fiber bundle**. 

[insert fiber bundle diagram] 

In the full Standard Model, each fiber may have several indepenpendent components.

#### Canonical commutator
In addition to all the palpable symmetry of nature and the fiber bundle structure that arises from the complex function representation, there is another symmetry group with altogether different and pivotal importance. This is symmetry group that stands behind Fourier transformations, known better by its commutator name than the symmetry group, the **canonical commutation relation**. Once we choose a complex wavefunction representation, one set of operators (for translation in $x$, $y$, $z$, and $t$) on the function space act to produce shifts in position and time. But a different set of operators produce shifts in wave number, and these operators do not commute. This failure to commute is not hard to show algebraically, but we will omit it. The effect of the commutator, that is, of shifting a wave in position, then in momentum, the completing the loop by undoing each operation, is to shift the phase of the wavefunction. 

```math
(T(a)\psi)(x)=\psi(x-a),
\qquad
(M(b)\widetilde\psi)(k)=\widetilde\psi(k-b).
```

Choosing the $x$-representation, the translation in $k$ becomes multiplication by a phase:

```math
(M(b)\psi)(x)=e^{ibx}\psi(x).
```

```math
T(a)M(b)T(-a)M(-b)
=
e^{-iab}I,
\qquad
[X,K]=iI.
```

The infinitesimal commutator can be exponentiated to obtain the finite phase advance:

```math
e^{-ab[X,K]}
=
e^{-iab}I.
```

So that:

```math
\left(e^{-iab}I\right)\psi(\bar{x})
=
e^{-iab}A e^{i\bar{k}\cdot\bar{x}}
=
A e^{i(\bar{k}\cdot\bar{x}-ab)}.
```

![Weyl order phase animation contact sheet](animations/differential-weyl-order-phase-contact-sheet.png)

*Applying position and wave-number shifts in opposite orders leaves a residual phase. The animation compares the inverse ordering, and therefore displays $e^{iab}$ rather than $e^{-iab}$.*

[Open MP4: differential-weyl-order-phase.mp4](animations/differential-weyl-order-phase.mp4)

We can write the phase of a wavefunction in terms of the time and position translation generators.

```math
\psi_{\mathbf k,\omega}(\mathbf x,t)
=
A e^{i(\mathbf k\cdot\mathbf x-\omega t)},
\qquad
-i\nabla\psi=\mathbf k\psi,
\qquad
i\partial_t\psi=\omega\psi.
```

$[X,K]$, then, tells us how phase advances, when applying the $\hat X$ and $\hat K$ operators interact when applied sequentially. But what does this mean? What does it mean to "apply the $\hat X$ operator" other than what we can say here, in the math itself, which is to transform the wavefunction along the $k$ axis. Because time and position translations commute, waves free state is to translate along $x$. However, waves do not freely change wave number over time. Thus "translation in wave number" doesn't freely happen over some time, making it yet harder to say what "applying the $\hat X$ operator" means.  


In quantum mechanics, indeed in wave mechanics in general, the information the wave carries is determined by the relative phases of its components. Shifting $k$ (or $x$ in the position representation) changes these relative phases, and the $[X,K]$ commutator tells us how a shift in $k$, and then in $x$ changes the shape of the wave function. But what, in practice, in physics, does it mean to shift the symmetry transformation's parameter? This is subtle. It is tempting to think that as a system evolves in time it is transformed along some symmetry. And this may we be the case if that symmetry is a symmetry of the system, such as transformation in position for a free particle. But a free wave certainly does not transform in $k$ space over time. The key to understanding the role of the commutator is to understand that the transformations are *hypothetical*. What we will see in a later is that path a system takes in time is the one for which some function on the path is **extremized**, that is, that it is minimized, maximized, or otherwise has a vanishing first derivative. To find the actual, physical path, we consider alternate paths between the same endpoints and ask how much they vary from alternate "wrong" paths. For a wave, as we will see later, this function is precisely the phase advance, and we can see how how rapidly the phase advance changes between candidate path by tiling the area they enclose with infinitesimal loops that contribute the value of the coummator. 

![A path variation tiled by local commutator loops](animations/symmetry-ccr-action-variation-contact-sheet.png)

[Open MP4: symmetry-ccr-action-variation.mp4](animations/symmetry-ccr-action-variation.mp4)

What have we said? That for travelling wave packets, the commutator encodes the actual, physical evolution of the packet. Once we have this, we can find the differential **equations of motion** which can be integrated to find the physical path, thus providing an alternate way to arrive at the real path. However, given the position and wave number generators and their commutator, we can directly derive the equations of motion without working out the **variational** procedure, as they are, precisely, the local measure of phase variation.

So much for waves, but why obsess about waves, or wave packets, or wavefunctions. The reason, which some may have guessed, is that in quantum mechanics, or we could say "the best mechanics we know," there are no particles or rigid objects with definite positions, but only probabilities of position and momentum measurements, which are encoded into a wavefunction. Thus in quantum mechanics the canonical commutation relation (CCR) along with the position and momentum (which is associated with wave number through Planck's constant, or $\hbar$) tells us the form of the equations of motion for *any* quantum system. 

...table of definitions...
...close...
