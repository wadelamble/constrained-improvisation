# Symmetry

## outline and notes

### Starting program

1. Take a shape.
2. Build out a mathematical vocabulary to describe its symmetry:
   - transformations,
   - invariants,
   - representations,
   - groups,
   - operators,
   - states.
3. Move to continuous symmetry:
   - rotation,
   - translation,
   - boost.
4. Add Lie vocabulary:
   - Lie group,
   - parameter,
   - generator,
   - commutation,
   - anticommutation,
   - function representations
   - waves as representations.
   - operators
   - eulers identities
5. Move to symmetries of nature:
   - the "pool table if moved over a foot" intuition,
   - equations of motion must keep the same form under translation, rotation, boost, and internal transformations for fields.

### Useful modifications / guardrails

- Keep the ordinary meaning of symmetry first: triangles, snowflakes, circles, lines.
- Distinguish the object from its symmetry group. The group is the set of transformations, not the shape itself.
- Introduce invariants early. A symmetry only means something once we say what remains unchanged.
- Use the triangle for discrete symmetry, then the circle for continuous symmetry.
- Use "discrete," not "discreet."
- The rotation group of the circle/plane should be \(SO(2)\), not \(SO(1)\).
- For the point \((\cos\theta,\sin\theta)\), the tangent is \((-\sin\theta,\cos\theta)\), not \((\sin\theta,\cos\theta)\).
- Let boosts enter as part of the ordinary inertial-frame intuition: the sealed train / moving pool table.
- Momentum as generator of translations can be introduced conceptually here, but the full physical definition of momentum should wait for action / Hamiltonian mechanics.
- Plane waves should be framed as the basis adapted to translation symmetry, not merely as a Fourier convenience.
- A commutator is the order-defect of infinitesimal transformations:

$$
[A,B]=AB-BA.
$$

- For rotations, use the schematic relation

$$
[L_x,L_y]\sim L_z,
$$

with conventional factors such as \(i\) and \(\hbar\) supplied later.
- For exponentials, do not write naive composition as though

$$
e^A e^B = e^{A+B}
$$

unless \([A,B]=0\). The Baker-Campbell-Hausdorff expansion begins

$$
e^A e^B
=
\exp\left(A+B+\frac{1}{2}[A,B]+\cdots\right).
$$

- Anticommutation should be introduced only as vocabulary unless there is a clear reason to go deeper:

$$
\{A,B\}=AB+BA.
$$

- Internal symmetry should be introduced as transformations of field values rather than movements through spacetime. A simple example is a global phase rotation:

$$
\psi(x)\mapsto e^{i\alpha}\psi(x).
$$

## existing material

### Opening: ordinary symmetry and translation intuition

When we say "symmetry," we really mean symmetry, like, you know, triangles, snowflakes, etc. The math for the symmetry of continuous spaces with coordinates is an outgrowth of the math for the symmetry of shapes. So let's take a bit of time to learn about the mathematical treatment of symmetry.

Before we dive into symmetry as such, let's clarify this odd idea that "picking up your experiment and moving it over there" constitutes a "symmetry." It's not obvious what this means. Consider the line simply as a shape and assume it has infinite length. Can you see the difference when we move it left or right? No. Thus the shape itself is symmetric with respect to translations.

[Diagram: Figure 1 - The symmetry of a line. Source image: `image1.png`.]

The "sameness" of the physics when our experiment is translated along a given dimension is treated in the same way as the sameness of the line shape. The symmetric action is translation, and the shape of a line and physical behavior both realize translational symmetry.

### Discrete symmetries

When we work through the concepts of particle classification in quantum mechanics, we will throw around terms that can seem abstract or opaque, but which we can build up to from simple examples of symmetry. Let's start with examples of shapes with discrete symmetries. The humble equilateral triangle is a suitable example. We can see at a glance that it has symmetries, for example rotating by 120 degrees. We can also see that the characteristic symmetries of triangles are present in other "triangly" objects.

[Diagram: Figure 2 - Triangly things. Source images: `image2.png`, `image3.png`, `image4.png`.]

There is a menagerie of shapes that have the same symmetries, but what are the symmetries? How do we define them without drawing more shapes? Let's try. If you rotate the triangle a little bit, it does not look the same. That is not a symmetry.

[Diagram: Figure 3 - Rotating a little bit is not a symmetry. Source images: `image5.png`, `image6.png`.]

But what if we rotate it by 120 degrees? Or 240 degrees? Those do make the shape look the same. And what if we flip along an axis going from one vertex and bisecting the opposite side? That is also a symmetry.

[Diagram: Figure 4 - Rotation and flip symmetries. Source images: `image7.png` through `image15.png`, with `image12.png` repeated.]

### Symmetry group, invariant, and generators

There are six total symmetries: three rotations and three flips. These actions form a **symmetry group**. We should pause here to stress something. The symmetry group is not the group of triangly things, but the group of actions that preserve the symmetry of the triangly things. For what it's worth, this particular group is called \(D_3\), the dihedral group of order six. Whoa.

Whenever we have a symmetry, we must have some **invariant**, some way of defining what we mean by "is the same." For triangles, one way to express the invariance is that vertices are always at the same location. This may seem pedantic, but it becomes all-important when we work in a coordinate space, where the invariant becomes a number whose value classifies objects.

We can build up the symmetry-preserving actions of \(D_3\) from two actions: rotation by 120 degrees and flipping along one axis. These building-block actions are **generators**.

### Representations

At this point, we need to take a bit of a conceptual leap. We can map the objects groups act on to vectors in a vector space and the group actions to matrices that transform the vectors. Once we do this, we can "do linear algebra" on symmetry groups, and that, in a sense, is the plot setup for modern physics: physical behavior is the symmetric thing, and the map onto linear algebra allows us to unpack the story in numbers.

So, let's try it with the triangle. We can represent a triangle as a vector as follows:

[Diagram: Figure 5 - Triangle A, B, C -> vector \([A,B,C]\). Source images: `image16.png` through `image20.png`.]

Now let's say we want to take vertex A to vertex B, leaving C alone. We do that by multiplying the triangle-vector with the rotation matrix:

$$
\begin{bmatrix}
0 & 1 & 0 \\
1 & 0 & 0 \\
0 & 0 & 1
\end{bmatrix}.
$$

We call a particular linear algebra version of the group a **representation**. It is important to note that different vector representations may correspond to different objects. For example, a more complex shape with \(D_3\) symmetry may require a higher-dimensional vector to represent it, but that vector space is still a representation of \(D_3\).

What if we instead put our triangle in a 2D plane and rotate it?

[Diagram: Figure 6 - Rotate a triangle in 2D space while keeping track of the vector corresponding to one vertex. Source images: `image21.png` through `image34.png`, with `image12.png` repeated.]

Our triangle is now represented by the single vector

$$
\begin{bmatrix}
0 \\
1
\end{bmatrix},
$$

with the other vertices implied. We can rotate it 120 degrees with the matrix

$$
\begin{bmatrix}
\cos(120^\circ) & -\sin(120^\circ) \\
\sin(120^\circ) & \cos(120^\circ)
\end{bmatrix}.
$$

We could construct matrices in this space that also represent flips. This representation is a subspace of our previous representation and realizes the same symmetry actions. When we have such a space that does not have any lower-dimensional subspace that represents the group, we call this an **irreducible representation**, or **irrep**.

These concepts -- group actions, invariants, generators, representations, and irreducible representations -- in the context of triangles may seem out of left field, but they turn out to be building blocks of quantum mechanics.

### Continuous symmetries: the circle

Many of the concepts from symmetry in physics require us to deal not with discrete symmetries like triangles exhibit, but with continuous symmetries such as circles. Recall that rotating a triangle a little bit did not preserve the symmetry. On the other hand, rotating a circle by any amount is a symmetry-preserving action.

[Diagram: Figure 7 - Any amount of rotation preserves the symmetry of a circle. Source images: `image35.png` through `image49.png`.]

The circle has an infinite number of group actions corresponding to rotation by any angle.

[Technical note: the original says "SO(1)." For rotations of the plane/circle, the intended group is likely \(SO(2)\).]

This group's invariant is easier to define than the triangle's. It is simply the length of any vector from the origin:

$$
\sqrt{x^2+y^2}=\text{const}.
$$

What is the generator of rotations? It is an infinitesimal rotation. A general principle of geometry is that everything is flat when you zoom in far enough. Since "infinitesimal" is fully zoomed in, such a rotation is "flat," that is, it is a tangent vector.

[Diagram: Figure 8 - Tangent vectors generate rotations. Source images: `image50.png`, `image51.png`, `image52.png`.]

And what is the tangent to a circle? We can label any point on the circle as

$$
\begin{bmatrix}
\cos\theta \\
\sin\theta
\end{bmatrix}.
$$

As every calculus student learns, the tangent vector of any function is the derivative of the function. Thus the tangent is

$$
\begin{bmatrix}
-\sin\theta \\
\cos\theta
\end{bmatrix}.
$$

[Technical note: the source had the first component as \(+\sin\theta\); the derivative of \(\cos\theta\) is \(-\sin\theta\).]

[Diagram: Figure 9 - Labelling a point on the circle and the tangent vector with sine and cosine functions. Source images: `image53.png` through `image58.png`.]

So what is the generator of rotations? Thinking back to the triangle, the generator was the action of rotating 120 degrees. Here our action is a function that labels the circle at every point. What performs that action? It is

$$
\frac{d}{d\theta}.
$$

This is an **operator**. Since a function has values at every point, it is equivalent to an infinite-dimensional vector, and an operator is equivalent to an infinite-dimensional matrix that maps one infinite-dimensional vector to a new one.

### Momentum as generator of translations

Physicists are fond of saying that momentum "generates" translations and, poetically, energy generates time, a phrase worth meditating on. We can now see what this means in terms of symmetry.

As we discussed above, translation is a symmetry. In notation, we would define translation as an operation that takes a vector and shifts it:

$$
x\mapsto x+a.
$$

If this is a symmetry, it must fulfill the requirements of a symmetry group:

1. If we translate by \(a\), then by \(b\), translating by \(a+b\) is still a translation.
2. If we translate by \(a+b\) and then by \(c\), that is the same as translating by \(a\), then by \(b+c\).

These relations are super obvious for translations. The point in saying them out loud is that we have not yet said how to **represent** translational symmetry, that is, how to express it in some linear algebra space. The most obvious representation is for a single point in a single dimension:

$$
T(a)=x+a.
$$

Here \(T(a)\) is the translation operator.

This is fine, but what if we have a system with multiple objects at different coordinates and we want to "pick up and move" the system? Then we need a representation that can carry this structure. We can do this with vectors and matrices in two dimensions:

$$
\begin{bmatrix}
1 & 0 & a \\
0 & 1 & a \\
0 & 0 & 1
\end{bmatrix}
\begin{bmatrix}
x_1 \\
x_2 \\
1
\end{bmatrix}.
$$

[Technical note: this matrix as written translates both coordinates by the same \(a\). If the intent is ordinary 2D translation, it may later want separate parameters \(a_x,a_y\).]

But what if we have three objects in our system? Or what if we have a whole field with infinitely many points, like waves on a pond? To fully represent our physical system, we need to represent the symmetry in function space:

$$
[M]
\begin{bmatrix}
x_1 \\
x_2 \\
\vdots \\
x_\infty
\end{bmatrix}.
$$

Or, in its more normal form:

$$
\widehat O(f(x)),
$$

where \(\widehat O\) means some operator that acts on \(f(x)\), such as

$$
\frac{d f(x)}{dx}.
$$

Recall that the infinite-dimensional vector form of the function means the value of \(f(x)\) at every \(x\).

### Translation in function space

In this representation, we can think of the symmetry action as shifting a function.

[Diagram: Figure 10 - Shifting a function by an amount \(a\). Source images: `image59.png` through `image74.png`.]

Another way to say this is that if we have translational symmetry in a dimension and some function on the dimension, if we move from one location to another, we can leave the function the same and just slide the coordinate system.

We know that continuous symmetries have generators that act to produce an infinitesimal shift. Let's try to find that generator for translations. We know from calculus that we can Taylor expand any function as

$$
f(x+a)
=
f(x)
+a\frac{df(x)}{dx}
+\frac{a^2}{2!}\frac{d^2f(x)}{dx^2}
+\cdots
=
e^{a\frac{d}{dx}}f(x).
$$

Very briefly, this is saying that if you know the value of a function at one point and all the derivatives of the function -- how fast it changes, how fast its change changes, and so on -- you can find the value of the function at nearby points, and in good cases at other points.

In any case, we have now found the translation operator:

$$
T(a)=e^{a\frac{d}{dx}}.
$$

[Technical note: the source had \(d/ax\); this is almost certainly \(d/dx\). Sign convention depends on active vs passive translation.]

Doing a bit more calculus, we can say that if \(a\) is an infinitesimally small shift, we only need the first two terms of the expansion, as the remaining terms get small faster than \(a\) does. We then have

$$
f(x+a)=f(x)+a\frac{df(x)}{dx}
$$

for infinitesimal \(a\).

We then have our generator of translations:

$$
\widehat a f(x)
=
a\frac{df(x)}{dx}
\quad\Rightarrow\quad
\widehat a
=
a\frac{d}{dx}.
$$

### Plane waves and wave packets as representations

Once we choose \(a\), we can find the **eigenfunctions** of the operator. An eigenfunction is a function that only changes by a scale factor when the operator acts on it. This is analogous to the way an axis is an eigenvector of rotation: no matter how much you rotate, the axis stays the same. No matter how many times you differentiate, the function maintains its shape. The eigenfunction will be of the form

$$
f(x)=e^{ax}.
$$

[Diagram: Figure 11 - Plots of plane waves and real exponentials; plane waves are symmetric. Source images: `image75.png` through `image94.png`.]

If we choose \(a\) to be real, our eigenfunctions grow without bound. These can encode the symmetry, but they do not retain their shape over \(x\) in the bounded/oscillatory sense we want.

Functions of the form

$$
e^{ikx}
$$

are complex plane waves. Their real components are sinusoidal waves. Keeping in mind that our plane wave extends to infinity in both directions, we can see that shifting it left or right has no impact on its shape. This is the essence of saying it represents translational symmetry. Algebraically:

$$
T(a)e^{ikx}=e^{ika}e^{ikx},
$$

up to the sign convention for \(T(a)\). The factor \(e^{ika}\) is just a phase factor.

Because a complex wave lies on a cylinder of constant radius, changing the phase does not change the length. Thus the amplitude at any point is unaffected by translation. When we talk about quantum mechanics and bodies as probability distributions, probability will be associated with amplitude. The fact that the translation operator does not affect amplitude will imply that it does not affect probability. This probability-preserving property is called **unitarity**.

A single plane wave is just one vector in a vector space of wave-like things. Because plane waves are eigenfunctions, they form a basis for an infinite-dimensional space of wave-like things, or wave packets. Any superposition of plane waves is a vector in this space. A unitary operator is a rotation of this space. Thus it preserves the amplitude of any wave packet.

These properties are wrapped up in the statement that a unitary operator preserves the inner product:

$$
\langle Uf,Ug\rangle=\langle f,g\rangle.
$$

What are the "wavy things" that live in this space? They are functions that look like wave packets and do not blow up.

[Diagram: Figure 12 - Examples of functions that can be composed from plane waves. Source images: `image95.png` through `image103.png`, with `image65.png` repeated.]

This composition of wave packets in a basis of plane waves, along with the unitarity of the translation operator, is the basis of Fourier analysis, which allows transformation between position and momentum representations: between wave packets and their decomposition in terms of pure plane waves.

It is worth stepping back and appreciating this bit of math. We have combined complex numbers, calculus, exponential functions, curvature, and flatness to show how observable, instinctive symmetry leads to dynamical, conserved physical quantities, all with no reference to any particular coordinate system.

### Momentum

The equation

$$
\widehat a(f(x))
=
a\frac{df(x)}{dx}
$$

is valid for any value of \(x\). Thus, when we act with it, we move to a new value:

$$
x\mapsto x+a.
$$

The equation still holds. Therefore, the eigenvalue \(a\) does not change as we move along a symmetry. Thus, we associate the role of \(\widehat a\) as the generator of spatial translation with \(a\) as a conserved quantity when there is spatial symmetry.

Replacing our generic \(a\) with the normal symbol for momentum \(p\), the source has

$$
\widehat p
=
i\frac{d}{dx}
\quad\Rightarrow\quad
\widehat p(f(x))=p f(x).
$$

[Technical note: in quantum mechanics the usual convention is \(\widehat p=-i\hbar\,d/dx\). Without \(\hbar\), the generator is often \(-i\,d/dx\).]

In a system with more than one body in a symmetric space, interactions between bodies may change the total velocity vector, but they preserve the total center-of-mass momentum vector. When we say in high school physics that two billiard balls colliding conserve momentum, we are saying that the eigenvalue of the translation operator is conserved.

Interestingly, we have defined momentum with no mention of mass, and yet we learn very early in physics that

$$
p=mv.
$$

Assuming \(v\) is fundamental as the expression of "motion" itself, does this mean that mass is not fundamental, that it somehow arises from symmetry? The source answers yes, with the note that this must wait until spacetime and relativity.

[Structural note: keep this as a teaser. The fuller definition of momentum belongs later, after action/endpoint variation and Hamiltonian mechanics.]

### Commutation

When you move around the world, you compose different degrees of freedom of symmetry, such as up/down, left/right, and rotation. Where you end up depends on the order in which you combined the motions. The simplest example is that rotations do not commute: the order of motions matters.

The source writes:

$$
\left[L_{x_i}L_y\right]=L_z.
$$

[Technical note: likely intended as \([L_x,L_y]\sim L_z\), with conventional \(i\) and \(\hbar\) factors supplied later.]

This says that if you compare rotating in \(x\) then \(y\) to rotating in \(y\) then \(x\), the difference is a rotation in \(z\), which you can convince yourself of by rotating a book.

The commutator measures the difference given by reversed order of application:

$$
[F,G]=FG-GF.
$$

The commutator is thought of as an expression of the overall shape, or curvature, of the symmetry: the actual difference in order of operation, shrunk to tiny, flat steps.

The commutator comes up again and again in quantum mechanics, which is framed in terms of symmetry. It can be confusing that some explanations begin with the commutator. But once you realize that the commutator and the generators themselves come from the same place -- the shape of the symmetry -- you see that it gives you an alternate mathematical formulation of the symmetry.

A Lie algebra relation has the form

$$
[A_i,A_j]=\sum_k c_{ij}^{\ k}A_k.
$$

When the symmetry is represented and given a basis, these equations amount to matrix equations that define the symmetry from a linear algebra perspective.

The general exponential form is

$$
g(\alpha)=\exp(\alpha^aG_a).
$$

To move around in a symmetric world by an amount \(\alpha\), you exponentiate an \(\alpha\)-worth contribution from each symmetry's generator.

#### Technical fixes to preserve

- Use

$$
[L_x,L_y]\sim L_z,
$$

not \([L_{x_i}L_y]=L_z\).
- The BCH leading commutator term is

$$
\frac{1}{2}[A,B],
$$

not \(2[A,B]\).
- Do not write

$$
f(\alpha)\circ g(\alpha)=\exp(F+G)
$$

as a general law. Composition of exponentials is governed by BCH, not by the naive law of exponents unless \([F,G]=0\).

### From symmetry to geometry

We live in a space that we feel in our bones. Up, down, left, right. Knowing this space, we immediately know what symmetries to expect, in the sense that things behave the same under symmetric transformations. Pick up your experiment and take it over there: nothing changes. Put it on a train: nothing changes.

If one were to try to pin us down on how we define this space we intuitively know so well, one answer, maybe the only answer, is precisely to move our experiment around to establish our space's symmetries. And that becomes the definition of our space.

As a bonus from defining space this way, we get a recipe for developing a coordinate system that maps symmetry transformations. These transforms allow us to make predictions, which validate our original assertions about the symmetry. One can guess at the symmetries, work out their coordinate transformations, and test whether the guess was correct.

Let's try to get an overview of this mathematical procedure for going from symmetry to geometry. We have already defined symmetry in two ways: the ways you can arrange a shape that leave it invariant, and the ways you can move a physical system, like a billiard table, and leave it invariant in terms of physical behavior.

Geometry is the rules governing angles and distances. Everyone knows the angles of a triangle add up to 180 degrees. But on a sphere they add to more than 180 degrees, and on a hyperboloid they add to less than 180 degrees.

[Diagram: Figure 13 - Sum of triangle interior angles with curvature. Source image: `image104.png`.]

[Source fragment: "Likewise, distances depend on a space's symmetries. This may seem" trails off.]

But, you may object, a sphere is just an object sitting in a space where the angles in a triangle add to 180 degrees. That is true, and it leads to one of the fundamental things that "following the math" tells us about the world: spaces can have curvature intrinsically without being embedded in another space.

How would you know you lived in curved space without looking down on it from some higher-dimensional space? Math offers a rigorous answer. If you carry an arrow and hold it straight as you walk, once you complete a loop the arrow will point in a different direction than it did when you began. How different it is tells us the space's curvature.

[Diagram: Figure 14 - Measuring curvature with parallel transport. Source image: `image105.png`.]

This may be difficult to visualize, but the important point is to convince yourself that if a flat insect's entire universe were confined to the surface of the Earth, it could still tell it lived on curved space, even as each small patch seemed flat.

Our job is to take the symmetries that we discover through experiment or intuition, discover the shape that carries that symmetry, and then write down the geometry for a world that exists within that shape. Since physical symmetries are continuous -- we can move our experiments by any amount -- we want to apply the basic idea of calculus to our space.

We want to say: if we parallel transport along a tiny loop and probe the shape of our space, because the space is symmetric, we can act with those tiny motions over and over and get a predictable result, which we express through exponentiation. The equations that encode the parallel-transport behavior around a tiny loop are just the commutation relationships:

$$
[A_i,A_j]=\sum_k c_{ij}^{\ k}A_k.
$$

Each \(A_i,A_j,A_k\) is a step in a given direction corresponding to the dimension of the symmetry group. For example, there are three generators for rotating a sphere.

### Symmetry to stage

Our first step is, given our symmetries, to construct the stage, or base space, on which these symmetries act. We do this by "dividing" the full symmetry space by the symmetries that leave an origin fixed, namely rotations. This quotient space establishes the notion of a space of points that one can move around in via translations:

$$
M=\frac{G}{H},
$$

where \(M\) is some physical stage, \(G\) is the full symmetry group, and \(H\) is the stabilizer group that leaves an origin unchanged. This gives us what mathematicians call a coset, a set of points in space.

This shrinks all the rotation and boost symmetries down to a point. That is, it says to think of the rotation symmetries as a person turning rather than the world turning. Then you can package all rotations into an observer, leaving only the translation operators.

The way that the translation operators change when an observer rotates -- boosts are rotations too -- spells out a kind of flow. For example, if in this flow, when you turned, you got swept away quickly, that would imply a symmetry in which physical behavior would dictate that our reading of time and space coordinates gets swept away, and with it our reading of momentum. This is pointing toward relativity's understanding of spacetime.

Under this flow, we can identify the thing that stays the same when we rotate and translate, in terms of the separation of two points. How to measure the invariant separation is the idea of dot product, or more generally inner product. It need not always be a length as we think of it. It only needs to reflect the flow corresponding to the symmetry. Once we have this inner product, we can define a coordinate system and a way to measure curvature. At that point, we are ready to do physics with rulers and clocks.

How does one go from an understanding of a system's symmetries to a testable, quantitative formulation of physical behavior? At its most basic level, that quantification is the path an object follows:

$$
x(t).
$$

But who is saying what this path is? If I am looking at a star 50 trillion miles away from me and turn half a turn to put the star behind me, it did not suddenly travel 100 trillion miles, but \(x(t)\) did change that much. In order to write \(x(t)\), we must specify an observer and that observer's orientation. Once we have done so, we have a frame of reference.

Different frames of reference are a reflection of physical symmetry: the fact that all frames of reference agree on physical behavior is what we mean by symmetry. Not all observers will agree on physical behavior. If one were to try to play pool on a train car oscillating back and forth, the behavior of pool balls would be unrecognizable. The frames of reference we have in mind are precisely those in which physical behavior does not change.

Now, identifying an observer and writing \(x(t)\) for that observer is just a starting point. In order to capture "that behavior all frames agree on," we must have a way to transform "my" \(x(t)\) to "your" \(x(t)\). If I am here, facing north, going 10 mph, and you are there, facing east, going 20 mph, then for every \(x\) from my perspective, I must have a way to map that to an \(x\) from your perspective.

Since that transformation must be done such that the physical behavior stays the same, the transformation must at least leave something the same. This is just the idea that a symmetry must have some invariant, but now that invariant must be expressible in coordinates.

Let's give ourselves two rigid rods. When we rotate, we plainly see that the rod lengths stay the same and the angle between them stays the same.

[Diagram: Figure 15 - Lengths and angles do not change under rotation. Source images: `image106.png` through `image109.png`.]

### Dot product and metric

How can we capture this in coordinates? The tried-and-true answer is the dot product. We take the vertex of our rods, place that at the origin, treat each rod as a vector, and calculate, for example in two dimensions:

$$
\langle v_1,v_2\rangle
=
\begin{bmatrix}a & b\end{bmatrix}
\begin{bmatrix}c \\ d\end{bmatrix}
=
ac+bd.
$$

[Diagram: Figure 16 - Visualization of dot product. Source images: `image110.png` through `image115.png`, with `image110.png` repeated.]

Note that a vector dotted with itself gives its length squared, so for a single vector the dot product encodes the invariance of its length. We could write this differently as

$$
\langle v_1,v_2\rangle
=
\begin{bmatrix}a & b\end{bmatrix}
\begin{pmatrix}
1 & 0 \\
0 & 1
\end{pmatrix}
\begin{bmatrix}c \\ d\end{bmatrix}.
$$

Here the identity matrix is doing nothing. But what if it were not the identity matrix? What meaning would that have?

We have to allow our imaginations to roam a bit. Suppose we live in a world where, if we are holding a stick and rotate, the stick grows; that is, \(\langle v_1,v_2\rangle\) gets larger. We can further imagine it grows to infinity as we turn, and we can never turn all the way around. Some unseen resistance builds as our stick approaches infinity.

Clearly we did not choose \(\langle v_1,v_2\rangle\) correctly, for it is not invariant. But we can fix this by changing our identity matrix above to a different **metric**. There is a metric matrix that works for the symmetry just described:

$$
\langle v_1,v_2\rangle
=
\begin{bmatrix}a & b\end{bmatrix}
\begin{pmatrix}
-1 & 0 \\
0 & 1
\end{pmatrix}
\begin{bmatrix}c \\ d\end{bmatrix}.
$$

This is the metric \((-+)\) for hyperbolic symmetry. Imagine sliding a vector along a hyperbola. Its length grows from our accustomed perspective. But we could define the invariant inner product this way, and then say: when you rotate and measure some physical system, you have to transform your measuring stick this way in order for the physical behavior to look the same.

Here we worked from the metric to the symmetry, but we can go the opposite direction and, with careful consideration, work from the symmetry to the metric.

## rewrite
When we say "symmetry," we really mean symmetry, like, you know, triangles, snowflakes, etc. The math for the symmetry of continuous spaces with coordinates is an outgrowth of the math for the symmetry of shapes. So let's take a bit of time to learn about the mathematical treatment of symmetry.

Before we dive into symmetry as such, let's clarify this odd idea that "picking up your experiment and moving it over there" constitutes a "symmetry." It's not obvious what this means. Consider the line simply as a shape and assume it has infinite length. Can you see the difference when we move it left or right? No. Thus the shape itself is symmetric with respect to translations.

[Diagram: Figure 1 - The symmetry of a line. Source image: `image1.png`.]

The "sameness" of the physics when our experiment is translated along a given dimension is treated in the same way as the sameness of the line shape. The symmetric action is translation, and the shape of a line and physical behavior both realize translational symmetry.

## Symmetry
Strike a pool ball with a cue, and the balls move in an expected way. Move the table over a few feet, and the balls move in recognizably the same way. Wait a few minutes, and the balls move in the same way. Turn the pool table a few degrees, and the balls still move the same way. Put the pool table on a train, and, again, the balls move in the same way. These are the manifest symmetries of the space we live in -- position and time translation, rotation, and velocity "boosts." The term "symmetry" in this context may not at first glance seem like the same concept as, say, a snowflake's symmetry, but it precisely is. We just have to be like mathematicians and be very careful about definitions. Why should we take so much care about defining the elements of symmetry? The answer is that, as we go farther in understanding fundamental physics, the abstractions we use from the math of symmetry are well understood, while the concrete objects those abstractions describe are elusive. We will become lost in a morass of abstract vocabulary if we do not have concrete examples to anchor our understanding.

### Discrete symmetries
Consider a triangle.

![](diagrams/symmetry-triangle.svg)

An equilateral triangle.

We can see its obvious symmetry. To categorize its symmetry we can write down all the actions that leave the it unchanged. These are:
1. Do nothing
2. Rotate 120°
3. Rotate 240°
4. Flip along an axix
5. Flip then rotate 120°
6. Flip then rotate 240°

![Triangle symmetry actions animation contact sheet](animations/symmetry-triangle-actions-contact-sheet.png)

[Open MP4: symmetry-triangle-actions.mp4](animations/symmetry-triangle-actions.mp4)

We say the triangle "belongs to the $D_3$ symmetry **group**." The group is more general than the triangle itself. Any number of object possess $D_3$ symmetry.

![](diagrams/symmetry-d3-carriers.svg)

#### Representations
What if we now want to track what a sequence of symmetry actions does to an object carrying the symmetry? For example, suppose we label the vertices \(A, B, C\) and ask, if we rotate twice, flip once, then rotate again, where is vertex \(A\) sent? Recognizing that the triangle's state has three ordered components, we might guess that we could represent the triangle as a three-dimensional vector, and we might then represent the 120° rotations as **transformations** on the vector space that permute the vertices in ways allowed by the symmetry group actions. Since the transformation that takes one vertex into another must also move the edges and interior of the triangle in a uniform way, the transformation must be linear, which means that it can be represented by matrix multiplication. We then say that a **representation** of a group is a vector space in which matrix multiplication composes in a way that mirrors the way group actions compose on a symmetric object.

To construct a 3 dimensional representation of $D_3$, we map the 3 vertices to elements of vector.

![](diagrams/symmetry-d3-vertices-to-vector.svg)

What numerical values to we put in for the vector? The answer is, it does not matter. What matters is only that the our transformation matrix permutes them properly. \(Notice that in this contruction, a transformation of $\begin{pmatrix}0\\0\\0\end{pmatrix}$ is just $\begin{pmatrix}0\\0\\0\end{pmatrix}$, ensuring the property that the origin remains fixed by linear transformations.\). We can represent rotation and flips, respectively with the following matrices:

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

We can see how this works in practice:

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

These actions have a nice and, as we will see in a moment, important visualization. Permutations that correspond to rotations of the triangle are 120 degree rotations about a diagonal axis in this vector space, while those that correspond to flips are flips about the plane that contains the diagonal axis.

![D3 rotations and flips in the 3D representation](animations/symmetry-d3-rotations-vs-flips-contact-sheet.png)

[Open MP4: symmetry-d3-rotations-vs-flips.mp4](animations/symmetry-d3-rotations-vs-flips.mp4)

Now, notice something about these visualizations. All the transformations leave a given vector in its own plane. Additionally, if we subtract off the average of the vectors, that is, if we move the point where the plane intersects the axis of rotation to the origin, we preserve the permutation structure of the transformations. We thus see that the $D_3$ symmetry is just as well represented as 120 degree rotations in the subspace of a 2-dimensional plane.

![D3 3D representation collapsing to the 2D plane](animations/symmetry-d3-irrep-collapse-contact-sheet.png)

[Open MP4: symmetry-d3-irrep-collapse.mp4](animations/symmetry-d3-irrep-collapse.mp4)

We also notice that vectors on the axis of rotation are taken by allowable transformations to themselves. Thus, just as any composition of transformations leaves the starting vector in a plane, for this subset of starting states, any composition leaves them on a line. A way to think of this is to allow the triangle's vertices to store some information, like a number or any numerical quantity. If the value they store is the same for all vertices, the symmetry actions have no effect, whereas if they are different, the actions permute those values in a way that can be represented in a 2-dimensional vector space. The 3-dimensional representation space we began with is thus decomposable into 2 subspaces. These cannot be decomposed further. That is, there is no lower-dimensional space such that an allowable transformation of any state remains in that space. The 1-dimensional and 2-dimensional representations are called **irreducible representations** or **irreps** for short. Why do we care about irreps? Because, in quantum physics, where states must carry the symmetry of nature, our models of those states are vectors in irreps. A "particle species," like an electron or photon, is an irrep of the symmetry, and the state of the particle -- what encodes our knowledge about its position, momentum, etc. -- is a vector in that representation space.

#### Invariants
Once we have chosen a representation for a symmetry, we might well ask, how do we know our transformations preserve the symmetry. If we look at a triangle and rotate by by 100 degrees we can "see" that doesn't preserve the symmetry. In a representation, we need some set of mathematical expressions that say "this transformation left the triange the same." We call these the **invariants** of the transformation. 

In our 2-dimensional irrep of $D_3$, we only need to check how a transformation acts on a single vector. The question "does the triangle overlay itself" becomes "is an arbitrary vector rotated by 120 degrees or flipped along a given axis." Let's pick a specific example to make this more concrete:

Rotation:
$$
\begin{bmatrix}
-2.2\\
-0.1
\end{bmatrix}
=
\begin{bmatrix}
\cos(120^\circ) & -\sin(120^\circ)\\
\sin(120^\circ) & \cos(120^\circ)
\end{bmatrix}
\begin{bmatrix}
1\\
2
\end{bmatrix}
$$

Choosing the x axis, flip:
$$
\begin{bmatrix}
1\\
-2
\end{bmatrix}
=
\begin{bmatrix}
1 & 0\\
0 & -1
\end{bmatrix}
\begin{bmatrix}
1\\
2
\end{bmatrix}
$$

These transformations have two invariants. First, because they are a subclass of rotations and flips generally, they leave the distance to the origin unchanged:

\(r^2=x^2+y^2\)

Then, to limit rotations to 120 degrees and flips to those about the three axes implied by an equilateral triangle, we have an additional invariant:

\(u=x^3-3xy^2\)

It's not hard to show this is the case using the example transformations above, but in the interest of not boring the reader, we will skip it. 

When we move on to deal with symmetries we encounter in physics, the invariants typically turn out to be simpler than this because the symmetries are less restrictive. Specifically, the invariants we will use are variations on the distance invariant above. 

In physics, invariants do more than provide a way to check that a transformation represents an element of a group action. Physics is about finding equations of motion that all observers separated by a symmetry transformation, that is, observers at different places, times, orientations, or velocities, agree on. A way to find these equations, as we will see later, is to build them from invariant quantities of the symmetry action.
